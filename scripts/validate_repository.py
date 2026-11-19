#!/usr/bin/env python3
"""Basic repository checks: JSON syntax, date window, and forbidden secret-like files."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []
for path in (ROOT / "config").glob("*.json"):
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}: {exc}")
for path in (ROOT / "schemas").glob("*.json"):
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}: {exc}")
forbidden = {".env", "service-account.json", "credentials.json"}
for path in ROOT.rglob("*"):
    if path.is_file() and path.name in forbidden:
        errors.append(f"Potential secret file committed: {path}")
if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print("Repository validation passed.")
