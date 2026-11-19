#!/usr/bin/env python3
"""Normalize OpenFootball JSON and Football.TXT files without inventing time zones.

Usage:
  python scripts/normalize_openfootball.py --root . --out data/normalized/openfootball_matches.jsonl

Dates are preserved as calendar dates. Kick-off times remain source_local_time because
the source files do not provide a reliable IANA timezone for every competition.
"""
from __future__ import annotations
import argparse
import json
import re
from datetime import datetime
from pathlib import Path

MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1
)}
DATE_RE = re.compile(r"^\s*(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+([A-Z][a-z]{2})\s+(\d{1,2})(?:\s+(\d{4}))?\s*$")
SCORE_RE = re.compile(r"(?P<score>\d+\s*[-–]\s*\d+)(?P<tail>.*)$")
INTL_RE = re.compile(r"^\s*(?P<home>.+?)\s+(?P<h>\d+)\s*[-–]\s*(?P<a>\d+)\s+(?P<away>.+?)(?:\s+@\s+(?P<venue>.+))?\s*$")

def iso_date(month: str, day: str, year: int) -> str:
    return datetime(year, MONTHS[month], int(day)).date().isoformat()

def parse_score_tail(score: str, tail: str) -> dict:
    parts = [int(x) for x in re.split(r"\s*[-–]\s*", score)]
    result = {"home_score": parts[0], "away_score": parts[1],
              "half_time_home_score": None, "half_time_away_score": None,
              "penalty_home_score": None, "penalty_away_score": None,
              "extra_time": "a.e.t." in tail.lower(),
              "penalties": "pen." in tail.lower(),
              "awarded": "awarded" in tail.lower(),
              "source_score_note": tail.strip() or None}
    ht = re.search(r"\((\d+)\s*[-–]\s*(\d+)(?:,\s*\d+\s*[-–]\s*\d+)?\)", tail)
    if ht:
        result["half_time_home_score"], result["half_time_away_score"] = int(ht.group(1)), int(ht.group(2))
    pens = re.search(r"pen\.\s*(\d+)\s*[-–]\s*(\d+)", tail, re.I)
    if pens:
        result["penalty_home_score"], result["penalty_away_score"] = int(pens.group(1)), int(pens.group(2))
    return result

def split_teams_and_score(text: str):
    m = SCORE_RE.search(text)
    if not m:
        return None
    before = text[:m.start()].strip()
    if " v " not in before:
        return None
    home, away = re.split(r"\s+v\s+", before, maxsplit=1)
    return home.strip(), away.strip(), parse_score_tail(m.group("score"), m.group("tail"))

def parse_football_txt(path: Path, competition_id: str, season: str, provider_url: str):
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    header = next((x for x in lines if x.startswith("= ")), "")
    year_match = re.search(r"(20\d{2})", header)
    if not year_match:
        year_match = re.search(r"(20\d{2})", path.name)
    default_year = int(year_match.group(1)) if year_match else int(season[:4])
    current_year, current_date, stage = default_year, None, None
    out, skipped = [], 0
    for line_no, line in enumerate(lines, 1):
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("="):
            continue
        if s.startswith(("▪", "•")):
            stage = s.lstrip("▪• ").strip()
            continue
        dm = DATE_RE.match(line)
        if dm:
            month, day, explicit_year = dm.groups()
            if explicit_year:
                current_year = int(explicit_year)
            else:
                # Roll year forward only when a Dec -> Jan transition is explicit.
                if MONTHS[month] == 1 and current_date and current_date[5:7] == "12":
                    current_year += 1
            try:
                current_date = iso_date(month, day, current_year)
            except ValueError:
                current_date = None
            continue
        if current_date is None:
            continue
        # Matchday style, optional kickoff time, team v team score.
        time_match = re.match(r"^\s*(?:(\d{1,2}:\d{2})\s+)?(.*)$", line)
        local_time, body = time_match.group(1), time_match.group(2)
        split = split_teams_and_score(body)
        if split:
            home, away, scores = split
            out.append({
                "sport": "football", "competition_id": competition_id, "season": season,
                "stage": stage, "date": current_date, "source_local_time": local_time,
                "status": "played", "home_team": home, "away_team": away,
                **scores, "source": {"provider": "openfootball", "source_url": provider_url,
                    "provider_record_id": None, "source_file": str(path.as_posix()),
                    "source_line": line_no, "license": "upstream CC0 claim; review third-party rights"}
            })
            continue
        # International-results style: Home 2-1 Away @ venue.
        im = INTL_RE.match(line)
        if im:
            out.append({
                "sport": "football", "competition_id": competition_id, "season": season,
                "stage": stage, "date": current_date, "source_local_time": None,
                "status": "played", "home_team": im.group("home").strip(),
                "away_team": im.group("away").strip(), "home_score": int(im.group("h")),
                "away_score": int(im.group("a")), "venue": im.group("venue"),
                "half_time_home_score": None, "half_time_away_score": None,
                "penalty_home_score": None, "penalty_away_score": None,
                "extra_time": False, "penalties": False, "awarded": False,
                "source_score_note": None,
                "source": {"provider": "openfootball", "source_url": provider_url,
                    "provider_record_id": None, "source_file": str(path.as_posix()),
                    "source_line": line_no, "license": "upstream CC0 claim; review third-party rights"}
            })
            continue
        # Ignore goal-detail continuation lines, but count other unparsed match-like rows.
        if re.search(r"\d+\s*[-–]\s*\d+", s):
            skipped += 1
    return out, skipped

def parse_json_file(path: Path, competition_id: str, season: str, provider_url: str):
    obj = json.loads(path.read_text(encoding="utf-8"))
    out = []
    for idx, m in enumerate(obj.get("matches", []), 1):
        score = m.get("score")
        if isinstance(score, list):
            ft, ht = score, [None, None]
        elif isinstance(score, dict):
            ft, ht = score.get("ft"), score.get("ht", [None, None])
        else:
            ft, ht = None, [None, None]
        played = isinstance(ft, list) and len(ft) == 2
        out.append({
            "sport": "football", "competition_id": competition_id, "season": season,
            "stage": None, "round": m.get("round"), "date": m.get("date"),
            "source_local_time": m.get("time"), "status": "played" if played else "scheduled",
            "home_team": m.get("team1"), "away_team": m.get("team2"),
            "home_score": ft[0] if played else None, "away_score": ft[1] if played else None,
            "half_time_home_score": ht[0] if isinstance(ht, list) and len(ht) == 2 else None,
            "half_time_away_score": ht[1] if isinstance(ht, list) and len(ht) == 2 else None,
            "penalty_home_score": None, "penalty_away_score": None,
            "extra_time": False, "penalties": False, "awarded": False,
            "source_score_note": None,
            "source": {"provider": "openfootball", "source_url": provider_url,
                "provider_record_id": None, "source_file": str(path.as_posix()),
                "source_record": idx, "license": "upstream CC0 claim; review third-party rights"}
        })
    return out

def infer(path: Path):
    p = path.as_posix()
    mappings = [
        ("soccer_epl", "2025-26", "/2025-26/en.1.json", "football.json"),
        ("soccer_spain_la_liga", "2025-26", "/2025-26/es.1.json", "football.json"),
        ("soccer_germany_bundesliga", "2025-26", "/2025-26/de.1.json", "football.json"),
        ("soccer_france_ligue_one", "2025-26", "/2025-26/fr.1.json", "football.json"),
        ("soccer_italy_serie_a", "2025-26", "/2025-26/it.1.json", "football.json"),
        ("soccer_brazil_campeonato", "2025", "2025_br1.txt", "south-america"),
        ("soccer_argentina_primera_division", "2025", "2025_ar1.txt", "south-america"),
        ("soccer_uefa_champs_league", "2025-26", "cl.txt", "champions-league"),
        ("soccer_conmebol_libertadores", "2025", "2025_copal.txt", "south-america"),
        ("soccer_conmebol_copa_sudamericana", "2025", "2025_copas.txt", "south-america"),
        ("soccer_uefa_nations_league", "2024-25", "2024_uefa_nations_league.txt", "internationals"),
        ("soccer_uefa_europa_league", "2025-26", "elq.txt", "champions-league"),
        ("soccer_uefa_europa_conference_league", "2025-26", "confq.txt", "champions-league"),
    ]
    for cid, season, needle, repo in mappings:
        if needle in p:
            return cid, season, f"https://github.com/openfootball/{repo}/blob/master/{needle}"
    raise ValueError(f"No competition mapping for {path}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default="data/normalized/openfootball_matches.jsonl")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    raw = root / "data/raw/openfootball"
    records, file_reports = [], []
    for path in sorted(raw.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".json", ".txt"}:
            continue
        cid, season, url = infer(path.relative_to(root))
        if path.suffix.lower() == ".json":
            parsed = parse_json_file(path, cid, season, url)
            skipped = 0
        else:
            parsed, skipped = parse_football_txt(path.relative_to(root), cid, season, url)
        records.extend(parsed)
        file_reports.append({"file": path.relative_to(root).as_posix(), "competition_id": cid,
            "season": season, "parsed_records": len(parsed), "unparsed_score_lines": skipped})
    seen, duplicates = set(), []
    for row in records:
        key = (row["competition_id"], row["season"], row["date"], row["home_team"], row["away_team"])
        if key in seen:
            duplicates.append({"key": key, "source": row["source"]})
        seen.add(key)
    out = root / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for row in records:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    report = {"provider": "openfootball", "records": len(records), "duplicate_keys": len(duplicates),
        "files": file_reports, "duplicate_samples": duplicates[:50],
        "time_policy": "date retained as calendar date; source_local_time preserved without timezone conversion",
        "rights_note": "CC0 is an upstream claim; verify third-party rights before public redistribution."}
    report_path = out.with_name("openfootball_normalization_report.json")
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
if __name__ == "__main__":
    main()
