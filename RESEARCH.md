# Research

Purpose: dated evidence behind this repository's design decisions. Read when: changing a skill's approach or revisiting a decision below.

## Research-Driven Development (2026-10-21)

**Brief:** whether "research-driven agentic development" (research existing solutions before building, gated by task complexity) is an established practice, and how to integrate it into these skills.

**Scope:** Anthropic and Claude Code docs, GitHub Spec Kit, HumanLayer's Research-Plan-Implement write-up, skill and MCP registries. Searched 2026-10-21.

**Findings:**

- The exact term is not established: one search for "research-driven development" with AI coding agents found no framework by that name. Weak signal; a single search.
- The practice is established under other names:
  - Claude Code best practices recommend explore, plan, implement, commit, and say to skip planning when "you could describe the diff in one sentence"; planning is most useful when the approach is uncertain, the change spans files, or the code is unfamiliar.
  - HumanLayer's Research-Plan-Implement workflow researches the codebase before planning and notes research is sometimes skipped or repeated. Its research is codebase-focused, not external reuse.
  - GitHub Spec Kit's `/plan` command runs "Phase 0: Outline & Research" and records each technology decision in `research.md` as decision, rationale, and alternatives considered.
- Discovery sources for reusable agent tooling: skills.sh (Vercel's agent skills directory, installed with `npx skills add <owner/repo>`) and the official MCP Registry.
- Inference: the gap these sources leave is external, reuse-first research with an explicit gate. That is what `research-driven-development` adds.

**Decision:** a dedicated `research-driven-development` skill with Skip, Quick, and Full tiers, an Adopt, Adapt, Borrow, or Build decision, and Spec Kit's decision, rationale, and alternatives record. `AGENTS.md` routes non-trivial work to it; `internet-research` keeps fact-finding and supplies the Source Rules. Alternatives considered: extending `internet-research` (rejected: mixes a gating workflow into a lookup skill, against one skill per workflow); an always-on rule in `AGENTS.md` only (rejected: no gate, so trivial tasks would pay the research cost).

**Sources:**

- Docs: [Claude Code best practices](https://code.claude.com/docs/en/best-practices); [Spec Kit plan command template](https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/plan.md).
- Practitioner write-ups: [HumanLayer, Advanced Context Engineering for Coding Agents](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md) (undated).
- Registries: [skills.sh](https://skills.sh/); [MCP Registry](https://registry.modelcontextprotocol.io/).

## Self-Improving Skills (2026-10-23)

**Brief:** how to make each solved problem reusable so it is never solved twice, at minimal context cost.

**Scope:** Every's compound engineering plugin and write-ups about it. Searched 2026-10-23 (one standard search; the plugin's file format was not confirmed).

**Findings:**

- Compound engineering adds a fourth step after plan, work, and review: document the solved problem (`/ce:compound`, formerly `/workflows:compound`) in searchable files that later sessions read. Command names have changed between versions.
- Its learnings live in a separate docs folder, which a session must know to search. Here, skills already load on trigger, so the owning skill is the cheaper and more reliable home.
- Inference: copies of installed skills drift from their source (this repository's `paper_check.py` differed from its installed copy), so a learning written to one copy can be lost.

**Decision:** Borrow, not Adopt. A harness-neutral `skill-improvement` skill records each fix as symptom, cause, fix, and check in the cheapest location that loads when it recurs, merging instead of appending; `AGENTS.md` adds one search-first, record-after rule; installs are links, not copies. Alternatives considered: installing the plugin (rejected: Claude Code only, a separate workflow and docs folder, much larger context); harness auto-memory (rejected: per-harness, disabled by this user, not reviewable in Git).

**Sources:**

- Repository: [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin).
- Docs: [Mintlify, compound engineering plugin commands](https://www.mintlify.com/EveryInc/compound-engineering-plugin/plugin/commands).
- Practitioner write-ups: [Ry Walker, compound engineering plugin](https://rywalker.com/research/compound-engineering-plugin) (undated).

## Skill Token Budgets and Progressive Disclosure (2026-10-21)

**Brief:** how to keep these skills cheap in context, prompted by Reddit advice to use progressive disclosure and narrowly scoped skills.

**Scope:** Anthropic skill authoring docs and Claude Code best practices. Searched 2026-10-21. The quoted Reddit threads were not found; their advice matches the official docs below.

**Findings:**

- Only `name` and `description` of every skill load at startup; `SKILL.md` loads when the skill triggers; other files load only when read, and scripts cost only their output. Descriptions are therefore the one cost paid in every session.
- Descriptions must say what the skill does and when to use it, in third person, at most 1024 characters.
- Keep `SKILL.md` under 500 lines; split conditional material into files linked directly from `SKILL.md` (one level deep), each with a pointer saying when to read it.
- "Claude is already very smart": add only context the model lacks.
- `CLAUDE.md` (and so `AGENTS.md`) loads every session; for each line ask whether removing it would cause mistakes, and move situational workflows into skills.

**Decision:** trim body detail out of descriptions while keeping every trigger; move situational sections into `references/` (frontend custom controls, local launch, notebook README walkthrough); document the three loading levels in the README.

**Sources:**

- Docs: [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices); [Claude Code best practices](https://code.claude.com/docs/en/best-practices).

## Hierarchical Model Delegation (2026-11-08)

**Brief:** make an Opus 5.5 orchestrator at medium effort delegate most routine work to Haiku 5.5 workers at xhigh effort, in parallel where safe, with every result validated. Supersedes the plan-then-execute handoff researched on 2026-10-26.

**Scope:** Claude Code subagent and model configuration docs, Anthropic's multi-agent research system write-up and skill authoring guide, and the earlier handoff research (obra/superpowers, goal commands in Antigravity, Claude Code, Codex, OpenCode). Searched 2026-11-08.

**Findings:**

- Claude Code subagent definitions (`.claude/agents/` or `~/.claude/agents/`) accept `model` (`haiku`, `sonnet`, `opus`, `fable`, a full ID, or `inherit`), `effort` (`low` to `max`, by model), `tools`, `disallowedTools`, and `isolation: worktree`. Model order: the Agent call's `model`, then the definition, then `CLAUDE_CODE_SUBAGENT_MODEL`, then the main model. A definition's `effort` overrides the session level but not `CLAUDE_CODE_EFFORT_LEVEL`; a per-call `effort` overrides the definition.
- Haiku 5.5 supports `low`, `medium`, `high`, `xhigh`, and `max`. Opus 5.5, Sonnet 5.5, and Haiku 5.5 default to `medium`. The `haiku` alias is Haiku 5.5 only on the Anthropic API; on Bedrock, Vertex, and Foundry it is Haiku 4.5.
- Docs guidance: subagents keep verbose exploration out of the main context and return summaries; use the main conversation for back-and-forth, shared-context phases, and quick targeted changes. Default concurrency is 20.
- Anthropic's multi-agent research system (published 2025-06-13): each subagent needs "an objective, an output format, guidance on the tools and sources to use, and clear task boundaries"; vague briefs caused duplicated work. Effort scaled by explicit rules (1 agent for simple facts, 2 to 4 for comparisons, more than 10 for complex research). Multi-agent runs used about 15 times the tokens of chat. Coding fits less well than research because it has fewer truly parallel parts. First-party claims about its own system, not independently checked.
- Skill authoring guide: test skills with every model that runs them; "What works perfectly for Opus might need more detail for Haiku."
- Earlier handoff research: plans for cheaper executors need small, self-contained tasks, each with files, a verification command, and its expected output (superpowers `writing-plans`), and goal commands work best with a measurable end state and the check that proves it. Inference: weak executors fail on undecided choices.
- Inference: the system prompt of Claude Code tells the agent not to spawn subagents unless asked, so delegation needs a standing permission in `AGENTS.md`, which user instructions let override defaults.

**Decision:** Build a `subagent-delegation` skill (roles, a Decide test, parallelism rules, a seven-part brief with a good and bad example, validation, recovery) and Adopt Claude Code subagent definitions for two workers, `task-worker` (all tools but spawning) and `research-worker` (no edits), both `model: haiku` and `effort: xhigh`. `AGENTS.md` gets a short Delegation section with the standing permission; heavy skills name what to fan out. Alternatives considered: `CLAUDE_CODE_SUBAGENT_MODEL=haiku` with `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` (rejected: also forces built-in agents, sets no effort, and lives outside the repository); per-call `model` and `effort` only (kept as the fallback when the definitions are not installed); the removed `implementation-plan` skill's plan files (rejected: a one-shot handoff without orchestrator validation). Revised the same day at the user's direction: the purpose is the lowest total usage, so delegation is the default, small tasks are batched, parallelism is used only for independent work, and validation uses the cheapest check that proves each claim.

**Sources:**

- Docs: [Claude Code subagents](https://code.claude.com/docs/en/sub-agents); [Claude Code model configuration](https://code.claude.com/docs/en/model-config); [Claude Code memory and imports](https://code.claude.com/docs/en/memory); [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
- Write-ups: [Anthropic, How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (2025-06-13).
- Repository: [obra/superpowers writing-plans](https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-plans/SKILL.md).
- Docs from the earlier handoff research: [Antigravity /goal](https://antigravity.google/docs/commands/goal/); [Claude Code /goal](https://code.claude.com/docs/en/goal.md); [Using Goals in Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex).

## Agent-First Documentation Set (2026-10-26)

**Brief:** one consistent format for `README.md`, `AGENTS.md`, `ARCHITECTURE.md`, `DATABASE.md`, `DESIGN.md`, `SECURITY.md`, `RESEARCH.md`, and similar, read mainly by agents, with no duplication and minimal tokens.

**Scope:** agents.md, Diataxis, Keep a Changelog, and this repository's skills. Searched 2026-10-26.

**Findings:**

- AGENTS.md is an open format, "a README for agents", stewarded by the Agentic AI Foundation and read by Codex, Jules, Aider, opencode, Cursor, Gemini CLI, Copilot's coding agent, and others. Suggested sections: overview, build and test commands, code style, testing, security. It complements the human README instead of cluttering it.
- Diataxis organises documentation around distinct needs (tutorials, how-to guides, reference, explanation).
- Keep a Changelog: an `Unreleased` section and Added, Changed, Deprecated, Removed, Fixed, Security groups.
- Inference: the doc content lists were spread across four skills with no shared format, no owner for `AGENTS.md`, `DATABASE.md`, `CONTRIBUTING.md`, or changelogs, and no rule for when a doc should not exist.

**Decision:** Build a `project-docs` skill with a documentation map (one question per file, a create-when rule, an owner skill), shared format rules (a `Purpose` and `Read when` line, one home per fact, about 200 lines per file), and one template per file; the owning skills now point to the templates instead of repeating content lists. A human-only `EXPLAINER.md` (`project-explainer`), following Diataxis's separation of explanation from reference, was removed 2026-10-27 at the user's request.

**Sources:**

- Standards: [AGENTS.md](https://agents.md/); [Diataxis](https://diataxis.fr/); [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).

## Kaggle Session Limits (2026-10-26)

**Brief:** the maximum run time of one Kaggle notebook session, to plan runs that finish their full scope in one session.

**Scope:** Kaggle docs and secondary sources. Searched 2026-10-26. Kaggle's notebook docs page renders with JavaScript and could not be read directly.

**Findings:**

- 12 hours per session for CPU and GPU, 9 hours for TPU: a comparison page that cites Kaggle's docs, checked 4 August 2026, and a PyPI package description agree. Older posts citing 9 hours for all sessions are outdated.
- The weekly GPU quota is about 30 hours and floats with demand; secondary sources disagree on whether the docs fix the number.

**Decision:** `kaggle-jupyter-notebooks` plans against 12 hours (9 on TPU) minus a margin of at least 45 minutes, sizes elastic work from a runtime timing probe, and splits scope that cannot fit into independent notebooks without resuming. Confidence: medium, because no primary source was opened.

**Sources:**

- Secondary: [Clusy, Colab vs Kaggle](https://www.clusy.io/compare/colab-vs-kaggle) (claims checked 2026-08-04); [kgz on PyPI](https://pypi.org/p/kgz).

## Windows Line Endings in Agent Diffs (2026-10-26)

**Brief:** stop agents analysing line-ending-only diffs on Windows.

**Scope:** local experiments with Git 2.54.0.windows.1 on 2026-10-26.

**Findings:**

- Git for Windows sets `core.autocrlf=true` in the system config. Formatters then write LF files and every touched file prints "LF will be replaced by CRLF the next time Git touches it".
- With LF in the index, a CRLF or LF working file shows no change under `autocrlf=true` or `input`, but shows as modified under `false`.
- With CRLF committed in the index, a file rewritten as LF shows as modified under every setting; only renormalising the repository fixes it.
- `git diff --ignore-cr-at-eol --stat` omits files whose only change is line endings.

**Decision:** `core.autocrlf=input` in the global config (LF checkouts, LF commits, existing CRLF checkouts stay clean), editors set to LF, `* text=auto eol=lf` plus a one-time `git add --renormalize .` per affected repository, and one `AGENTS.md` rule to triage diffs with `--ignore-cr-at-eol`. Alternative considered: `autocrlf=false` (rejected: existing CRLF checkouts would show every file as modified).

## Source Weighting and Paper Fact-Checking (2026-11-02)

**Brief:** stop `internet-research` ranking sources by status, and make `latex-research-papers` fact-check every claim and reference before journal submission.

**Scope:** user direction on 2026-11-02. No external search was run for this decision.

**Findings:**

- Owners publish self-interested claims about their own outcomes. The user's example: a university's official placement statistics contradicted by student-run, student-reported placement data (such as [a student-run placements tracker](https://placements-tracker-btech2026.streamlit.app/)) and Reddit threads. Not independently verified here.
- The old rule "Primary sources first" and "Forums and issues are anecdotal" let status stand in for evidence quality.
- Journal reviewers check claims, numbers, and citations, so a citation that does not support its claim, or wrong metadata, is a rejection risk.

**Decision:** sources are weighed on transparency, verifiability, independence and incentives, recency, and relevance. First-party sources stay authoritative for what their owner defines but are checked against independent evidence on their own outcomes. Conflicts are reported with their evidence, never settled by authority. Research extracts full content (browser automation, PDFs, datasets) within legal access. Papers get a fact-check step: every claim traced to a result file or opened source, every reference checked for existence, access, metadata, retraction, and passage-level support. The reference list itself still holds only peer-reviewed papers, a venue convention, not a judgement of truth. Alternative considered: keeping a fixed source hierarchy with forums demoted (rejected: rewards status over evidence).

## Skill Linting, Tests, and CI (2026-11-03)

**Brief:** add automated checks so skill metadata, README consistency, and the two helper scripts cannot silently break, with Python 3.11 tooling, a permissive licence, and no account or paid service.

**Scope:** Agent Skills specification, PyPI and GitHub pages of `skills-ref`, `skillsaw`, and `skillscheck`, and a local trial of all three on this repository. Searched and run 2026-11-03.

**Findings:**

- The [Agent Skills specification](https://agentskills.io/specification) fixes `name` (1 to 64 lowercase letters, digits, and single hyphens, matching the folder) and `description` (1 to 1024 characters), recommends `SKILL.md` under 500 lines, and names `skills-ref validate` as its validator.
- `skills-ref` 0.1.1 (Apache-2.0, released 2026-01-10) says in its README it is "intended for demonstration purposes only" and "not meant to be used in production".
- `skillsaw` 0.22.0 (Apache-2.0, released 2026-10-16, about 1,575 commits, 17 contributors) checks spec front matter, broken internal references, unreferenced files, and content rules, with per-rule disabling in `.skillsaw.yaml`. On this repository: 0 errors and 4 warnings, of which 3 were false positives (it treats prose semicolon rules as Prettier-enforced) and 1 was real (the `research-driven-development` description lacked "Use when").
- `skillscheck` 0.9.7 reported 18 warnings, mostly "user-centric trigger" on `Use when the user asks`, a phrasing Anthropic's own spec examples use. Too opinionated for this repository.
- No linter knows this repository's own conventions: only `name` and `description` in front matter, the required body sections, `agents/openai.yaml` fields, and the README Skills table and folder count. The README said 16 skill folders while there were 14.
- Writing tests exposed six script bugs: `notebook_doctor.py` wrote CRLF on Windows, `repair` crashed on format 4.4 notebooks, `inspect` flagged missing IDs on 4.4 notebooks, and positional `mp_context` was flagged as a fork pool; `paper_check.py` resolved `\input{a.v2}` to `a.tex` and crashed on a missing `--tectonic` path. A non-raw docstring also printed `\ref` as a carriage return.

**Decision:** Adopt `skillsaw` for spec and content linting, with two noisy rules disabled and their reasons in `.skillsaw.yaml`. Build `scripts/check_repo.py` for the repository-specific conventions only. Add pytest tests for both scripts, ruff, pinned `requirements.txt`, a SHA-pinned GitHub Actions workflow running every check, and Dependabot. Alternatives considered: `skills-ref` (rejected: demonstration only, spec checks only), `skillscheck` (rejected: opinionated warnings contradict the spec's own examples), the skillsaw GitHub Action (rejected: posts PR comments and needs write permissions, while a plain CLI step needs only `contents: read`).

**Sources:**

- Standards: [Agent Skills specification](https://agentskills.io/specification).
- Registries: [skills-ref on PyPI](https://pypi.org/project/skills-ref/); [skillsaw on PyPI](https://pypi.org/project/skillsaw/); [skillscheck on PyPI](https://pypi.org/project/skillscheck/).
- Repositories: [agentskills/agentskills skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref); [stbenjam/skillsaw](https://github.com/stbenjam/skillsaw).
- Docs: [skillsaw configuration](https://skillsaw.org/configuration/).

## Naming Conventions and Skill Prompt Design (2026-11-08)

**Brief:** one repository-wide naming standard for people and agents, and skill text that small models follow reliably, without new paid or account-bound tools.

**Scope:** Anthropic skill authoring guide, ls-lint and eslint-plugin-check-file on npm, ruff rules, and this repository's own files. Searched 2026-11-08. The Reddit advice the user cited (outcomes over method, concise rules, good and bad examples, explicit negative constraints) was taken from the request, not from opened threads.

**Findings:**

- The authoring guide recommends consistent skill names (gerunds, noun phrases, or action forms, without mixing), descriptive file names ("`form_validation_rules.md`, not `doc2.md`"), one term per concept, input and output examples where output style matters, a contents list in references over 100 lines, and forward slashes in paths.
- `@ls-lint/ls-lint` 2.3.2 (MIT, updated 2026-10-17) lints file and directory names from `.ls-lint.yml`. `eslint-plugin-check-file` 3.3.2 (Apache-2.0, updated 2026-07-18) does the same inside ESLint. Ruff's pep8-naming rules (`N`) check Python identifiers.
- This repository mixed conventions: two references named only `fixes.md`, `paper_check.py` beside `check_repo.py`, a PascalCase `Resume.tex` asset, headings capitalising "And", "To", and "Of" in some files but not others, US "Rationalizations" against the Indian English rule, and test fixtures named `paper` and `doctor`. A message in `check_paper.py` pointed to a "Bookmarks" section that did not exist.
- Inference: names that state their kind and responsibility let an agent find a file by search on the first try, and a checker stops drift that a style note alone does not.

**Decision:** Build a harness-neutral `naming-conventions` skill (precedence from external contracts to defaults, a defaults table, semantic rules, examples) that target repositories record in `AGENTS.md`. Here, rename the outliers (`check_paper.py`, `latex-fixes.md`, `environment-fixes.md`, `resume-template.tex`), keep the 14 existing skill names because renaming breaks installed links and invocations, extend `scripts/check_repo.py` to enforce file names, heading case, H1 against `display_name`, intent map coverage, and worker definitions, and enable ruff `N`. Add good and bad examples to the skills where output style matters. Alternatives considered: ls-lint for this repository (runner-up: a second Node tool for checks the existing Python checker covers in a few lines); renaming every skill to gerunds (rejected: breaks links for no reader gain).

**Sources:**

- Docs: [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices); [Ruff rules](https://docs.astral.sh/ruff/rules/).
- Repositories and registries: [loeffel-io/ls-lint](https://github.com/loeffel-io/ls-lint); [@ls-lint/ls-lint on npm](https://www.npmjs.com/package/@ls-lint/ls-lint); [eslint-plugin-check-file on npm](https://www.npmjs.com/package/eslint-plugin-check-file).
