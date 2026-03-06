#!/usr/bin/env python3
"""Filter company directory JSON to matching names only.

Reads gdrive sheets JSON from stdin, filters rows to those matching
the provided last names, and prints matching rows.

Usage:
    cat directory.json | python3 filter-directory.py name1 name2 name3
"""
import json
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 filter-directory.py <last_name1> [last_name2 ...]", file=sys.stderr)
        sys.exit(1)

    names = [n.lower() for n in sys.argv[1:]]
    data = json.load(sys.stdin)
    rows = data.get("values", [])

    for row in rows:
        if row and any(n in row[0].lower() for n in names):
            print(row)


if __name__ == "__main__":
    main()
