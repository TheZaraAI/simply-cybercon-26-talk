#!/usr/bin/env python3
"""Deterministic fallback run. No model, no network, no API key.

This exists for two reasons:
  1. It is the recording you play if the live run dies on stage.
  2. It proves the plumbing works on any laptop, today.

The live demo is Claude Code doing this with judgment. This does the
mechanical part only, so the output is a real brief built from real matching.
"""
import json, os, sys, subprocess, datetime

FEED = sys.argv[1] if len(sys.argv) > 1 else "data/kev-sample.json"

def sev(m):
    if m["ransomware"] == "Known" and m["exposure"] == "internet-facing":
        return "CRITICAL"
    if m["exposure"] == "internet-facing" or m["criticality"] == "high":
        return "HIGH"
    return "MEDIUM"

def main():
    print(f"[plan]   read {FEED}, isolate, match against data/assets.csv, write output/brief.md")
    subprocess.run([sys.executable, "scripts/scan_feed.py", FEED], check=True)
    subprocess.run([sys.executable, "scripts/match.py", FEED], check=True)
    matches = json.load(open("output/matches.json"))["matches"]
    flagged = json.load(open("output/flagged.json"))["records"]

    # Act: compose the brief.
    lines = [
        "# Overnight threat brief",
        f"_Generated {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} from {FEED}_",
        "",
        f"{len(matches)} of your assets appear in the catalog of actively exploited vulnerabilities.",
        "",
    ]
    wake = [m for m in matches if sev(m) == "CRITICAL"]
    lines += [f"**Wake-up items: {len(wake)}**", ""]
    for f in flagged:
        lines += [f"> Advisory {f['cveID']} contained embedded instructions. Flagged, not followed.", ""]
    for m in sorted(matches, key=lambda x: (sev(x) != "CRITICAL", x["cveID"])):
        lines += [
            f"## {m['cveID']} — {m['product']}",
            f"- Severity: {sev(m)}",
            f"- Action: patch per vendor advisory; owner is {m['owner']}"
            + (f"; CISA due date {m['dueDate']} has passed" if m["overdue"] else f"; CISA due date {m['dueDate']}"),
            f"- Exposure: {m['exposure']}, business criticality {m['criticality']}, ransomware use {m['ransomware']}",
            f"- {m['description']}",
            "",
        ]
    os.makedirs("output", exist_ok=True)
    open("output/brief.md", "w").write("\n".join(lines))
    print(f"[act]    wrote output/brief.md ({len(matches)} sections)")

    print("[verify] running scripts/verify_brief.py")
    r = subprocess.run([sys.executable, "scripts/verify_brief.py"])
    print("[decide] done" if r.returncode == 0 else "[decide] escalate: verification failed")
    sys.exit(r.returncode)

if __name__ == "__main__":
    main()
