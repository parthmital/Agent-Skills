# Research

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
