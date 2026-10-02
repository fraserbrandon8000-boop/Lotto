# Super Lotto #1756 prospective experiment (Friday 2026-10-02)

Frozen **2026-10-02T17:22:36 UTC** (12:22 Jamaica), about 8 hours before the 20:30 Jamaica draw (2026-10-03T01:30Z). Freeze commit `3fc61ca1`; the V1 pool was committed before Jev at `1bcb011`. Cutoff #1755 (03 11 15 21 33 + SB1), appended as one ordinary observation. The frozen V1/P0 rules were not changed by #1755. No other #1756 prediction was inspected.

| Ticket | Numbers |
|---|---|
| 1 V1 Science (SL10: D_trend mains, S_gap SB) | **01 · 06 · 11 · 18 · 22 + SB 2** |
| 2 P0 Coverage 1 | **02 · 09 · 12 · 23 · 24 + SB 7** |
| 3 P0 Coverage 2 | **01 · 12 · 17 · 18 · 29 + SB 3** |

## V1 (unchanged)
- 20 candidates; no main or SB model passes the V1 gate. **No validated edge.**
- One production Jev HTTP call (jev-1.13.0, 161 questions). The caller's strict in-line check rejected two Scores whose rounded value differs from the probability-weighted mean by exactly 0.03 (SL08/SL09 stability). As in #1754, the first and only response was validated offline by V1's inclusive 0.03 boundary rule (`validate_super_v1_response.mjs`), with no response modification and no network retry (response SHA-256 `d917ef03775f4cd0…` unchanged).
- Selection: predeclared seeded uniform no-edge rule → SL10. Jev Choice for SL10 0.5 (Jev's production favourite), confidence 0.46. Jev plays no role under the no-edge rule.

## P0 (frozen protocol `5cce8a37`; not V2)
- Top 12 pool 01 02 06 09 11 12 17 18 22 23 24 29 (equal-weight convention; every credibility is 0). All 792 combinations enumerated (`p0/universe_scores.csv`).
- All five V1 mains were inside the pool, so after ticket 2 (≤1 shared main) the frozen rule relaxed ticket 3's limit to ≤2 (infeasible at ≤1).
- Pairwise main overlap {'1-2': 0, '1-3': 2, '2-3': 1}; 12 distinct mains (the whole pool); SBs 2, 7, 3 (rule C; P0 SB order 7 3 5 4 6 1 8 9 2 10).
- Historical gate **FAIL**. The Super Lotto P0 portfolio is a coverage experiment, not a demonstrated predictive edge.

## Post-freeze research (changed nothing)
- **Jev audit:** robustness T1/T2/T3 0.09/0.13/0.11 of 4; chance/overfit 0.95/0.95/0.94; weak-model dependence 0.98/0.97/0.97; fragility 0.39/0.39/0.73; portfolio edge 0.04, coverage 2.58/4. Evidence judgments, not winning probabilities.
- **Jev stability** (5 byte-identical replicates): production SL10 0.50 / replicate_1 SL19 0.58 / replicate_2 SL19 0.56 / replicate_3 SL19 0.64 / replicate_4 SL19 0.54 / replicate_5 SL19 0.50. Production favourite SL10, but **0/5** replicates agreed (all chose SL19); mean pairwise Spearman 0.955 (min 0.924); top-3 overlap 2.67/3; confidence 0.46–0.61. The first-response favourite is unstable when two candidates are close. **Aggregation would change the V1 ticket: NO** (no-edge rule).
- **Random control** (seed 2026093061; research only, not recommended): 03 · 04 · 13 · 22 · 26 + SB 4 / 02 · 03 · 20 · 23 · 31 + SB 2 / 09 · 10 · 14 · 29 · 30 + SB 3. It is identical to the #1755 control because the frozen protocol fixes this seed (a constant control portfolio is a valid random baseline; draws are independent).
