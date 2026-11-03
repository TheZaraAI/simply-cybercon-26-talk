# Prompting Is Dead. Long Live Context.

Simply Cyber Con 2026. Jax Scott, TheZaraAI.

Everything from the session: the agent you watched run, the context file, the
permissions that stopped the attack, the poisoned feed so you can run the
attack yourself, and five checklists.

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
| `kit/` | The five checklists |
| `RUN.md` | The stage runbook |
| `tests/test_demo.py` | 18 checks covering every scenario in the talk |
| `demos/` | The two demo videos, cut in the deck's visual language |

## Verify it does what the talk says

```bash
python3 tests/test_demo.py
```

18 checks: the clean run, the agent that stops early, the poisoned feed
guarded, the poisoned feed obeyed, and stage safety.

## The kit

- `kit/SECURE_YOUR_AGENT.md` — pre-deployment checklist
- `kit/AGENT_SCORECARD.md` — eight questions before any agent gets credentials
- `kit/CONTEXT_FILE_TEMPLATE.md` — fill it in tonight
- `kit/AGENT_LOOP_TEMPLATE.md` — plan, act, verify, decide
- `kit/COST_AND_BACKUP.md` — cut the bill, keep the checkpoints

## The three controls

1. Its own scoped credential, with an expiry. Never yours, never shared.
2. A human gate on anything irreversible. In the permissions, not the prompt.
3. Everything it reads is untrusted, and every tool call is logged.

MIT licensed. Take it, change it, teach it.
