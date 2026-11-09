# The two demo videos

Both are short recordings of the agent in this repo. Play them in any video
player. They are not needed to run anything: they show what you should see when
you run it yourself.

## Which file is which

| File | Length | What it shows |
|---|---|---|
| `Demo_01_The_Overnight_Run_NARRATED.mp4` | about 52 s | The agent doing its job at 2am: it reads the feed, matches your assets, checks its own work with a script, and writes the brief. Voiceover included |
| `Demo_01_The_Overnight_Run.mp4` | about 52 s | The same picture with no sound |
| `Demo_02_The_Injection_NARRATED.mp4` | about 64 s | The same agent given a poisoned feed. Left side, no protection: it obeys the planted instruction. Right side, with the context file and permissions in place: it reports the attempt instead. Voiceover included |
| `Demo_02_The_Injection.mp4` | about 64 s | The same picture with no sound |
| `narration_demo_01.txt` | | The words spoken in Demo 1 |
| `narration_demo_02.txt` | | The words spoken in Demo 2 |

## Watch them in this order

1. Demo 1 first. This is what "working" looks like.
2. Demo 2 second. This is what an attack on that same agent looks like, and what
   stops it.

## Then do it yourself

Demo 1 is what you get from `SETUP.md`, steps 4 and 5. Demo 2 is steps 6a and 6b.
You will not see exactly the same words on your screen. A model writes its own
wording each time. What should match is the result: a brief with six sections, and
with the poisoned feed a line that says `Flagged, not followed` and no
`output/export.txt` file.

## The deck

The slides that go with these are in `../deck/`.
