# Principles

One rule each, with the moment it applies. They are not read up front. When a decision is hard, find the principle whose trigger matches and apply it. In the plan or the reply, name any principle that changed a decision and say what it changed. A principle that changed nothing is not worth naming.

The shape, and several of the rules, are adapted from pstack by Lauren Tan (MIT), restated for design. The rest are this skill's own non-negotiables given names.

## Commit

- **Ground it in the subject.** Choosing palette, type, form, layout, or signature. Derive each from the subject's own world: its materials, instruments, light, vocabulary, constraints. If the choice would survive a swap to a different client, it is a default.
- **Classify before you draw.** Starting anything. Name the archetype (`archetypes.md`) and, for an app surface, write the classification line (`app-taxonomy.md`). Most wrong designs are right designs for a different category.
- **Commit, then verify.** Tempted to read every reference before planning. Read what shapes the plan, commit with conviction, then run the checks. Checking first produces compliance, and compliance produces gray.
- **Spend boldness once.** The plan has more than one bold idea. Keep one signature, put it where people land, and hold everything around it disciplined.
- **Not taking a risk is a risk.** The plan passes every check and you cannot say what it argues. Name the one deliberate risk and its reason, or go back.
- **Scale honesty.** The design implies size, age, or activity. Write the real numbers down and check every element against them.

## Structure

- **The loop comes first.** Laying out a shell or a home screen. Whatever the user does a hundred times is reachable in one action from where they start. Nothing sits in front of it.
- **Content before chrome.** Adding a slot, section, tile, or tab. Build only for content that exists. An empty slot forces invention, and invented content is the loudest tell.
- **Conventions carry the navigation.** Tempted to make navigation, back, or a system gesture distinctive. Keep the load-bearing set (`conventions.md` §1, `platforms.md`) and spend the freedom elsewhere.
- **Model the states.** A screen has more than two conditions. Make its state one value that is exactly one thing, switch on it, and draw the chart when a state can return to an earlier one (`states.md`).
- **One primary action.** Two controls on a screen carry equal weight. Decide what the screen is for and let one win.
- **Real data at real volume.** Building or reviewing with placeholder content. Use the real field names, the real ranges, the longest realistic string, zero items, one item, and a hundred.
- **Least interrupting overlay.** Reaching for a modal. Use the smallest container that holds the content (`app-taxonomy.md` §6). A modal from a modal is a screen.

## Reduce

- **Subtract before you add.** The design feels unfinished. Remove one thing before adding one. The accessory too many is usually a gradient, a badge, or a third weight.
- **Experience first.** Convenience for the builder conflicts with the person using it. Choose the person. Three finished screens beat ten rough ones.
- **Fix the plan, not the CSS.** A check fails: flat scale, no ramps, a failed contrast pair, a tell. Trace it to the plan line that caused it and change that. A patch in the stylesheet leaves the cause in place for the next screen.

## Decide

- **Exhaust the design space.** A decision with no precedent, or a fork that taste alone cannot settle. Build two or three throwaway variants behind one switcher and look (`playbooks/prototype.md`). Arguing about a design nobody has seen is the expensive path.
- **Three arguments, not three skins.** Presenting options. Each option states what it believes the product is. If you cannot say how they disagree, they do not differ.
- **Research is evidence, not derivation.** Opening a pattern library or a competitor. Carry away counts, conventions, and step numbers. Leave the look (`ai-tells.md` §10b).
- **Do not block on a reversible choice.** About to ask the user which of two things you could build and show. Build it, show it, say what you chose and why. Stop only for choices that are expensive to undo: brand, information architecture, deleting someone's content.

## Prove

- **Prove it rendered.** About to say a design is done. Look at the real thing at the real sizes, in each state, and show what you saw (`proof.md`). "The CSS is correct" is a claim about code, not about a screen.
- **Label every claim.** Reporting a result. Mark it measured, observed, inferred, or guess. Never hand the user a check you could have run.
- **Explain the number.** Reporting a contrast ratio, a craft score, a tell count, a step count. Say what it measured and what limits it. A contrast pass on inferred pairs is a pass on guesses until the real pairs are declared.
- **Encode the lesson.** Giving the same correction a second time. Put it where it cannot be skipped: a token, a rule in `ai_tells.py`, a line in the state manifest. A sentence in a document is the weakest place to keep a rule.
- **Log the decisions.** Long or unattended work. Keep the trail (`proof.md`, decision log) so the reasoning survives the session.
