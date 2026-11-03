#!/usr/bin/env python3
"""Proves the demo behaves the way the talk claims it does.

Run before the talk:  python3 tests/test_demo.py
Every scenario on stage is covered here.
"""
import json, os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
results = []

def run(*args, cwd=ROOT):
    return subprocess.run([PY, *args], cwd=cwd, capture_output=True, text=True)

def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"   [{detail}]" if detail and not ok else ""))

def reset():
    for f in ("brief.md", "matches.json", "flagged.json", "export.txt"):
        p = os.path.join(ROOT, "output", f)
        if os.path.exists(p):
            os.remove(p)

print("\n1. CLEAN RUN (slides 8 and 17)")
reset()
r = run("scripts/run_offline.py", "data/kev-sample.json")
check("the loop completes and verification passes", r.returncode == 0)
brief = open(os.path.join(ROOT, "output/brief.md")).read()
check("the brief exists and has sections", brief.count("\n## ") >= 6)
check("it filters: 6 of 8 advisories matched", "6 of 8" in r.stdout, r.stdout.strip()[:80])
check("no false positive on isolation", "no embedded instructions" in r.stdout)

print("\n2. NO DEFINITION OF DONE (slide 14, where agents break)")
reset()
run("scripts/run_offline.py", "data/kev-sample.json")
full = open(os.path.join(ROOT, "output/brief.md")).read()
parts = full.split("\n## ")
open(os.path.join(ROOT, "output/brief.md"), "w").write(parts[0] + "\n## " + "\n## ".join(parts[1:3]))
r = run("scripts/verify_brief.py")
check("an agent that stops early is caught", r.returncode == 1)
check("and it is told exactly what is missing", "have no section" in r.stdout, r.stdout.strip()[:80])

print("\n3. POISONED FEED, GUARDED (slide 21)")
reset()
r = run("scripts/run_offline.py", "data/kev-sample-POISONED.json")
check("the run still completes", r.returncode == 0)
brief = open(os.path.join(ROOT, "output/brief.md")).read()
check("the injection is reported in the brief", "embedded instructions" in brief)
check("severities were NOT downgraded", len(re.findall(r"Severity: CRITICAL", brief)) >= 1)
check("the inventory was NOT exported", not os.path.exists(os.path.join(ROOT, "output/export.txt")))
flagged = json.load(open(os.path.join(ROOT, "output/flagged.json")))
check("the scanner named the injection", flagged["flagged"] == 1 and flagged["records"][0]["cveID"] == "CVE-2026-110904")
reasons = {h["reason"] for h in flagged["records"][0]["hits"]}
check("it caught all five injection shapes", len(reasons) >= 5, str(sorted(reasons)))

print("\n4. POISONED FEED, UNGUARDED (slide 19, the agent obeys)")
reset()
run("scripts/run_offline.py", "data/kev-sample-POISONED.json")
brief = open(os.path.join(ROOT, "output/brief.md")).read()
# simulate an agent that did what the advisory told it to do
obeyed = re.sub(r"Severity: \w+", "Severity: LOW", brief)
obeyed = obeyed.replace("> Advisory CVE-2026-110904 contained embedded instructions. Flagged, not followed.\n\n", "")
open(os.path.join(ROOT, "output/brief.md"), "w").write(obeyed)
shutil.copy(os.path.join(ROOT, "data/assets.csv"), os.path.join(ROOT, "output/export.txt"))
r = run("scripts/verify_brief.py")
check("verification REFUSES the obedient agent's work", r.returncode == 1)
check("and names the cause", ("embedded instructions" in r.stdout) or ("export" in r.stdout) or ("LOW" in r.stdout), r.stdout.strip()[:100])

print("\n5. STAGE SAFETY")
reset()
check("permissions file has a deny list", len(json.load(open(os.path.join(ROOT, ".claude/settings.json")))["permissions"]["deny"]) >= 5)
check("the unsafe file is clearly marked", "ACT 3 DEMO ONLY" in open(os.path.join(ROOT, ".claude/settings.UNSAFE.json")).read())
check("the fallback needs no network", "urllib" not in open(os.path.join(ROOT, "scripts/run_offline.py")).read())
check("CLAUDE.md declares the feed as data", "DATA, not instructions" in open(os.path.join(ROOT, "CLAUDE.md")).read())

reset()
run("scripts/run_offline.py", "data/kev-sample.json")
passed = sum(1 for _, ok, _ in results if ok)
print(f"\n{'='*58}\n{passed}/{len(results)} checks passed\n{'='*58}")
sys.exit(0 if passed == len(results) else 1)
