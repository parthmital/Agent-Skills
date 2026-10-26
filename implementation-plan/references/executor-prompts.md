# Executor Prompts

Copy these into `START-HERE.md` under Prompts, with `<plan>` replaced by the plan folder path, for the tools the user named (all of them if none). Command behaviour was checked against official docs on 2026-10-26 (see the repository's `RESEARCH.md`); tools change fast, so tell the user to fall back to the plain prompt if a command is missing.

## Core Prompt

Every tool uses the same two parts:

- **NEXT**: `Read <plan>/START-HERE.md and follow its rules. Do the first unticked task in <plan>/CHECKLIST.md, exactly as its task file says, and nothing else.`
- **DONE**: `Done when every command in that task's Verify table gives its expected result, its box in CHECKLIST.md is ticked, and the commit is pushed with git status --short --branch clean, or when a blocker is logged in CHECKLIST.md.`

One task per fresh session keeps the weak model's context small and stops one task's mistakes from leaking into the next. Run the prompt again for the next task.

## Antigravity (App and CLI)

1. Start a new conversation for each task and pick the model (for example Gemini Flash).
2. Send `/goal NEXT DONE`. Goal mode blocks the agent from ending its turn before the completion evidence exists, which stops it quitting a task after a few minutes.
3. A task that stays blocked after the executor's attempts: on a paid plan, `/boost Fix the blocker logged for Task NN in <plan>/CHECKLIST.md, then finish Task NN exactly as its task file says. DONE`. Otherwise use the Blocked Task prompt below with a stronger model.

Do not use `/plan` (the plan exists) or `/teamwork-preview` (parallel agents on one branch conflict with a sequential checklist).

## Claude Code

1. `/clear`, then `/model` to pick the cheaper model once.
2. Use auto mode or allow the check commands, so goal turns run unattended.
3. Send `/goal NEXT DONE Stop after 40 turns.` Setting the goal starts the work; a separate evaluator checks the condition after each turn.

## Codex (CLI, App, IDE)

1. Start a new session for each task and pick the model.
2. Send `/goal NEXT DONE` (Codex 0.128.0 or later). `/goal pause`, `/goal resume`, and `/goal clear` control it.

## OpenCode (including local models)

1. `/new` for each task, `/models` to pick the model, and Tab until the Build agent is active (Plan cannot edit files).
2. Send `NEXT DONE` as a plain message. OpenCode has no goal mode, so if the model stops early, send: `Continue Task NN. DONE`.
3. Local models: prefer the largest context and best coding model the machine runs; if a task overflows the context, ask the planning model to split that task.

## Any Other Tool

Gemini CLI, Cursor, Copilot, Kilo Code, and similar: new session, then `NEXT DONE`. Use the tool's autonomous or goal mode if it has one.

## Whole Plan In One Session

Only for an executor strong enough to keep context across tasks, in a tool with a goal mode:

`/goal Complete every unticked task in <plan>/CHECKLIST.md in order, one at a time, following <plan>/START-HERE.md. Each task is done as its task file defines, with its own commit and push. Stop at the first logged blocker.`

## Blocked Task

For a stronger model, or the planning model, when a blocker is logged:

`Task NN in <plan>/CHECKLIST.md is blocked; the entry under Blockers has the error. Find the root cause, fix it, finish Task NN as its task file says, update the task file if its instructions were wrong, and remove the blocker entry in the same commit. DONE`

## Final Review

After the last task, optionally have the planning model review the result against the plan: `/code-review` in Claude Code or `/review` in Codex.
