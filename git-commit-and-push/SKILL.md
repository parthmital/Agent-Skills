---
name: git-commit-and-push
description: Create accurate Git commits with inspected, detailed commit messages, .gitignore upkeep so unwanted files are never committed, and an automatic push after each successful commit. Use when the user asks to commit, stage and commit, commit and push, push after committing, write or amend a commit message, or verify the latest commit message, including requests that every body line start with a hyphen or that the subject not start with punctuation.
---

# Git Commit And Push

Create one factual commit from inspected changes. Commit only the requested scope and leave unrelated work untouched. Update `.gitignore` before staging, and push after every successful commit unless the user says not to.

## Message Format

```text
Imperative subject summarising the whole commit

- Concrete change, risk reduction, test, or documentation update.
- Another concrete change.

Co-authored-by: Name <email>
```

- Subject: one concise imperative line covering the whole diff. It must not start with `-`, `*`, a number, or any other punctuation.
- Exactly one blank line after the subject. Without it, Git folds body lines into the subject.
- Every body line starts with `- `. No prose paragraphs and no other blank lines in the body.
- Trailers such as `Co-authored-by:`, `Signed-off-by:`, or `Refs:` appear only when the user, repository, or harness requires them, as a final block after one blank line, in plain `Key: value` form without `- `.
- Base every line on the inspected diff and use precise nouns, not "misc updates". Mention validation only if it actually ran. Never invent tests, migrations, deployment work, or fixes.
- Never create an empty commit unless explicitly asked.

## Workflow

1. Run `git status --short`, then read `git diff --stat`, `git diff --cached --stat`, and targeted diffs until the behavioural scope is clear.
2. Run Ignore Hygiene below.
3. Stage. For a staged-only request, commit exactly the staged diff plus any `.gitignore` change, and stage nothing else. Otherwise stage only the requested changes, and ask if the scope is ambiguous or unrelated changes look risky to include.
4. Run `git diff --cached --check`. Fix only issues caused by the requested changes.
5. Commit through stdin or a file so newlines survive exactly:

   ```bash
   git commit -F - <<'EOF'
   Subject

   - Body line.
   EOF
   ```

   In PowerShell, pipe a single-quoted here-string instead: `@'` ... `'@ | git commit -F -`, with the closing `'@` at column 0.

6. Verify with `git log -1 --pretty=format:%H%n%B` that the message matches the format, and that `git log -1 --pretty=format:%s` prints only the subject. Fix problems with `git commit --amend` before pushing. If the commit is already pushed, do not amend or force-push; report the problem.
7. Push unless the user asked for a local-only commit. Check `git status --branch --short` and the remotes, then run `git push`. With no upstream, use `git push -u <remote> <branch>` only when the target is clear. Do not push if the branch is behind or diverged or the target is ambiguous; report the blocker.
8. Confirm the final state with `git status --branch --short`.

## Ignore Hygiene

Run on every commit, including staged-only ones.

1. Review untracked files (`git status --short --untracked-files=all`) and everything staged or about to be staged.
2. Flag what does not belong in the repository:
   - dependencies and environments: `node_modules/`, `.venv/`, `venv/`, and installed (not deliberately committed) `vendor/`
   - build output: `dist/`, `build/`, `out/`, `.next/`, `target/`, `*.pyc`, `__pycache__/`, coverage reports, compiled binaries
   - caches, logs, and temp files: `.cache/`, `.pytest_cache/`, `*.log`, `*.tmp`, backups
   - local agent or tool work areas such as `.agent-local/`
   - editor and OS files: `.vscode/` and `.idea/` unless the project shares them, `.DS_Store`, `Thumbs.db`, `desktop.ini`
   - secrets and local config: `.env`, `.env.*` (keep `.env.example`), keys, certificates, credential files
   - large data, media, archives, or model files the project does not track on purpose
3. Add a pattern for each to the root `.gitignore` (create it if missing) or to the nearest `.gitignore` already covering that folder. Follow its grouping and comments, prefer folder or glob patterns, and skip patterns that already exist.
4. Never ignore what the project needs: source, lockfiles, `.env.example`, shared config, fixtures, or anything committed on purpose. Ask when unsure.
5. Confirm the rules with `git check-ignore -v <path>` and `git status --short`.
6. Put the `.gitignore` change in the same commit and mention it in a body line.
7. Ignoring does not untrack. If a tracked file matches a new rule, ask before `git rm --cached <path>`: the file stays on disk, but it is deleted for everyone who pulls.
8. If a secret is staged, unstage it and do not commit it. If one is already committed or pushed, stop and tell the user that ignoring it does not remove it from history and the secret should be rotated.
