# Jamaica Lotto experimental decision report

**Conclusion: No detectable edge in this dataset.**

**Primary pick: 01 – 04 – 13 – 14 – 24 – 38 (C05)**

**Secondary pick: 02 – 06 – 08 – 12 – 18 – 25 (C03)**

These are disciplined diversified selections, not statistically superior tickets. Latest observed draw: #2338, 2026-09-16. Intended next draw: #2339 on September 19, 2026, provided it has not already occurred. This saved report is a fixed snapshot; refresh the archive before using it for a later draw.

No methodology passed the corrected confirmation edge gate. Seeded uniform selection among the candidates, then minimum-overlap diversification. No predictive superiority claimed. The picks share 0 numbers. Under the uniform model each ticket has a jackpot chance of 1 in 2,760,681; any two distinct tickets have combined probability 2/2,760,681.

## 1. Dataset audit

| Check | Result |
|---|---|
| Workbook found | Lotto-Draw-Dataset.xlsx; requested (1) variant not present |
| Original records | 167 |
| Original range | #2161–#2337; 2025-01-01–2026-09-12 |
| Source range | Lotto Draws!A6:J172 |
| Order | Strictly descending dates and IDs; analysis reverses to ascending |
| Missing IDs | 2252–2261 |
| Duplicate IDs / duplicate records | 0 / 0 |
| Missing cells / malformed dates | 0 / 0 |
| Invalid main / bonus numbers | 0 / 0 |
| Repeated main numbers / bonus-main overlap | 0 / 0 |
| Six main numbers present | All records |
| Valid range | Main and bonus 1–38; all observed bonus balls distinct from main balls |
| Unexpected weekdays | 0; Wednesday/Saturday |
| Source conflicts in fetched overlap | 0; #2262 and #2337 agree |
| Merged analysis records | 178; consecutive #2161–#2338 |
| Original unchanged | SHA-256 verified after analysis |

Original SHA-256: `5d55e059df0ca5cece2838a48a5ac9608625ad9941feadf35a3b481a0875641d`. Original source labels refer to an earlier workbook and two screenshots; most original rows have not been independently reverified against primary records. Auditing validity does not prove historical source accuracy.

## 2. Missing and new draws recovered

| Draw | Date | Main numbers | Bonus |
|---|---|---|---|
| 2252 | 2025-11-19 | 2, 10, 21, 24, 29, 32 | 23 |
| 2253 | 2025-11-22 | 7, 12, 15, 23, 29, 38 | 3 |
| 2254 | 2025-11-26 | 6, 16, 19, 22, 28, 33 | 1 |
| 2255 | 2025-11-29 | 1, 3, 5, 16, 22, 28 | 34 |
| 2256 | 2025-12-03 | 16, 17, 21, 24, 28, 32 | 19 |
| 2257 | 2025-12-06 | 1, 6, 8, 12, 29, 33 | 37 |
| 2258 | 2025-12-10 | 2, 6, 9, 13, 15, 18 | 3 |
| 2259 | 2025-12-13 | 9, 11, 18, 26, 33, 38 | 21 |
| 2260 | 2025-12-17 | 5, 7, 10, 15, 33, 34 | 16 |
| 2261 | 2025-12-20 | 11, 18, 19, 20, 30, 34 | 23 |
| 2338 | 2026-09-16 | 1, 3, 10, 13, 18, 29 | 17 |

Source: [Supreme Ventures official past-results page](https://supremeventures.com/past-results/). Its public JavaScript directs results requests to `https://test-results.supremeventures.com/public/game/5/from/{start}/to/{end}` with a ten-day limit. The host name contains “test”, but this is the feed used by the official public site, not an invented endpoint. Raw successful archive responses are retained in `data/official-YYYY-MM-DD.json`. Queries covered November 19–December 24, 2025 and September 12–19, 2026. Latest returned result was #2338; no #2339 was returned at retrieval. External additions are separate in `data/external_draws.json`; no guessed rows. Official overlap checks corroborated #2262 and #2337. The full original workbook was not overwritten.

[Official rules](https://supremeventures.com/game/lotto/) specify six numbers from 1–38, Wednesday/Saturday at 8:25 PM Jamaica time. Bonus is recorded separately and is excluded from all six-main-number match scores; payout/return-on-money modelling is outside this experiment.

## 3. Exact random baseline

For k matches: **P(M=k) = C(6,k) C(32,6−k) / C(38,6)**. Expected matches = **36/38 = 0.947368**.

| Matches | Probability | Percentage |
|---|---|---|
| 0 | 0.3282494428 | 32.824944% |
| 1 | 0.4376659237 | 43.766592% |
| 2 | 0.1953865731 | 19.538657% |
| 3 | 0.0359331629 | 3.593316% |
| 4 | 0.0026949872 | 0.269499% |
| 5 | 0.0000695481 | 0.006955% |
| 6 | 0.0000003622 | 0.000036% |

At least two matches occur naturally on 23.41% of random tickets; at least three on 3.87%. Across 128 trials, approximately 4.95 results with three or more matches are expected. Occasional two- or three-match tickets are not evidence of useful prediction.

## 4. Exploratory statistics and draw structure

Each of the 38 main numbers has expected full-history count **28.1053** in 178 draws. `number_statistics.csv` includes all requested rolling frequencies (100/50/30/20/10), EW frequency (half-life 20), counts, deviations, gap summaries, trend, short/long ratio and block volatility.

Current gap counts draws since the last appearance (zero if drawn most recently). Completed gaps count intervening absent draws; left/right censored gaps are excluded from completed-gap summaries. Longest observed absence includes boundary runs. Finite-window censoring is retained in the Monte Carlo gap test. Frequency volatility is the standard deviation of appearance rates in complete 10-draw blocks.

Most frequent numbers (descriptive only):

| Number | Count | Expected | Holm p |
|---|---|---|---|
| 18 | 38 | 28.105 | 1.000 |
| 8 | 37 | 28.105 | 1.000 |
| 38 | 35 | 28.105 | 1.000 |
| 24 | 34 | 28.105 | 1.000 |
| 33 | 34 | 28.105 | 1.000 |
| 1 | 32 | 28.105 | 1.000 |
| 10 | 32 | 28.105 | 1.000 |
| 15 | 32 | 28.105 | 1.000 |

Draw-level sum, mean, median, extrema, range, parity, low/high (1–19/20–38), bands (1–10/11–20/21–30/31–38), adjacency, spacing, repeated numbers from preceding 1/2/3/5 draws, last digits and clustering (sorted gaps ≤2) are in `draw_structure.csv`.

| Property | Observed mean | Random mean (200,000 tickets) |
|---|---|---|
| sum | 116.326 | 116.934 |
| median | 19.022 | 19.498 |
| minimum | 5.646 | 5.564 |
| maximum | 33.736 | 33.402 |
| range | 28.090 | 27.838 |
| odd_count | 2.888 | 3.003 |
| low_count | 3.079 | 3.000 |
| adjacent_pairs | 0.685 | 0.789 |
| largest_spacing | 11.910 | 12.044 |
| close_spacings_le2 | 1.371 | 1.473 |

Expected counts per draw in the four bands are 1.579/1.579/1.579/1.263, reflecting unequal band sizes. Last digits 0 and 9 each cover three numbers; the other digits cover four. Common sums/parities occupy more combinations, but no particular combination gains probability because it looks typical. The structural model tests the hypothesis rather than assuming it.

## 5. Relationships and randomness tests

All 703 pairs are enumerated. Expected count per pair = 178×30/(38×37) = **3.798**. Pair lift relative to uniform and empirical marginal rates, exact enrichment p-values, Holm/BH correction, recency, last-50/100 and half-period counts are saved.

| Pair test summary | Count |
|---|---|
| Raw pair p < .05 | 27 |
| Pair Holm p < .05 | 0 |
| Pair BH q < .05 | 0 |
| Marginal number Holm p < .05 | 0 |
| Ordered transition Holm p < .05 | 0 |

All 8,436 triples are counted, but each has expected count only about 0.422. Triple findings are descriptive; this sample cannot sustain reliable triple-specific predictive estimation. The 1,444 ordered previous-number → next-number relationships use exact conditional hypergeometric enrichment tests (Fisher upper tail) and Holm correction. Number-level lag-1/2/3/5 correlations are also saved.

10,000 synthetic histories, each 178 independent uniform six-without-replacement draws, calibrate the following diagnostics. Simulations preserve within-draw dependence and finite-window gap censoring. P-values include the +1 Monte Carlo correction; resolution is 1/10,001. Holm correction covers these 14 tests.

| Test | Observed | Null mean | MC p | Holm p |
|---|---|---|---|---|
| marginal_dispersion | 26.955 | 31.950 | 0.7404 | 1.0000 |
| max_number_deviation | 9.895 | 11.693 | 0.8582 | 1.0000 |
| pair_dispersion | 661.219 | 688.434 | 0.7048 | 1.0000 |
| max_pair_count | 11.000 | 11.062 | 0.6849 | 1.0000 |
| max_abs_serial_lags1_3 | 0.246 | 0.220 | 0.2154 | 1.0000 |
| complete_gap_CDF_distance | 0.028 | 0.024 | 0.2432 | 1.0000 |
| repeat_distribution | 0.952 | 6.717 | 0.9403 | 1.0000 |
| mean_repeats | 0.938 | 0.947 | 0.9221 | 1.0000 |
| mean_sum | 116.326 | 116.979 | 0.7401 | 1.0000 |
| sum_sd | 26.020 | 24.888 | 0.3590 | 1.0000 |
| mean_odd | 2.888 | 3.002 | 0.1920 | 1.0000 |
| mean_adjacent_pairs | 0.685 | 0.789 | 0.0784 | 1.0000 |
| mean_range | 28.090 | 27.856 | 0.5789 | 1.0000 |
| mean_clustering | 1.371 | 1.472 | 0.1450 | 1.0000 |

No global test provides statistically meaningful or even nominal p<.05 evidence here. These results are consistent with randomness, not proof that every possible dependence is absent. Pair simulations assess both aggregate dispersion and the largest observed pair count; rare-cell Pearson statistics are calibrated by simulation rather than a naive chi-square reference.

## 6. Models and strict walk-forward design

| Model | Definition |
|---|---|
| A_long | Smoothed full-history number frequency |
| B_recent | Half last-30 rate + half EW rate, half-life 20 |
| C_gap | Current absence/gap; explicit overdue hypothesis |
| D_trend | Last-20 appearance rate minus preceding-40 |
| E_pairs | Training-only Holm-significant pair lift; uniform fallback if none |
| F_structure | Smallest standardized distance from training structure |
| G_ensemble | A–F objective combination with earlier-OOS-learned weights |
| H_random | Separate uniformly random six-number control |

Each historical origin starts with at least 50 past draws. A–G optimize their combination-level objective over a common seeded pool of 512 uniform combinations; H is independently sampled. Each prediction, training cutoff, realized outcome and ensemble weight is saved in `walk_forward_predictions.json`. Features, normalization, significance thresholds and ensemble history use the training prefix only.

There are **128 out-of-sample origins**, split into 88 development and the last 40 confirmation draws. G uses positive earlier-OOS excess over the baseline, shrunk with 20 baseline pseudo-draws; if all excesses vanish it uses equal weights. Its weights are frozen before the confirmation period, while model features update causally. No test-period winner is chosen merely on raw score.

The protocol was written before calculating performance and before Jev. This remains a retrospective experiment, not a prospectively preregistered trial. Candidate variants and the Jev decision layer are not backtested systems. The final candidate search uses 4,096 combinations to obtain diversity, versus 512 per historical origin; it does not inherit validated performance automatically.

## 7. Walk-forward results

Random expected matches: **0.947368 per draw** in every table.

| Model | All 128 mean | All total | All Holm p | Confirm 40 mean | 95% block CI | Confirm Holm p |
|---|---|---|---|---|---|---|
| A_long | 1.023 | 131 | 0.976 | 1.125 | 0.925–1.350 | 0.846 |
| B_recent | 1.047 | 134 | 0.682 | 0.975 | 0.725–1.225 | 1.000 |
| C_gap | 0.891 | 114 | 1.000 | 0.750 | 0.550–0.950 | 1.000 |
| D_trend | 1.055 | 135 | 0.645 | 0.975 | 0.800–1.150 | 1.000 |
| E_pairs | 0.961 | 123 | 1.000 | 1.000 | 0.775–1.200 | 1.000 |
| F_structure | 0.969 | 124 | 1.000 | 0.950 | 0.700–1.200 | 1.000 |
| G_ensemble | 0.992 | 127 | 1.000 | 0.875 | 0.650–1.125 | 1.000 |
| H_random | 0.977 | 125 | 1.000 | 0.875 | 0.625–1.150 | 1.000 |

The full-period raw leader is D_trend; the confirmation raw leader is A_long. Qualifying methodologies: none. Ensemble confirmation mean: 0.875 versus random 0.947. Raw rank alone does not establish an edge.

Confirmation match distributions:

| Model | 0 | 1 | 2 | 3 | 4+ | Best | Older 20 mean | Recent 20 mean |
|---|---|---|---|---|---|---|---|---|
| A_long | 20.0% | 52.5% | 25.0% | 0.0% | 2.5% | 4 | 1.050 | 1.200 |
| B_recent | 25.0% | 52.5% | 22.5% | 0.0% | 0.0% | 2 | 0.750 | 1.200 |
| C_gap | 40.0% | 45.0% | 15.0% | 0.0% | 0.0% | 2 | 0.700 | 0.800 |
| D_trend | 25.0% | 52.5% | 22.5% | 0.0% | 0.0% | 2 | 1.100 | 0.850 |
| E_pairs | 30.0% | 45.0% | 20.0% | 5.0% | 0.0% | 3 | 1.150 | 0.850 |
| F_structure | 35.0% | 40.0% | 20.0% | 5.0% | 0.0% | 3 | 0.950 | 0.950 |
| G_ensemble | 35.0% | 45.0% | 17.5% | 2.5% | 0.0% | 3 | 0.800 | 0.950 |
| H_random | 37.5% | 45.0% | 10.0% | 7.5% | 0.0% | 3 | 1.050 | 0.700 |

Full period ranking diagnostics are in `model_performance.csv`: average precision over all 38 numbers and recall@12. Random-ranking expectations are AP ≈ 0.2314, recall@12 = 0.3158. Structure has no unique individual-number ranking; pair rankings are omitted when the pair objective is flat. G’s individual ranking is a marginal proxy and excludes the structure component. Ranking metrics are descriptive, not additional validated edges.

Exact one-sided p-values convolve the hypergeometric PMF once per target draw. This is valid under the independent uniform null even for a causally adaptive ticket: conditional on the past, every valid ticket has the same match law. A separate 20,000-replicate random-control simulation cross-checks means. CIs include ordinary bootstrap and circular five-draw block bootstrap (10,000 replicates); the edge gate uses the block lower bound. Small samples and overlapping model histories limit precision.

## 8. Sensitivity and ensemble stability

Fourteen reruns change windows (20/40), decay (10/40), trend spans (10/30), pair correction thresholds (.01/.10), training warmup (40/60), history cap (100), ensemble weights (equal/more shrinkage), or the pool seed. Baseline definitions are not replaced by the best sensitivity result.

| Model | Confirmation mean range | Smallest Holm p | Mean ticket overlap range |
|---|---|---|---|
| A_long | 0.900–1.125 | 0.846 | 2.55–6.00 |
| B_recent | 0.775–1.025 | 1.000 | 2.38–6.00 |
| C_gap | 0.750–1.050 | 1.000 | 2.62–6.00 |
| D_trend | 0.900–1.000 | 1.000 | 1.55–6.00 |
| E_pairs | 0.875–1.000 | 1.000 | 0.97–6.00 |
| F_structure | 0.850–0.950 | 1.000 | 1.05–6.00 |
| G_ensemble | 0.850–1.025 | 1.000 | 2.20–6.00 |
| H_random | 0.850–0.875 | 1.000 | 0.93–6.00 |

No sensitivity run produces a corrected confirmation edge. Low ticket overlap across some perturbations shows that exact combinations can move substantially even when aggregate performance is similar. Candidate-specific perturbed ranks and top-quartile fractions are saved. Neutral ranks for uniform fallbacks are not counted as stability. An original-only source ablation for A/B/D is saved separately; gaps prevent interpreting its omitted records as consecutive observations. That ablation is exploratory and is not used to select a model.

The final choice under the no-edge branch is governed by a seed and coverage; it is not a stable statistical optimum. Changed candidate-generation assumptions can change the ticket, which is expected when no winning-probability difference is established.

## 9. Candidate shortlist and Jev Choice

Twenty tickets were generated with no more than three shared numbers between any two. Evidence profiles include individual scores, contributing models, ensemble score, frequency/gap/trend/pair/structure summaries, overlap, method support, sensitivity and counterevidence. These are exploratory combinations, not 20 separately validated strategies.

| ID | Numbers | Generator | Jev Choice probability | Robustness /4 | Evidence quality /4 |
|---|---|---|---|---|---|
| C01 | 01 – 08 – 15 – 18 – 24 – 25 | A_long | 2.0% | 0.10 | 0.03 |
| C02 | 02 – 10 – 13 – 18 – 24 – 33 | A_long | 90.0% | 0.10 | 0.03 |
| C03 | 02 – 06 – 08 – 12 – 18 – 25 | A_long | 0.0% | 0.02 | 0.02 |
| C04 | 01 – 02 – 09 – 22 – 24 – 38 | B_recent | 0.0% | 0.03 | 0.01 |
| C05 | 01 – 04 – 13 – 14 – 24 – 38 | B_recent | 0.0% | 0.04 | 0.02 |
| C06 | 01 – 02 – 04 – 10 – 13 – 35 | B_recent | 0.0% | 0.05 | 0.01 |
| C07 | 16 – 23 – 28 – 33 – 34 – 38 | C_gap | 0.0% | 0.00 | 0.00 |
| C08 | 05 – 11 – 16 – 24 – 27 – 34 | C_gap | 0.0% | 0.00 | 0.00 |
| C09 | 05 – 11 – 14 – 16 – 23 – 32 | C_gap | 0.0% | 0.00 | 0.00 |
| C10 | 04 – 07 – 12 – 13 – 19 – 24 | D_trend | 0.0% | 0.05 | 0.01 |
| C11 | 04 – 07 – 10 – 22 – 24 – 31 | D_trend | 5.0% | 0.07 | 0.02 |
| C12 | 02 – 03 – 04 – 07 – 10 – 15 | D_trend | 0.0% | 0.02 | 0.01 |
| C13 | 01 – 05 – 08 – 12 – 26 – 34 | E_pairs | 3.0% | 0.00 | 0.00 |
| C14 | 08 – 10 – 11 – 15 – 21 – 24 | E_pairs | 0.0% | 0.01 | 0.00 |
| C15 | 06 – 08 – 15 – 17 – 19 – 38 | E_pairs | 0.0% | 0.01 | 0.00 |
| C16 | 06 – 07 – 13 – 24 – 32 – 35 | F_structure | 0.0% | 0.01 | 0.00 |
| C17 | 04 – 16 – 17 – 21 – 26 – 33 | F_structure | 0.0% | 0.00 | 0.00 |
| C18 | 07 – 08 – 12 – 23 – 29 – 34 | F_structure | 0.0% | 0.01 | 0.00 |
| C19 | 12 – 13 – 15 – 18 – 22 – 24 | G_ensemble | 0.0% | 0.07 | 0.01 |
| C20 | 05 – 07 – 14 – 21 – 33 – 38 | H_random | 0.0% | 0.00 | 0.00 |

Jev model: **jev-1.13.0**, requested through `jev-latest`. One request answered **141 questions**: 1 Choice, 60 Scores, 80 Nouls. Usage: **43,240 input / 2,900 output tokens**. Choice winner: **C02**, probability **0.90**, confidence **0.89**.

The forced Choice result is highly concentrated even though the same response gives almost no support for a predictive advantage. This is a limitation of using a forced qualitative choice in statistically indistinguishable cases. **0.90 is not a 90% chance of winning and not a calibrated probability of a lottery edge.** The deterministic gate prevents this preference from overriding negative statistical evidence.

## 10. Jev Scores and Noul risk checks

Robustness levels range from no support beyond random, through weak/fragile and repeatable-but-uncertain support, to corrected multi-test and unusually robust independently replicated support. Consensus counts independently validated approaches, not correlated unvalidated agreement. Evidence quality scores the quality of positive evidence for an advantage; a rigorous negative experiment is not positive evidence. Exact descriptions are saved in `jev_request.json`.

| ID | Consensus /4 | Overfit/chance Noul | Stable Noul | Stronger than random Noul | Single-model Noul |
|---|---|---|---|---|---|
| C01 | 0.00 | 0.95 | 0.37 | 0.04 | 0.88 |
| C02 | 0.00 | 0.95 | 0.45 | 0.05 | 0.49 |
| C03 | 0.00 | 0.96 | 0.32 | 0.04 | 0.90 |
| C04 | 0.01 | 0.96 | 0.44 | 0.04 | 0.58 |
| C05 | 0.01 | 0.95 | 0.44 | 0.04 | 0.55 |
| C06 | 0.01 | 0.96 | 0.46 | 0.04 | 0.58 |
| C07 | 0.00 | 0.96 | 0.18 | 0.04 | 0.92 |
| C08 | 0.00 | 0.96 | 0.22 | 0.03 | 0.89 |
| C09 | 0.01 | 0.96 | 0.18 | 0.03 | 0.73 |
| C10 | 0.00 | 0.96 | 0.38 | 0.04 | 0.85 |
| C11 | 0.01 | 0.96 | 0.43 | 0.04 | 0.42 |
| C12 | 0.00 | 0.96 | 0.24 | 0.04 | 0.83 |
| C13 | 0.00 | 0.96 | 0.07 | 0.03 | 0.12 |
| C14 | 0.00 | 0.96 | 0.08 | 0.04 | 0.17 |
| C15 | 0.00 | 0.96 | 0.08 | 0.04 | 0.21 |
| C16 | 0.01 | 0.95 | 0.30 | 0.04 | 0.87 |
| C17 | 0.01 | 0.96 | 0.31 | 0.04 | 0.58 |
| C18 | 0.01 | 0.96 | 0.28 | 0.04 | 0.85 |
| C19 | 0.01 | 0.96 | 0.14 | 0.04 | 0.82 |
| C20 | 0.00 | 0.96 | 0.08 | 0.03 | 0.83 |

`jev_response.json` preserves every score, score-level distribution, confidence, Noul and token usage. Noul is a yes-probability judgment with no separate confidence. These model judgments, especially causal “overfit” judgments, are not independently calibrated statistical tests. The full request supplies already-computed statistics; Jev did not calculate them. See [TypeSafe Score](https://docs.typesafe.ai/primitives/score), [Noul](https://docs.typesafe.ai/primitives/noul), and [composite scoring](https://docs.typesafe.ai/patterns/composite-scoring).

## 11. Final decision and reasons

**Primary: 01 – 04 – 13 – 14 – 24 – 38 (C05; generator B_recent).** Selected by the reproducible no-edge policy from the diverse shortlist. This selection has no demonstrated predictive advantage.

**Secondary: 02 – 06 – 08 – 12 – 18 – 25 (C03; generator A_long).** Selected from the minimum-overlap alternatives; shared numbers: 0. Diversification changes coverage, not the per-ticket chance.

Jev’s preferred candidate **C02: 02 – 10 – 13 – 18 – 24 – 33** remains available for comparison. Its generator has confirmation Holm p=0.846. The empirical gate, not forced Choice probability, determines eligibility.

Next candidates by the predeclared hypothetical policy score (analysis only; not valid edge ranks):

| ID | Numbers | Policy score | Eligible |
|---|---|---|---|
| C02 | 02 – 10 – 13 – 18 – 24 – 33 | 0.259 | False |
| C05 | 01 – 04 – 13 – 14 – 24 – 38 | 0.174 | False |
| C11 | 04 – 07 – 10 – 22 – 24 – 31 | 0.166 | False |
| C06 | 01 – 02 – 04 – 10 – 13 – 35 | 0.161 | False |
| C04 | 01 – 02 – 09 – 22 – 24 – 38 | 0.155 | False |

The policy was documented before the Jev request: corrected confirmation p<.05, block-CI lower bound above random, both halves above random, then empirical/sensitivity/Jev weighting if support exists. Otherwise seeded diversification applies. 0 candidates meet all empirical/Jev eligibility requirements. Numerical differences in heuristic scores cannot replace corrected evidence.

## 12. Reality check, verification and update files

**Did we discover an out-of-sample statistical edge over random selection? No detectable edge in this dataset.**

This is a small-data negative result across the declared tests, not a proof that every future model must fail. There is no evidence here supporting higher winning probabilities for the final tickets. The next useful evidence is prospective recorded performance, with fixed rules and no retrospective changes.

Verification passed: original SHA-256 unchanged; exact PMF normalized and mean reconciled; all predictions contain six distinct legal numbers; every stored match count independently recomputed; historical cutoff precedes target; future-outcome mutation leaves earlier predictions unchanged; confirmation ensemble weights frozen; uniform sampler agrees with the exact baseline.

Reusable entry point: `./run.ps1` rebuilds deterministic results from saved data and reuses the saved Jev response only when evidence is unchanged; `./run.ps1 -Refresh -AskJev` fetches new official results, reruns analysis and requests a fresh Jev review. Credentials are read from the environment without logging. Do not treat the snapshot as current after new draws.

Machine-readable outputs include audit, normalized/provenanced draws, baseline, number/pair/triple/conditional statistics, structural statistics, all predictions, performance, sensitivity, candidate evidence, full Jev request/response, and final decision. Model and request hashes are retained. See `README.md` for commands and scope. No original Excel cells were changed.
