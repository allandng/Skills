### Cleanup

**You own leaving no trace of the experiment in the product, the code or the data.**

1. Feature at 100% and stable: remove the flag from the code, then archive it. On mobile, wait until versions that read the flag are a negligible share, or keep the server answer fixed.
2. Delete the losing code path, its tests, its copy and its assets.
3. Mark events that no longer fire as deprecated in the tracking plan and in the analytics tool. The `tracking-plan` skill's comparison confirms nothing deprecated still fires.
4. Remove or relabel dashboards that chart removed events. A dashboard that silently reads zero is worse than none.
5. Rolled back: remove the feature's schema with expand, migrate, contract in reverse, after confirming no client reads it.
6. For features that are not earning their keep: read their usage and retention, write a deprecation plan with notice, a migration path and a removal date.
7. Re-run `scripts/vocab_check.py`. Dead names come back.

**Reply:** flags removed and archived, code deleted, events deprecated with the comparison result, dashboards changed, and any sunset plan with its dates.
