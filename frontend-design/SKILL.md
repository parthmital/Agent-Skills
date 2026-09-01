---
name: frontend-design
description: Clean, minimal, functional frontend, UI, and UX design guidance for websites, web apps, dashboards, landing pages, components, custom component systems, visual redesigns, CSS styling, typography, layout, colour palettes, responsive polish, interaction design, usability, accessibility, user flows, information architecture, and non-template user-facing product design. Use automatically whenever the user asks to build, redesign, restyle, modernise, polish, improve, simplify, declutter, or visually implement a frontend UI, UX flow, page, component, site, app, game, dashboard, or design system, especially when the result must use custom components, avoid browser-native looking controls, or avoid looking vibe coded, AI generated, generic, or template-like.
---

# Frontend Design

Design and build the actual usable experience the user asked for. Prioritise clarity, speed of comprehension, and successful task completion over visual novelty. Treat the brief, existing codebase, and target audience as constraints. Make deliberate choices about layout, type, colour, content, and interaction that are specific to the subject without making the interface feel bloated, complicated, overwhelming, vibe coded, or templated.

## Operating Mode

- Infer a concrete subject, user, and primary job when the brief is vague. Ask only when a wrong assumption would make the work unusable.
- Follow any existing design system, component library, brand tokens, routing, data model, and interaction pattern before adding new conventions.
- Prefer a restrained, complete product surface over a decorative mockup. Dashboards and tools should prioritise density, scanning, and repeat use without overcrowding the screen. Games and expressive sites can carry more motion and visual character only when it helps users understand or enjoy the interaction.
- Use real, searched, provided, or generated bitmap assets when visual assets are needed. Do not rely on generic gradients, abstract blobs, or decorative SVGs as the main visual signal.
- Keep all design decisions grounded in the product domain, not in trend words.
- Remove interface elements that do not help users navigate, decide, enter data, understand state, or complete the primary task.
- Make the user-facing side feel product-native and intentional. Avoid obvious AI defaults: fake metrics, generic SaaS cards, placeholder testimonials, vague feature copy, stock-looking layouts, oversized empty heroes, random gradients, repeated icon tiles, and decorative elements that could belong to any product.
- Use a consistent custom component system for the user-facing UI. Do not expose raw browser-default controls such as unstyled buttons, selects, date inputs, file inputs, checkboxes, radios, range sliders, dialogs, tooltips, or scrollbars. Native elements may be used underneath for semantics, autofill, mobile keyboards, and form behaviour, but their visible presentation must be custom, consistent, and accessible.

## Design Process

1. Establish the design brief: subject, audience, primary task, required screens, existing constraints, and success criteria.
2. Create a compact design plan before coding:
   - Palette: 3 to 5 named colours with roles and enough neutral space.
   - Type: a clear type scale with few roles and readable default sizes.
   - Components: the reusable primitives needed for controls, forms, overlays, feedback, navigation, and data display.
   - Layout: grid, hierarchy, responsive behaviour, navigation structure, and what is intentionally omitted.
   - Signature: at most one memorable visual or interaction idea tied to the subject.
3. Critique the plan before implementation. Remove clutter first. Revise anything that could fit almost any unrelated brief, especially cream editorial pages, dark neon dashboards, purple-blue gradients, glassmorphism, floating cards, decorative orbs, generic numbered sections, boilerplate hero layouts, and fake dashboards.
4. Implement the plan exactly, using repository conventions and stable responsive constraints.
5. Verify the finished UI in realistic desktop and mobile viewports when tools are available. Check screenshots rather than trusting the first render.

## Interface Standards

- Make the first screen useful. Build the application, dashboard, game, editor, or tool itself unless the user specifically asked for a landing page.
- Keep the visible choices small and obvious. Prefer one primary action per view, clear secondary actions, and progressive disclosure for advanced controls.
- Use real domain objects, realistic labels, and meaningful empty or sample states. Do not ship lorem ipsum, filler cards, fake social proof, invented metrics, or generic "powerful insights" copy.
- Implement familiar controls as custom components: icons for common actions, segmented controls for modes, sliders or steppers for numbers, menus or comboboxes for option sets, tabs for view switching, and toggles or checkboxes for binary choices.
- Style every component state deliberately: default, hover, focus-visible, active, selected, disabled, loading, invalid, success, empty, and skeleton states where relevant.
- For custom inputs, selects, comboboxes, menus, dialogs, tooltips, tabs, and toggles, preserve keyboard navigation, focus management, labels, ARIA state, pointer targets, escape and outside-click behaviour, and screen-reader output. Use proven accessible primitives already present in the repo when available.
- Use cards only for individual repeated items, modals, or genuinely framed tools. Do not nest cards inside cards or style every section as a floating card.
- Keep text inside its container at all viewports. Add stable widths, aspect ratios, grid tracks, min and max sizes, wrapping, and overflow handling where dynamic content could shift layout.
- Use accessible names, visible focus states, sufficient contrast, keyboard reachability, reduced motion support, and clear loading, empty, error, disabled, and success states.
- Do not use visible in-app text to explain the UI design, implementation, keyboard shortcuts, or visual styling unless that text is part of the user-facing product.

## Copy

- Write from the end user's side of the screen. Name controls by the action or object users recognise.
- Use active, specific labels: "Save changes" beats "Submit" when the action saves.
- Keep terminology consistent across buttons, headings, empty states, toasts, and errors.
- Treat empty and error states as guidance. Say what happened and what the user can do next.
- Avoid filler, hype, and vague adjectives unless there is visible evidence in the product.

## Implementation Discipline

- Match existing framework, styling stack, icon library, state management, data loading, and routing.
- Reuse existing shared components first. If none exist, create small custom primitives only for components used by the requested UI; do not generate a bloated design system for a narrow task.
- Keep CSS specificity predictable. Avoid broad selectors that accidentally override component styles.
- Do not scale font size directly with viewport width. Use a sensible type scale and responsive layout changes instead.
- Use animation only when it clarifies state, hierarchy, direct manipulation, or the subject's character.
- Avoid building extra panels, metrics, filters, tabs, charts, onboarding text, empty decoration, or settings unless the user asked for them or the workflow clearly needs them.
- Before adding a section or component, identify the user decision or action it supports. If it only makes the page look fuller, remove it.
- For 3D scenes, use Three.js and verify the canvas is nonblank, framed, moving or interactive as intended, and usable on mobile.

## Final Verification

Before finalising, check:

- Desktop and mobile layouts render without overlap or clipped text.
- Primary workflows are reachable and controls have clear states.
- The screen has a clear hierarchy and users are not forced to parse competing panels or actions.
- Nothing visible reads as placeholder, fake, AI generated, or copied from a generic template.
- Visual assets load and are relevant to the product or subject.
- The palette does not read as a one-colour theme unless the brief requires it.
- Console, build, lint, and test checks pass where available.
- Any unverified behaviour is stated plainly.
