# P0 shadow holdout: #2341 (descriptive only)

This is the frozen P0 protocol (commit `72e1c075`) applied to the pre-draw #2341 state (cutoff #2340), with the frozen #2341 V1 Science ticket as ticket 1. The portfolio was constructed and hashed (`CONSTRUCTED_BEFORE_SCORING.sha256`) before it was scored. **P0 was not retuned after scoring.**

Discovery pool (Top 15, frozen weights): 13 04 24 02 01 14 10 07 12 18 31 08 09 22 38. All 5,005 combinations were enumerated (`universe_scores.csv`).

| Ticket | Numbers | Matches vs 01 04 06 22 33 38 |
|---|---|---|
| 1 V1 Science | 01 · 04 · 13 · 14 · 24 · 38 | 3 (01 04 38) |
| 2 P0 Coverage | 02 · 08 · 09 · 10 · 12 · 31 | 0 |
| 3 P0 Coverage | 02 · 07 · 13 · 18 · 22 · 24 | 1 (22) |

- Portfolio best: 3. Total matches: 4.
- Unique winners covered across the 3 tickets: 01, 04, 22, 38 (4). For 15 numbers, 2.37 is expected at random.
- Winners outside the discovery pool: 06, 33.
- Pairwise overlap: 1–2 = 0, 1–3 = 2, 2–3 = 1. Unique numbers: 15, the whole pool.
- The two challengers together scored 1 match, against 1.89 expected. P(≥1 under the null) = 0.89, so they did slightly worse than random.

**Did P0 outperform the V1-only ticket on #2341?** Not on the best ticket: 3 vs 3, and the V1 ticket is the best ticket either way. The challengers added 1 match and one more winner covered. This is one draw, it is descriptive only, and P0's historical gate is FAIL.
