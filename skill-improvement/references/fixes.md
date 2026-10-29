# Fixes

Tool and environment problems that no other skill owns. Search by symptom text. Entry format: `- **<symptom>**: <cause>. <fix>. Check: <how>.` Move an entry into a skill once one owns its area.

## Skills

- **Installed skill differs from the source repository**: installed folders were copies, so edits made in one place drifted. Install each skill as a link to its repository folder (README Installation). Check: `diff -rq <installed>/<skill> <repo>/<skill>` prints nothing.

## Node and npm

- **`next dev` prints "Your version of Next.js is affected by a known security vulnerability" and exits**: `node_modules` is older than `package-lock.json` (often after a merged dependency bump), so the installed `next` is the vulnerable one. Run `npm ci`. Check: `npm ls next` shows no `invalid`, and `next dev` stays up.
- **npm 12 warns "install scripts blocked because they are not covered by allowScripts"** (prisma, @prisma/engines, esbuild, unrs-resolver): npm 12 skips dependency lifecycle scripts by default. Prisma 7, tsx, vitest, and Next build work without them, so leave them blocked unless a tool fails. Check: `npx prisma generate`, `npm test`, and `npm run build` pass.
- **`npm ci` fails with ERESOLVE "peer react@"^19.3.1" from react-dom@19.3.1"**: a bumped package needs a newer version of a sibling that is still on the old version. Bump the sibling in the same change (react and react-dom). Check: `npm ci` passes on the combined change.
- **`npm ci` fails with ERESOLVE "peer typescript@">=4.8.4 <6.1.0"" from typescript-eslint**: typescript-eslint caps the TypeScript major, so a bump past the cap conflicts. Hold that bump until the linter supports it. Check: `npm view typescript-eslint@latest peerDependencies` lists the new range.

## Python dependencies

- **`pip install --require-hashes` fails: "all requirements must have their versions pinned with ==" for `setuptools` (or `pip`) "from pip-tools"**: pip-tools needs setuptools, and `pip-compile` without `--allow-unsafe` leaves setuptools and pip out of the lock. A Python 3.11 venv ships setuptools, which hides the gap; a fresh Python 3.12 venv does not. Recompile with `pip-compile --allow-unsafe --generate-hashes`. Check: `pip uninstall -y setuptools` in a fresh venv, then the hash-checked install succeeds.

## Git

- **After a formatter run, many files show as modified, or Git warns "LF will be replaced by CRLF the next time Git touches it"**: Git for Windows defaults to `core.autocrlf=true`, which checks out CRLF while formatters write LF, and repos that committed CRLF differ on every line once a file is rewritten as LF. Machine: `git config --global core.autocrlf input` and the editor set to LF (VS Code `"files.eol": "\n"`). Repo: `.gitattributes` with `* text=auto eol=lf`, then one commit of `git add --renormalize .`. Check: `git diff --ignore-cr-at-eol --stat` lists only real changes.

## Shell

- **A file's other uncommitted changes vanish while comparing one file with HEAD**: `git stash` stashes the whole working tree, not one path. Use `git show HEAD:<path> > <tmp>` and compare the copy. Check: `git stash list` is empty and `git status` shows every earlier change.
- **A Python edit turns an LF file into CRLF on Windows**: `Path.write_text` and text-mode `open` translate `\n` to `\r\n`. Pass `newline="\n"` when writing. Check: `file <path>` reports no CRLF terminators.
- **`python -I` on Windows fails with `UnicodeEncodeError: 'charmap' codec can't encode character` even with `PYTHONIOENCODING=utf-8`**: `-I` implies `-E`, which ignores every `PYTHON*` variable, so stdout stays cp1252. Add `-X utf8`, or call `sys.stdout.reconfigure(encoding="utf-8")` in the script. Check: the script prints non-ASCII text.

## Documents

- **A PDF reports hundreds of thousands of embedded images and extracted images are tiny fragments**: the PDF stores each screenshot as many tiles. Render whole pages to PNG (PyMuPDF `page.get_pixmap(matrix=fitz.Matrix(z, z))`) instead of extracting images. Check: the rendered page shows complete figures.
- **A bash heredoc fails with `unexpected EOF while looking for matching`, or text sent through it loses backslashes: `re.error: bad escape \c`, `unicodeescape ... truncated \uXXXX`, a LaTeX `\fi` arriving as a form feed (`\x0c`), a regex matching nothing, or a JSON payload failing with `Invalid \escape`**: the Bash tool turns `\\` into `\` even inside `<<'EOF'`. The rule lives in `AGENTS.md` (Implementation), which loads every session: write payloads to a file with the Write tool, edit with the Edit tool. Check: a heredoc of `a\\b` prints `a\b`.
