### Build check

**You own every state of the flow, and how much it costs the user to get through it.**

1. Walk the flow as a user on each platform it ships on, before reading code.
2. For every view and component, check the seven states (`references/feature-gates.md`, gate 3). Record each as built, missing, or `n/a` with a reason.
3. Count the friction: screens, actions, fields, decisions, waits, context switches (`references/efficiency.md` §1). Then challenge each: remove, defer, infer, merge, speed up.
4. Replace confirmation dialogs with undo wherever the action can be reversed.
5. Check perceived speed on frequent actions: does the interface respond at once and reconcile on failure? What does the user see when the server refuses?
6. Accessibility: keyboard path, focus into and out of modals and drawers, semantic markup, contrast, breakpoints.
7. Check what each non-ideal state does to tracking: an error or an empty state is an event too (the `tracking-plan` skill covers the edge cases).
8. If the flow needs redesigning, not patching, hand it to `ui-ux-studio`'s flow or screen playbook with the state table and the friction count.

**Reply:** the state table per view, the friction count before and after, what was removed or deferred, accessibility findings, the platforms walked, and anything handed off.
