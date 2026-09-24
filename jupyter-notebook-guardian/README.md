# Jupyter Notebook Guardian skill

Copy this folder into the skills directory used by your agent or harness, preserving the folder name and `SKILL.md`.

The skills directory location depends on the harness. Repository-embedded skills may be kept in the project and committed with the codebase.

Dependency (install into a project-local virtual environment, not the system interpreter):

```bash
python -m venv .venv
./.venv/bin/python -m pip install nbformat
```

On Windows, use `.\.venv\Scripts\python` instead of `./.venv/bin/python`.

Smoke test:

```bash
./.venv/bin/python scripts/notebook_doctor.py --help
```
