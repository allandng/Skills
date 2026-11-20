# The teardown

How to walk an onboarding as a new user and write down what it costs.

## Before you start

- A fresh account, a fresh browser profile or a freshly installed app, and a real device for mobile. A simulator has no slow network and no thumb.
- Decide which user you are: the organizer, the attendee, the invited teammate. Each has a different path. Do one at a time.
- Start a timer at the first screen. Do not stop it for anything: waiting for a verification email is part of the experience.
- Do not skip what a real user could not skip.

## The step table

One row per screen or interruption, including emails, system prompts and store sheets.

| # | Step | Asks for | Fields | Decisions | Seconds | Class | If removed |
|---|---|---|---|---|---|---|---|
| 1 | Landing | Tap "Get started" | 0 | 1 | 4 | Required | - |
| 2 | Sign up | Email, password, name | 3 | 0 | 38 | Required | Could be one tap with a platform account |
| 3 | Verify email | Leave, find email, tap, return | 0 | 0 | 71 | Neither | Could come after first value |
| 4 | "Tell us about you" | Role, team size, how you heard | 3 | 3 | 22 | Neither | Product works without it |
| 5 | Notification prompt | Allow or deny | 0 | 1 | 3 | Neither | Could be asked when there is something to notify |
| 6 | Empty dashboard | Find where to start | 0 | 1 | 15 | Neither | A template or sample would remove it |
| 7 | Create first event | Title, date, venue | 3 | 1 | 64 | Required | - |
| 8 | Event page live | - | 0 | 0 | - | **Value** | - |

**Class** is value, required, or neither. **If removed** is the honest answer to "what breaks without this step".

Totals to report, per platform: steps, fields, decisions, context switches, and seconds to first value.

## The friction log

Alongside the table, write down every moment you hesitated, in the order it happened. These are the findings the table cannot hold.

```
0:42  Step 2  Password rule appeared only after I submitted
1:10  Step 3  Verification email took 40 seconds. No way to continue meanwhile
2:35  Step 6  Three buttons of equal weight. Did not know which starts an event
3:02  Step 7  Venue field wants an exact match. My venue is not in the list. No way to add one
```

Note what you expected, what happened, and whether you could recover without help.

## Things to try on purpose

A real user does not follow the path. Try each and record what happens.

- **Leave and come back.** Close the tab or background the app at each step. Return an hour later. Are you where you left off, at the start, or somewhere confusing?
- **Refuse.** Deny every permission. Skip every optional step. Is the product still usable?
- **Get it wrong.** A bad email, a mismatched password, an expired code. Does the message say what happened and what to do?
- **Go back.** Use the browser's or system's back at every step. Is anything lost?
- **Use the other door.** Arrive by an invite link, a shared link, a push notification, a search result. Does onboarding still make sense, and do you land where the link promised?
- **Switch device.** Start on web, continue on the app, and the reverse. Are you recognized?
- **Be slow.** Throttle the network. What do you see while waiting?
- **Be the second user.** Join an existing workspace instead of creating one. This path is usually the least designed.

## On mobile, also record

- Steps before the first screen of the app: store page, install size, launch time.
- Every system prompt, when it appeared, and whether the app said why first.
- Which keyboard each field showed, and whether autofill and paste worked.
- What happens with one hand: is the primary action reachable with a thumb?
- What a push notification or deep link opens.

## On web, also record

- What loads first, and how long before anything can be clicked.
- Whether the URL changes at each step, so a refresh or a shared link keeps your place.
- Tab order through each form, and where focus lands on each new screen.
- What it looks like at the width of a phone browser, where many sign-ups begin.

## Turning it into findings

For each row classed "neither", and each friction-log line, write:

```
STEP       3, verify email, before any value
COST       71 seconds median here, one context switch
EVIDENCE   observed in teardown. Funnel: 18% lost at this step on web (measured, n=2,140)
CHANGE     defer: let the user create an event first, verify before publishing
AFFECTS    every new sign-up
RISK       unverified accounts creating content. Guardrail: spam reports
```

The teardown says what the step costs. The funnel says how many pay that cost and leave. A finding needs both.
