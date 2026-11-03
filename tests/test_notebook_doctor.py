import ast
import json

import pytest

KAGGLE_OK = [
    ("markdown", "# Overview"),
    ("markdown", "Setup"),
    ("code", 'from tqdm.auto import tqdm\nprint("start", flush=True)\n!pip list'),
    ("markdown", "Zip outputs"),
    (
        "code",
        'import zipfile\nfrom IPython.display import FileLink\nWORK = "/kaggle/working"\n'
        'FileLink("outputs.zip")',
    ),
]


def write_notebook(path, cells, minor=4, ids=None):
    raw = []
    for index, (kind, source) in enumerate(cells):
        cell = {"cell_type": kind, "metadata": {}, "source": source}
        if kind == "code":
            cell.update(outputs=[], execution_count=index + 1)
        if ids is not None:
            cell["id"] = ids[index]
        raw.append(cell)
    notebook = {"cells": raw, "metadata": {}, "nbformat": 4, "nbformat_minor": minor}
    path.write_bytes(json.dumps(notebook).encode())
    return path


def test_repair_upgrades_old_notebook_and_adds_ids(doctor, tmp_path):
    path = write_notebook(tmp_path / "old.ipynb", KAGGLE_OK, minor=4)
    assert doctor.repair_notebook(path, make_backup=False) == 0
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert saved["nbformat_minor"] >= 5
    ids = [cell["id"] for cell in saved["cells"]]
    assert all(ids) and len(set(ids)) == len(ids)


def test_repair_replaces_duplicate_ids(doctor, tmp_path):
    cells = KAGGLE_OK[:2]
    path = write_notebook(tmp_path / "dup.ipynb", cells, minor=5, ids=["a", "a"])
    assert doctor.repair_notebook(path, make_backup=False) == 0
    assert doctor.validate_notebook(path) == 0


def test_writes_use_lf(doctor, tmp_path):
    path = write_notebook(tmp_path / "nb.ipynb", KAGGLE_OK)
    doctor.clean_notebook(path, make_backup=False, drop_widgets=False)
    assert b"\r\n" not in path.read_bytes()
    out = tmp_path / "cells.py"
    doctor.export_code(path, out)
    assert b"\r\n" not in out.read_bytes()


def test_clean_clears_outputs_and_counts(doctor, tmp_path):
    path = write_notebook(tmp_path / "nb.ipynb", KAGGLE_OK)
    doctor.clean_notebook(path, make_backup=False, drop_widgets=False)
    saved = json.loads(path.read_text(encoding="utf-8"))
    code = [cell for cell in saved["cells"] if cell["cell_type"] == "code"]
    assert all(cell["execution_count"] is None for cell in code)


def test_inspect_does_not_require_ids_before_4_5(doctor, tmp_path, capsys):
    path = write_notebook(tmp_path / "old.ipynb", KAGGLE_OK, minor=4)
    assert doctor.inspect_notebook(path) == 0
    assert "0 missing" in capsys.readouterr().out


def test_backup_goes_to_agent_local_inside_git_repo(doctor, tmp_path):
    (tmp_path / ".git").mkdir()
    path = write_notebook(tmp_path / "nb.ipynb", KAGGLE_OK)
    first, second = doctor.backup_file(path), doctor.backup_file(path)
    assert first.parent == tmp_path / ".agent-local" / "backups"
    assert first.name == "nb.ipynb.bak" and second.name == "nb.ipynb.bak.1"


def test_check_kaggle_passes_conforming_notebook(doctor, tmp_path):
    path = write_notebook(tmp_path / "ok.ipynb", KAGGLE_OK)
    assert doctor.check_kaggle(path) == 0


def test_check_kaggle_reports_missing_markdown_and_zip(doctor, tmp_path, capsys):
    path = write_notebook(tmp_path / "bad.ipynb", [("code", "x = 1")])
    assert doctor.check_kaggle(path) == 1
    out = capsys.readouterr().out
    assert "first cell is not a markdown overview" in out
    assert "does not create the output zip" in out


@pytest.mark.parametrize(
    ("source", "flagged"),
    [
        ("from multiprocessing import Pool\nPool(4)", True),
        ("import multiprocessing\nmultiprocessing.Pool(4)", True),
        ("ProcessPoolExecutor(4)", True),
        ("ProcessPoolExecutor(4, mp_context=ctx)", False),
        ("ProcessPoolExecutor(4, ctx)", False),
        ('get_context("spawn").Pool(4)', False),
    ],
)
def test_fork_pool_detection(doctor, source, flagged):
    assert bool(doctor.fork_pool_lines(ast.parse(source))) is flagged


@pytest.mark.parametrize(
    ("source", "silent"),
    [
        ("for x in tqdm(items):\n    pass", True),
        ("for x in tqdm(items):\n    log(x)", False),
        ("for x in items:\n    pass", False),
    ],
)
def test_silent_progress(doctor, source, silent):
    assert doctor.silent_progress(ast.parse(source)) is silent


def test_cell_python_masks_magics(doctor):
    assert (
        doctor.cell_python("!pip install x\n%time y = 1\nz = 2") == "pass\npass\nz = 2"
    )
    assert doctor.cell_python("%%writefile lib.py\ndef f():\n    pass") == (
        "def f():\n    pass"
    )
    assert doctor.cell_python("%%writefile notes.txt\nhello") is None
    assert doctor.cell_python("%%bash\nls") is None


def test_diff_reports_changes(doctor, tmp_path, capsys):
    before = write_notebook(tmp_path / "a.ipynb", KAGGLE_OK)
    changed = [*KAGGLE_OK[:-1], ("code", "print('changed')")]
    after = write_notebook(tmp_path / "b.ipynb", changed)
    assert doctor.diff_notebooks(before, before) == 0
    assert doctor.diff_notebooks(before, after) == 1
    assert "changed" in capsys.readouterr().out
