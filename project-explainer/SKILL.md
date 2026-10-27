---
name: project-explainer
description: Writes EXPLAINER.md, a single beginner-friendly document at the repository root that explains the whole project from scratch for human readers, covering the problem, every component, how it works end to end, every term, method, dataset, model, hyperparameter, metric, and result, every notebook cell by cell with its outputs, and every decision with its reasons, pros, cons, and alternatives, plus likely interview questions. Use when the user asks to explain a repository, project, or codebase end to end, or to prepare for an interview, viva, presentation, demo, or pitch about a project.
---

# Project Explainer

## Overview

`EXPLAINER.md` lets someone with no background understand the project well enough to defend every part of it in an interview. It is for humans only: agents get their facts from `README.md`, `AGENTS.md`, and the other docs (`project-docs`), so this file may be long, but never padded or repetitive.

## When to Use

- Explaining a whole repository for learning, interviews, vivas, presentations, demos, or pitches.
- Not for setup docs (`readme-generator`), agent-facing docs (`project-docs`), or a LinkedIn summary (`linkedin-project-description`).

## Process

1. Read everything: source, configs, dependency manifests, tests, CI, scripts, every doc, notebooks with their saved outputs and downloaded output folders (never execute notebooks), data files' headers and sizes, and `git log` for how and why things changed.
2. Build a coverage list: every component, file group, dependency, external service, dataset, model, metric, result, and decision found. Every item gets explained.
3. For the project's type, read the matching checklists in [references/domain-checklists.md](references/domain-checklists.md) and add what they require to the coverage list.
4. For each decision, find the documented reason (`RESEARCH.md`, `ARCHITECTURE.md`, comments, commit messages). For alternatives and tradeoffs, use well-established knowledge and `internet-research` for anything current (versions, pricing, newer options).
5. Write `EXPLAINER.md` at the root with the structure below.
6. Run Verification against the coverage list.

## Structure

1. **The project in one minute**: the problem, who has it, what the project does, and the headline result, in plain words.
2. **Background**: the domain from zero, so the rest makes sense.
3. **How it works, end to end**: a diagram (Mermaid or ASCII) and a walkthrough of one real input, request, or data item travelling through the whole system, with real values from the repo.
4. **Every part explained**: one subsection per component, in the order data or control flows: what it does, how it works inside, its inputs and outputs, and why it exists.
5. **Notebooks, cell by cell** (when the repository has notebooks): one subsection per notebook, then one entry per cell in order, markdown cells included. Each entry gives the cell's purpose, what every line or block does and why, every library call, parameter, and value it sets, and every saved output (printed text, logs, tables, metrics, warnings, errors, and figures, linking the image files) with what it shows and how to read it. Close each notebook with how its cells connect and what its final results mean.
6. **Decisions**: one entry per decision with what was chosen, why, pros, cons, the main alternatives, and when an alternative would be the better choice.
7. **Results and quality**: every metric with what it measures, how to read it, and what this project's values mean; how it was tested and validated; limitations, risks, and known issues.
8. **Running and demoing it**: the shortest path to show it working, linking `README.md` for setup details.
9. **What could come next**: improvements the evidence supports.
10. **Interview and pitch preparation**: a 30-second and a 2-minute explanation; likely questions, including hard and critical ones ("why not X?", "what would break at scale?", "what was the hardest part?"), each with a short answer grounded in this document; for products, the user, value, and competitors.
11. **Glossary**: every technical term, alphabetical, one or two plain sentences each.

## Writing Rules

- Simple Indian English: short sentences, everyday words, one idea per paragraph. Define every term at its first use, even common ones, then add it to the glossary.
- Explain why before how. Use a concrete analogy for each hard idea, then the precise version.
- Use real names, numbers, and outputs from the repository in every example.
- Ground every fact in the repository. A reason that is not documented is written as "Likely reason (not recorded in the repository): ...". Never invent results, users, or history.
- Explain each thing once in full and link to it elsewhere with a relative anchor.
- ASCII only, valid Markdown, a table of contents, tables for comparisons.

## Common Rationalizations

| Rationalization                       | Reality                                                                 |
| ------------------------------------- | ----------------------------------------------------------------------- |
| "Everyone knows what an API or F1 is" | The reader may not; an interviewer will ask. Define it.                 |
| "The code is the explanation"         | The reader needs why and what else was possible, which code never says. |
| "I can guess why they chose this"     | Mark it as a likely reason; a confident guess fails in an interview.    |
| "Covering the main parts is enough"   | Interview questions target the parts that were skipped.                 |

## Red Flags

- A term used before it is defined, or missing from the glossary.
- A decision without alternatives, or a metric without an interpretation.
- A number that does not appear in the repository's code, outputs, or docs.
- A component in the coverage list with no subsection.
- A notebook cell, or a saved output, skipped, summarised as a group, or explained without its values.

## Verification

- [ ] Every notebook cell and saved output is explained individually, in order.
- [ ] Every coverage list item and every domain checklist item is explained, or noted as absent from the repository.
- [ ] Every number, name, and path checked against the repository.
- [ ] Every decision has reasons, pros, cons, and alternatives; undocumented reasons are marked.
- [ ] Every term is defined at first use and in the glossary; anchors and links work.
- [ ] The interview section answers at least one hard question per major component.
