# Claude + TypeSafe Jev clean-room experiment: Jamaica Lotto #2340

```
CLAUDE + JEV CLEAN ROOM — LOTTO #2340

01 · 04 · 10 · 13 · 18 · 24
```

- **Data cutoff:** draw #2339 (2026-09-19); 169 observed draws #2161–#2339, gap #2252–#2261 not recovered
- **Validated edge found:** NO
- **Selection basis:** Branch B of the frozen rule: no validated predictive edge; highest Jev Choice probability over the full candidate pool (candidate C09, method `consensus`)
- **Jev Choice probability:** 0.42 (relative preference among 21 candidates, not a winning probability)
- **Jev confidence:** 0.38
- **Jev model/version:** `jev-latest` → `jev-1.13.0`
- **Exact random expectation for this (and every) ticket:** 0.947 matches, P(3+) = 3.87%, P(4+) = 0.28%, jackpot 1 in 2,760,681

## 1. Data audit

- Workbook: 167 rows, draws 2161–2337, newest first; sha256 `5d55e059df0ca5ce…`
- Issues found: 0 (IDs, duplicates, dates, missing values, six unique mains in 1–38, bonus validity, Wed/Sat weekday, chronology all pass)
- Missing IDs: 2252–2261 (10 draws, expected dates 2025-11-19 … 2025-12-20). Official Supreme Ventures pages were blocked by the environment's egress policy, so nothing was recovered or guessed.
- Schedule note: #2246 (2025-10-25) → #2247 (2025-11-01) skipped one Wed/Sat slot with consecutive IDs (a suspended draw date, not a missing draw).
- #2338 and #2339 were added as ordinary rows (user-supplied); no conflicts; schedule continuity OK.
- Final analysis dataset: 169 draws, 2025-01-01 → 2026-09-19; layers kept separately in `data/01..04`.

## 2. Exact random baseline (6 of 38)

| matches | probability | 1 in |
|---|---|---|
| 0 | 0.32824944 (43152/131461) | 3.05 |
| 1 | 0.43766592 (57536/131461) | 2.28 |
| 2 | 0.19538657 (179800/920227) | 5.12 |
| 3 | 0.03593316 (99200/2760681) | 27.83 |
| 4 | 0.00269499 (2480/920227) | 371.06 |
| 5 | 0.00006955 (64/920227) | 14,378.55 |
| 6 | 0.00000036 (1/2760681) | 2,760,681.00 |

Expected matches = 18/19 = 0.9474; P(3+) = 0.03870; P(4+) = 0.002765; P(5+) = 6.991e-05; jackpot = 1/2,760,681.

Top-k pool baselines (expected winners captured): top 6: 0.947, top 8: 1.263, top 10: 1.579, top 12: 1.895, top 15: 2.368, top 20: 3.158

## 3. Randomness tests

| test | p | Holm p | classification |
|---|---|---|---|
| freq_chisq | 0.6142 | 1.000 | consistent with randomness |
| freq_max | 0.7769 | 1.000 | consistent with randomness |
| freq_min | 0.5852 | 1.000 | consistent with randomness |
| gap_chisq | 0.8077 | 1.000 | consistent with randomness |
| gap_mean | 0.3289 | 1.000 | consistent with randomness |
| pair_chisq | 0.6094 | 1.000 | consistent with randomness |
| pair_max | 0.5330 | 1.000 | consistent with randomness |
| transition_chisq | 0.5485 | 1.000 | consistent with randomness |
| sum_lag1_autocorr | 0.8741 | 1.000 | consistent with randomness |
| lag1_overlap | 0.8793 | 1.000 | consistent with randomness |
| lag2_overlap | 0.4981 | 1.000 | consistent with randomness |
| lag3_overlap | 0.7885 | 1.000 | consistent with randomness |
| lag4_overlap | 0.1576 | 1.000 | consistent with randomness |
| lag5_overlap | 0.2206 | 1.000 | consistent with randomness |
| structure_sum | 0.5338 | 1.000 | consistent with randomness |
| structure_odd_count | 0.5196 | 1.000 | consistent with randomness |
| structure_low_count_1_19 | 0.3603 | 1.000 | consistent with randomness |
| structure_consecutive_pairs | 0.1172 | 1.000 | consistent with randomness |
| structure_range | 0.7692 | 1.000 | consistent with randomness |
| bonus_uniformity | 0.3429 | 1.000 | consistent with randomness |

Per-number binomial: 1/38 raw p<0.05, min BH q = 0.85. Pairs: 21/703 raw p<0.05 (≈35 expected by chance), min BH q = 0.78.
**Conclusion: consistent with an independent uniform draw process.**

## 4. Walk-forward design

140 causal targets (#2190–#2339); development #2190–#2269, confirmation #2270–#2339. Leakage test (scrambling all future draws leaves every prediction unchanged): PASSED. Protocol committed before any predictive result (`config/protocol.json`).

## 5. Number discovery (mean winners captured in top k; exact p is one-sided, full period)

| ranker | top 6 | top 8 | top 10 | top 12 | top 15 | top 20 | top-12 dev | top-12 conf | top-12 p | top-12 3+% |
|---|---|---|---|---|---|---|---|---|---|---|
| *random expectation* | *0.947* | *1.263* | *1.579* | *1.895* | *2.368* | *3.158* | *1.895* | *1.895* | | *27.3* |
| H_random | 1.007 | 1.314 | 1.629 | 1.979 | 2.429 | 3.093 | 1.957 | 2.000 | 0.185 | 35.0 |
| A_freq_all | 0.971 | 1.271 | 1.564 | 1.864 | 2.329 | 3.071 | 1.929 | 1.800 | 0.647 | 27.1 |
| A_inv_cold | 0.857 | 1.293 | 1.629 | 1.979 | 2.457 | 3.229 | 1.971 | 1.986 | 0.185 | 29.3 |
| B_roll_10 | 0.986 | 1.321 | 1.693 | 2.036 | 2.450 | 3.243 | 2.171 | 1.900 | 0.063 | 35.0 |
| B_roll_20 | 1.029 | 1.321 | 1.636 | 1.893 | 2.336 | 3.164 | 1.900 | 1.886 | 0.523 | 31.4 |
| B_roll_30 | 0.957 | 1.279 | 1.529 | 1.871 | 2.379 | 3.186 | 1.771 | 1.971 | 0.617 | 27.9 |
| B_roll_50 | 1.029 | 1.321 | 1.614 | 1.936 | 2.393 | 3.071 | 1.971 | 1.900 | 0.337 | 28.6 |
| B_roll_100 | 0.929 | 1.207 | 1.564 | 1.836 | 2.271 | 3.064 | 1.929 | 1.743 | 0.757 | 26.4 |
| B_ew_10 | 1.021 | 1.400 | 1.671 | 2.007 | 2.407 | 3.143 | 1.957 | 2.057 | 0.112 | 35.7 |
| B_ew_20 | 1.021 | 1.371 | 1.643 | 1.957 | 2.364 | 3.157 | 1.957 | 1.957 | 0.255 | 30.0 |
| B_ew_40 | 0.993 | 1.257 | 1.664 | 1.950 | 2.357 | 3.050 | 2.000 | 1.900 | 0.281 | 28.6 |
| C_overdue | 0.986 | 1.221 | 1.493 | 1.764 | 2.300 | 3.000 | 1.814 | 1.714 | 0.934 | 25.7 |
| C_recent | 0.964 | 1.343 | 1.643 | 1.907 | 2.429 | 3.329 | 1.900 | 1.914 | 0.459 | 26.4 |
| C_hazard | 1.007 | 1.321 | 1.543 | 1.893 | 2.407 | 3.179 | 1.900 | 1.886 | 0.523 | 29.3 |
| C_own_gap_pct | 0.886 | 1.150 | 1.471 | 1.821 | 2.271 | 3.036 | 1.829 | 1.814 | 0.805 | 24.3 |
| D_trend_20v40 | 1.021 | 1.293 | 1.557 | 1.857 | 2.421 | 3.186 | 1.814 | 1.900 | 0.676 | 30.7 |
| D_slope_50 | 0.950 | 1.336 | 1.679 | 2.036 | 2.529 | 3.193 | 1.957 | 2.114 | 0.063 | 34.3 |
| E_transition | 0.936 | 1.243 | 1.564 | 1.857 | 2.293 | 3.100 | 1.771 | 1.943 | 0.676 | 26.4 |
| E_pair_centrality | 0.929 | 1.214 | 1.521 | 1.921 | 2.329 | 3.064 | 2.043 | 1.800 | 0.397 | 26.4 |
| G_ensemble_equal | 1.029 | 1.336 | 1.550 | 1.843 | 2.371 | 3.086 | 1.800 | 1.886 | 0.732 | 25.7 |
| G_ensemble_adaptive | 0.971 | 1.271 | 1.543 | 1.886 | 2.329 | 3.164 | 1.843 | 1.929 | 0.555 | 27.9 |

Pre-registered number-discovery check: dev-selected ranker `B_roll_10` top-12 dev 2.171 → confirmation 1.900 (random 1.895, p = 0.504). Not validated. Full 3+/4+/5+/6 coverage for every pool size is in `outputs/05_number_discovery_coverage.json`.

## 6. Ticket methods (6-number tickets, 140 targets)

| method | mean | 95% CI | sd | 0% | 1% | 2% | 3% | 4+% | 6s | dev | conf | exact p | Holm p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| *exact random* | *0.947* | | *0.831* | *32.8* | *43.8* | *19.5* | *3.6* | *0.28* | | *0.947* | *0.947* | | |
| A_freq_all|top6 | 0.971 | 0.84–1.11 | 0.86 | 32.9 | 41.4 | 22.1 | 2.9 | 0.7 | 0 | 1.000 | 0.943 | 0.382 | 1.00 |
| A_freq_all|opt_top12 | 1.000 | 0.87–1.13 | 0.78 | 28.6 | 44.3 | 25.7 | 1.4 | 0.0 | 0 | 1.029 | 0.971 | 0.241 | 1.00 |
| A_inv_cold|top6 | 0.857 | 0.73–0.99 | 0.78 | 36.4 | 42.9 | 20.0 | 0.0 | 0.7 | 0 | 0.843 | 0.871 | 0.910 | 1.00 |
| A_inv_cold|opt_top12 | 0.893 | 0.76–1.04 | 0.85 | 37.1 | 40.7 | 17.9 | 4.3 | 0.0 | 0 | 0.914 | 0.871 | 0.795 | 1.00 |
| B_roll_10|top6 | 0.986 | 0.86–1.11 | 0.76 | 28.6 | 45.0 | 25.7 | 0.7 | 0.0 | 0 | 1.100 | 0.871 | 0.308 | 1.00 |
| B_roll_10|opt_top12 | 0.971 | 0.84–1.10 | 0.80 | 30.7 | 44.3 | 22.1 | 2.9 | 0.0 | 0 | 1.100 | 0.843 | 0.382 | 1.00 |
| B_roll_50|top6 | 1.029 | 0.89–1.17 | 0.84 | 27.9 | 47.1 | 19.3 | 5.7 | 0.0 | 0 | 1.100 | 0.957 | 0.135 | 1.00 |
| B_roll_50|opt_top12 | 1.050 | 0.92–1.19 | 0.82 | 26.4 | 46.4 | 22.9 | 4.3 | 0.0 | 0 | 1.071 | 1.029 | 0.080 | 1.00 |
| B_ew_20|top6 | 1.021 | 0.89–1.16 | 0.80 | 28.6 | 42.9 | 26.4 | 2.1 | 0.0 | 0 | 1.043 | 1.000 | 0.158 | 1.00 |
| B_ew_20|opt_top12 | 0.993 | 0.86–1.14 | 0.84 | 32.9 | 37.9 | 26.4 | 2.9 | 0.0 | 0 | 0.943 | 1.043 | 0.273 | 1.00 |
| C_hazard|top6 | 1.007 | 0.86–1.16 | 0.87 | 33.6 | 35.7 | 27.1 | 3.6 | 0.0 | 0 | 1.000 | 1.014 | 0.211 | 1.00 |
| C_hazard|opt_top12 | 0.936 | 0.79–1.09 | 0.86 | 34.3 | 42.9 | 18.6 | 3.6 | 0.7 | 0 | 0.957 | 0.914 | 0.583 | 1.00 |
| C_overdue|top6 | 0.986 | 0.85–1.12 | 0.86 | 31.4 | 44.3 | 18.6 | 5.7 | 0.0 | 0 | 1.057 | 0.914 | 0.308 | 1.00 |
| C_overdue|opt_top12 | 0.943 | 0.81–1.09 | 0.84 | 35.0 | 38.6 | 23.6 | 2.9 | 0.0 | 0 | 0.929 | 0.957 | 0.543 | 1.00 |
| C_recent|top6 | 0.964 | 0.83–1.10 | 0.79 | 30.7 | 44.3 | 22.9 | 2.1 | 0.0 | 0 | 0.914 | 1.014 | 0.421 | 1.00 |
| C_recent|opt_top12 | 0.950 | 0.82–1.08 | 0.80 | 32.1 | 42.9 | 22.9 | 2.1 | 0.0 | 0 | 1.029 | 0.871 | 0.502 | 1.00 |
| D_trend_20v40|top6 | 1.021 | 0.88–1.16 | 0.86 | 31.4 | 39.3 | 25.0 | 4.3 | 0.0 | 0 | 1.000 | 1.043 | 0.158 | 1.00 |
| D_trend_20v40|opt_top12 | 1.050 | 0.90–1.21 | 0.92 | 32.9 | 35.0 | 27.1 | 4.3 | 0.7 | 0 | 1.043 | 1.057 | 0.080 | 1.00 |
| E_transition|top6 | 0.936 | 0.80–1.08 | 0.85 | 33.6 | 44.3 | 17.9 | 3.6 | 0.7 | 0 | 0.857 | 1.014 | 0.583 | 1.00 |
| E_transition|opt_top12 | 0.979 | 0.84–1.13 | 0.88 | 32.9 | 42.9 | 17.9 | 6.4 | 0.0 | 0 | 0.900 | 1.057 | 0.344 | 1.00 |
| E_pair_centrality|top6 | 0.929 | 0.79–1.08 | 0.89 | 36.4 | 39.3 | 20.7 | 2.9 | 0.7 | 0 | 0.986 | 0.871 | 0.622 | 1.00 |
| E_pair_centrality|opt_top12 | 0.971 | 0.82–1.13 | 0.92 | 33.6 | 44.3 | 15.0 | 5.7 | 1.4 | 0 | 1.071 | 0.871 | 0.382 | 1.00 |
| G_ensemble_equal|top6 | 1.029 | 0.90–1.16 | 0.77 | 25.7 | 47.9 | 24.3 | 2.1 | 0.0 | 0 | 0.914 | 1.143 | 0.135 | 1.00 |
| G_ensemble_equal|opt_top12 | 0.957 | 0.81–1.11 | 0.88 | 33.6 | 43.6 | 17.1 | 5.0 | 0.7 | 0 | 0.900 | 1.014 | 0.461 | 1.00 |
| G_ensemble_adaptive|top6 | 0.971 | 0.84–1.10 | 0.80 | 31.4 | 41.4 | 25.7 | 1.4 | 0.0 | 0 | 0.929 | 1.014 | 0.382 | 1.00 |
| G_ensemble_adaptive|opt_top12 | 0.943 | 0.80–1.09 | 0.83 | 35.0 | 37.9 | 25.0 | 2.1 | 0.0 | 0 | 0.886 | 1.000 | 0.543 | 1.00 |
| H_random|top6 | 1.007 | 0.86–1.16 | 0.92 | 33.6 | 39.3 | 20.7 | 5.7 | 0.7 | 0 | 0.971 | 1.043 | 0.211 | nan |
| H_random|opt_top12 | 0.993 | 0.85–1.14 | 0.88 | 34.3 | 35.7 | 27.1 | 2.1 | 0.7 | 0 | 1.000 | 0.986 | 0.273 | nan |
| consensus | 1.029 | 0.89–1.18 | 0.86 | 30.0 | 42.1 | 23.6 | 3.6 | 0.7 | 0 | 1.014 | 1.043 | 0.135 | 1.00 |
| M_follow_leader | 0.943 | 0.81–1.07 | 0.78 | 31.4 | 44.3 | 22.9 | 1.4 | 0.0 | 0 | 1.057 | 0.829 | 0.543 | 1.00 |
| random_ticket | 0.843 | 0.71–0.98 | 0.81 | 38.6 | 41.4 | 17.1 | 2.9 | 0.0 | 0 | 0.871 | 0.814 | 0.940 | nan |
| B_roll_10|pair_top12 | 1.079 | 0.94–1.21 | 0.84 | 27.1 | 42.1 | 26.4 | 4.3 | 0.0 | 0 | 1.243 | 0.914 | 0.036 | 1.00 |
| B_roll_50|opt_top10 | 1.071 | 0.94–1.21 | 0.82 | 25.7 | 45.7 | 24.3 | 4.3 | 0.0 | 0 | 1.057 | 1.086 | 0.044 | 1.00 |
| B_roll_50|diversity_top15 | 1.086 | 0.95–1.23 | 0.83 | 25.7 | 44.3 | 25.7 | 4.3 | 0.0 | 0 | 1.100 | 1.071 | 0.029 | 1.00 |
| B_ew_10|opt_top8 | 1.079 | 0.94–1.22 | 0.88 | 28.6 | 40.7 | 25.7 | 4.3 | 0.7 | 0 | 1.086 | 1.071 | 0.036 | 1.00 |
| B_ew_10|opt_top10 | 1.079 | 0.94–1.22 | 0.89 | 30.0 | 37.9 | 26.4 | 5.7 | 0.0 | 0 | 1.143 | 1.014 | 0.036 | 1.00 |
| B_ew_10|opt_top15 | 1.071 | 0.93–1.21 | 0.88 | 30.0 | 37.9 | 27.1 | 5.0 | 0.0 | 0 | 1.129 | 1.014 | 0.044 | 1.00 |
| D_trend_20v40|opt_top15 | 1.071 | 0.93–1.21 | 0.89 | 30.0 | 37.9 | 27.9 | 3.6 | 0.7 | 0 | 1.071 | 1.071 | 0.044 | 1.00 |

All 162 methods plus 9 random controls, with medians, two-sided p, BH q and the λ sensitivity grid, are in `outputs/05_*.json`.

## 7. Pre-registered validation

- Dev-selected method: `B_roll_10|pair_top12`: development 1.243 (p = 0.0023) → confirmation 0.914 (p = 0.654).
- Sensitivity variants above random in confirmation: 38% (needed ≥ 67%).
- Methods with raw p < 0.05: 7 of 162 (≈8.1 expected by chance); surviving Holm: 0.
- Power: with 70 confirmation targets, the minimum detectable improvement at 80% power is 0.25 matches per ticket (+26%).
- **VALIDATED EDGE: NO**. Formally 'suggestive' under the protocol wording (raw p < 0.05 results exist), but their count is at the chance rate.

## 8. #2340 candidate pool and Jev's first and only response

| candidate | ticket | generating method(s) | Jev Choice p |
|---|---|---|---|
| C09 | 01 · 04 · 10 · 13 · 18 · 24 | consensus | 0.42 |
| C20 | 01 · 02 · 04 · 07 · 13 · 24 | B_roll_10|opt_top12, B_roll_20|opt_top12, D_trend_20v40|opt_top12 | 0.20 |
| C06 | 01 · 04 · 13 · 18 · 24 · 25 | G_ensemble_equal|opt_top12 | 0.14 |
| C07 | 01 · 02 · 06 · 18 · 25 · 35 | E_transition|opt_top12 | 0.14 |
| C18 | 04 · 09 · 10 · 13 · 24 · 35 | B_ew_20|opt_top12, G_ensemble_adaptive|opt_top12 | 0.03 |
| C08 | 01 · 04 · 09 · 10 · 13 · 24 | B_ew_10|opt_top12 | 0.02 |
| C04 (control) | 02 · 16 · 17 · 25 · 33 · 37 | random_ticket | 0.01 |
| C11 | 04 · 08 · 09 · 13 · 24 · 35 | B_ew_40|opt_top12 | 0.01 |
| C12 | 01 · 08 · 13 · 18 · 24 · 25 | A_freq_all|opt_top12 | 0.01 |
| C13 (control) | 01 · 21 · 26 · 31 · 34 · 36 | H_random|top6 | 0.01 |
| C19 | 08 · 09 · 13 · 15 · 22 · 24 | B_roll_30|opt_top12 | 0.01 |
| C01 | 03 · 04 · 13 · 18 · 24 · 29 | D_slope_50|opt_top12 | 0.00 |
| C02 | 05 · 16 · 23 · 28 · 29 · 32 | A_inv_cold|opt_top12 | 0.00 |
| C03 | 03 · 09 · 16 · 17 · 24 · 26 | C_hazard|opt_top12 | 0.00 |
| C05 | 01 · 06 · 08 · 13 · 35 · 38 | B_roll_100|opt_top12 | 0.00 |
| C10 | 11 · 14 · 18 · 21 · 25 · 34 | E_pair_centrality|opt_top12 | 0.00 |
| C14 | 05 · 11 · 16 · 31 · 32 · 34 | C_overdue|opt_top12 | 0.00 |
| C15 | 01 · 04 · 13 · 18 · 28 · 29 | C_recent|opt_top12 | 0.00 |
| C16 | 06 · 09 · 10 · 31 · 35 · 38 | B_roll_50|opt_top12 | 0.00 |
| C17 | 01 · 04 · 06 · 13 · 18 · 29 | B_roll_10|pair_top12 | 0.00 |
| C21 | 16 · 27 · 31 · 34 · 35 · 38 | C_own_gap_pct|opt_top12 | 0.00 |

| Jev Score (0–4) | expected score | confidence |
|---|---|---|
| empirical_robustness | 0.22 | 0.82 |
| evidence_quality | 2.02 | 0.98 |
| model_consensus | 2.57 | 0.64 |
| stability | 1.56 | 0.63 |

| Jev Noul | P(yes) |
|---|---|
| likely_chance_or_overfitting | 0.96 |
| depends_on_one_model | 0.40 |
| unstable_under_reasonable_assumptions | 0.83 |
| materially_stronger_than_random | 0.03 |

Jev: model `jev-1.13.0`, 16095 input tokens, one request (`jev/jev_call_log.json`).

## 9. Clean-room controls

- Branch `claude/lotto-2340-cleanroom` created from clean base `a810de0` (base tree: `.gitignore` only).
- No other branch was checked out, logged, diffed or read; GitHub was not searched; no prior #2340 prediction, candidate set, Jev response or ticket performance was seen.
- #2339 entered only as one row of the dataset; no feature, candidate or Jev input singles it out, and the Jev state contains no raw draw list.
- Protocol committed before walk-forward results; the decision rule, candidate pool and exact request bytes were hashed, committed and pushed before the Jev call.
- Jev was called once; the first valid result is final; no rerun, no regeneration, no manual edits.

## 10. Limitations

- docs.typesafe.ai and supremeventures.com were blocked by the environment's network policy. The Jev request was built from the OpenAPI contract served by api.typesafe.ai (`jev/typesafe_openapi.json`) and the installed TypeSafe skill; the missing draws were not recovered.
- 169 draws is a small sample, so only large effects were detectable; the randomness tests and walk-forward results are both consistent with a fair, independent draw.
- Jev's Choice probabilities rank the strength of evidence cases. They are not probabilities of winning, and the final ticket has exactly the same odds as any other ticket.
