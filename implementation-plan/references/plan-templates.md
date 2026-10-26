# Plan Templates

Fill every `<placeholder>`. Delete template lines that do not apply; never leave a placeholder in the plan.

## START-HERE.md

```markdown
# <Plan title>

Goal: <one or two sentences: the end state when every task is done>.

## Rules For The Executor

1. Work on exactly one task per session: the first unticked task in `CHECKLIST.md`. Read only `START-HERE.md`, `CHECKLIST.md`, and that task file, plus the files the task names.
2. Follow the task's steps exactly and in order. Do not refactor, rename, reformat, upgrade, or "improve" anything the task does not name.
3. A task is done only when every command in its Verify table gives the expected result, its box in `CHECKLIST.md` is ticked, and the commit is pushed.
4. Never edit or delete tests to make them pass, skip a check, add a dependency the task does not name, or use `--no-verify` or `--force`.
5. When stuck, follow the task's "If Something Fails" section: log the blocker in `CHECKLIST.md` and stop.
6. Ignore files that show as changed only because of line endings: `git diff --ignore-cr-at-eol --stat` does not list them.

## Project Facts

- Stack: <languages, frameworks, versions>.
- Install: `<command>`.
- Checks (run all before every commit): `<test command>`, `<lint command>`, `<type-check command>`, `<build command>`.
- Baseline on <date>: <e.g. "84 tests pass, lint clean, build succeeds">.
- Branch: `<main>`. Commit format: <the repo's format, one example>.

## Prompts

<Per-tool prompts from references/executor-prompts.md, with <plan> filled in.>
```

## CHECKLIST.md

```markdown
# Checklist: <Plan title>

Tick a box (`- [x]`) in the same commit that completes the task.

- [ ] 01 <task title> (`tasks/01-<slug>.md`)
- [ ] 02 <task title> (`tasks/02-<slug>.md`)

## Blockers

<!-- Executor: append "Task NN, <date>: <what failed>, <command and its last lines of output>" and stop. -->
```

## tasks/NN-slug.md

````markdown
# Task NN: <title>

Depends on: <Task MM, or "nothing">. Size: <files touched, approximate lines>.

## Goal

<One or two sentences: the observable outcome of this task.>

## Before You Start

1. `git pull --ff-only`, then `git status --short`: the output must be empty (line-ending-only files excepted).
2. In `CHECKLIST.md`, tasks before NN are ticked and this one is not.
3. Run `<test command>`. Expected: <baseline result after Task MM>.

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

1. Tick Task NN in `CHECKLIST.md`.
2. `git add <each path changed>` (never `git add -A`).
3. Commit with this message:

   ```text
   <subject>

   - <change>
   ```

4. `git push origin <main>`, then `git status --short --branch`: clean and not ahead.

## If Something Fails

- A Verify command fails: read the full error, fix it within the files listed in "Do Not", and rerun every Verify command. At most 3 attempts.
- Still failing, or the fix needs a file outside the list: do not commit. Append the blocker to `CHECKLIST.md` under Blockers with the failing command and the last 20 lines of its output, then stop and report.
- `git push` is rejected: run `git pull --rebase`, rerun Verify, push again. If the rebase conflicts, run `git rebase --abort`, log a blocker, and stop.
````
