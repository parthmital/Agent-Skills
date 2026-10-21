# Local Launch

`npm run dev` at the root is the only launcher, cross-platform, via one Node script; delete `start.ps1`, `start.sh`, and similar.

- First run installs everything (Node deps, `.venv` with Python deps, `.env` from the example). Later runs skip setup unless a lockfile hash (Git-ignored stamp) changed or an environment is broken.
- Run Python via the `.venv` interpreter, no activation.
- Interrupted setup must resume: write each stamp only after its step succeeds, run installs asynchronously with a SIGINT/SIGBREAK listener so an interrupt prints "run again to resume" instead of dying silently, and delete and rebuild a `.venv` whose interpreter or pip does not run. VS Code's Python auto-activation sends Ctrl+C into the terminal when a new `.venv` appears (`python-envs.terminal.autoActivationType: "shellStartup"` keeps auto-activation without it).
- npm `allowScripts`: approve only reviewed install scripts, pinned (`npm install-scripts approve <pkg>`), never `--all`.
- `.gitattributes` uses `* text=auto eol=lf` so Windows checkouts match the formatters and CI.
- One titled terminal window per long-running process (frontend, backend, services, workers), else prefixed output in the main terminal.
- The main terminal shows status, URLs, and crashes; Ctrl+C kills every process tree and window.
- Clean logs: summarise install noise, never hide errors. Fail fast on missing runtimes or busy ports.
- Open the browser once the frontend responds, except in CI.
