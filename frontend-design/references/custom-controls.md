# No Browser-Native UI

Native UI differs across Chrome, Safari, Firefox, and mobile, so replace everything visible with one custom component system:

- `alert`, `confirm`, `prompt`: custom modals and toasts.
- `<select>`, `<datalist>`: custom listbox, menu, or combobox.
- Date, time, datetime-local, month, week, colour inputs: custom pickers.
- `title` tooltips: custom tooltips.
- Validation bubbles: `novalidate` plus custom inline errors.
- Checkbox, radio, range, file, number spinner, search clear button, `<progress>`, `<meter>`: `appearance: none` or hidden, with a custom control.
- `<details>` and `<summary>` markers, `<dialog>`, popovers: custom disclosure, modal, or popover with its own backdrop, animation, and focus trap.
- Focus rings, selection colour, caret, placeholder, autofill background, scrollbars (panels, menus, and code blocks too), fonts, user-agent spacing: style explicitly, with a reset layer and explicit font stacks.
- Drag previews and file pickers: a custom drop zone and a button that opens the picker from code.

Allowed only as invisible plumbing: real `<input>` and `<textarea>` for typing, fully restyled, because rebuilding text editing breaks IME, autofill, spell check, password managers, and mobile keyboards; visually hidden native elements that give custom controls semantics or form value; the OS file chooser, share sheet, and permission prompts, triggered from custom controls.

Custom controls keep native-level behaviour: keyboard support, focus management, ARIA roles and states, screen-reader labels, escape and outside-click handling, touch targets. Build on the repo's headless accessible library, else add a maintained one (such as React Aria or Radix) rather than hand-rolling behaviour.
