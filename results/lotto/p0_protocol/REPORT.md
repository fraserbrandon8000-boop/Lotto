# P0 portfolio research protocol (frozen)

Frozen 2026-09-29T02:35:29 UTC, before any P0 evaluation of #2341. Implements the design pre-commitment `DESIGN_PRECOMMIT.json` (commit `a0b2f39`, SHA-256 `d8d9c8b2687de54f…`), which was written before the #2341 forensic ranking analysis. All data-driven quantities were computed from `results/lotto/draw2341/draws.json` (history 2161–2340; the code asserts #2341 is absent). **P0 is not Lotto V2** and never changes V1.

## Frozen constants

| Component | n origins | Standardized mean evidence | Shrunk d | Stability h | **Weight** |
|---|---|---|---|---|---|
| A_long | 130 | -0.0017 | -0.0009 | 0.5 | **0.0000** |
| B_recent | 130 | +0.0613 | +0.0314 | 1.0 | **0.0314** |
| C_gap | 130 | -0.0888 | -0.0456 | 0.0 | **0.0000** |
| D_trend | 130 | +0.0463 | +0.0238 | 1.0 | **0.0238** |
| E_pairs | 0 | — | +0.0000 | 0.0 | **0.0000** |
| pair | 0 | — | +0.0000 | 0.0 | **0.0000** |
| struct | 130 | +0.0263 | +0.0135 | 0.5 | **0.0067** |

Formula: `w_f = max(0, d_f) * h_f; d_f = dbar_f * n tau^2/(n tau^2 + 1); dbar_f = mean(x_f,u)/sigma; tau = 0.09; sigma = 0.112522; n >= 20`. E_pairs never retained a Holm-significant pair at any of the 130 origins, so E_pairs and the pair component are flat (weight 0). G is derived from A–E (weight 0, no double counting); F has no number-level representation (it enters only as the ticket-level `struct` component); H is a control. Weights are frozen as constants for the #2341 shadow and #2342 and are not updated with #2341.

- Discovery pool: **Top 15**, basis: NO EDGE: predeclared default K=15 (no pool size passed on the development period).
- Universe: all C(15,6) = 5,005 combinations enumerated.
- Ticket score T = Σ w·Z(component); portfolio objective J = T + 1.0·Cov; overlap ≤ 2 with every selected ticket (relax to 3/4 only if infeasible); evidence exception at 2.0 SD of T as pre-committed.

## Number-discovery reliability (130 V1 origins, targets 2211–2340)

| Family | Mean winner midrank (random 19.5) | Mean percentile excess | z | Holm p | Confirmation excess | Halves | Top-12 capture (1.89) | Top-20 capture (3.16) |
|---|---|---|---|---|---|---|---|---|
| A_long | 19.51 | -0.0002 | -0.02 | 1.00 | +0.0068 | -0.0008 / +0.0004 | 1.90 | 3.17 |
| B_recent | 19.24 | +0.0069 | +0.70 | 0.97 | +0.0089 | +0.0046 / +0.0092 | 1.93 | 3.32 |
| C_gap | 19.87 | -0.0100 | -1.01 | 1.00 | -0.0265 | -0.0074 / -0.0126 | 1.76 | 3.05 |
| D_trend | 19.31 | +0.0052 | +0.53 | 0.97 | +0.0052 | +0.0058 / +0.0046 | 1.95 | 3.23 |
| E_pairs | flat at every origin | | | | | | | |

Score correlations: A~B 0.58, B~D 0.48, B~C -0.48, C~D -0.43, A~D -0.00. No family has corrected evidence (all Holm p ≥ 0.97). The positive weights for B_recent and D_trend are shrinkage of statistically null evidence, not a signal. Weight sensitivity to τ (reported only): τ=0.05 → B 0.015, D 0.011; τ=0.18 → B 0.050, D 0.037.

## Discovery-pool size (development targets 2231–2300 only)

| K | Mean winners captured | Random | Excess | z | Holm p | Halves | Block 95% | Confirmation excess (reported) |
|---|---|---|---|---|---|---|---|---|
| 10 | 1.586 | 1.579 | +0.007 | +0.06 | 1.00 | +0.021 / -0.008 | [-0.24, +0.25] | -0.129 |
| 12 | 1.900 | 1.895 | +0.005 | +0.04 | 1.00 | +0.048 / -0.038 | [-0.22, +0.23] | +0.030 |
| 15 | 2.400 | 2.368 | +0.032 | +0.24 | 1.00 | -0.026 / +0.089 | [-0.21, +0.27] | +0.282 |
| 20 | 3.086 | 3.158 | -0.072 | -0.53 | 1.00 | -0.101 / -0.044 | [-0.32, +0.16] | +0.142 |

Excess is measured against the exact hypergeometric expectation 6K/38, which removes the mechanical advantage of larger pools. No K passed, so the predeclared default **K=15** is used and labelled **NO EDGE**.

## Historical walk-forward portfolio test (K=15)

Ticket 1 is the V1-style reconstruction (validated candidate generator, V1 gate, fixed-seed fallback with the ≤2-overlap chain). Random comparators average 200 replicates per origin.

**Development** (70 targets)

| Metric | P0 | A: 3 random | B: 3 random, overlap ≤2 | C: V1 + 2 random | D: top-3 standalone | P0 − C (95% CI) |
|---|---|---|---|---|---|---|
| best-ticket matches | 1.614 | 1.643 | 1.642 | 1.621 | 1.057 | -0.007 [-0.18, +0.19] |
| total portfolio matches | 2.729 | 2.856 | 2.851 | 2.671 | 2.614 | +0.058 [-0.21, +0.37] |
| tickets 2+3 matches | 1.957 | 1.897 | 1.898 | 1.899 | 1.743 | +0.058 [-0.21, +0.37] |
| P(any ticket ≥3) | 0.114 | 0.113 | 0.110 | 0.130 | 0.057 | -0.016 [-0.07, +0.05] |
| P(any ticket ≥4) | 0.014 | 0.009 | 0.008 | 0.004 | 0.000 | +0.010 [-0.00, +0.04] |
| P(any ticket ≥5) | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | -0.000 [-0.00, +0.00] |
| P(6/6) | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | +0.000 [+0.00, +0.00] |
| unique numbers | 16.500 | 15.312 | 15.508 | 15.524 | 7.571 | +0.976 [+0.72, +1.20] |
| mean pairwise overlap | 0.524 | 0.946 | 0.868 | 0.861 | 5.000 | -0.337 [-0.42, -0.24] |

**Confirmation** (40 targets)

| Metric | P0 | A: 3 random | B: 3 random, overlap ≤2 | C: V1 + 2 random | D: top-3 standalone | P0 − C (95% CI) |
|---|---|---|---|---|---|---|
| best-ticket matches | 1.850 | 1.624 | 1.634 | 1.703 | 1.100 | +0.147 [-0.02, +0.33] |
| total portfolio matches | 2.975 | 2.835 | 2.830 | 2.873 | 2.750 | +0.102 [-0.23, +0.45] |
| tickets 2+3 matches | 2.000 | 1.903 | 1.885 | 1.898 | 1.875 | +0.102 [-0.23, +0.45] |
| P(any ticket ≥3) | 0.175 | 0.109 | 0.110 | 0.151 | 0.025 | +0.024 [-0.06, +0.12] |
| P(any ticket ≥4) | 0.025 | 0.007 | 0.009 | 0.030 | 0.000 | -0.005 [-0.01, -0.00] |
| P(any ticket ≥5) | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | +0.000 [+0.00, +0.00] |
| P(6/6) | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | +0.000 [+0.00, +0.00] |
| unique numbers | 16.775 | 15.281 | 15.528 | 15.505 | 7.550 | +1.270 [+1.04, +1.49] |
| mean pairwise overlap | 0.408 | 0.957 | 0.860 | 0.869 | 4.975 | -0.461 [-0.54, -0.39] |

## Evidence gate (confirmation, 40 targets): **FAIL**

- E1 tickets 2+3 total matches: 80 vs 75.8 expected, p = 0.294, Holm p = 0.327, mean excess +0.105 per draw, block 95% [-0.22, +0.46], halves +0.305 / -0.095.
- E2 best-ticket matches: 74, p = 0.086, Holm p = 0.259.
- E3 draws with a ≥3 ticket: 7 of 40, p = 0.164, Holm p = 0.327.

**The portfolio is a coverage experiment, not a demonstrated predictive edge.** P0 reliably covers more distinct numbers (about 1.3 more than V1 + 2 random, lower overlap), but its match differences against every comparator have confidence intervals that include zero.

## Implementation notes
- Ticket 1 history is a V1-style reconstruction; it does not equal the actual prospective tickets at #2339/#2340 (those runs started without, or from a different, previous-ticket chain). G_ensemble passed the V1 gate at targets 2249, 2250, 2251, 2252 (early, short histories); those origins use the fallback ticket and are flagged.
- The pre-committed evidence exception fired 12 times for ticket 3 at K=15, but the tickets it allowed never broke the ≤2-overlap rule (0 violations, 0 relaxations at K=15). Violations occur only at the unselected K=10/12, where the V1 ticket can occupy most of a small pool.
