# Critique panel

Several reviewers, each with one lens, try to break a design. A finding survives only when the reviewer can point at it. The panel reports. It does not fix.

Use it before shipping anything contested, after a self-critique that found nothing (suspicious), and whenever the user asks for a review, a stress test, or "what's wrong with this". It is the adversarial half of `audit`: audit walks every dimension once, the panel attacks from positions the author does not hold.

## Why separate reviewers

The author of a design reads it with the plan in their head. They see the hierarchy they intended. A reviewer who has only the screens sees the hierarchy that is there. So each reviewer gets the artifact and the intent, and nothing else: no plan, no rationale, no earlier critique.

With subagents available, spawn one per lens with a fresh context and run them in parallel. Without them, run the lenses one at a time, write each lens's findings down before starting the next, and do not revise an earlier lens's list.

## The lenses

Pick four to six. Always include the first three.

| Lens | Holds this position | Looks for |
|---|---|---|
| **First-timer** | Has never seen the product. Has ten seconds. Cannot read the code | What is this, what do I do first, what does this word mean, where did that go |
| **Daily user** | On the hundredth run, in a hurry | Clicks per loop, missing shortcuts, anything that animates on a frequent action, density, no bulk action, no undo |
| **Access** | Keyboard only, then a screen reader, then low vision, then a small touch target | Focus order and visibility, traps, names and roles, contrast on real pairs, targets, meaning carried by color alone |
| **Hostile content** | Supplies the worst data | Zero and one item, 10,000 rows, the 200-character name, missing fields, right-to-left text, a slow or dropped connection, a double submit |
| **Builder** | Has to implement and maintain it | One-off values outside the tokens, components that differ only by accident, states modeled as booleans, layouts that cannot survive real content |
| **Category skeptic** | Has seen a thousand of these | Could this be any other product. Archetype fit, scale honesty, tells (`ai-tells.md`), borrowed-weight copy (`copy-gate.md`) |
| **Platform native** | Lives on this OS | Back, gestures, system idioms, anything that fights the platform (`platforms.md`) |
| **Skimmer** | Reads headings and buttons only | Whether the page makes sense from its labels alone |

## The brief each reviewer gets

> Here is the design and what it is for: `<intent, one or two sentences>`. Hold this position: `<lens>`. Try to break the design from that position only.
>
> Report each finding with a title, where it is (screen and region, or `file:line`), what you did or looked at, what happened, and what the intent requires instead. Attach the evidence: a screenshot region, a selector, script output, or the exact steps to reproduce it.
>
> Leave out anything you cannot point at. That covers taste, things that might matter after a future change, and general advice. No findings is a valid result.

## Verify, then merge

For each finding, go to where it points and check that it is there. Keep it when the evidence shows the problem and the problem breaks the intent. Drop the rest and count them.

Merge findings that share a root cause. Three reviewers reporting the same weak primary action from three positions is one finding with three witnesses, and those are the findings to trust most.

## Output

```
INTENT     the restatement
FINDINGS   for each: title · where · evidence · how it breaks the intent
           · which lenses found it
DROPPED    per lens: how many, and why (no evidence, taste, out of scope)
```

Say "no verified findings" when none survive. Then stop. Turning findings into fixes is the `audit` playbook's three-phase plan, or the user's call.
