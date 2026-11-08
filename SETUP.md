# Setting this up on your laptop

Follow top to bottom. Every step has a CHECK so you know it worked before you
move on. Takes about 20 minutes.

---

## Step 0a. Just get the files (2 minutes)

If you are following along live and want the fastest path, do this and skip
ahead. The rest of this guide is for setting the habit properly afterwards.

**If you have git:**

```bash
git clone https://github.com/TheZaraAI/simply-cybercon-26-talk
cd simply-cybercon-26-talk
```

**If you do not:** green **Code** button on the repo page, **Download ZIP**.

Then three things that catch people out:

1. **Unzip it.** An agent cannot work inside a `.zip`. Claude Code, Cursor and
   every other tool open a *folder*, not an archive. Double-click the zip and
   use the folder it produces.
2. **Your folder is called `simply-cybercon-26-talk-main`**, with `-main` on
   the end, because that is the branch name. The `cd` commands in this guide
   and on the slides do not have it. Either rename the folder or add `-main`
   when you type.
3. **The `.claude` folder is there even though you cannot see it.** It starts
   with a dot, so Finder and File Explorer hide it. On a Mac press
   `Cmd + Shift + .` to show hidden files, or just run `ls -a` in the terminal.
   That folder holds the permissions, which is half the point of this repo.

Desktop is fine. Documents is fine. It does not care where it lives.

**CHECK:** from inside the folder, run this:

```bash
python3 scripts/run_offline.py && cat output/brief.md
```

You should see a threat brief. No API key, no install, no network. If that
works, you have everything you need to follow along.

---

## Step 0. Decide where your projects live

This matters more than it sounds, and it is the first thing worth teaching.

Pick ONE folder that holds every project, one subfolder per project, and every
one of them a git repo. On a Mac the convention is:

```
~/Projects/
  simply-cybercon-26-talk/     <- this talk
  getlogoff-cloud/             <- you already have this
  thezaraai-website/
```

The rule that keeps it clean:

- **If it matters, it is committed.** Code, context files, permissions, docs.
- **If it is generated, it is gitignored.** Output, logs, caches, keys.
- **GitHub is the source of truth. Your laptop is a working copy.**

Make the folder if you do not have one:

```bash
mkdir -p ~/Projects
cd ~/Projects
```

**Why this is worth saying on stage:** the folder IS the context boundary. What
sits in that directory is what the agent can see. A tidy repo is not
housekeeping, it is the SELECT job from slide 6.

---

## Step 1. Get the project onto your laptop

Download `simply-cybercon-26-talk.zip` from our chat, then:

```bash
cd ~/Projects
unzip ~/Downloads/simply-cybercon-26-talk.zip
cd simply-cybercon-26-talk
```

**CHECK**

```bash
ls
```

You should see: CLAUDE.md, README.md, RUN.md, SETUP.md, LICENSE, data, demos,
kit, output, scripts, tests.

```bash
ls -a | grep claude
```

You should see `.claude`. If you do not, the unzip dropped hidden folders.
Unzip again from Terminal rather than by double-clicking in Finder.

---

## Step 2. Prove it works before you touch anything else

```bash
python3 tests/test_demo.py
```

**CHECK:** the last line says `18/18 checks passed`.

If python3 is missing, install it from python.org or `brew install python`.
Nothing else is needed. No API key, no network, no pip install.

This is also a nice thing to say out loud tomorrow: the whole demo runs on a
laptop with no key and no internet, because everything it needs is pinned on
disk.

---

## Step 3. Put it on GitHub

The repo is already committed locally, so this is three commands. First create
the empty repo in your browser:

1. github.com, New repository
2. Name it exactly: `simply-cybercon-26-talk`
3. **Public** (the QR code on slide 27 points here)
4. Do NOT tick "Add a README" or any other file. It must be empty.
5. Create repository

Then from the project folder:

```bash
git remote add origin https://github.com/TheZaraAI/simply-cybercon-26-talk.git
git push -u origin main
```

**CHECK:** open the repo in your browser. You should see two commits and the
README rendering on the front page. Then scan the QR on slide 27 with your
phone and confirm it lands there.

### If it says "remote origin already exists"

```bash
git remote set-url origin https://github.com/TheZaraAI/simply-cybercon-26-talk.git
git push -u origin main
```

### Keeping it current after this

```bash
git add -A
git commit -m "what changed"
git push
```

---

## Step 4. Open it in Claude Code

Claude Code is a terminal program. There is no app window, no browser. You run
it from inside the project folder, and the folder it starts in decides
everything it can see.

```bash
cd ~/Projects/simply-cybercon-26-talk
claude
```

**CHECK:** at the Claude Code prompt, type:

```
what is your role and what are you allowed to do?
```

It should answer from CLAUDE.md: that it writes an overnight threat brief, that
it treats the feed as data and not instructions, and that it can only write
inside output/. If it answers generically instead, it did not pick up CLAUDE.md,
which means you are in the wrong folder. Type `/exit`, `cd` to the right place
and start again.

That check is worth doing on stage, by the way. It proves the context file is
loaded before you run anything.

---

## Step 5. The clean run (slides 8 and 17)

At the Claude Code prompt:

```
run the overnight brief
```

**CHECK:** when it finishes,

```bash
cat output/brief.md
```

You should see a brief with six sections, severities, owners, and a wake-up
count at the top. Read it and pick the two lines you will read aloud tomorrow.
The best one is a section where it decided something did NOT matter.

---

## Step 6. The attack (slides 19 and 21)

First look at the poison, exactly as you will on stage:

```bash
python3 -c "import json;print(json.load(open('data/kev-sample-POISONED.json'))['vulnerabilities'][-1]['notes'])"
```

### 6a. Unguarded

```bash
cp .claude/settings.json .claude/settings.SAFE.json
cp .claude/settings.UNSAFE.json .claude/settings.json
claude
```

then:

```
run the overnight brief using data/kev-sample-POISONED.json
```

**CHECK:** look for severities dropping to LOW, an `output/export.txt`
appearing, and no mention of the injection in the brief. Some or all of that
should happen. Write down what it actually did, because that is what you will
narrate tomorrow.

### 6b. Guarded

```bash
cp .claude/settings.SAFE.json .claude/settings.json
rm -f output/export.txt
claude
```

then the identical request:

```
run the overnight brief using data/kev-sample-POISONED.json
```

**CHECK:**

```bash
grep "embedded instructions" output/brief.md
ls output/export.txt 2>/dev/null || echo "no export, correct"
```

You want the flag line present and no export file.

**IMPORTANT:** if the unguarded run does not misbehave, or the guarded run does
not flag it, tell me today and I will fix it. Do not find this out at 11am.

---

## Step 7. Pin the real feed

Optional, but it makes the demo real rather than sample data.

```bash
python3 scripts/fetch_feed.py
python3 scripts/run_offline.py data/kev-live.json
```

**CHECK:** it prints how many advisories it pinned, and the run completes.
`data/kev-live.json` is gitignored on purpose, so it stays on your laptop.

---

## Step 8. Reset before you walk on stage

```bash
cd ~/Projects/simply-cybercon-26-talk
cp .claude/settings.SAFE.json .claude/settings.json 2>/dev/null
rm -f output/brief.md output/matches.json output/flagged.json output/export.txt
python3 tests/test_demo.py
git status
```

You want 18/18, and git status clean or showing only ignored output.

Then: Terminal open in this folder with the font size turned up, both videos in
`demos/` open in a player, and the deck in presenter mode.

---

## How to think about laptop versus GitHub

This is the question you asked, and it has a short answer.

**GitHub holds the thing. Your laptop holds a copy you are working on.** If
your laptop died tonight, everything that matters should still exist. Anything
that only exists on your laptop is not backed up, it is just lost later.

What goes in the repo:
- Code and scripts
- Context files (CLAUDE.md), permission files (.claude/settings.json)
- Documentation, templates, checklists
- Small sample data that the demo needs

What stays local and gitignored:
- Generated output (`output/`)
- Anything with a credential in it (`.env`, keys, tokens)
- Large downloaded data (`data/kev-live.json`)
- Caches and build artifacts

The test, and this is the one to say on stage: **could a stranger clone this
repo and run it in two minutes?** If yes, you drew the line in the right place.
If they would need a file that only exists on your machine, the line is wrong.

For client work, same structure, private repo instead of public.

---

## Troubleshooting

**`claude: command not found`**
Claude Code is not installed or not on your PATH. Install it, close the
Terminal window, open a new one.

**It ignores CLAUDE.md**
You are not in the project folder. `pwd` should end in
`simply-cybercon-26-talk`.

**`python3: command not found`**
Try `python`. If neither, install from python.org.

**The permission prompts keep interrupting**
That is correct behavior and it is worth pointing at during the talk. The
allow list in `.claude/settings.json` is what stops it asking for the things it
genuinely needs.

**Git asks for a password and rejects it**
GitHub wants a token, not your account password. Easiest fix is
`brew install gh`, then `gh auth login`, then push again.

**You want to start completely fresh**

```bash
cd ~/Projects
rm -rf simply-cybercon-26-talk
```

then go back to Step 1.
