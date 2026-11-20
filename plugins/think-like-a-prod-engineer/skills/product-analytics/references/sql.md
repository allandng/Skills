# The same numbers in SQL

Two queries that return the same counts as `funnel.py` and `retention.py`. Both were run against the scripts on the sample data and matched exactly, including the users left out as too recent.

They are written to move between warehouses. Time is converted to epoch seconds once, in the first block, and everything after is integer arithmetic. **That first conversion is the only line to change.** As written it is SQLite. Other engines:

| Engine | Replace the `strftime` expression with |
|---|---|
| PostgreSQL | `CAST(EXTRACT(EPOCH FROM timestamp) AS BIGINT)` |
| BigQuery | `UNIX_SECONDS(timestamp)` |
| ClickHouse, PostHog SQL | `toUnixTimestamp(timestamp)` |
| Snowflake | `DATE_PART(EPOCH_SECOND, timestamp)` |

Only the SQLite form was executed here. Check the others against the script on a small export before relying on them.

## Funnel

Three ordered steps, each within 7 days of entering. Returns the number who entered with a full window, and the number reaching steps 2 and 3. Add a block per extra step.

```sql
WITH ev AS (
  SELECT user_id, event,
         CAST(strftime('%s', timestamp) AS INTEGER) AS ts
  FROM events
),
bounds AS (
  SELECT MAX(ts) AS data_end, 7 * 86400 AS win FROM ev
),
s1 AS (
  SELECT user_id, MIN(ts) AS t1
  FROM ev WHERE event = 'signup_completed'
  GROUP BY user_id
),
entered AS (
  SELECT s1.user_id, s1.t1
  FROM s1 CROSS JOIN bounds
  WHERE s1.t1 <= bounds.data_end - bounds.win
),
s2 AS (
  SELECT e.user_id, e.t1, MIN(x.ts) AS t2
  FROM entered e
  CROSS JOIN bounds
  JOIN ev x ON x.user_id = e.user_id
           AND x.event = 'profile_completed'
           AND x.ts >= e.t1
           AND x.ts <= e.t1 + bounds.win
  GROUP BY e.user_id, e.t1
),
s3 AS (
  SELECT s.user_id, s.t1, MIN(x.ts) AS t3
  FROM s2 s
  CROSS JOIN bounds
  JOIN ev x ON x.user_id = s.user_id
           AND x.event = 'project_created'
           AND x.ts >= s.t2
           AND x.ts <= s.t1 + bounds.win
  GROUP BY s.user_id, s.t1
)
SELECT
  (SELECT COUNT(*) FROM entered) AS entered,
  (SELECT COUNT(*) FROM s2)      AS reached_step_2,
  (SELECT COUNT(*) FROM s3)      AS reached_step_3;
```

To segment, carry the property through from the first step and group by it at the end. Read the property at the entry event, as the script does.

## Retention

Users retained on day 28: at least one return event between 28 and 29 days after their own start. Only users for whom day 28 has fully passed.

```sql
WITH ev AS (
  SELECT user_id, event,
         CAST(strftime('%s', timestamp) AS INTEGER) AS ts
  FROM events
),
bounds AS (
  SELECT MAX(ts) AS data_end, 28 AS n, 86400 AS span FROM ev
),
starts AS (
  SELECT user_id, MIN(ts) AS t0
  FROM ev WHERE event = 'signup_completed'
  GROUP BY user_id
),
mature AS (
  SELECT s.user_id, s.t0
  FROM starts s CROSS JOIN bounds
  WHERE s.t0 + (bounds.n + 1) * bounds.span <= bounds.data_end
),
back AS (
  SELECT DISTINCT m.user_id
  FROM mature m
  CROSS JOIN bounds
  JOIN ev x ON x.user_id = m.user_id
           AND x.event = 'session_started'
           AND x.ts >= m.t0 + bounds.n * bounds.span
           AND x.ts <  m.t0 + (bounds.n + 1) * bounds.span
)
SELECT
  (SELECT COUNT(*) FROM mature) AS users_old_enough,
  (SELECT COUNT(*) FROM back)   AS retained;
```

For weekly retention set `span` to `7 * 86400` and `n` to the week number.

## Why the `mature` and `entered` blocks matter

They are the lines most often missing from a hand-written query, and the ones that change the answer. Without them, a user who signed up yesterday is counted as not retained on day 28, and recent cohorts look worse than old ones for no reason but their age. If a query and a chart disagree, check this first.

## Intervals

SQL gives counts. For the interval on a rate, use the Wilson score interval, which behaves at small n and near 0% or 100%. With `p = k / n` and `z = 1.96` for 95%:

```
centre = (p + z*z / (2n)) / (1 + z*z / n)
half   = z * sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z / n)
interval = centre - half  to  centre + half
```

The scripts compute it for you.
