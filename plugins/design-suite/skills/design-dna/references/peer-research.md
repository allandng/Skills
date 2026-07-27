# Peer research

Extracting one site tells you what that site does. Extracting six tells you what the *category* does — and the difference between those two is where design decisions actually live.

This is the part that replaces a paid style database, and it is better than one, because a database is a snapshot of what was fashionable when it was compiled, and this is current.

## Why the comparison set matters

Every visual choice on a site is one of three things:

1. **Convention** — everyone in the category does it, and breaking it costs comprehension. Banking sites use blue and conservative type because trust is the product. Breaking that is a real risk with a real cost.
2. **Herd behavior** — everyone does it, and nobody remembers why. This looks identical to convention from inside a single site, and it is the largest available source of differentiation.
3. **Distinction** — one competitor does it and it is why you remember them.

You cannot tell these apart by looking at one site. That is the entire argument for doing this.

## Building the set

Aim for six to eight sites. More than that and the analysis flattens; fewer and convention is indistinguishable from coincidence.

Pull from four groups:

- **Direct competitors** (2–3) — same product, same buyer.
- **Category leaders** (1–2) — the site everyone in the space is unconsciously copying. Often the oldest or the best-funded.
- **Adjacent categories** (2) — different product, same *job* or same user. A recipe app should look at note-taking tools and field guides, not only at other recipe apps. This is usually where the distinctive move comes from.
- **The outlier** (1) — the one in the category that looks nothing like the others. Whether or not it succeeded, it shows you which conventions are actually load-bearing.

Find them by searching for the category plus the year, "best X tools", review-aggregator listicles, and the "similar sites" sections of comparison pages. Then verify each is live and current before extracting — a dead startup's 2019 site is evidence about 2019.

## Running the set

For each site:

```bash
python3 scripts/extract_style.py --url https://competitor.com --out ./dna/competitor
```

If the sandbox has no network, fetch each page with your own web tooling, save the HTML and CSS, and use `--dir`. Note in the output which sites were extracted from the live page and which from a saved copy.

Then do a fast manual pass on each — you do not need the full walk from `extraction.md` for peers. Three things per site: the signature element, the type roles, and the voice in one sentence.

## The comparison table

Build this. It is the deliverable.

| | Peer A | Peer B | Peer C | Peer D | Peer E | Peer F |
|---|---|---|---|---|---|---|
| contrast model | | | | | | |
| surface hex | | | | | | |
| primary hex | | | | | | |
| accent count | | | | | | |
| neutral temperature | | | | | | |
| display face category | | | | | | |
| body face category | | | | | | |
| utility face present | | | | | | |
| type steps / ratio | | | | | | |
| median spacing | | | | | | |
| radius personality | | | | | | |
| shadow levels | | | | | | |
| motion character | | | | | | |
| layout system | | | | | | |
| signature element | | | | | | |
| named style | | | | | | |

## Reading it

Then answer four questions, in writing:

**1. What is unanimous?** Any row where all six agree is either convention or herd behavior. Separate them by asking what breaking it would actually cost the user. If the answer is "nothing, it would just look different" — that is herd behavior, and it is available.

**2. What is contested?** Rows with real spread mean the category has no consensus, so this axis is free. Free axes are cheap differentiation: you can take an unusual position without confusing anyone.

**3. Who is memorable, and on which axis?** Usually one peer is distinctive on exactly one axis and conventional everywhere else. That is the correct pattern — it is `ui-ux-studio`'s "spend boldness once", visible in the wild.

**4. What does nobody do?** Scan the taxonomy in `style-taxonomy.md` for families absent from the set entirely. An unoccupied position is only worth taking if the subject supports it — but when it does, it is the strongest available move.

## Output

```
## Category: <name>
Set: <sites, with extraction date and live/saved noted>

CONVENTION      what to keep, and the cost of breaking each
HERD            what everyone does for no reason - the opportunity list
CONTESTED       axes with no consensus - free to take a position
MEMORABLE       who stands out, on which single axis
UNOCCUPIED      taxonomy families nobody in the set uses
RECOMMENDATION  the two or three axes to differentiate on, with reasoning
                tied to the subject, not to novelty for its own sake
```

Hand `CONTESTED` and `UNOCCUPIED` straight into `ui-ux-studio`'s divergence matrix — they are exactly what it needs to keep three directions from collapsing into one.

## Two cautions

**Do not copy a peer.** The output is a map of the space, not a template to borrow. Extracting a competitor's palette and using it is both bad design and, if the identity is distinctive enough, a legal question.

**Differentiation is not the goal — appropriateness is.** If a category convention exists because it genuinely helps users, keep it. The point of this exercise is knowing *which* conventions those are, so the freedom gets spent on the ones that don't matter.
