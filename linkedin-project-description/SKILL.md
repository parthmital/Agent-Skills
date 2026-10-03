---
name: linkedin-project-description
description: Turns a project README or write-up into a LinkedIn project description of at most 1000 characters, grounded only in the source. Use when the user asks for a LinkedIn project description, LinkedIn project summary, LinkedIn post about a project, or to convert a README for LinkedIn.
---

# LinkedIn Project Description

## Overview

A short, factual LinkedIn description that recruiters and engineers both understand, using only claims the source supports.

## When to Use

- Converting a README or project write-up for LinkedIn.
- Not for resumes (`resume-tailoring`) or READMEs (`readme-generator`).

## Process

1. Get the source; ask if none is given. For a repository, read `README.md` and any linked docs holding metrics.
2. Silently identify: purpose and users, 3 to 5 main technical contributions, the strongest supported metrics, clear impact, and what to leave out.
3. Write one simple sentence on what was built and why, then 3 to 5 concise bullets starting with `•`, ordered what, how, then measurable impact.
4. Count characters including spaces and punctuation; cut to 1000 or fewer.

## Rules

- Technologies, scale, workflows, and metrics only when the source supports them; no tech-stack list.
- Metrics and units exactly as in the source. Never invent, estimate, infer, or exaggerate.
- Combine related features; focus on substantial engineering and clear outcomes.
- Strong verbs (Built, Designed, Engineered, Automated, Implemented, Developed). No buzzwords such as "cutting-edge", "innovative", "seamless", "scalable", "revolutionary".
- If the source contradicts itself, use the most specific or current information without guessing.
- Reply with only the description in one code block: no title, intro, or citations. Add one short line after it only when something needs attention, such as a contradiction or an unsupported claim left out.

## Common Rationalizations

| Rationalization                    | Reality                               |
| ---------------------------------- | ------------------------------------- |
| "Rounding the metric reads better" | Changed numbers are invented numbers. |
| "Listing every tool shows breadth" | Tech lists bury the impact.           |

## Red Flags

- Any number not found verbatim in the source.
- Text outside the code block beyond one attention line.

## Verification

- [ ] At most 1000 characters, counted.
- [ ] Every claim and metric traces to the source.
- [ ] One opening sentence plus 3 to 5 `•` bullets.
