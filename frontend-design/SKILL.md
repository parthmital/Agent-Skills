---
name: frontend-design
description: "Clean, minimal, functional frontend UI and UX for websites, web apps, dashboards, landing pages, games, components, and design systems: layout, typography, colour, custom accessible components, interaction states, responsive behaviour, and copy. Use whenever the user asks to build, redesign, restyle, polish, or simplify any user-facing page, component, app, game, or dashboard. Enforces fully custom UI with no browser-native controls and a result that does not look generic, templated, or AI generated."
---

# Frontend Design

Build the usable experience asked for. Clarity, fast comprehension, and task completion matter more than visual novelty. Treat the brief, codebase, and audience as constraints, and ground every choice in the product domain so the result feels product-native rather than bloated, templated, or vibe coded.

## Approach

- If the brief is vague, infer a concrete subject, user, and primary job. Ask only if a wrong guess would make the work unusable.
- Follow the existing design system, component library, tokens, routing, data model, and interaction patterns before adding new ones.
- Make the first screen the actual tool, app, dashboard, or game unless a landing page was asked for. Tools and dashboards favour density and scanning without crowding. Games and expressive sites may carry more motion and character when it helps.
- Assets: use user- or repo-provided ones first, others only with clear source and licence, otherwise a clearly marked placeholder. Never rely on gradients, blobs, or decorative SVGs as the main visual.
- Every element must help users navigate, decide, enter data, understand state, or finish the task. Before adding a section, panel, metric, filter, tab, chart, setting, or onboarding text, name the decision or action it supports. If it only makes the page look fuller, cut it.
- Avoid AI tells: fake metrics, generic SaaS cards, placeholder testimonials, fake social proof, vague "powerful insights" copy, lorem ipsum, oversized empty heroes, random gradients, repeated icon tiles, and decoration that could belong to any product.

## Process

1. Brief: subject, audience, primary task, screens, constraints, and success criteria.
2. Plan before coding:
   - Palette: 3 to 5 named colours with roles and enough neutral space. Not a one-colour theme unless the brief requires it.
   - Type: a small, readable scale with few roles.
   - Components: reusable primitives for controls, forms, overlays, feedback, navigation, and data display.
   - Layout: grid, hierarchy, responsive behaviour, navigation, and what is left out.
   - Signature: at most one memorable visual or interaction idea tied to the subject.
3. Critique the plan. Cut clutter first, then revise anything that could fit an unrelated brief: cream editorial pages, dark neon dashboards, purple-blue gradients, glassmorphism, floating cards, orbs, generic numbered sections, boilerplate heroes, and fake dashboards.
4. Implement the plan exactly, using repo conventions.
5. Verify in desktop and mobile viewports with browser or screenshot tools when available, and read the screenshots rather than trusting the first render. Without such tools, say the visual result is unverified.

## No Browser-Native UI

Browser defaults differ across Chrome, Safari, Firefox, and mobile, so any native UI breaks consistency. Use one consistent custom component system for everything visible:

- `alert`, `confirm`, `prompt`: custom modals and toasts.
- `<select>`, `<datalist>`: custom listbox, menu, or combobox.
- Date, time, datetime-local, month, week, and colour inputs: custom pickers.
- `title` tooltips: custom tooltips.
- Native validation bubbles: `novalidate` on forms and custom inline errors.
- Checkbox, radio, range, file, number spinner, search clear button, `<progress>`, `<meter>`: `appearance: none` or hidden, with a custom control.
- `<details>` and `<summary>` markers: custom disclosure or accordion.
- `<dialog>` and popover defaults: custom modal or popover with its own backdrop, animation, and focus trap.
- Focus rings, selection colour, caret, placeholder, autofill background, scrollbars (including panels, menus, and code blocks), fonts, and user-agent spacing: style explicitly, with a reset or normalise layer and explicit font stacks.
- Drag previews and file picker triggers: a custom drop zone and button that opens the picker from code.

Allowed only as invisible plumbing:

- Real `<input>` and `<textarea>` for typing, fully restyled, because rebuilding text editing breaks IME, autofill, spell check, password managers, and mobile keyboards.
- Visually hidden native elements that give custom controls their semantics or form value.
- The OS file chooser, share sheet, and permission prompts, triggered from custom controls.

Custom controls must keep native-level behaviour: keyboard support, focus management, ARIA roles and states, screen-reader labels, escape and outside-click handling, touch targets, and mobile use. Build on the repo's headless accessible library if it has one.

## Interface Standards

- Keep choices few and obvious: one primary action per view, clear secondary actions, and progressive disclosure for advanced controls.
- Use real domain objects, realistic labels, and meaningful empty or sample states.
- Use the familiar control type: icons for common actions, segmented controls for modes, sliders or steppers for numbers, menus or comboboxes for option sets, tabs for views, and toggles or checkboxes for binary choices.
- Style every relevant state: default, hover, focus-visible, active, selected, disabled, loading, invalid, success, empty, and skeleton.
- Use cards only for repeated items, modals, or framed tools. Never nest cards or make every section a floating card.
- Keep text inside its container at every viewport with stable widths, aspect ratios, grid tracks, min and max sizes, wrapping, and overflow handling.
- Meet accessibility basics: accessible names, visible focus, sufficient contrast, keyboard reach, and reduced-motion support.
- Do not add in-app text explaining the UI's design, implementation, shortcuts, or styling unless it is part of the product.

## Copy

- Write from the user's side of the screen. Name controls by the action or object users recognise: "Save changes", not "Submit".
- Keep terminology consistent across buttons, headings, empty states, toasts, and errors.
- Empty and error states say what happened and what to do next.
- No filler, hype, or vague adjectives without visible evidence.

## Implementation

- Match the existing framework, styling stack, icon library, state management, data loading, and routing. Reuse shared components; otherwise create only the primitives this UI needs, not a full design system.
- Keep CSS specificity predictable and avoid broad selectors that override components.
- Never scale font size directly with viewport width. Use a type scale and layout changes instead.
- Animate only to clarify state, hierarchy, direct manipulation, or the subject's character.
- For 3D or canvas, use the repo's rendering library and verify the canvas is nonblank, framed, animating or interactive as intended, and usable on mobile.

## Final Check

- Desktop and mobile render without overlap or clipped text, with a clear hierarchy and no competing panels or actions.
- Primary workflows are reachable and controls show clear states.
- Nothing reads as placeholder, fake, templated, or AI generated. Assets load and fit the subject.
- No native UI remains. Search for `alert(`, `confirm(`, `prompt(`, `title=`, `<select`, `<datalist`, native picker `type=` values, `<details`, `<dialog`, `<progress`, `<meter`, and forms without `novalidate`, then check focus, selection, autofill, and scrollbar styling in the rendered UI.
- Console, build, lint, and tests pass where available. State anything unverified.
