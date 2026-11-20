### Activation

**You own the definition of "this user got it". It is a hypothesis until an experiment says otherwise.**

1. Write the candidate first-value moments from what the product is for. Start from the user's job, not from the event list.
2. Run the early-behaviour analysis in the `product-analytics` skill (its retention script with `--candidates`), at the product's natural rhythm.
3. Read the table for behaviours that are common enough to matter, go with much higher retention, and are something the product could cause. A behaviour 2% of users do is not an activation metric.
4. Suspect each: is it a cause, or a marker of users who were going to stay anyway? Would nudging people into it change anything? Write the answer down.
5. Check the candidate by platform and by source. An activation definition that only works on web is a web definition.
6. Write the definition: the event sequence, the count, the window. "Created a project and invited one teammate within 3 days."
7. Record it in `docs/product/context.md` as a hypothesis, with the data and date behind it.
8. Design the test that would confirm it: a change that moves more users into the behaviour, with retention as the metric (**experiment**).

**Reply:** the candidates table with intervals, the chosen definition, why it might be a marker and not a cause, how it holds by platform and source, and the confirming experiment.
