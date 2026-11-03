#!/usr/bin/env python3
"""Isolation check: find text in the feed that is trying to act like an instruction.

This is the ISOLATE job from the talk, as code. It does not ask a model to
"be careful". It scans the untrusted fields of every record for the shapes an
injection takes, and reports them.

Output: output/flagged.json
Exit 0 always. Finding an injection is a normal result, not an error.
"""
import json, os, re, sys

FEED = sys.argv[1] if len(sys.argv) > 1 else "data/kev-sample.json"
OUT = "output/flagged.json"

# Fields that come from outside and are therefore never instructions.
UNTRUSTED_FIELDS = ("shortDescription", "requiredAction", "notes", "vulnerabilityName")

PATTERNS = [
    (r"\b(prior|previous|earlier|above)\s+instructions?\b", "claims to supersede instructions"),
    (r"\bsystem\s+(notice|prompt|message|instruction)", "impersonates a system message"),
    (r"\bignore\s+(all\s+)?(prior|previous|the\s+above)", "asks the reader to ignore instructions"),
    (r"\b(mark|set|treat|rate)\b.{0,40}\bas\s+(severity\s+)?(low|informational|no\s+action)", "asks for a severity downgrade"),
    (r"\bdo not (mention|report|disclose|log|tell)", "asks for concealment"),
    (r"\b(copy|write|export|exfiltrate|send|upload)\b.{0,40}\.(csv|json|env|pem|key|txt)\b", "asks for a file to be moved"),
    (r"\byou (must|should|are to)\b", "addresses the reader as an agent"),
]

def main():
    feed = json.load(open(FEED))
    flagged = []
    for v in feed.get("vulnerabilities", []):
        hits = []
        for field in UNTRUSTED_FIELDS:
            text = v.get(field) or ""
            for pat, why in PATTERNS:
                if re.search(pat, text, re.I):
                    hits.append({"field": field, "reason": why})
        if hits:
            flagged.append({"cveID": v.get("cveID"), "hits": hits})

    os.makedirs("output", exist_ok=True)
    json.dump({"feed": FEED, "flagged": len(flagged), "records": flagged}, open(OUT, "w"), indent=2)

    if flagged:
        print(f"ISOLATION: {len(flagged)} record(s) contain embedded instructions. Reported, not followed.")
        for f in flagged:
            reasons = ", ".join(sorted({h["reason"] for h in f["hits"]}))
            print(f"  {f['cveID']}: {reasons}")
    else:
        print("ISOLATION: no embedded instructions found in untrusted fields.")
    print(f"-> {OUT}")

if __name__ == "__main__":
    main()
