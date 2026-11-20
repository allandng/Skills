# Product context

What the product-mode skill cannot guess. Keep it in the repo at `docs/product/context.md` and current. Write `unknown` where something is not known: an honest gap is more useful than a confident guess.

No customer data, no personal data, no secrets in this file.

## The product

- **What it is, in one sentence:**
- **Who it is for:**
- **The job users hire it for:**
- **Natural rhythm:** how often a user with this problem needs it (daily, weekly, per event, ...)
- **Platforms:** web / iOS / Android, and which is primary for which task
- **Units:** what is a user, what is an account or workspace, and which one retention is counted in

## Metrics

Each has a card (`playbooks/metric.md` in the skill). Link or paste them.

- **North star:**
- **Activation:** the event sequence, count and window. Hypothesis or confirmed by experiment? Date and evidence:
- **Retention:** the return event, the period
- **Core action:** the action that means a user got more value
- **Guardrails:** what must not get worse

## Lifecycle thresholds

| State | Definition here |
|---|---|
| Activated | |
| Engaged | |
| Power | |
| At risk | |
| Dormant | |

## Data

- **Analytics tool:**
- **Where events can be exported or queried:**
- **Tracking plan:** `docs/product/tracking-plan.csv`
- **Glossary:** `docs/product/glossary.csv`
- **User ID used in events:** (a stable pseudonymous ID, never an email)
- **Platform property name and values:**
- **App version property name:**
- **How internal and test users are marked:**
- **Known tracking gaps and the dates of tracking changes:**

## Release

- **Feature flag tool:**
- **Rollout stages used here:**
- **Mobile release cadence, and how long a release takes to reach most users:**

## Decisions

`docs/product/decisions.md`
