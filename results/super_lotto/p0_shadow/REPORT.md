# Super Lotto P0: SHADOW HOLDOUT on #1754

**This is a shadow holdout, not prospective evidence.** The frozen protocol (commit `5cce8a37`) was applied to the pre-draw #1754 state (cutoff #1753), with the frozen #1754 V1 Science ticket as ticket 1. The portfolio was constructed and hashed (`CONSTRUCTED_BEFORE_SCORING.sha256`) before it was scored. P0 was not retuned after scoring.

- Main pool (Top 12; non-evidential ordering because every credibility is 0): 01 02 04 06 07 11 12 18 22 23 24 34.
- All 792 combinations were enumerated (`universe_scores.csv`).
- P0 Super Ball order: 5 3 7 4 6 1 8 2 9 10 (rule C).

| Ticket | Mains | SB | vs 03 04 21 23 31 + SB8 |
|---|---|---|---|
| 1 V1 Science | 01 · 02 · 18 · 34 · 35 | 2 | 0/5, SB miss |
| 2 P0 Coverage | 04 · 06 · 11 · 12 · 22 | 5 | 1/5 (04), SB miss |
| 3 P0 Coverage | 06 · 07 · 18 · 23 · 24 | 3 | 1/5 (23), SB miss |

- Portfolio best: 1/5. Total main matches: 2.
- No SB hit. SB8 was 7th in the P0 SB order.
- Unique winners covered: 04, 23. For 13 numbers, 1.86 are expected at random. Winners outside the pool: 03, 21, 31.
- Pairwise main overlap: 1–2 = 0, 1–3 = 1, 2–3 = 1. 13 unique mains, 3 distinct SBs.
- Challenger main matches: 2 vs 1.43 expected. P(≥2 under the null) = 0.43.

**Did P0 outperform V1-only on #1754?** Descriptively, yes on mains: the best ticket was 1/5 against V1's 0/5, and the challengers added 04 and 23. There was no SB gain. This is one draw, it is descriptive only, and P0's historical gate is FAIL.
