---
name: frontend-design
description: "Builds clean, minimal, intuitive, fully responsive frontend UI and UX with custom accessible components, light and dark modes, and proven patterns, never generic or templated. Use when the user asks to build, redesign, restyle, polish, or simplify any user-facing website, web app, page, component, dashboard, landing page, game, or design system."
---

# Frontend Design

## Overview

Build the usable experience asked for. Clarity, fast comprehension, and task completion beat visual novelty. Ground every choice in the product domain so the result feels product-native, not bloated or templated.

## When to Use

- Any new or changed user-facing UI: pages, components, apps, dashboards, games, design systems.
- Not for backend-only work or whole-repo restructuring (`production-architecture`).

## Process

1. Brief: subject, user, primary task, screens, constraints, success criteria. If vague, infer concrete ones; ask only if a wrong guess makes the work unusable.
2. Reuse the existing design system, component library, tokens, routing, data model, and interaction patterns before adding new ones. For anything missing, use `research-driven-development` to find how established products in the domain solve it and which maintained open-source libraries or templates fit; adapt proven patterns instead of inventing new ones.
3. Plan before coding:
   - Palette: 3 to 5 named colours with roles and enough neutral space, as semantic tokens with light and dark values; not one colour unless the brief requires it.
   - Type: a small readable scale with few roles.
   - Components: reusable primitives for controls, forms, overlays, feedback, navigation, and data display.
   - Layout: grid, hierarchy, responsive behaviour, navigation, and what is left out.
   - Signature: at most one memorable visual or interaction idea tied to the subject.
4. Critique the plan. Cut clutter, then revise anything that could fit an unrelated brief: cream editorial pages, dark neon dashboards, purple-blue gradients, glassmorphism, floating cards, orbs, generic numbered sections, boilerplate heroes, fake dashboards.
5. Implement the plan exactly, in repo conventions. Before building or changing any control, form, overlay, tooltip, or scrollable panel, read [references/custom-controls.md](references/custom-controls.md): every browser-native UI to replace and what may stay native.
6. Write or update root `DESIGN.md` from the `project-docs` template, in sync with the code.
7. Run Verification.

## Content

- The first screen is the actual tool, app, dashboard, or game unless a landing page was asked for. Tools favour density and scanning without crowding; games and expressive sites may carry more motion and character.
- Every element must help users navigate, decide, enter data, understand state, or finish the task. Before adding a section, panel, metric, filter, tab, chart, setting, or onboarding text, name the action it supports; cut it if it only fills the page.
- Assets: user or repo ones first, others only with clear source and licence, else a marked placeholder. Never gradients, blobs, or decorative SVGs as the main visual.
- Real domain objects, realistic labels, meaningful empty and sample states.
- No AI tells: fake metrics, testimonials, or social proof, generic SaaS cards, "powerful insights" copy, lorem ipsum, oversized empty heroes, random gradients, repeated icon tiles, decoration that fits any product.
- No in-app text about the UI's design, implementation, shortcuts, or styling unless it is part of the product.
- Copy from the user's side: name controls by the action or object ("Save changes", not "Submit"), keep terms consistent across buttons, headings, toasts, and errors, and make empty and error states say what happened and what to do next. No filler or hype.

## Interface Standards

- Light and dark modes always: default to `prefers-color-scheme`, offer a persisted toggle, set `color-scheme`, and use only theme tokens, never hard-coded colours. Both themes meet contrast.
- Simple and intuitive first: familiar patterns over novelty, fewest steps to finish the task.
- One primary action per view, clear secondary actions, progressive disclosure for advanced controls.
- Familiar control types: icons for common actions, segmented controls for modes, sliders or steppers for numbers, menus or comboboxes for option sets, tabs for views, toggles or checkboxes for binary choices.
- Style every state: default, hover, focus-visible, active, selected, disabled, loading, invalid, success, empty, skeleton.
- Cards only for repeated items, modals, or framed tools; never nested, never one per section.
- Text stays inside its container at every viewport: stable widths, aspect ratios, grid tracks, min and max sizes, wrapping, overflow handling.
- Accessible names, visible focus, sufficient contrast, keyboard reach, reduced-motion support.
- Responsive from 320px to wide desktop, tablets, touch, and 200% zoom: reflow, no horizontal scroll, 44px touch targets.
- Body text at least 14px, generous spacing. Never scale font size directly with viewport width; use a type scale and layout changes.
- Instant press feedback, 150 to 250ms eased transitions, no layout shift. Animate only to clarify state, hierarchy, direct manipulation, or the subject's character.
- One consistent, subject-specific icon set; no scattered default icons or emoji.
- Match the existing framework, styling stack, icon library, state management, data loading, and routing. Create only the primitives this UI needs. Keep CSS specificity predictable; no broad overriding selectors.
- 3D or canvas: use the repo's rendering library; the canvas must be nonblank, framed, animating or interactive as intended, and usable on mobile.

## Common Rationalizations

| Rationalization                                   | Reality                                                                                   |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| "A native `<select>` is accessible enough"        | It looks different on every browser and breaks the system. Build a custom accessible one. |
| "Sample metrics make the dashboard feel complete" | Fake data is the clearest AI tell and misleads users.                                     |
| "More sections show more effort"                  | Elements with no user action behind them are clutter.                                     |
| "It looks right at desktop width"                 | Most breakage is at 320px, tablet, and 200% zoom.                                         |
| "Dark mode can come later"                        | Retrofitting themes means hunting hard-coded colours. Token both themes from the start.   |

## Red Flags

- `alert(`, `<select`, `title=`, or native picker types in the diff.
- Clipped text or horizontal scroll at narrow widths.
- Hex, `rgb(`, or named colours outside the theme tokens.
- A visual idea that would fit an unrelated brief.
- Claiming the UI looks right without reading a screenshot.

## Verification

- [ ] Desktop and mobile screenshots in light and dark modes taken and read, not trusted on first render. Without browser or screenshot tools, the visual result is reported unverified.
- [ ] Phone, tablet, desktop: no overlap or clipped text, clear hierarchy, no competing panels or actions.
- [ ] Primary workflows reachable; controls show clear states; legible, smooth, consistent icons.
- [ ] Nothing placeholder, fake, templated, or AI-looking; assets load and fit.
- [ ] Searched for `alert(`, `confirm(`, `prompt(`, `title=`, `<select`, `<datalist`, native picker `type=` values, `<details`, `<dialog`, `<progress`, `<meter`, and forms without `novalidate`; focus, selection, autofill, and scrollbars checked in the render.
- [ ] `DESIGN.md` matches the code.
- [ ] Console, build, lint, and tests pass where available; anything unverified is stated.
