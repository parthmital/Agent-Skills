---
name: git-commit-and-push
description: Runs the full local CI until it passes, then makes accurate, logically scoped Git commits from inspected diffs in a strict hyphenated-body format, keeps .gitignore current, blocks secrets, and pushes. Use when the user asks to commit, stage and commit, commit and push, push after committing, write or amend a commit message, or verify the latest commit message.
---

# Git Commit and Push

## Overview

Commits that a reviewer can trust without reading the diff: each one logically scoped, made only after every test, check, and CI job passes locally, with every body line taken from the inspected diff, no secrets or generated files, the user's unrelated work left unstaged, and a push afterwards unless the user says not to.

## When to Use

- Committing, amending, or verifying a commit message, with or without pushing.
- Not for history rewrites or force pushes. Ask first.

## Message Format

```text
Imperative subject summarising the whole commit

- Concrete change, and why when the reason is not obvious from the change.

Co-authored-by: Name <email>
```

- Subject: one imperative line of at most about 72 characters covering the whole commit, never starting with `-`, `*`, a number, or other punctuation, no trailing full stop.
- Exactly one blank line after the subject. Every body line starts with `- `. No prose paragraphs or other blank lines.
- Trailers (`Co-authored-by:`, `Signed-off-by:`, `Refs:`) only when the user, repository, or harness requires them, as a final `Key: value` block after one blank line, without `- `.
- Every line comes from the inspected diff, with precise nouns, never "misc updates". Mention validation only if it ran. Never invent tests, migrations, deployments, or fixes.
- No em dashes or semicolons. No empty commits unless asked.

## Process

1. **Inspect.** `git status --short`, `git diff --ignore-cr-at-eol --stat`, `git diff --cached --stat`, and targeted diffs until the behavioural scope is clear.
2. **Scope.** One logical change per commit. When the diff mixes unrelated changes (a refactor and a feature, formatting and behaviour, two separate fixes), split it into several commits, staging by path or hunk (`git add -p` is interactive and unavailable to agents, so stage whole files or apply a patch with `git apply --cached`). Ask if the split is ambiguous.
3. **Ignore Hygiene** (below), on every commit.
4. **Docs.** Every doc the diff affects (README, other docs, skill files, docstrings, comments, help text) is updated. Update stale ones before continuing.
5. **Local CI** (below). Do not commit or push until it passes.
6. **Stage.** For a staged-only request, commit exactly the staged diff plus any `.gitignore` change and fixes made during the task. Otherwise stage the requested changes and every fix made with them, leaving the user's unrelated uncommitted work unstaged.
7. **Gate.** `git diff --cached --check` passes, and the staged diff holds no secret: scan with `gitleaks git --staged` when installed (`gitleaks protect --staged` before 8.19), else search the staged diff for key, token, password, and private-key patterns. A staged secret is unstaged, never committed.
8. **Commit** with `git commit -F -` from stdin or a file so newlines survive (bash: quoted heredoc, PowerShell: single-quoted here-string with `'@` at column 0).
9. **Check** `git log -1 --pretty=format:%H%n%B` matches the format and `git log -1 --pretty=format:%s` prints only the subject. Fix with `--amend` before pushing. If already pushed, report instead of amending or force-pushing.
10. **Push** unless asked for local only. Check `git status --branch --short` and remotes, then `git push`. With no upstream, `git push -u <remote> <branch>` only when the target is clear. If behind, diverged, or ambiguous, report the blocker. Confirm with `git status --branch --short`.

## Local CI

1. Find every check: CI workflows (`.github/workflows/`, `.gitlab-ci.yml`, `azure-pipelines.yml`, `Jenkinsfile`, `.circleci/`), task runners and manifests (`package.json` scripts, `Makefile`, `justfile`, `tox.ini`, `noxfile.py`, `pyproject.toml`), pre-commit hooks, and documented check commands.
2. Run every CI job's steps locally, plus every test, lint, format, type, and build check, with the same commands and options CI uses. A long, verbose suite may run in a `task-worker` at `low` effort that returns only failing output, when `subagent-delegation` shows it is cheaper. The final full pass runs in the main session.
3. Fix every failure, including ones the requested changes did not cause, and rerun everything until all pass in one run. Commit the fixes with body lines describing them.
4. A job that cannot run locally (deploy steps, required secrets, unavailable OS or service, or notebook execution, which `kaggle-jupyter-notebooks` forbids locally) blocks the commit: report it and ask before committing without it. With no tests or CI at all, say so and run whatever checks exist.

## Ignore Hygiene

1. Review `git status --short --untracked-files=all` and everything staged or about to be.
2. Flag what does not belong: dependencies and environments (`node_modules/`, `.venv/`, installed `vendor/`), build output (`dist/`, `build/`, `.next/`, `target/`, `__pycache__/`, coverage, binaries), caches, logs, temp files, backups, agent work areas (`.agent-local/`, `.cache/`), editor and OS files (`.vscode/` and `.idea/` unless shared, `.DS_Store`, `Thumbs.db`, `desktop.ini`), secrets and local config (`.env`, `.env.*` except `.env.example`, keys, certificates, `*.pem`), and large data, media, archives, or models not tracked on purpose.
3. Add patterns to the root or nearest `.gitignore`, following its grouping, preferring folder or glob patterns, skipping existing ones. Never ignore source, lockfiles, `.env.example`, shared config, fixtures, or deliberately committed files. Ask when unsure.
4. Confirm with `git check-ignore -v <path>`, and include the `.gitignore` change in the same commit with a body line.
5. Ignoring does not untrack. Ask before `git rm --cached <path>`: it deletes the file for everyone who pulls.
6. A secret already committed or pushed: stop and tell the user that history still holds it and it must be rotated.

## Examples

Bad (vague subject, prose body):

```text
Updates

Fixed some stuff in the parser and the tests.
```

Good:

```text
Reject expired tokens in session middleware

- Return 401 when the JWT `exp` claim is in the past, so stale sessions cannot reach handlers.
- Add regression tests for expired and missing `exp` claims.
- Document the 401 response in the README API table.
```

Bad scope: one commit titled `Refactor parser and add CSV export` mixing a rename across 30 files with a new feature. Good: `Rename parser modules by responsibility` first, then `Add CSV export to the report page`.

## Common Rationalisations

| Rationalisation                  | Reality                                                               |
| -------------------------------- | --------------------------------------------------------------------- |
| "`git add -A` is faster"         | It sweeps in unrelated work, build output, and secrets.               |
| "One big commit is simpler"      | Mixed commits cannot be reviewed, reverted, or bisected cleanly.      |
| "The subject says enough"        | Reviewers need the body to see what changed without reading the diff. |
| "Tests probably pass"            | Only mention checks that actually ran.                                |
| "CI will catch it"               | Run the full pipeline locally and get it green before committing.     |
| "That failure was already there" | Fix it anyway. Commit only when everything passes.                    |
| "I'll just force-push the fix"   | Rewriting pushed history breaks collaborators. Report instead.        |

## Red Flags

- Body lines that are prose, or describe changes not in the diff.
- Generated files, `.env`, keys, or caches in `git diff --cached --stat`.
- A refactor and a behaviour change in one commit.
- Pushing while behind or diverged.
- Committing after a failing, skipped, or partial check run.
- Behaviour, command, or path changes with no matching documentation update.

## Verification

- [ ] Every test, check, and CI job ran locally and passed in one final run before the commit, or the blocker was reported.
- [ ] Each commit holds one logical change, with every doc it affects updated.
- [ ] Commit contains the requested scope, any `.gitignore` update, and every fix, and none of the user's unrelated uncommitted work.
- [ ] Staged diff scanned for secrets, and no ignorable files committed.
- [ ] `git log -1` shows a clean subject, one blank line, `- ` body lines, and trailers only if required.
- [ ] Pushed, or the blocker or local-only request reported, with the final `git status --branch --short` shown.
