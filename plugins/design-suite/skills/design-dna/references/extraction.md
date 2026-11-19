# The manual pass

`extract_style.py` reads what the CSS declares. It cannot see what the design *does*. This is the second half of an extraction, and skipping it produces a token dump rather than a design system.

## What the script structurally cannot see

- **Runtime styles.** Anything applied by JavaScript, CSS-in-JS with generated class names, or a theme switcher.
- **States.** Hover, focus, active, disabled, loading, error. These are in the CSS but the script cannot tell you whether they are *consistent*, which is the thing that matters.
- **Hierarchy.** Which of the extracted colors is the primary action versus an incidental fill. Frequency is a weak proxy.
- **Composition.** Rhythm, asymmetry, where the eye lands, whether the grid is real or decorative.
- **Imagery strategy.** Photography treatment, illustration style, whether images are full-bleed or contained, aspect ratio discipline.
- **Voice.** The copy register, sentence length, how errors and empty states speak.
- **Intent.** Every question of *why*. A warm cream ground might be a ceramics studio's actual glaze color or an AI default. Only the context tells you which.

## The walk

Open the site and work through this in order. Take screenshots at 375px, 768px, and 1440px before forming an opinion.

**1. The two-second test.** Load the page and look away. What do you remember? That is the signature element, whether or not it was designed as one. If you remember nothing, the site has no signature — record that.

**2. Type in use.** The script lists declared families; you need the *roles*. Which face carries display, which carries body, which carries numbers and labels. Is there a utility face at all, or is everything one family? Where does the scale actually get used versus merely declared?

**3. Color in use.** Take the extracted palette and find each color on the page. What is each one *for*? A color used once on a single button is a primary; the same hex used as a background wash is something else. Note any color that appears in the CSS but nowhere on screen — dead tokens are common and tell you the system has drifted.

**4. The grid.** Is there one? Do elements actually align to it, or is alignment coincidental? Where is it broken, and is the break deliberate? Measure two or three sections and check whether the spacing scale is obeyed or approximated.

**5. States.** Hover every interactive element. Tab through the page. Trigger a form error. Load it on a throttled connection to see the loading state. Find an empty state if you can. Record whether these are designed or absent — most sites fail here, and for `update` mode this is the single most important thing to know, because you will have to invent what is missing.

**6. Density and rhythm.** Does section spacing vary by hierarchy, or is it uniform? Uniform section padding tells you the layout is a stack rather than a structure.

**7. Motion.** Scroll slowly. What animates, when, and why? Is motion communicating something or decorating? Check `prefers-reduced-motion` if you can.

**8. Imagery.** Photographic or illustrated? Treated (duotone, grain, crop discipline) or raw? Consistent aspect ratios? This is often the largest visual surface and the script sees none of it.

**9. Voice.** Read three buttons, one error, and one empty state. Write down the register in a sentence. Copy is part of the design system and `update` mode has to match it.

## Recording the result

Append to the generated `profile.md`, below the `Evidence` block from `evidence.md`. End every line except `GAPS` with an evidence label: `[measured]`, `[observed]`, `[inferred]` or `[guess]`. `scripts/dna_check.py` fails a profile with an unlabeled or empty line.

```
## Manual pass

SIGNATURE     what you remember after two seconds, or "none"
TYPE ROLES    display / body / utility, and where each is used
COLOR ROLES   what each extracted color is actually FOR
FRAMEWORK     bespoke | stock <name> | stock-with-overrides — start from the
              script's fingerprint report, verify by eye which parts were
              actually customized
DEAD TOKENS   declared but unused
GRID          real | approximate | absent; where broken and whether deliberate
STATES        which exist, which are missing, which are inconsistent
RHYTHM        does section spacing vary by hierarchy?
IMAGERY       kind, treatment, crop discipline
VOICE         one sentence on register, plus three verbatim examples
INTENT        which choices look deliberate and which look like defaults
GAPS          what a new section would need that the system does not define
```

That `GAPS` line is what `update` mode consumes. Everything a design system does not define is a place where the next contributor will guess, and guessing is how systems drift.

## When the site has no system

Frequently the honest finding is that there isn't one: spacing is arbitrary, there are eleven grays, four radii, and six shadows. Say so plainly and quantify it — "17 distinct spacing values across 4 pages" is more useful than a diplomatic summary.

In that case `update` mode has a decision to make, and it belongs to the user, not to you: match the inconsistency to stay invisible, or introduce a small system for the new work and flag it as a deliberate departure. Ask.
