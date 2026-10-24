# Fixes

Tool and environment problems that no other skill owns. Search by symptom text. Entry format: `- **<symptom>**: <cause>. <fix>. Check: <how>.` Move an entry into a skill once one owns its area.

## Skills

- **Installed skill differs from the source repository**: installed folders were copies, so edits made in one place drifted. Install each skill as a link to its repository folder (README Installation). Check: `diff -rq <installed>/<skill> <repo>/<skill>` prints nothing.

## Node and npm

- **`next dev` prints "Your version of Next.js is affected by a known security vulnerability" and exits**: `node_modules` is older than `package-lock.json` (often after a merged dependency bump), so the installed `next` is the vulnerable one. Run `npm ci`. Check: `npm ls next` shows no `invalid`, and `next dev` stays up.
- **npm 12 warns "install scripts blocked because they are not covered by allowScripts"** (prisma, @prisma/engines, esbuild, unrs-resolver): npm 12 skips dependency lifecycle scripts by default. Prisma 7, tsx, vitest, and Next build work without them, so leave them blocked unless a tool fails. Check: `npx prisma generate`, `npm test`, and `npm run build` pass.

## Shell

- **A regex passed through a bash heredoc into a JS string matches nothing, or an empty match inserts text at the start of the file**: the heredoc and the JS string each consume a level of backslashes (`\s` arrives as `s`). Prefer exact-string replacements, or edit with the Edit tool. Check: the target line changed and line 1 of the file is unchanged.
