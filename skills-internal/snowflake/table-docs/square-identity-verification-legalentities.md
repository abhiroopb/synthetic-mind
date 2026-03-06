# Brand A Identity Verification — LEGALENTITIES

Query and analyze legal entity structure and verification data from the LEGALENTITIES Snowflake database, owned by the Business Identities team in the Identity Organization at Brand A.

## Overview

The LEGALENTITIES database manages structured representations of businesses and individuals for compliance purposes:

- **Legal entity structures**: Hierarchical structures linking businesses to individuals (owners, officers, beneficial owners)
- **Verification decisions**: Automated verification of entity identity at both structure and node levels
- **Entity data management**: Current and historical data for businesses and individuals

LEGALENTITIES is linked to ONBOARD via `STRUCTURE_TOKEN` — see `square-identity-verification-onboard.md` for ONBOARD tables.

For ROSTER merchant/unit token lookups, see `roster-merchant-location-employee-lookups.md`.

---

## Tables

### Legal Entity Structure

#### LEGALENTITIES.RAW_OLTP.STRUCTURE_MERCHANT

Maps legal entity structures to merchants. The key lookup table for going from customer_id to a legal entity structure.

**Key Fields:**
- `STRUCTURE_TOKEN` (TEXT) — FK → all LEGALENTITIES tables with STRUCTURE_TOKEN
- `CUSTOMER_ID` (TEXT) — Merchant token (TEXT, not BINARY like ROSTER)
- `PRODUCT` (TEXT) — Product context
- `PURPOSE` (TEXT) — Purpose of the structure
- `CREATED_AT` (TIMESTAMP_NTZ)
- `UPDATED_AT` (TIMESTAMP_NTZ)

#### LEGALENTITIES.RAW_OLTP.STRUCTURE_SNAPSHOTS

Versioned snapshots of legal entity structures. Each revision captures the full structure state.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `TOKEN` (TEXT) — Structure token
- `REVISION` (NUMBER) — Revision number
- `CLIENT_SERVICE` (TEXT) — Service that created the snapshot
- `CUSTOMER_ID` (TEXT) — Merchant token
- `PRODUCT` (TEXT) — Product context
- `ENCRYPTED_DATA` (BINARY) — Encrypted structure data (not directly queryable)
- `CREATED_AT` (TIMESTAMP_NTZ)

#### LEGALENTITIES.RAW_OLTP.STRUCTURE_CHANGES

Feed of structure change events. Used for event-driven processing when structures are modified.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `FEED_SYNC_ID` (NUMBER) — Feed sync ID
- `SHARD` (NUMBER) — Shard number
- `STRUCTURE_TOKEN` (TEXT) — Structure that changed
- `STRUCTURE_VERSION` (NUMBER) — New version number
- `TYPE` (TEXT) — Type of change
- `CREATED_AT` (TIMESTAMP_NTZ)

#### LEGALENTITIES.RAW_OLTP.INDIVIDUAL_LEGAL_ENTITY

Individual (person) legal entity records. Minimal record — detailed data is in `LES_INDIVIDUAL_DATA`.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `STRUCTURE_TOKEN` (TEXT) — FK → structure
- `STRUCTURE_VERSION` (NUMBER) — Structure version
- `CREATED_AT` (TIMESTAMP_NTZ)

#### LEGALENTITIES.RAW_OLTP.BUSINESS_LEGAL_ENTITY

Business legal entity records with country-specific identifiers.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `STRUCTURE_TOKEN` (TEXT) — FK → structure
- `STRUCTURE_VERSION` (NUMBER) — Structure version
- `PHONE_CALLING_CODE` (TEXT) — Phone calling code
- `US_EIN_LAST_FOUR` (TEXT) — Last 4 digits of US EIN
- `AU_ABN` (TEXT) — Australian Business Number
- `AU_ACN` (TEXT) — Australian Company Number
- `CA_CRA_BUSINESS_NUMBER` (TEXT) — Canadian CRA business number
- `GB_CHRN` (TEXT) — UK Company House Registration Number
- `JP_KANJI_NAME` (TEXT) — Japanese kanji name
- `JP_KATAKANA_NAME` (TEXT) — Japanese katakana name
- `CREATED_AT` (TIMESTAMP_NTZ)

---

### Entity Data (Current + History)

These tables store current entity data. Each has a corresponding `*_HISTORY` table with identical columns that tracks all historical versions.

#### LEGALENTITIES.RAW_OLTP.LES_BUSINESS_DATA

Current business data for legal entity nodes.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `NODE_TOKEN` (TEXT) — Legal entity node token
- `LEGAL_NAME` (TEXT) — Legal business name
- `DBA_NAME` (TEXT) — Doing Business As name
- `PHONE_CALLING_CODE` (TEXT), `PHONE_NUMBER` (TEXT) — Phone
- `ADDRESS_LINE_1` (TEXT), `CITY` (TEXT), `ADMIN_LEVEL_1` (TEXT), `COUNTRY` (TEXT), `POSTAL_CODE` (TEXT) — Address
- `IS_ROOT` (NUMBER) — Whether this is the root business node
- `STRUCTURE_TOKEN` (TEXT) — FK → structure
- `STRUCTURE_VERSION` (NUMBER) — Structure version
- `UPDATED_AT` (TIMESTAMP_NTZ)

**History table:** `LEGALENTITIES.RAW_OLTP.LES_BUSINESS_DATA_HISTORY` — same columns, tracks all versions.

#### LEGALENTITIES.RAW_OLTP.LES_INDIVIDUAL_DATA

Current individual (person) data for legal entity nodes.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `NODE_TOKEN` (TEXT) — Legal entity node token
- `GIVEN_NAME` (TEXT) — First name
- `MIDDLE_NAME` (TEXT) — Middle name
- `FAMILY_NAME` (TEXT) — Last name
- `BIRTH_DATE_YMD` (TEXT) — Date of birth (YYYY-MM-DD format)
- `EMAIL` (TEXT) — Email address
- `PHONE_CALLING_CODE` (TEXT), `PHONE_NUMBER` (TEXT) — Phone
- `ADDRESS_LINE_1` (TEXT), `CITY` (TEXT), `ADMIN_LEVEL_1` (TEXT), `COUNTRY` (TEXT), `POSTAL_CODE` (TEXT) — Address
- `STRUCTURE_TOKEN` (TEXT) — FK → structure
- `STRUCTURE_VERSION` (NUMBER) — Structure version
- `UPDATED_AT` (TIMESTAMP_NTZ)

**History table:** `LEGALENTITIES.RAW_OLTP.LES_INDIVIDUAL_DATA_HISTORY` — same columns, tracks all versions.

#### LEGALENTITIES.RAW_OLTP.LES_NODE_IDENTIFIER

Identifiers associated with legal entity nodes (e.g., SSN, EIN, tax IDs).

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `NODE_TYPE` (TEXT) — Type of node (individual, business)
- `NODE_TOKEN` (TEXT) — Legal entity node token
- `IDENTIFIER_TYPE` (TEXT) — Type of identifier (e.g., SSN, EIN)
- `VALUE` (TEXT) — Identifier value (may be encrypted/tokenized)
- `STRUCTURE_TOKEN` (TEXT) — FK → structure
- `STRUCTURE_VERSION` (NUMBER)

**History table:** `LEGALENTITIES.RAW_OLTP.LES_NODE_IDENTIFIER_HISTORY` — same columns, tracks all versions.

#### LEGALENTITIES.RAW_OLTP.LES_NODE_RELATIONSHIP

Relationships between legal entity nodes (e.g., individual is owner of business).

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `PARENT_NODE_TOKEN` (TEXT) — Parent node token (typically business)
- `CHILD_NODE_TOKEN` (TEXT) — Child node token (typically individual)
- `IS_PRIMARY` (NUMBER) — Whether this is the primary relationship
- `OWNERSHIP` (TEXT) — Ownership percentage or type
- `ROLE` (TEXT) — Role (e.g., owner, officer, beneficial_owner)
- `STRUCTURE_TOKEN` (TEXT) — FK → structure
- `STRUCTURE_VERSION` (NUMBER)

**History table:** `LEGALENTITIES.RAW_OLTP.LES_NODE_RELATIONSHIP_HISTORY` — same columns, tracks all versions.

---

### Verification

#### LEGALENTITIES.RAW_OLTP.VERIFICATION_REQUESTS

Verification request lifecycle for legal entity structures.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `STRUCTURE_TOKEN` (TEXT) — FK → structure
- `STRUCTURE_REVISION` (NUMBER) — Structure revision being verified
- `PRODUCT` (TEXT) — Product context
- `TIER` (TEXT) — Verification tier
- `STATE` (TEXT) — Request state
- `EXCLUDED` (NUMBER) — Whether excluded from verification
- `DECISION_SEQUENCE_NUMBER` (NUMBER) — Decision sequence number
- `CONTINUATION` (NUMBER) — Whether this is a continuation of a previous request
- `CREATED_AT` (TIMESTAMP_NTZ)

#### LEGALENTITIES.RAW_OLTP.VERIFICATION_DECISIONS

Verification decision outcomes for legal entity structures.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `STRUCTURE_TOKEN` (TEXT) — FK → structure
- `STRUCTURE_REVISION` (NUMBER) — Structure revision
- `PRODUCT` (TEXT) — Product context
- `STATUS` (TEXT) — Decision status
- `REASON` (TEXT) — Decision reason
- `SEQUENCE` (NUMBER) — Decision sequence number
- `CREATED_AT` (TIMESTAMP_NTZ)

#### LEGALENTITIES.RAW_OLTP.VERIFICATION_ATTEMPTS

Tracking individual verification attempts.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `FEED_SYNC_ID` (NUMBER), `SHARD` (NUMBER)
- `VERIFICATION_REQUEST_ID` (NUMBER) — FK → `VERIFICATION_REQUESTS.ID`
- `STRUCTURE_TOKEN` (TEXT) — FK → structure
- `CREATED_AT` (TIMESTAMP_NTZ)

#### LEGALENTITIES.RAW_OLTP.VERIFICATION_STATUS_CHANGES

Feed of verification status change events.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `FEED_SYNC_ID` (NUMBER), `SHARD` (NUMBER)
- `STRUCTURE_TOKEN` (TEXT) — FK → structure
- `PRODUCT` (TEXT) — Product context
- `CREATED_AT` (TIMESTAMP_NTZ)

#### LEGALENTITIES.RAW_OLTP.NODE_VERIFICATION_DECISIONS

Per-node verification decisions within a legal entity structure. More granular than structure-level `VERIFICATION_DECISIONS`.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `NODE_TOKEN` (TEXT) — Legal entity node being verified
- `STRUCTURE_TOKEN` (TEXT) — FK → structure
- `STRUCTURE_REVISION` (NUMBER)
- `PRODUCT` (TEXT) — Product context
- `ROLE` (TEXT) — Node's role in the structure
- `OWNERSHIP` (TEXT) — Node's ownership
- `IS_PRIMARY_INDIVIDUAL` (BOOLEAN) — Whether primary individual
- `DECISION` (TEXT) — Verification decision for this node
- `IDENTITYVERIFIER_VERIFICATION_ID` (TEXT) — Identity verifier reference
- `IDMATCH_POLL_TOKEN` (TEXT) — IDMatch poll token
- `SEQUENCE` (NUMBER) — Decision sequence
- `CREATED_AT` (TIMESTAMP_NTZ)

#### LEGALENTITIES.RAW_OLTP.NODE_VERIFICATION_DECISION_REASONS

Reason codes for node-level verification decisions.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `NODE_TOKEN` (TEXT), `STRUCTURE_TOKEN` (TEXT), `STRUCTURE_REVISION` (NUMBER)
- `PRODUCT` (TEXT), `SEQUENCE` (NUMBER)
- `CODE` (TEXT) — Reason code
- `COMMENT` (TEXT) — Reason comment

---

### Other

#### LEGALENTITIES.RAW_OLTP.CUSTOMER_IDENTIFIERS

Maps personal and business identifiers within a structure.

**Key Fields:**
- `ID` (NUMBER), `VERSION` (NUMBER), `STRUCTURE_TOKEN` (TEXT)
- `PERSONAL_ID` (TEXT), `BUSINESS_ID` (TEXT)
- `PERSONAL_ID_DESCRIPTION` (TEXT), `BUSINESS_ID_DESCRIPTION` (TEXT)

#### LEGALENTITIES.RAW_OLTP.DOC_IDV_EVENTS

Document identity verification event feed.

**Key Fields:**
- `ID` (NUMBER), `FEED_SYNC_ID` (NUMBER), `SHARD` (NUMBER)
- `STRUCTURE_TOKEN` (TEXT), `NODE_TOKEN` (TEXT)
- `CREATED_AT` (TIMESTAMP_NTZ)

#### LEGALENTITIES.RAW_OLTP.IDV_JOB_DATA_ENTRIES

Identity verification job data entries.

**Key Fields:**
- `ID` (NUMBER), `STRUCTURE_TOKEN` (TEXT), `STRUCTURE_REVISION` (NUMBER)
- `SOURCE` (TEXT), `PRODUCT` (TEXT), `REVISION` (NUMBER)

#### LEGALENTITIES.RAW_OLTP.POPULATE_STRUCTURE_REQUESTS

Requests to populate a legal entity structure from external sources.

**Key Fields:**
- `ID` (NUMBER), `STRUCTURE_TOKEN` (TEXT), `STRUCTURE_VERSION` (NUMBER)
- `PRODUCT_INTENT` (TEXT), `BUSINESS_IDENTITIFER` (TEXT) — (typo is in original schema)
- `POLL_TOKEN` (TEXT), `STATUS` (TEXT)
- `CREATED_AT` (TIMESTAMP_NTZ), `UPDATED_AT` (TIMESTAMP_NTZ)

#### LEGALENTITIES.RAW_OLTP.QUICK_VERIFY_SESSIONS

Quick verify session tracking for streamlined verification flows.

**Key Fields:**
- `ID` (NUMBER), `VERIFICATION_ID` (TEXT), `STRUCTURE_TOKEN` (TEXT)
- `CLONE_STRUCTURE_TOKEN` (TEXT), `PRODUCT` (TEXT), `STATUS` (TEXT)
- `FAILURE_REASON` (TEXT), `SSN_LAST4` (TEXT), `PHONE_NUMBER` (TEXT)
- `CREATED_AT` (TIMESTAMP_NTZ), `UPDATED_AT` (TIMESTAMP_NTZ)

#### LEGALENTITIES.RAW_OLTP.REDACTED_LEGAL_ENTITIES

Records of legal entities that have been redacted (e.g., for data privacy compliance).

**Key Fields:**
- `ID` (NUMBER), `STRUCTURE_TOKEN` (TEXT), `LEGAL_ENTITY_TOKEN` (TEXT)

#### LEGALENTITIES.RAW_OLTP.SIGNALS

Structure-level signals for triggering actions or recording events.

**Key Fields:**
- `ID` (NUMBER), `STRUCTURE_TOKEN` (TEXT), `STRUCTURE_REVISION` (NUMBER)
- `TYPE` (TEXT), `REVISION` (NUMBER)
- `CREATED_AT` (TIMESTAMP_NTZ), `UPDATED_AT` (TIMESTAMP_NTZ)

#### LEGALENTITIES.RAW_OLTP.FEED_CURSORS

Internal feed sync cursor tracking. Tracks consumer offsets for event processing.

**Key Fields:**
- `ID` (NUMBER), `CONSUMER` (TEXT), `TOKEN` (TEXT)
- `LAST_FETCHED_AT` (TIMESTAMP_NTZ), `SHARD` (NUMBER), `ENABLED` (NUMBER)

**Note:** This is an internal infrastructure table for event processing. Rarely useful for analytical queries.

---

## Table Relationships

```
STRUCTURE_MERCHANT.STRUCTURE_TOKEN → all other tables

LES_NODE_RELATIONSHIP
    ├── PARENT_NODE_TOKEN → LES_BUSINESS_DATA.NODE_TOKEN (business)
    └── CHILD_NODE_TOKEN → LES_INDIVIDUAL_DATA.NODE_TOKEN (individual)

NODE_VERIFICATION_DECISIONS.NODE_TOKEN → LES_INDIVIDUAL_DATA.NODE_TOKEN / LES_BUSINESS_DATA.NODE_TOKEN
NODE_VERIFICATION_DECISION_REASONS (same STRUCTURE_TOKEN + SEQUENCE as decisions)

VERIFICATION_ATTEMPTS.VERIFICATION_REQUEST_ID → VERIFICATION_REQUESTS.ID
```

### Cross-Database Link: STRUCTURE_TOKEN

`STRUCTURE_TOKEN` is the primary key that links LEGALENTITIES to ONBOARD:

```
LEGALENTITIES.RAW_OLTP.STRUCTURE_MERCHANT.STRUCTURE_TOKEN
    ← ONBOARD.RAW_OLTP.ACTIVATION_FLOWS.STRUCTURE_TOKEN
```

See `square-identity-verification-onboard.md` for ONBOARD tables and cross-database queries.

---

## Common Query Patterns

### Legal Entity Structure Traversal

```sql
-- Get the full legal entity structure for a merchant
SELECT
    SM.STRUCTURE_TOKEN,
    SM.CUSTOMER_ID,
    SM.PRODUCT,
    NR.PARENT_NODE_TOKEN,
    NR.CHILD_NODE_TOKEN,
    NR.ROLE,
    NR.OWNERSHIP,
    NR.IS_PRIMARY,
    BD.LEGAL_NAME AS business_name,
    BD.DBA_NAME,
    ID.GIVEN_NAME,
    ID.FAMILY_NAME,
    ID.EMAIL
FROM LEGALENTITIES.RAW_OLTP.STRUCTURE_MERCHANT SM
LEFT JOIN LEGALENTITIES.RAW_OLTP.LES_NODE_RELATIONSHIP NR
    ON NR.STRUCTURE_TOKEN = SM.STRUCTURE_TOKEN
LEFT JOIN LEGALENTITIES.RAW_OLTP.LES_BUSINESS_DATA BD
    ON BD.NODE_TOKEN = NR.PARENT_NODE_TOKEN
    AND BD.STRUCTURE_TOKEN = SM.STRUCTURE_TOKEN
LEFT JOIN LEGALENTITIES.RAW_OLTP.LES_INDIVIDUAL_DATA ID
    ON ID.NODE_TOKEN = NR.CHILD_NODE_TOKEN
    AND ID.STRUCTURE_TOKEN = SM.STRUCTURE_TOKEN
WHERE SM.CUSTOMER_ID = '<customer_id>'
```

### Verification Decision History for a Structure

```sql
SELECT
    VD.STRUCTURE_TOKEN,
    VD.PRODUCT,
    VD.STATUS,
    VD.REASON,
    VD.SEQUENCE,
    VD.CREATED_AT,
    NVD.NODE_TOKEN,
    NVD.DECISION AS node_decision,
    NVD.ROLE,
    NVDR.CODE AS reason_code,
    NVDR.COMMENT AS reason_comment
FROM LEGALENTITIES.RAW_OLTP.VERIFICATION_DECISIONS VD
LEFT JOIN LEGALENTITIES.RAW_OLTP.NODE_VERIFICATION_DECISIONS NVD
    ON NVD.STRUCTURE_TOKEN = VD.STRUCTURE_TOKEN
    AND NVD.STRUCTURE_REVISION = VD.STRUCTURE_REVISION
    AND NVD.PRODUCT = VD.PRODUCT
    AND NVD.SEQUENCE = VD.SEQUENCE
LEFT JOIN LEGALENTITIES.RAW_OLTP.NODE_VERIFICATION_DECISION_REASONS NVDR
    ON NVDR.STRUCTURE_TOKEN = NVD.STRUCTURE_TOKEN
    AND NVDR.STRUCTURE_REVISION = NVD.STRUCTURE_REVISION
    AND NVDR.PRODUCT = NVD.PRODUCT
    AND NVDR.SEQUENCE = NVD.SEQUENCE
    AND NVDR.NODE_TOKEN = NVD.NODE_TOKEN
WHERE VD.STRUCTURE_TOKEN = '<structure_token>'
ORDER BY VD.SEQUENCE DESC
```

### Find Structure by Merchant Token

```sql
SELECT
    SM.STRUCTURE_TOKEN,
    SM.CUSTOMER_ID,
    SM.PRODUCT,
    SM.PURPOSE,
    SM.CREATED_AT
FROM LEGALENTITIES.RAW_OLTP.STRUCTURE_MERCHANT SM
WHERE SM.CUSTOMER_ID = '<customer_id>'
```

### Structure Change History

```sql
SELECT
    SC.STRUCTURE_TOKEN,
    SC.STRUCTURE_VERSION,
    SC.TYPE,
    SC.CREATED_AT
FROM LEGALENTITIES.RAW_OLTP.STRUCTURE_CHANGES SC
WHERE SC.STRUCTURE_TOKEN = '<structure_token>'
ORDER BY SC.STRUCTURE_VERSION DESC
```

### Node Identifiers for a Structure

```sql
SELECT
    NI.NODE_TOKEN,
    NI.NODE_TYPE,
    NI.IDENTIFIER_TYPE,
    NI.VALUE,
    NI.STRUCTURE_VERSION
FROM LEGALENTITIES.RAW_OLTP.LES_NODE_IDENTIFIER NI
WHERE NI.STRUCTURE_TOKEN = '<structure_token>'
ORDER BY NI.NODE_TOKEN, NI.IDENTIFIER_TYPE
```
