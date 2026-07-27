# Archetypes

Before any visual decision, answer one question: **what kind of thing is this?**

This step exists because of a specific, repeatable failure. A design can be well-spaced, accessible, distinctive, and pass every tell check, and still be wrong — because it was built to the conventions of a category the subject does not belong to. The most common version is a small, human, low-stakes thing dressed as a large, institutional, high-stakes one. Nothing in a token system catches that. Only the archetype does.

## Diagnosis: the SPARC case

Three directions were produced for a twelve-person student club with three shipped projects and no meeting currently scheduled. Two failed and one worked, and the difference was entirely archetype fit.

- **A · The Register** framed the club as an institutional archive: accession numbers (`SPARC·2025·P01`), "members on the books," "register opened 2025 · revised April 2026," "entries are numbered on opening and stamped on delivery." Eleven distinct pieces of institutional-weight language.
- **B · Standby** framed it as an operations dashboard: "Status: live," "Crew 12," "3 / 3 shipped, 0 currently running," "Next session: None set." Nine such terms. The live status board's main achievement was advertising that nothing was happening.
- **C · Contact Sheet** framed it as a room with people in it: "Twelve people, one room, three shipped products." "Mohammed, the club president, brought in CollegiateX — and every member got an internship building their mobile app." One such term.

All three passed the divergence matrix. All three had defensible token systems. Two were still wrong, because a twelve-person club is not an archive and does not have live operational state. The concept itself was the tell — not the CSS.

The lesson: **divergence without archetype fit produces directions that are reliably different and reliably inappropriate.** Fit is the gate; divergence happens inside it.

## Step 1 — Classify

Name the archetype explicitly and state it to the user before designing. When it is genuinely a hybrid, name the primary and say what it borrows.

| Archetype | Recognize it by |
|---|---|
| Club / campus org / community group | Volunteer-run, members not customers, joining is free, activity is episodic |
| Personal portfolio | One person, the work is the product, the goal is being hired or commissioned |
| Product marketing / SaaS | Something is for sale or signup, there is a pricing question |
| Program or app UI | Logged-in, task-oriented, the user returns repeatedly |
| Internal tool / admin | Captive audience, efficiency over persuasion, nobody chose to be here |
| Documentation | Readers arrive with a specific question and leave when answered |
| Event / conference | Fixed date, the date is the most important fact on the page |
| Nonprofit / cause | Asking for money, time, or attention on behalf of someone else |
| Local business / service | Hours, location, and phone number outrank everything |
| Editorial / publication | The writing is the product |
| Open-source project | Developers evaluating whether to adopt; install and docs are the conversion |
| Agency / studio | Selling taste; the site is itself the proof |
| Course / educational | Structured progression, learner anxiety is the main design constraint |

## Step 2 — Answer these four

For the chosen archetype:

1. **The ten-second job.** What does a visitor need to know before they decide to stay or go? For a club that is *what it is, whether I can join, and when it meets*. For docs it is *does this answer my question*. Everything else is secondary and the layout should say so.
2. **The content model.** What content actually exists — not what a template expects. A club has photos, names, dates, projects, and a form. It does not have testimonials, pricing tiers, or logo clouds. Designing slots for content that does not exist is what forces invention, and invented content is the loudest tell there is.
3. **Load-bearing conventions.** Which category conventions genuinely help, and which are herd behavior. Users looking for a meeting time expect to find it near the top; that convention is load-bearing. A hero with a big claim and two buttons is not.
4. **Scale honesty.** How big, old, and busy is this thing *actually*? Write the numbers down. Twelve members. Three projects. Three meetings held. Zero scheduled. Then check every design decision against them.

## Step 3 — The scale-honesty test

Ask directly: **does this design imply more weight, activity, or permanence than the subject has?**

| Design move | Implies | Fails when |
|---|---|---|
| Archive, ledger, register, accession numbers | Decades of records, institutional custody | The thing is two years old with three entries |
| Live status board, ops readout, "currently running" | Continuous operation worth monitoring | State changes monthly, or there is no state |
| Enterprise trust signals, compliance badges, SOC2 | Procurement review, security questionnaires | Nobody is buying anything |
| Logo cloud, "trusted by" | Named customers who consented | There are no customers |
| Pricing table with a highlighted tier | A pricing decision exists | It is free |
| Testimonial carousel | Volume of user opinion | You would have to invent the people |
| Big round stat triad (10x, 99.9%, 500+) | Measured scale | The real numbers are 12 and 3 |
| Manifesto hero, abstract mission claim | Earned authority | The reader has never heard of you |

Getting caught by this table is not a styling problem. It means going back to the concept.

The inverse failure exists too and is rarer: rendering something genuinely high-stakes as casual and playful. A payroll tool with hand-drawn illustrations and jokes in the error states undercuts the trust the product needs.

## Archetype notes

Each entry: the ten-second job, what content exists, what actually helps, the register, and the cosplay traps specific to it.

### Club / campus org / community group

**Ten seconds:** What is this, can I join, when and where does it meet.
**Content:** Real photos of real members. Names and roles. Meeting time and room. Past projects or events with dates. A join link, usually a form. An email address.
**Helps:** Photographs of actual people doing the actual thing — this is the single strongest asset and most club sites bury it. The meeting time visible without scrolling. Plain description of what members do. Named officers, because a prospective member wants to know who they would be emailing.
**Register:** First person plural, concrete, unpolished. "We meet Thursdays in Room 8065." Specific beats impressive. A club that says "we shipped three products and everyone got an internship" is more persuasive than one that says it is "fostering innovation."
**Cosplay traps:** institutional archive; ops dashboard; startup landing page with a hero claim and two CTAs; fake testimonials from members; invented metrics; a mission statement in place of a description of activities; "join our community" instead of the actual meeting time.

### Personal portfolio

**Ten seconds:** Who is this, what do they make, are they any good, how do I reach them.
**Content:** Work with images. What each piece is, the role played, the outcome. Contact. Sometimes a résumé.
**Helps:** Work first, biography second. Specific role attribution on team projects. Enough context per piece that a non-expert understands it. One clear contact path.
**Register:** First person, direct. Owning a specific role beats vague credit.
**Cosplay traps:** agency plural ("we") for one person; SaaS marketing structure for a body of work; a services/pricing page for someone seeking employment; skill bars with invented percentages; a hero claiming a philosophy before showing anything.

### Product marketing / SaaS

**Ten seconds:** What does it do, for whom, roughly what does it cost.
**Content:** The product, ideally shown working. Pricing. Real customers if any. Documentation link.
**Helps:** A demo, screenshot, or live interaction beats any description. Pricing that does not require contacting sales. Specific claims.
**Register:** Second person, active, concrete.
**Cosplay traps:** enterprise trust signals on a pre-revenue product; invented customer logos; the canonical hero → logos → three features → testimonial → pricing → CTA stack; a triad of round invented statistics.

### Program or app UI

**Ten seconds:** Where am I, what can I do, what needs my attention.
**Content:** Real data at real volume, and every state — empty, first-run, loading, partial, error, permission-denied, dense.
**Helps:** Density matched to task frequency. Keyboard paths for anything done repeatedly. States that are designed rather than absent. URLs that reflect state.
**Register:** Terse, action-first. Buttons name what happens.
**Cosplay traps:** marketing-page density inside a tool; onboarding for something used daily; celebratory animation on routine actions; dashboards of vanity metrics nobody acts on.

### Internal tool / admin

**Ten seconds:** Find the record, do the thing, leave.
**Content:** Tables, forms, logs, audit trails, bulk operations.
**Helps:** Ruthless density. Bulk actions. Undo. Speed over polish. The users are captive and repeat-visiting, so learnability matters less than throughput.
**Register:** Plain and unadorned. No persuasion, ever.
**Cosplay traps:** consumer-app polish; marketing language; illustration; onboarding tours; anything that adds a click for aesthetic reasons.

### Documentation

**Ten seconds:** Does this answer my question.
**Content:** Reference material, examples, working code.
**Helps:** Search. Stable deep links. Copy-pasteable examples that actually run. Version clarity. Predictable structure across pages.
**Register:** Imperative, precise, no personality in the reference layer.
**Cosplay traps:** marketing copy in reference docs; narrative where a table belongs; hiding the search; a landing page in front of the content.

### Event / conference

**Ten seconds:** When, where, how much, who is speaking.
**Content:** Date, location, price, schedule, speakers, registration.
**Helps:** Date and location above everything, in large type. A schedule that works on a phone. Registration one click away. Clear signal on whether it already happened.
**Register:** Direct, time-anchored.
**Cosplay traps:** burying the date under a hero image; countdown timers on an evergreen page; speaker grids for three speakers styled like grids for thirty.

### Nonprofit / cause

**Ten seconds:** What is the problem, what does this org do, how do I help.
**Content:** The work, outcomes, financials, ways to give or volunteer.
**Helps:** Specifics about outcomes. Transparency about money. One clear primary action. Photographs of real work.
**Register:** Plain and unsentimental. Understatement outperforms.
**Cosplay traps:** stock imagery of people who are not the beneficiaries; emotional manipulation in place of evidence; invented impact numbers; corporate SaaS structure applied to a cause.

### Local business / service

**Ten seconds:** Are you open, where are you, what does it cost, how do I book.
**Content:** Hours, address, map, phone, services, prices, photos of the actual place.
**Helps:** Hours and phone visible immediately and tappable on mobile. Real photos, not stock. Prices if at all possible.
**Register:** Plain and local.
**Cosplay traps:** national-brand polish on a single location; stock photography; hiding the phone number behind a contact form; a startup hero above the hours.

### Editorial / publication

**Ten seconds:** Is there something here worth reading.
**Content:** Articles, authors, dates, sections.
**Helps:** Typography that supports sustained reading. A measure of 60–75 characters. Clear hierarchy among pieces. Visible dates.
**Register:** Whatever the publication's is — this is the one archetype where voice is the product.
**Cosplay traps:** broadsheet styling on a three-post blog; product-marketing structure around writing; engagement furniture that outweighs the text.

### Open-source project

**Ten seconds:** What does it do, is it maintained, how do I install it.
**Content:** Description, install command, minimal example, docs link, license, activity signals.
**Helps:** The install command visible immediately. A runnable example above the philosophy. Honest maturity signals. Recent commit or release visible.
**Register:** Technical, unadorned, honest about limitations.
**Cosplay traps:** SaaS landing page for a library; enterprise language on a solo side project; benchmark charts with no methodology; a logo cloud of projects that merely depend on it.

### Agency / studio

**Ten seconds:** What kind of work, for whom, is it good.
**Content:** Case studies with outcomes, client list, services, contact.
**Helps:** The site being itself a demonstration. Named clients with real outcomes. Being clear about what you decline.
**Register:** Confident and specific. Named results.
**Cosplay traps:** claiming a scale you do not have; process diagrams in place of work; buzzword service lists; anonymous case studies.

### Course / educational

**Ten seconds:** What will I learn, how long, is it for my level, what does it cost.
**Content:** Curriculum, prerequisites, time commitment, instructor, price, outcomes.
**Helps:** Honest prerequisites. Realistic time estimates. Visible progression. Sample content before commitment.
**Register:** Encouraging without overpromising. The main constraint is learner anxiety.
**Cosplay traps:** hard-sell marketing on educational content; invented outcome statistics; false urgency; hiding the difficulty level.

## Hybrids

Many real briefs are hybrids, and naming the primary matters more than choosing a pure category.

- A club with a **program it built** — the club site is a club site; the program gets app-UI treatment. Do not let the app's dashboard aesthetic leak onto the club's front page.
- A portfolio that is also **a product for sale** — portfolio primary, one commerce surface, not a shop.
- An open-source project with **a commercial tier** — OSS primary above the fold; commerce below it.
- Documentation for **an internal tool** — docs primary, with the internal tool's density.

State the primary and what it borrows: "Primary archetype: campus club. Borrows from open-source project for the three shipped-project entries, since a prospective member evaluates those the way a developer evaluates a repo."

## Feeding this forward

The archetype constrains every later step.

| Later step | What the archetype supplies |
|---|---|
| The design plan's SUBJECT and THESIS | The ten-second job |
| Hero decision | The one fact from the ten-second job |
| Section order | Ranked by what the visitor came for |
| Content slots | The content model — build slots only for content that exists |
| Copy register | The register line |
| Divergence matrix | Which concepts are appropriate at all — the fit gate |
| Peer set for a survey | The category to survey |
