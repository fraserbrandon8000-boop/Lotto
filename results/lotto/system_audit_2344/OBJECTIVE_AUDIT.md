# Objective audit (A2, A3, A4, A5, A9, A22 construction)

**User objective:** at least one of three played tickets matches all six mains. Universe C(38,6) = 2,760,681.

## A2. The jackpot probability of a portfolio (exact)

For distinct tickets the events "draw = ticket i" are disjoint, so

P(at least one 6/6) = Σᵢ P(draw = ticketᵢ).

Under a uniform (no-edge) draw each term is 1/C(38,6), so **any three distinct tickets give exactly 3/C(38,6) = 1.0867e-06** (1 in 920,227), whatever their overlap, number spread or coverage. Verified by enumerating all 2,760,681 draws for seven structures (`data/a2_objective.json`, verified = True):

| Structure | distinct tickets | unique numbers | P(6/6) | P(best ≥5) | P(best ≥4) | P(best ≥3) | E[best] | E[total matches] | E[unique winners covered] |
|---|---|---|---|---|---|---|---|---|---|
| zero_overlap (18 numbers) | 3 | 18 | 1.0867e-06 | 2.097e-04 | 0.00829 | 0.11566 | 1.7163 | 2.842 | 2.842 |
| one_shared_each (pairwise 1) | 3 | 15 | 1.0867e-06 | 2.097e-04 | 0.00829 | 0.11286 | 1.6319 | 2.842 | 2.368 |
| frozen_2343_structure (0,2,0) | 3 | 16 | 1.0867e-06 | 2.097e-04 | 0.00828 | 0.11233 | 1.6592 | 2.842 | 2.526 |
| pairwise 2 (coverage-style) | 3 | 12 | 1.0867e-06 | 2.097e-04 | 0.00826 | 0.10605 | 1.5243 | 2.842 | 1.895 |
| pairwise 3 | 3 | 9 | 1.0867e-06 | 2.097e-04 | 0.00797 | 0.09533 | 1.3722 | 2.842 | 1.421 |
| concentration (5 shared) | 3 | 8 | 1.0867e-06 | 1.804e-04 | 0.00602 | 0.06969 | 1.2015 | 2.842 | 1.263 |
| three identical tickets | 1 | 6 | 3.6223e-07 | 6.991e-05 | 0.00276 | 0.03870 | 0.9474 | 2.842 | 0.947 |

What this proves:
- **Maximising unique-number coverage, minimising overlap and spreading numbers do not change P(6/6).** They are not jackpot optimisation.
- **Expected total portfolio matches is identical (2.842) for every portfolio**, so it cannot be optimised at all; it is pure noise as a success metric.
- Unique winners covered rises with the union size, but a winner on another ticket does nothing for 6/6 (the #2342 random control covered 6 winners across tickets with a best of 3).
- Low overlap **does** maximise the secondary tiers: zero overlap gives the highest P(4+), P(3+) and E[best] of all structures; P(5+) is maximal for every structure with pairwise overlap ≤3. Concentration (five shared numbers) lowers every secondary tier without raising P(6/6).

## A9. Can P(exact combination) be estimated better than uniform?

Model: conditional-Bernoulli (exponential family on 6-subsets) P(S) ∝ Πᵢ∈S exp(β·sᵢ), β fitted by maximum likelihood on prior origins only. This is the defensible way to turn number scores into exact-ticket probabilities (it does not multiply uncalibrated marginals). Score = log P_model(realised combination) − log(1/C), averaged over 113 causal targets:

| Score vector | mean log-ratio vs uniform | implied multiplier on the realised ticket | p (one-sided) | causal β (mean / range) | confirmation mean | best in-sample (hindsight) mean |
|---|---|---|---|---|---|---|
| P0_M | +0.0000 | 1.0000 | 0.404 | -0.580 / [-0.77, +0.16] | -0.0109 | +0.0023 |
| equal_weight | -0.0103 | 0.9897 | 0.772 | -0.076 / [-0.19, +0.14] | -0.0135 | +0.0001 |
| A_long | -0.0118 | 0.9883 | 0.792 | -0.027 / [-0.08, +0.09] | -0.0176 | +0.0001 |
| B_recent | -0.0080 | 0.9920 | 0.795 | -0.024 / [-0.09, +0.05] | -0.0066 | +0.0002 |
| C_gap | -0.0059 | 0.9941 | 0.985 | -0.004 / [-0.02, +0.02] | -0.0039 | +0.0013 |
| D_trend | -0.0087 | 0.9914 | 0.957 | -0.017 / [-0.06, +0.01] | -0.0066 | +0.0001 |

**No score assigns the realised combinations more probability than uniform.** The causally fitted β is near zero or negative, and even the best in-sample (hindsight) β gains ≤0.0023 nats per draw (a jackpot-probability multiplier of ≤1.002). **The defensible estimate of P(exact ticket) is 1/C(38,6) for every ticket.** So Σ P(ticket) cannot be raised by construction with present evidence.

## A3. Concentration vs coverage, historical (targets 2231–2343, n = 113, strictly causal)

Primary = best single-ticket matches against the **exact null of that portfolio's own overlap structure** (enumerated over all C(38,6) draws per origin). Secondary/diagnostic columns at the right. Holm across the 8 strategies.

| Strategy | best (obs) | best (null) | excess | p | Holm | ≥3 (exp) | ≥4 (exp) | ≥5 (exp) | 6/6 | conf. excess | halves | block 95% | total | unique winners | unique numbers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A_coverage_P0 | 1.717 | 1.676 | +0.041 | 0.294 | 1.00 | 16 (12.8) | 2 (0.94) | 0 (0.024) | 0 | +0.219 | -0.012 / +0.093 | [-0.10, +0.18] | 2.86 | 2.67 | 16.6 |
| B_top3_standalone | 1.088 | 1.158 | -0.069 | 0.815 | 1.00 | 5 (7.5) | 0 (0.65) | 0 (0.020) | 0 | -0.030 | -0.127 / -0.013 | [-0.23, +0.10] | 2.72 | 1.15 | 7.6 |
| C_best_plus_2_diversified | 1.619 | 1.549 | +0.071 | 0.186 | 1.00 | 15 (12.0) | 3 (0.93) | 0 (0.024) | 0 | +0.301 | -0.048 / +0.187 | [-0.08, +0.23] | 2.89 | 2.13 | 13.0 |
| D_concentration_top_numbers | 1.159 | 1.202 | -0.042 | 0.714 | 1.00 | 10 (7.9) | 0 (0.68) | 0 (0.020) | 0 | -0.002 | -0.094 / +0.009 | [-0.21, +0.13] | 2.77 | 1.19 | 8.0 |
| E_hybrid_score_coverage | 1.602 | 1.629 | -0.027 | 0.673 | 1.00 | 16 (12.5) | 2 (0.94) | 0 (0.024) | 0 | +0.113 | -0.072 / +0.017 | [-0.18, +0.12] | 2.77 | 2.36 | 15.3 |
| F_V1_plus_2_random | 1.673 | 1.637 | +0.036 | 0.325 | 1.00 | 18 (12.6) | 3 (0.93) | 0 (0.024) | 0 | +0.160 | +0.009 / +0.062 | [-0.12, +0.20] | 2.74 | 2.34 | 15.4 |
| G_3_random | 1.531 | 1.634 | -0.103 | 0.938 | 1.00 | 9 (12.6) | 0 (0.93) | 0 (0.024) | 0 | -0.090 | -0.216 / +0.007 | [-0.22, +0.01] | 2.67 | 2.32 | 15.3 |
| H_V1_plus_2_zero_overlap_by_T | 1.796 | 1.716 | +0.080 | 0.127 | 1.00 | 19 (13.1) | 1 (0.94) | 0 (0.024) | 0 | +0.234 | -0.002 / +0.161 | [-0.04, +0.20] | 2.88 | 2.88 | 18.0 |

- A = current P0 (V1 + coverage challengers); B = top-3 standalone T; C = best T + 2 diversified (overlap ≤2); D = concentration on top-ranked numbers (Top-6, Top-5+7th, Top-5+8th); E = V1 + standardised T/coverage hybrid; F = V1 + 2 random; G = 3 random; H = V1 + 2 tickets with zero overlap, ranked by T.
- The no-edge P(6/6) per draw is **1.0867e-06 for every strategy** (3 distinct tickets). No 5/6 or 6/6 occurred in any strategy.
- **No strategy beats its own null** (all Holm p = 1.0). Concentration strategies (B, D) have the lowest best-ticket means because their null expectation is lowest (they repeat numbers); they do not concentrate winners because the ranking that drives them has no skill (A6).
- Differences between A, C, F, H are what their overlap structures predict under the null.

## A5. Conditional construction efficiency (in-pool winners only)

**A_coverage_P0**

| K winners in pool | draws | E[best] | E[2nd] | E[portfolio in-pool winners] | max possible | efficiency | random: 1 pool ticket | best of 2 random | best of 3 random |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 5 | 0.00 | 0.00 | 0.00 | 0 | None | 0.00 | 0.00 | 0.00 |
| 1 | 19 | 0.89 | 0.11 | 0.89 | 1 | 0.89 | 0.40 | 0.64 | 0.78 |
| 2 | 31 | 1.32 | 0.45 | 1.74 | 2 | 0.66 | 0.80 | 1.15 | 1.33 |
| 3 | 34 | 1.82 | 0.94 | 2.88 | 3 | 0.61 | 1.20 | 1.62 | 1.83 |
| 4 | 18 | 2.33 | 1.39 | 3.83 | 4 | 0.58 | 1.60 | 2.07 | 2.30 |
| 5 | 6 | 2.83 | 1.67 | 4.33 | 5 | 0.57 | 2.00 | 2.50 | 2.75 |

**B_top3_standalone**

| K winners in pool | draws | E[best] | E[2nd] | E[portfolio in-pool winners] | max possible | efficiency | random: 1 pool ticket | best of 2 random | best of 3 random |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 5 | 0.00 | 0.00 | 0.00 | 0 | None | 0.00 | 0.00 | 0.00 |
| 1 | 19 | 0.42 | 0.32 | 0.42 | 1 | 0.42 | 0.40 | 0.64 | 0.78 |
| 2 | 31 | 0.90 | 0.65 | 0.90 | 2 | 0.45 | 0.80 | 1.15 | 1.33 |
| 3 | 34 | 1.29 | 1.12 | 1.32 | 3 | 0.43 | 1.20 | 1.62 | 1.83 |
| 4 | 18 | 1.61 | 1.50 | 1.89 | 4 | 0.4 | 1.60 | 2.07 | 2.30 |
| 5 | 6 | 2.33 | 2.00 | 2.50 | 5 | 0.47 | 2.00 | 2.50 | 2.75 |

**D_concentration_top_numbers**

| K winners in pool | draws | E[best] | E[2nd] | E[portfolio in-pool winners] | max possible | efficiency | random: 1 pool ticket | best of 2 random | best of 3 random |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 5 | 0.00 | 0.00 | 0.00 | 0 | None | 0.00 | 0.00 | 0.00 |
| 1 | 19 | 0.42 | 0.32 | 0.42 | 1 | 0.42 | 0.40 | 0.64 | 0.78 |
| 2 | 31 | 0.97 | 0.55 | 0.97 | 2 | 0.48 | 0.80 | 1.15 | 1.33 |
| 3 | 34 | 1.38 | 1.00 | 1.41 | 3 | 0.46 | 1.20 | 1.62 | 1.83 |
| 4 | 18 | 1.72 | 1.39 | 1.89 | 4 | 0.43 | 1.60 | 2.07 | 2.30 |
| 5 | 6 | 2.50 | 1.83 | 2.50 | 5 | 0.5 | 2.00 | 2.50 | 2.75 |

**C_best_plus_2_diversified**

| K winners in pool | draws | E[best] | E[2nd] | E[portfolio in-pool winners] | max possible | efficiency | random: 1 pool ticket | best of 2 random | best of 3 random |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 5 | 0.00 | 0.00 | 0.00 | 0 | None | 0.00 | 0.00 | 0.00 |
| 1 | 19 | 0.79 | 0.26 | 0.79 | 1 | 0.79 | 0.40 | 0.64 | 0.78 |
| 2 | 31 | 1.42 | 0.68 | 1.68 | 2 | 0.71 | 0.80 | 1.15 | 1.33 |
| 3 | 34 | 1.82 | 1.03 | 2.59 | 3 | 0.61 | 1.20 | 1.62 | 1.83 |
| 4 | 18 | 2.50 | 1.56 | 3.50 | 4 | 0.62 | 1.60 | 2.07 | 2.30 |
| 5 | 6 | 2.83 | 2.00 | 3.83 | 5 | 0.57 | 2.00 | 2.50 | 2.75 |

The current constructor (A) places in-pool winners on its best ticket at about the rate of the best of three random pool tickets, slightly above best-of-two. Concentration strategies (B, D) put **fewer** in-pool winners on their best ticket than one random pool ticket would at K = 2–4, because concentration follows the (skill-less) ranking. **Once discovery finds winners, no constructor can concentrate them without knowing which pool numbers won.** That information does not exist before the draw.

## A4 / A22. #2342 and #2343 construction counterfactuals (diagnosis only; nothing promoted)

| | #2342 | #2343 |
|---|---|---|
| available in-pool winners | 12, 13, 14 | 04, 07, 13, 33 |
| pool tickets containing all of them | 220 (random count 220) | 55 (random count 55) |
| raw-T rank of those tickets: best / median / worst (of 5,005) | 22 / 2266 / 4518 | 159 / 848 / 2015 |
| best such ticket | 01 · 04 · 12 · 13 · 14 · 24 | 04 · 07 · 12 · 13 · 24 · 33 |
| available winners on frozen V1 / T2 / T3 | [0, 1, 2] | [2, 1, 3] |
| frozen T2 / T3 raw-T rank | [116, 4952] | [4084, 1957] |
| standalone top-3 tickets: available winners each | [1, 2, 1] | [2, 2, 2] |
| concentration (Top-6 numbers): available winners | 1 | 2 |

- **#2343:** 04 and 13 were P0 ranks 2 and 1, 07 rank 9, 33 rank 15. A 4-winner ticket needs 07 and 33 next to 04 and 13, but the T ordering ranks such tickets 159th at best. **No pre-draw objective (standalone, concentration or hybrid) would have chosen one**; each puts the top-ranked numbers (13, 04, 12, 14, 24) together, so they hold 2 available winners. The frozen portfolio split the four because V1 already held 04 and 13 (5 of its 6 numbers are pool numbers), and the coverage term (SD 3.5× the T SD) pushes the challengers onto other pool numbers.
- **#2342:** 220 pool tickets contained 12, 13 and 14; the best was ranked 22nd; the standalone top-3 held 1, 2 and 1.
- **Conclusion:** both "split" outcomes are what any objective without knowledge of the winners produces. The split is not a construction defect, and concentrating would not have helped before the draw.

## Rational 3-ticket policy
- **A. No predictive edge (current state):** P(6/6) = 3/C(38,6) for any 3 distinct tickets, so the jackpot objective is **indifferent** among them. The rational choice then maximises the secondary tiers exactly: **three pairwise-disjoint tickets** (maximal P(5+), P(4+), P(3+), E[best]). Ticket identity can be set by any pre-declared rule (evidence tie-break or seeded random) at zero jackpot cost.
- **B. Weak, unvalidated signal:** its value for 6/6 is bounded by its prospective likelihood ratio, measured here as ≤1 (A9). Use it **only as a tie-break inside the secondary-optimal set**, because following it costs nothing if it is noise but concentrating on it costs secondary tiers for no demonstrated jackpot gain.
- **C. Genuinely calibrated signal (P̂(S) validated prospectively):** maximise Σ P̂(Sᵢ), i.e. **the three highest-P̂ distinct combinations, with no diversity penalty** (diversity would trade jackpot probability for lower tiers). Switch rule: only when the A9 log-score passes the prospective gate (see `results/lotto/protocol_2344/PROTOCOL.md`).
