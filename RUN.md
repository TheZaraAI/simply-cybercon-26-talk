# Stage runbook

Monday 9 Nov 2026, 11:00, Room 1 Track A. 45 minutes.

Slide numbers below match the live deck (43 slides).

## The night before

```bash
python3 scripts/fetch_feed.py        # pin the real catalog, needs internet
python3 scripts/run_offline.py data/kev-live.json
```

Read the brief it produces. Pick the two lines you will read out loud on the
`output` slide (26), and note the token counts for slide 24.

Run the test suite. All 18 checks must pass:

```bash
python3 tests/test_demo.py
```

Check the Claude Code sign-in will outlive the talk:

```bash
claude auth status      # loginExpiresAt must be after Mon 9 Nov 12:00
```

If it is not, run `claude auth login` tonight.

**Both recordings are in the deck**, click to play, sound on: Demo 1 on
slide 12, Demo 2 on slide 13. The same clips are in `demos/` (narrated and
silent) if you would rather play them from a player:

- `Demo_01_The_Overnight_Run_NARRATED.mp4` (52s), the clean run
- `Demo_02_The_Injection_NARRATED.mp4` (64s), the breach, unguarded then contained

## On stage

**Slide 12.** Click the clean run recording. Let it talk. 52 seconds.

**Slide 13.** Click the breach recording. 64 seconds. One line after: everything
that separated those two runs is the rest of this talk.

**Slide 14, "Run it."** In the terminal:

```bash
claude            # then: run the overnight brief
```

Leave it. Switch back to the deck. Do not watch it. On this Mac expect one or
two permission prompts for reading data and writing the brief, because the home
folder name ends in a dot and Claude Code treats that path as suspicious. Click
Yes and keep talking.

**Slide 26, "Read it."** Switch to the terminal, `cat output/brief.md`,
read two or three lines. Pick the one where it decided something did NOT matter.

**Slide 30, the poisoned advisory.** Show the record and read it out loud:

```bash
python3 -c "import json;print(json.load(open('data/kev-sample-POISONED.json'))['vulnerabilities'][-1]['notes'])"
```

Nothing else runs on this slide. The unguarded run is the first half of the
recording on slide 13.

**Slide 32, guarded, live.** Same request, real context file, real permissions:

```bash
claude            # then: run the overnight brief using data/kev-sample-POISONED.json
```

It flags the embedded instruction in the brief, leaves the severities alone,
writes no export, and `verify_brief.py` passes.

## If anything dies

Jump back to slide 12 or 13 and play the recording, and say "and this is why
you always have the recording." Do not debug in front of 200 people.

The deterministic fallback also always works, no key and no network:

```bash
python3 scripts/run_offline.py                          # clean run
python3 scripts/run_offline.py data/kev-sample-POISONED.json   # guarded, flags the injection
```

## Why the unguarded run is a recording and not live

With the permissions stripped (`.claude/settings.UNSAFE.json`) the model still
refuses the injection most of the time, because refusing is what a well trained
model tends to do on a good day. The recording is the bad day. You do not get to
choose which day you get on stage, which is the whole argument for the three
controls. To try the unguarded run yourself, see SETUP.md step 6a.

## Reset between rehearsals

```bash
cp .claude/settings.SAFE.json .claude/settings.json 2>/dev/null
rm -f output/brief.md output/matches.json output/flagged.json output/export.txt
```
