---
name: git-commit-and-push
description: Creates accurate Git commits from inspected diffs with a strict hyphenated-body message format, keeps .gitignore up to date so unwanted files are never committed, and pushes after each successful commit. Use when the user asks to commit, stage and commit, commit and push, push after committing, write or amend a commit message, or verify the latest commit message.
---

# Git Commit And Push

## Overview

One factual commit of the requested scope, with unrelated work left untouched, `.gitignore` updated first, and a push afterwards unless the user says not to.

## When to Use

- Committing, amending, or verifying a commit message, with or without pushing.
- Not for history rewrites or force pushes; ask first.

## Message Format

```text
Imperative subject summarising the whole commit

- Concrete change, risk reduction, test, or documentation update.

Co-authored-by: Name <email>
```

- Subject: one concise imperative line covering the whole diff, never starting with `-`, `*`, a number, or other punctuation.
- Exactly one blank line after the subject, or Git folds the body into it.
- Every body line starts with `- `. No prose paragraphs or other blank lines.
- Trailers (`Co-authored-by:`, `Signed-off-by:`, `Refs:`) only when the user, repo, or harness requires them, as a final `Key: value` block after one blank line, without `- `.
- Every line comes from the inspected diff, with precise nouns, not "misc updates". Mention validation only if it ran. Never invent tests, migrations, deployments, or fixes.
- No empty commits unless asked.

## Process

1. Read `git status --short`, `git diff --stat`, `git diff --cached --stat`, and targeted diffs until the behavioural scope is clear.
2. Run Ignore Hygiene.
3. Stage. For a staged-only request, commit exactly the staged diff plus any `.gitignore` change. Otherwise stage only the requested changes; ask if scope is ambiguous or unrelated changes look risky.
4. `git diff --cached --check`; fix only issues the requested changes caused.
5. Commit with `git commit -F -` from stdin or a file so newlines survive (bash: quoted heredoc; PowerShell: single-quoted here-string with `'@` at column 0).
6. Check `git log -1 --pretty=format:%H%n%B` matches the format and `git log -1 --pretty=format:%s` prints only the subject. Fix with `--amend` before pushing; if already pushed, report instead of amending or force-pushing.
7. Push unless asked for local only. Check `git status --branch --short` and remotes, then `git push`; with no upstream, `git push -u <remote> <branch>` only when the target is clear. If behind, diverged, or ambiguous, report the blocker instead.
8. Confirm with `git status --branch --short`.

## Ignore Hygiene

Run on every commit, including staged-only ones.

1. Review `git status --short --untracked-files=all` and everything staged or about to be.
2. Flag what does not belong: dependencies and environments (`node_modules/`, `.venv/`, installed `vendor/`), build output (`dist/`, `build/`, `.next/`, `target/`, `__pycache__/`, coverage, binaries), caches, logs, temp files, and backups, agent work areas (`.agent-local/`), editor and OS files (`.vscode/` and `.idea/` unless shared, `.DS_Store`, `Thumbs.db`, `desktop.ini`), secrets and local config (`.env`, `.env.*` except `.env.example`, keys, certificates), and large data, media, archives, or models not tracked on purpose.
3. Add patterns to the root or nearest relevant `.gitignore`, following its grouping, preferring folder or glob patterns, skipping existing ones. Never ignore source, lockfiles, `.env.example`, shared config, fixtures, or deliberately committed files; ask when unsure.
4. Confirm with `git check-ignore -v <path>`. Include the `.gitignore` change in the same commit with a body line.
5. Ignoring does not untrack. Ask before `git rm --cached <path>`: it deletes the file for everyone who pulls.
6. A staged secret is unstaged, not committed. If one is already committed or pushed, stop and tell the user that history still holds it and it must be rotated.

## Common Rationalizations

| Rationalization                | Reality                                                               |
| ------------------------------ | --------------------------------------------------------------------- |
| "`git add -A` is faster"       | It sweeps in unrelated work, build output, and secrets.               |
| "The subject says enough"      | Reviewers need the body to see what changed without reading the diff. |
| "Tests probably pass"          | Only mention checks that actually ran.                                |
| "I'll just force-push the fix" | Rewriting pushed history breaks collaborators; report instead.        |

## Red Flags

- Body lines that are prose, or describe changes not in the diff.
- Generated files, `.env`, or caches in `git diff --cached --stat`.
- Pushing while behind or diverged.

## Verification

- [ ] Commit contains only the requested scope plus any `.gitignore` update.
- [ ] `git log -1` shows a clean subject, one blank line, `- ` body lines, and trailers only if required.
- [ ] No secrets or ignorable files committed.
- [ ] Pushed, or the blocker or local-only request is reported; final `git status --branch --short` shown.
