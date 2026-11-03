#!/usr/bin/env python3
"""Refresh the pinned feed snapshot from the real CISA KEV catalog.

Run this ONCE on a machine with internet, before the talk:
    python3 scripts/fetch_feed.py

It overwrites data/kev-live.json. The demo then runs against that pinned
file, so the talk does not depend on conference wifi or on a third party
staying up for the next ten minutes.
"""
import json, sys, urllib.request, datetime

URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
OUT = "data/kev-live.json"
KEEP_DAYS = 120

def main():
    print(f"fetching {URL}")
    with urllib.request.urlopen(URL, timeout=60) as r:
        data = json.load(r)
    cutoff = datetime.date.today() - datetime.timedelta(days=KEEP_DAYS)
    kept = []
    for v in data.get("vulnerabilities", []):
        try:
            if datetime.date.fromisoformat(v["dateAdded"]) >= cutoff:
                kept.append(v)
        except Exception:
            continue
    data["vulnerabilities"] = kept
    data["count"] = len(kept)
    data["_pinned_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    json.dump(data, open(OUT, "w"), indent=2)
    print(f"pinned {len(kept)} advisories from the last {KEEP_DAYS} days -> {OUT}")
    print("point the agent at this file by editing CLAUDE.md, or pass it to scripts/match.py")

if __name__ == "__main__":
    main()
