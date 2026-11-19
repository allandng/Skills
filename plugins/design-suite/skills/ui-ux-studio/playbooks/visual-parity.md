### Visual parity

**You own pixel-level equivalence. The baseline is the spec. You do not touch it.**

Adapted from pstack's Visual parity playbook. For migrations, refactors and design-system rollouts where the look must not change.

1. Establish the baseline before changing anything: captures of the current implementation across its states and sizes. No baseline, no parity claim.
2. State the anti-shortcut rules and hold them: no editing the baseline, no changing the capture setup to make a diff pass, no restructuring a component to hide a difference. If the baseline looks wrong, stop and ask.
3. Migrate one component or screen at a time. Shared primitives first.
4. Compare each against its baseline at the same size, theme, content and state. By image diff when a tool for it exists, side by side when it does not. Say which.
5. A difference is a fail until explained. Find the property that moved.
6. Repeat until there is no unexplained difference. Then the next component.

**Reply:** what was migrated, the comparison result for each with its method, where the baseline lives, any intended differences listed, what is left.
