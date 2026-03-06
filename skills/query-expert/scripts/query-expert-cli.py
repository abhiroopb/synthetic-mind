#!/usr/bin/env python3
"""Query Expert CLI - standalone data discovery and SQL query tool.

Provides a JSON-based interface to:
  - Semantic search of historical queries (Databricks vector search)
  - Table metadata discovery
  - SQL execution on Snowflake (Okta SSO via externalbrowser)
  - Brand/domain knowledge browsing
  - Table permission checking
  - Block Metric Store search

Zero dependency on the mcp_query_expert package.
"""
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "databricks-sdk>=0.55.0",
#     "snowflake-connector-python[secure-local-storage]>=3.12.0",
#     "pyyaml>=6.0",
# ]
# ///

import argparse
import getpass
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# ---------------------------------------------------------------------------
# Databricks vector search indexes (hardcoded from search_indexes.yaml)
# ---------------------------------------------------------------------------
SEARCH_INDEXES = {
    "query_expert_v2.0.0": {
        "index_name": "add_ons_data.mcp_query_expert_vector_search.query_search_index_v2_0_0",
        "columns": [
            "query_id",
            "query_text",
            "user_name",
            "query_description",
            "tables_in_query",
            "query_source",
        ],
    },
    "table_meta_data_v3.0.0": {
        "index_name": "add_ons_data.mcp_query_expert_vector_search.table_metadata_search_index_v3_0_0",
        "columns": [
            "table_name",
            "table_database",
            "table_schema",
            "table_description",
            "column_schema",
            "table_verification_status",
            "total_users_recent",
            "brand",
            "table_type",
            "updated_by",
            "table_updated_at",
            "table_owners",
            "top_tables_joined",
            "top_table_users",
        ],
    },
    "metric_store_v2.0.0": {
        "index_name": "add_ons_data.mcp_query_expert_vector_search.block_metrics_store_index_v2_0_0",
        "columns": ["name", "description", "domain", "short_name", "label", "brand"],
    },
}

DATABRICKS_HOST = "https://block-lakehouse-production.cloud.databricks.com"

QUERY_SOURCE_RANKING = {
    "Looker": 1,
    "Mode": 1,
    "MCP Block Data - Metric Store": 0,
    "Query Expert: Labeled": 0,
    "Query Expert: Top User": 2,
}

TABLE_VERIFICATION_RANKING = {"VERIFIED": 0, "UNVERIFIED": 1}

VALID_BRANDS = ["Square", "Cash App", "Block", "Afterpay", "Tidal", "Bitkey"]
VALID_TABLE_TYPES = ["Analytics", "Production", "Event"]
VALID_QUERY_SOURCES = list(QUERY_SOURCE_RANKING.keys())

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def strip_none_values(data: Any) -> Any:
    """Recursively remove None values from dictionaries."""
    if isinstance(data, dict):
        return {k: strip_none_values(v) for k, v in data.items() if v is not None}
    elif isinstance(data, list):
        return [strip_none_values(item) for item in data]
    return data


def extract_table_names(query_text: str) -> Dict[str, List[str]]:
    """Extract source and join table names from SQL text."""
    def _extract(pattern):
        return list(
            {m.group(1).upper() for m in re.finditer(pattern, query_text, re.IGNORECASE) if m.group(1).count(".") >= 2}
        )
    return {
        "source_tables": _extract(r"\b(?:FROM)\s+([a-zA-Z0-9_.]+)"),
        "join_tables": _extract(r"\b(?:JOIN)\s+([a-zA-Z0-9_.]+)"),
    }


def build_filters(filters_to_add: Dict[str, Optional[str]]) -> Optional[str]:
    """Build Databricks vector search filter JSON string."""
    if not any(v for v in filters_to_add.values()):
        return None
    parts = []
    for key, value in filters_to_add.items():
        if not value:
            continue
        if "," in value and key != "tables_in_query":
            formatted = str([x.strip() for x in value.split(",")])
        else:
            formatted = f'"{value.strip()}"'
        parts.append(f'"{key}" : {formatted}')
    result = "{" + ", ".join(parts) + "}"
    return result.replace("'", '"')


def validate_input(input_type: str, input_value: Optional[str]) -> Optional[str]:
    """Validate and normalize filter inputs."""
    if not input_value:
        return None

    validators = {
        "query_source": lambda v: [x.strip() for x in v.split(",") if x.strip() in VALID_QUERY_SOURCES],
        "table_names": lambda v: [x.upper().strip() for x in v.split(",") if x.count(".") == 2],
        "table_database": lambda v: [x.upper().strip() for x in v.split(",")],
        "table_schema": lambda v: [x.upper().strip() for x in v.split(",") if x.count(".") == 1],
        "user_names": lambda v: [x.strip().upper() for x in v.split(",")],
        "brand": lambda v: _validate_brand(v),
        "table_status": lambda v: [x.strip().upper() for x in v.split(",") if x.strip() in ["ACTIVE", "INACTIVE"]],
        "table_verification_status": lambda v: [x.strip().upper() for x in v.split(",") if x.strip() in ["VERIFIED", "UNVERIFIED"]],
        "table_type": lambda v: [x.strip() for x in v.split(",") if x.strip() in VALID_TABLE_TYPES],
    }

    fn = validators.get(input_type)
    if not fn:
        return None
    valid = fn(input_value)
    return ", ".join(valid) if valid else None


def _validate_brand(value: str) -> List[str]:
    valid = [x.strip() for x in value.split(",") if x.strip() in VALID_BRANDS]
    if valid and "Block" not in valid:
        valid.append("Block")
    return valid


def reranker(
    results: Dict,
    column_to_rerank: str,
    unique_id: str,
    sort_type: str = "ascending",
    ranking_priority: Optional[Dict] = None,
) -> Dict:
    """Re-rank search results by a priority column."""
    new_rank = {}
    for key in results:
        if ranking_priority is not None:
            new_rank[key] = ranking_priority.get(results[key].get(column_to_rerank), 2)
        else:
            new_rank[key] = results[key].get(column_to_rerank)

    if len(new_rank) != len(results):
        return results

    reverse = sort_type != "ascending"
    sorted_keys = sorted(new_rank, key=lambda k: new_rank[k] if new_rank[k] is not None else 0, reverse=reverse)

    updated = {}
    for i, key in enumerate(sorted_keys):
        updated[str(i)] = results[key]

    if len(updated) != len(results):
        return results
    try:
        assert all(updated[r].get(unique_id) is not None or True for r in updated)
    except Exception:
        return results
    return updated


def format_vector_results(results) -> Optional[Dict]:
    """Format Databricks vector search results into a dictionary."""
    try:
        column_names = [c.name for c in results.manifest.columns]
        data_array = results.result.data_array
        if not data_array:
            return None
        results_dict = {}
        for i, row in enumerate(data_array):
            entry = {}
            for col, val in zip(column_names, row):
                entry[col] = val
                if col == "query_text" and val:
                    tables = extract_table_names(val)
                    for table_type in tables:
                        entry[table_type] = ", ".join(tables.get(table_type, []))
            results_dict[str(i)] = entry
        return strip_none_values(results_dict)
    except Exception as e:
        raise ValueError(f"Failed to format results: {e}")


# ---------------------------------------------------------------------------
# Databricks client
# ---------------------------------------------------------------------------

_db_client = None


def get_databricks_client():
    """Get or create a Databricks WorkspaceClient."""
    global _db_client
    if _db_client is not None:
        return _db_client

    try:
        from databricks.sdk import WorkspaceClient
    except ImportError:
        print(json.dumps({
            "success": False,
            "error": "databricks-sdk not installed",
            "suggestion": "Run with: uv run scripts/query-expert-cli.py"
        }), file=sys.stderr)
        sys.exit(1)

    token = os.getenv("QUERY_EXPERT_DATABRICKS_TOKEN")
    _db_client = WorkspaceClient(
        host=os.getenv("DATABRICKS_HOST", DATABRICKS_HOST),
        token=token,
        auth_type="external-browser" if not token else None,
    )
    return _db_client


# ---------------------------------------------------------------------------
# Snowflake connection (direct, like snowflake-cli.py)
# ---------------------------------------------------------------------------


def get_snowflake_connection(
    database: Optional[str] = None,
    schema: Optional[str] = None,
    warehouse: Optional[str] = None,
    role: Optional[str] = None,
):
    """Get authenticated Snowflake connection with Okta SSO."""
    try:
        import snowflake.connector
    except ImportError:
        print(json.dumps({
            "success": False,
            "error": "snowflake-connector-python not installed",
            "suggestion": "Run with: uv run scripts/query-expert-cli.py"
        }), file=sys.stderr)
        sys.exit(1)

    user = os.getenv("SNOWFLAKE_USER") or f"{getpass.getuser()}@squareup.com"

    conn_params = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT", "squareinc-square"),
        "user": user,
        "authenticator": "externalbrowser",
        "warehouse": warehouse or os.getenv("SNOWFLAKE_WAREHOUSE", "ADHOC__LARGE"),
        "database": database or os.getenv("SNOWFLAKE_DATABASE", "ANALYTICS"),
        "schema": schema or os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC"),
    }
    if role or os.getenv("SNOWFLAKE_ROLE"):
        conn_params["role"] = role or os.getenv("SNOWFLAKE_ROLE", "ANALYST")

    return snowflake.connector.connect(**conn_params)


def generate_snowflake_query_link(query_id: Optional[str]) -> Optional[str]:
    if not query_id:
        return None
    return f"https://app.snowflake.com/squareinc/square/#/compute/history/queries/{query_id}/detail"


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_search(
    search_text: str,
    user_name: Optional[str] = None,
    table_names: Optional[str] = None,
    query_source: Optional[str] = None,
    limit: int = 5,
) -> Dict[str, Any]:
    """Semantic search of historical queries."""
    if not search_text:
        return {"success": False, "error": "search_text is required"}

    idx = SEARCH_INDEXES["query_expert_v2.0.0"]

    query_source_ = validate_input("query_source", query_source)
    table_names_ = validate_input("table_names", table_names)
    user_names_ = validate_input("user_names", user_name)

    effective_search = search_text
    if table_names_ and "," in table_names_:
        parts = [t.strip() for t in table_names_.split(",")]
        effective_search = f"{search_text} {' JOIN '.join(parts)}"
        parts.sort()
        table_names_ = ", ".join(parts)

    filters = build_filters({
        "user_name": user_names_,
        "tables_in_query": table_names_,
        "query_source": query_source_,
    })

    client = get_databricks_client()
    results = client.vector_search_indexes.query_index(
        index_name=idx["index_name"],
        query_text=effective_search,
        columns=idx["columns"],
        num_results=limit,
        filters_json=filters,
        score_threshold=0.40,
    )

    formatted = format_vector_results(results)
    if not formatted:
        return {"success": False, "error": "No matching queries found. Try different search terms or increase the limit."}

    if "query_source" in idx["columns"] and "query_text" in idx["columns"]:
        formatted = reranker(
            results=formatted,
            unique_id="query_id",
            column_to_rerank="query_source",
            ranking_priority=QUERY_SOURCE_RANKING,
            sort_type="ascending",
        )

    return {"success": True, "results": formatted}


def cmd_tables(
    search_text: str,
    table_name: Optional[str] = None,
    domain: Optional[str] = None,
    sub_domain: Optional[str] = None,
    table_owner: Optional[str] = None,
    table_verification_status: Optional[str] = "VERIFIED, UNVERIFIED",
    brand: Optional[str] = None,
    table_database: Optional[str] = None,
    table_schema: Optional[str] = None,
    table_type: Optional[str] = None,
    limit: int = 5,
) -> Dict[str, Any]:
    """Discover table metadata via semantic search."""
    if not search_text:
        return {"success": False, "error": "search_text is required"}

    idx = SEARCH_INDEXES["table_meta_data_v3.0.0"]

    table_names_ = validate_input("table_names", table_name)
    table_owner_ = validate_input("user_names", table_owner)
    if table_owner_ and "," in table_owner_:
        table_owner_ = table_owner_.split(",")[0]
    verification_ = validate_input("table_verification_status", table_verification_status)
    brand_ = validate_input("brand", brand)
    schema_ = validate_input("table_schema", table_schema)
    database_ = validate_input("table_database", table_database)
    type_ = validate_input("table_type", table_type)

    filters_map = {
        "table_name": table_names_,
        "data_domain": domain,
        "sub_domain": sub_domain,
        "table_owners": table_owner_,
        "table_verification_status": verification_,
        "brand": brand_,
        "table_schema": schema_,
        "table_database": database_,
        "table_type": type_,
    }

    if table_names_:
        score_threshold = 0
        for k in filters_map:
            if k != "table_name":
                filters_map[k] = None
    elif table_owner_:
        score_threshold = 0.25
    else:
        score_threshold = 0.4

    filters = build_filters(filters_map)

    client = get_databricks_client()
    results = client.vector_search_indexes.query_index(
        index_name=idx["index_name"],
        query_text=search_text,
        columns=idx["columns"],
        num_results=limit,
        filters_json=filters,
        score_threshold=score_threshold,
    )

    formatted = format_vector_results(results)
    if not formatted:
        return {"success": False, "error": "No matching tables found. Try different search terms."}

    formatted = reranker(
        results=formatted,
        unique_id="table_name",
        sort_type="descending",
        column_to_rerank="total_users_recent",
        ranking_priority=None,
    )
    formatted = reranker(
        results=formatted,
        unique_id="table_name",
        sort_type="ascending",
        column_to_rerank="table_verification_status",
        ranking_priority=TABLE_VERIFICATION_RANKING,
    )

    return {"success": True, "results": formatted}


def cmd_execute(
    sql: str,
    database: Optional[str] = None,
    schema: Optional[str] = None,
    warehouse: Optional[str] = None,
    role: Optional[str] = None,
    limit: Optional[int] = None,
) -> Dict[str, Any]:
    """Execute a SQL query on Snowflake."""
    if not sql:
        return {"success": False, "error": "SQL query is required"}

    from snowflake.connector import DictCursor

    conn = get_snowflake_connection(database, schema, warehouse, role)
    try:
        cur = conn.cursor(DictCursor)

        if limit is not None:
            if not isinstance(limit, int) or limit <= 0:
                return {"success": False, "error": f"Limit must be a positive integer, got: {limit}"}
            if "LIMIT" not in sql.upper():
                sql = f"{sql.rstrip(';')} LIMIT {int(limit)}"

        cur.execute(sql)

        query_id = cur.sfqid

        if cur.description:
            rows = cur.fetchall()
            return {
                "success": True,
                "row_count": len(rows),
                "rows": rows,
                "snowflake_query_link": generate_snowflake_query_link(query_id),
            }
        else:
            return {
                "success": True,
                "message": "Query executed successfully (no results returned)",
                "snowflake_query_link": generate_snowflake_query_link(query_id),
            }
    except Exception as e:
        return {"success": False, "error": str(e), "error_type": type(e).__name__}
    finally:
        conn.close()


def cmd_permissions(
    tables: List[str],
    role: Optional[str] = None,
) -> Dict[str, Any]:
    """Check access permissions for a list of tables."""
    if not tables:
        return {"success": False, "error": "At least one table is required"}

    accessible = []
    inaccessible = []

    conn = get_snowflake_connection(role=role)
    try:
        cur = conn.cursor()
        for table in tables:
            parts = table.strip().split(".")
            if len(parts) != 3:
                inaccessible.append({
                    "table": table,
                    "error": "Invalid format. Must be DATABASE.SCHEMA.TABLE",
                    "access_url": None,
                })
                continue
            try:
                cur.execute(f"SELECT 1 FROM {table} LIMIT 0")
                accessible.append(table)
            except Exception as e:
                error_msg = str(e).lower()
                db_name = parts[0].lower()
                app_name = db_name.replace("_", "-")
                access_url = None
                if "does not exist or not authorized" in error_msg:
                    access_url = f"https://registry.sqprod.co/groups/{app_name}--snowflake__read_only"
                inaccessible.append({
                    "table": table,
                    "database": parts[0],
                    "error": str(e),
                    "access_url": access_url,
                })
    finally:
        conn.close()

    summary = f"Access check complete: {len(accessible)} accessible, {len(inaccessible)} inaccessible out of {len(tables)} tables."
    return {
        "success": True,
        "accessible_tables": accessible,
        "inaccessible_tables": inaccessible,
        "total_checked": len(tables),
        "access_summary": summary,
    }


def cmd_knowledge(
    knowledge_dir: str,
    brand: Optional[str] = None,
    domain: Optional[str] = None,
    subdomain: Optional[str] = None,
    scope_area: Optional[str] = None,
    relevant_files: Optional[str] = None,
) -> Dict[str, Any]:
    """Discover or load brand/domain knowledge files."""
    base = Path(knowledge_dir)
    if not base.exists():
        return {"success": False, "error": f"Knowledge directory not found: {knowledge_dir}"}

    # Listing mode
    if not brand and not domain:
        result = {"brands": {}, "domains": {}}

        brands_path = base / "brands"
        if brands_path.exists():
            for bp in sorted(brands_path.iterdir()):
                if bp.is_dir() and not bp.name.startswith("."):
                    result["brands"][bp.name] = {
                        "files": sorted(f.name for f in bp.iterdir() if f.is_file() and not f.name.startswith("."))
                    }

        domains_path = base / "domains"
        if domains_path.exists():
            for dp in sorted(domains_path.iterdir()):
                if dp.is_dir() and not dp.name.startswith("."):
                    dinfo = {"files": [], "subdomains": {}}
                    for item in dp.iterdir():
                        if item.is_file() and not item.name.startswith("."):
                            dinfo["files"].append(item.name)
                    dinfo["files"].sort()
                    for sdp in dp.iterdir():
                        if sdp.is_dir() and not sdp.name.startswith("."):
                            sinfo = {"files": sorted(f.name for f in sdp.iterdir() if f.is_file() and not f.name.startswith(".")), "scope_areas": {}}
                            for sap in sdp.iterdir():
                                if sap.is_dir() and not sap.name.startswith("."):
                                    sinfo["scope_areas"][sap.name] = {
                                        "files": sorted(f.name for f in sap.iterdir() if f.is_file() and not f.name.startswith("."))
                                    }
                            dinfo["subdomains"][sdp.name] = sinfo
                    result["domains"][dp.name] = dinfo

        return {"success": True, "results": result}

    if brand and domain:
        return {"success": False, "error": "Specify either --brand or --domain, not both."}

    # Resolve target directory
    if brand:
        brand = brand.lower().strip().replace(" ", "_").replace("-", "_")
        target = base / "brands" / brand
        label = f"brand '{brand}'"
    else:
        domain = domain.lower().strip().replace(" ", "_").replace("-", "_")
        components = [domain]
        if subdomain:
            components.append(subdomain.lower().strip().replace(" ", "_").replace("-", "_"))
        if scope_area:
            if not subdomain:
                return {"success": False, "error": "subdomain required when scope_area is specified"}
            components.append(scope_area.lower().strip().replace(" ", "_").replace("-", "_"))
        target = base / "domains"
        for c in components:
            # Prevent path traversal
            if ".." in c or "/" in c or "\\" in c:
                return {"success": False, "error": f"Invalid path component: {c}"}
            target = target / c
        label = f"domain '{'/'.join(components)}'"

    if not target.exists():
        return {"success": False, "error": f"Path not found for {label}: {target}"}

    # Determine files to load
    if relevant_files:
        file_list = [f.strip() for f in relevant_files.split(",") if f.strip()]
    else:
        file_list = [f.name for f in target.iterdir() if f.is_file() and not f.name.startswith(".")]

    if not file_list:
        return {"success": False, "error": f"No files found in {label}"}

    loaded = {}
    for fname in sorted(file_list):
        if ".." in fname or "/" in fname or "\\" in fname:
            return {"success": False, "error": f"Invalid filename: {fname}"}
        fpath = target / fname
        if not fpath.exists():
            available = [f.name for f in target.iterdir() if f.is_file() and not f.name.startswith(".")]
            return {"success": False, "error": f"File '{fname}' not found in {label}. Available: {sorted(available)}"}
        try:
            text = fpath.read_text(encoding="utf-8")
            if fpath.suffix == ".json":
                loaded[fname] = json.loads(text)
            else:
                loaded[fname] = text
        except Exception as e:
            return {"success": False, "error": f"Error reading '{fname}': {e}"}

    return {"success": True, "results": loaded}


def cmd_metrics(
    search_text: str,
    brand: Optional[str] = None,
    domains: Optional[str] = None,
    metric_name: Optional[str] = None,
    cut_off: str = ".5",
) -> Dict[str, Any]:
    """Search the Block Metric Store."""
    if not search_text:
        return {"success": False, "error": "search_text is required"}

    idx = SEARCH_INDEXES["metric_store_v2.0.0"]

    brand_ = validate_input("brand", brand) if brand else None
    filters_map = {"name": metric_name, "brand": brand_}
    if domains and "domain" in idx["columns"]:
        filters_map["domain"] = domains
    filters = build_filters(filters_map)

    threshold = 0 if metric_name else float(cut_off)

    client = get_databricks_client()
    results = client.vector_search_indexes.query_index(
        index_name=idx["index_name"],
        query_text=search_text,
        columns=idx["columns"],
        score_threshold=threshold,
        num_results=5,
        filters_json=filters,
    )

    formatted = format_vector_results(results)
    if not formatted:
        return {"success": True, "results": {"use_block_metric_store": False, "top_metrics": "None Found"}}

    top_metrics = ""
    for i, key in enumerate(formatted):
        entry = formatted[key]
        name = entry.get("name", "")
        desc = entry.get("description", "No Description").strip().replace("\n", " ").replace("..", ".")
        top_metrics += f"{i + 1}. {name} | {desc}\n"

    return {
        "success": True,
        "results": {
            "use_block_metric_store": True,
            "user_choice_required": len(formatted) > 1,
            "top_metrics": top_metrics.strip(),
        },
    }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def _default_knowledge_dir() -> str:
    """Try to locate the knowledge directory relative to common project layouts."""
    candidates = [
        Path(__file__).parent.parent / "knowledge",
        Path(__file__).parent / "knowledge",
        Path.cwd() / "knowledge",
        Path.cwd() / "src" / "mcp_query_expert" / "knowledge",
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    return str(candidates[0])


def main():
    parser = argparse.ArgumentParser(
        description="Query Expert CLI - Discover tables, data experts and write SQL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s search --text "revenue by merchant last month"
  %(prog)s search --text "GPV by seller" --user-name PAZAR --limit 10
  %(prog)s tables --text "payment transactions" --brand "Square"
  %(prog)s tables --text "timecards" --table-name "APP_PAYROLL.APP_PAYROLL.TIMECARDS"
  %(prog)s execute --sql "SELECT CURRENT_USER() as user, CURRENT_ROLE() as role"
  %(prog)s execute --sql "SELECT * FROM ANALYTICS.PUBLIC.MY_TABLE" --limit 10
  %(prog)s knowledge
  %(prog)s knowledge --brand square --files "context.txt,glossary.json"
  %(prog)s permissions --tables ANALYTICS.PUBLIC.TABLE1 APP_BI.HEXAGON.TABLE2
  %(prog)s metrics --text "total GPV" --brand "Square"

Environment variables:
  QUERY_EXPERT_DATABRICKS_TOKEN   Databricks PAT (falls back to browser SSO)
  DATABRICKS_HOST                 Databricks workspace URL
  SNOWFLAKE_USER                  Snowflake username (default: $USER@squareup.com)
  SNOWFLAKE_ACCOUNT               Snowflake account (default: squareinc-square)
  SNOWFLAKE_WAREHOUSE             Default warehouse (default: ADHOC__LARGE)
  SNOWFLAKE_DATABASE              Default database (default: ANALYTICS)
  SNOWFLAKE_SCHEMA                Default schema (default: PUBLIC)
  SNOWFLAKE_ROLE                  Default role (default: ANALYST)
  QUERY_EXPERT_KNOWLEDGE_DIR      Path to knowledge directory
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # --- search ---
    sp = subparsers.add_parser("search", help="Semantic search of historical queries")
    sp.add_argument("--text", required=True, help="Question or query to search for")
    sp.add_argument("--user-name", help="Filter by LDAP username")
    sp.add_argument("--table-names", help="Comma-delimited table names (validates JOIN patterns)")
    sp.add_argument("--query-source", help="Filter: Looker, Mode, Query Expert: Top User, Query Expert: Labeled")
    sp.add_argument("--limit", type=int, default=5, help="Max results (default: 5)")

    # --- tables ---
    sp = subparsers.add_parser("tables", help="Discover table metadata")
    sp.add_argument("--text", required=True, help="Semantic search query")
    sp.add_argument("--table-name", help="Full table name (DATABASE.SCHEMA.TABLE)")
    sp.add_argument("--domain", help="Data domain filter")
    sp.add_argument("--sub-domain", help="Sub-domain filter")
    sp.add_argument("--table-owner", help="Filter by owner LDAP")
    sp.add_argument("--verification-status", default="VERIFIED, UNVERIFIED", help="VERIFIED, UNVERIFIED, or both")
    sp.add_argument("--brand", help="Brand: Square, Cash App, Afterpay, Tidal, Bitkey, Block")
    sp.add_argument("--table-database", help="Filter by database")
    sp.add_argument("--table-schema", help="Filter by schema (DATABASE.SCHEMA)")
    sp.add_argument("--table-type", help="Filter: Analytics, Production, Event")
    sp.add_argument("--limit", type=int, default=5, help="Max results (default: 5)")

    # --- execute ---
    sp = subparsers.add_parser("execute", help="Execute SQL query on Snowflake")
    sp.add_argument("--sql", required=True, help="SQL query to execute")
    sp.add_argument("--database", help="Database override")
    sp.add_argument("--schema", help="Schema override")
    sp.add_argument("--warehouse", help="Warehouse override")
    sp.add_argument("--role", help="Role override")
    sp.add_argument("--limit", type=int, help="Limit number of results")

    # --- permissions ---
    sp = subparsers.add_parser("permissions", help="Check table access permissions")
    sp.add_argument("--tables", nargs="+", required=True, help="Tables in DATABASE.SCHEMA.TABLE format")
    sp.add_argument("--role", help="Role override")

    # --- knowledge ---
    sp = subparsers.add_parser("knowledge", help="Discover or load brand/domain knowledge")
    sp.add_argument("--brand", help="Brand: square, cash_app, afterpay")
    sp.add_argument("--domain", help="Domain: product, financial")
    sp.add_argument("--subdomain", help="Subdomain within domain")
    sp.add_argument("--scope-area", help="Scope area within subdomain")
    sp.add_argument("--files", help="Comma-delimited filenames to load")
    sp.add_argument("--knowledge-dir", default=os.getenv("QUERY_EXPERT_KNOWLEDGE_DIR", _default_knowledge_dir()), help="Path to knowledge directory")

    # --- metrics ---
    sp = subparsers.add_parser("metrics", help="Search the Block Metric Store")
    sp.add_argument("--text", required=True, help="Search query for metrics")
    sp.add_argument("--brand", help="Brand filter")
    sp.add_argument("--domains", help="Metric domain filter")
    sp.add_argument("--metric-name", help="Specific metric name")
    sp.add_argument("--cut-off", default=".5", help="Similarity threshold (default: 0.5)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "search":
            result = cmd_search(
                search_text=args.text,
                user_name=args.user_name,
                table_names=args.table_names,
                query_source=args.query_source,
                limit=args.limit,
            )
        elif args.command == "tables":
            result = cmd_tables(
                search_text=args.text,
                table_name=args.table_name,
                domain=args.domain,
                sub_domain=args.sub_domain,
                table_owner=args.table_owner,
                table_verification_status=args.verification_status,
                brand=args.brand,
                table_database=args.table_database,
                table_schema=args.table_schema,
                table_type=args.table_type,
                limit=args.limit,
            )
        elif args.command == "execute":
            result = cmd_execute(
                sql=args.sql,
                database=args.database,
                schema=args.schema,
                warehouse=args.warehouse,
                role=args.role,
                limit=args.limit,
            )
        elif args.command == "permissions":
            result = cmd_permissions(tables=args.tables, role=args.role)
        elif args.command == "knowledge":
            result = cmd_knowledge(
                knowledge_dir=args.knowledge_dir,
                brand=args.brand,
                domain=args.domain,
                subdomain=args.subdomain,
                scope_area=args.scope_area,
                relevant_files=args.files,
            )
        elif args.command == "metrics":
            result = cmd_metrics(
                search_text=args.text,
                brand=args.brand,
                domains=args.domains,
                metric_name=args.metric_name,
                cut_off=args.cut_off,
            )
        else:
            result = {"success": False, "error": f"Unknown command: {args.command}"}

        print(json.dumps(result, indent=2, default=str))
        sys.exit(0 if result.get("success", False) else 1)

    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
