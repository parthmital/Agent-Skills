# Recommended repository protections

Install:

```bash
python -m pip install nbformat nbstripout nbdime
nbdime config-git --enable
nbstripout --install
```

Example `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/kynan/nbstripout
    rev: 0.8.1
    hooks:
      - id: nbstripout
```

Do not strip outputs from notebooks whose committed outputs are intentional deliverables.
