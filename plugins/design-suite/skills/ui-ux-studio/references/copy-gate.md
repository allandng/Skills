# The copy gate

Every string a human reads passes through this before the work ships. Headlines, body copy, button labels, form labels, help text, error messages, empty states, tooltips, alt text, page titles, meta descriptions, and any placeholder or sample content that survives into the deliverable.

The reason this is a gate rather than a guideline: copy is the fastest-read part of an interface and the least protected. A page can survive every visual check and still announce itself on the first line of the hero. In the ORBIT case the concept failure was legible almost entirely through language — "members on the books," "entries are numbered on opening and stamped on delivery," "Status: live" — before anyone looked at the type.

## First: decide whether the copy is the asset

The gate runs in two directions, and running it the wrong way destroys value. Before editing anything, judge the existing copy:

**Signs it is the asset:** specific numbers and named things instead of adjectives; limitations admitted voluntarily ("what we are not claiming", "this does not work for X"); sentences no competitor could publish; a register consistent enough to recognize. Copy like that took someone real effort and is doing real work.

**When it is the asset, the gate inverts.** The job becomes *protection*: new strings must match its register, and the checklist question changes from "does this pass" to "could the person who wrote the original have written this." Do not smooth its quirks, do not lengthen what is deliberately short, do not replace dry precision with marketing warmth. In remix mode good copy is an **invariant** carried across all three directions unchanged; in update mode it is part of the system the seam test protects.

**When it is not the asset** — template phrasing, borrowed weight, invented specifics — run the gate as written below.

State which way you ran it in the handoff. "Copy gate: inverted, existing copy preserved as the register standard" is a decision; silently rewriting good copy is the same failure as restyling a good design.

## Order of operations

1. **Check the archetype register first.** `archetypes.md` gives a register line per archetype. Copy that reads AI is very often copy written for the wrong archetype — startup-marketing voice on a student club, consumer polish on an internal tool. Fix the register before polishing sentences, or you will produce well-edited copy that is still wrong.
2. **Run the UI-specific rules below.** General prose tools are not tuned for microcopy and some of their rules invert here.
3. **For any prose longer than about two sentences, hand off.** If `anti-ai-writing` or `avoid-ai-writing` is available, use it — those cover vocabulary tiers, sentence rhythm, and structural tells at a depth this file does not attempt. This gate covers what they do not: interface strings.
4. **Read it aloud.** The single most reliable test. Anything you would not say out loud to the user's face gets rewritten.

## Where UI copy rules differ from prose rules

Prose-humanizing tools will give advice that is wrong for interfaces. Reconcile like this:

| Prose rule | In UI copy |
|---|---|
| Remove em dashes | Mostly agree in body copy. But `…` for loading, curly quotes, and non-breaking spaces in `10 MB` / `⌘ K` are correct typography, not tells — see `interface-guidelines.md` §8 |
| Vary sentence rhythm | Does not apply to labels. Parallel structure across a set of buttons or nav items is correct and consistency beats variety |
| Avoid repetition | Inverted. The same action keeps the same word everywhere: a "Publish" button produces a "Published" toast. Synonym variation is a usability bug |
| Immaculate typography is a tell | Inverted. Interface copy should be typographically correct |
| Cut hedging | Mostly agree, but genuine uncertainty must be stated: "This may take a few minutes" is honest, not hedging |
| Bullets are overused | Agree in marketing copy. In documentation and reference content, lists are correct |

## The rules

### Buttons and actions

Name what happens. The label is a promise about the next screen.

- "Save changes" not "Submit" · "Send invite" not "Continue" · "Delete project" not "OK"
- The action keeps its name through the whole flow. Publish → Published. Not Publish → Success!
- Destructive actions say what is destroyed: "Delete 3 drafts", not "Are you sure?"
- Sentence case unless the surrounding system is title case. Match the house style over your preference.

**Flag:** Get Started · Learn More · Continue · Submit · Click Here · Explore · Discover

### Errors

State what happened, then the fix. Errors do not apologize and are never vague.

- "Password needs at least one number" not "Invalid password"
- "That file is 12 MB. The limit is 5 MB." not "Upload failed"
- No blame: "Check the email address" not "You entered an invalid email"
- No apology theatre: "Sorry, something went wrong!" says nothing. What went wrong, and what now?
- No exposed internals: never a stack trace or error code alone, though a code alongside plain language is fine for support.

### Empty states

An empty screen is an invitation, not a dead end. Say what goes here and give the action.

- "No projects yet. Create one to get started." with the button present.
- Distinguish *nothing yet* from *nothing matched*. A filtered list with no results needs "No results for 'foo'" and a way to clear the filter, not the first-run message.
- No mascots apologizing. No "Oops! It's empty in here."

### Labels and help text

- Labels name the thing in the user's words, not the system's. "Notifications", not "Webhook configuration".
- Placeholders show an example pattern and end with `…`. A placeholder never replaces a label.
- Help text earns its place or goes. "Enter your email address" under a field labeled Email is noise.
- Each element does one job: a label labels, an example demonstrates, and nothing does double duty.

### Headings and hero copy

- The hero says the one fact from the archetype's ten-second job. For a club that is what it is and when it meets — not a claim about transformation.
- Specific outranks impressive, every time. "Twelve people, one room, three shipped products" beats "Fostering the next generation of innovators."
- Numerals for counts: "3 projects", not "three projects", in UI contexts.
- No two-abstract-noun feature titles: "Smart Insights", "Powerful Analytics", "Seamless Integration".

### Sample and placeholder content

This is where invented content enters and it counts as copy.

- Never `lorem ipsum` in a deliverable.
- Never invented people: `Sarah Chen, CTO at TechCorp`, `Marcus Rodriguez`, `Jane Doe`.
- Never invented metrics presented as fact: `10x`, `99.9%`, `500+`, `trusted by thousands`.
- Sample data uses the real schema, real field names, and realistic value ranges including the long strings.
- If real content is unavailable, use plainly-marked placeholders and say so in the handoff. An honest `[client name]` is better than a fabricated one.

## Vocabulary to cut

Interface and marketing copy, on sight:

effortlessly · seamlessly · supercharge · unlock · elevate · empower · streamline · harness · leverage · revolutionize · game-changing · cutting-edge · robust · comprehensive · delve · dive into · realm · landscape (as metaphor) · tapestry · testament to · pivotal · meticulous · showcase · thriving · vibrant · nestled · bustling

Structural patterns to cut:

- "Transform your X into Y" · "Take your X to the next level" · "X, reimagined"
- "It's not X — it's Y" and its split form across two sentences
- The em-dash triad: "Fast, simple — and secure."
- "Built for teams who move fast" · "Designed for the way you work"
- Compulsive triads. Two items or four is fine; three every time is a rhythm tell.
- Hollow intensifiers: genuinely, truly, really, quite frankly, to be honest, it's worth noting

## Borrowed-weight language

The specific class that produced the ORBIT failure. This language implies institutional scale, custody, or continuous operation. Check it against the numbers from the archetype's scale-honesty step.

**Archive register:** on the books · on record · standing record · accession · register opened · revised [date] · stamped · entries are numbered · of record · custody · holdings

**Operations register:** status: live · currently running · crew · on duty · channels · uptime · board revised · none set · operational

Each is fine when true. "On record" is right for a registry with thousands of entries and wrong for twelve members. "Currently running: 0" is right for a system with jobs and wrong for a club that meets monthly — and it advertises inactivity, which is worse than saying nothing.

Test: **would the subject's own members use this word about themselves?** A student club says "we have twelve people." It does not say "twelve members on the books."

## Checklist

```
COPY GATE
  [ ] direction decided first: is the existing copy the asset?
  [ ] register matches the archetype, not a borrowed category
  [ ] borrowed-weight language checked against the real numbers
  [ ] every button names what happens
  [ ] one word per action, used consistently through the flow
  [ ] errors give the fix, not just the problem
  [ ] empty states distinguish "nothing yet" from "nothing matched"
  [ ] labels use the user's words
  [ ] no invented people, metrics, testimonials, or logos
  [ ] no lorem ipsum, no unmarked placeholder
  [ ] vocabulary list clean
  [ ] specific beats impressive in every headline
  [ ] read aloud, and you would say it to the user's face
  [ ] longer prose passed to anti-ai-writing / avoid-ai-writing if available
```

Report it in the handoff as `COPY GATE: passed` plus anything deliberately kept and why. A tell kept on purpose with a stated reason is a decision; an unexamined one is a default.
