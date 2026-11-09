# Prompting Is Dead. Long Live Context.

Simply Cyber Con 2026. Jax Scott, TheZaraAI.

Everything from the session: the agent you watched run, the context file, the
permissions that stopped the attack, the poisoned feed so you can run the
attack yourself, and five checklists.

## Start here: build your own

The point of this repo is not that you run my agent. It is that you write your
own context file tonight, for a job you already do.

**`kit/CONTEXT_FILE_TEMPLATE.md`** is the whole talk in one file: a blank
seven-section template, plus two complete worked examples filled in end to end.

- Example A is the vulnerability-brief agent you watched run.
- Example B is a daily threat brief written for publishing on social, which is
  the version to steal if the research is eating your morning. It is also a
  runnable folder: see `social-brief/`.

Read whichever is closer to your job, steal its shape, and change the Role,
Output and Voice sections. The other four sections barely change at all, and
that is the lesson.

## Following along in class with an AI assistant

Copy the prompt in [`AGENT_GUIDE.md`](AGENT_GUIDE.md) into any assistant. It will coach
you through the session as the speaker presents: where we are, what it means,
and what to try. Read the note there first if you use a coding agent, because
this folder's `CLAUDE.md` changes how one behaves.

## New to this?

Open `SETUP.md`. It assumes nothing: how to get the files, how to open a terminal,
what each command does, and a check after every step. If you get stuck, open
this folder in any AI assistant and ask it to walk you through `SETUP.md`.

The two demo videos are in `demos/`. Watch Demo 1 (the agent working) then Demo 2
(the same agent under attack) before you run anything.

## Run it in two minutes

```bash
git clone https://github.com/TheZaraAI/simply-cybercon-26-talk
cd simply-cybercon-26-talk
python3 scripts/run_offline.py
cat output/brief.md
```

No API key, no network, no setup. That is the mechanical part of the loop.

To run it as a real agent, open the folder in Claude Code and ask it to run
the overnight brief. `CLAUDE.md` is its context file. `.claude/settings.json`
is what it is allowed to touch.

## Run the attack on yourself

```bash
python3 scripts/match.py data/kev-sample-POISONED.json
```

One record in that feed carries an injection in its `notes` field. Point an
agent at it with permissive settings and watch what happens. Then put the
deny list back.

## What is in here

| Path | What it is |
|---|---|
| `CLAUDE.md` | The context file. Role, inputs, loop, definition of done, constraints |
| `.claude/settings.json` | What the agent can touch. The control |
| `.claude/settings.UNSAFE.json` | The "before" state, for the Act 3 demo only |
| `data/assets.csv` | A sample inventory |
| `data/kev-sample.json` | A sample advisory feed |
| `data/kev-sample-POISONED.json` | The same feed with one injected record |
| `scripts/fetch_feed.py` | Pin the real CISA KEV catalog |
| `scripts/match.py` | Match the feed against the inventory |
| `scripts/verify_brief.py` | The definition of done, as a script |
| `scripts/run_offline.py` | Deterministic fallback run, no model needed |
| `kit/` | The five checklists, including the context file template |
| `social-brief/` | A second runnable agent: the daily threat brief for social |
| `RUN.md` | The stage runbook |
| `tests/test_demo.py` | 18 checks covering every scenario in the talk |
| `demos/` | The two demo videos and what to watch for in each. See `demos/README.md` |
| `deck/` | The slides, as a PowerPoint file with the videos embedded. See `deck/README.md` |
| `AGENT_GUIDE.md` | Hand this to your AI assistant and it coaches you through the class |
| `SETUP.md` | Step by step, for beginners. Start here if this is new to you |

## Verify it does what the talk says

```bash
python3 tests/test_demo.py
```

18 checks: the clean run, the agent that stops early, the poisoned feed
guarded, the poisoned feed obeyed, and stage safety.

## The kit

- `kit/SECURE_YOUR_AGENT.md`: pre-deployment checklist
- `kit/AGENT_SCORECARD.md`: eight questions before any agent gets credentials
- `kit/CONTEXT_FILE_TEMPLATE.md`: the blank template plus two worked examples. Start here
- `kit/AGENT_LOOP_TEMPLATE.md`: plan, act, verify, decide
- `kit/COST_AND_BACKUP.md`: cut the bill, keep the checkpoints

## The three controls

1. Its own scoped credential, with an expiry. Never yours, never shared.
2. A human gate on anything irreversible. In the permissions, not the prompt.
3. Everything it reads is untrusted, and every tool call is logged.

## A second agent, ready to run

`social-brief/` is the same seven-section file pointed at content you publish
instead of a task you run. Paste twenty of your own posts into
`social-brief/voice/my-last-20-posts.md`, drop today's articles into
`social-brief/sources/pinned/`, and open the folder in Claude Code.

```bash
python3 social-brief/scripts/verify_post.py
```

That script is its definition of done. It fails a post for being too long, for
a statistic with no source, for anything on your banned-words list, and for any
sign that something tried to publish. Same idea as `verify_brief.py`, different
job. That is the point.

MIT licensed. Take it, change it, teach it.
