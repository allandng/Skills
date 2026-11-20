# Web and mobile

The same product on web and mobile is two products for measurement purposes. They differ in how events are sent, how fast a fix reaches users, how people use them, and what "a session" means. A blended number hides all of it.

The rule: **segment by platform first, then decide whether it is safe to combine.**

## What differs

| | Web | Mobile app |
|---|---|---|
| **A fix reaches users** | On the next page load | Days to weeks, and never for users who do not update |
| **Versions in the wild** | One | Many at once. Old versions keep sending old events |
| **Events get lost to** | Ad blockers, closed tabs, blocked scripts | Offline use, the app being killed before the queue flushes |
| **Events arrive** | Immediately | Sometimes hours late, in a batch, when the device reconnects |
| **Device clock** | Usually right | Often wrong |
| **A session is** | A tab, until idle | Foreground time. Backgrounding splits it |
| **Identity before login** | A cookie, per browser | Per install. Reinstall makes a new anonymous person |
| **Entry points** | URL, search, link | Icon, push notification, deep link, app store |
| **Input** | Pointer and keyboard, long sessions | Touch, one hand, interrupted, short sessions |
| **Permission prompts** | Rare | Notifications, location, camera, tracking. Each is a funnel step |
| **Payments** | Your checkout | Often the store's, with its own failure modes |

## Rules that follow

**For tracking**

- **Put the user's platform on every event,** as your own property (`web`, `ios`, `android`), including events sent from the server. A server-side event carries the server's library, not the user's device, so without this the most important events cannot be segmented by platform. `event_qa.py` reports blank platforms.
- **Put the app version on every mobile event.** Without it a tracking fix cannot be told apart from a behaviour change.
- **Parity is checked, not assumed.** The same action fires the same event name with the same properties on each platform. `event_qa.py` finds events that fire on one platform and never on another.
- **Order by server receive time, analyse by event time, and know the difference.** Late batches from offline devices land after dashboards were read. Re-read anything from the last 48 hours before quoting it.
- **Carry identity across the handoff.** A user who signs up on web and opens the app, or follows an email link from phone to desktop, must end up as one person. Pass the ID through the transition instead of letting each side mint its own.

**For reading numbers**

- **A change on mobile takes a release cycle to show.** Read mobile results by app version, and wait for adoption before calling an effect. An experiment that ships in a new version only reaches the users who updated, who are not a random sample.
- **Compare like with like.** Mobile sign-ups and web sign-ups often come from different sources with different intent. A retention gap between platforms is first a mix question (`metric-check`).
- **Funnels have different steps.** Mobile adds install, permission prompts and sometimes a store purchase sheet. A "shared" funnel that omits them hides where mobile users go.
- **Rhythm differs.** Many products are set up on web and checked on mobile. Low mobile depth can be the product working.

**For the experience**

- **Design the loop for the platform,** not the layout. What does the core action look like with a thumb, on a train? `ui-ux-studio`'s platform-adapt playbook does the translation.
- **Budget for the network.** Mobile users are on worse connections. Offline and stale are common states there, not edge cases.
- **Ask for permissions at the moment of need,** after explaining why. A prompt on first launch is a funnel step that many users fail.
- **Deep links are part of the feature.** A push notification or email that opens the home screen instead of the thing it mentioned has lost the user.

## What to state in any cross-platform finding

```
PLATFORMS   which were included, and each one's n
VERSIONS    for mobile: which app versions, and their share
SPLIT       the number for each platform, before the combined one
PARITY      whether the events involved fire identically on each
LAG         for mobile: how long since the relevant release, and its adoption
```
