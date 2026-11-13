---
name: frontend-design
description: Builds distinctive, minimal, intuitive, fully responsive frontend UI and UX by studying several real reference products first and designing to beat them, with custom accessible components, light and dark modes, and a screenshot-verified result that never looks generic or templated. Use when the user asks to build, redesign, restyle, polish, or simplify any user-facing website, web app, page, component, dashboard, landing page, game, or design system.
---

# Frontend Design

## Overview

Generic AI frontends come from designing without references: the model falls back to its average. This skill grounds every design in several real, current products from the same domain, takes the best idea from each, avoids their weaknesses, and ships something clearer and more distinctive than all of them. Usability beats novelty, and every element must earn its place.

## When to Use

- Any new or changed user-facing UI: pages, components, apps, dashboards, games, design systems.
- Small changes to an existing UI (one component, a bug, a restyle within the system) skip steps 2 and 3 and follow the existing design system.
- Not for backend-only work or whole-repo restructuring (`production-architecture`).

## Process

1. **Brief.** Subject, user, primary task, screens, constraints, success criteria. If vague, infer concrete ones and state them. Ask only if a wrong guess makes the work unusable. Read `DESIGN.md` and the existing design system, component library, tokens, and patterns: reuse before adding.
2. **References.** Find 3 to 5 real, current references with `internet-research`: the leading products in the domain, strong direct competitors, and one adjacent product known for excellent UX. Prefer shipping products over concept shots (Dribbble and award galleries only for inspiration, never as the only references). Open each one (screenshots with a browser tool when available) and record per reference: what it does best (layout, hierarchy, a control, density, onboarding, empty states), what it does poorly, and one idea worth taking. Also look for maintained open-source component libraries or templates that fit the stack.
3. **Plan** before coding, in the reply or `DESIGN.md`:
   - Direction: one sentence on the look and feel, drawn from the subject's world (materials, vernacular, users), naming which reference ideas it combines and how it beats each.
   - Tokens: 4 to 6 named colours with roles and light and dark values, a small type scale with one or two clearly distinct families, a spacing scale.
   - Layout: the first screen as an ASCII wireframe, hierarchy, responsive behaviour, and what is left out.
   - Components: the primitives this UI needs, with states.
   - Signature: at most one memorable visual or interaction idea tied to the subject. Everything else stays disciplined.
4. **Critique the plan.** Revise anything that could fit an unrelated brief or appears in Generic Tells below. If the brief names a visual direction, follow it exactly, even when it is one of those looks.
5. **Build** the plan in repo conventions, naming per `naming-conventions`. Before building any control, form, overlay, tooltip, or scrollable panel, read [references/custom-controls.md](references/custom-controls.md). Independent screens may go to workers only when `subagent-delegation` shows it is cheaper. The plan, critique, and screenshot review stay with the orchestrator.
6. **Review screenshots** at 375px, 768px, and 1440px in light and dark modes. Read each one critically against the references: is it clearer, denser where it should be, calmer where it should be? Fix what fails, then remove one element that does not earn its place.
7. **Record** tokens, components, patterns, the references used, and decisions in `DESIGN.md` per the `project-docs` template. Run Verification.

## Quality Priorities

Check in this order. A higher item never trades away for a lower one.

1. Accessibility: 4.5:1 text contrast (3:1 large text and UI) in both themes, accessible names, visible focus, full keyboard reach, reduced-motion support, no meaning carried by colour alone.
2. Touch and interaction: 44px targets with 8px spacing, instant press feedback, no hover-only actions, loading and disabled states.
3. Layout: responsive from 320px to wide desktop and 200% zoom, no horizontal scroll, no clipped or overflowing text, reserved space for media (no layout shift).
4. Task flow: the first screen is the actual tool, app, or game unless a landing page was asked for. One primary action per view, fewest steps, progressive disclosure for advanced controls.
5. Content: real domain objects and labels, meaningful empty, error, and loading states, visible form labels (never placeholder-only) with errors beside the field.
6. Visual system: theme tokens only (no raw hex in components), one icon set, a type scale (body at least 16px on mobile, 14px minimum in dense tools, never sized by viewport width), line length under about 80 characters, every state styled.
7. Motion: 150 to 250ms eased transitions that clarify state or direct manipulation, one orchestrated moment at most.

## Generic Tells

Never use these by default, because they mark a frontend as AI-generated. Derive palette, layout, type, and motion from the subject and the references instead:

- Palettes: purple-blue gradients, warm cream with a serif and terracotta accent, near-black with acid green or neon, glassmorphism, glowing orbs and blobs.
- Layout: SaaS grids of identical rounded cards with the same soft shadow, nested cards, a card per section, oversized empty heroes, fake dashboards.
- Type and copy: a big hero number with a small label and gradient accent, one highlighted word in a headline, decorative eyebrow labels, all-caps labels everywhere, "powerful insights" copy, arrows appended to every button, lorem ipsum.
- Content: fake metrics, testimonials, logos, or social proof, repeated icon tiles, emoji as icons.
- Motion: fade-and-slide-up on every section, hover lift on every card.

Copy is written for the user: name controls by action ("Save changes", not "Submit"), keep terms consistent, make errors say what went wrong and how to fix it, and make empty states invite the next action. No text about the UI's own design.

## Examples

Bad plan: `Modern, clean dashboard with a dark theme, gradient accents, and cards for each metric.` (fits any product, no references, no task)

Good plan (illustrative):

```text
Brief: clinic receptionists rebook missed appointments, 40 to 80 a day, mostly on a desktop beside a phone.
References: Linear (keyboard-first list, instant filters), Calendly (clear slot picker), Superhuman (triage flow, one action per row), NHS app (plain-language states). Taking: Linear's list density and shortcuts, Calendly's slot grid, Superhuman's one-key triage. Avoiding: Calendly's multi-page flow, Linear's low-contrast metadata.
Direction: a calm clinical worklist, white and warm grey with one teal action colour, dense rows, nothing decorative.
First screen: missed-appointment queue (left, 60%), slot picker for the selected patient (right), "Rebook" as the single primary action.
Signature: pressing R on a row opens the next three free slots inline, so most rebookings take two keystrokes.
```

## Common Rationalisations

| Rationalisation                                   | Reality                                                                          |
| ------------------------------------------------- | -------------------------------------------------------------------------------- |
| "I know what good looks like, skip references"    | Without references the output regresses to the generic average.                  |
| "Copy the best reference closely"                 | Take ideas, not layouts or branding. The goal is to beat each reference.         |
| "A native `<select>` is accessible enough"        | It looks different on every browser and breaks the system. Build a custom one.   |
| "Sample metrics make the dashboard feel complete" | Fake data is the clearest AI tell and misleads users.                            |
| "It looks right at desktop width"                 | Most breakage is at 375px, tablet, and 200% zoom.                                |
| "Dark mode can come later"                        | Retrofitting themes means hunting hard-coded colours. Token both from the start. |

## Red Flags

- No references named for a new design, or references that were never opened.
- `alert(`, `<select`, `title=`, or native picker types in the diff.
- Raw hex, `rgb(`, or named colours outside the theme tokens.
- Any item from Generic Tells that the brief did not ask for.
- Claiming the UI looks right without reading a screenshot.

## Verification

- [ ] New designs: 3 to 5 opened references recorded with what each does best and how the design beats it.
- [ ] Screenshots at 375px, 768px, and 1440px in light and dark modes taken and read. Without browser tools, the visual result is reported unverified.
- [ ] Quality Priorities checked in order: contrast, focus, keyboard, targets, no overflow or horizontal scroll, real states.
- [ ] Searched the diff for `alert(`, `confirm(`, `prompt(`, `title=`, `<select`, `<datalist`, native picker `type=` values, `<details`, `<dialog`, `<progress`, `<meter`, and forms without `novalidate`.
- [ ] No Generic Tells, nothing placeholder or fake, and one element removed after review.
- [ ] `DESIGN.md` matches the code. Console, build, lint, and tests pass where available, and anything unverified is stated.
