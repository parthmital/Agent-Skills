---
name: skill-improvement
description: Records the reusable fix for a solved problem in the skill the agent will load when it recurs, and creates, edits, merges, or trims agent skills so no problem is solved twice and context stays small. Use after resolving a hard, non-obvious, or repeated problem (several failed attempts, an unclear root cause, a tool or environment quirk, a user correction), when a skill rule was wrong, missing, or caused a mistake, or when the user asks to improve, update, create, deduplicate, or shorten skills, AGENTS.md, or lessons learned.
---

# Skill Improvement

## Overview

Skills are the agent's memory. Each hard problem is solved once, then written where the next agent will read it at the moment the problem recurs, in the fewest words that prevent the repeat.

## When to Use

- Record after the fix is verified, when the problem took more than one attempt, had a non-obvious cause, exposed a wrong or missing skill rule, or the user corrected the approach.
- Skip one-off slips, facts the target repository already documents, and anything the agent gets right by default.
- Facts about one project (its commands, quirks, layout) go in that project's `AGENTS.md` or docs, never in a global skill.

## Process

1. Look before solving. On a non-trivial error, search the skills directory for its distinctive text, and read the owning skill's `references/`. Apply a recorded fix; if it fails, correct that entry instead of adding another.
2. Generalise: the symptom as the agent sees it (exact error text or observable sign, so a search finds it), root cause, fix, and how to confirm. Drop session narrative, machine paths, names, and secrets.
3. Place it in the cheapest location that is loaded when the problem recurs:

   | Scope                                         | Location                                                                  |
   | --------------------------------------------- | ------------------------------------------------------------------------- |
   | Every run of a skill needs it                 | Rule in that `SKILL.md`                                                   |
   | Only some runs of a skill                     | Entry in its `references/<topic>.md`, with a pointer in `SKILL.md` if new |
   | A script or check can catch it                | The skill's script, plus a one-line rule                                  |
   | The skill did not trigger                     | Missing trigger words added to its `description`                          |
   | A recurring workflow no skill covers          | New skill, per the README's Writing And Maintaining Skills                |
   | Tool or environment quirk with no owner skill | [references/fixes.md](references/fixes.md)                                |
   | Every task, every repository                  | One line in `AGENTS.md`                                                   |

4. Merge, never append: rewrite the rule or entry that already covers the area, and delete rules that proved wrong or redundant. Aim for no net growth.
5. Write entries as `- **<symptom>**: <cause>. <fix>. Check: <how>.` in one to three lines.
6. Keep budgets: description at most 1024 characters, `SKILL.md` well under 500 lines, references one level deep.
7. Edit the source repository of the skills. If the installed skill folders are not links to it, copy the changed folders over and confirm with a recursive diff. Update its README, `agents/openai.yaml`, and `RESEARCH.md` as the change requires, and run its checks. Commit only when asked (`git-commit-and-push`).
8. Report in one line what was recorded and where.

## Common Rationalizations

| Rationalization                        | Reality                                                                   |
| -------------------------------------- | ------------------------------------------------------------------------- |
| "I will remember next time"            | The next session starts empty; only loaded text persists.                 |
| "Add a new section, it is safer"       | Appending duplicates rules and costs context in every later run; merge.   |
| "Write down the whole debugging story" | The next agent needs symptom, cause, fix, and check, nothing else.        |
| "Put it in AGENTS.md so it is seen"    | `AGENTS.md` loads every session; only cross-cutting rules earn that cost. |

## Red Flags

- The same error solved twice across sessions with no entry recorded.
- An entry without the searchable symptom text, or with a machine path or secret.
- A skill or `AGENTS.md` that grew with no rule removed or merged.
- The installed copy differs from the source repository.

## Verification

- [ ] Fix verified before it was recorded.
- [ ] Skills searched first; an existing entry was corrected rather than duplicated.
- [ ] Entry sits in the cheapest location loaded when the problem recurs, in the entry format.
- [ ] Budgets hold; README, `agents/openai.yaml`, and `RESEARCH.md` updated as needed; repository checks pass.
- [ ] Installed skills match the source repository.
