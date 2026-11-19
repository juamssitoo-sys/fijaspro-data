#!/usr/bin/env python3
"""Audit remote NBA catalog metadata without copying third-party game records.

Requires: pip install duckdb
This script only reads the catalog metadata and writes a compact coverage report.
It deliberately does not mirror game/player rows into this repository.
"""
from __future__ import annotations
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import duckdb

CATALOG = os.getenv("NBA_DUCKDB_URL", "https://basketball-data.billmill.org/nba/nba.duckdb")
OUT = Path(os.getenv("COVERAGE_OUT", "data/metadata/nba_catalog_audit.json"))
START = "2025-01-01"
END = "2026-11-19"

def main() -> None:
    con = duckdb.connect()
    con.execute("INSTALL httpfs; LOAD httpfs;")
    con.execute("ATTACH ? AS nba (READ_ONLY)", [CATALOG])
    tables = con.execute("SHOW ALL TABLES").fetchall()
    # The catalog metadata table describes table/season availability.
    try:
        rows = con.execute("SELECT * FROM nba.metadata").fetchdf().to_dict("records")
    except Exception as exc:
        rows = []
        metadata_error = str(exc)
    else:
        metadata_error = None
    report = {
        "provider": "llimllib/nba_data",
        "catalog_url": CATALOG,
        "audited_at_utc": datetime.now(timezone.utc).isoformat(),
        "requested_window": {"start": START, "end": END},
        "tables_seen": [list(row) for row in tables],
        "metadata_rows": rows,
        "metadata_error": metadata_error,
        "rights_status": "review_required_no_mirroring",
        "note": "This is a catalog coverage audit only. No third-party game/player records are stored here."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
