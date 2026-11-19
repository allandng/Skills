---
name: design-dna
description: Reverse-engineer the design of any website or app into something reusable, and research how a whole category designs itself. Extracts palette, typography, spacing, radii, elevation, motion, and layout from a live URL, saved files, or a codebase into a tokens.json plus a written style profile, names the style from an open taxonomy, and flags AI tells. Tears down how a product is organized (app type, navigation shell, screens, flows, state coverage). Surveys competitors and adjacent categories to separate convention from herd behavior. Use this whenever the user points at a website or app and wants to know how it is designed or structured, wants to match, extend, or diverge from an existing style, asks what competitors look like or how they handle a screen or flow, or needs design tokens or a screen inventory pulled out of a codebase. Feeds ui-ux-studio directly - use it before that skill's remix, update, platform-adapt, design-system, or create playbooks whenever a real reference exists.
---

# Design DNA

Turn real websites and apps into design systems you can reuse.

Three jobs. **Extract** pulls a single site apart into tokens and a written profile. **Teardown** describes how a product is organized: what kind of app it is, its shell, its screens, its flows, and which states were designed. **Survey** runs either across a category so you can tell what is convention, what is herd behavior, and what is actually distinctive. Extraction alone tells you what a site does, and only the comparison tells you whether that means anything.

An extraction is a set of claims about someone else's design. Every one is labeled measured, observed, inferred, or guess (`references/evidence.md`), because the unlabeled guesses are where the next person goes wrong.

This exists because style databases go stale and the good ones charge for the interesting categories. Deriving a style from six real sites you picked is more current than any snapshot, and it is specific to the competitive set that actually matters.

## Route

| Ask | Do |
|---|---|
| "how is this site designed", "pull the tokens out of this", "what style is this" | **Extract** |
| "what do sites like this look like", "how do competitors design", "what's the convention here" | **Survey** (extract runs inside it) |
| "match this style", "add to this site" | **Extract**, then hand off to `ui-ux-studio` **update** mode |
| "redesign this", "give me options" | **Survey**, then hand off to `ui-ux-studio` **remix** mode |
| "how is this app structured", "what screens does it have", "how does X handle onboarding" | **Teardown** |
| "bring this to mobile", "port this to desktop" | **Teardown**, then hand off to `ui-ux-studio` **platform-adapt** |
| "pull the tokens out of this repo", "clean up our design system" | **Extract** from the codebase, then hand off to `ui-ux-studio` **design-system** |
| "what changed in the redesign", "how do we differ from X" | **Compare** |

Each job has a step list in `playbooks/`: `extract-site`, `extract-codebase`, `survey`, `teardown`, `compare`, and `handoff`. Open the one that matches, copy its steps into your todo list as written, and work them in order. A step that does not apply keeps its line with `n/a: <reason>`. The sections below hold the detail the steps point to.

---

## Extract

### 1. Get the source

```bash
python3 scripts/extract_style.py --url https://example.com --out ./dna/example
```

`--url` needs network access from wherever the script runs. When the sandbox has no egress — common — fetch the page with your own web tooling, save the HTML and any stylesheets to a folder, and use `--dir`:

```bash
python3 scripts/extract_style.py --dir ./saved --name "Example" --out ./dna/example
```

For a codebase rather than a live site, point `--dir` at the source tree. The script reads `.html`, `.css`, `.scss`, `.jsx`, `.tsx`, `.vue`, and `.svelte`, and skips `node_modules`.

Three files come out: `tokens.json` (feeds `ui-ux-studio`'s `contrast.py` unchanged), `profile.md` (the written breakdown), and `raw.json` (everything extracted, for when you need a value the profile omits). A fourth, `tokens-dark.json`, appears when the site has a dark theme.

**Themes are separated.** `@media (prefers-color-scheme: dark)` blocks and `.dark` / `[data-theme="dark"]` selectors are split out and measured on their own. Without that, a site with a theme toggle reports whichever block parsed last as its palette — so a light-default site with dark support comes back dark. Both themes are real systems; check contrast on each.

### 2. Read what it found

The script reports declared CSS custom properties separately from inferred roles, and that distinction matters. **If the site exposes `--primary`, `--surface`, and friends, that is the real system and the inferred roles are noise** — the author already told you the answer. Inference only earns its place when there is no token layer.

Watch for these in the output:

- **Dead tokens** — declared but never used. Common, and a sign the system has drifted.
- **Shadow count above four** — elevation with no system.
- **More than four font weights** — weight soup.
- **`untinted` neutral temperature** — a gray ramp straight from the framework.
- **Flagged AI tells** — the script cross-checks against `ui-ux-studio`'s tell catalogue.

### 3. Do the manual pass

Non-optional. The script reads declarations; it cannot see states, hierarchy, imagery, voice, or intent. `references/extraction.md` has the walk — nine steps, and the last one produces the `GAPS` list that `update` mode depends on.

### 4. Name the style

Match the extracted axes against `references/style-taxonomy.md`, which defines each family by its mechanics rather than its vibe. The signal-to-style table at the bottom of that file does most of the work.

Say "no coherent system" when that is the truth. It usually is, and it is the most actionable finding available.

---

## Teardown

Read `references/app-dna.md` and follow it. The short version:

1. Pick sources and say which: the codebase, the running product, Mobbin when connected, or the user's screenshots.
2. From a codebase, list the screens and their file-level states:

   ```bash
   python3 scripts/route_inventory.py ./path/to/app
   ```

3. Use the product. Do its core loop once before describing anything.
4. Walk it in the vocabulary of `references/app-taxonomy.md`: surface, app type, loop, shell, levels, screens as `family:type`, flows, states, components, overlays.
5. Append the `Structure` block to `profile.md`, ending with `GAPS`: what a new screen would need that the product does not define.

Count templates, not pages. Two hundred product pages are one screen.

---

## Survey

**Optional tooling:** if the user has a Mobbin MCP connection, it can source peer candidates (`peer-research.md`, "Sourcing the set") — it returns screenshots, so extraction still runs on the real sites. Without the connection, web search sources the set; the survey is identical either way and Mobbin is never a prerequisite.

Read `references/peer-research.md` and follow it. The short version:

1. Assemble six to eight sites: 2–3 direct competitors, 1–2 category leaders, 2 adjacent categories, 1 outlier. The adjacent ones matter most — they are where non-obvious moves come from.
2. Extract each.
3. Build the comparison table.
4. Answer four questions in writing: what is unanimous, what is contested, who is memorable and on which axis, and what nobody does.

The output is `CONTESTED` and `UNOCCUPIED` — the axes where the category has no consensus and the styles nobody has taken. Those feed `ui-ux-studio`'s divergence matrix directly and are what stop three "different" directions from collapsing into one design in three hues.

---

## Handing off to ui-ux-studio

The profile is built to be consumed, not admired.

| Target mode | What to pass | How to use it |
|---|---|---|
| **update** | `tokens.json` + the manual pass, especially `GAPS` and `STATES` | Match every axis exactly |
| **remix** | The survey's `CONTESTED` and `UNOCCUPIED` | Required, not optional — remix Step 2c. Pick *different* values per direction |
| **create** | The survey's `CONVENTION` and `HERD` | Keep convention, spend freedom on herd behavior |
| **audit** | `tokens.json` + flagged tells + the teardown's state table | Baseline to measure drift against |
| **platform-adapt** | The teardown's `Structure` block and `routes.json` | Translate each screen's job to the new surface |
| **design-system** | Declared against used, dead tokens, the component inventory | Collapse it into one system |
| **app-shell** | A survey's shell and level conventions | Decide which to keep |

Before any handoff, prove the extraction (`references/evidence.md`):

```bash
python3 scripts/dna_check.py ./dna/example              # complete and labeled?
python3 scripts/dna_check.py ./dna/example --structure  # after a teardown
```

Then build the round-trip specimen: a one-page sample made from `tokens.json` alone, set next to a capture of the source at the same width. It is the only check that tests the tokens instead of the script.

Always run the contrast check before treating an extracted palette as usable — inheriting someone else's accessibility failures is a real risk when matching a style:

```bash
python3 scripts/contrast.py --tokens ./dna/example/tokens.json \
  --tokens-dark ./dna/example/tokens-dark.json
```

The roles are inferred, so the pairs `contrast.py` checks are guesses and some never co-occur on screen — an inverted band will pair a color against itself. Once you know the real combinations, declare them and re-run:

```json
{ "tokens": { "...": "..." },
  "pairs": [["ink-body","stock"], ["band-ink","band-bg"]] }
```

## Honesty about limits

Say which sites were extracted live and which from saved copies, and when. Say what the script could not see. An extraction presented as complete when half the system is applied at runtime is worse than one that names its gaps, because the gaps are exactly where the next person will guess wrong.

Do not reproduce a peer's distinctive identity. This produces a map of the space, not assets to lift.

## Files

| File | Read it when |
|---|---|
| `playbooks/` | Always — the step list for the job in hand |
| `references/extraction.md` | Always, after running the script — the nine-step manual walk |
| `references/evidence.md` | Before writing a profile and before any handoff — claim labels, the evidence block, proving an extraction, the reply frame |
| `references/app-dna.md` | Running a teardown — sources, the ten-step walk, the `Structure` block |
| `references/app-taxonomy.md` | Naming an app's type, shell, screens, states, and flows (same file `ui-ux-studio` plans with) |
| `references/peer-research.md` | Running a survey |
| `references/style-taxonomy.md` | Naming a style, or picking families that differ |
| `scripts/extract_style.py` | Every extraction |
| `scripts/contrast.py` | Checking an extracted palette before reusing it (same script ui-ux-studio ships) |
| `scripts/route_inventory.py` | Every teardown of a codebase — routes, templates, and file-level loading, error and not-found states |
| `scripts/dna_check.py` | Before every handoff — the profile is complete and every claim is labeled |

The playbook form and the proof-before-handoff discipline are adapted from pstack by Lauren Tan (MIT).
