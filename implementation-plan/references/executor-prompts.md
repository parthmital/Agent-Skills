# Executor Prompts

Copy these into `START-HERE.md` under Prompts, with `<plan>` replaced by the plan folder path, for the tools the user named (all of them if none). Command behaviour was checked against official docs on 2026-10-26 (see the repository's `RESEARCH.md`); tools change fast, so tell the user to fall back to the plain prompt if a command is missing.

## Run Prompt

One prompt runs the whole plan. It has two parts:

- **RUN**: `Read <plan>/START-HERE.md and follow its rules. Work through <plan>/CHECKLIST.md from the first unticked line to the last, in order, without stopping between lines: do each Task line exactly as its file says, expand each Expand line with the plan's expansion procedure and continue into the tasks it adds, and do each Reference pass line as its file says. Human-only work goes to <plan>/OWNER-QUEUE.md and never stops the run. Use the unblock procedure in START-HERE.md before logging any blocker.`
- **DONE**: `Done when no line in <plan>/CHECKLIST.md is unticked ([ ]) and the last commit is pushed with git status --short --branch clean, or when a blocker remains after the unblock procedure and is logged in CHECKLIST.md and pushed.`

The prompt is idempotent: it always starts at the first unticked line. If the conversation ends early (context limit, quota, crash), start a new conversation and paste the same prompt.

## Antigravity (App and CLI)

1. New conversation, pick the model (for example Gemini Flash).
2. Send `/goal RUN DONE`. Goal mode blocks the agent from ending its turn before the completion evidence exists, so it keeps working through the checklist instead of stopping after one task.
3. If the run stops on a logged blocker: on a paid plan, `/boost Fix the blocker logged in <plan>/CHECKLIST.md as START-HERE.md's unblock procedure says, then continue the run. RUN DONE`. Otherwise run the Blocked Run prompt below with a stronger model, then paste `/goal RUN DONE` again.

Do not use `/plan` (the plan exists) or `/teamwork-preview` (parallel agents on one branch conflict with a sequential checklist).

## Claude Code

1. `/model` to pick the cheaper model. Use auto mode or allow the check commands, so goal turns run unattended.
2. Send `/goal RUN DONE`. A separate evaluator checks the condition after each turn. Claude Code compacts context automatically, so one session can run long.

## Codex (CLI, App, IDE)

1. New session, pick the model.
2. Send `/goal RUN DONE` (Codex 0.128.0 or later). `/goal pause`, `/goal resume`, and `/goal clear` control it.

## OpenCode (including local models)

1. `/new`, `/models` to pick the model, and Tab until the Build agent is active (Plan cannot edit files).
2. Send `RUN DONE` as a plain message. OpenCode has no goal mode, so when the model stops before DONE holds, send `Continue. RUN DONE`.
3. Local models with small context windows: start a new session every few tasks with the same message; the checklist carries the state.

## Any Other Tool

Gemini CLI, Cursor, Copilot, Kilo Code, and similar: new session, then `RUN DONE`, in the tool's autonomous or goal mode if it has one. Paste it again whenever the tool stops early.

## Blocked Run

For a stronger model when the run stops on a blocker:

`The run of <plan>/CHECKLIST.md stopped on the blocker logged under Blockers. Find the root cause, fix it, finish that line exactly as its file says, correct the task file with a dated revision note if its instructions were wrong, remove the blocker entry, commit, and push. Do only that line, then stop.`

Then paste the run prompt again with the cheaper model.

## Final Review

After the last line, optionally have the planning model review the result against the plan: `/code-review` in Claude Code or `/review` in Codex.
