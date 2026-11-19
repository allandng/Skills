### Flow

**You own the path between screens. Every screen can be good and the flow still bad.**

1. Name the flow's purpose (`references/app-taxonomy.md` §7) and its one outcome. Name where users enter it from.
2. Write the flow inventory line: entry points, steps, branches, escape hatch, and the abandonment line (`references/flows.md` §6).
3. Cut steps. Ask late, ask less, and never ask what you can infer or defer (`references/flows.md` §2 and §3).
4. Check the step count and the hardest step against shipped products, with counts (`references/app-taxonomy.md` §8, `references/flows.md` §5b).
5. Draw the statechart, including resumed and blocked (`references/states.md` §3). Every state has a way out. Every submit is safe to repeat.
6. Design each step as an `entry` or `input` screen with its required states. Position, back, persistence and completion per `references/flows.md` §4.
7. Build. Walk it forward, backward, with a refresh mid-step, and abandoned then resumed.
8. Proof ladder (`references/proof.md`), with `states.json` covering every step.

**Reply:** purpose and outcome, the flow inventory with the abandonment line, the chart, steps cut and why, what the lookup showed, the four walks and their results, open decisions.
