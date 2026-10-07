# Statistical audit (A6, A7, A8, A11, A14, A15, A16, A18, A21)

## A6. Does the number ordering predict winners better than random?
Strictly causal origins 2231–2343 (n = 113). Exact nulls: mean winner rank 19.5 (SD per draw 4.16), hypergeometric Top-N capture, simulated MRR/AP. One Holm family of 100 tests.

| Ordering | n | mean winner rank | p | MRR (null) | AP (null) | Top5 | Top10 | Top12 | Top15 | Top18 | Top20 | Top25 | Top30 | Top-15 p | Top-15 Holm | halves (rank z) | block 95% (rank z) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A_long | 113 | 19.55 | 0.554 | 0.1130 (0.1114) | 0.2336 (0.2317) | -0.03 | -0.07 | -0.01 | +0.12 | +0.05 | -0.04 | -0.07 | -0.06 | 0.139 | 1.00 | -0.08 / +0.05 | [-0.26, +0.24] |
| B_recent | 113 | 19.33 | 0.337 | 0.1117 (0.1114) | 0.2334 (0.2317) | +0.04 | +0.08 | -0.00 | +0.06 | +0.10 | +0.13 | +0.03 | +0.02 | 0.309 | 1.00 | -0.01 / +0.09 | [-0.17, +0.25] |
| C_gap | 113 | 19.91 | 0.851 | 0.1108 (0.1114) | 0.2270 (0.2317) | +0.02 | -0.04 | -0.08 | -0.10 | -0.13 | -0.14 | -0.02 | -0.06 | 0.847 | 1.00 | -0.07 / -0.13 | [-0.25, +0.05] |
| D_trend | 113 | 19.35 | 0.355 | 0.1177 (0.1114) | 0.2401 (0.2317) | +0.04 | +0.08 | +0.07 | +0.10 | +0.12 | +0.11 | +0.01 | -0.11 | 0.179 | 1.00 | +0.03 / +0.04 | [-0.15, +0.22] |
| P0_order | 113 | 19.42 | 0.424 | 0.1136 (0.1114) | 0.2361 (0.2317) | -0.00 | -0.01 | +0.04 | +0.15 | +0.10 | +0.05 | +0.05 | -0.06 | 0.077 | 1.00 | -0.04 / +0.07 | [-0.19, +0.24] |
| equal_weight | 113 | 19.40 | 0.397 | 0.1123 (0.1114) | 0.2334 (0.2317) | -0.01 | +0.02 | +0.02 | +0.03 | +0.07 | -0.02 | +0.10 | +0.07 | 0.403 | 1.00 | -0.05 / +0.09 | [-0.18, +0.25] |
| G_proxy | 113 | 19.33 | 0.330 | 0.1121 (0.1114) | 0.2348 (0.2317) | -0.00 | +0.02 | +0.01 | +0.11 | +0.06 | +0.02 | +0.10 | +0.02 | 0.158 | 1.00 | -0.00 / +0.08 | [-0.15, +0.24] |
| uniform_random | 113 | 20.21 | 0.965 | 0.1044 (0.1114) | 0.2205 (0.2317) | -0.11 | -0.30 | -0.26 | -0.18 | -0.19 | -0.05 | -0.10 | -0.08 | 0.963 | 1.00 | -0.10 / -0.23 | [-0.33, +0.00] |
| best_trailing30 | 113 | 19.88 | 0.835 | 0.1094 (0.1114) | 0.2301 (0.2317) | +0.02 | +0.02 | -0.01 | -0.01 | -0.06 | -0.11 | -0.13 | -0.08 | 0.571 | 1.00 | -0.12 / -0.06 | [-0.29, +0.12] |
| bayes_empirical | 113 | 19.44 | 0.434 | 0.1113 (0.1114) | 0.2320 (0.2317) | -0.01 | +0.05 | +0.01 | +0.01 | +0.02 | -0.02 | +0.11 | +0.09 | 0.470 | 1.00 | -0.07 / +0.09 | [-0.20, +0.25] |

(Top-N cells = excess winners captured over 6N/38.) Smallest raw p 0.077 (P0_order:top15); smallest Holm p 1.00. The uniform-random ordering's spread shows the noise level.

**THE CURRENT NUMBER ORDERING DOES NOT PREDICT WINNERS BETTER THAN RANDOM.** Calibration/Brier: the conditional-Bernoulli fit (A9) is the calibrated version of each ordering; its causal β is ≤ 0 on average, so calibrated inclusion probabilities collapse to 6/38 and the Brier skill is ≤ 0.

### P0 ordering by pool size (A6/A7)
| Pool | mean captured | random | excess | P(≥2/3/4/5/6) | random | conf. excess | p | Holm |
|---|---|---|---|---|---|---|---|---|
| Top 5 | 0.788 | 0.789 | -0.002 | 0.18 / 0.01 / 0.00 / 0.00 / 0.00 | 0.17 / 0.02 / 0.00 / 0.00 / 0.00 | +0.011 | 0.530 | 1.00 |
| Top 10 | 1.566 | 1.579 | -0.013 | 0.51 / 0.24 / 0.03 / 0.00 / 0.00 | 0.51 / 0.17 / 0.03 / 0.00 / 0.00 | -0.054 | 0.569 | 1.00 |
| Top 12 | 1.938 | 1.895 | +0.043 | 0.65 / 0.33 / 0.08 / 0.01 / 0.00 | 0.63 / 0.27 / 0.07 / 0.01 / 0.00 | +0.130 | 0.347 | 1.00 |
| Top 15 | 2.522 | 2.368 | +0.154 | 0.79 / 0.51 / 0.21 / 0.05 / 0.00 | 0.78 / 0.44 / 0.15 / 0.03 / 0.00 | +0.357 | 0.077 | 1.00 |
| Top 18 | 2.947 | 2.842 | +0.105 | 0.88 / 0.68 / 0.32 / 0.10 / 0.00 | 0.88 / 0.62 / 0.28 / 0.07 / 0.01 | +0.358 | 0.174 | 1.00 |
| Top 20 | 3.212 | 3.158 | +0.054 | 0.92 / 0.74 / 0.41 / 0.17 / 0.00 | 0.93 / 0.72 / 0.38 / 0.12 / 0.01 | +0.267 | 0.320 | 1.00 |
| Top 25 | 4.000 | 3.947 | +0.053 | 0.96 / 0.88 / 0.67 / 0.41 / 0.10 | 0.99 / 0.91 / 0.67 / 0.31 / 0.06 | +0.303 | 0.319 | 1.00 |
| Top 30 | 4.673 | 4.737 | -0.064 | 1.00 / 0.96 / 0.87 / 0.61 / 0.23 | 1.00 / 0.99 / 0.91 / 0.63 / 0.22 | -0.012 | 0.785 | 1.00 |

No pool size captures more than its size implies. Larger pools only capture more mechanically.

## A7. Hard Top-15 cutoff
Full-universe scoring of all 2,760,681 combinations takes 8.77 s. At the 31 origins where P0 weights were non-zero, the full-universe best ticket was always inside the Top-15 pool (best pool ticket = full rank 1). But only 56% of the full top-1,000 lie inside it (83% at Top 20, 95% at Top 25). The cutoff does not hide the single best-scoring ticket. It does remove most near-best alternatives and **forces overlap** whenever ticket 1 occupies pool numbers (at #2343 V1 held 5 of the 15). A wider universe creates no skill; it removes an unnecessary constraint.

## A8. Score calibration
Family scores are z-scores over the 38 numbers (SDs [1.0, 1.0, 1.0, 1.0, 0.0]; E_pairs flat = 0), so families are commensurate. But: (i) universe components are Z-normalised **within the pool**, so their relative scale depends on K; (ii) frozen weights are tiny (B 0.031, D 0.024, struct 0.007), so T has SD 0.043 while the coverage term has SD 0.152 (**3.5×**): coverage, not evidence, picks the tickets; (iii) T is not a probability. Sign conventions are consistent (C_gap: longer absence = higher score, an explicit "overdue" hypothesis). Ties are broken deterministically by EQ, then number.

## A11. Fixed-seed / repeated-ticket designs (V1 chain, targets [2211, 2343])
| Design | total matches (exp 126) | p(≥obs) | ≥3 (exp 5.1) | distinct tickets | distinct IDs | top-ticket share | consecutive overlap | lag-2 exact repeat |
|---|---|---|---|---|---|---|---|---|
| fixed_current_seed | 114 | 0.91 | 7 | 101 | 5 | 0.045 | 0.73 | 0.122 |
| per_draw_seed | 133 | 0.25 | 6 | 71 | 20 | 0.083 | 0.89 | 0.046 |
| rotating_index | 119 | 0.78 | 6 | 80 | 20 | 0.068 | 0.91 | 0.015 |
| no_repeated_position | 120 | 0.75 | 6 | 106 | 5 | 0.030 | 0.60 | 0.107 |
| fixed_seed_without_overlap_rule | 129 | 0.39 | 6 | 66 | 1 | 0.053 | 3.17 | 0.153 |
| uniform candidate (expectation) | 125.9 | — | — | — | — | — | — | — |

1. **Predictive performance:** no design differs from chance (all p ≥ 0.25). Repeating a ticket does not change its per-draw jackpot probability.
2. **Exploration:** the fixed seed concentrates on 5 candidate IDs, and with the overlap rule live V1 played only two distinct tickets in five draws. Per-draw seeding or rotation explore far more. This is an experiment-quality issue, not a predictive one.

## A14. Leakage
Mutation test (all draws at and after the target replaced by random draws) at 4 origins: features, P0 weights, P0 order and V1 candidates are identical. **PASS = True.** Code review: rolling windows, EW, gaps, trends, pair Holm tests, ensemble weights (prior walk rows only), structure means/SDs and P0 reliability weights (prior origins only) all use `d[:t]`.

## A15. Holdout contamination — CRITICAL
Draws 2299–2343 have each been used as "confirmation" by up to **7 separate studies** (43 draws used ≥3 times), and every forensic inspected them. They are **not** a pristine holdout. Historical "confirmation" results are descriptive from now on.

**Validation hierarchy (adopted for future research):**
1. Development: rolling-origin walk-forward over the full history.
2. Historical pseudo-holdout: descriptive only, never sufficient for promotion.
3. **Prospective live draws after a protocol is frozen are the only promotion evidence.**

## A16. Cumulative multiple testing — CRITICAL
`RESEARCH_REGISTRY.json`: **385 formal tests** across 10 Lotto studies (plus about 3,802 exploratory comparisons). Holm was applied within each batch only. Bonferroni at the cumulative family gives α = 1.3e-04 per test; **no result anywhere comes close**. Because every promotion test failed, no false discovery entered production, but batch-wise correction understates the risk.

**Policy:**
- Every new hypothesis is added to the registry before testing.
- Promotion requires a pre-registered prospective test with a fixed α budget (α = 0.05 split across all challengers alive at the time).
- Shadows accumulate live evidence only.
- No historical re-test can promote.

## A18. Random control
The fixed control (seed 20260930) repeats the same three tickets every draw. That is a valid but very noisy single-portfolio null. It is kept unchanged for continuity. From #2344 research also records:
- a per-draw seeded random portfolio;
- the exact null pmf of best-ticket matches for the played portfolio's overlap structure (enumerated).

Historical controls are not changed.

## A21. Prospective record (re-scored from frozen artifacts)
| Draw | Track | Ticket | Result | mains | matched | bonus on ticket (not a main match) | generator | Jev favourite (its matches) |
|---|---|---|---|---|---|---|---|---|
| 2339 | V1_primary | 01 · 04 · 13 · 14 · 24 · 38 | 01 · 04 · 06 · 13 · 23 · 28 + 20 | 3 | 01, 04, 13 | no | B_recent | C02 (1) |
| 2339 | V1_secondary | 02 · 06 · 08 · 12 · 18 · 25 | 01 · 04 · 06 · 13 · 23 · 28 + 20 | 1 | 06 | no | A_long | C02 (1) |
| 2340 | V1 | 05 · 11 · 16 · 24 · 27 · 34 | 06 · 08 · 12 · 14 · 18 · 31 + 28 | 0 | — | no | C_gap | C02 (1) |
| 2341 | V1 | 01 · 04 · 13 · 14 · 24 · 38 | 01 · 04 · 06 · 22 · 33 · 38 + 34 | 3 | 01, 04, 38 | no | B_recent | C04 (3) |
| 2342 | V1 | 05 · 11 · 16 · 24 · 27 · 34 | 12 · 13 · 14 · 15 · 19 · 33 + 21 | 0 | — | no | C_gap | C03 (2) |
| 2342 | P0_coverage_1 | 01 · 02 · 04 · 13 · 22 · 38 | 12 · 13 · 14 · 15 · 19 · 33 + 21 | 1 | 13 | no | P0 | C03 (2) |
| 2342 | P0_coverage_2 | 08 · 09 · 10 · 12 · 14 · 18 | 12 · 13 · 14 · 15 · 19 · 33 + 21 | 2 | 12, 14 | no | P0 | C03 (2) |
| 2342 | random_control_1 | 12 · 14 · 15 · 17 · 20 · 29 | 12 · 13 · 14 · 15 · 19 · 33 + 21 | 3 | 12, 14, 15 | no | random | C03 (2) |
| 2342 | random_control_2 | 13 · 19 · 25 · 26 · 28 · 29 | 12 · 13 · 14 · 15 · 19 · 33 + 21 | 2 | 13, 19 | no | random | C03 (2) |
| 2342 | random_control_3 | 01 · 08 · 20 · 21 · 33 · 36 | 12 · 13 · 14 · 15 · 19 · 33 + 21 | 1 | 33 | yes | random | C03 (2) |
| 2343 | V1 | 01 · 04 · 13 · 14 · 24 · 38 | 04 · 07 · 13 · 23 · 33 · 35 + 38 | 2 | 04, 13 | yes | B_recent | C04 (2) |
| 2343 | P0_coverage_1 | 02 · 06 · 07 · 08 · 12 · 22 | 04 · 07 · 13 · 23 · 33 · 35 + 38 | 1 | 07 | no | P0 | C04 (2) |
| 2343 | P0_coverage_2 | 04 · 09 · 10 · 13 · 18 · 33 | 04 · 07 · 13 · 23 · 33 · 35 + 38 | 3 | 04, 13, 33 | no | P0 | C04 (2) |
| 2343 | random_control_1 | 12 · 14 · 15 · 17 · 20 · 29 | 04 · 07 · 13 · 23 · 33 · 35 + 38 | 0 | — | no | random | C04 (2) |
| 2343 | random_control_2 | 13 · 19 · 25 · 26 · 28 · 29 | 04 · 07 · 13 · 23 · 33 · 35 + 38 | 1 | 13 | no | random | C04 (2) |
| 2343 | random_control_3 | 01 · 08 · 20 · 21 · 33 · 36 | 04 · 07 · 13 · 23 · 33 · 35 + 38 | 1 | 33 | no | random | C04 (2) |

V1 (#2339–#2343): 3, 0, 3, 0, 2 = 8 vs 4.74 expected (P(≥8) = 0.073). Two ≥3 tickets in 5 (nominal p 0.014, chosen after seeing the data). **Only 2 distinct V1 tickets were played.** P0 best single ticket: #2342 2, #2343 3; fixed random control best: 3, 1. Exact single-ticket null: P(≥3) = 0.0387, P(≥4) = 0.00276, P(6) = 3.622e-07. **Everything is consistent with chance; the 3,0,3,0,2 sequence is two tickets played repeatedly.**
