from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "heading",
    [
        "Writing and Maintaining Skills",
        "Keep the GPUs Fed",
        "When to Use",
        "`checkov`",
        "Node.js and `npm`",
        "Kaggle Session Limits (2026-10-26)",
        "Step 1: The Plan",
    ],
)
def test_heading_case_accepts_title_case(check_repo, heading):
    assert check_repo.heading_problems(heading) == []


@pytest.mark.parametrize(
    ("heading", "wrong"),
    [
        ("Writing And Maintaining Skills", ["And"]),
        ("Table Of Contents", ["Of"]),
        ("Python dependencies", ["dependencies"]),
        ("checkov", ["checkov"]),
    ],
)
def test_heading_case_reports_wrong_words(check_repo, heading, wrong):
    assert check_repo.heading_problems(heading) == wrong


@pytest.mark.parametrize(
    ("folder", "name", "ok"),
    [
        ("references", "latex-fixes.md", True),
        ("references", "fixes_latex.md", False),
        ("assets", "Resume.tex", False),
        ("scripts", "check_paper.py", True),
        ("scripts", "checkPaper.py", False),
    ],
)
def test_file_names_follow_convention(check_repo, folder, name, ok):
    assert (check_repo.check_file_name("skill", folder, Path(name)) == []) is ok


def test_intent_map_reports_missing_and_unknown_skills(check_repo):
    agents = "- Commit: `git-commit-and-push`\n- Other: `no-such-skill`\n"
    problems = check_repo.check_intent_map(
        agents, ["git-commit-and-push", "project-docs"]
    )
    assert any("no-such-skill" in p for p in problems)
    assert any("no route to `project-docs`" in p for p in problems)
