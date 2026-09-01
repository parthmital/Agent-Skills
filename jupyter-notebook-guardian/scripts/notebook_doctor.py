#!/usr/bin/env python3
"""Safe Jupyter notebook inspection and maintenance utility."""

from __future__ import annotations

import argparse
import ast
import copy
import difflib
import json
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any

try:
    import nbformat
    from nbformat.validator import NotebookValidationError
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: install with `python -m pip install nbformat`."
    ) from exc


def load_notebook(path: Path):
    try:
        return nbformat.read(path, as_version=4)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc
    except Exception as exc:
        raise SystemExit(f"Unable to read {path}: {exc}") from exc


def backup_file(path: Path) -> Path:
    candidate = path.with_suffix(path.suffix + ".bak")
    index = 1
    while candidate.exists():
        candidate = path.with_suffix(path.suffix + f".bak.{index}")
        index += 1
    shutil.copy2(path, candidate)
    return candidate


def atomic_write(nb, path: Path) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    nbformat.write(nb, tmp)
    nbformat.validate(nb)
    tmp.replace(path)


def source_text(cell: Any) -> str:
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else str(source)


def inspect_notebook(path: Path) -> int:
    nb = load_notebook(path)
    ids = [cell.get("id") for cell in nb.cells]
    counts = [
        cell.get("execution_count") for cell in nb.cells if cell.cell_type == "code"
    ]
    numeric_counts = [value for value in counts if isinstance(value, int)]
    output_bytes = 0
    error_outputs = 0
    code_cells = 0
    markdown_cells = 0
    warnings: list[str] = []

    for index, cell in enumerate(nb.cells):
        if cell.cell_type == "code":
            code_cells += 1
            for output in cell.get("outputs", []):
                output_bytes += len(
                    json.dumps(output, ensure_ascii=False).encode("utf-8")
                )
                if output.get("output_type") == "error":
                    error_outputs += 1
            src = source_text(cell)
            if any(
                token in src
                for token in ("globals()", "locals()", "exec(", "eval(", "%run ")
            ):
                warnings.append(f"cell {index}: dynamic or hidden-state construct")
        elif cell.cell_type == "markdown":
            markdown_cells += 1

    duplicates = sorted(value for value, n in Counter(ids).items() if value and n > 1)
    missing_ids = sum(value is None for value in ids)
    non_monotonic = any(b <= a for a, b in zip(numeric_counts, numeric_counts[1:]))

    print(f"File: {path}")
    print(f"Format: {nb.nbformat}.{nb.nbformat_minor}")
    print(f"Cells: {len(nb.cells)} total, {code_cells} code, {markdown_cells} markdown")
    print(f"Kernel: {nb.metadata.get('kernelspec', {}).get('name', 'unspecified')}")
    print(f"Outputs: {output_bytes / 1024:.1f} KiB, {error_outputs} error output(s)")
    print(f"Cell IDs: {missing_ids} missing, {len(duplicates)} duplicate value(s)")
    print(
        f"Execution counts: {'non-monotonic or repeated' if non_monotonic else 'monotonic/empty'}"
    )
    if "widgets" in nb.metadata:
        print("Widget state: present")
    if duplicates:
        warnings.append("duplicate cell IDs: " + ", ".join(duplicates))
    if missing_ids:
        warnings.append(f"{missing_ids} missing cell ID(s)")
    if non_monotonic:
        warnings.append("execution counts suggest out-of-order execution")
    if output_bytes > 5 * 1024 * 1024:
        warnings.append("embedded outputs exceed 5 MiB")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
        return 1
    print("Warnings: none detected")
    return 0


def validate_notebook(path: Path) -> int:
    nb = load_notebook(path)
    try:
        nbformat.validate(nb)
    except NotebookValidationError as exc:
        print(f"INVALID: {path}\n{exc}", file=sys.stderr)
        return 1
    ids = [cell.get("id") for cell in nb.cells]
    duplicates = [value for value, n in Counter(ids).items() if value and n > 1]
    if duplicates:
        print(f"INVALID: duplicate cell IDs: {duplicates}", file=sys.stderr)
        return 1
    print(f"VALID: {path}")
    return 0


def repair_notebook(path: Path, make_backup: bool) -> int:
    nb = load_notebook(path)
    if make_backup:
        print(f"Backup: {backup_file(path)}")
    nb = nbformat.convert(nb, 4)
    nbformat.validator.normalize(nb)
    seen: set[str] = set()
    for cell in nb.cells:
        cell_id = cell.get("id")
        if not cell_id or cell_id in seen:
            cell["id"] = nbformat.corpus.words.generate_corpus_id()
        seen.add(cell["id"])
    atomic_write(nb, path)
    print(f"Repaired: {path}")
    return validate_notebook(path)


def clean_notebook(path: Path, make_backup: bool, drop_widgets: bool) -> int:
    nb = load_notebook(path)
    if make_backup:
        print(f"Backup: {backup_file(path)}")
    changed = 0
    for cell in nb.cells:
        if cell.cell_type == "code":
            if cell.get("outputs"):
                cell["outputs"] = []
                changed += 1
            if cell.get("execution_count") is not None:
                cell["execution_count"] = None
                changed += 1
    if drop_widgets and "widgets" in nb.metadata:
        del nb.metadata["widgets"]
        changed += 1
    atomic_write(nb, path)
    print(f"Cleaned: {path} ({changed} field group(s) changed)")
    return 0


def export_code(path: Path, output: Path) -> int:
    nb = load_notebook(path)
    chunks = []
    for index, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        cell_id = cell.get("id", "missing-id")
        source = source_text(cell)
        chunks.append(f"# %% [cell {index}, id={cell_id}]\n{source.rstrip()}\n")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(chunks), encoding="utf-8")
    print(f"Exported {len(chunks)} code cells to {output}")
    return 0


def semantic_lines(path: Path) -> list[str]:
    nb = load_notebook(path)
    lines: list[str] = []
    for index, cell in enumerate(nb.cells):
        cell_id = cell.get("id", "missing-id")
        lines.append(f"@@ cell {index} id={cell_id} type={cell.cell_type} @@\n")
        source = source_text(cell)
        lines.extend(line + "\n" for line in source.splitlines())
        if cell.cell_type == "code":
            lines.append(
                f"[outputs={len(cell.get('outputs', []))}, execution_count={cell.get('execution_count')}]\n"
            )
    return lines


def diff_notebooks(before: Path, after: Path) -> int:
    diff = difflib.unified_diff(
        semantic_lines(before),
        semantic_lines(after),
        fromfile=str(before),
        tofile=str(after),
    )
    text = "".join(diff)
    print(text or "No semantic differences.")
    return 1 if text else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    for command in ("inspect", "validate"):
        p = sub.add_parser(command)
        p.add_argument("notebook", type=Path)

    p = sub.add_parser("repair")
    p.add_argument("notebook", type=Path)
    p.add_argument("--backup", action="store_true")

    p = sub.add_parser("clean")
    p.add_argument("notebook", type=Path)
    p.add_argument("--backup", action="store_true")
    p.add_argument("--drop-widgets", action="store_true")

    p = sub.add_parser("export-code")
    p.add_argument("notebook", type=Path)
    p.add_argument("--output", type=Path, required=True)

    p = sub.add_parser("diff")
    p.add_argument("before", type=Path)
    p.add_argument("after", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "inspect":
        return inspect_notebook(args.notebook)
    if args.command == "validate":
        return validate_notebook(args.notebook)
    if args.command == "repair":
        return repair_notebook(args.notebook, args.backup)
    if args.command == "clean":
        return clean_notebook(args.notebook, args.backup, args.drop_widgets)
    if args.command == "export-code":
        return export_code(args.notebook, args.output)
    if args.command == "diff":
        return diff_notebooks(args.before, args.after)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
