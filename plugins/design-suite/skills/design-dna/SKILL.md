---
name: design-dna
description: Reverse-engineer the design system of any website into reusable tokens, and research how a whole category designs itself. Extracts palette, typography, spacing, radii, elevation, motion, and layout from a live URL or saved files into a tokens.json plus a written style profile, names the style from an open taxonomy, and flags AI tells. Also builds a peer comparison set across competitors and adjacent categories to separate genuine convention from herd behavior. Use this whenever the user points at a website and wants to know how it is designed, wants to match, extend, or deliberately diverge from an existing style, asks what competitors or similar sites look like, needs design tokens pulled out of an existing codebase, or asks for a style breakdown, design audit input, or a moodboard grounded in real sites. Output is built to feed the ui-ux-studio skill directly - use it before ui-ux-studio's remix, update, or create modes whenever a real reference site exists.
---

# Design DNA

Turn real websites into design systems you can reuse.

Two jobs. **Extract** pulls a single site apart into tokens and a written profile. **Survey** runs that across a category so you can tell what is convention, what is herd behavior, and what is actually distinctive. Most useful work needs both: extraction alone tells you what a site does, and only the comparison tells you whether that means anything.

This exists because style databases go stale and the good ones charge for the interesting categories. Deriving a style from six real sites you picked is more current than any snapshot, and it is specific to the competitive set that actually matters.

## Route

| Ask | Do |
|---|---|
| "how is this site designed", "pull the tokens out of this", "what style is this" | **Extract** |
| "what do sites like this look like", "how do competitors design", "what's the convention here" | **Survey** (extract runs inside it) |
| "match this style", "add to this site" | **Extract**, then hand off to `ui-ux-studio` **update** mode |
| "redesign this", "give me options" | **Survey**, then hand off to `ui-ux-studio` **remix** mode |

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

## Survey

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
| **audit** | `tokens.json` + flagged tells | Baseline to measure drift against |

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
| `references/extraction.md` | Always, after running the script — the nine-step manual walk |
| `references/peer-research.md` | Running a survey |
| `references/style-taxonomy.md` | Naming a style, or picking families that differ |
| `scripts/extract_style.py` | Every extraction |
| `scripts/contrast.py` | Checking an extracted palette before reusing it (same script ui-ux-studio ships) |
