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

## Skill Token Budgets And Progressive Disclosure (2026-10-21)

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

## Plan-Then-Execute Handoff To Cheaper Models (2026-10-26)

**Brief:** a frontier model writes a plan that a cheaper model (Gemini Flash in Antigravity, a smaller Claude or GPT, a local model in OpenCode) executes reliably, across tools.

**Scope:** obra/superpowers `writing-plans`, official command docs for Antigravity, Claude Code, Codex, and OpenCode. Searched 2026-10-26.

**Findings:**

- Superpowers `writing-plans` writes one plan file of small tasks, each with files, interfaces, tests, verification commands and expected output, and frequent commits, for an executor who "has not seen the codebase". It gives code bodies only where signatures and tests do not determine the algorithm, and executes with a fresh subagent per task.
- Antigravity: `/goal` blocks the agent from ending its turn until it maps every deliverable to evidence, with no iteration cap and one goal per conversation; the docs suggest `/plan` first, then handing the plan to `/goal`. `/boost` (multi-agent deep reasoning) and `/teamwork-preview` (agent teams for repo-scale work) are paid-plan only. App and CLI support slash commands.
- Claude Code: `/goal <condition>` starts work immediately and a separate small model judges the condition after every turn; conditions should name a measurable end state, the check that proves it, and constraints, and may cap turns. `/clear` starts a fresh context.
- Codex: `/goal <objective>` from Codex 0.128.0, with `pause`, `resume`, `clear`; recommended form "end state verified by evidence while preserving constraints".
- OpenCode: no goal mode; `/new` starts a session, `/models` picks a model, Tab cycles primary agents, and the Plan agent cannot edit files.
- Inference: weak executors fail on undecided choices and algorithms, and lose the thread in long files, so plans for them need complete code and one file per task, beyond what superpowers gives a capable executor.

**Decision:** Borrow. A new `implementation-plan` skill writes `plans/<slug>/` with `START-HERE.md`, `CHECKLIST.md`, and one self-contained task file per commit-sized task, plus a shared NEXT and DONE prompt wrapped in each tool's goal command. Revised 2026-10-27 after user feedback: one RUN and DONE goal prompt now runs the whole checklist in one conversation (idempotent, so pasting it again resumes), Expand lines are expanded and continued in the same run, human-only work goes to a non-blocking owner queue with `[~]` lines and later Reference pass lines, a self-unblock procedure precedes any stop, and the planner no longer builds, tests, trials migrations, or executes any task, because planner execution spends the budget the handoff exists to save. Alternatives considered: installing superpowers (rejected: single-file plans for capable executors, Claude Code plugin oriented); Spec Kit (rejected: heavier spec workflow, not aimed at weak executors). Removed 2026-10-27 at the user's request.

**Sources:**

- Repository: [obra/superpowers writing-plans](https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-plans/SKILL.md).
- Docs: [Antigravity slash commands](https://antigravity.google/docs/slash-commands/); [Antigravity /goal](https://antigravity.google/docs/commands/goal/); [Claude Code commands](https://code.claude.com/docs/en/commands); [Claude Code /goal](https://code.claude.com/docs/en/goal.md); [Using Goals in Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex); [OpenCode TUI commands](https://opencode.ai/docs/tui); [OpenCode agents](https://opencode.ai/docs/agents).

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

## Windows Line Endings In Agent Diffs (2026-10-26)

**Brief:** stop agents analysing line-ending-only diffs on Windows.

**Scope:** local experiments with Git 2.54.0.windows.1 on 2026-10-26.

**Findings:**

- Git for Windows sets `core.autocrlf=true` in the system config. Formatters then write LF files and every touched file prints "LF will be replaced by CRLF the next time Git touches it".
- With LF in the index, a CRLF or LF working file shows no change under `autocrlf=true` or `input`, but shows as modified under `false`.
- With CRLF committed in the index, a file rewritten as LF shows as modified under every setting; only renormalising the repository fixes it.
- `git diff --ignore-cr-at-eol --stat` omits files whose only change is line endings.

**Decision:** `core.autocrlf=input` in the global config (LF checkouts, LF commits, existing CRLF checkouts stay clean), editors set to LF, `* text=auto eol=lf` plus a one-time `git add --renormalize .` per affected repository, and one `AGENTS.md` rule to triage diffs with `--ignore-cr-at-eol`. Alternative considered: `autocrlf=false` (rejected: existing CRLF checkouts would show every file as modified).
