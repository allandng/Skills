# Teardown: how a product is organized

Extract answers *what does it look like*. A teardown answers *how is it put together*: what kind of app this is, what stays on screen, which screens exist, how you move between them, and which states were designed. It is the structural half of a product's design DNA, and it is what `ui-ux-studio` needs before it adapts a product to another platform, adds a screen to it, or rebuilds its shell.

Describe with the vocabulary in `app-taxonomy.md`. The point of a shared vocabulary is that the teardown and the later design plan use the same words for the same things.

## Sources, best first

| Source | Gives | Limits |
|---|---|---|
| **The codebase** | Every route, every layout, which states have files | Not what it looks like rendered, and not which routes anyone uses |
| **The running product** | The real shell, real states, real density | Only the screens you can reach. Signed-in areas need the user's own session or their screenshots |
| **Mobbin, when connected** | Screens and whole flows of a named shipped product | Images only, a curated subset, `ios` or `web`, and possibly an older version |
| **Screenshots the user provides** | Exactly the screens they care about | No behavior, no states they did not capture |

Say which sources you used. A teardown built from six marketing screenshots is not a teardown of the product.

**From a codebase**, start with the route inventory. It finds the screens and, where the framework has file conventions for them, the loading, error and not-found states:

```bash
python3 scripts/route_inventory.py ./path/to/app
python3 scripts/route_inventory.py ./path/to/app --json > routes.json
```

It recognizes Next.js (app and pages routers), Expo Router, SvelteKit, Nuxt, Astro, and plain HTML. For anything else (React Router, SwiftUI, Jetpack Compose, Flutter) find the router or navigation graph by hand and build the same table.

**From a running product**, walk it in this order: sign in, land, do the core loop once, open one of each kind of object, search, open settings, then try to break it (empty search, a bad URL, a narrow window). Capture as you go.

**From Mobbin**, name the app in the query so results are restricted to it, and search screens and flows separately:

```
search_screens  platform=ios  "Duolingo home"
search_flows    platform=ios  "Duolingo onboarding"
```

Look at the images. Do not describe a screen from its metadata.

## The walk

1. **Classify.** Surface, app type, and the loop in one sentence (`app-taxonomy.md` §2 and §3). If you cannot state the loop, you have not used the product enough to tear it down.
2. **Shell.** What never moves. The navigation pattern at each width, and the content arrangement per screen family (§4).
3. **Levels.** Each level of "where am I" and the control that carries it. Note any control doing two levels' work.
4. **Screen inventory.** Every screen as `family:type`, with its route, its primary action, and how it is reached. Count templates, not pages: two hundred product pages are one screen.
5. **Flows.** The ones that exist, by purpose (§7), with step counts. Note which purposes have no flow at all. Recover and exit are the usual gaps.
6. **States.** For each screen family present, which required states exist, which are absent, and which are inconsistent between screens of the same family. This line is the one `ui-ux-studio` leans on hardest.
7. **Components.** By family, with the variant count for each. Flag accidental variants.
8. **Overlays.** Which overlay is used for which job. Inconsistency here (the same job in a modal on one screen and a drawer on another) is a finding.
9. **Density and input.** Rows per screen at the default size. Whether keyboard and touch are first-class or afterthoughts.
10. **Departures.** Where the product leaves its platform's conventions, and whether that reads as deliberate.

## Recording the result

Append to `profile.md`. Every line carries an evidence label (`evidence.md`).

```
## Structure

SURFACE     web app, desktop-first, breaks below 900            [observed]
APP TYPE    workflow/queue, borrows monitoring for the overview [inferred]
LOOP        open the queue, take the top item, resolve, next    [observed]
SHELL       persistent sidebar, list-detail split               [observed]
LEVELS      workspace: sidebar switcher · area: sidebar ·
            object: page header · view: tabs (also used for
            areas in Settings: two levels in one control)       [observed]
SCREENS     14 templates: 4 collection, 5 object, 2 input,
            1 orientation, 2 system. Table in routes.json       [measured]
FLOWS       sign up (3 steps), invite (2), resolve (1).
            No recover or exit flow found                       [observed]
STATES      collection: loading yes, first-run yes, no-results
            absent, error inherited from root only.
            object: not-found yes, permission-denied absent     [measured]
COMPONENTS  buttons 6 variants (2 accidental), inputs 3,
            tables 2                                            [observed]
OVERLAYS    create in a modal, edit in a drawer: inconsistent   [observed]
DENSITY     12 rows at 900 tall, no density setting             [measured]
GAPS        what a new screen would need that does not exist:
            no-results state, bulk actions, a mobile shell
```

`GAPS` is the handoff. It is the list of things the next designer will have to invent, written down so they invent them on purpose.

## What a teardown is not

It is not a copy. It records structure, conventions and gaps so that new work can fit a product or deliberately differ from it. A product's distinctive look and its specific content stay with the product.
