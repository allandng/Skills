---
name: onboarding
description: Tear down and improve the path from sign-up to first value in a web or mobile app. Signs up fresh and records every screen, field, decision, and wait; classifies each step as value, required for value, or neither; measures time-to-value and drop-off per step by platform; and produces ranked, testable changes - what to remove, defer, default, or explain. Covers empty states, permission prompts, progressive disclosure, contextual guidance instead of tours, and getting activated users to deeper use. Use when new users sign up and do not come back, when onboarding or activation is being designed or reviewed, when time-to-value is too long, or when comparing web and app onboarding.
---

# Onboarding

Onboarding is the distance between a person deciding to try the product and the product doing something for them. Everything in that distance is cost. The work is to make the distance shorter, and to prove that it got shorter.

The stance: a new user arrived with a reason. They are not there to learn the interface, complete a profile, or take a tour. Get them to the thing they came for, then earn the rest.

## 1. Name the first-value moment

Before looking at any screen: what is the first moment this product has done something the user wanted?

- It is an outcome for the user, not an action for the company. "Published their first event" is one. "Completed their profile" is not.
- A product with two kinds of user has two. An organizer's first value and an attendee's are different moments on different paths.
- If the team has an activation definition in `docs/product/context.md`, start there, and note whether it is a hypothesis or was confirmed by an experiment.

Then split what is around it into three moments, because each is a different problem:

| Moment | What it is | Fails as |
|---|---|---|
| **Setup** | What must exist before value is possible | Too much asked too early |
| **First value** | The outcome the user came for, once | Too far away, or not noticed when it happens |
| **Habit** | The second and third time, at the product's natural rhythm | No reason or reminder to return |

## 2. The teardown

Sign up as a new user, on each platform, with a fresh account. Record every step in the format in `references/teardown.md`: what the screen asks, how many fields and decisions, how long it took, and what would happen if the step were not there.

Do it yourself before reading the code or the funnel. The teardown is the only source for what the experience is like, and the people who built it can no longer see it.

Classify every step:

| Class | Meaning | What to do |
|---|---|---|
| **Value** | The user gets something they wanted | Keep, and bring earlier |
| **Required** | Value is impossible without it | Keep, and make it as light as possible |
| **Neither** | Helps the company, or helps later | Remove, or defer until after first value |

Most onboarding is longer than it needs to be because of the third class: profile photos, team invites, notification preferences, billing details, a survey about how they heard of you. Each is defensible alone. Together they are the reason people leave.

## 3. Measure it

With the `product-analytics` skill, on the events for these steps:

- The funnel over the onboarding steps, by platform and by source, with intervals.
- The median and 90th-percentile wait at each step. The median from sign-up to first value is the time-to-value. The 90th percentile is what the slowest tenth experience.
- Users who entered too recently are left out automatically.

If the steps are not tracked, that is the first finding. Instrument them with the `tracking-plan` skill before changing anything, or the change cannot be evaluated.

Put the teardown next to the funnel. The step where the teardown says "nine fields" and the funnel says "loses 40%" is the place to start.

## 4. What usually works

In the order to try them. Each is a hypothesis for this product until tested.

1. **Remove the step.** Does the product work without the answer?
2. **Defer it.** Ask after first value, at the moment the answer is needed. Ask for a teammate's email when the user tries to share, not on screen two.
3. **Default it.** Infer from locale, device, the sign-up source, or what most users choose. Let them change it later.
4. **Do it for them.** A template, sample data, or a pre-filled example. An empty product asks the user to imagine the value. A populated one shows it.
5. **Let them in before sign-up.** If value can be shown without an account, show it, then ask.
6. **Make the empty state do the work.** Never a blank screen with "No items yet". Say what belongs here and why it is worth having, and give one action.
7. **Guide in context.** Inline hints, good defaults, and a checklist tied to real actions. A multi-step tour is dismissed and teaches nothing: the user has not hit the problem the tour is solving.
8. **Reveal as needed.** Advanced settings and power features appear when behaviour shows the user is ready for them.
9. **Say when it worked.** First value that happens silently is missed. Confirm it in plain words.

Efficiency is part of this: `product-mode`'s efficiency reference has the friction count and how to challenge each line.

## 5. Mobile and web are different onboardings

- **Mobile adds steps:** install, launch, and permission prompts. Each is a funnel step with its own drop.
- **Ask for a permission when it is needed,** after saying why in your own words. A system prompt on first launch, before the user knows what it is for, is often denied, and cannot easily be asked again.
- **Typing is expensive on a phone.** Every field costs more. Use the right keyboard, autofill, sign-in with a platform account, and codes that fill themselves.
- **People switch.** Many sign up on web and open the app later, or the reverse. The second surface should recognize them, not onboard them again.
- **Deep links are onboarding.** An invited user who taps a link should land on the thing they were invited to, signed in or one step from it.

Run the teardown, the funnel and the changes per platform.

## 6. Look at how others handle the hard step

For the step that loses the most, look at how shipped products in the same category handle it. This is evidence about conventions, not a source of design. Carry away counts: how many steps before first value, which ask for this before or after, what the empty state offers.

With the Mobbin connector available, search flows by app kind and journey, and look at the returned screens instead of summarizing from metadata. Without it, sign up for two or three competing products and tear them down the same way. Record:

```
QUESTION    How many steps before first value in ticketing-app organizer onboarding?
LOOKED AT   5 products, <date>
FOUND       3, 4, 4, 6, 9 steps. 4 of 5 defer payout details until after the
            first event is drafted. 1 of 5 requires them first.
TAKE        deferring payout details is the convention. Requiring it early is not.
```

## 7. After activation: more of the value

"Maximizing user potential" means a user getting more of what the product can do for them. It is measured in their outcomes, not their minutes.

- Find what power users use that most users have never opened (`product-mode`'s engagement playbook).
- For each: is it undiscovered or unwanted? Only the first is an onboarding problem.
- Introduce a feature at the moment the user hits the problem it solves. That is the only time the explanation lands.
- A prompt the user did not ask for needs a guardrail: dismissals, unsubscribes, uninstalls.

## 8. Output

```
FIRST VALUE   the moment, per user type, and whether it is a tested definition
TEARDOWN      the table, per platform
FUNNEL        per step, per platform: conversion, interval, median and p90 wait
WORST STEP    where the teardown and the funnel agree
SEEN          what replays or sessions showed at that step
CHANGES       ranked: the step, remove / defer / default / do-for-them / explain,
              the users it could affect, and how sure that estimate is
FIRST TEST    one change, with the metric and guardrail (experiment skill)
HAND OFF      the redesign brief for ui-ux-studio's flow playbook
```

Rank by users affected times a plausible change in conversion, and label each number measured, estimated or guess. An estimate presented as a forecast is how onboarding projects disappoint.

## Reference map

| File | Read it when |
|---|---|
| `references/teardown.md` | Doing the teardown - the step table, the friction log, what to try on each platform |
