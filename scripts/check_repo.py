#!/usr/bin/env python3
"""Check this repository's own conventions, which generic skill linters do not know.

Usage: python scripts/check_repo.py
Exits 1 and lists every problem when:
- a SKILL.md front matter has keys other than `name` and `description`,
- a SKILL.md lacks a required section, or its H1 differs from `agents/openai.yaml` display_name,
- `agents/openai.yaml` is missing a field or its default prompt does not name `$<skill>`,
- a file in `references/`, `scripts/`, or `assets/` is not mentioned in its SKILL.md or
  README.md, or breaks the file naming convention (kebab-case, Python snake_case),
- a Markdown heading breaks the heading case convention,
- the AGENTS.md intent map does not route to exactly the skill folders,
- a Claude Code agent definition lacks `name` (matching its file), `description`,
  `model`, or `effort`, or is not listed in README.md,
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
    "Common Rationalisations",
    "Red Flags",
    "Verification",
)
OPENAI_FIELDS = ("display_name", "short_description", "default_prompt")
SUPPORT_DIRS = ("references", "scripts", "assets")
AGENT_FIELDS = ("name", "description", "model", "effort")
AGENTS_DIR = ROOT / "claude-code-agents"
SKIPPED_DIRS = {".git", ".venv", ".cache", ".agent-local", "node_modules"}
KEBAB_FILE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.[a-z0-9]+$")
PYTHON_FILE = re.compile(r"^[a-z][a-z0-9_]*\.py$")
# Title case: these words stay lowercase unless they open the heading or follow a colon.
MINOR_WORDS = {
    *("a", "an", "the", "and", "but", "or", "nor", "as", "at", "by", "for"),
    *("from", "in", "into", "of", "on", "onto", "per", "to", "via", "vs", "with"),
}


def front_matter(text: str) -> dict | None:
    match = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    data = yaml.safe_load(match.group(1)) if match else None
    return data if isinstance(data, dict) else None


def skill_dirs() -> list[Path]:
    return sorted(p.parent for p in ROOT.glob("*/SKILL.md"))


def check_file_name(skill: str, folder: str, path: Path) -> list[str]:
    pattern = PYTHON_FILE if path.suffix == ".py" else KEBAB_FILE
    if pattern.match(path.name):
        return []
    rule = "snake_case" if path.suffix == ".py" else "kebab-case"
    return [f"{skill}: {folder}/{path.name} must be {rule}"]


def check_skill(skill: Path, readme: str) -> list[str]:
    name, problems = skill.name, []
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    front = front_matter(text)
    if front is None or set(front) != {"name", "description"}:
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
    title = re.search(r"^# (.+?)\s*$", text, re.MULTILINE)
    if title and interface.get("display_name") != title.group(1):
        problems.append(
            f"{name}: H1 `{title.group(1)}` differs from display_name "
            f"`{interface.get('display_name')}`"
        )

    for folder in SUPPORT_DIRS:
        for path in sorted((skill / folder).rglob("*")):
            relative = path.relative_to(skill).as_posix()
            if "__pycache__" in path.parts or not path.is_file():
                continue
            if relative not in text:
                problems.append(f"{name}: {relative} is not mentioned in SKILL.md")
            if path.name not in readme:
                problems.append(f"{name}: {relative} is not listed in README.md")
            problems += check_file_name(name, folder, path)
    return problems


def heading_problems(heading: str) -> list[str]:
    """Return the words of one heading that break title case."""
    plain = re.sub(r"`[^`]*`", "Code", heading)
    plain = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", plain)
    wrong, after_colon = [], True
    for word in plain.split():
        core = word.strip("\"'()[],.!?")
        if core[:1].isalpha():
            minor = core.lower() in MINOR_WORDS and not after_colon
            if (minor and core != core.lower()) or (not minor and core[0].islower()):
                wrong.append(core)
        after_colon = word.endswith(":")
    return wrong


def markdown_files() -> list[Path]:
    return sorted(
        p
        for p in ROOT.rglob("*.md")
        if not SKIPPED_DIRS.intersection(p.relative_to(ROOT).parts)
    )


def check_headings() -> list[str]:
    problems = []
    for path in markdown_files():
        in_fence = False
        lines = path.read_text(encoding="utf-8").splitlines()
        for number, line in enumerate(lines, 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            match = None if in_fence else re.match(r"#{1,6} (.+?)\s*$", line)
            wrong = heading_problems(match.group(1)) if match else []
            if wrong:
                where = f"{path.relative_to(ROOT).as_posix()}:{number}"
                problems.append(f"{where}: heading case of {', '.join(wrong)}")
    return problems


def check_intent_map(agents: str, names: list[str]) -> list[str]:
    routed = set(re.findall(r"^- .+: `([a-z0-9-]+)`", agents, re.MULTILINE))
    problems = [
        f"AGENTS.md intent map routes to `{n}`, which is not a skill folder"
        for n in sorted(routed - set(names))
    ]
    problems += [
        f"AGENTS.md intent map has no route to `{n}`"
        for n in sorted(set(names) - routed)
    ]
    return problems


def check_agent_definitions(readme: str) -> list[str]:
    problems = []
    for path in sorted(AGENTS_DIR.glob("*.md")):
        where = f"claude-code-agents/{path.name}"
        front = front_matter(path.read_text(encoding="utf-8")) or {}
        problems += [
            f"{where}: front matter lacks `{field}`"
            for field in AGENT_FIELDS
            if not front.get(field)
        ]
        if front.get("name") != path.stem:
            problems.append(f"{where}: `name` must equal the file name `{path.stem}`")
        if not KEBAB_FILE.match(path.name):
            problems.append(f"{where}: file name must be kebab-case")
        if path.name not in readme:
            problems.append(f"{where} is not listed in README.md")
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
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    skills = skill_dirs()
    names = [s.name for s in skills]
    problems = check_readme(readme, names)
    problems += check_intent_map(agents, names)
    problems += check_agent_definitions(readme)
    problems += check_headings()
    for skill in skills:
        problems += check_skill(skill, readme)
    for problem in problems:
        print(f"- {problem}")
    print(f"{len(skills)} skills checked, {len(problems)} problem(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
