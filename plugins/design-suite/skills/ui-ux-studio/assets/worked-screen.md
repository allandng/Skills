# Worked example: the screen playbook, run end to end

One screen taken through `playbooks/screen.md`, with the real output of every rung. It shows the shape of the work and, more usefully, what each check caught. The numbers below are from an actual run, not illustrations.

This is an example of the *state and proof* procedure. The visual plan is deliberately thin. `worked-example.md` is the example for design plans.

## The screen

A small pottery studio tracks batches of work through the kiln.

```
SURFACE   web app, desktop-first, usable at 375
APP TYPE  system of record
LOOP      find a project, see what stage its pieces are at, leave
SHELL     persistent sidebar (3 areas), table, detail
SCREEN    Projects  -  collection:table
JOB       is the project I want here, and what stage is it at
ACTION    New project
```

## Step 3: the states owed

```bash
python3 scripts/state_coverage.py --template collection:table
```

Nine: loading, first-run, no-results, error, offline, permission-denied, single-item, dense, max-length.

## Step 4: one value, one status

```js
const states = {
  loading:             { status: "loading" },
  "first-run":         { status: "empty", reason: "first-run" },
  "no-results":        { status: "empty", reason: "no-results", query: "porcelain" },
  error:               { status: "error", message: "The studio server did not answer." },
  "permission-denied": { status: "denied", owner: "Mara Voss" },
  offline:             { status: "ready", items, stale: true },
  ready:               { status: "ready", items },
};
```

The view is one `switch (s.status)`. "Loading and error at once" cannot be written. The page reads `?state=<name>` so each state has a URL and can be captured.

## Step 5: the states that are not the happy path

| State | What it shows | Why |
|---|---|---|
| first-run | Shell stays. "No projects yet", one sentence on what a project is, one action | Looked up: 4 web products with an empty project list (Mobbin, Spellbook, Remote, incident.io, Plane). 4 of 4 keep the shell. 3 of 4 show one line and one create action |
| no-results | "No projects match "porcelain"", what search looks at, Clear search | Names the query and offers the way out. A different screen from first-run |
| error | What failed, "Nothing was lost", Try again | Says what happened and what to do |
| offline | The table, with a banner: "Showing projects as of 2:14 pm" | Says what still works and how old it is |
| permission-denied | Who owns the studio and a way to ask them | Never a blank page |
| max-length | A 190-character project name, and a record with no pieces and no firing | Wraps instead of truncating. "None yet" and "Not fired" instead of blanks |

## Steps 7 and 8: capture, look, record

```bash
for s in loading first-run no-results error offline permission-denied single-item dense max-length; do
  python3 scripts/capture.py index.html --query state=$s --name projects-$s --widths 375,1280
done
python3 scripts/capture.py index.html --name projects-ready --widths 375,1280
python3 scripts/capture.py index.html --name projects-ready --widths 375,1280 --dark
```

22 captures: nine states, the ready state, and ready in dark, each at 375 and 1280. Every file was written at the size asked for (measured: 375x900 and 1280x900), and every one was looked at.

**What looking found.** Two problems, both at 375, neither visible to any script:

1. **The navigation was about 190px tall.** The shell is a grid with `min-height: 100vh`. Collapsed to one column, its rows stretched, and the nav links stretched with them. Fix: `grid-template-rows: auto 1fr` and `align-items: start`.
2. **Stacked rows lost their meaning.** With the table header hidden on mobile, a row read "4 / Drying / Nov 3". Four of what? Fix: each stacked cell carries its column label ("Pieces: 4", "Last fired: Nov 3").

Both were fixed and the captures retaken before the manifest was filled in.

```
$ python3 scripts/state_coverage.py states.json
Projects  [collection:table]
  ok    loading            shots/projects-loading-375.png
  ok    first-run          shots/projects-first-run-375.png
  ok    no-results         index.html#No projects match
  ok    error              shots/projects-error-375.png
  ok    offline            index.html#Showing projects as of
  ok    permission-denied  shots/projects-permission-denied-375.png
  ok    single-item        shots/projects-single-item-375.png
  ok    dense              shots/projects-dense-375.png
  ok    max-length         shots/projects-max-length-375.png

1 screen(s), 9 state(s): 9 shown, 0 n/a, 0 missing
```

## Step 9: the ladder

| # | Rung | Result | Label |
|---|---|---|---|
| 1 | Rendered | 22 captures, each looked at. Two layout problems found and fixed (above) | observed |
| 2 | States | 9 of 9, exit 0 | measured |
| 3 | Content stress | 0, 1, 5 and 120 rows. A 190-character name wraps. Missing fields read "None yet" | observed |
| 4 | Keyboard | Not run. `capture.py` cannot press keys. Focus styles exist in the CSS | inferred |
| 5 | Contrast | **Failed first.** White on the mid clay was 4.13:1, on a 14px button label. Moved the button to the dark clay: 8.12:1. Then 8 pairs, 0 failing | measured |
| 6 | Craft and tells | Craft floor met: largest type 60px against 14px body, 4.29x. No mechanical tells | measured |
| 7 | Copy | Buttons name what happens ("New project", "Clear search", "Try again"). No invented counts | observed |
| 8 | Motion | The skeleton pulse sits inside `prefers-reduced-motion: no-preference` | inferred |
| 9 | Platform | `n/a: web only, no departures` | |
| 10 | Parity | `n/a: new screen, no baseline` | |

Two rungs are inferred, and the reply said so. That is the honest state of this screen: its keyboard path has not been walked.

## What this run teaches

- **The scripts passed while the screen was broken.** State coverage was 9 of 9 before either layout problem was fixed. Coverage proves a state exists. Only looking proves it is right.
- **The contrast failure was on the most important control.** The primary button. It passed for large text and failed for the size it was used at, which is the failure `contrast.py` words as "large-text-only".
- **Real content found what placeholder content hides.** The missing labels only showed with real rows on a narrow screen.
