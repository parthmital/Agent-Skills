---
name: implementation-plan
description: Writes a complete, exhaustive, end-to-end implementation plan as a folder of small, self-contained task files with a checklist, exact code, commands, expected results, and commit steps, plus ready-to-paste prompts and slash commands so a cheaper or weaker model (Gemini Flash in Antigravity, a smaller Claude, GPT, or a local model in OpenCode) can execute it task by task. Use when the user asks for an implementation plan, execution plan, handoff plan, task breakdown, step-by-step build plan, or a plan for another model, agent, or tool to execute.
---

# Implementation Plan

## Overview

A capable model does all the thinking once; a cheaper model only follows instructions. The plan therefore holds every decision, path, code block, command, and expected result, split into tasks small enough that a weak model finishes each in one short session without judgement calls.

## When to Use

- The user wants a plan that another model, agent, or session executes, or a full build plan for a large change.
- Not for a plan this same session will execute immediately; use the harness's plan mode.
- Not for research only (`internet-research`) or a whole-repo restructure done now (`production-architecture`).

## Output

```text
plans/<slug>/              <slug>: kebab-case name of the change
  START-HERE.md            executor rules, commands, and prompts per tool
  CHECKLIST.md             ordered task list with checkboxes, blockers log
  tasks/NN-<task-slug>.md  one self-contained task per file, NN = 01, 02, ...
```

Templates for all three files are in [references/plan-templates.md](references/plan-templates.md); the prompts per tool are in [references/executor-prompts.md](references/executor-prompts.md). Read both before writing.

## Process

1. Scope. Restate the goal as verifiable outcomes. Ask about every ambiguity that changes the result now: the executor cannot ask and will guess.
2. Research with `research-driven-development` and read the codebase: entry points, conventions, the files to change, and the exact install, test, lint, type-check, build, and run commands. Run the checks to record the baseline (pass counts, known failures).
3. Decide everything: libraries with exact versions, file layout, names, data shapes, interfaces, error handling, tests, and docs to update. Nothing is left as "choose", "appropriate", or "as needed".
4. Split into tasks. Each task:
   - has one observable outcome and ends in one commit that leaves every check passing;
   - touches about 5 files and 200 changed lines at most, so a weak model finishes it in about 15 minutes;
   - is ordered so its dependencies come first; scaffolding and shared code come before their users, and the last task is an end-to-end verification and documentation pass.
5. Write each task file from the template, self-contained: it repeats the context, decisions, and commands it needs instead of pointing to other tasks or a conversation.
   - New files and any non-trivial logic: the complete code. Weak models fail at algorithms, not typing.
   - Edits: the unique anchor text to find, then the exact replacement.
   - Tests in the same task as the code, written first where the repo has tests.
   - A Verify table of exact commands and expected results, and an exact commit message.
6. Write `CHECKLIST.md` and `START-HERE.md`, filling the prompts for the tools the user named, or all of them.
7. Cold-read review: read each task as an executor holding only that file and `START-HERE.md`. Fix every reference to unwritten context ("as above", "similar to Task 3", "etc."), every undecided choice, and every path or command that neither exists now nor is created by an earlier task.
8. Report the folder, task count, first prompt to paste, and any assumption the user should confirm. Commit the plan only when asked (`git-commit-and-push`); the executor needs it committed before Task 01.

## Rules

- The plan lives in the repository so progress survives sessions and tools: the checklist is the single source of task status.
- Every task ends with the full check suite, a commit in the repo's message format, and `git push` to the branch the user named (default `main`). One task, one commit.
- The executor never improvises around a failure: the task says how many fix attempts are allowed and how to log a blocker and stop.
- No code is repeated across tasks; later tasks quote only the anchor lines they need.
- Keep task files under about 300 lines; split a longer task.

## Common Rationalizations

| Rationalization                         | Reality                                                                     |
| --------------------------------------- | --------------------------------------------------------------------------- |
| "The executor can work out the details" | A weak model guesses differently each run; decide it in the plan.           |
| "One big plan file is easier to follow" | Weak models lose the thread and stop early; small files keep them on track. |
| "See Task 3 for the setup" is enough    | Each executor session starts empty; repeat what the task needs.             |
| "Tests can come in a final task"        | A broken early task then corrupts every later one.                          |

## Red Flags

- "TBD", "choose", "appropriate", "etc.", "similar to", or "as discussed" in a task.
- A task without a Verify table, an expected result, or a commit message.
- A task whose checks cannot pass until a later task is done.
- A command or path that was never confirmed in the repo or created by an earlier task.

## Verification

- [ ] Every outcome from step 1 maps to at least one task, and the final task proves the whole change end to end.
- [ ] Baseline checks were run and their commands and results appear in `START-HERE.md`.
- [ ] Each task passed the cold-read review and is within the size limits.
- [ ] `CHECKLIST.md` lists every task in order; `START-HERE.md` has the prompts for each target tool.
- [ ] Report lists assumptions and what was not verified.
