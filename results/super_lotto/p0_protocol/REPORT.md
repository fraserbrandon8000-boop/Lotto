# Super Lotto P0 portfolio protocol (frozen)

Frozen 2026-09-30T00:39:13 UTC, before any Super Lotto P0 shadow evaluation. Implements the Super-Lotto-specific pre-commitment `DESIGN_PRECOMMIT.json` (commit `c3cbcd6`, SHA-256 `3da3580791aa99c6…`), written before the #1754 forensic ranking analysis. Every data-driven quantity comes from `results/super_lotto/draw1754/draws.json` (history 1577–1753; the code asserts #1754 is absent). **No Lotto code, data, weights or formulas are used. P0 is not V2** and never changes V1.

## Frozen credibility weights (design cutoff #1753)

Formula: `c = max(0, 1 - 2*p_Holm) * [both halves positive]; p from mean AP excess (main), mean SB percentile excess (SB), exact hypergeometric total hits (E/F tickets); minimum 25 prior origins`.

| Component | n | Mean excess | one-sided p | Holm p | Both halves > 0 | **Credibility** |
|---|---|---|---|---|---|---|
| main: A_long | 127 | +0.0042 | 0.324 | 1.000 | False | **0.00** |
| main: B_recent | 127 | -0.0060 | 0.743 | 1.000 | False | **0.00** |
| main: C_gap | 127 | +0.0045 | 0.311 | 1.000 | True | **0.00** |
| main: D_trend | 127 | -0.0040 | 0.669 | 1.000 | False | **0.00** |
| main: E_pairs | 0 | — | — | — | None | **0.00** |
| SB: S_long | 127 | +0.0066 | 0.408 | 1.000 | False | **0.00** |
| SB: S_recent | 127 | -0.0372 | 0.905 | 1.000 | False | **0.00** |
| SB: S_gap | 127 | +0.0311 | 0.136 | 0.546 | False | **0.00** |
| SB: S_trend | 127 | -0.0236 | 0.798 | 1.000 | False | **0.00** |
| SB: S_transition | 0 | — | — | — | None | **0.00** |
| ticket: E_ticket | 0 | — | — | — | None | **0.00** |
| ticket: F_ticket | 127 | -0.0529 | 0.807 | 0.807 | False | **0.00** |

**Every credibility is 0.** No main family, Super Ball model or ticket-level component has corrected, stable evidence (E_pairs and S_transition were flat at every origin). So the reliability-weighted scores M and Q are flat, main ordering falls back to the declared **non-evidential** convention (the equal-weight mean of informative model z-scores), and the ticket score T is 0 for every combination. Selection is then driven by coverage, the overlap rule and the declared tie-breaks.

- Main discovery pool: **Top 12**, basis NO EDGE: predeclared default K=12 (no pool size passed on development). All **792** five-number combinations are enumerated.
- Super Ball rule: **C** (challengers get the top-2 SBs by Q, then the EQ_SB convention, distinct from the V1 SB). Basis: predeclared: C unless an SB model passes the V1 SB gate at the design cutoff (V1 SB gate passing models: []).
- Overlap: at most 1 shared main with every selected ticket (relax to 2/3 only if infeasible). Objective J = T + 1.0·coverage.

## Main-model reliability (127 V1 origins, targets 1627–1753)
| Family | Mean AP (random 0.2222) | z | Top-8 (1.14) | Top-12 (1.71) | Top-15 (2.14) | Confirmation AP excess | Halves |
|---|---|---|---|---|---|---|---|
| A_long | 0.2264 | +0.46 | 1.18 | 1.65 | 2.13 | -0.0115 | +0.0126 / -0.0040 |
| B_recent | 0.2162 | -0.65 | 1.00 | 1.54 | 2.06 | +0.0104 | -0.0164 / +0.0043 |
| C_gap | 0.2267 | +0.49 | 1.24 | 1.72 | 2.23 | +0.0191 | +0.0005 / +0.0085 |
| D_trend | 0.2182 | -0.44 | 1.08 | 1.64 | 2.10 | +0.0124 | -0.0057 / -0.0024 |
| E_pairs | flat at every origin | | | | | | |

Score correlations: A~B 0.63, B~D 0.49, B~C -0.54, C~D -0.46. SB calibration (reported only): the long-run Dirichlet frequency log loss 2.3377 vs uniform 2.3026, i.e. no better than uniform.

## Main pool size (development targets 1652–1713 only)

| K | Mean winners | Random 5K/35 | Excess | z | Holm p | Halves | P(≥2 / ≥3 / ≥4 / 5) actual | Random | Confirmation excess |
|---|---|---|---|---|---|---|---|---|---|
| 8 | 1.065 | 1.143 | -0.078 | -0.70 | 1.00 | -0.143 / -0.014 | 0.323 / 0.065 / 0.000 / 0.000 | 0.319 / 0.067 / 0.006 / 0.000 | +0.207 |
| 10 | 1.290 | 1.429 | -0.138 | -1.15 | 1.00 | -0.138 / -0.138 | 0.468 / 0.081 / 0.016 / 0.000 | 0.447 / 0.128 / 0.017 / 0.001 | +0.071 |
| 12 | 1.565 | 1.714 | -0.150 | -1.18 | 1.00 | -0.230 / -0.069 | 0.532 / 0.161 / 0.048 / 0.000 | 0.569 / 0.209 / 0.038 / 0.002 | +0.036 |
| 15 | 2.177 | 2.143 | +0.035 | +0.26 | 1.00 | +0.051 / +0.018 | 0.710 / 0.339 / 0.113 / 0.048 | 0.728 / 0.360 / 0.093 / 0.009 | +0.057 |

The exact hypergeometric baseline removes the mechanical advantage of larger pools. No K passed, so the predeclared **Top 12** is used and labelled **NO EDGE**.

## Super Ball portfolio rule (historical, P0 mains fixed)

| Rule | Period | Any SB in portfolio | SB hits (3 tickets) | Challenger SB hits | Distinct SBs |
|---|---|---|---|---|---|
| A same top SB | development | 0.161 | 0.355 | 0.194 | 1.21 |
| B top distinct (EQ) | development | 0.387 | 0.387 | 0.226 | 3.00 |
| C reliability-weighted distinct | development | 0.371 | 0.371 | 0.210 | 3.00 |
| D random | development | 0.339 | 0.355 | 0.194 | 2.66 |
| A same top SB | confirmation | 0.125 | 0.250 | 0.200 | 1.48 |
| B top distinct (EQ) | confirmation | 0.275 | 0.275 | 0.225 | 3.00 |
| C reliability-weighted distinct | confirmation | 0.225 | 0.225 | 0.175 | 3.00 |
| D random | confirmation | 0.100 | 0.100 | 0.050 | 2.77 |

Under a fair draw every rule has the same expected SB hits (0.1 per ticket); distinct SBs mechanically maximise the chance that at least one ticket hits (0.3 for three distinct SBs vs at most 0.2 when the challengers share one). The historical differences are within noise. The predeclared rule C stands; it was not chosen from #1753/#1754.

## Historical portfolio test (K=12)

**Development** (62 targets)

| Metric | P0 | A 3 random | B 3 random, overlap ≤1 | C V1 + 2 random | D top-3 standalone | E P0 mains, random SBs | P0 − C (95% CI) |
|---|---|---|---|---|---|---|---|
| best-ticket main matches | 1.306 | 1.320 | 1.334 | 1.271 | 0.710 | — | +0.035 [-0.09, +0.16] |
| total main matches | 2.032 | 2.142 | 2.143 | 1.997 | 1.742 | — | +0.035 [-0.16, +0.23] |
| challenger main matches | 1.484 | 1.431 | 1.422 | 1.449 | 1.161 | — | +0.035 [-0.16, +0.23] |
| P(any ≥2 mains) | 0.339 | 0.364 | 0.366 | 0.331 | 0.145 | — | +0.007 [-0.09, +0.11] |
| P(any ≥3) | 0.048 | 0.041 | 0.041 | 0.029 | 0.000 | — | +0.020 [-0.03, +0.07] |
| P(any ≥4) | 0.000 | 0.001 | 0.001 | 0.002 | 0.000 | — | -0.002 [-0.00, -0.00] |
| P(5/5) | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | — | +0.000 [+0.00, +0.00] |
| P(any SB hit) | 0.371 | 0.271 | 0.273 | 0.320 | 0.323 | 0.318 | +0.051 [-0.04, +0.15] |
| challenger SB hits | 0.210 | 0.200 | 0.200 | 0.200 | 0.226 | 0.195 | +0.010 [-0.09, +0.11] |
| P(any ≥2 mains + SB) | 0.032 | 0.042 | 0.042 | 0.044 | 0.016 | 0.043 | -0.012 [-0.03, +0.02] |
| unique mains | 13.516 | 12.963 | 13.551 | 13.544 | 6.419 | — | -0.028 [-0.32, +0.31] |
| mean main overlap | 0.495 | 0.711 | 0.494 | 0.495 | 4.000 | — | -0.001 [-0.11, +0.09] |

**Confirmation** (40 targets)

| Metric | P0 | A 3 random | B 3 random, overlap ≤1 | C V1 + 2 random | D top-3 standalone | E P0 mains, random SBs | P0 − C (95% CI) |
|---|---|---|---|---|---|---|---|
| best-ticket main matches | 1.350 | 1.311 | 1.335 | 1.335 | 1.075 | — | +0.015 [-0.13, +0.16] |
| total main matches | 2.225 | 2.139 | 2.138 | 2.129 | 2.425 | — | +0.096 [-0.07, +0.27] |
| challenger main matches | 1.525 | 1.425 | 1.433 | 1.429 | 1.700 | — | +0.096 [-0.07, +0.27] |
| P(any ≥2 mains) | 0.400 | 0.355 | 0.365 | 0.383 | 0.325 | — | +0.017 [-0.10, +0.14] |
| P(any ≥3) | 0.000 | 0.038 | 0.042 | 0.028 | 0.000 | — | -0.028 [-0.03, -0.02] |
| P(any ≥4) | 0.000 | 0.001 | 0.001 | 0.001 | 0.000 | — | -0.001 [-0.00, -0.00] |
| P(5/5) | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | — | +0.000 [+0.00, +0.00] |
| P(any SB hit) | 0.225 | 0.272 | 0.268 | 0.231 | 0.225 | 0.229 | -0.006 [-0.10, +0.09] |
| challenger SB hits | 0.175 | 0.196 | 0.199 | 0.201 | 0.125 | 0.198 | -0.026 [-0.12, +0.07] |
| P(any ≥2 mains + SB) | 0.100 | 0.040 | 0.039 | 0.028 | 0.075 | 0.032 | +0.072 [-0.00, +0.15] |
| unique mains | 13.375 | 12.963 | 13.553 | 13.544 | 6.450 | — | -0.169 [-0.53, +0.22] |
| mean main overlap | 0.542 | 0.713 | 0.493 | 0.495 | 4.000 | — | +0.047 [-0.08, +0.17] |

## Evidence gate (confirmation, 40 targets): **FAIL**
- E1 challenger main matches: 61 vs 57.1 expected, p 0.306, Holm p 0.917, mean excess +0.096, block 95% [-0.05, +0.27], halves +0.071 / +0.121.
- E2 challenger SB hits: 7, p 0.712, Holm p 0.982.
- E3 best-ticket main matches: 54, p 0.491, Holm p 0.982.

**The Super Lotto P0 portfolio is a coverage experiment, not a demonstrated predictive edge.**

## Implementation notes
- Ticket 1 history is the validated V1 reconstruction (it reproduces the frozen #1753/#1754 pools exactly). V1's fallback selects SL10 at every cutoff.
- At targets 1657, 1669, 1670, 1671, 1672, 1673, 1674 V1 itself could not have run: its H-fill step raises "Diversity fallback needs new seed counter". The pre-commitment did not anticipate this. For those 7 development targets the SL10 slot (D_trend's top ticket + S_gap SB, fixed before the H fill) is used and flagged. No V1 gate would have passed at any cutoff.
- At K=12 the ≤1 overlap rule held in 194 of 204 ticket selections and relaxed to ≤2 in 10 (V1 ticket 4–5 numbers deep in the pool). The evidence exception never fired (all credibilities 0).
