#!/usr/bin/env python3
"""Check this repository's own skill conventions, which generic skill linters do not know.

Usage: python scripts/check_repo.py
Exits 1 and lists every problem when:
- a SKILL.md front matter has keys other than `name` and `description`,
- a SKILL.md lacks a required section,
- `agents/openai.yaml` is missing a field or its default prompt does not name `$<skill>`,
- a file in `references/`, `scripts/`, or `assets/` is not mentioned in its SKILL.md or README.md,
- the README skills table or skill folder count does not match the skill folders.
Spec checks (name format, description length, links) are left to skillsaw.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = (
    "Overview",
    "When to Use",
    "Common Rationalizations",
    "Red Flags",
    "Verification",
)
OPENAI_FIELDS = ("display_name", "short_description", "default_prompt")
SUPPORT_DIRS = ("references", "scripts", "assets")


def skill_dirs() -> list[Path]:
    return sorted(p.parent for p in ROOT.glob("*/SKILL.md"))


def check_skill(skill: Path, readme: str) -> list[str]:
    name, problems = skill.name, []
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    front = yaml.safe_load(match.group(1)) if match else None
    if not isinstance(front, dict) or set(front) != {"name", "description"}:
        problems.append(
            f"{name}: front matter must have exactly `name` and `description`"
        )
    headings = set(re.findall(r"^## (.+?)\s*$", text, re.MULTILINE))
    problems += [f"{name}: missing `## {s}`" for s in SECTIONS if s not in headings]

    meta_path = skill / "agents" / "openai.yaml"
    meta = (
        yaml.safe_load(meta_path.read_text(encoding="utf-8"))
        if meta_path.exists()
        else {}
    )
    interface = (meta or {}).get("interface") or {}
    problems += [
        f"{name}: agents/openai.yaml lacks interface.{field}"
        for field in OPENAI_FIELDS
        if not interface.get(field)
    ]
    if f"${name}" not in str(interface.get("default_prompt", "")):
        problems.append(
            f"{name}: agents/openai.yaml default_prompt does not name ${name}"
        )
    if "allow_implicit_invocation" not in ((meta or {}).get("policy") or {}):
        problems.append(
            f"{name}: agents/openai.yaml lacks policy.allow_implicit_invocation"
        )

    for folder in SUPPORT_DIRS:
        for path in sorted((skill / folder).rglob("*")):
            relative = path.relative_to(skill).as_posix()
            if "__pycache__" in path.parts:
                continue
            if path.is_file() and relative not in text:
                problems.append(f"{name}: {relative} is not mentioned in SKILL.md")
            if path.is_file() and path.name not in readme:
                problems.append(f"{name}: {relative} is not listed in README.md")
    return problems


def check_readme(readme: str, names: list[str]) -> list[str]:
    problems = []
    table = re.search(r"^## Skills\n(.*?)^## ", readme, re.MULTILINE | re.DOTALL)
    rows = re.findall(
        r"^\| `([a-z0-9-]+)` +\|", table.group(1) if table else "", re.MULTILINE
    )
    if rows != names:
        problems.append(
            f"README Skills table lists {rows}, expected the skill folders {names} in order"
        )
    count = re.search(r"each of the (\d+) skill folders", readme)
    if not count or int(count.group(1)) != len(names):
        problems.append(f"README must say `each of the {len(names)} skill folders`")
    return problems


def main() -> int:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    skills = skill_dirs()
    problems = check_readme(readme, [s.name for s in skills])
    for skill in skills:
        problems += check_skill(skill, readme)
    for problem in problems:
        print(f"- {problem}")
    print(f"{len(skills)} skills checked, {len(problems)} problem(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
