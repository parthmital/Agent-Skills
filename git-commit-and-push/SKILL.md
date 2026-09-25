---
name: git-commit-and-push
description: Create accurate Git commits with inspected, detailed commit messages, .gitignore upkeep so unwanted files are never committed, automatic remote pushes after successful commits, and strict formatting. Use automatically when the user asks to commit changes, stage and commit, create a Git commit, commit and push, push committed changes after committing, write or amend a detailed commit message, verify the latest commit message, require every body line to start with a hyphen, or ensure the commit subject does not start with punctuation.
---

# Git Commit And Push

## Objective

Create one factual Git commit from inspected changes. Commit only the scope the user requested and preserve unrelated work. Before staging, update `.gitignore` so nothing unnecessary is committed or pushed. Push after every successful commit unless the user explicitly asks not to push.

The commit subject must not start with a hyphen or other punctuation. Exactly one blank line separates the subject from the body. Every non-empty body line must start with `- `, except for an optional trailer block at the end.

## Workflow

1. Inspect the repository state with `git status --short`.
2. Read the diff before committing. Use `git diff --stat`, `git diff --cached --stat`, and targeted file diffs or file reads until the behavioural scope is clear.
3. Update ignore rules as described in [Ignore Hygiene](#ignore-hygiene) before staging anything.
4. If the user requested staged-only, commit exactly the staged diff. Do not stage additional files.
5. If the user did not specify staged-only, stage only the requested working tree changes. If the scope is ambiguous or unrelated changes look risky to include, ask before staging them.
6. Run `git diff --cached --check` after staging. Fix issues only when they are caused by the requested changes.
7. Write a subject that summarises the whole commit in one sentence and does not start with punctuation.
8. Leave one blank line after the subject, then write detailed body lines. Each body line must start with `- ` and describe a concrete change, risk reduction, test, or documentation update.
9. Commit with `git commit -F -` or an equivalent file-based message path so newlines are preserved exactly.
10. Verify with `git log -1 --pretty=format:%H%n%B` that the subject and all body lines match the required format. Also check `git log -1 --pretty=format:%s` prints only the subject; if body lines appear there, the blank separator line is missing. Fix any formatting problem with `git commit --amend` before pushing.
11. Confirm the final worktree state with `git status --short`.
12. Unless the user explicitly requested a local-only commit or no push, inspect `git status --branch --short` and remotes before pushing.
13. Push the current branch to its configured upstream with `git push`. If no upstream exists, use `git push -u <remote> <branch>` only when the intended remote and branch are clear.
14. Do not push when the branch is behind, diverged, or the target remote/branch is ambiguous. Report the blocker instead.
15. After a push, confirm the final branch state with `git status --branch --short`.

## Ignore Hygiene

Run this on every commit, including staged-only commits.

1. List every untracked file with `git status --short --untracked-files=all`, and review the files about to be staged or already staged.
2. Flag anything that should not be in the repository:
   - dependencies and environments: `node_modules/`, `.venv/`, `venv/`, `vendor/` when it is installed rather than committed deliberately
   - build and generated output: `dist/`, `build/`, `out/`, `.next/`, `target/`, `*.pyc`, `__pycache__/`, coverage reports, compiled binaries
   - caches, logs, and temporary files: `.cache/`, `.pytest_cache/`, `*.log`, `*.tmp`, backups
   - local agent or tool work areas, such as `.agent-local/`
   - editor and OS files: `.vscode/` and `.idea/` unless the project shares their settings, `.DS_Store`, `Thumbs.db`, `desktop.ini`
   - secrets and local configuration: `.env`, `.env.*` (keep `.env.example`), keys, certificates, credential files
   - large data, media, archives, or model files that the project does not track on purpose
3. Add a pattern for each flagged item to the repository root `.gitignore`, or to the nearest `.gitignore` that already covers that folder. Create a root `.gitignore` if none exists. Follow the file's existing grouping and comments, prefer folder or glob patterns over single file names, and do not duplicate patterns that already exist.
4. Never ignore files the project needs: source, lock files, `.env.example`, shared configuration, fixtures, or anything already committed on purpose. If unsure whether a file is intentional, ask.
5. Confirm the new rules work with `git check-ignore -v <path>` and `git status --short`.
6. Include the `.gitignore` change in the same commit and mention it in a body line, even for a staged-only commit.
7. `.gitignore` does not affect files that are already tracked. If a tracked file matches the new rules, ask before removing it from the index with `git rm --cached <path>`. The file stays on disk, but it is deleted for everyone else when they pull.
8. If a secret is staged, unstage it and do not commit. If a secret is already committed or pushed, stop and tell the user: ignoring it now does not remove it from history, and the secret should be rotated.

## Message Rules

- Keep the subject concise, imperative, and broad enough to cover the staged diff.
- Do not prefix the subject with `-`, `*`, or a number.
- Start every body line with `- `.
- Do not include blank explanatory paragraphs in the body. Blank lines are allowed only between the subject and body, and before the trailer block.
- Trailers such as `Co-authored-by:`, `Signed-off-by:`, or `Refs:` are allowed only as a final block after one blank line, only when the user, repository, or harness requires them, and they keep their standard `Key: value` form without a leading `- `.
- Base every body line on inspected changes. Do not invent tests, migrations, deployment work, or fixes.
- Mention validation only if it was actually run.
- Prefer precise nouns over vague categories like "misc updates".
- If there are no staged or requested changes, do not create an empty commit unless the user explicitly asked for one.

## Commit Command Pattern

Use a literal message body through standard input when practical. Note the blank line after the subject.

PowerShell:

```powershell
@'
Subject without leading hyphen

- First detailed body line.
- Second detailed body line.
- Validation line if checks were run.
'@ | git commit -F -
```

POSIX shell:

```bash
git commit -F - <<'EOF'
Subject without leading hyphen

- First detailed body line.
- Second detailed body line.
- Validation line if checks were run.
EOF
```

After committing, inspect the saved message before pushing. If formatting is wrong, amend it with a corrected message before the push. If the commit has already been pushed, do not amend or force-push; report the problem instead.
