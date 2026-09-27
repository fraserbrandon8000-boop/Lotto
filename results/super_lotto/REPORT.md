# SUPER LOTTO ANALYSIS

## SUPER LOTTO PRIMARY

Main: **01 · 22 · 32 · 34 · 35**

Super Ball: **2**

Target **#1753, 2026-09-22**. Frozen PRE-DRAW at **2026-09-21T15:56:06.709644+00:00**. This is the one primary selection, candidate SL10, selected by the predeclared seeded no-edge rule. **No main or Super Ball model passed the statistical gate. No predictive superiority is claimed.**

## Separation, rules and audit

This analysis uses only the Super Lotto workbook and official Super Lotto verification. No Lotto draws, rankings, fitted weights, tickets or Jev responses enter its modelling or Jev state. Generic combinatorics/serialization helpers are shared, not game data. Rules: five unique main numbers from 1–35, plus one Super Ball from 1–10. [Official rules and schedule](https://supremeventures.com/game/super-lotto/) list Tuesday/Friday draws at 8:30 p.m. Jamaica time.

Recalculated **176 draws**, #1577–#1752, 2025-01-03–2026-09-18. Workbook rows are descending; modelling uses ascending chronology. No missing/duplicate IDs, duplicate records, invalid dates, invalid values, repeated main numbers, derived-column discrepancies or frequency discrepancies. Main expected frequency is 25.142857, explaining the workbook's 25.1 rounding. Original SHA-256: `e7c654a8e7c4ce56738b4bb9ea7032209f52a609e3341e448a3f260f9036a07f`.

The official feed matched #1752 and contained no newer draw at the pre-draw check. External data and provenance are saved separately. Earlier workbook rows are screenshot transcriptions and were not all independently reconciled against official records; structural validation is not a guarantee against transcription errors. Both source workbooks remain unchanged.

## Exact random baseline

| Main matches | Main probability | Same mains + SB | Same mains without SB |
|---|---|---|---|
| 0 | 43.90% | 0.0438977057 | 0.3950793514 |
| 1 | 42.21% | 0.0422093324 | 0.3798839917 |
| 2 | 12.51% | 0.0125064689 | 0.1125582198 |
| 3 | 1.34% | 0.0013399788 | 0.0120598093 |
| 4 | 0.05% | 0.0000462062 | 0.0004158555 |
| 5 | 0.00% | 0.0000003080 | 0.0000027724 |

Expected main matches **0.714286**; Super Ball accuracy **10%**. Jackpot probability **1 in 3,246,320**. Main probabilities are C(5,k)C(30,5−k)/C(35,5); joint probabilities multiply by 0.1 under independent uniform draws. Main and SB models remain separate.

## Features and relationships

main_features.csv and super_ball_features.csv contain full/rolling/EW frequency, expected values, gap distributions and percentiles, trend and volatility. draw_structure.csv contains sums, mean/median, ranges, parity, low/high split, bands, consecutive/spacing/clustering, prior-draw overlap and last-digit properties. pairs.csv contains every pair, expectation, lift, rolling/half stability, gap and corrected enrichment. main_transitions.csv and super_ball_transitions.csv test conditional relationships. Triples are descriptive because expected counts are sparse; no triple-driven prediction is made. Typical-looking combinations are not inherently more likely as individual tickets.

## Independent randomness tests

| Test | Observed | Raw p | Holm p | Conclusion |
|---|---|---|---|---|
| main_dispersion | 28.727 | 0.939 | 1.000 | consistent with randomness |
| pair_dispersion | 553.739 | 0.465 | 1.000 | consistent with randomness |
| max_pair | 10.000 | 0.404 | 1.000 | consistent with randomness |
| serial_max_lag1_3 | 0.227 | 0.364 | 1.000 | consistent with randomness |
| gap_CDF | 0.018 | 0.917 | 1.000 | consistent with randomness |
| repeat_mean | 0.634 | 0.169 | 1.000 | consistent with randomness |
| sum_mean | 87.114 | 0.072 | 0.720 | consistent with randomness |
| odd_mean | 2.545 | 0.764 | 1.000 | consistent with randomness |
| SB_dispersion | 9.341 | 0.818 | 1.000 | consistent with randomness |
| SB_repeat_rate | 0.120 | 0.438 | 1.000 | consistent with randomness |

10,000 independently simulated histories; two-sided dispersion/repeat/location tests and upper-tail maximum/deviation tests. None detects a corrected deviation. Failure to reject randomness does not prove the generating process is uniform or rule out weak effects beyond this sample size.

## Walk-forward design

126 expanding-window targets after 50 warmup draws; 86 development and 40 retrospective confirmation. Main A–G select from 512 uniform candidate combinations; H is independently uniform. G learns only from earlier out-of-sample performance and freezes its weights at confirmation start. SB has seven separate models. Training-only Holm filtering controls pair and conditional enrichment. Flat E has no informative number ranking; F scores combinations only. G number rank is a marginal proxy; when flat its ties are neutrally seeded and not evidence of number-discovery skill.

Confirmation performance (main mean matches; SB accuracy):

| Domain | Model | n | Mean | 95% block CI | Older half | Recent half | Holm p | Gate |
|---|---|---|---|---|---|---|---|---|
| main | A_long | 40 | 0.675 | 0.500–0.850 | 0.600 | 0.750 | 1.000 | False |
| main | B_recent | 40 | 0.750 | 0.550–0.975 | 0.750 | 0.750 | 1.000 | False |
| main | C_gap | 40 | 0.700 | 0.525–0.875 | 0.650 | 0.750 | 1.000 | False |
| main | D_trend | 40 | 0.625 | 0.400–0.900 | 0.800 | 0.450 | 1.000 | False |
| main | E_pairs | 40 | 0.625 | 0.475–0.775 | 0.750 | 0.500 | 1.000 | False |
| main | F_structure | 40 | 0.625 | 0.425–0.850 | 0.850 | 0.400 | 1.000 | False |
| main | G_ensemble | 40 | 0.625 | 0.475–0.775 | 0.750 | 0.500 | 1.000 | False |
| main | H_random | 40 | 0.625 | 0.450–0.775 | 0.650 | 0.600 | 1.000 | False |
| SB | S_long | 40 | 0.050 | 0.000–0.150 | 0.100 | 0.000 | 1.000 | False |
| SB | S_recent | 40 | 0.125 | 0.050–0.200 | 0.100 | 0.150 | 1.000 | False |
| SB | S_gap | 40 | 0.050 | 0.000–0.100 | 0.050 | 0.050 | 1.000 | False |
| SB | S_trend | 40 | 0.150 | 0.050–0.250 | 0.200 | 0.100 | 1.000 | False |
| SB | S_transition | 40 | 0.050 | 0.000–0.125 | 0.050 | 0.050 | 1.000 | False |
| SB | S_ensemble | 40 | 0.050 | 0.000–0.100 | 0.050 | 0.050 | 1.000 | False |
| SB | S_random | 40 | 0.100 | 0.025–0.175 | 0.100 | 0.100 | 1.000 | False |

All-target performance:

| Domain | Model | n | Total hits | Mean | 0/1/2/3/4/5 rates | Holm p |
|---|---|---|---|---|---|---|
| main | A_long | 126 | 87 | 0.690 | 44.44%/42.86%/11.90%/0.79%/0.00%/0.00% | 1.000 |
| main | B_recent | 126 | 88 | 0.698 | 41.27%/47.62%/11.11%/0.00%/0.00%/0.00% | 1.000 |
| main | C_gap | 126 | 87 | 0.690 | 46.03%/38.89%/15.08%/0.00%/0.00%/0.00% | 1.000 |
| main | D_trend | 126 | 86 | 0.683 | 42.86%/46.03%/11.11%/0.00%/0.00%/0.00% | 1.000 |
| main | E_pairs | 126 | 87 | 0.690 | 47.62%/35.71%/16.67%/0.00%/0.00%/0.00% | 1.000 |
| main | F_structure | 126 | 83 | 0.659 | 46.03%/42.86%/10.32%/0.79%/0.00%/0.00% | 1.000 |
| main | G_ensemble | 126 | 78 | 0.619 | 46.83%/44.44%/8.73%/0.00%/0.00%/0.00% | 1.000 |
| main | H_random | 126 | 80 | 0.635 | 51.59%/35.71%/10.32%/2.38%/0.00%/0.00% | 1.000 |
| SB | S_long | 126 | 9 | 0.071 | 92.86%/7.14% | 1.000 |
| SB | S_recent | 126 | 13 | 0.103 | 89.68%/10.32% | 1.000 |
| SB | S_gap | 126 | 13 | 0.103 | 89.68%/10.32% | 1.000 |
| SB | S_trend | 126 | 14 | 0.111 | 88.89%/11.11% | 1.000 |
| SB | S_transition | 126 | 15 | 0.119 | 88.10%/11.90% | 1.000 |
| SB | S_ensemble | 126 | 12 | 0.095 | 90.48%/9.52% | 1.000 |
| SB | S_random | 126 | 10 | 0.079 | 92.06%/7.94% | 1.000 |

Exact null mean-match tests use convolution of the appropriate hypergeometric distribution (SB Bernoulli 0.1). Five-draw circular block bootstrap CIs use 5,000 replicates. Corrections are separate predeclared main and SB families. performance.json retains all periods, rates and uncertainty; combined_performance.json contains every main×SB pairing as a 6×2 outcome count matrix. Joint comparisons are descriptive, not evidence-selected joint models.

## Ranking coverage and construction

| Model | Pool | Mean winners | Random mean | 3+ | 4+ | All5 | AP | Holm p |
|---|---|---|---|---|---|---|---|---|
| A_long | 5 | 0.725 | 0.714 | 2.50% | 0.00% | 0.00% | 0.217 | 1.000 |
| A_long | 7 | 1.000 | 1.000 | 2.50% | 2.50% | 0.00% | 0.217 | 1.000 |
| A_long | 8 | 1.125 | 1.143 | 5.00% | 2.50% | 0.00% | 0.217 | 1.000 |
| A_long | 10 | 1.525 | 1.429 | 12.50% | 5.00% | 0.00% | 0.217 | 1.000 |
| A_long | 12 | 1.725 | 1.714 | 15.00% | 7.50% | 0.00% | 0.217 | 1.000 |
| A_long | 15 | 2.125 | 2.143 | 27.50% | 12.50% | 0.00% | 0.217 | 1.000 |
| A_long | 20 | 2.875 | 2.857 | 65.00% | 22.50% | 5.00% | 0.217 | 1.000 |
| B_recent | 5 | 0.775 | 0.714 | 0.00% | 0.00% | 0.00% | 0.228 | 1.000 |
| B_recent | 7 | 1.000 | 1.000 | 5.00% | 0.00% | 0.00% | 0.228 | 1.000 |
| B_recent | 8 | 1.050 | 1.143 | 5.00% | 0.00% | 0.00% | 0.228 | 1.000 |
| B_recent | 10 | 1.250 | 1.429 | 5.00% | 0.00% | 0.00% | 0.228 | 1.000 |
| B_recent | 12 | 1.625 | 1.714 | 20.00% | 0.00% | 0.00% | 0.228 | 1.000 |
| B_recent | 15 | 2.125 | 2.143 | 30.00% | 12.50% | 0.00% | 0.228 | 1.000 |
| B_recent | 20 | 2.775 | 2.857 | 60.00% | 27.50% | 5.00% | 0.228 | 1.000 |
| C_gap | 5 | 0.750 | 0.714 | 0.00% | 0.00% | 0.00% | 0.243 | 1.000 |
| C_gap | 7 | 1.050 | 1.000 | 5.00% | 2.50% | 0.00% | 0.243 | 1.000 |
| C_gap | 8 | 1.225 | 1.143 | 7.50% | 2.50% | 2.50% | 0.243 | 1.000 |
| C_gap | 10 | 1.550 | 1.429 | 17.50% | 5.00% | 2.50% | 0.243 | 1.000 |
| C_gap | 12 | 1.725 | 1.714 | 20.00% | 5.00% | 2.50% | 0.243 | 1.000 |
| C_gap | 15 | 2.350 | 2.143 | 50.00% | 15.00% | 5.00% | 0.243 | 1.000 |
| C_gap | 20 | 2.975 | 2.857 | 72.50% | 32.50% | 7.50% | 0.243 | 1.000 |
| D_trend | 5 | 0.725 | 0.714 | 0.00% | 0.00% | 0.00% | 0.232 | 1.000 |
| D_trend | 7 | 1.000 | 1.000 | 2.50% | 0.00% | 0.00% | 0.232 | 1.000 |
| D_trend | 8 | 1.200 | 1.143 | 10.00% | 0.00% | 0.00% | 0.232 | 1.000 |
| D_trend | 10 | 1.425 | 1.429 | 12.50% | 0.00% | 0.00% | 0.232 | 1.000 |
| D_trend | 12 | 1.825 | 1.714 | 25.00% | 5.00% | 0.00% | 0.232 | 1.000 |
| D_trend | 15 | 2.225 | 2.143 | 37.50% | 10.00% | 2.50% | 0.232 | 1.000 |
| D_trend | 20 | 2.950 | 2.857 | 70.00% | 25.00% | 7.50% | 0.232 | 1.000 |
| G_ensemble | 5 | 0.775 | 0.714 | 2.50% | 0.00% | 0.00% | 0.233 | 1.000 |
| G_ensemble | 7 | 1.175 | 1.000 | 7.50% | 0.00% | 0.00% | 0.233 | 1.000 |
| G_ensemble | 8 | 1.325 | 1.143 | 12.50% | 0.00% | 0.00% | 0.233 | 1.000 |
| G_ensemble | 10 | 1.575 | 1.429 | 17.50% | 2.50% | 0.00% | 0.233 | 1.000 |
| G_ensemble | 12 | 1.850 | 1.714 | 25.00% | 5.00% | 2.50% | 0.233 | 1.000 |
| G_ensemble | 15 | 2.225 | 2.143 | 40.00% | 15.00% | 2.50% | 0.233 | 1.000 |
| G_ensemble | 20 | 3.000 | 2.857 | 65.00% | 37.50% | 12.50% | 0.233 | 1.000 |
| H_random | 5 | 0.825 | 0.714 | 0.00% | 0.00% | 0.00% | 0.252 | 1.000 |
| H_random | 7 | 1.125 | 1.000 | 0.00% | 0.00% | 0.00% | 0.252 | 1.000 |
| H_random | 8 | 1.250 | 1.143 | 5.00% | 0.00% | 0.00% | 0.252 | 1.000 |
| H_random | 10 | 1.625 | 1.429 | 17.50% | 2.50% | 0.00% | 0.252 | 1.000 |
| H_random | 12 | 1.875 | 1.714 | 25.00% | 5.00% | 0.00% | 0.252 | 1.000 |
| H_random | 15 | 2.350 | 2.143 | 42.50% | 10.00% | 2.50% | 0.252 | 1.000 |
| H_random | 20 | 3.150 | 2.857 | 70.00% | 40.00% | 10.00% | 0.252 | 1.000 |

coverage.json includes full/development/confirmation periods and exact same-pool random coverage probabilities. AP is mean average precision on all 35 numbers. E/F inapplicability is preserved. Corrected coverage tests do not establish an exploitable ranking edge.

Top retrospective confirmation construction methods:

| Method | Mean | 95% CI | Holm p |
|---|---|---|---|
| B_recent:pool15:uniform | 1.000 | 0.750–1.250 | 0.500 |
| G_ensemble:pool7:uniform | 0.925 | 0.700–1.175 | 1.000 |
| G_ensemble:pool8:uniform | 0.875 | 0.625–1.100 | 1.000 |
| D_trend:pool8:structure | 0.850 | 0.600–1.100 | 1.000 |
| D_trend:pool10:structure | 0.825 | 0.575–1.075 | 1.000 |
| D_trend:pool12:structure | 0.825 | 0.575–1.075 | 1.000 |
| D_trend:pool15:structure | 0.825 | 0.575–1.075 | 1.000 |
| D_trend:pool15:uniform | 0.825 | 0.600–1.050 | 1.000 |
| D_trend:pool7:structure | 0.825 | 0.600–1.075 | 1.000 |
| G_ensemble:pool10:uniform | 0.825 | 0.625–1.075 | 1.000 |
| B_recent:pool7:structure | 0.800 | 0.625–0.975 | 1.000 |
| B_recent:pool7:uniform | 0.800 | 0.600–1.000 | 1.000 |

Forty-four unique construction rules compare A/B/D/G top-five, exact structure-penalized combinations within top 7/8/10/12/15, and uniform draws within those pools. Pure additive optimization reduces to top five regardless of the larger pool. Construction results are exploratory; no corrected construction advantage is established. Full match distributions and per-origin tickets are saved.

## Sensitivity and random controls

| Model | Min confirmation mean | Max confirmation mean | Best variant Holm p |
|---|---|---|---|
| A_long | 0.600 | 0.800 | 1.000 |
| B_recent | 0.700 | 0.800 | 1.000 |
| C_gap | 0.675 | 0.700 | 1.000 |
| D_trend | 0.625 | 0.825 | 1.000 |
| E_pairs | 0.625 | 0.625 | 1.000 |
| F_structure | 0.625 | 0.850 | 1.000 |
| G_ensemble | 0.625 | 0.875 | 0.823 |
| H_random | 0.600 | 0.625 | 1.000 |
| S_ensemble | 0.050 | 0.150 | 1.000 |
| S_gap | 0.050 | 0.050 | 1.000 |
| S_long | 0.050 | 0.050 | 1.000 |
| S_random | 0.050 | 0.100 | 1.000 |
| S_recent | 0.075 | 0.150 | 1.000 |
| S_transition | 0.025 | 0.050 | 1.000 |
| S_trend | 0.075 | 0.175 | 0.697 |

Eleven perturbations cover rolling windows, EW decay, trend horizon, history length, pair threshold, ensemble weighting and search seed. These reuse the same outcomes and are not eleven independent replications; no best variant replaces the declared model. random_controls.json records 20,000 independent 40-draw null means. Candidate rank stability under unvalidated or flat objectives is not predictive robustness.

## Analytical candidate shortlist and Jev

The following is an analytical audit, not a set of additional recommended plays. Candidates are complete tickets, with at most three shared main numbers between any pair. Each profile records main/SB generator support, individual ranks, long/recent/gap/trend/pair/structure evidence, model agreement, sensitivity and counterevidence. The final no-edge rule chooses uniformly among these fixed candidates using seed 2026092109; it is not claimed to sample all playable tickets uniformly.

| ID | Main | SB | Main generator | SB generator | Jev Choice p | Robustness | Consensus | Quality | Stability |
|---|---|---|---|---|---|---|---|---|---|
| SL01 | 09 · 11 · 12 · 17 · 24 | 5 | A_long | S_long | 35.00% | 0.100 | 0.010 | 0.030 | 2.250 |
| SL02 | 03 · 06 · 12 · 17 · 24 | 5 | A_long | S_recent | 1.00% | 0.100 | 0.010 | 0.030 | 2.270 |
| SL03 | 12 · 17 · 22 · 23 · 24 | 2 | A_long | S_gap | 0.00% | 0.060 | 0.010 | 0.030 | 1.850 |
| SL04 | 09 · 11 · 18 · 24 · 25 | 5 | B_recent | S_trend | 7.00% | 0.130 | 0.010 | 0.040 | 2.280 |
| SL05 | 06 · 09 · 18 · 24 · 29 | 6 | B_recent | S_transition | 0.00% | 0.120 | 0.010 | 0.030 | 2.290 |
| SL06 | 01 · 12 · 18 · 23 · 25 | 2 | B_recent | S_ensemble | 27.00% | 0.130 | 0.010 | 0.040 | 2.810 |
| SL07 | 04 · 07 · 13 · 33 · 34 | 4 | C_gap | S_random | 12.00% | 0.080 | 0.020 | 0.030 | 2.110 |
| SL08 | 04 · 06 · 07 · 17 · 33 | 5 | C_gap | S_long | 1.00% | 0.100 | 0.010 | 0.030 | 2.310 |
| SL09 | 04 · 10 · 16 · 17 · 33 | 5 | C_gap | S_recent | 1.00% | 0.110 | 0.010 | 0.030 | 1.820 |
| SL10 | 01 · 22 · 32 · 34 · 35 | 2 | D_trend | S_gap | 2.00% | 0.070 | 0.020 | 0.030 | 1.460 |
| SL11 | 01 · 06 · 11 · 18 · 22 | 5 | D_trend | S_trend | 7.00% | 0.210 | 0.030 | 0.060 | 2.680 |
| SL12 | 02 · 19 · 22 · 32 · 35 | 6 | D_trend | S_transition | 0.00% | 0.070 | 0.020 | 0.020 | 1.100 |
| SL13 | 18 · 22 · 23 · 24 · 30 | 2 | E_pairs | S_ensemble | 0.00% | 0.020 | 0.000 | 0.020 | 0.280 |
| SL14 | 05 · 10 · 20 · 22 · 32 | 4 | E_pairs | S_random | 0.00% | 0.050 | 0.010 | 0.020 | 0.300 |
| SL15 | 03 · 08 · 12 · 20 · 32 | 5 | E_pairs | S_long | 0.00% | 0.080 | 0.010 | 0.030 | 0.600 |
| SL16 | 06 · 07 · 18 · 22 · 29 | 5 | F_structure | S_recent | 0.00% | 0.150 | 0.010 | 0.050 | 2.270 |
| SL17 | 06 · 07 · 18 · 25 · 28 | 2 | F_structure | S_gap | 0.00% | 0.060 | 0.010 | 0.020 | 1.840 |
| SL18 | 06 · 12 · 18 · 19 · 29 | 5 | F_structure | S_trend | 2.00% | 0.140 | 0.020 | 0.040 | 2.460 |
| SL19 | 10 · 11 · 16 · 21 · 22 | 6 | G_ensemble | S_transition | 0.00% | 0.040 | 0.010 | 0.020 | 0.850 |
| SL20 | 04 · 06 · 13 · 17 · 18 | 2 | H_random | S_ensemble | 4.00% | 0.020 | 0.010 | 0.010 | 0.530 |

Requested model `jev-latest`, returned **jev-1.13.0**. All **161** typed answers passed schema/probability checks. Jev preferred **SL01**, Choice probability **35.00%**, confidence **0.310**. The complete distribution above and raw Score distributions/confidences are preserved in jev_response.json. Four Noul judgments per candidate are listed below; Noul has a probability, not a separate confidence.

| ID | Overfit/chance | Stable | Stronger than random | Single-family dependence |
|---|---|---|---|---|
| SL01 | 95.00% | 24.00% | 4.00% | 77.00% |
| SL02 | 95.00% | 28.00% | 4.00% | 72.00% |
| SL03 | 95.00% | 20.00% | 5.00% | 72.00% |
| SL04 | 95.00% | 29.00% | 5.00% | 67.00% |
| SL05 | 95.00% | 25.00% | 4.00% | 71.00% |
| SL06 | 95.00% | 30.00% | 5.00% | 65.00% |
| SL07 | 95.00% | 31.00% | 4.00% | 55.00% |
| SL08 | 95.00% | 26.00% | 4.00% | 72.00% |
| SL09 | 95.00% | 23.00% | 4.00% | 76.00% |
| SL10 | 95.00% | 21.00% | 4.00% | 74.00% |
| SL11 | 95.00% | 39.00% | 5.00% | 66.00% |
| SL12 | 95.00% | 22.00% | 4.00% | 76.00% |
| SL13 | 95.00% | 9.00% | 4.00% | 63.00% |
| SL14 | 95.00% | 10.00% | 4.00% | 64.00% |
| SL15 | 95.00% | 10.00% | 4.00% | 75.00% |
| SL16 | 94.00% | 31.00% | 5.00% | 75.00% |
| SL17 | 95.00% | 25.00% | 5.00% | 69.00% |
| SL18 | 95.00% | 28.00% | 4.00% | 73.00% |
| SL19 | 95.00% | 10.00% | 4.00% | 69.00% |
| SL20 | 95.00% | 10.00% | 4.00% | 42.00% |

Score scale is 0–4 with concrete supplied levels. Choice/Score confidence summarizes concentration in the model response; it is not a winning probability or external validation. Jev cannot override the statistical gate. A forced preference between unsupported candidates does not establish an edge. The primary is therefore the predeclared fallback rather than Jev’s favorite.

## Prospective freeze and reproducibility

Primary SL10 is recorded in prospective/prediction_1753.json, with timestamp, target, source/configuration/code hashes, exact full pre-draw rankings, Jev request hash and complete response, seed and model versions. The exclusive-create freeze script refuses to replace it. prospective/ledger.jsonl stores its SHA-256; future outcomes must be appended as new events. Local files are not cryptographically immutable storage; the digest and exclusive-write workflow make changes detectable.

Verification passed: 126 valid backtest origins, independently recomputed scores, exact baselines, unchanged source workbook, and a future-data mutation test starting at #1662 that leaves the target and earlier predictions unchanged. This test supplements code inspection; it is not a claim that every possible implementation defect has been excluded.

From the project root: `python scripts/research/super_lotto.py` regenerates deterministic Super Lotto analytical outputs; `python scripts/research/verify_research.py` validates them; `python scripts/research/reports.py` renders both reports. The frozen prediction remains unchanged. `scripts/research/super_jev.mjs` uses the installed SDK and TYPESAFE_API_KEY environment variable; do not rerun Jev to search for a preferred answer. No key is stored in these results. The protected first response and prediction are the experiment of record.
