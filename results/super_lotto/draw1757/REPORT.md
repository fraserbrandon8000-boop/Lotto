# Super Lotto #1757 prospective experiment (Tuesday 2026-10-06)

Frozen **2026-10-06T21:36:16 UTC** (16:36 Jamaica), about 3 h 54 min before the 20:30 Jamaica draw (2026-10-07T01:30Z). Freeze commit `dd2b47eb`; the V1 pool was committed before Jev at `c19bada`. Cutoff #1756 (05 07 15 29 32 + SB3), appended as one ordinary observation. No V1/P0 rule, weight, seed, pool size, objective or SB rule was changed. No other #1757 prediction was inspected. Pre-draw check: clock 16:34 Jamaica; official result hosts unreachable from this environment; web search found no #1757 result.

| Ticket | Numbers |
|---|---|
| 1 V1 Science (SL10: D_trend mains, S_gap SB) | **01 · 02 · 11 · 15 · 22 + SB 2** |
| 2 P0 Coverage 1 | **06 · 12 · 18 · 23 · 24 + SB 3** |
| 3 P0 Coverage 2 | **01 · 12 · 17 · 18 · 29 + SB 7** |

## V1 (unchanged)
- 20 candidates frozen 2026-10-06T21:35:24 UTC (candidates.json sha256 `01a698e8940083e0…`); no main or SB generator passes the V1 gate. **No validated edge.**
- One production Jev HTTP call (jev-1.13.0, 161 questions; request `6530a93640078829…`, response `956b96462b10a11a…`). The caller's strict in-line check rejected Scores at exactly the 0.03 rounding boundary (SL09/SL14/SL20 stability). As in #1754 and #1756 the first and only response was validated offline by V1's inclusive 0.03 boundary rule, with no response edit and no retry.
- Selection: predeclared seeded uniform no-edge rule → SL10. Jev Choice for SL10 0.01, overall confidence 0.78. Jev's favourite was SL19 (0.80). Jev plays no role under the no-edge rule.
- 15 appears in SL10 because D_trend ranks it highly after two recent wins. That is the unchanged generator, not a repeat rule.

## P0 (frozen protocol `5cce8a37`; not V2)
- Top-12 pool 01 02 06 11 12 15 17 18 22 23 24 29 (equal-weight convention; every credibility 0). All 792 combinations enumerated and scored (`p0/universe_scores.csv`).
- Ticket 2 overlap limit 1; ticket 3 limit relaxed by the frozen rule to 2 (≤1 infeasible). Pairwise main overlap {'1-2': 0, '1-3': 1, '2-3': 2}; 12 distinct mains (the whole pool); SBs 2, 3, 7 (rule C; P0 SB order 3 7 5 4 6 1 8 9 2 10).
- Ticket 3's mains equal #1756 ticket 3's mains. That is the same frozen deterministic construction on a nearly unchanged pool (one pool number changed: 09 → 15), not a manual choice.
- Historical gate **FAIL**. P0 is a coverage experiment with no demonstrated predictive edge (see `forensic_1756/REPORT.md` §6: the P0 discovery order has no demonstrated predictive value).

## Post-freeze research (changed nothing; commit `8d0d18c`)
- **P0 Jev audit** (one call): robustness T1/T2/T3 0.10/0.15/0.11 of 4; overfit 0.95/0.94/0.95; weak-model dependence 0.98/0.97/0.98; fragility 0.39/0.41/0.66; portfolio robustness 0.36; portfolio edge 0.04; portfolio overfit 0.95; portfolio concentration 0.94; portfolio coverage 2.78. Evidence judgments, not winning probabilities.
- **Jev stability** (5 byte-identical replicates): production SL19 0.80; replicates 5/5 SL19; mean pairwise Spearman 0.979 (min 0.944); top-3 overlap 3.00/3; confidence 0.77–0.8. Aggregation would change the V1 ticket: **NO** (no-edge rule).
- **Random control** (seed 2026093061; research only): 03 · 04 · 13 · 22 · 26 + SB 4 / 02 · 03 · 20 · 23 · 31 + SB 2 / 09 · 10 · 14 · 29 · 30 + SB 3.
- **P1 shadow:** none. 144 research variants in one Holm family; none passes (`p1_research/REPORT.md`).
