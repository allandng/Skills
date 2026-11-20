# Event edge cases

Walk this list for every new event. For each case, write what the event does: fires, does not fire, fires with which properties. "Not considered" is how a metric ends up wrong.

The cases are grouped by what goes wrong. Each has the check that catches it.

## 1. It fires when it should not

| Case | What happens | What to do |
|---|---|---|
| **Fired on intent, not success** | The event is sent on tap. The server rejects the action. The count includes things that never happened | Fire on confirmed success, from the server. With optimistic updates this matters most: the interface shows success before it is true |
| **Double fire** | A re-render, a handler bound twice, a retry, or both client and server sending | Send from one place. Give retried requests an idempotency key and send the event once per key. `event_qa.py` reports repeats within two seconds |
| **Refire on back or refresh** | Returning to a confirmation page sends the purchase event again | Fire on the state change, not on the page view |
| **Fired for the wrong person** | The previous user's identity is still set after logout | Reset identity on logout. Test by logging out and in as someone else on one device |
| **Tests, staff and bots** | Internal use and automated traffic counted as users | Mark internal accounts with a property, exclude them in every query, and keep test environments out of the production project |

## 2. It does not fire when it should

| Case | What happens | What to do |
|---|---|---|
| **Blocked or dropped on the client** | Ad blockers, privacy browsers, a tab closed before the request left | Critical events from the server |
| **Failure paths untracked** | Only success is tracked, so the funnel shows a drop with no reason | Track the failure with its reason: `payment_failed` with an error code enum |
| **Empty and error states untracked** | Nobody knows how often users see them | An event when an empty or error state is shown, where that state is a funnel step |
| **Offline** | The mobile app queues events. The app is killed before they send, or they arrive days later | Know the SDK's queue behaviour. Treat the last 48 hours as incomplete |
| **Missing on one platform** | Implemented on web, forgotten on Android | `event_qa.py` reports events that never fire on a platform |
| **Old app versions** | A version from four months ago does not send the new event, and never will | Put `app_version` on every event, and read new events only from versions that have them |

## 3. It fires, but means something different

| Case | What happens | What to do |
|---|---|---|
| **Same name, different trigger per platform** | `checkout_started` fires on page load on web and on button tap on iOS | One trigger definition in the plan, implemented identically. Review the implementations side by side |
| **Same name, different properties** | iOS sends `price` in cents, web in dollars | Types and units in the plan. Units in the property name when ambiguous: `price_cents` |
| **Redefined in place** | The trigger changed in March. Charts across March are comparing two things | New event name. Record the date |
| **Autocaptured stand-in** | A chart built on a click on a button whose label later changed | Explicit events for anything a metric depends on |
| **One action, two events** | The client sends `order_placed` and the server sends `order_created` for the same thing | One event. The linter flags near-duplicate names |

## 4. It is attached to the wrong user, or to two

| Case | What happens | What to do |
|---|---|---|
| **Anonymous then identified** | Activity before sign-up is on an anonymous ID | Identify at sign-up and login so the two are linked. Count people, not IDs |
| **Server and client disagree** | The server event uses the database ID, the client an anonymous one | Pass the client's ID to the server, or identify before the server event |
| **Web to app handoff** | Signs up on web, opens the app: two people | Pass the ID through the transition |
| **Several devices** | One person, several anonymous IDs until each logs in | Expected. It is why pre-login funnels overcount people |
| **Shared device** | Two people, one identity | Reset on logout |
| **Reinstall** | A new anonymous person on the same phone | Expected. Install counts are not people counts |
| **Account-level actions** | A workspace upgrades. Which user gets the event? | Group analytics: attach the account to the event |

`event_qa.py --requires later:earlier` finds users with a later step and no earlier one, which is how identity breaks show up in data.

## 5. Time is wrong

| Case | What happens | What to do |
|---|---|---|
| **Device clock** | Events stamped next year, or in 1970 | Order and window by server receive time |
| **Late arrival** | Offline events land after the dashboard was read | Re-read recent periods before quoting them |
| **Timezones** | "Daily" means a different day for the server and the user | Store in UTC. Choose one reporting timezone and state it |
| **Out of order** | A batch delivers step 3 before step 2 | Order by event time within a user, with receive time as a sanity bound |
| **Long gaps** | A user starts checkout Monday and finishes Friday | Decide the funnel window deliberately, and state it |

## 6. It carries something it should not

| Case | What happens | What to do |
|---|---|---|
| **Personal data in properties** | An email in `user_email`, a name in a free-text field | IDs only. The linter flags property names that look personal |
| **Personal data in URLs** | A reset token or an email in a query string, captured with the page view | Strip query strings, or allow-list parameters |
| **Free text** | A search query or a note the user typed | Do not send it. Send its length, or a category |
| **Replays** | A card number or a password field recorded | Mask inputs by default. Check a recording before sharing |
| **No consent** | Tracking before the user agreed, where agreement is required | Gate capture on consent, and accept the gap in the data |

## Web against mobile, in one table

| | Web | Mobile app |
|---|---|---|
| Lost events | Blockers, closed tabs | Offline, app killed before the queue sends |
| Arrival | Immediate | Sometimes late and batched |
| Fix reaches users | Next page load | Next release, for those who update |
| Versions live | One | Many |
| Session | Tab until idle | Foreground time |
| Pre-login identity | Per browser | Per install |
| Extra funnel steps | None | Install, permission prompts, store purchase sheet |

For each event, the QA is done once per platform, and the two implementations are read side by side.

## What to write for each event

```
EVENT       ticket_purchased
FIRES       server, after payment is confirmed and the order is committed
ONCE PER    order id (idempotent on retry)
ON FAILURE  payment_failed, with reason
OFFLINE     n/a: server-side
LOGOUT      n/a: server-side, uses the order's owner
PLATFORM    passed from the client with the order request
OLD APPS    versions before 4.2 use the old checkout and send the same event
CHECKED     web, iOS, Android: triggered, failed, retried. Arrived once each
```
