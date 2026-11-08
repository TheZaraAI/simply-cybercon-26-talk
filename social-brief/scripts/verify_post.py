#!/usr/bin/env python3
"""The definition of done for the social threat brief, as a script.

The agent does not get to decide the post is publishable. This does.
Exits 0 when the post passes every check, 1 with a reason when it does not.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
POST = ROOT / "output" / "post.md"
RECEIPTS = ROOT / "output" / "receipts.md"
BANNED = ROOT / "voice" / "banned.md"

MAX_WORDS = 120
EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]"
)
URL = re.compile(r"https?://\S+")
# A statistic: a bare number, a percentage, a money figure, or a CVE.
STAT = re.compile(r"\b(?:CVE-\d{4}-\d{4,7}|\$[\d,.]+[KMB]?|\d[\d,.]*%?)\b")

failures = []


def fail(msg):
    failures.append(msg)


if not POST.exists():
    print("FAIL: output/post.md does not exist. Nothing was written.")
    sys.exit(1)

post = POST.read_text()
receipts = RECEIPTS.read_text() if RECEIPTS.exists() else ""

# 1. Length. A post nobody finishes is not a post.
words = len(post.split())
if words > MAX_WORDS:
    fail(f"post is {words} words, limit is {MAX_WORDS}")

# 2. Receipts exist and carry at least one real source.
if not RECEIPTS.exists():
    fail("output/receipts.md does not exist, so no claim can be defended")
elif not URL.search(receipts):
    fail("output/receipts.md contains no URL, so no claim has a source")

# 3. Every statistic in the post is in the receipts.
post_stats = set(STAT.findall(post))
unsourced = sorted(s for s in post_stats if s not in receipts)
if unsourced:
    fail("statistics in the post with no matching receipt: " + ", ".join(unsourced))

# 4. No banned words or framings.
if BANNED.exists():
    phrases = [
        ln.strip().lstrip("-").strip().lower()
        for ln in BANNED.read_text().splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    hits = sorted({p for p in phrases if p and p in post.lower()})
    if hits:
        fail("banned phrasing found: " + "; ".join(hits))

# 5. House style: no hashtags, no emoji.
if "#" in re.sub(r"^#+ ", "", post, flags=re.M):
    fail("post contains a hashtag")
if EMOJI.search(post):
    fail("post contains an emoji")

# 6. Never ship a hedge you did not resolve.
if "unverified" in post.lower():
    fail('the word "unverified" appears in the post')

# 7. The agent must not have published anything.
for stray in ("output/posted.json", "output/scheduled.json"):
    if (ROOT / stray).exists():
        fail(f"{stray} exists, which means something tried to publish")

if failures:
    print("NOT PUBLISHABLE:")
    for f in failures:
        print("  -", f)
    sys.exit(1)

print(f"PUBLISHABLE: {words} words, {len(post_stats)} sourced statistics, 0 banned phrases.")
sys.exit(0)
