---
name: subagent-delegation
description: Decides whether a piece of work is cheaper inline or in a low-cost worker subagent (Haiku 5.5 in Claude Code), picks the lowest effort level that will succeed, writes a short brief, and validates the result cheaply. Use before spawning any subagent, before reading many files, long logs, or many web pages in the main session, or when the user asks to delegate, parallelise, orchestrate, use subagents, or save usage limits.
---

# Subagent Delegation

## Overview

The goal is the lowest total usage for a correct result, not the most delegation. A Haiku 5.5 token costs about one fortieth of an Opus 5.5 token (API list prices: Haiku 5.5 $0.10 input and $0.50 output per million tokens, Opus 5.5 $4 and $20), but every spawn also pays fixed costs that land partly on the orchestrator:

- The orchestrator writes the brief (Opus output tokens) and later reads the report (Opus context, re-read on every later turn).
- The worker starts cold: system prompt, `AGENTS.md`, skill list, and tool definitions, with no shared prompt cache.
- The orchestrator validates the result, and a failed worker costs a retry or a redo.

So delegation pays only when the worker absorbs much more reading than the brief, report, and validation cost the orchestrator. Inline is the default.

## When to Use

- Before every subagent spawn, and before the orchestrator reads many files, long logs, or many web pages itself.
- `AGENTS.md` gives standing permission to spawn workers under this skill without asking.
- In a harness without subagents, keep the same discipline inline: read only what a decision needs.

## Process

1. **Decide.** Delegate only when all of these hold. Otherwise do the work inline.
   - The work would put a lot of material into the orchestrator's context: roughly 20 or more files, 1,500 or more lines, long logs or scanner output, or several web pages.
   - The result compresses to a short report (about 25 lines) that the orchestrator can check cheaply: a test or command, a quoted source, `path:line` evidence, or a short diff.
   - The brief is much shorter than the work: paths and decisions, not conversation history.
   - It is not a decision (architecture, technology, scope, severity, what to tell the user), not risky or hard to detect when wrong (security fixes, migrations, public API changes, irreversible actions), and needs no back-and-forth with the user.
2. **Size.** One worker per independent chunk of reading. Batch related small tasks into one worker. Never split work so two workers read the same material. Parallel workers save wall time, not usage: run them in parallel only when each is needed anyway, they are independent, and no two edit the same file (otherwise in sequence, or with `isolation: "worktree"`).
3. **Pick the model and effort.** `model: "haiku"`, with the lowest effort the table allows. Pass `effort` on the Agent call. Raise one level only after a failure caused by reasoning, not by a bad brief.

   | Effort   | Use for                                                                                                          |
   | -------- | ---------------------------------------------------------------------------------------------------------------- |
   | `low`    | Mechanical work with an exact recipe: bulk renames, format fixes, running a check suite and returning failures   |
   | `medium` | Default. Bounded searches and summaries, routine edits from a clear spec, fact lookups with sources              |
   | `high`   | Multi-step code analysis, research synthesis across sources, fixing failing tests whose cause is not given       |
   | `xhigh`  | Ceiling. Hard debugging or analysis that failed at `high`. Never `max`: the gain over `xhigh` rarely pays for it |

4. **Brief.** Seven parts, in this order, as short as possible:
   1. Goal: the outcome in one sentence.
   2. Context: exact paths, decisions already made, and the skills to load by name.
   3. Scope: what to change or answer, and what to leave alone.
   4. Constraints: the negative rules that matter here (no new dependencies, no commits, no weakening tests, no notebook execution).
   5. Deliverable: the shortest return format that lets you validate. Never "return the file" or "paste the output".
   6. Done when: the check to run and its expected result.
   7. If blocked: stop and report what blocked and what was tried. Never guess or widen scope.
5. **Validate** with the cheapest check that proves the claim, scaled to risk. Never redo the work.
   - Code: rerun the done-when command and read `git diff --stat`. Read hunks only for risky or surprising files.
   - Research: open the sources behind the claims a decision rests on. Accept the rest with their cited URL or `path:line`. Reject claims with neither.
   - Audits: confirm a finding against the code only before acting on it.
   - "Done" or "passing" without command output counts as unverified. Repository-wide checks run once, after all workers finish.
6. **Recover.** Wrong or partial result: one short follow-up to the same worker (it keeps its context) naming exactly what is wrong. A second failure: do it inline. Never resend the same brief. Revert any change outside the boundary.
7. **Measure.** On subscription plans, `/usage` in Claude Code shows the share of recent usage spent by subagents. If delegation is not lowering total usage, delegate less.

Spawn with `subagent_type: "task-worker"` (edits) or `"research-worker"` (read-only), defined in this repository's `claude-code-agents/` and linked into `~/.claude/agents/`. Their definitions default to `effort: medium`. Without them, use a general agent with `model: "haiku"` and an explicit `effort`. Leave `CLAUDE_CODE_EFFORT_LEVEL` unset: it overrides every subagent's effort.

## Examples

Inline, not delegated: "Rename `calc_total` in 4 files and rerun the tests." Reading 4 files costs less than a brief, a cold start, and a report.

Delegated: "Find every place the 30 services under `services/` read environment variables, and list each variable with `path:line`." Hundreds of files of reading compress into a short table that a `git grep` spot check validates.

Bad brief: `Fix the billing tests.`

Good brief (`task-worker`, `effort: "low"`, because the fix is fully specified):

```text
Goal: make tests/billing pass after `calc_total` was renamed to `compute_invoice_total` in src/billing/totals.py (done, do not revert).
Context: about 40 call sites under src/ and tests/. Load naming-conventions. Python 3.11 at .venv/Scripts/python.
Scope: update call sites under src/ and tests/ only. Do not edit totals.py or any assertion.
Constraints: no new dependencies, no commits, no other refactors.
Deliverable: changed files, one line each, the final pytest summary line, anything unresolved.
Done when: `.venv/Scripts/python -m pytest tests/billing -q` passes and `git grep -n calc_total` prints nothing.
If blocked: stop and report the failing test and its error.
```

## Common Rationalisations

| Rationalisation                        | Reality                                                                                           |
| -------------------------------------- | ------------------------------------------------------------------------------------------------- |
| "Haiku is 40 times cheaper, delegate"  | Only per token. Brief, cold start, report, validation, and retries often cost more than the work. |
| "Use xhigh to be safe"                 | Effort multiplies thinking tokens. Start at the lowest level the table allows.                    |
| "Parallel is faster, so spawn more"    | Parallelism saves time, not usage. Each spawn adds start-up and report cost.                      |
| "The worker said the tests pass"       | Rerun the one command. Workers report optimistically.                                             |
| "Re-check everything the worker did"   | Validation that repeats the work erases the saving. Check the claim, not the whole effort.        |
| "The worker will work out the context" | It starts empty. Missing context produces plausible, wrong work and a costly retry.               |

## Red Flags

- A worker spawned for work smaller than its brief, or for a decision.
- `effort: "xhigh"` on a mechanical or well-specified task.
- Several workers reading the same files, or many tiny workers where one batched worker would do.
- A brief with no done-when check, or a deliverable that returns whole files or raw output.
- Validation that re-reads or redoes all of a worker's work.
- The same brief sent twice.

## Verification

- [ ] Every spawn passed Decide, and the inline alternative was cheaper to skip.
- [ ] Each worker got the lowest fitting effort, and every brief had all seven parts.
- [ ] Parallel workers were independent, with disjoint file scopes and no shared reading.
- [ ] Every result validated with the cheapest proving check, and the repository checks ran once at the end.
- [ ] The final reply says what was delegated, at which effort, what the orchestrator verified, and what remains unverified.
