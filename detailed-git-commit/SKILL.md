---
name: detailed-git-commit
description: Create accurate Git commits with inspected, detailed commit messages, automatic remote pushes after successful commits, and strict formatting. Use automatically when the user asks to commit changes, stage and commit, create a Git commit, commit and push, push committed changes after committing, write or amend a detailed commit message, verify the latest commit message, require every body line to start with a hyphen, or ensure the commit subject does not start with punctuation.
---

# Detailed Git Commit

## Objective

Create one factual Git commit from inspected changes. Commit only the scope the user requested and preserve unrelated work. Push after every successful commit unless the user explicitly asks not to push.

The commit subject must not start with a hyphen or other punctuation. Exactly one blank line separates the subject from the body. Every non-empty body line must start with `- `, except for an optional trailer block at the end.

## Workflow

1. Inspect the repository state with `git status --short`.
2. Read the diff before committing. Use `git diff --stat`, `git diff --cached --stat`, and targeted file diffs or file reads until the behavioural scope is clear.
3. If the user requested staged-only, commit exactly the staged diff. Do not stage additional files.
4. If the user did not specify staged-only, stage only the requested working tree changes. If the scope is ambiguous or unrelated changes look risky to include, ask before staging them.
5. Run `git diff --cached --check` after staging. Fix issues only when they are caused by the requested changes.
6. Write a subject that summarises the whole commit in one sentence and does not start with punctuation.
7. Leave one blank line after the subject, then write detailed body lines. Each body line must start with `- ` and describe a concrete change, risk reduction, test, or documentation update.
8. Commit with `git commit -F -` or an equivalent file-based message path so newlines are preserved exactly.
9. Verify with `git log -1 --pretty=format:%H%n%B` that the subject and all body lines match the required format. Also check `git log -1 --pretty=format:%s` prints only the subject; if body lines appear there, the blank separator line is missing. Fix any formatting problem with `git commit --amend` before pushing.
10. Confirm the final worktree state with `git status --short`.
11. Unless the user explicitly requested a local-only commit or no push, inspect `git status --branch --short` and remotes before pushing.
12. Push the current branch to its configured upstream with `git push`. If no upstream exists, use `git push -u <remote> <branch>` only when the intended remote and branch are clear.
13. Do not push when the branch is behind, diverged, or the target remote/branch is ambiguous. Report the blocker instead.
14. After a push, confirm the final branch state with `git status --branch --short`.

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
