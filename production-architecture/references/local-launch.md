# Local Launch

`npm run dev` at the root is the only launcher, cross-platform, via one Node script; delete `start.ps1`, `start.sh`, and similar.

- First run installs everything (Node deps, `.venv` with Python deps, `.env` from the example). Later runs skip setup unless a lockfile hash (Git-ignored stamp) changed or an environment is broken.
- Run Python via the `.venv` interpreter, no activation.
- Interrupted setup must resume: write each stamp only after its step succeeds, run installs asynchronously with a SIGINT/SIGBREAK listener so an interrupt prints "run again to resume" instead of dying silently, and delete and rebuild a `.venv` whose interpreter or pip does not run. VS Code's Python auto-activation sends Ctrl+C into the terminal when a new `.venv` appears (`python-envs.terminal.autoActivationType: "shellStartup"` keeps auto-activation without it).
- npm `allowScripts`: approve only reviewed install scripts, pinned (`npm install-scripts approve <pkg>`), never `--all`.
- `.gitattributes` uses `* text=auto eol=lf` so Windows checkouts match the formatters and CI.
- One titled terminal window per long-running process (frontend, backend, services, workers), else prefixed output in the main terminal.
- The main terminal shows status, URLs, and crashes; Ctrl+C kills every process tree and window.
- Clean logs: summarise install noise, never hide errors. Fail fast on missing runtimes or busy ports. Never run pip `--quiet` in a blocking call: stream it, log large downloads and the install phase, print a heartbeat every ~20 s (unpacking PyTorch is silent for minutes), and keep `pip --log .cache/pip-install.log`. Register the launcher's own Ctrl+C handler only after setup, or it pre-empts setup's resume message.
- **First setup "hangs" downloading PyTorch, a rerun completes**: often resolver backtracking from a version cap that conflicts with a transitive dependency (for example `websockets<14` against `langsmith`, which needs `>=15`), hidden by `--quiet`. Fix: remove or widen the cap. Check: `grep "looking at multiple versions" .cache/pip-install.log` is empty, and `pip install --dry-run --ignore-installed -r <reqs>` resolves in one pass.
- Open the browser once the frontend responds, except in CI.
