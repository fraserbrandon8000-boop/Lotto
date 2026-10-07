# M0 — Sequential Draw Reconstruction: historical results (exploratory)

Rolling pseudo-prospective reconstruction over **133 targets** (#2211–#2343). For each target the models saw only earlier draws: the full-universe scores were frozen before the realised draw was revealed. Tuning was nested within the prior history. Leakage mutation test (future draws replaced at #2241, #2291, #2343): **PASS = True** for every model. Dataset sha256 `099c244b801ae0a5…`.

Universe C(38,6) = 2,760,681. Expected random rank 1,380,341; mean percentile u = 0.5 (SD 0.0250). Expected Top-K hits in 133: Top-1 0.00005, Top-1,000 0.048, Top-10,000 0.48, Top-100,000 4.8.

## Exact-ticket reconstruction (primary)
| Model | mean u | median rank | rank improvement | p(u<.5) | Holm | Top-1/10/100/1k/10k/100k hits | primary-ticket matches (p) | best match in top 10/100/1000 | mean exact log-score vs uniform | permutation p | gate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M0-A | 0.4882 | 1,336,805 | +3.2% | 0.319 | 1.0 | 0 / 0 / 0 / 0 / 1 / 5 | 0.955 (0.476) | 1.5 / 2.15 / 2.87 | -0.0675 | 1.000 | fail |
| M0-B | 0.5194 | 1,484,128 | -7.5% | 0.781 | 1.0 | 0 / 0 / 0 / 0 / 1 / 4 | 0.902 (0.750) | 1.38 / 1.89 / 2.39 | -0.0161 | 0.776 | fail |
| M0-C | 0.4756 | 1,298,102 | +6.0% | 0.165 | 1.0 | 0 / 0 / 0 / 0 / 1 / 2 | 1.053 (0.081) | 1.59 / 2.14 / 2.82 | -0.0159 | 0.149 | fail |
| M0-D | 0.4998 | 1,380,341 | +0.0% | 0.497 | 1.0 | 0 / 0 / 0 / 0 / 0 / 5 | 0.947 (0.517) | 1.53 / 2.13 / 2.83 | -0.0196 | 1.000 | fail |
| M0-E | 0.4881 | 1,302,349 | +5.7% | 0.317 | 1.0 | 0 / 0 / 0 / 0 / 1 / 5 | 0.970 (0.394) | 1.46 / 2.17 / 2.87 | -0.1451 | 1.000 | fail |
| M0-F | 0.5231 | 1,441,474 | -4.4% | 0.822 | 1.0 | 0 / 0 / 0 / 0 / 0 / 2 | 0.842 (0.936) | 1.34 / 1.98 / 2.63 | -0.0387 | 0.748 | fail |
| M0-G | 0.4893 | 1,336,805 | +3.2% | 0.334 | 1.0 | 0 / 0 / 0 / 0 / 0 / 5 | 0.947 (0.517) | 1.49 / 2.16 / 2.89 | -0.0878 | 1.000 | fail |
| M0-H | 0.4909 | 1,380,341 | +0.0% | 0.358 | 1.0 | 0 / 0 / 0 / 0 / 0 / 1 | 0.985 (0.317) | 1.55 / 2.15 / 2.78 | -0.0160 | 0.251 | fail |
| M0-X | 0.4793 | 1,427,260 | -3.4% | 0.204 | 1.0 | 0 / 0 / 0 / 0 / 0 / 1 | 1.000 (0.247) | 1.69 / 2.0 / 2.95 | — | 0.240 | fail |
| R1-uniform | 0.4622 | 1,178,139 | +14.6% | 0.066 | — | 0 / 0 / 0 / 0 / 0 / 8 | 0.865 (0.886) | nan / nan / nan | — | — | control |
| R2-random-numbers | 0.5062 | 1,358,664 | +1.6% | 0.598 | — | 0 / 0 / 0 / 0 / 1 / 10 | 0.955 (0.476) | 1.41 / 1.98 / 2.56 | -0.2250 | — | control |
| R3-random-rule | 0.5057 | 1,419,227 | -2.8% | 0.589 | — | 0 / 0 / 0 / 0 / 0 / 4 | 0.970 (0.394) | 1.67 / 1.97 / 2.9 | — | — | control |

- Holm family: 26 tests (9 models). **No model passes** (smallest Holm p = 1.00).
- **No model ranked any realised draw inside its Top 1,000.** Top-10,000 and Top-100,000 hit counts match the exact null.
- **Every exact log-score is negative:** no model assigned the realised combinations more probability than uniform.
- The uniform-random control R1 reached mean u 0.462 (p 0.066) purely by chance, a reminder of the noise level.

## Number level
| Model | mean winner rank (null 19.5) | Top-6/10/15/20 capture (null 0.95/1.58/2.37/3.16) | log loss (uniform 0.43616) | Brier (uniform 0.13296) |
|---|---|---|---|---|
| M0-A | 19.36 | 0.89 / 1.49 / 2.41 / 3.16 | 0.43789 | 0.13342 |
| M0-B | 19.74 | 0.77 / 1.49 / 2.29 / 3.03 | 0.43658 | 0.13308 |
| M0-C | 19.07 | 0.87 / 1.61 / 2.50 / 3.17 | 0.43656 | 0.13308 |
| M0-D | 19.45 | 0.68 / 1.12 / 1.66 / 4.08 | 0.43666 | 0.13310 |
| M0-E | 19.36 | 0.89 / 1.49 / 2.41 / 3.16 | 0.44005 | 0.13403 |
| M0-F | 19.98 | 0.84 / 1.47 / 2.20 / 3.02 | 0.43717 | 0.13326 |
| M0-G | 19.36 | 0.89 / 1.49 / 2.41 / 3.16 | nan | nan |
| M0-H | 19.33 | 0.40 / 0.71 / 1.06 / 4.77 | 0.43657 | 0.13308 |
| R2-random-numbers | 19.60 | 0.95 / 1.59 / 2.39 / 3.20 | nan | nan |

## Best reconstructions (lowest exact rank among all 1197 model×target rankings)
| Draw | Actual | Model | Exact rank | Primary ticket (matches) |
|---|---|---|---|---|
| #2308 | 06 08 11 13 20 34 | M0-B | 6,432 | 04 08 11 12 13 19 (3) |
| #2212 | 03 11 14 18 21 24 | M0-A | 6,846 | 02 11 18 19 24 25 (3) |
| #2212 | 03 11 14 18 21 24 | M0-E | 6,862 | 02 11 18 19 24 25 (3) |
| #2219 | 07 18 24 26 28 33 | M0-C | 7,738 | 04 18 25 28 30 33 (3) |
| #2219 | 07 18 24 26 28 33 | M0-X | 11,423 | 04 18 25 28 30 33 (3) |
| #2225 | 05 08 11 17 27 30 | M0-B | 19,871 | 08 12 19 25 27 38 (2) |
| #2341 | 01 04 06 22 33 38 | M0-D | 23,844 | 08 10 18 33 35 38 (2) |
| #2327 | 02 12 14 20 24 27 | M0-F | 31,186 | 02 04 10 12 26 28 (2) |
| #2212 | 03 11 14 18 21 24 | M0-G | 33,184 | 11 19 25 30 33 34 (1) |
| #2341 | 01 04 06 22 33 38 | M0-E | 37,572 | 01 08 18 24 33 38 (3) |

- The best of 1197 rankings was rank 6,432. The expected best of that many random rankings is about 2,304, so even the best case is **not beyond random expectation**.
- Primary tickets never exceeded 4/6 (three times in 1197 model-targets).
- Draws ranked well by the selected model (M0-C) had fewer numbers retained from the previous draw (0.36 vs 1.07). That is the mechanical signature of its fitted mild anti-repeat coefficient. It is descriptive only; no rule is built from it.

## Overfit audit (in-sample = fitted on all draws including the target)
| Model variant | in-sample mean u | out-of-sample mean u | effective params | flag |
|---|---|---|---|---|
| M0-A | 0.376 | 0.4882 | 2 | HISTORICAL FIT, NOT PREDICTION |
| M0-B | 0.466 | 0.5194 | 8 | no overfit flag |
| M0-C | 0.377 | 0.4756 | 8 | HISTORICAL FIT, NOT PREDICTION |
| M0-F | 0.390 | 0.5231 | 13 | HISTORICAL FIT, NOT PREDICTION |
| M0-E (BIC choice K=1) | 0.377 | 0.4881 | 39 | HISTORICAL FIT, NOT PREDICTION |
| M0-E forced K=3 (smoothed, sees target) | 0.154 | 0.4881 | 39 | HISTORICAL FIT, NOT PREDICTION |
| M0-G | 0.376 | 0.4893 | 3 | HISTORICAL FIT, NOT PREDICTION |
| M0-G forced gamma=1 (pairs include target) | 0.179 | 0.4893 | 3 | HISTORICAL FIT, NOT PREDICTION |
| M0-X | 0.517 | 0.4793 | 1 | no overfit flag |

Seeing the target produces apparent reconstruction (u 0.15–0.39). Hiding it removes it (u ≈ 0.48–0.52). **This is HISTORICAL FIT, NOT PREDICTION.**

## Representations (Phase 1, `data/representations.json`)
Extraction order is unavailable; sorted positions are a representation only. Every state representation behaves like its null:
- previous-draw retention: mean 0.951 vs 0.947;
- overlap with the last 2/3/5/10 draws: at the null;
- causal frequency-rank state of drawn numbers: 19.63 vs 19.5;
- prior pair lift of drawn pairs: 0.992 vs 1;
- HMM regimes: BIC selects K = 1;
- best transformation rule mean overlap: 1.050 vs 0.947.

## Null-control note (honest disclosure)
The pre-registered permutation null (R4) pairs each target's frozen scores with other targets' realised draws. **Earlier** targets' draws are training data for the later model, which biases that null against state-accumulating models (p = 1.0 for A, D, E, G). A post-hoc forward-only null (pairing only with later draws, `data/forward_shift_null.json`) gives raw p = 0.024 for A/E/G and ≥ 0.17 for the others. It is uncorrected, uses correlated shifts and was not pre-registered, so it is not evidence and does not change the verdict: every model already fails the primary Holm test (p = 1.0).

## Verdict
**M0 HAS NOT DEMONSTRATED A PREDICTIVE RECONSTRUCTION EDGE.** Historical results are exploratory in any case: this history has been analysed before.

## Selection (charter rule, mechanical)
Lowest out-of-sample mean u: **M0-C** (0.4756). Ranking: M0-C 0.4756, M0-X 0.4793, M0-E 0.4881, M0-A 0.4882, M0-G 0.4893, M0-H 0.4909, M0-D 0.4998, M0-B 0.5194, M0-F 0.5231. It is selected as the single prospective procedure **labelled NO EDGE**.
