# Plan Templates

Fill every `<placeholder>`. Delete template lines that do not apply; never leave a placeholder in the plan.

## START-HERE.md

```markdown
# <Plan title>

Goal: <one or two sentences: the end state when every line is done>.

## Rules For The Executor

1. Run the whole checklist in one go: take the first `[ ]` line in `CHECKLIST.md`, do it, commit, push, then take the next. Do not stop between lines. For each line read only `START-HERE.md`, that line's file, and the files it names.
2. Follow each task's steps exactly and in order. Do not refactor, rename, reformat, upgrade, or "improve" anything the task does not name.
3. A task is done only when every command in its Verify table gives the expected result, its box is ticked, and the commit is pushed.
4. Never edit or delete tests to make them pass, skip a check, add a dependency the task does not name, or use `--no-verify` or `--force`.
5. Human-only work never stops the run: do everything a model can, add the entry the task gives to `OWNER-QUEUE.md`, mark the line `[~]`, commit, push, continue. Never fake the owner's input.
6. Failure: after the task's 3 fix attempts, follow the Unblock Procedure below. Only after it fails, log the blocker, push, and stop.
7. After each commit, keep only what the next line needs: re-read files rather than relying on memory of earlier tasks.
8. Ignore files that show as changed only because of line endings: `git diff --ignore-cr-at-eol --stat` does not list them.

## Unblock Procedure

1. Read the whole error and the code it names. State the root cause in one sentence.
2. If the task file is wrong (an anchor that no longer matches, an API that changed, a wrong expected value), correct the task file and add `Revision <date>: <what changed and why>` at its end.
3. Fix within the task's file list, plus files the root cause proves must change. At most 3 more attempts, rerunning every Verify command each time.
4. Still failing: discard code changes, append under Blockers in `CHECKLIST.md`: `<line ID>, <date>: <root cause>`, the failing command, and the last 20 lines of its output. Commit only `CHECKLIST.md`, push, stop the run.

## Project Facts

- Stack: <languages, frameworks, versions>.
- Install: `<command>`.
- Checks (run all before every commit): `<test command>`, `<lint command>`, `<type-check command>`, `<build command>`.
- Baseline: recorded by Task 01 in its Verify table.
- Branch: `<main>`. Commit format: <the repo's format, one example>.

## Prompts

<Run prompt and per-tool steps from references/executor-prompts.md, with <plan> filled in.>
```

## CHECKLIST.md

```markdown
# Checklist: <Plan title>

States: `[ ]` to do, `[x]` done, `[~]` done except owner input queued in `OWNER-QUEUE.md`. Change the box in the same commit that completes the line. Work top to bottom without stopping.

- [ ] 01 <task title> (`tasks/01-<slug>.md`)
- [ ] 02 <task title> (`tasks/02-<slug>.md`)
- [ ] Reference pass: finish `[~]` lines whose owner input has arrived (`tasks/NN-reference-pass.md`)

## Blockers

<!-- Executor: only after the Unblock Procedure fails, append "<line ID>, <date>: <root cause>", the failing command, and the last 20 lines of its output, then stop. -->
```

## OWNER-QUEUE.md

```markdown
# Owner Queue

Human-only work the executor needs. The run continues without it; a Reference pass line finishes the dependent `[~]` lines once the input exists. Do items in any order, at any time, including while the run is going.

| ID  | Needed by line | What to do (exact steps) | Where to put the result | Status |
| --- | -------------- | ------------------------ | ----------------------- | ------ |

<!-- Executor: append one row per request, Status "Open". Owner: set Status to "Done <date>" when the result is in place. -->
```

## tasks/NN-slug.md

````markdown
# Task NN: <title>

Depends on: <Task MM, or "nothing">. Size: <files touched, approximate lines>.

## Goal

<One or two sentences: the observable outcome of this task.>

## Before You Start

1. `git pull --ff-only`, then `git status --short`: the output must be empty (line-ending-only files excepted).
2. In `CHECKLIST.md`, no line before NN is `[ ]`, and this one is `[ ]`.
3. Run `<test command>`. Expected: <result after Task MM; for Task 01, "record the result as the baseline">.

## Context

<What exists now and why this task is needed. Every decision this task depends on, stated as fact ("Use library X 2.3.1 because ..."). The relevant current code, quoted with its path and line numbers. Conventions to copy, with a short example from the repo.>

## Steps

1. Create `<path>` with exactly this content:

   ```<language>
   <complete file>
   ```

2. In `<path>`, find this unique text:

   ```<language>
   <anchor lines>
   ```

   Replace it with:

   ```<language>
   <new lines>
   ```

3. Run `<command>`. Expected: <result>.

## Do Not

- Change files other than: `<path>`, `<path>`, `CHECKLIST.md`.
- <Task-specific traps, e.g. "Do not rename `foo`; Task 07 depends on the name.">

## Verify

| Command             | Expected result               |
| ------------------- | ----------------------------- |
| `<test command>`    | <N> passed, 0 failed          |
| `<lint command>`    | no errors                     |
| `<build command>`   | exits 0                       |
| `<behaviour check>` | <exact output or observation> |

## Commit And Push

1. Tick Task NN in `CHECKLIST.md` (`[~]` if this task queued owner work).
2. `git add <each path changed>` (never `git add -A`).
3. Commit with this message:

   ```text
   <subject>

   - <change>
   ```

4. `git push origin <main>`, then `git status --short --branch`: clean and not ahead. Continue with the next line.

## If Something Fails

- A Verify command fails: read the full error, fix it within the files listed in "Do Not", and rerun every Verify command. At most 3 attempts, then the Unblock Procedure in `START-HERE.md`.
- `git push` is rejected: run `git pull --rebase`, rerun Verify, push again. If the rebase conflicts, run `git rebase --abort` and follow the Unblock Procedure.
````
