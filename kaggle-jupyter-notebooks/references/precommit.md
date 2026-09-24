# Recommended repository protections

Install into the project-local virtual environment:

```bash
./.venv/bin/python -m pip install nbformat nbstripout nbdime
./.venv/bin/nbdime config-git --enable
./.venv/bin/nbstripout --install
```

On Windows, use `.\.venv\Scripts\` instead of `./.venv/bin/`.

Both `config-git --enable` and `nbstripout --install` write to the repository's `.git/config` by default. Do not pass `--global` or `--system` unless the user explicitly asks.

Example `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/kynan/nbstripout
    rev: 0.8.1
    hooks:
      - id: nbstripout
```

Do not strip outputs from notebooks whose committed outputs are intentional deliverables.
