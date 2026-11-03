"""Load the skills' helper scripts as modules: they live in skill folders, not in a package."""

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
# Skill folders are linked into agent harnesses; keep __pycache__ out of them.
sys.dont_write_bytecode = True


def load_script(relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def doctor():
    return load_script("kaggle-jupyter-notebooks/scripts/notebook_doctor.py")


@pytest.fixture(scope="session")
def paper():
    return load_script("latex-research-papers/scripts/paper_check.py")
