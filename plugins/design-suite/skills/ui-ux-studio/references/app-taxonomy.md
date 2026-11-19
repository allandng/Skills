# App taxonomy

A vocabulary for the product surface: the part of an application a signed-in person works in. `archetypes.md` answers *what kind of thing is this* for a whole site. This file takes over when that answer is **Program or app UI**, **Internal tool**, **Single-purpose utility**, or the logged-in half of a **Course**, and names the parts precisely enough that two people mean the same screen.

It exists because "build a dashboard" is not a specification. A dashboard for a monitoring tool and a home screen for a habit tracker share a name and nothing else. Classify first, on six layers, then design.

This file is identical in `ui-ux-studio` and `design-dna`. One uses it to plan, the other to describe what already exists. The other files it names (`archetypes.md`, `platforms.md`, `states.md`, `modes.md`, `flows.md`, `ai-tells.md`) and `scripts/state_coverage.py` live in `ui-ux-studio`.

## Contents

1. [The classification line](#1-the-classification-line)
2. [Layer 1: surface](#2-layer-1-surface)
3. [Layer 2: app type](#3-layer-2-app-type)
4. [Layer 3: shell](#4-layer-3-shell)
5. [Layer 4: screen types](#5-layer-4-screen-types)
6. [Layer 5: regions and overlays](#6-layer-5-regions-and-overlays)
7. [Layer 6: states and flows](#7-layer-6-states-and-flows)
8. [Looking a pattern up](#8-looking-a-pattern-up)

## 1. The classification line

Write this before any layout. Every later file refers back to it.

```
SURFACE   web app, desktop-first, usable at 375
APP TYPE  workflow/queue (borrows monitoring for the overview)
LOOP      open the queue, take the top item, resolve or hand off, next
SHELL     collapsible sidebar, list-detail split, command palette
SCREENS   inbox (collection:list) · ticket (object:conversation)
          · customer (object:detail) · macros (system:settings)
FLOWS     first-run import · assign and resolve · escalate
STATES    states.json, checked by scripts/state_coverage.py
```

`LOOP` is the line that earns its place. It is the thing the user does a hundred times, in one sentence. A shell that puts anything in front of the loop is wrong however good it looks.

## 2. Layer 1: surface

Where it runs decides what input exists, what the system already provides, and what the user expects without being told. `platforms.md` has the conventions for each.

| Surface | Input | What it changes |
|---|---|---|
| Web app | Pointer, keyboard, sometimes touch | URLs are state. Hover exists. The window resizes continuously. |
| Mobile, iOS or Android | Touch, one hand, interrupted | No hover. System back and gestures. Small targets fail. Sessions are short. |
| Tablet and foldable | Touch, sometimes keyboard and pointer | Two panes become possible. Layout changes with posture and window size. |
| Desktop native | Pointer, keyboard, menus | Multiple windows. A menu bar. Shortcuts are expected. Density is welcome. |
| Embedded and ambient | Varies | Extension popup, widget, watch, TV, terminal, voice. One job, a few seconds, almost no chrome. |

State the primary surface and the smallest one you must still work on. "Web app, desktop-first, usable at 375" is a decision. "Responsive" is not.

## 3. Layer 2: app type

Classify by the job the user returns for, not by industry. A bank and a pharmacy can be the same type. Most products are one primary type that borrows a second.

| Type | Core loop | Default shell | Screens that carry it | States that dominate | Density |
|---|---|---|---|---|---|
| **System of record** (CRM, admin, inventory) | Find a record, read or change it, leave | Sidebar, table, detail | table, detail, form | dense, permission-denied, stale | High |
| **Workflow / queue** (support desk, review, triage) | Take the next item, disposition it, next | List-detail split or single-item focus | inbox, conversation, quick-action bar | empty-cleared, blocked, assigned-elsewhere | High |
| **Creation tool** (editor, canvas, IDE, builder) | Open a document, make, save or export | Canvas with panels and palettes | canvas or editor, file browser, export | unsaved, conflict, offline, autosaving | Chrome low, content high |
| **Monitoring** (analytics, ops, health) | Glance, spot the anomaly, drill in | Dashboard-first | overview, chart detail, alert list | loading-partial, no-data-yet, stale, degraded | Medium to high |
| **Communication** (messaging, community) | Read what's new, reply, move on | Conversation list plus thread | thread, composer, people | unread, sending, failed-to-send, offline | Medium |
| **Consumption** (reader, player, feed) | Pick something, take it in, pick the next | Feed or library, then an immersive viewer | feed, viewer or player, library | buffering, end-of-feed, offline-saved | Low |
| **Transaction** (shop, booking, banking, marketplace) | Find, decide, pay, confirm | Browse, detail, cart or review, receipt | results, detail, review, receipt | out-of-stock, price-changed, payment-failed, pending | Medium |
| **Utility** (converter, calculator, scanner) | Give input, get output, leave | One screen | the tool, result | processing, bad-input, too-large | Low |
| **Learning / habit** (course, tracker, practice) | Do today's unit, see progress, return tomorrow | Path or today view | today, lesson or session, progress | streak-at-risk, completed-today, locked, resumed | Low to medium |
| **Spatial** (map, floor plan, scheduling grid) | Orient, find a place or slot, act on it | Map or grid with a sheet or side panel | map, place detail, route | locating, no-signal, out-of-bounds | Chrome low |
| **Conversational / agentic** (assistant, copilot) | Ask, read or watch the work, refine, keep the result | Thread plus an artifact or side panel | thread, artifact, history | streaming, tool-running, needs-approval, interrupted, failed-partway | Medium |
| **Game / play** | Play a round, see the result, again | Full-screen play with a hub between | play, results, hub or shop | paused, reconnecting, out-of-energy | Varies |

Two checks before moving on.

- **The cosplay check.** Does the plan give the product a shell from a different type? A utility with a sidebar and a dashboard is the usual offender. A queue dressed as a system of record makes people hunt for their next item.
- **The borrow, stated.** When the product borrows a second type, say which screens belong to it. "Workflow/queue, borrows monitoring for the overview" tells the reader the overview is one screen, not the product.

## 4. Layer 3: shell

The shell is what stays put while the content changes. `modes.md` (spec-to-ui, Step 3) lists eight interaction models. Pick one there. This layer is the chrome that carries it.

**Levels.** Count how many levels of "where am I" the product has, then give each one exactly one home.

| Level | Example | Usual home |
|---|---|---|
| Account or workspace | Which organization | Switcher at the top of the sidebar or in the header |
| Area | Projects, Inbox, Reports | Primary navigation |
| Object | This project | Page header, breadcrumb |
| View of the object | Board, list, timeline | Tabs or a view switcher in the page header |
| Selection | This card | Side panel, detail pane, or a pushed screen |

Two levels in one control is the most common shell bug: tabs that are sometimes areas and sometimes views of an object.

**Primary navigation patterns.**

| Pattern | Use when | Breaks when |
|---|---|---|
| Persistent sidebar | 5 to 15 areas, desktop width, users move between areas all day | The content needs the width, or the product has three areas |
| Collapsible sidebar or rail | Same, but content is wide: tables, canvases | Icons alone are ambiguous and labels are hidden by default |
| Top navigation | 3 to 6 areas, content benefits from full width | Areas multiply, or there is a second level |
| Bottom tab bar | Mobile, 3 to 5 peer areas the user switches between often | More than 5, or the tabs are steps instead of peers |
| Drawer | Mobile, many areas with one dominant one | It hides the only way to reach daily destinations |
| Hub and spoke | Few areas, each a self-contained task: utilities, kiosks, TV | Users hop between spokes and must return to the hub each time |
| Single surface with palettes | Creation tools and maps: the content is the navigation | The product actually has several kinds of object |
| Command palette | An addition to any of the above for frequent, keyboard-first users | It is the only way to reach something |

**Arrangement of content inside the shell.** Stack (push and pop, mobile default), list-detail split (two panes, desktop and tablet default for collections), three-pane (areas, list, detail: mail-shaped products), canvas with inspector, and feed. A product usually has one arrangement per screen type and should not invent a second for the same type.

**Depth rule.** Anything the loop touches is reachable in one action from where the loop starts. Settings can be three levels deep. The next item in the queue cannot.

## 5. Layer 4: screen types

Seven families. The family decides which states are mandatory (`states.md`) and what the screen's ten-second job is. Name each screen as `family:type`.

| Family | Types | Ten-second job |
|---|---|---|
| **entry** | launch, sign in, sign up, verify, reset, onboarding step, permission priming, paywall or upgrade | What is this asking of me, and can I leave |
| **orientation** | home, dashboard, hub, feed, search results, notifications, activity | What needs me, and where do I go next |
| **collection** | list, table, grid or gallery, board, calendar, timeline, map, tree | Is the thing I want here, and how do I get to it |
| **object** | detail, profile, editor or composer, canvas, viewer or player, conversation | What is this, what state is it in, what can I do to it |
| **input** | form, wizard step, picker, filter and sort, import or upload, review and confirm | What do I need to give, and what happens when I submit |
| **outcome** | success or receipt, error, not found, offline, empty | What happened, and what now |
| **system** | settings, account, billing, team and permissions, help, legal | Where is the one thing I came to change |

Rules that follow from the families.

- **One primary action per screen.** If two actions look equally important, the screen has not decided what it is for.
- **A collection always has a way in and a way to narrow.** Opening an item, and search, filter or sort once it can exceed one screenful.
- **An object screen shows its status before its fields.** Draft, paid, archived, failed: the status changes what every other element means.
- **Orientation screens earn their widgets.** Every tile answers "what needs me" or links to the loop. A number nobody acts on is decoration (`archetypes.md`, cosplay traps).
- **Outcome screens are never dead ends.** Each names what happened and offers the next action.
- **System screens are searched, not browsed.** Group by what the user is trying to change, label with the user's words, and make the page findable from the thing it configures.

## 6. Layer 5: regions and overlays

**Regions of a screen**, outside in: global chrome (primary navigation, workspace switcher, global search or command, account), page header (title, breadcrumb, status, primary action, view switcher), toolbar (filter, sort, bulk actions, density), content, secondary panel (inspector, detail, activity), and status (sync, connection, progress).

Bulk actions replace the toolbar when a selection exists. They do not appear next to it.

**Component families**, for inventories: navigation, action, input, selection, data display, feedback, container, overlay. An inventory lists each family, the components in it, and the variants of each. Three button variants is a system. Nine is drift.

**Choosing an overlay.** Reach for the least interrupting one that can hold the content.

| Overlay | For | Never for |
|---|---|---|
| Inline change | Edits that take one field | Anything needing confirmation |
| Tooltip | A label for an icon, a shortcut hint | Content the user must read, or anything on touch |
| Popover or menu | A short list of choices tied to a control | Forms longer than three fields |
| Toast or snackbar | Confirmation of something already done, with undo | Errors that need action, or the only record of an event |
| Banner | A condition that persists: offline, trial ending, read-only | One-time confirmations |
| Side panel or drawer | Detail or editing while the list stays visible | Flows the user must finish before continuing |
| Sheet (mobile) | A scoped task or choice, dismissible | Deep navigation |
| Modal dialog | A decision that blocks: destructive confirmation, a required choice | Reading, browsing, or anything with its own navigation |
| Full screen | A focused multi-step task | A yes or no question |

A modal opened from a modal means the flow should have been a screen.

## 7. Layer 6: states and flows

**States** come in five groups. `states.md` has the per-family requirements, the state model, and the manifest the coverage script checks.

| Group | States |
|---|---|
| Data | loading (first, refresh, more), empty (first-run, no-results, cleared), partial, error, offline, stale, not-found |
| Access | permission-denied, read-only, over-limit, locked or upgrade-required |
| Content extremes | single-item, dense (100+), max-length, missing-fields |
| Interaction | rest, hover, focus, pressed, selected, disabled, dragging, busy |
| Flow | pristine, invalid, submitting, submit-error, success, unsaved-exit, resumed, blocked |

The three empties are different screens. **First-run** teaches and offers the first action. **No-results** names the filter and offers to clear it. **Cleared** means the user finished, and usually offers nothing.

**Flows** by purpose. `flows.md` governs how each is built.

| Purpose | Flows |
|---|---|
| Acquire | sign up, accept invite, verify |
| Activate | onboarding, import, first object created |
| Core loop | create, edit, find, share, complete |
| Commerce | trial, paywall, checkout, receipt, cancel or refund |
| Collaborate | invite, share, set permissions, comment, hand off |
| Recover | reset password, undo, restore, retry after failure |
| Exit | export, downgrade, delete account |

Recover and exit are the two purposes that get skipped. Both are where trust is decided.

## 8. Looking a pattern up

The taxonomy gives you the words. Shipped products give you the evidence. This is research, never derivation (`ai-tells.md` §10b): take the convention, the step count, the state. Leave the look.

**With the Mobbin connector** (check the tool list; proceed without comment when absent). Its search takes one screen or one journey per query, phrased as app kind plus screen type, with a state only when the state is the question. `platform` is `ios` or `web`. For Android or desktop-native conventions, read the platform's own guidelines instead (`platforms.md`).

```
search_screens  platform=web  "project management app empty state for a list with no items"
search_screens  platform=ios  "banking app transaction detail"
search_flows    platform=ios  "language learning app onboarding"
search_flows    platform=web  "team invite"
```

Name a specific app in the query to restrict results to it. Look at the returned images. Do not summarize from metadata.

**What to carry away**, in this form:

```
QUESTION    What does a first-run empty collection show?
LOOKED AT   4 web products (project management), <date>
FOUND       4 of 4 keep the full shell. 3 of 4: one sentence and one create
            action. 1 of 4 is a cleared state, not first-run, and offers none.
CONVENTION  shell stays, one line, one action: keep
HERD        illustration above the line: 2 of 4, no comprehension cost, free
            to drop
```

Counts, not impressions. "Most apps do X" is a guess until it is "6 of 8".

**Without the connector**, the same questions go to web search for teardowns and the platform guidelines, or to `design-dna`'s teardown of two or three named products. The output format does not change.

**When not to look.** Palette, type, form language and signature are Phase 1 and come from the subject. Do not open a pattern library to decide them.
