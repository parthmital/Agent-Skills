---
name: subagent-delegation
description: Minimises usage by having the main session orchestrate while low-cost worker subagents (Haiku 5.5 at xhigh effort in Claude Code) do the routine implementation, research, code analysis, documentation, and testing, from short written briefs, with cheap, risk-proportional validation by the orchestrator. Use before spawning any subagent, before reading many files or long output in the main session, when a task has independent parts or verbose side work (searches, audits, scans, bulk edits, long check runs), or when the user asks to delegate, parallelise, orchestrate, use subagents, or save usage limits.
---

# Subagent Delegation

## Overview

The goal is the lowest total usage for a correct result. Orchestrator tokens (Opus 5.5) cost several times worker tokens (Haiku 5.5), so the orchestrator spends them only on understanding the request, decisions, briefs, and validation. Everything a worker can do reliably goes to a worker. Every spawn also has a fixed cost: the brief, the worker's start-up context, and its report in the orchestrator's context. Delegate only when the orchestrator tokens saved exceed that cost.

## When to Use

- Before every subagent spawn, and before the orchestrator reads many files, long logs, or search results itself.
- `AGENTS.md` gives standing permission to spawn workers under this skill without asking.
- In a harness without subagents, keep the same discipline inline: read only what a decision needs.

## Roles

| Role              | Claude Code                                   | Spends tokens on                                                                                                 |
| ----------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Orchestrator      | Main session, Opus 5.5 at medium effort       | The request, decomposition, architecture and design decisions, risky or irreversible actions, briefs, validation |
| `task-worker`     | Haiku 5.5 at xhigh, all tools except spawning | One bounded change: implement, refactor, write tests or docs, run checks and fix failures, bulk mechanical edits |
| `research-worker` | Haiku 5.5 at xhigh, no file edits, web access | One bounded question: codebase search and analysis, external research, scanner runs, audits, fact checks         |

Spawn with `subagent_type: "task-worker"` or `"research-worker"` (definitions in this repository's `claude-code-agents/`, linked into `~/.claude/agents/`). If they are not installed, use any general agent with `model: "haiku"` and `effort: "xhigh"`. The `CLAUDE_CODE_EFFORT_LEVEL` environment variable overrides every subagent's effort, so leave it unset.

## Decide

Delegate by default. A task goes to a worker when all three hold:

- It has a clear deliverable and a cheap check that proves it: a test, a command, a quoted source, or a short diff.
- Its brief is shorter than the work: the context it needs is paths and facts, not this conversation.
- It would cost the orchestrator more than about five tool calls, or read more than a few hundred lines of files, logs, or search results.

Keep it with the orchestrator when any holds:

- It is a decision: architecture, technology choice, scope, trade-off, severity, or what to tell the user.
- A wrong result is costly or hard to detect: security fixes, data migrations, public API changes, irreversible or outward-facing actions.
- It is smaller than its brief, or the answer is already in the orchestrator's context.
- It needs back-and-forth with the user, or depends on results that do not exist yet.

Size tasks to minimise spawns: batch related small tasks into one worker rather than one worker each, and prefer one well-bounded worker over several that would read the same files. Decompose a vague goal before delegating any part of it.

## Parallelise

Parallel workers save wall time, not usage. Run them in parallel only when they are needed anyway and are independent:

- No worker needs another's output, and no two edit the same file. Overlapping edits run in sequence, or each with `isolation: "worktree"`.
- No two workers would read the same large material. Shared reading belongs in one worker.
- Each brief states its boundary ("only files under `src/billing/`") so work neither collides nor duplicates.

## Brief

A worker starts with no conversation history, so the brief is all it knows. Keep it short: paths instead of file contents, decisions instead of their history. Every brief has these seven parts:

1. Goal: the outcome in one sentence.
2. Context: exact paths, decisions already made, and the skills to load by name (`naming-conventions`, `repo-local-workspace`, and the task's own skill).
3. Scope: what to change or answer, and what to leave alone.
4. Constraints: the negative rules that matter here, such as no new dependencies, no commits or pushes, no weakening of tests, no notebook execution.
5. Deliverable: the shortest return format that lets you validate, because the report lands in the orchestrator's context. Never "return the file" or "paste the output".
6. Done when: the check to run and its expected result.
7. If blocked: stop and report what blocked and what was tried. Never guess or widen scope.

Bad brief: `Fix the billing tests.`

Good brief:

```text
Goal: make tests/billing pass after `calc_total` was renamed to `compute_invoice_total` in src/billing/totals.py (done, do not revert).
Context: callers still use the old name. Load naming-conventions. Python 3.11 at .venv/Scripts/python.
Scope: update call sites under src/ and tests/ only. Do not edit totals.py or any assertion.
Constraints: no new dependencies, no commits, no other refactors.
Deliverable: changed files, one line each, the final pytest summary line, anything unresolved.
Done when: `.venv/Scripts/python -m pytest tests/billing -q` passes and `git grep -n calc_total` prints nothing.
If blocked: stop and report the failing test and its error.
```

## Validate

A worker's report is a claim, not a fact. Validate with the cheapest check that proves the claim, scaled to risk, and never redo the work:

- Code: rerun the done-when command and read `git diff --stat`. Read the hunks only for risky or surprising files, not every line.
- Research: open the sources behind the claims a decision rests on. Accept the rest with their cited URL or `path:line`. Reject claims with neither.
- Audits and analysis: confirm a finding against the code only before acting on it.
- "Done" or "passing" without command output counts as unverified.
- Conflicting results: settle them by the evidence each cites, and read the code only when the evidence does not decide.
- The final repository checks run once, after all workers finish, not after each one.

## Recover

- Wrong or partial result: send one short follow-up to the same worker (it keeps its context) naming exactly what is wrong. Re-briefing a fresh worker repeats the start-up cost.
- A second failure, or a task harder than briefed: do it in the orchestrator or decompose it further. Never resend the same brief.
- Changes outside the boundary: inspect, revert them, and tighten the boundary in the next brief.

## Common Rationalisations

| Rationalisation                        | Reality                                                                                      |
| -------------------------------------- | -------------------------------------------------------------------------------------------- |
| "Doing it myself is safer"             | For routine, checkable work, a worker plus a cheap check gives the same result for less.     |
| "I'll just read these files quickly"   | Each file read in the orchestrator is paid at the expensive rate; a worker can summarise it. |
| "The worker said the tests pass"       | Rerun the one command; workers report optimistically.                                        |
| "Re-check everything the worker did"   | Validation that repeats the work erases the saving. Check the claim, not the whole effort.   |
| "Parallel is faster, so spawn more"    | Parallelism saves time, not usage. Each spawn adds start-up and report cost.                 |
| "The worker will work out the context" | It starts empty; missing context produces plausible, wrong work and a costly retry.          |

## Red Flags

- The orchestrator reading many files, logs, or search results that a worker could have summarised.
- A brief with no done-when check, or a deliverable that returns whole files or raw output.
- Many tiny workers where one batched worker would do, or parallel workers reading the same material.
- Validation that re-reads or redoes all of a worker's work.
- A delegated architecture, severity, scope, or irreversible decision.
- The same brief sent twice.

## Verification

- [ ] Every delegated task passed Decide, and related small tasks were batched.
- [ ] Every brief had all seven parts and asked for a short report.
- [ ] Parallel workers were independent, with disjoint file scopes and no shared reading.
- [ ] Every result validated with the cheapest proving check, and the repository checks ran once at the end.
- [ ] The final reply says what was delegated, what the orchestrator verified, and what remains unverified.
