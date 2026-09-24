---
name: frontend-design
description: Clean, minimal, functional frontend UI and UX design for websites, web apps, dashboards, landing pages, components, and design systems, covering layout, typography, colour, custom accessible components, interaction states, responsive behaviour, and copy. Use automatically when the user asks to build, redesign, restyle, polish, or simplify a user-facing page, component, app, game, or dashboard. Every visible control, popup, and piece of feedback must be a custom component with no browser-native UI, and the result must not look generic, templated, or AI generated.
---

# Frontend Design

Design and build the actual usable experience the user asked for. Prioritise clarity, speed of comprehension, and successful task completion over visual novelty. Treat the brief, existing codebase, and target audience as constraints. Make deliberate choices about layout, type, colour, content, and interaction that are specific to the subject without making the interface feel bloated, complicated, overwhelming, vibe coded, or templated.

## Operating Mode

- Infer a concrete subject, user, and primary job when the brief is vague. Ask only when a wrong assumption would make the work unusable.
- Follow any existing design system, component library, brand tokens, routing, data model, and interaction pattern before adding new conventions.
- Prefer a restrained, complete product surface over a decorative mockup. Dashboards and tools should prioritise density, scanning, and repeat use without overcrowding the screen. Games and expressive sites can carry more motion and visual character only when it helps users understand or enjoy the interaction.
- When visual assets are needed, use assets provided by the user or already in the repository first. Use other assets only when their source and licence are clear, and otherwise leave a clearly marked placeholder. Do not rely on generic gradients, abstract blobs, or decorative SVGs as the main visual signal.
- Keep all design decisions grounded in the product domain, not in trend words.
- When the `ui-ux-design-reference`, `shadcn-tailwind-ui`, or `design-system` skills are available, use them as references for palettes, font pairings, UX guidelines, tokens, and stack-specific guidance. Treat its results as suggestions. This skill's rules take precedence, including no browser-native UI and avoiding generic styles such as glassmorphism, random gradients, and floating cards.
- Remove interface elements that do not help users navigate, decide, enter data, understand state, or complete the primary task.
- Make the user-facing side feel product-native and intentional. Avoid obvious AI defaults: fake metrics, generic SaaS cards, placeholder testimonials, vague feature copy, stock-looking layouts, oversized empty heroes, random gradients, repeated icon tiles, and decorative elements that could belong to any product.
- Use one consistent custom component system for the whole user-facing UI. Nothing the user sees or interacts with may be browser-native. See No Browser-Native UI below.

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
5. Verify the finished UI in realistic desktop and mobile viewports when browser or screenshot tools are available. Check screenshots rather than trusting the first render. If no such tools are available, say that the visual result was not verified.

## No Browser-Native UI

Everything visible must be custom so the look and behaviour are consistent across browsers and fully under the product's control. Browser defaults differ between Chrome, Safari, Firefox, and mobile browsers, so any native UI left in place breaks consistency.

Replace, never ship:

- `alert()`, `confirm()`, and `prompt()`: use custom modal dialogs and toasts.
- Native `<select>` dropdowns and `<datalist>` suggestions: use a custom listbox, menu, or combobox.
- `<input type="date">`, `time`, `datetime-local`, `month`, `week`, and `color` pickers: use custom date, time, and colour pickers.
- `title` attribute tooltips: use custom tooltips.
- Native form validation bubbles: set `novalidate` on forms and show custom inline errors.
- Default checkbox, radio, range, file, number spinner, search clear button, `<progress>`, and `<meter>` appearance: set `appearance: none` or hide the element, and render a custom control.
- Default `<details>` and `<summary>` markers: use a custom disclosure or accordion.
- Default `<dialog>` and popover presentation: use a custom modal or popover component with its own backdrop, animation, and focus trap.
- Default focus rings, text selection colour, caret colour, placeholder styling, and autofill background: style them all explicitly.
- Default scrollbars: style them to match the product, including in scrollable panels, menus, and code blocks.
- Default browser fonts and user-agent spacing: set a CSS reset or normalise layer and explicit font stacks.
- Default drag previews and file picker triggers: use a custom drop zone and button, and open the file picker from code.

Allowed only as invisible plumbing:

- Real `<input>` and `<textarea>` elements for typing text. Rebuilding text editing breaks IME, autofill, spell check, password managers, and mobile keyboards. They must be fully restyled so no default appearance remains.
- Hidden native elements that give custom controls their semantics or form value, such as a visually hidden checkbox or file input.
- The operating system file chooser, share sheet, and permission prompts, which web pages cannot replace. Trigger them from custom controls.

Every custom replacement must keep native-level behaviour: keyboard support, focus management, ARIA roles and states, screen-reader labels, escape and outside-click handling, touch targets, and mobile usability. If the repository has a headless accessible component library, build on it rather than hand-rolling behaviour.

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
- For 3D or canvas scenes, use the repository's existing rendering library where one exists, and verify the canvas is nonblank, framed, moving or interactive as intended, and usable on mobile.

## Final Verification

Before finalising, check:

- Desktop and mobile layouts render without overlap or clipped text.
- Primary workflows are reachable and controls have clear states.
- The screen has a clear hierarchy and users are not forced to parse competing panels or actions.
- Nothing visible reads as placeholder, fake, AI generated, or copied from a generic template.
- No browser-native UI remains: search the code for `alert(`, `confirm(`, `prompt(`, `title=`, `<select`, `<datalist`, `type="date"` and other native picker types, `<details`, `<dialog`, `<progress`, `<meter`, and forms without `novalidate`, and check focus, selection, autofill, and scrollbar styling in the rendered UI.
- Visual assets load and are relevant to the product or subject.
- The palette does not read as a one-colour theme unless the brief requires it.
- Console, build, lint, and test checks pass where available.
- Any unverified behaviour is stated plainly.
