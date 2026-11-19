### Spec to UI

**You own making the system comprehensible. Three models that differ in structure, not in skin.**

1. Classify the archetype, then write the classification line (`references/app-taxonomy.md` §1). App type and loop come from the spec's actors and actions.
2. Read the artifact: entities, relationships, actions, states, access, volume (`references/modes.md`, spec-to-ui Step 1). If it is a planning bundle from the `swe-plan` skill, the entities are `E-##` in `03-data-model.md` with their lifecycle state machines, and the journeys are `UC-##` in `04-flows.md`. Keep the IDs: every screen names the use cases it serves.
3. Build the interface inventory: entities to screens (each named `family:type`), actions to controls, states per screen, and `GAPS`, the endpoints the interface needs that do not exist.
4. Choose three interaction models that differ structurally (`references/modes.md`, Step 3). For each: what it optimizes, what it makes harder, which endpoints it needs.
5. Produce the flow inventory for any multi-step journey (`references/flows.md` §6).
6. Build all three against the real data shape: real field names, real ranges, long strings. Every screen ships the states its family requires (`references/states.md`).
7. Proof ladder on each (`references/proof.md`), with `states.json` per model. With a planning bundle, run `python3 scripts/state_coverage.py states.json --bundle docs/`: every use case has a screen, and no screen covers an ID that does not exist.

**Reply:** the classification, the interface inventory, `GAPS` first and prominent, the three models with what each costs the backend and how each degrades at 100 times the data, proof per model, a recommendation.
