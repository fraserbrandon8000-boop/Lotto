# Lotto #2342 forensic (research only)

Actual #2342 (2026-09-30, 8:25 PM Jamaica): **12 · 13 · 14 · 15 · 19 · 33**, bonus 21.

| Ticket | Numbers | Matches |
|---|---|---|
| V1 Science (C07, C_gap) | 05 · 11 · 16 · 24 · 27 · 34 | 0 |
| P0 Coverage 1 | 01 · 02 · 04 · 13 · 22 · 38 | 1 (13) |
| P0 Coverage 2 | 08 · 09 · 10 · 12 · 14 · 18 | 2 (12, 14) |

Only Lotto data was used. No Super Lotto file, result or protocol was read. No prior artifact was modified.

Scripts:
- `scripts/research/forensic_2342.py`: integrity, pool scoring, winner evidence, P0 pool audit, two-layer diagnosis, Jev follow-up, prospective record.
- `scripts/research/historical_2342.py`: cluster/consecutive tests, Top-N audit, recurring core, fixed-seed follow-up.
- `scripts/research/research_2342.py`: research challengers with Holm correction.

## 1. Integrity: all checks pass (`verification.json`)

- **Hashes.** Every hash embedded in `frozen.json` (V1 pool files, the Jev state/request/response/receipt, and the V1 code) matches exactly. So do the pool-freeze hashes, the P0 `p0_frozen.json` hashes, the P0 protocol hash and all six ledger entries for #2342.
- **Jev.** The receipt matches the state and request (compact-JSON sha256). The model was jev-1.13.0 and returned 113 answers. The frozen choice probability, confidence and preferred candidate equal the response.
- **Commit chronology (all 2026-09-29 UTC):**
  - pool fd3b724 02:40:11
  - Jev receipt 02:40:15
  - V1 6c03e6c 02:40:23
  - P0 685e35d 02:40:45
  - random control 4cf8063 02:41:16
  - P0 audit 425e3c8 02:42:47
  - stability f31d294 02:44:07

  The scheduled draw was 2026-10-01T01:25Z. **All tickets were frozen about 46.7 h before the draw.**
- **No later changes.** The pool files and tickets did not change after their freeze commits. The V1 code is unchanged since snapshot ba7c5a3. All research replicates came after the freeze.

## 2. V1 pool scored (`pool_scores.json`)

**Match distribution over the 20 candidates:**

| Matches | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| Candidates | 5 | 10 | 5 | 0 | 0 | 0 | 0 |

- **Best.** The best result was 2/6, shared by five candidates: C03, C04, C06, C15 and C20. C04 and C06 were ineligible under the ≤2-overlap rule.
- **V1-selected.** C07 (C_gap), 0/6. Under the no-edge fallback V1 takes the candidate at index 3 of the 16 eligible.
- **Jev-preferred.** C03 (A_long, 02 10 13 18 24 33), 2/6 (13, 33), with Jev Choice 0.71. It was also the favourite in all five replicates.
- **Threshold.** No candidate reached ≥3. The chance that any of 20 random tickets reaches ≥3 is 0.546, so this is unremarkable.
- **Jev vs outcome.** The Spearman correlation between Jev Choice and matches across the 16 eligible candidates is 0.47. That is one draw with many ties, so it is not evidence.
- **No hindsight promotion.** No candidate is promoted on the basis of this outcome.

## 3. Pre-draw evidence for the six winners (`winner_evidence.json`)

Ranks are out of 38, with exact-tie intervals in brackets. E_pairs was flat because no pair was retained after Holm. F_structure scores whole tickets, so it has no number rank.

| # | A_long | B_recent | C_gap | D_trend | G proxy | H | freq | last10/20/30 | gap (pctl) | trend | Top-12 families | P0 rank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 12 | 15 | 12 | 30 | 9 | 10 | 24 | 31 | 2/5/6 | 1 (0.40) | +0.10 | B, D | 9 |
| 13 | 13 [8-13] | 3 | 27 | 3 | 3 | 2 | 32 | 4/6/8 | 2 (0.42) | +0.175 | B, D | 2 |
| 14 | 18 | 8 | 28 | 13 | 13 | 4 | 28 | 1/4/8 | 1 (0.33) | +0.05 | B | 8 |
| 15 | 10 [8-13] | 14 | 13 | 33 | 17 | 22 | 32 | 1/3/6 | 6 (0.77) | −0.10 | A | 19 |
| 19 | 31 | 23 | 12 | 23 | 24 | 5 | 25 | 1/2/5 | 7 (0.71) | −0.025 | C | 22 |
| 33 | 4 | 24 | 34 | 14 | 14 | 19 | 35 | 1/3/4 | 0 (0.15) | +0.025 | A | 18 |

No winner had a Holm-retained pair partner. No number in the dataset has a significant frequency deviation (Holm p = 1.0).

## 4. P0 pool audit (exact frozen pool)

- **Frozen Top-15 pool:** 04 13 24 02 01 22 10 14 12 07 38 18 08 09 06.
- **Winners inside:** 12 (rank 9), 13 (rank 2) and 14 (rank 8).
- **Winners outside:** 33 (rank 18), 15 (rank 19) and 19 (rank 22).

| Missed | P0 rank | Highest support | Lowest support | Top-18 | Top-20 | Top-25 | Equal-weight rank | No-stability-factor rank |
|---|---|---|---|---|---|---|---|---|
| 15 | 19 | A_long 10 | D_trend 33 | no | yes | yes | 14 | 19 |
| 19 | 22 | C_gap 12 | A_long 31 | no | no | yes | 25 | 22 |
| 33 | 18 | A_long 4 | C_gap 34 | yes | yes | yes | 16 | 18 |

Why they were missed:
- **Families with weight.** P0 gives positive weight only to B_recent (0.0314) and D_trend (0.0238). A_long and C_gap have zero weight because their historical winner-percentile evidence was not positive in both halves. 15, 19 and 33 had their only support in A_long or C_gap, and were weak on B and D.
- **Shrinkage.** Shrinkage does not change the ordering, because every family has n = 130 and so all weights are scaled by the same factor.
- **Equal weighting.** Equal weighting would have put 15 inside the pool (rank 14). The equal-weights challenger fails historically, though: 204 observed vs 212.2 expected, and −0.17 per draw vs P0 (§12). This is a single-draw observation, not a reason to change anything.

**Discovery loss = 3 (15, 19, 33); construction loss = 0.**

## 5. Cluster / consecutive forensic (`historical_2342.json` → `cluster_consecutive`)

The exact null is computed over all 2,760,681 combinations. Under it:
- P(longest run ≥ 2) = 0.599
- P(≥ 3) = 0.078
- P(≥ 4) = 0.0067
- P(4 numbers within a 6-number window) = 0.055

#2342 had a 4-run (12–15) with 3 adjacent pairs. A 4-run occurs in about 1 draw in 149.

| Set | ≥2-run | ≥3-run | ≥4-run | dense-4 | n |
|---|---|---|---|---|---|
| Exact null | 0.599 | 0.078 | 0.0067 | 0.055 | 2.76M |
| Actual draws 2161–2342 | 0.505 | 0.066 | 0.016 | 0.049 | 182 |
| V1 candidate pools 2211–2342 | 0.619 | **0.031** | 0.004 | **0.022** | 2,640 |
| V1 fixed 4,096 source pool | 0.587 | 0.075 | 0.008 | 0.050 | 4,096 |
| V1 F_structure candidates | 1.000 | **0.000** | 0.000 | 0.000 | 396 |
| V1 fallback chain (reconstructed) | 0.652 | 0.068 | 0.008 | 0.053 | 132 |
| P0 pool universes (all 6-subsets) | 0.594 | 0.065 | 0.003 | 0.045 | 560,560 |
| P0 historical challengers (K=15) | 0.605 | 0.082 | 0.009 | 0.036 | 220 |

- **Actual draws vs null.** The draws match the exact null. All Holm p ≥ 0.06; the only nominal deviation is *fewer* 2-runs than expected (p = 0.012, Holm 0.062). The three 4-runs in 182 draws give p = 0.12.
- **V1 suppresses dense clusters in its candidate pool.** The candidate pool has 0.40× the null rate of ≥3-runs and 0.40× the rate of dense 4-spans.
  - The cause is F_structure. It scores −mean(z²) over 10 structure features, two of which are `adjacent_pairs` and `close_spacings_le2`. Every one of its 396 candidates has exactly one adjacent pair, and none has a 3-run.
  - At cutoff 2341, 4-run tickets averaged the 6th percentile of F, and the actual #2342 combination sat at the 12th percentile.
  - E_pairs (flat) and the fixed H filler contribute fixed tickets with no runs.
- **The final V1 ticket is not suppressed.** The fallback chain has 0.87× the null 3-run rate, because the fixed-seed index usually lands on non-F candidates.
- **P0 does not materially suppress.**
  - The struct weight is 0.0067, about 2.5% of T variance. 4-run combinations have a lower mean T rank (4,254 of 5,005).
  - However, the selected historical challengers carry 3-runs at 1.05× the null rate, because coverage dominates selection.
  - P0 pools hold 5.38 adjacent pairs on average, against 5.53 for random 15-subsets.
- **Causal test.** Among historical V1 candidates, those with ≥3-runs averaged 0.90 matches and the rest 0.95 (permutation p = 0.69). Under uniform draws, a fixed ticket's match distribution does not depend on its structure, so suppressing or favouring runs cannot change expected matches. A cluster rule could only help if real draws deviated from the run null, and they do not.

**No cluster rule is justified.** The `cluster_neutral_struct0` challenger also fails (§12).

## 6. Two-layer diagnosis (`two_layer_diagnosis.json`)

| A: winners in pool | B: reached the portfolio | C: lost before construction | D: lost during construction |
|---|---|---|---|
| 3 (12, 13, 14) | 3 (13 in T2; 12, 14 in T3) | 3 (15, 19, 33) | 0 |

- **Capture was ordinary.** Capturing 3 winners in a random Top-15 is ordinary: the expectation is 2.37, and P(≤3) = 0.85.
- **Counterfactual (no ticket built from the outcome).** Treat each of the 5,005 six-subsets of the frozen pool as the winning set and score the frozen portfolio against it:
  - mean best = 3.09
  - P(best ≥ 3) = 0.83, P(≥ 4) = 0.24, P(≥ 5) = 0.022
  - mean total = 5.2

  So the unchanged constructor converts a fully discovered draw reasonably well. But an all-six-in-pool event has probability 5,005 / 2,760,681 = 0.0018.

## 7. Top-N historical discovery audit (causal P0 ordering, targets 2231–2342, n = 112)

The orderings are identical to `p0_protocol/historical_origins.json` for 2231–2340 (verified).

| N | mean capture | random | excess | 95% block CI | halves | p (one-sided) | Holm | conf. 2303–2342 excess (p) |
|---|---|---|---|---|---|---|---|---|
| 10 | 1.554 | 1.579 | −0.025 | [−0.22, 0.16] | +0.05 / −0.10 | 0.62 | 1.00 | −0.05 (0.66) |
| 12 | 1.920 | 1.895 | +0.025 | [−0.15, 0.19] | +0.03 / +0.02 | 0.42 | 1.00 | +0.11 (0.29) |
| 15 | 2.509 | 2.368 | +0.141 | [−0.06, 0.33] | +0.08 / +0.20 | 0.098 | 0.59 | +0.38 (0.018; Holm 0.11) |
| 18 | 2.938 | 2.842 | +0.095 | [−0.12, 0.30] | −0.07 / +0.27 | 0.20 | 0.99 | +0.38 (0.020; Holm 0.11) |
| 20 | 3.196 | 3.158 | +0.039 | [−0.18, 0.24] | −0.09 / +0.16 | 0.38 | 1.00 | +0.27 (0.078) |
| 25 | 3.982 | 3.947 | +0.035 | [−0.23, 0.31] | −0.00 / +0.07 | 0.38 | 1.00 | +0.28 (0.059) |

- **Top-15 detail.** P(≥2..6) = 0.79 / 0.51 / 0.21 / 0.054 / 0, against random 0.78 / 0.44 / 0.15 / 0.027 / 0.002.
- **No pool size passes.** Pool size is not widened because of #2342.
- **#2342 capture.** It was 3 / 3 / 3 / 4 / 5 / 6 at N = 10 / 12 / 15 / 18 / 20 / 25.

## 8. Recurring core 01 04 13 24 38 (+ 12 14)

| Driver | Finding |
|---|---|
| Independent evidence | None. Every core number has frequency Holm p = 1.0. |
| Correlated models | B_recent~D_trend r = 0.48 and A_long~B_recent r = 0.58 (mean over 132 cutoffs). 13 is Top-12 in B 57% and D 41% of cutoffs (chance 32%). 24, 01 and 04 are Top-12 in A_long 92%, 74% and 68%. P0 uses B and D at every target (A in 50%, C and E never). |
| Construction | One fixed 4,096-combination candidate pool at every cutoff; consecutive pools share 14.1 of 20 tickets. 01 04 13 14 24 38 appears in 6 pools and 05 11 16 24 27 34 in 5. Fixed data-independent tickets: the H filler 05 07 14 21 33 38 is in all 132 pools (that is where 14 and 38 come from). E_pairs, when flat, gives 08 10 11 15 21 24, 01 05 08 12 26 34 and 06 08 15 17 19 38 (≥129 pools; source of 12). |
| Fixed seed | The index depends only on the eligible count (n = 13–16 → 3; n = 17–20 → 4). |
| Overlap rule | ≤2 overlap with the previous primary makes V1 alternate between two tickets: 01 04 13 14 24 38 (2339, 2341) and 05 11 16 24 27 34 (2340, 2342). 24 is in both. |
| Random filler | H_random is a fixed ticket, so it carries 14 and 38 every time. |
| Jev | Jev's preferred ticket contained 13 and 24 in all four runs, 2339–2342. |
| P0 | 38 was in the P0 pool at 85% of targets (chance 39%). The live #2342 T2 contains 01 04 13 38, from B/D-driven ordering, not from V1. |

## 9. Fixed-seed follow-up (V1 fallback chain, targets 2211–2342, n = 132, ≤2-overlap kept)

| Design | top-ID share | distinct IDs | lag-2 exact repeat | consecutive overlap | core rate | total matches | ≥3 |
|---|---|---|---|---|---|---|---|
| A fixed production seed | 0.477 | 5 | 0.123 | 0.73 | 0.231 | 112 | 7 |
| B per-draw seed | 0.091 | 20 | 0.046 | 0.89 | 0.215 | 133 | 6 |
| C uniform (2,000 streams; mean [95%]) | 0.088 [0.07–0.11] | 20 | 0.035 [0.01–0.07] | 0.93 [0.79–1.07] | 0.230 | 124.4 [106–143] | 4.8 [1–9] |
| D rotating index | 0.076 | 20 | 0.015 | 0.92 | 0.216 | 118 | 6 |

The null expectation is 125.05 total matches. The p(total ≥ observed) values are A 0.92, B 0.22 and D 0.78.

- **Effect of the fixed seed.** It concentrates ID recurrence and ticket repetition far outside the uniform range, but leaves matches inside the chance range.
- **No seed promoted.** The per-draw seed also fails the corrected gate (§12).

## 10. Jev follow-up

- **#2342.** The production call preferred C03 with confidence 0.68. All 5 identical replicates also preferred C03:
  - mean Spearman 0.997
  - confidence 0.65–0.75
  - first-valid = aggregate favourite.
- **Historical aggregation test.** A historical first-valid vs 3/5-call comparison is **not feasible**: it would need about 550 Jev calls on reconstructed states.
- **Effect on tickets.** Under the no-edge rule Jev cannot change the V1 ticket.
- **Verdict.** No evidence either way on whether aggregation beats first-valid.

## 11. Combined prospective record

**V1, #2339–#2342: 3, 0, 3, 0.**
- Total 6 against 3.79 expected; P(total ≥ 6) = 0.15.
- Two ≥3 events in 4: nominal p = 0.0085, Clopper–Pearson 95% for the ≥3 rate [0.068, 0.932]. This statistic was chosen after seeing the record, and the predeclared total-match test gives p = 0.15.
- The 3, 0, 3, 0 alternation is two tickets each played twice (§8), not a pattern.
- **Reconstructed production chain, 132 targets:** 112 matches vs 125.05 expected, and 7 ≥3 events vs 5.1 expected (p = 0.25).

**P0 live (#2342 only):**
- Best 2; portfolio total 3 vs 2.84 expected; P(best ≥ 2) = 0.61.
- The #2341 run was a shadow (best 3, total 4) and is not prospective.

**Fixed-seed random control (#2342, frozen before the draw):**
- Tickets 12 14 15 17 20 29 / 13 19 25 26 28 29 / 01 08 20 21 33 36 scored 3, 2 and 1: best 3, total 6.
- That beats the P0 portfolio's best 2 and total 3. It is one draw, so it supports no inference either way.

Nothing here indicates an edge.

## 12. Research challengers (`research_challengers.json`)

**Gate.** One Holm family of 19 challengers, evaluated on targets 2231–2342 with strict walk-forward. The P0 baseline reproduces `historical_origins.json` exactly. To pass, a challenger needs all of:
- Holm p < 0.05 vs the exact null
- block-bootstrap 95% lower bound of the excess > 0
- both halves > 0
- paired 95% lower bound vs the baseline > 0
- Holm p < 0.05 again with #2342 removed

**Baselines.** P0 baseline: 223 vs 212.2 (p = 0.19). V1 production chain: 112 vs 125.1 (p = 0.92).

| Challenger | obs | exp | p | Holm | vs baseline per draw |
|---|---|---|---|---|---|
| K18 / K20 / K25 | 227 / 228 / 226 | 212.2 | 0.10 / 0.09 / 0.12 | 1.0 | +0.04 / +0.05 / +0.03 |
| dynamic K | 209 | 212.2 | 0.61 | 1.0 | −0.13 |
| τ 0.05 / τ 0.20 / no shrinkage | 225 / 224 / 224 | 212.2 | 0.15 / 0.18 / 0.19 | 1.0 | +0.02 / +0.01 / +0.01 |
| equal weights | 204 | 212.2 | 0.73 | 1.0 | −0.17 |
| no stability factor | 224 | 212.2 | 0.17 | 1.0 | +0.01 |
| overlap ≤1 / ≤3 | 223 / 224 | 212.2 | 0.19 / 0.17 | 1.0 | 0.00 / +0.01 |
| cluster-neutral (struct 0) | 226 | 212.2 | 0.13 | 1.0 | +0.03 |
| exhaustive: top-2 standalone T / coverage-only / evidence-only | 197 / 228 / 196 | 212.2 | 0.83 / 0.10 / 0.88 | 1.0 | −0.23 / +0.05 / −0.24 |
| V1: per-draw seed / rotating index | 133 / 118 | 125.1 | 0.22 / 0.78 | 1.0 | +0.16 / +0.05 |
| V1: no repeated position / drop fixed data-independent candidates | 120 / 124 | 125.1 | 0.72 / 0.56 | 1.0 | +0.06 / +0.09 |
| Jev aggregation | not testable historically | | | | |

**NO LOTTO V2/P1 REFINEMENT IS JUSTIFIED.** No P1 challenger exists, so nothing is written to `p1_research/` or `p1_shadow_2343/`. P0 stays frozen.
