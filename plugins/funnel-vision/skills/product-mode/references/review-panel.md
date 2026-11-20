# Review panel

Several reviewers, each holding one position, try to break an analysis, a metric or a plan. A finding survives only when the reviewer can point at it: a rerun number, a definition, a row in the data. The panel reports. It does not rewrite.

After pstack's `interrogate`, which does this to code.

Each reviewer gets the artifact, the decision it serves, and its lens. Nothing else: no narrative of how the analysis was done, no earlier review. With subagents available, one per lens in parallel with fresh context. Without them, one lens at a time, each list written down before the next.

## The lenses

Pick four to six. The first three are always in.

| Lens | Holds this position | Looks for |
|---|---|---|
| **Statistician** | Trusts nothing without n | Missing intervals, differences inside the noise, peeking, many comparisons with one "winner", means of skewed data, users counted before their window passed |
| **Data engineer** | Knows how events get lost | Double fires, client-only tracking of critical events, identity splits, late mobile batches, a tracking change inside the date range, blank properties dropping rows from a segment |
| **User's advocate** | Is the person on the other side of the metric | A win that costs the user: a dark pattern, a guardrail that moved, value not delivered. Whether the user would thank you |
| **Skeptical PM** | Has seen this chart before | Mix shift, season, novelty, another launch in the window, selection (adopters were always going to stay), a metric chosen after seeing the data |
| **Platform lead** | Ships the mobile app | Blended web and mobile numbers, app version not controlled, an effect that is really release adoption, a flow never walked on a phone |
| **Newcomer** | Was not in the room | Undefined terms, a metric with no card, a chart with no denominator, a conclusion that does not follow from the numbers shown |
| **Accountant** | Asks what it is worth | Whether the effect, at the low end of its interval, justifies the cost of keeping the feature |

## The brief each reviewer gets

> Here is an analysis and the decision it will drive: `<decision>`. Hold this position: `<lens>`. Try to break it from that position only.
>
> Report each finding with a title, where it is, the evidence, and how it could change the decision. Evidence is one of: a number you recomputed and how, a definition quoted from the artifact that contradicts another part of it, or a row or event that shows the problem.
>
> Leave out anything you cannot point at. That covers style, preference, and worries with no evidence. No findings is a valid result.

## Verify, then merge

Rerun or reread what each finding cites. Keep it when the evidence shows the problem and the problem could change the decision. Drop the rest and count them.

Merge by root cause. A statistician who finds an inflated count and a data engineer who finds a double fire have found one thing.

## Output

```
DECISION   what this analysis will drive
FINDINGS   for each: title · where · evidence · how it could change the
           decision · which lenses found it
DROPPED    per lens: how many, and why
```

Say "no verified findings" when none survive. Then stop.
