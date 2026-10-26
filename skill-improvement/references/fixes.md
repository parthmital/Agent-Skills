# Fixes

Tool and environment problems that no other skill owns. Search by symptom text. Entry format: `- **<symptom>**: <cause>. <fix>. Check: <how>.` Move an entry into a skill once one owns its area.

## Skills

- **Installed skill differs from the source repository**: installed folders were copies, so edits made in one place drifted. Install each skill as a link to its repository folder (README Installation). Check: `diff -rq <installed>/<skill> <repo>/<skill>` prints nothing.

## Node and npm

- **`next dev` prints "Your version of Next.js is affected by a known security vulnerability" and exits**: `node_modules` is older than `package-lock.json` (often after a merged dependency bump), so the installed `next` is the vulnerable one. Run `npm ci`. Check: `npm ls next` shows no `invalid`, and `next dev` stays up.
- **npm 12 warns "install scripts blocked because they are not covered by allowScripts"** (prisma, @prisma/engines, esbuild, unrs-resolver): npm 12 skips dependency lifecycle scripts by default. Prisma 7, tsx, vitest, and Next build work without them, so leave them blocked unless a tool fails. Check: `npx prisma generate`, `npm test`, and `npm run build` pass.

## Git

- **After a formatter run, many files show as modified, or Git warns "LF will be replaced by CRLF the next time Git touches it"**: Git for Windows defaults to `core.autocrlf=true`, which checks out CRLF while formatters write LF, and repos that committed CRLF differ on every line once a file is rewritten as LF. Machine: `git config --global core.autocrlf input` and the editor set to LF (VS Code `"files.eol": "\n"`). Repo: `.gitattributes` with `* text=auto eol=lf`, then one commit of `git add --renormalize .`. Check: `git diff --ignore-cr-at-eol --stat` lists only real changes.

## Shell

- **A file's other uncommitted changes vanish while comparing one file with HEAD**: `git stash` stashes the whole working tree, not one path. Use `git show HEAD:<path> > <tmp>` and compare the copy. Check: `git stash list` is empty and `git status` shows every earlier change.
- **A Python edit turns an LF file into CRLF on Windows**: `Path.write_text` and text-mode `open` translate `\n` to `\r\n`. Pass `newline="\n"` when writing. Check: `file <path>` reports no CRLF terminators.
- **A bash heredoc fails with `unexpected EOF while looking for matching`, or text sent through it loses backslashes: a regex matches nothing, an empty match inserts text at the start of the file, or a JSON payload fails with `Invalid \escape` / an exact LaTeX match finds 0**: the agent's Bash tool on Windows Git Bash can collapse backslashes even in `<<'EOF'` heredocs, and a JS or JSON string then consumes another level. Write payloads (JSON, LaTeX, code) to a file with the Write tool and pass the path; prefer exact-string replacements or the Edit tool. Check: the target line changed and line 1 of the file is unchanged.
