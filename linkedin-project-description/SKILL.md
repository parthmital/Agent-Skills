---
name: linkedin-project-description
description: Turns a project README or write-up into a LinkedIn project description of at most 500 characters, grounded only in the source. Use when the user asks for a LinkedIn project description, LinkedIn project summary, LinkedIn post about a project, or to convert a README for LinkedIn.
---

# LinkedIn Project Description

## Overview

A short, factual LinkedIn description that recruiters and engineers both understand, using only claims the source supports.

## When to Use

- Converting a README or project write-up for LinkedIn.
- Not for resumes (`resume-tailoring`) or READMEs (`readme-generator`).

## Process

1. Get the source; ask if none is given. For a repository, read `README.md` and any linked docs holding metrics.
2. Silently list everything that must appear: purpose and users, every major feature or technical contribution, key technologies, every headline metric, and the impact.
3. Write one simple sentence on what was built and why, then 3 to 6 concise bullets starting with `•`, ordered what, how, then measurable impact. A bullet may carry several related items.
4. Count characters including spaces and punctuation. Over 500: compress, never drop a listed item. In order: cut filler and adjectives, shorten phrasing, merge related bullets, fold technologies into the clause they serve, use symbols (`&`, `~`, `→`, `+`) and common abbreviations. Recount after each pass.

## Rules

- Technologies, scale, workflows, and metrics only when the source supports them; no tech-stack list.
- Metrics and units exactly as in the source. Never invent, estimate, infer, or exaggerate.
- Combine related features into one clause rather than omitting any; substantial engineering and outcomes first.
- Strong verbs (Built, Designed, Engineered, Automated, Implemented, Developed). No buzzwords such as "cutting-edge", "innovative", "seamless", "scalable", "revolutionary".
- If the source contradicts itself, use the most specific or current information without guessing.
- Reply with only the description in one code block: no title, intro, or citations. Add one short line after it only when something needs attention, such as a contradiction, an unsupported claim left out, or a listed item that could not fit even after full compression.

## Common Rationalizations

| Rationalization                    | Reality                               |
| ---------------------------------- | ------------------------------------- |
| "Rounding the metric reads better" | Changed numbers are invented numbers. |
| "Listing every tool shows breadth" | Tech lists bury the impact.           |
| "It's over 500, drop a feature"    | Compress the wording; items stay.     |

## Red Flags

- Any number not found verbatim in the source.
- Text outside the code block beyond one attention line.
- A listed feature or metric missing from the final text.

## Verification

- [ ] At most 500 characters, counted.
- [ ] Every claim and metric traces to the source.
- [ ] One opening sentence plus 3 to 6 `•` bullets.
- [ ] Every item from step 2 appears, or the attention line names what could not fit.
