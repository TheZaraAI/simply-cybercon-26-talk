# Daily threat brief, social edition

A second worked example of the same seven-section context file, pointed at
content you publish instead of a task you run. From the Simply Cyber Con 2026
session "Prompting Is Dead. Long Live Context."

Use this one if you post daily and the research is eating your morning.

## Make it yours in three steps

1. **Paste your voice in.** Open `voice/my-last-20-posts.md` and replace it
   with twenty of your real posts, in full. This is the step people skip and
   it is the step that decides whether the output sounds like you or like a
   vendor newsletter. Describing your voice does not work. Paste the posts.

2. **Pin today's sources.** Save the articles you want it to read into
   `sources/pinned/`. The agent never touches the network, so that folder is
   the entire world it can see. You chose every file in it, which is the
   whole point.

3. **Run it.** Open this folder in Claude Code and say:

   > read CLAUDE.md and write today's post

   Then read `output/post.md`, and read `output/receipts.md` before you
   publish anything.

## Check it yourself

```bash
python3 scripts/verify_post.py
```

That script is the definition of done. It fails the post for being too long,
for a statistic with no source, for anything on your banned list, for
hashtags, for emoji, and for any sign that something tried to publish. The
agent does not get to call its own work finished.

Edit `voice/banned.md` every time you catch yourself rewriting the same tic
out of a draft. That file turns a preference into a control.

## Why the permissions file matters

`.claude/settings.json` denies network access and denies writes outside
`output/`. The context file explains the rules; that file enforces them. If
you only take one habit from the talk, take that one: write the rule in both
places, and know which of the two is actually stopping you.
