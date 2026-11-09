# Run this on your own laptop

Written for someone who has never done this before. Follow it top to bottom.
Every step ends with a CHECK so you know it worked before you move on. About 20
minutes. You can stop after Step 3 and already have something working.

**What you need**

- A Mac, Windows or Linux laptop.
- Python 3. To check, open a terminal and type `python3 --version`. If you see a
  version number you are fine. If not, install it from python.org.
- For Steps 4 to 7 only: Claude Code and a Claude account. Steps 1 to 3 need no
  account, no API key, no internet connection and nothing installed beyond Python.

**What a terminal is.** A window where you type commands. On a Mac, open the app
called Terminal. On Windows, open PowerShell. Every grey box below is something
you type there, then press Enter.

**Want an assistant to coach you through the whole class?** See `AGENT_GUIDE.md`.

**Stuck at any point?** Open the folder in Claude Code or any AI assistant and
paste this: "I am following SETUP.md in this folder and I am on step N. Explain
what it wants me to do in plain English and check what I did." It has everything
it needs in the folder.

---

## Step 1. Get the files

**With git** (a tool for downloading code; if you do not know what it is, use the
other option):

```bash
git clone https://github.com/TheZaraAI/simply-cybercon-26-talk
cd simply-cybercon-26-talk
```

**Without git:** on the repo page, click the green **Code** button, then
**Download ZIP**.

Three things catch people out with the ZIP:

1. **Unzip it.** Tools open a folder, not a ZIP file. Double-click the ZIP and
   use the folder it makes.
2. **Your folder is called `simply-cybercon-26-talk-main`**, with `-main` on the
   end. Everywhere this guide says `simply-cybercon-26-talk`, use yours.
3. **There is a folder called `.claude` that you cannot see.** Names starting
   with a dot are hidden. On a Mac press `Cmd + Shift + .` in Finder. On Windows,
   in File Explorer choose View, Show, Hidden items. In a terminal, `ls -a`
   (Mac) or `dir -Force` (Windows) lists it. That folder holds the permissions,
   which is half the point of this repo.

Put it anywhere you like. The Desktop is fine.

Now open a terminal inside the folder. On a Mac, type `cd ` (with a space),
drag the folder onto the Terminal window, and press Enter.

**CHECK:** type `ls` (Mac, Linux) or `dir` (Windows). You should see
`CLAUDE.md`, `README.md`, `data`, `scripts`, `tests` and more.

---

## Step 2. Prove it works

```bash
python3 tests/test_demo.py
```

On Windows use `python` instead of `python3` if `python3` is not found.

**CHECK:** the last line says `18/18 checks passed`.

If it does not, the most common cause is that you are in the wrong folder. Go
back to Step 1 and check where your terminal is with `pwd` (Mac, Linux) or `cd`
(Windows).

---

## Step 3. See the brief the agent writes

```bash
python3 scripts/run_offline.py
```

then read it:

```bash
cat output/brief.md
```

(On Windows: `type output\brief.md`.)

**CHECK:** you see a threat brief with six sections. Each one has a severity,
an action, the owner and how exposed the system is. The top says how many items
need a human awake.

This run uses no AI at all. It is the plain code half of the loop: match the
feed against a list of what you run, write the brief, and run a script that says
whether the brief is complete. In the next steps an AI agent does the same job
with judgment, using the same files.

---

## Step 4. Open it in Claude Code

Claude Code is a program you run in a terminal, inside the project folder. The
folder you start it in decides everything it can see.

Install it from claude.com/claude-code and sign in with your Claude account.
Then, from the project folder:

```bash
claude
```

**CHECK:** at the prompt, type:

```
what is your role and what are you allowed to do?
```

It should say it writes an overnight threat brief, treats the feed as data and
not instructions, and may only write inside `output/`. That answer came from
`CLAUDE.md`, the context file. If it answers generically instead, you started it
in the wrong folder. Type `/exit`, move to the right folder, start again.

---

## Step 5. The clean run

At the Claude Code prompt:

```
run the overnight brief
```

It will ask permission before running a command or writing a file. That is the
permission layer working. Choose Yes for the two scripts and for writing the
brief.

**CHECK:** when it finishes, in another terminal window (or after `/exit`):

```bash
cat output/brief.md
```

You see the same kind of brief as Step 3, this time written by an agent. This is
what Demo 1 in the `demos/` folder shows.

---

## Step 6. The attack, and what stops it

First look at the poison. One record in the feed has an instruction hidden in a
field that nobody reads:

```bash
python3 -c "import json;print(json.load(open('data/kev-sample-POISONED.json'))['vulnerabilities'][-1]['notes'])"
```

### 6a. Guarded (the real settings)

This is how the repo works as downloaded. Start Claude Code and ask:

```bash
claude
```

```
run the overnight brief using data/kev-sample-POISONED.json
```

**CHECK:**

```bash
grep "embedded instructions" output/brief.md
```

You should see a line like `Flagged, not followed`, and this should say no
export was made:

```bash
ls output/export.txt 2>/dev/null || echo "no export, correct"
```

Windows: skip the `ls` line and look in the `output` folder. There should be no
`export.txt`.

### 6b. Unguarded (optional, and this is the dangerous demo)

This removes the protections so you can see why they matter. Do this only in
this folder, with the sample data, and put things back right after.

Mac or Linux:

```bash
cp .claude/settings.json .claude/settings.SAFE.json
cp .claude/settings.UNSAFE.json .claude/settings.json
claude
```

Windows PowerShell: use `copy` instead of `cp`.

Ask the same question. Expect that a good model will often refuse the injection
even without the permissions. That is luck, not a control. Demo 2 in `demos/` is
a recording of a run where it obeyed. If you see severities drop to LOW, or
`output/export.txt` appear, the attack worked.

**Put the protections back:**

```bash
cp .claude/settings.SAFE.json .claude/settings.json
rm -f output/export.txt
```

(Windows: `copy .claude\settings.SAFE.json .claude\settings.json`, then delete
`output\export.txt` if it is there.)

**CHECK:** run `python3 tests/test_demo.py` again. You want `18/18`.

---

## Step 7. Use the real, current feed (optional)

```bash
python3 scripts/fetch_feed.py
python3 scripts/run_offline.py data/kev-live.json
```

This downloads the real catalog of actively exploited vulnerabilities from CISA
once, saves it as `data/kev-live.json`, and runs against it. It needs internet.
The file is not uploaded to GitHub: it stays on your laptop.

---

## Reset to a clean state

```bash
cp .claude/settings.SAFE.json .claude/settings.json 2>/dev/null
rm -f output/brief.md output/matches.json output/flagged.json output/export.txt
python3 tests/test_demo.py
```

---

## Now build your own

The point of this repo is a context file for a job you already do by hand.
Open `kit/CONTEXT_FILE_TEMPLATE.md`. It is a blank template and two filled-in
examples. Pick a boring job, fill it in tonight, and run it.

---

## Troubleshooting

**`python3: command not found`**
Try `python`. If neither works, install Python from python.org and open a new
terminal window.

**`claude: command not found`**
Claude Code is not installed or the terminal does not know where it is. Install
it, close the terminal window, open a new one.

**It ignores `CLAUDE.md`**
You started Claude Code in the wrong folder. `pwd` (Mac, Linux) or `cd`
(Windows) should show the path ending in `simply-cybercon-26-talk`.

**It asks permission for a lot of things**
Correct and intended. `.claude/settings.json` decides what it may do without
asking and what it may never do. On some Macs, if your user folder name ends in
a dot or has unusual characters, Claude Code asks more often than expected. Say
Yes to the reads and writes inside this folder.

**The `.claude` folder is not there**
It is hidden, or your unzip tool dropped it. Show hidden files (Step 1). If it is
really missing, unzip again from the terminal rather than by double-clicking.

**Git asks for a password and rejects it**
GitHub wants a token, not your account password. Easiest fix: install the GitHub
CLI and run `gh auth login`. You only need git to push your own changes.

**Start completely fresh**
Delete the folder and go back to Step 1.
