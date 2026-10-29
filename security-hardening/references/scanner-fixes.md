# Scanner fixes

Quirks of the security scanners and their CI jobs. Search by symptom text. Entry format: `- **<symptom>**: <cause>. <fix>. Check: <how>.`

## checkov

- **`checkov: error: Invalid frameworks specified: docker_compose`**: checkov 3.3.30 has no Compose framework. Drop it from `--framework`, and validate the Compose file with `docker compose config --quiet`. Check: `checkov --framework dockerfile,github_actions --directory .` exits 0.
- **checkov fails a Dockerfile on CKV_DOCKER_2 (HEALTHCHECK), CKV_DOCKER_3 (user created), or CKV_DOCKER_8 (last USER is root)**: the file does not state these itself, and a base image's default user does not count. Add `USER <non-root user>` in the final stage and a `HEALTHCHECK` instruction. Check: the dockerfile summary shows `Failed checks: 0`.
- **`ModuleNotFoundError: No module named 'checkov'` from `checkov.cmd` in a venv**: the `.cmd` launcher runs whichever `python` is first on PATH. Call the venv interpreter: `<venv>\Scripts\python.exe -m checkov.main ...`. Check: the scan prints its results.

## gitleaks

- **gitleaks-action on a pull request fails with `Resource not accessible by integration` (HTTP 403) on `/repos/<owner>/<repo>/pulls/<n>/commits`**: the job's `GITHUB_TOKEN` lacks `pull-requests: read`, and a top-level `contents: read` does not grant it. Add `pull-requests: read` to that job's `permissions`. Push runs do not need it. Check: the gitleaks step passes on a `pull_request` run.

## zizmor

- **zizmor prints `(N suppressed)` with no `zizmor: ignore` comment in the workflows**: the default persona hides pedantic findings. Run `zizmor --persona pedantic` to list them. A `permissions` entry with no comment is flagged (`undocumented-permissions`); put the reason on the same line. Check: `zizmor --persona pedantic` reports no findings.
