# Agent Loop Template

The difference between a chatbot and a coworker is the loop. A chatbot answers. An agent plans, acts, checks its own work, and decides whether to go again or stop.

Most broken agents are broken in one of two places: there is no verify step, or there is no stop condition.

Jax Scott, TheZaraAI. Simply Cyber Con 2026.

---

## The four steps

### 1. Plan
Before acting, the agent states what it is about to do and why, in one or two lines. This is not ceremony. It gives you a log line to read later, and it makes a drifting agent visible on the first iteration instead of the fifth.

### 2. Act
One tool call. Not a batch. One call, one result, then reassess. Batched actions hide which step went wrong.

### 3. Verify
The step everyone skips. The agent checks its own output against the definition of done, using something external to its own opinion:

- a script that returns pass or fail
- a schema the output must match
- a count that must reconcile
- a second cheap model pass asking only "does this meet the stated criteria, yes or no, and which criterion failed"

If verification is just the agent saying "looks good," you do not have a verify step.

### 4. Decide
Three outcomes only:
- **Done.** Verification passed. Stop and report.
- **Retry.** Verification failed, iterations remain, and the agent can name what to change. Go again.
- **Escalate.** Verification failed and the agent cannot name a fix, or the cap is hit. Stop and hand to a human with what it tried.

An agent that cannot escalate will invent success.

---

## The stop conditions

Write all four. Every one of them has saved somebody a bill or an incident.

```
MAX_ITERATIONS = 5          # hard stop on the loop
MAX_SPEND = $2.00           # hard stop on cost
MAX_RUNTIME = 10 minutes    # hard stop on wall clock
STOP_ON = any write failure, any auth error, any unexpected tool result
```

When a cap is hit, the run stops and escalates. It does not quietly return partial work as if it were finished.

---

## Writing a definition of done

Bad: "Produce a good summary of today's advisories."

Good:
```
done = output/brief.md exists
  AND it contains one section per asset in assets.csv with a matching advisory
  AND every section states severity and whether action is required
  AND zero sections contain the string "unverified"
```

The second one can be checked by a script in four lines. That script is your verify step.

---

## Pseudocode

```
plan = agent.plan(goal, context)
for i in range(MAX_ITERATIONS):
    result = agent.act(plan.next_action)      # one tool call
    log(plan.next_action, result)             # every call, always
    check = verify(output, done_criteria)     # external, not self-assessed
    if check.passed:
        return report(output)
    if not agent.can_name_a_fix(check):
        return escalate(check, attempts)
    plan = agent.replan(check.failure)
return escalate("iteration cap reached", attempts)
```

---

## The three failure modes this prevents

1. **The runaway.** No stop condition, so the agent loops until the bill arrives.
2. **The premature victory.** No verify step, so the agent reports success on empty output.
3. **The silent partial.** A cap is hit and the agent returns half the work without saying so.
