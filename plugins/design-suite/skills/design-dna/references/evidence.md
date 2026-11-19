# Evidence

An extraction is a set of claims about someone else's design. Some were read out of a file, some were seen, some were reasoned, and some are guesses. They look identical in a profile unless they are labeled, and the guesses are where the next person goes wrong.

Read this before writing a profile's manual pass, and before handing anything to `ui-ux-studio`.

## Labels

Put one at the end of every line in the `Manual pass` and `Structure` blocks.

| Label | Means | Examples |
|---|---|---|
| `[measured]` | A script or tool produced it, and it can be rerun | Declared custom properties. Counts of distinct spacing values. Contrast ratios. The route inventory |
| `[observed]` | You looked at the rendered product | The signature. Which states exist. What animates. Imagery treatment |
| `[inferred]` | Reasoned from frequency, naming or structure | Color roles when there is no token layer. "This is the primary action". App type. Intent |
| `[guess]` | None of the above | Anything about screens you could not reach |

Two rules follow.

- **Inferred roles are not the system.** `extract_style.py` guesses roles from frequency when a site declares no tokens, and those guesses are often wrong: a border color that is really a text color, an accent that is really a divider. Declared custom properties are `[measured]`. Inferred roles stay `[inferred]` until you have found the color on the page and seen what it does.
- **Never upgrade a label by rewording.** "The primary color is blue" and "blue appears to be the primary" are the same inferred claim. It becomes observed when you look.

## The evidence block

Append to `profile.md`, above the manual pass:

```
## Evidence

SOURCE      live URL | saved copy | codebase at <commit> | Mobbin | user screenshots
CAPTURED    2026-03-02, viewport 375 / 768 / 1440
COVERAGE    4 of 11 templates read: home, pricing, docs article, sign in.
            Signed-in app not reached
THEMES      light measured, dark measured | dark exists but not extracted | none
NOT SEEN    runtime-applied styles, the dashboard, any error state
```

`COVERAGE` and `NOT SEEN` are the two lines that keep an extraction honest. Four templates out of eleven is a fine extraction of four templates.

## Proving an extraction

Before handing off, in order:

1. **Completeness.** `python3 scripts/dna_check.py ./dna/<name>` confirms the token file parses, every manual-pass line is filled, the evidence block exists, and reports how many claims carry each label. Add `--structure` after a teardown.
2. **Round trip.** Build a one-page specimen from `tokens.json` alone: the palette as swatches with their roles, the type scale set in the extracted faces, one button, one card, one input. Put it next to a capture of the source at the same width. If the specimen does not look like it belongs to the source, the tokens are wrong or incomplete, and the mismatch tells you which. This is the only check that tests the tokens instead of the script.
3. **Contrast.** `python3 scripts/contrast.py --tokens tokens.json`, with the real pairs declared once you know them. You are about to reuse this palette. Do not inherit its failures.
4. **Spot checks.** Pick three extracted values at random and find each on the page. Three for three, or look harder.
5. **Freshness.** A saved copy or a Mobbin capture is a snapshot. Say how old.

If a step cannot be run here, write `n/a: <reason>` for it in the reply. Do not skip it silently.

## The reply

```
GOAL       what was asked
SOURCE     what was read, when, and how much of it
FOUND      the system in five lines, or "no coherent system" with the counts
STRUCTURE  the classification line, if a teardown ran
PROOF      dna_check output, the round-trip result, contrast, spot checks
LIMITS     what was not seen and what that puts at risk downstream
HANDOFF    which ui-ux-studio playbook this feeds and which lines it needs
```

Lead with what the user can now do. A profile is for building from.
