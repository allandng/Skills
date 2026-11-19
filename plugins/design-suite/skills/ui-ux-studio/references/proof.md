# Proof

Done means shown. A design is finished when someone has looked at the real thing, at the real sizes, in each of its states, and the result is in the reply. Everything short of that is a claim about code.

This is Phase 2 of "commit, then verify". It runs after building, never before the plan, and it does not replace conviction. A flagged risk taken on purpose, stated with its reason, is a decision and may stay.

## The ladder

Work up it. Stop only when a rung genuinely does not apply, and write `n/a: <reason>` for that rung instead of dropping it.

| # | Rung | How | Passes when |
|---|---|---|---|
| 1 | **Rendered** | Open the built page or app with whatever can render it here: a browser tool, a preview, a simulator, a screenshot script. Capture 375, 768 and 1280 wide, plus dark if a dark theme exists | You looked at each capture and it matches the plan's wireframe and hierarchy |
| 2 | **States** | `python3 scripts/state_coverage.py states.json` (`states.md`) | Exit 0, and every `n/a` has a reason you would defend |
| 3 | **Content stress** | Zero items, one, a hundred. The 200-character name. The record with missing fields | Nothing overflows, truncates without a way to read it, or collapses |
| 4 | **Keyboard** | Tab through each screen. Write the order down | Order follows reading order, focus is always visible, every action is reachable, overlays trap and return focus |
| 5 | **Contrast** | `python3 scripts/contrast.py --tokens tokens.json`, with the real `pairs` declared | Every pair that actually co-occurs passes |
| 6 | **Craft and tells** | `python3 scripts/craft_check.py <files>` and `python3 scripts/ai_tells.py <files>` | Craft floor met. Each surviving tell is removed or justified out loud |
| 7 | **Copy** | Every string through `copy-gate.md` | Nothing invented, no borrowed weight, buttons name what happens |
| 8 | **Motion** | With reduced motion on | Nothing essential is conveyed only by animation |
| 9 | **Platform** | The `DEPARTURES` line from `platforms.md` | Each departure has a reason. Back, system gestures and targets behave as the platform expects |
| 10 | **Parity** (update and visual-parity work only) | Side-by-side or image diff against the baseline | Differences are the intended ones, listed |

**If nothing here can render the work**, say so in the first line of the reply: "Not rendered: no browser or preview available in this session." Then give the one command or step that renders it. Do not describe how it looks. Inconclusive is not a pass, and a check on the wrong surface (a desktop capture for a mobile design) is not a check.

## Labels

Every claim in the reply about how the design behaves carries one:

| Label | Means | Example |
|---|---|---|
| **measured** | A script or tool produced it, and the output is shown or linked | "Body text on surface is 11.2:1 (measured, contrast.py)" |
| **observed** | You looked at a rendering | "At 375 the table becomes two-line rows (observed, screenshot 3)" |
| **inferred** | Reasoned from code or structure without rendering | "The sheet should trap focus: it uses the dialog element (inferred)" |
| **guess** | None of the above | "Probably fine on Android (guess: not run)" |

A reply made of inferred and guess lines has not been verified, whatever its tone. The fix is to climb the ladder, not to reword.

## The reply

Each playbook ends with its own **Reply** line. All of them share this frame:

```
GOAL        one sentence: what was asked, restated
BUILT       what exists now, and where
DECISIONS   the choices that mattered, each with its reason and the principle
            that drove it
PROOF       the ladder: rung, result, label. n/a rungs listed with reasons
OPEN        what is waiting on the user, each decidable from this reply alone
NOT DONE    anything skipped, with why
```

Lead with what changed for the user. Do not list checks that passed as if they were features: "responsive, accessible, keyboard-friendly" is the floor, and narrating it reads as padding.

## Decision log

For long or unattended work, and whenever the user asks for a trail, append one line per decision to `design-decisions.tsv` next to the work:

```
ts	phase	decision	why	evidence	result
2026-03-02T14:10Z	plan	list-detail split, not a table	loop is triage, one item at a time	app-taxonomy §3, 5 of 6 peers	kept
2026-03-02T15:40Z	verify	dropped the sidebar illustration	Chanel test; nothing lost at 375	screenshot 2 vs 4	kept
```

Log choices between real alternatives, reversals, and anything a reviewer might ask "why" about. Do not log every keystroke. A decision reversed later gets a new line that points at the old one. It is never edited away.

## When a check fails

Suspect the observation before the design: the wrong file, a stale build, a capture at the wrong width. Then trace the failure to the plan line that caused it (`principles.md`, "Fix the plan, not the CSS"). Then rerun the whole rung, not just the case that failed.
