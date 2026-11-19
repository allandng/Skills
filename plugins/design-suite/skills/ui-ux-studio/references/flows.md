# Flows

Everything else in this skill designs *screens*. This designs the path between them.

The distinction matters because a flow can be built entirely from good screens and still be bad: every step well-spaced, accessible, on-token, and the user still ends up stuck, asked something irrelevant, or unable to get back. Flow failures are invisible in a screenshot, which is why they survive review.

Read this whenever the work involves more than one step: sign-up, onboarding, checkout, multi-step forms, wizards, setup, upgrade paths, anything with a "next" button.

## 1. Every flow needs an escape hatch

At every step, the user must be able to leave without losing everything.

The canonical case: **a sign-up page with no link to sign in.** A returning user who lands there is stuck in a flow built for someone else, and their only move is the back button or the tab close. The same failure in other forms:

- Onboarding with no skip, on a product the user already understands
- A modal with no visible close, dismissible only by clicking outside — which is undiscoverable
- Checkout that hides the cart, so the only way to change an item is to abandon
- A wizard with no way back to a previous step
- An error state whose only affordance is "try again," on the thing that just failed

**The rule:** every step answers *what if this isn't what I wanted*. The answer is a visible control, not a browser affordance. And the escape should preserve work — a cancel that silently discards ten minutes of input is worse than no cancel.

## 2. Conditional paths — never ask what you don't need

If an answer makes later steps irrelevant, those steps must not appear.

Someone who selects "just me" should never see "invite your team." Someone on a free tier should not walk through billing. A returning user should not be asked what they already answered. Each irrelevant step is a small insult that says the product isn't paying attention.

Design the branches explicitly rather than discovering them:

```
FLOW: onboarding
  1. account            all users
  2. role               all users
  3. invite team        only if role != solo
  4. connect data       only if role in (analyst, admin)
  5. first project      all users
  DEPTH: 3 steps solo, 5 steps team admin
```

State the shortest and longest path. If the shortest is still long, the flow is the problem, not the step design.

**Cost of branching:** every branch is a state to build, test, and keep working. Two or three meaningful branches is usually right; a flow with eleven is a sign the product is asking questions it should be inferring or deferring.

## 3. Ask late, ask less

- **Defer anything not needed to complete the current job.** A payment method before the user has seen value, a company size before they have signed up — both are abandonment points collecting data for someone else's dashboard.
- **Infer instead of asking** where the answer is already available: timezone, locale, referrer, plan from the link they clicked.
- **One decision per step** in a wizard. A step with four unrelated questions is a form wearing a wizard's clothes.
- **Optional means skippable in one click**, and labelled optional at the field, not in a legend.

## 4. Steps have shape

| | Requirement |
|---|---|
| Position | The user can tell where they are and how much is left. Show real counts, not a progress bar that lies. |
| Reversibility | Back preserves entered data. Always. |
| Persistence | Refreshing or losing connection mid-flow does not start over. |
| Deep-linkability | A step the user might return to has its own URL. |
| Validation | At the field on blur, not only on submit. Errors name the fix (`copy-gate.md`). |
| Completion | The final step says what happened and what is next — never a dead end. |

## 5. States, per step

Every step in a flow needs the same state coverage a screen does, plus two that are specific to flows:

- **Resumed** — the user comes back three days later. What do they see?
- **Blocked** — a prerequisite is missing and cannot be resolved here. Say what is needed and who can provide it, rather than a disabled button with no explanation.

## 5b. Checking a flow against shipped products

Everything above is reasoned from principle. Where a flow decision is genuinely uncertain — how many steps before signup, whether a step can be deferred, what a blocked state looks like — check it against products that already solved it — via web search for teardowns and documentation, or, **if the user has the Mobbin MCP connection** (optional; check the tool list, and proceed without comment when absent):

```
search_flows   platform=web, "onboarding with team invite step"
search_flows   platform=web, "checkout with guest option"
search_screens platform=web, "empty state for a project list with no items"
```

Three things it answers better than reasoning: **step count** in a real journey, **empty and error states** (which this skill demands constantly and had no reference for), and **whether an escape hatch is actually present** in shipped work or only in advice.

Read it as evidence, not instruction. A pattern in eight products may be load-bearing convention or may be herd behavior — `conventions.md` §1 is how to tell, and the answer changes with archetype. Consumer apps optimize for a stranger's first run; an internal tool used daily has the opposite objective, and importing the consumer pattern is a downgrade.

## 6. The flow inventory

Produce this alongside the interface inventory in spec-to-ui mode, or before building any multi-step feature:

```
FLOW INVENTORY
  flow            entry points        steps  branches  escape hatch
  sign up         /, /pricing, ads    3      1         "Already have an account"
  onboarding      post sign-up        3-5    2         Skip, resumable
  checkout        cart, buy button    4      1         Back to cart, cart visible
  upgrade         in-app limit hit    2      0         Dismiss, returns to task

  ABANDONMENT     where a user is most likely to drop, and what happens
                  to their partial state when they do
```

The abandonment line is the one that gets skipped and matters most. A user who leaves mid-flow either has their progress saved and can return, or does not — and if they do not, say so out loud rather than discovering it later.

## 7. Archetype notes

Flow design is not uniform across archetypes (`archetypes.md`):

- **Single-purpose utility** — the flow should be one step. If converting a file takes a wizard, the product has failed. Escape hatch is irrelevant; there is nothing to escape from.
- **Internal tool** — captive users doing this repeatedly. Optimize for the hundredth run, not the first: keyboard paths, bulk actions, no onboarding.
- **App UI** — the flow is used repeatedly by people who know it. Progressive disclosure beats hand-holding.
- **Product marketing** — the flow is short and the escape hatch is the whole point, since most visitors are not converting today.
- **Course / educational** — the flow *is* the product, and the main constraint is learner anxiety: show position clearly, allow return, never punish a wrong turn.
