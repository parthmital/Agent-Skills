---
name: skill-improvement
description: Records the reusable fix for a solved problem in the skill the agent will load when it recurs, and creates, edits, merges, tests, or trims agent skills to a workflow standard (steps, examples, verification) so no problem is solved twice and context stays small. Use after resolving a hard, non-obvious, or repeated problem (several failed attempts, an unclear root cause, a tool or environment quirk, a user correction), when a skill rule was wrong, missing, or caused a mistake, or when the user asks to improve, update, create, merge, deduplicate, or shorten skills, AGENTS.md, or lessons learned.
---

# Skill Improvement

## Overview

Skills are the agent's memory and its workflows. Each hard problem is solved once, then written where the next agent reads it at the moment the problem recurs, in the fewest words that prevent the repeat. Every skill is a workflow the agent executes, not guidance it skims: numbered steps with checkpoints, few-shot examples of the standard to meet, and a checklist of evidence.

## When to Use

- Record after the fix is verified, when the problem took more than one attempt, had a non-obvious cause, exposed a wrong or missing skill rule, or the user corrected the approach.
- Skip one-off slips, facts the target repository already documents, and anything the agent gets right by default.
- Facts about one project (its commands, quirks, layout) go in that project's `AGENTS.md` or docs, never in a global skill.
- Creating, upgrading, or merging a skill: follow Skill Anatomy and step 7.

## Skill Anatomy

Every `SKILL.md` has front matter with only `name` and `description` (what it does and when to use it, third person, trigger words, at most 1024 characters), then these sections, checked by `scripts/check_repo.py` in this repository:

- `## Overview`: the outcome and why it matters, in a few sentences.
- `## When to Use`: triggers, exclusions, and which skill owns neighbouring work.
- `## Process`: numbered steps, each ending in something checkable. Low freedom (exact commands) for fragile steps, high freedom for judgement.
- `## Examples`: at least one Bad and one Good example of the output standard, concrete, marked illustrative when invented.
- `## Common Rationalisations`: the excuses agents use to skip steps, each with its rebuttal.
- `## Red Flags`: observable signs the skill is being violated.
- `## Verification`: a checklist of evidence, never "seems right".

Body under 500 lines, and under about 150 where the workflow allows. Conditional detail goes in `references/<topic>.md`, one level deep, each linked from `SKILL.md` with when to read it. Deterministic checks go in `scripts/`. No em dashes or semicolons.

## Process

1. **Look before solving.** On a non-trivial error, search the skills directory for its distinctive text and read the owning skill's `references/`. Apply a recorded fix. If it fails, correct that entry instead of adding another.
2. **Generalise**: the symptom as the agent sees it (exact error text or observable sign, so a search finds it), root cause, fix, and how to confirm. Drop session narrative, machine paths, names, and secrets.
3. **Place** it in the cheapest location that is loaded when the problem recurs:

   | Scope                                         | Location                                                                  |
   | --------------------------------------------- | ------------------------------------------------------------------------- |
   | Every run of a skill needs it                 | Rule or step in that `SKILL.md`                                           |
   | Only some runs of a skill                     | Entry in its `references/<topic>.md`, with a pointer in `SKILL.md` if new |
   | A script or check can catch it                | The skill's script, plus a one-line rule                                  |
   | The skill did not trigger                     | Missing trigger words added to its `description`                          |
   | A recurring workflow no skill covers          | New skill, per Skill Anatomy                                              |
   | Tool or environment quirk with no owner skill | [references/environment-fixes.md](references/environment-fixes.md)        |
   | Every task, every repository                  | One line in `AGENTS.md`                                                   |

4. **Merge, never append**: rewrite the rule or entry that already covers the area, and delete rules that proved wrong or redundant. Aim for no net growth. Merge whole skills when two share most of their rules and triggers, and keep them separate when their workflows differ.
5. **Write entries** as `- **<symptom>**: <cause>. <fix>. Check: <how>.` in one to three lines, like [references/environment-fixes.md](references/environment-fixes.md).
6. **Write for the least capable model** that runs the skill, including Haiku workers: explicit steps, stated negative constraints, and examples where output style matters, without explaining what any model already knows.
7. **Upgrading or creating a skill**: research the best existing skills and current practice for the domain with `internet-research` (skill registries such as skills.sh, well-maintained skill repositories, vendor docs), adopt what beats the current text, then trial it once on a representative task in a fresh context. Fix every step the trial skipped or misread.
8. **Ship**: edit the source repository of the skills (installed skills are links to it, otherwise copy the changed folders and confirm with a recursive diff). Update its README, `agents/openai.yaml`, and `RESEARCH.md` as the change requires, and run its checks. Commit only when asked (`git-commit-and-push`).
9. **Report** in one line what was recorded or changed and where.

## Examples

Bad entry: `Had a lot of trouble with the build today, eventually fixed it by changing some settings in the config.`

Good entry:

```text
- **`EPERM: operation not permitted, symlink` during `npm install` on Windows**: Developer Mode is off, so symlinks need admin rights. Set `npm_config_bin_links=false` for the install, or enable Developer Mode. Check: `npm ls` exits 0.
```

Bad skill step: `Make sure the UI looks good.` Good skill step: `Take screenshots at 375px and 1440px in light and dark modes, read each one, and fix any clipped text or horizontal scroll before continuing.`

## Common Rationalisations

| Rationalisation                        | Reality                                                                   |
| -------------------------------------- | ------------------------------------------------------------------------- |
| "I will remember next time"            | The next session starts empty. Only loaded text persists.                 |
| "Add a new section, it is safer"       | Appending duplicates rules and costs context in every later run. Merge.   |
| "Write down the whole debugging story" | The next agent needs symptom, cause, fix, and check, nothing else.        |
| "Put it in AGENTS.md so it is seen"    | `AGENTS.md` loads every session. Only cross-cutting rules earn that cost. |
| "The rule is clear, no example needed" | Clear to the writer is not clear to a smaller model. Show the standard.   |

## Red Flags

- The same error solved twice across sessions with no entry recorded.
- An entry without searchable symptom text, or with a machine path or secret.
- A skill or `AGENTS.md` that grew with no rule removed or merged.
- A skill step with no checkable outcome, or a skill with no Good and Bad example.
- The installed copy differs from the source repository.

## Verification

- [ ] Fix verified before it was recorded, and skills searched first so an existing entry was corrected rather than duplicated.
- [ ] Entry sits in the cheapest location loaded when the problem recurs, in the entry format.
- [ ] Changed skills follow Skill Anatomy and the budgets, and `scripts/check_repo.py` passes where it exists.
- [ ] README, `agents/openai.yaml`, and `RESEARCH.md` updated wherever the change affects them.
- [ ] Installed skills match the source repository.
