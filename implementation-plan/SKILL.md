---
name: implementation-plan
description: Writes a complete, exhaustive, end-to-end implementation plan as a folder of small, self-contained task files with a checklist, exact code, commands, expected results, and commit steps, plus one ready-to-paste prompt that makes a cheaper or weaker model (Gemini Flash in Antigravity, a smaller Claude, GPT, or a local model in OpenCode) execute the whole plan from the first task to release without stopping between tasks. The planning model only plans and never executes tasks. Use when the user asks for an implementation plan, execution plan, handoff plan, task breakdown, step-by-step build plan, or a plan for another model, agent, or tool to execute.
---

# Implementation Plan

## Overview

A capable model does all the thinking once; a cheaper model does all the doing. The plan holds every decision, path, code block, command, and expected result, split into tasks small enough that a weak model finishes each without judgement calls, and one prompt runs every task in order to the end.

The planner never executes the plan. It reads code and docs and runs cheap read-only commands (`git log`, `ls`, `cargo metadata`, `npm ls`, `--help`). It never builds, runs tests, trials migrations, edits product code, or commits anything but the plan. Every token the planner spends executing is the cost the plan exists to save, and the executor's fix attempts and unblock procedure catch what a trial would have.

## When to Use

- The user wants a plan that another model, agent, or session executes, or a full build plan for a large change.
- Not for a plan this same session will execute immediately; use the harness's plan mode.
- Not for research only (`internet-research`) or a whole-repo restructure done now (`production-architecture`).

## Output

```text
plans/<slug>/              <slug>: kebab-case name of the change
  START-HERE.md            executor rules, unblock procedure, the run prompt per tool
  CHECKLIST.md             ordered lines with checkboxes, blockers log
  OWNER-QUEUE.md           human-only work the executor queues without stopping
  tasks/NN-<task-slug>.md  one self-contained task per file, NN = 01, 02, ...
  milestones/, tools/, files/   only when needed: later-phase specs (step 4), helper scripts, files tasks copy (step 5)
```

Templates for these files are in [references/plan-templates.md](references/plan-templates.md); the prompts per tool are in [references/executor-prompts.md](references/executor-prompts.md). Read both before writing.

## Process

1. Scope. Restate the goal as verifiable outcomes. Ask about every ambiguity that changes the result now, including decisions only the owner can make (licences, legal, paid services): the executor cannot ask. Give each owner decision a default the executor uses until the owner answers, so no decision stops the run.
2. Research with `research-driven-development` and read the codebase: entry points, conventions, the files to change, and the exact install, test, lint, type-check, build, and run commands from the repo's docs and CI config. Do not run them: Task 01 records the baseline, and later tasks' "Before You Start" refer to the previous task's result.
3. Decide everything: libraries with exact versions, file layout, names, data shapes, interfaces, error handling, tests, and docs to update. Nothing is left as "choose", "appropriate", or "as needed".
4. Split into tasks. When the scope needs more than about 60 tasks, or later work depends on code not yet written, write only the first phase as tasks and each later phase as a milestone spec (scope, fixed decisions, interfaces, ordered task outline, acceptance criteria) behind an `Expand` checklist line. The executor expands it with the plan's expansion procedure in the same run and continues straight into the new tasks. Each task:
   - has one observable outcome and ends in one commit that leaves every check passing;
   - touches about 5 files and 200 changed lines at most, so a weak model finishes it in about 15 minutes;
   - is ordered so its dependencies come first; scaffolding and shared code come before their users, and the last task is an end-to-end verification and documentation pass.
5. Write each task file from the template, self-contained: it repeats the context, decisions, and commands it needs instead of pointing to other tasks or a conversation.
   - New files and any non-trivial logic: the complete code. Weak models fail at algorithms, not typing. Long code goes in `<plan>/files/`, copied by the task and checked by SHA-256; mechanical multi-file edits go in a script in `<plan>/tools/`.
   - Risky steps (dependency upgrades, edition or framework migrations): write the steps from the upstream changelog and migration guide, list the breaking changes that touch this repo's code with the expected compiler errors and their fixes, and give a fallback (stay on the previous version and log it). Never trial them yourself.
   - Edits: the unique anchor text to find, then the exact replacement.
   - Tests in the same task as the code, written first where the repo has tests.
   - Human-only work (captures, measurements, signing, legal review, third-party approval): the task does everything a model can, adds an entry to `OWNER-QUEUE.md`, marks its line `[~]`, and continues. A later `Reference pass` line finishes `[~]` lines whose owner input has arrived. No checklist line is human-only.
   - A Verify table of exact commands and expected results, and an exact commit message.
6. Write `CHECKLIST.md`, `OWNER-QUEUE.md`, and `START-HERE.md`, with the run prompt for the tools the user named, or all of them.
7. Cold-read review: read each task as an executor holding only that file and `START-HERE.md`. Fix every reference to unwritten context ("as above", "similar to Task 3", "etc."), every undecided choice, and every path or command that neither exists now nor is created by an earlier task. Check anchors statically: a script confirms each anchor occurs exactly once in the file as it will be when that task runs (current file, or after the earlier tasks' literal edits). No builds or test runs.
8. Report the folder, task count, the one prompt to paste, owner decisions taken by default, and what was not verified. Commit the plan only when asked (`git-commit-and-push`); the executor needs it committed before Task 01.

## Rules

- The plan lives in the repository so progress survives sessions and tools: the checklist is the single source of task status.
- One prompt runs the whole plan. The executor loops: first unticked line, do it, commit, push, next line, until no `[ ]` line is left. The prompt is idempotent, so pasting it again in a new conversation resumes after a context limit, quota stop, or crash.
- Every task ends with the full check suite, a commit in the repo's message format, and `git push` to the branch the user named (default `main`). One task, one commit.
- The executor never improvises around a failure: each task allows 3 fix attempts, then `START-HERE.md`'s unblock procedure (root cause, correct the task file with a dated revision note, 3 more attempts). Only then does it log a blocker, push, and stop the run.
- No code is repeated across tasks; later tasks quote only the anchor lines they need.
- Keep task files under about 300 lines; split a longer task.

## Common Rationalizations

| Rationalization                               | Reality                                                                                       |
| --------------------------------------------- | --------------------------------------------------------------------------------------------- |
| "The executor can work out the details"       | A weak model guesses differently each run; decide it in the plan.                             |
| "I'll trial the risky task myself to be sure" | That spends the expensive model on execution; write the migration notes and fallback instead. |
| "I'll just do Task 01 while I'm here"         | Same cost problem; the executor does every task, including the first.                         |
| "One big plan file is easier to follow"       | Weak models lose the thread and stop early; small files keep them on track.                   |
| "See Task 3 for the setup" is enough          | The executor may resume in a fresh conversation; repeat what the task needs.                  |
| "A HUMAN line can just stop the run"          | Then one prompt cannot finish the plan; queue the human work and continue.                    |
| "Tests can come in a final task"              | A broken early task then corrupts every later one.                                            |

## Red Flags

- The planner built, tested, migrated, or committed product code.
- A checklist line that ends the run by design ("commit and stop", "next session", a human-only line).
- "TBD", "choose", "appropriate", "etc.", "similar to", or "as discussed" in a task.
- A task without a Verify table, an expected result, or a commit message.
- A task whose checks cannot pass until a later task is done.
- A command or path that was never confirmed in the repo or created by an earlier task.

## Verification

- [ ] Every outcome from step 1 maps to at least one task, and the final task proves the whole change end to end.
- [ ] The planner ran no build, test, or migration and committed no product code; Task 01 records the baseline.
- [ ] One prompt in `START-HERE.md` runs every line to the end; nothing stops the run except a blocker after the unblock procedure.
- [ ] Each task passed the cold-read review and static anchor check and is within the size limits.
- [ ] `CHECKLIST.md` lists every line in order; owner decisions have defaults; human-only work goes to `OWNER-QUEUE.md`.
- [ ] Report lists owner decisions taken by default, assumptions, and what was not verified.
