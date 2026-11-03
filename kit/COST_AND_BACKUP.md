# Cost and Backup

Two unglamorous practices that decide whether your agent survives contact with production.

Jax Scott, TheZaraAI. Simply Cyber Con 2026.

---

## Part 1: Cutting token cost

Cost is a context problem. Almost every surprise bill traces back to a context window that grew without anyone watching.

**Measure first.** Log tokens in and out for every run. You cannot cut what you are not counting. One number per run, in the same log as your tool calls.

**The five cuts, in order of payoff:**

1. **Trim the context.** More context is not better context. Pass the three documents the task needs, not the folder. The model does not reward you for thoroughness, it charges you for it.
2. **Route by difficulty.** A cheap fast model triages and filters. The expensive model only sees what survived triage and only makes the judgment call. This is usually the single biggest saving.
3. **Summarize history.** On long runs, replace the transcript with a running summary. Keep the last two turns verbatim, compress everything older.
4. **Cap the iterations.** An iteration cap is a spend cap. See AGENT_LOOP_TEMPLATE.md.
5. **Cache the stable parts.** If the same instructions and reference data go into every call, cache them rather than resending.

**The trap:** retries. A failing agent that retries five times costs five times as much as one that escalates after two. Cost control and loop control are the same control.

---

## Part 2: Backing up agent work

An agent is software that changes its own behavior based on files. Treat those files like code.

**In version control, always:**
- The context file (CLAUDE.md, system prompt, instructions)
- Tool and permission configuration
- The definition of done and the verify script
- Example inputs and expected outputs

When output quality changes, the first question is "what changed in the context file," and git answers it in seconds.

**Checkpoint before every run:**
- Snapshot anything the agent will write to
- Keep the last N runs, not just the last one
- Tag the checkpoint with the config version that produced it

A bad run should cost you one revert, not one afternoon.

**Keep the run log:**
- Every tool call with inputs, outputs and timestamp
- Tokens and spend
- The verify result and why it passed or failed

That log is how you debug, how you prove what happened, and how you audit. It is also the first thing an incident responder will ask for.

**Test the revert.** A backup you have never restored is a theory. Restore one on purpose, once, before you need it.

---

## The weekly five minutes

- Read the run log for one run, start to finish.
- Check the token trend. Rising means context is growing somewhere.
- Confirm the checkpoints are being written and are not empty.
- Confirm the agent's credential has not quietly gained new scope.
