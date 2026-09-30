# Super Lotto #1755 prospective experiment

Frozen **2026-09-30T00:51:17 UTC** (19:51 Jamaica), before the 20:30 Jamaica draw (01:30 UTC). Freeze commit `ef94b7b9`; V1 pool committed before Jev at `7edb0dc`. Cutoff #1754 (03 04 21 23 31 + SB8, appended as one ordinary observation). No #1755 information was used and no other #1755 prediction was inspected.

| Ticket | Numbers |
|---|---|
| 1 V1 Science (SL10: D_trend mains, S_gap SB) | **01 · 02 · 18 · 34 · 35 + SB 2** |
| 2 P0 Coverage 1 | **06 · 11 · 12 · 22 · 23 + SB 3** |
| 3 P0 Coverage 2 | **07 · 17 · 18 · 24 · 25 + SB 7** |

## V1 (unchanged)
- 20 candidates; no main or SB model passes the V1 gate. **No validated edge.**
- One production Jev call (jev-1.13.0, 161 questions): Choice for SL10 0.01, confidence 0.4; Jev preferred SL04 (0.44), which the no-edge rule does not use.
- The predeclared seeded uniform no-edge rule gives index 9 → SL10. This is the same ticket as #1754 (D_trend's top ticket and S_gap's overdue SB2 were unchanged after #1754).

## P0 (frozen protocol `5cce8a37`; not V2)
- Top 12 pool 01 02 06 07 11 12 17 18 22 23 24 25 (non-evidential ordering: every credibility weight is 0). All 792 combinations enumerated (`p0/universe_scores.csv`).
- Coverage objective with ≤1 shared main; SB rule C gives the next two SBs in P0's frozen order that differ from V1's SB2 → SB3, SB7.
- Pairwise main overlap {'1-2': 0, '1-3': 1, '2-3': 0}; 14 distinct mains; 3 distinct SBs.
- Historical gate **FAIL**: the portfolio is a coverage experiment, not a demonstrated predictive edge.

## Post-freeze research (changed nothing)
- **Jev audit** (1 call): robustness T1/T2/T3 0.09/0.13/0.13 of 4; chance/overfit 0.95/0.94/0.94; weak-model dependence 0.98/0.97/0.97; concentration 0.94/0.88/0.90; fragility 0.39/0.28/0.71. Portfolio: edge 0.05, robustness 0.39/4, coverage 2.94/4. These are evidence judgments, not winning probabilities.
- **Jev stability** (5 replicates of the byte-identical request): top choice SL04 in 4/5 (one replicate chose SL11); mean pairwise Spearman 0.938 (min 0.872); top-3 overlap 2.67/3; confidence 0.36–0.52. Aggregation would change the V1 ticket: **NO** (no-edge rule).
- **Random control** (seed 2026093061, research only, not a recommendation): 03 · 04 · 13 · 22 · 26 + SB 4 / 02 · 03 · 20 · 23 · 31 + SB 2 / 09 · 10 · 14 · 29 · 30 + SB 3.
