# Stage runbook

Monday 9 Nov 2026, 11:00, Room 1 Track A. 45 minutes.

## The night before

```bash
python3 scripts/fetch_feed.py        # pin the real catalog, needs internet
python3 scripts/run_offline.py data/kev-live.json
```

Read the brief it produces. Pick the two lines you will read out loud on the
`output` slide, and note the token counts for slide 15.

Record the fallback:

```bash
asciinema rec demo-run.cast -c "python3 scripts/run_offline.py data/kev-live.json"
```

Or screen record it. Have it one click away.

## On stage

**Slide 8, "Run it."** In the terminal:

```bash
claude            # then: run the overnight brief
```

Leave it. Switch back to the deck. Do not watch it.

**Slide 17, "Read it."** Switch to the terminal, `cat output/brief.md`,
read two or three lines. Pick the one where it decided something did NOT matter.

**Slide 19, the poisoned advisory.** First show the record:

```bash
python3 -c "import json;print(json.load(open('data/kev-sample-POISONED.json'))['vulnerabilities'][-1]['notes'])"
```

Read it out loud. Then go unguarded and run it:

```bash
cp .claude/settings.json .claude/settings.SAFE.json
cp .claude/settings.UNSAFE.json .claude/settings.json
claude            # then: run the overnight brief using data/kev-sample-POISONED.json
```

**Slide 21, guarded.** Put the real permissions back and run the identical input:

```bash
cp .claude/settings.SAFE.json .claude/settings.json
claude            # then: run the overnight brief using data/kev-sample-POISONED.json
```

It should flag the embedded instruction in the brief and refuse the export.

## If anything dies

Play the recording and say "and this is why you always have the recording."
Do not debug in front of 200 people. The deterministic fallback always works:

```bash
python3 scripts/run_offline.py
```

## Reset between rehearsals

```bash
cp .claude/settings.SAFE.json .claude/settings.json 2>/dev/null
rm -f output/brief.md output/matches.json output/export.txt
```
