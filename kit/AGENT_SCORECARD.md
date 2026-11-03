# Agent Scorecard

Eight questions to ask before any agent gets credentials to your environment. Ask them of your own build, your vendor, or your MSP, and ask for the answers in writing.

Score each 0, 1 or 2. Under 10 of 16 means do not deploy yet.

Jax Scott, TheZaraAI. Simply Cyber Con 2026.

---

**1. What credential does this agent use, and who else uses it?**
Good: its own identity, scoped to this job, with an expiry and a named owner.
Red flag: a personal account, an admin token, or a shared service account that three other things also use.

**2. List every tool it can call, and what each one can do.**
Good: a short explicit list, with write actions called out separately.
Red flag: "it has access to the workspace," or nobody can produce the list.

**3. Can it move money, send external email, delete, deploy, or grant access without a human?**
Good: no, and that is enforced by the token or the sandbox rather than by instructions.
Red flag: "we told it not to."

**4. What does it read that comes from outside your control?**
Good: a named list of inputs, all treated as data, with a tested example of a poisoned input being ignored.
Red flag: it reads email, tickets, web pages or feeds and nobody has tested what happens when one contains instructions.

**5. How does it know when it is done?**
Good: a machine-checkable condition, an iteration cap, and a spend cap.
Red flag: it runs until it decides it is finished.

**6. Where do its tool calls get logged, and who reads them?**
Good: every call logged with inputs and outputs, retained, alerting on anomalies, with a named human.
Red flag: no logs, or logs nobody has opened.

**7. How do you stop it right now?**
Good: a documented kill switch, a named person who owns it, and they have used it at least once in a test.
Red flag: "we would disable the API key, probably."

**8. When was this last reviewed by someone who did not build it?**
Good: within the last quarter, with findings and a closed-items list.
Red flag: never, or it was reviewed by the team that built it.

---

## Scoring

| Total | What it means |
|---|---|
| 14 to 16 | Deploy. Re-score quarterly. |
| 10 to 13 | Deploy with the gaps on a dated plan. |
| Under 10 | Do not give it credentials yet. |

The most common failing answers are 1, 4 and 7. They are also the three cheapest to fix.
