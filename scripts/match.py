#!/usr/bin/env python3
"""Match a KEV-format feed against the asset inventory.

Pure data work, no model involved. The agent calls this as a tool.
Output: output/matches.json
"""
import csv, json, sys, os
from datetime import date

FEED = sys.argv[1] if len(sys.argv) > 1 else "data/kev-sample.json"
ASSETS = "data/assets.csv"
OUT = "output/matches.json"

def norm(s):
    return (s or "").strip().lower()

def main():
    feed = json.load(open(FEED))
    assets = list(csv.DictReader(open(ASSETS)))
    matches = []
    for v in feed.get("vulnerabilities", []):
        for a in assets:
            if norm(v.get("vendorProject")) == norm(a["vendor"]) and norm(v.get("product")) == norm(a["product"]):
                overdue = False
                try:
                    overdue = date.fromisoformat(v["dueDate"]) < date.today()
                except Exception:
                    pass
                matches.append({
                    "cveID": v["cveID"],
                    "product": f'{a["vendor"]} {a["product"]} {a["version"]}',
                    "owner": a["owner"],
                    "exposure": a["exposure"],
                    "criticality": a["business_criticality"],
                    "ransomware": v.get("knownRansomwareCampaignUse", "Unknown"),
                    "dueDate": v.get("dueDate"),
                    "overdue": overdue,
                    "description": v.get("shortDescription", ""),
                })
    os.makedirs("output", exist_ok=True)
    json.dump({"feed": FEED, "matched": len(matches), "matches": matches}, open(OUT, "w"), indent=2)
    print(f"{len(matches)} of {len(feed.get('vulnerabilities', []))} advisories match the inventory -> {OUT}")

if __name__ == "__main__":
    main()
