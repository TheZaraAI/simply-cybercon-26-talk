# Secure Your Agent

A pre-deployment checklist. Work through it before any agent gets credentials to anything that matters.

Jax Scott, TheZaraAI. Simply Cyber Con 2026.

---

## The one idea

An agent is a loop: it reads a goal, picks a tool, runs it, reads the result, picks the next tool, and keeps going until it decides it is done.

Two things control that loop. What the agent can **see**, and what the agent can **touch**.

Everything below is one of those two. Instructions are neither. "Read-only" written in a prompt is a wish. "Read-only" enforced by a token that cannot write is a control.

---

## Before it gets credentials

**Scope**
- [ ] The agent has one job, written down in one sentence.
- [ ] "Done" is defined in a way a machine can check, not "when it looks good."
- [ ] There is a maximum number of iterations and a maximum spend.

**Identity**
- [ ] The agent has its own credential. Not yours. Not a shared service account.
- [ ] That credential expires, and someone owns renewing it.
- [ ] Revoking this one agent does not break any other agent.

**What it can see**
- [ ] It has access to the data this job needs, and nothing adjacent.
- [ ] No chat history, ticket queue or shared drive is in scope "just in case."
- [ ] Secrets are not in its context window. Ever. Not in a file it reads, not in an example.

**What it can touch**
- [ ] Every tool it has is listed, by name, with what that tool can do.
- [ ] Nothing in that list can move money, send external mail, delete, deploy or grant access without a human.
- [ ] The write permissions are enforced by the token or the sandbox, not by instructions.

**What it reads from outside**
- [ ] Every external input is treated as data, never as instruction.
- [ ] The agent cannot be redirected by text inside a document, email, ticket, web page or feed.
- [ ] You have tested this with a deliberately poisoned input. You have seen what happens.

**Oversight**
- [ ] Every tool call is logged with inputs, outputs and a timestamp.
- [ ] Logs go somewhere a human actually reads, with an alert on anything unusual.
- [ ] There is a kill switch, a named person who can pull it, and they know they own it.

**Recovery**
- [ ] Config and context files are in version control.
- [ ] There is a checkpoint before each run, so a bad run is one revert away.
- [ ] You have tested the revert.

---

## The three controls, if you only do three

1. **Its own scoped credential.** Never your admin token, never a shared account.
2. **A human gate on anything irreversible.** Send, pay, delete, deploy, grant.
3. **Everything it reads is untrusted, and every tool call is logged.**

Those three would have contained most of the public agent incidents of 2026.

---

## The ten-minute version

If you have one agent running right now and ten minutes:

1. Find out which credential it uses. If it is yours, stop and fix that first.
2. List every tool it has. Remove anything that can move money or send mail externally.
3. Turn on logging for tool calls. Point it somewhere you will see it.
4. Write one sentence defining done, and an iteration cap.
5. Paste a poisoned instruction into something it reads, and watch what it does.

Step 5 is the one people skip and the one that changes behavior.
