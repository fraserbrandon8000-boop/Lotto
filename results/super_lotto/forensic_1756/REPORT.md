# Super Lotto #1756 forensic

Actual #1756: **05 · 07 · 15 · 29 · 32 + SB3**.

| Frozen ticket | Result |
|---|---|
| V1 Science 01 · 06 · 11 · 18 · 22 + SB2 | 0/5, SB miss |
| P0 Coverage 1 02 · 09 · 12 · 23 · 24 + SB7 | 0/5, SB miss |
| P0 Coverage 2 01 · 12 · 17 · 18 · 29 + SB3 | 1/5 (29), **SB3 hit** |

## 1. Frozen record

All checks pass: **True**. Pre-Jev pool freeze hashes all exact; `prediction_1756.json` embedded hashes {'exact': 43}; P0 freeze hashes all exact; all 24 other entries of `draw1756/HASHES.sha256` exact; the ledger at the #1756 freeze is an exact prefix of today's ledger (append-only). Jev receipt: state, request (compact), response all match; one HTTP attempt, retries disabled. Offline validation: inclusive 0.03 Score boundary on SL08/SL09 stability (no response edit, no retry). The 5 replicate Jev calls used byte-identical request bytes and all ran after the ticket freeze. Ticket files are unchanged since the freeze commit.

Chronology (UTC): pool frozen 2026-10-02T17:21:49 (commit `1bcb011 2026-10-02T17:21:49+00:00`) → Jev 2026-10-02T17:21:57 → V1 frozen 2026-10-02T17:22:35 → P0 frozen 2026-10-02T17:22:36 (commit `3fc61ca 2026-10-02T17:22:36+00:00`) → post-freeze audit, replicates, random control (commit `a811beb 2026-10-02T17:23:36+00:00`) → draw 2026-10-03T01:30. **All three tickets were frozen about 8 hours before the draw.** Random control (seed 2026093061): 03 · 04 · 13 · 22 · 26 + SB4 / 02 · 03 · 20 · 23 · 31 + SB2 / 09 · 10 · 14 · 29 · 30 + SB3.

## 2. Whole V1 candidate pool (scored after the draw; nothing promoted)

| ID | Mains | SB | Generator | Matches | Matched | SB3 | Prod. Jev Choice | Prod. rank | Replicate mean rank | Sens. range | Agreement | Ensemble |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SL01 | 03 · 06 · 12 · 17 · 24 | 5 | A_long | 0 | — | no | 0.01 | 5–7 | 4.6 | 1–6 | 2 | 0.08 |
| SL02 | 12 · 17 · 22 · 23 · 24 | 3 | A_long | 0 | — | yes | 0 | 8–20 | 13.7 | 2–4 | 2 | 0.08 |
| SL03 | 09 · 11 · 12 · 17 · 24 | 2 | A_long | 0 | — | no | 0.01 | 5–7 | 10.5 | 1–3 | 3 | 0.20 |
| SL04 | 09 · 11 · 18 · 24 · 25 | 1 | B_recent | 0 | — | no | 0.01 | 5–7 | 5.7 | 1–6 | 2 | 0.29 |
| SL05 | 01 · 09 · 11 · 18 · 29 | 1 | B_recent | 1 | 29 | no | 0.03 | 3 | 3.4 | 1–4 | 3 | 0.33 |
| SL06 | 01 · 05 · 11 · 12 · 18 | 2 | B_recent | 1 | 05 | no | 0 | 8–20 | 13.7 | 1–3 | 2 | 0.08 |
| SL07 | 07 · 16 · 19 · 27 · 34 | 3 | C_gap | 1 | 07 | yes | 0 | 8–20 | 13.7 | 1–1 | 1 | -0.37 |
| SL08 | 06 · 07 · 10 · 13 · 16 | 5 | C_gap | 1 | 07 | no | 0 | 8–20 | 13.7 | 2–2 | 1 | -0.70 |
| SL09 | 07 · 10 · 13 · 20 · 34 | 3 | C_gap | 1 | 07 | yes | 0 | 8–20 | 13.7 | 3–3 | 1 | -0.40 |
| SL10 | 01 · 06 · 11 · 18 · 22 | 2 | D_trend | 0 | — | no | 0.5 | 1 | 2.0 | 2–5 | 3 | 0.40 |
| SL11 | 01 · 02 · 11 · 15 · 22 | 1 | D_trend | 1 | 15 | no | 0 | 8–20 | 13.7 | 1–8 | 3 | 0.21 |
| SL12 | 01 · 12 · 15 · 18 · 35 | 1 | D_trend | 1 | 15 | no | 0 | 8–20 | 13.7 | 1–4 | 2 | 0.07 |
| SL13 | 18 · 22 · 23 · 24 · 30 | 2 | E_pairs | 0 | — | no | 0 | 8–20 | 13.7 | 13–13 | 1 | -0.19 |
| SL14 | 05 · 10 · 20 · 22 · 32 | 3 | E_pairs | 2 | 05 32 | yes | 0 | 8–20 | 13.7 | 14–14 | 0 | -0.26 |
| SL15 | 03 · 08 · 12 · 20 · 32 | 5 | E_pairs | 1 | 32 | no | 0 | 8–20 | 13.7 | 15–15 | 0 | -0.36 |
| SL16 | 06 · 07 · 18 · 22 · 29 | 3 | F_structure | 2 | 07 29 | yes | 0.02 | 4 | 4.7 | 1–2 | 1 | 0.36 |
| SL17 | 06 · 07 · 18 · 25 · 28 | 2 | F_structure | 1 | 07 | no | 0 | 8–20 | 13.7 | 1–2 | 0 | 0.07 |
| SL18 | 05 · 13 · 18 · 28 · 29 | 1 | F_structure | 2 | 05 29 | no | 0 | 8–20 | 13.7 | 3–3 | 0 | -0.16 |
| SL19 | 01 · 12 · 18 · 23 · 25 | 1 | G_ensemble | 0 | — | no | 0.42 | 2 | 1.0 | 1–7 | 2 | 0.43 |
| SL20 | 04 · 06 · 13 · 17 · 18 | 2 | H_random | 0 | — | no | 0 | 8–20 | 13.7 | 13–17 | 0 | -0.15 |

Main matches 0:8 · 1:9 · 2:3 · 3:0 · 4:0 · 5:0. Best: SL14, SL16, SL18 (2/5). V1 selected SL10: 0/5. Production Jev favourite SL10 (0/5); five-replicate favourite SL19 (5/5) (0/5). Candidates carrying SB3: SL02, SL07, SL09, SL14, SL16; **SL14 (05 32 + SB3) and SL16 (07 29 + SB3) paired two mains with SB3**; both had production Choice ≤ 0.02. Reached ≥2: yes (3 candidates; random expectation 2.78); ≥3: none. Jev Choice vs matches Spearman -0.02. E_pairs ranks are flat (no Holm-retained pair), so E_pairs candidates are effectively unranked.

## 3. Pre-draw evidence for the #1756 winners (cutoff #1755)

Every P0 credibility was 0, so the P0 order is the declared equal-weight average of the informative A–D z-scores (E_pairs flat; F has no number score). Model reliability contribution = credibility × score = 0 for every family.

| Winner | A_long | B_recent | C_gap | D_trend | E_pairs (flat) | G_ensemble | H (control) | EQ z | **P0 rank** | Count (exp 25.6) | Last 30 | EW rate | Gap (pct) | Trend | Max pair lift (Holm-retained) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 05 | 15 [13–16] | 15 | 24 [23–27] | 28 [26–31] | 16 [1–35] | 24 | 5 | -0.264 | **24** | 27 | 4 | 0.172 | 2 (0.50) | -0.075 | 1.99 (0) |
| 07 | 21 [20–22] | 34 | 1 | 27 [26–31] | 12 [1–35] | 14 | 6 | +0.053 | **14** | 25 | 2 | 0.095 | 19 (1.00) | -0.075 | 1.99 (0) |
| 15 | 17 [17–19] | 8 | 31 [31–35] | 7 [7–12] | 2 [1–35] | 13 | 8 | +0.064 | **13** | 26 | 5 | 0.179 | 0 (0.08) | +0.050 | 2.33 (0) |
| 29 | 13 [13–16] | 17 | 20 [20–22] | 8 [7–12] | 4 [1–35] | 12 | 11 | +0.130 | **12** | 27 | 4 | 0.164 | 3 (0.42) | +0.050 | 3.32 (0) |
| 32 | 24 [24–26] | 22 | 9 [9–10] | 14 [13–15] | 18 [1–35] | 17 | 27 | +0.014 | **17** | 23 | 4 | 0.123 | 9 (0.73) | +0.025 | 1.66 (0) |

| Missed winner | A. P0 rank | B. Best model | C. Worst model | D. Disagreement (spread ≥15) | E. Zero/weak credibility weighting suppressed useful support? | F. Top 15 | G. Top 18 | H. Top 20 | I. Top 25 |
|---|---|---|---|---|---|---|---|---|---|
| 05 | 24 | A_long 15 | D_trend 28 | no (13) | no — no informative model had it in its Top 12 | no | no | no | yes |
| 07 | 14 | C_gap 1 | B_recent 34 | yes (33) | no — a single unvalidated model had it in its Top 12 and equal-weight averaging pushed it out | yes | yes | yes | yes |
| 15 | 13 | D_trend 7 | C_gap 31 | yes (24) | no — a single unvalidated model had it in its Top 12 and equal-weight averaging pushed it out | yes | yes | yes | yes |
| 32 | 17 | C_gap 9 | A_long 24 | yes (15) | no — a single unvalidated model had it in its Top 12 and equal-weight averaging pushed it out | no | yes | yes | yes |

- **05** (P0 24): no informative model had it in a Top 12 (best A_long/B_recent 15). Nothing to suppress.
- **07** (P0 14): **C_gap's #1** (19-draw absence, most overdue), but B_recent ranked it 34th and D_trend 27th. Equal-weight averaging put it at 14. Same pattern as 33 in #1755: C_gap is anti-correlated with B/D, so its top pick is averaged away. Over 105 causal origins C_gap alone has no corrected skill (full-period AP excess p = 0.331), so this is not a suppressed validated signal.
- **15** (P0 13): D_trend 7, B_recent 8, but C_gap 31 (it had just been drawn). Missed the pool by one place.
- **32** (P0 17): C_gap 9 was its only Top-12 support.
- **E (zero weighting):** the zero credibilities did not hide a validated model. The unshrunk, lightly shrunk and Bayesian reliability weightings each capture *fewer* or equal #1756 winners in their Top 12 (1, 1, 1) than the frozen order (1). The only single orderings with 2 in their Top 12 were D_trend, C_gap (E_gap), K_best_trailing, LOFO-minus-B and the **random control** (2).

Top-N winners captured for #1756 by each pre-draw ordering:

| Ordering | Top 8 | Top 10 | Top 12 | Top 15 | Top 18 | Top 20 | Top 25 |
|---|---|---|---|---|---|---|---|
| A_random | 1 | 2 | 2 | 3 | 4 | 4 | 4 |
| B_long | 0 | 0 | 0 | 2 | 3 | 3 | 5 |
| C_recent | 1 | 1 | 1 | 2 | 3 | 3 | 4 |
| D_trend | 2 | 2 | 2 | 3 | 3 | 3 | 3 |
| E_gap | 1 | 2 | 2 | 2 | 2 | 3 | 4 |
| F_P0_frozen_protocol | 0 | 0 | 1 | 3 | 4 | 4 | 5 |
| G_equal_weight | 0 | 0 | 1 | 3 | 4 | 4 | 5 |
| H_unshrunk_reliability | 1 | 1 | 1 | 2 | 2 | 3 | 4 |
| I_light_shrinkage | 0 | 0 | 1 | 3 | 4 | 4 | 5 |
| L_bayes_empirical | 0 | 0 | 1 | 3 | 4 | 4 | 5 |
| J_lofo_minus_A | 0 | 0 | 1 | 3 | 4 | 4 | 4 |
| J_lofo_minus_B | 0 | 1 | 2 | 3 | 3 | 3 | 4 |
| J_lofo_minus_C | 0 | 0 | 1 | 2 | 3 | 4 | 4 |
| J_lofo_minus_D | 0 | 1 | 1 | 1 | 2 | 2 | 5 |
| K_best_trailing_model | 1 | 2 | 2 | 2 | 2 | 3 | 4 |
| M_family_vote_borda | 0 | 0 | 1 | 2 | 3 | 3 | 5 |
| random expectation 5N/35 | 1.14 | 1.43 | 1.71 | 2.14 | 2.57 | 2.86 | 3.57 |

## 4. Two consecutive discovery misses: exact random baseline

Top-12 pool from 35, 5 winners: X ~ Hypergeometric(35, 5, 12).

| One draw | Value |
|---|---|
| expected winners captured | 1.7143 |
| P(0) | 0.1037 |
| P(1) | 0.3273 |
| P(≤1) | 0.4310 |
| P(≥2) | 0.5690 |
| P(≥3) | 0.2090 |
| P(all 5) | 0.00244 |

| Two independent draws | Value |
|---|---|
| expected total captured (of 10) | 3.4286 |
| observed | 2 |
| P(total ≤ 2) | **0.2604** |
| P(total ≤ 1) | 0.0786 |
| P(≤1 in both draws) | 0.1857 |
| percentile of 2/10 (P(<2) + ½P(=2)) | 0.169 (≈ 17th percentile) |

Historical P0 Top-12 capture (105 causal origins): mean 1.629, ≤1 in 44% of draws; two consecutive draws totalling ≤2 in 32% of consecutive pairs.

**Verdict: mildly unusual at most (about 1 in 4 random Top-12 pools do this badly or worse over two draws). Not statistically concerning, and fully compatible with chance.** Two observations carry almost no information.

## 5. Strict causal walk-forward: P0 order by pool size (targets 1652–1756, n = 105; confirmation 1717–1756)

Excess is measured against the exact random capture 5N/35, which removes the mechanical advantage of larger pools. ≥k coverage is shown observed / random. Holm across the whole family of 144 variants.

| Pool | Mean captured | Random | Excess | ≥1 | ≥2 | ≥3 | ≥4 | 5/5 | Development | Confirmation | Halves (std excess, full) | Block 95% (std, full) | raw p (full) | raw p (conf) | Holm p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Top 8 | 1.162 | 1.143 | +0.019 | 0.75 / 0.75 | 0.35 / 0.32 | 0.05 / 0.07 | 0.01 / 0.01 | 0.00 / 0.00 | 1.108 | 1.250 | -0.05 / +0.09 | [-0.16, +0.18] | 0.431 | 0.247 | 1.00 |
| Top 10 | 1.352 | 1.429 | -0.076 | 0.79 / 0.84 | 0.48 / 0.45 | 0.07 / 0.13 | 0.02 / 0.02 | 0.00 / 0.00 | 1.338 | 1.375 | -0.13 / -0.03 | [-0.24, +0.08] | 0.809 | 0.668 | 1.00 |
| Top 12 | 1.629 | 1.714 | -0.086 | 0.87 / 0.90 | 0.56 / 0.57 | 0.16 / 0.21 | 0.04 / 0.04 | 0.00 / 0.00 | 1.615 | 1.650 | -0.14 / -0.04 | [-0.23, +0.07] | 0.824 | 0.685 | 1.00 |
| Top 15 | 2.181 | 2.143 | +0.038 | 0.98 / 0.95 | 0.72 / 0.73 | 0.35 / 0.36 | 0.10 / 0.09 | 0.03 / 0.01 | 2.231 | 2.100 | +0.05 / +0.03 | [-0.13, +0.21] | 0.371 | 0.631 | 1.00 |
| Top 18 | 2.590 | 2.571 | +0.019 | 1.00 / 0.98 | 0.85 / 0.85 | 0.50 / 0.53 | 0.21 / 0.19 | 0.03 / 0.03 | 2.646 | 2.500 | +0.06 / -0.02 | [-0.15, +0.19] | 0.445 | 0.694 | 1.00 |
| Top 20 | 2.895 | 2.857 | +0.038 | 1.00 / 0.99 | 0.94 / 0.91 | 0.64 / 0.64 | 0.26 / 0.27 | 0.06 / 0.05 | 2.985 | 2.750 | +0.14 / -0.06 | [-0.12, +0.19] | 0.372 | 0.767 | 1.00 |
| Top 25 | 3.505 | 3.571 | -0.067 | 1.00 / 1.00 | 0.98 / 0.98 | 0.89 / 0.87 | 0.50 / 0.55 | 0.14 / 0.16 | 3.569 | 3.400 | +0.01 / -0.14 | [-0.25, +0.11] | 0.780 | 0.889 | 1.00 |

At every size the P0 order captures winners at the rate its size implies. Larger pools capture more winners only mechanically. **Top 12 is not shown to be too narrow, and no other size is better.** The production pool is not widened.

## 6. Does P0 rank winners better than a random ordering?

Every method is computed causally at each origin. AP = average precision of the full 35-number ordering against the 5 winners (exact random mean 0.2222).

| Method | Top 8 | Top 10 | Top 12 | Top 15 | Top 18 | Top 20 | Top 25 | AP excess (full) | AP p (full) | Top-12 p (full) | Top-12 conf mean |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A. random ranking (explicit null) | -0.057 | +0.095 | +0.219 | +0.143 | +0.124 | +0.095 | +0.133 | -0.0027 | 0.604 | 0.014 | 1.850 |
| B. long-run frequency | +0.038 | -0.010 | -0.057 | -0.010 | +0.038 | +0.019 | +0.067 | +0.0029 | 0.388 | 0.737 | 1.575 |
| C. recent frequency | -0.133 | -0.162 | -0.152 | -0.038 | -0.067 | -0.048 | -0.038 | -0.0020 | 0.580 | 0.948 | 1.500 |
| D. trend | -0.010 | -0.124 | -0.086 | -0.010 | -0.076 | -0.048 | +0.010 | -0.0025 | 0.599 | 0.824 | 1.825 |
| E. gap | +0.038 | +0.048 | -0.038 | +0.019 | -0.038 | +0.000 | -0.019 | +0.0044 | 0.331 | 0.669 | 1.700 |
| F. frozen P0 ordering | +0.019 | -0.076 | -0.086 | +0.038 | +0.019 | +0.038 | -0.067 | +0.0045 | 0.329 | 0.824 | 1.650 |
| G. equal weight | +0.019 | -0.076 | -0.086 | +0.038 | +0.019 | +0.038 | -0.067 | +0.0045 | 0.329 | 0.824 | 1.650 |
| H. unshrunk reliability | +0.000 | -0.086 | -0.076 | -0.048 | -0.038 | -0.038 | -0.019 | -0.0012 | 0.547 | 0.797 | 1.625 |
| I. lightly shrunk (unadjusted p) | -0.076 | -0.143 | -0.076 | -0.067 | -0.048 | +0.029 | -0.029 | -0.0088 | 0.808 | 0.797 | 1.650 |
| regularized (empirical Bayes) | +0.000 | -0.067 | -0.057 | +0.000 | -0.048 | -0.019 | -0.095 | +0.0021 | 0.417 | 0.737 | 1.650 |
| J. leave out A_long | -0.105 | -0.029 | -0.067 | -0.048 | +0.000 | +0.067 | +0.010 | -0.0050 | 0.690 | 0.768 | 1.700 |
| J. leave out B_recent | +0.038 | +0.010 | -0.010 | +0.029 | -0.010 | -0.029 | -0.133 | +0.0088 | 0.190 | 0.557 | 1.625 |
| J. leave out C_gap | -0.048 | -0.076 | -0.114 | -0.114 | +0.038 | +0.010 | -0.076 | +0.0039 | 0.351 | 0.890 | 1.550 |
| J. leave out D_trend | -0.019 | -0.057 | -0.086 | -0.029 | -0.029 | -0.067 | +0.057 | +0.0006 | 0.478 | 0.824 | 1.625 |
| K. best trailing-30 model | +0.029 | -0.048 | -0.038 | -0.029 | -0.019 | +0.038 | +0.019 | +0.0052 | 0.304 | 0.669 | 1.725 |
| family vote (Borda) | -0.010 | -0.019 | -0.067 | -0.038 | -0.010 | -0.067 | -0.076 | -0.0018 | 0.572 | 0.768 | 1.575 |

(Cells are mean excess winners captured over random, full period.) No P0 credibility was ever non-zero at any origin, so F and G are identical by construction.

The frozen P0 ordering's AP excess is +0.0045 (p = 0.33); its Top-12 capture is 1.629 against 1.714 random (p = 0.82). No method beats random after correction. Note the **explicit random control itself reached raw p = 0.014 at Top 12** over the full period. That is what noise looks like in a family this size, and it is why only the corrected gate counts.

**THE CURRENT P0 MAIN-NUMBER DISCOVERY ORDER HAS NO DEMONSTRATED PREDICTIVE VALUE.**

## 7. Number 15 (won #1755 and #1756)

| Model | #1755 run rank | #1756 run rank |
|---|---|---|
| A_long | 22 | 17 |
| B_recent | 18 | 8 |
| C_gap | 18 | 31 |
| D_trend | 22 | 7 |
| E_pairs | 32 | 2 |
| F_structure | — | — |
| G_ensemble | 32 | 13 |
| H_random | 3 | 8 |
| **P0 rank** | **20** | **13** |
| V1 candidates containing 15 | 0 | 2 (SL11, SL12) |

Feature movement #1755 run → #1756 run: count 25 → 26; ew_rate 0.15 → 0.179; last30 4 → 5; last20 3 → 4; last10 3 → 4; current_gap 4 → 0; gap_percentile 0.542 → 0.08; trend 0 → 0.05.

Before #1755, 15 was mid-table everywhere (ranks 18–22). After winning #1755, B_recent and D_trend moved it to 8 and 7, while C_gap dropped it to 31 (just drawn). The average put it at 13, one place outside the pool. Historically its P0 rank averaged 19.4 (Top 12 in 32% of origins, expected 34%); it has won 27 of 180 draws (expected 25.7). A specific number repeats with probability 5/35 = 0.143. At least one number repeats between consecutive draws with probability 0.561 (historically 0.508). **15 was not systematically under-ranked; its repeat is ordinary random recurrence. No repeat rule is created.** In the frozen #1757 run, unchanged V1/P0 rank 15 at P0 position 12, inside the pool, purely from its updated recent-frequency/trend features, not from any rule.

## 8. Discovery vs construction

**#1756:** winners available to the constructor: **1** (29); absent before construction: **4** (05, 07, 15, 32); available but not placed: **0**; placed on playable tickets: **29**.

**Historical conditional analysis** (frozen constructor replayed causally at every origin, K = 12, rule C; reproduces the frozen historical P0 portfolios exactly, mismatches []):

| Winners in pool (K) | Draws | Share (random) | Mean best-ticket matches | Mean total portfolio matches | Mean unique winners covered | Challenger in-pool captures | Blind expectation |
|---|---|---|---|---|---|---|---|
| 0 | 14 | 0.13 (0.10) | 0.57 | 0.57 | 0.57 | 0.00 | 0.00 |
| 1 | 32 | 0.30 (0.33) | 1.09 | 1.38 | 1.16 | 0.91 | 0.76 |
| 2 | 42 | 0.40 (0.36) | 1.40 | 2.48 | 2.17 | 1.67 | 1.55 |
| 3 | 13 | 0.12 (0.17) | 2.00 | 3.54 | 3.08 | 2.38 | 2.35 |
| 4 | 4 | 0.04 (0.04) | 2.50 | 4.25 | 4.00 | 3.25 | 2.92 |

The challengers captured 143 of 171 in-pool winners (84%), against 131.6 (77%) expected from the share of the pool they cover. Best-ticket matches track K closely (correlation 0.70). **The binding layer is DISCOVERY**: construction converts whatever reaches the pool, and discovery is at random level. Because discovery has no skill, a better constructor cannot create an edge either.

## 9. Super Ball (actual SB3; played 2, 7, 3)

| SB | S_long | S_recent | S_gap | S_trend | S_transition (flat) | S_ensemble | P0 rank |
|---|---|---|---|---|---|---|---|
| 1 | 6 | 5 | 10 | 1 | 1 | 10 | 6 |
| 2 | 9 | 10 | 1 | 10 | 7 | 1 | 9 |
| 3 **(actual)** | 5 | 1 | 8 | 2 | 4 | 8 | 2 |
| 4 | 2 | 6 | 4 | 6 | 3 | 4 | 4 |
| 5 | 1 | 2 | 7 | 8 | 2 | 7 | 3 |
| 6 | 3 | 8 | 5 | 7 | 9 | 5 | 5 |
| 7 | 4 | 4 | 3 | 3 | 6 | 3 | 1 |
| 8 | 8 | 3 | 9 | 5 | 8 | 9 | 7 |
| 9 | 7 | 7 | 6 | 9 | 10 | 6 | 8 |
| 10 | 10 | 9 | 2 | 4 | 5 | 2 | 10 |

SB3: S_long 5, **S_recent 1**, S_gap 8, **S_trend 2**, S_transition 4 (flat; tie 1–10), S_ensemble 8, **P0 SB rank 2**. All SB credibilities were 0, so the P0 SB order is the equal-weight average of the SB model z-scores (SB7 0.463, SB3 0.426). Rule C gave the two challengers the top two P0 SBs other than V1's SB2, which were SB7 and SB3.

**Driver: both.** SB3 reached rank 2 through unvalidated equal-weight model evidence (S_recent and S_trend), and rule C's diversification placed it. Historically the P0 SB Top-3 contains the winner 28.6% of the time vs 30% random (p = 0.66), so in practice **the hit was essentially chance.**

Combined live P0 SB record: #1755 miss, #1756 hit. With 3 distinct SBs from 10 the hit rate is 0.30 per draw; P(≥1 hit in 2) = 0.51, P(exactly 1) = 0.42. 1/2 is the single most likely outcome. **No SB predictive skill is claimed.**

## 10. V1 fixed slot (SL10)

Under the no-edge rule V1 selects `default_rng(2026092109).integers(20)` = 9 every time, i.e. **SL10 (D_trend's top ticket with S_gap's SB) in 100% of no-edge runs** (98 reconstructable origins; V1 never passed its gate).

| Selection rule | Mean main matches | SB hit rate | Consecutive main overlap | Identical consecutive tickets | SB repeats next draw | SB entropy (bits, max 3.32) |
|---|---|---|---|---|---|---|
| SL10 fixed slot | 0.602 | 0.112 | 3.18 | 29 | 88% | 2.64 |
| per-draw seed | 0.786 | 0.184 | 1.29 | 5 | 21% | 3.09 |
| rotating slot (target mod 20) | 0.765 | 0.122 | 1.81 | 5 | 14% | 2.95 |
| uniform candidate (expectation) | 0.733 | — | — | — | — | — |
| random ticket | 0.714 | 0.100 | 0.71 | ≈0 | 10% | 3.32 |

SL10's mean (0.602) is below random and below the other slots, but the shortfall is within noise (one-sided p for excess 0.97; the lower-tail deviation is about 1.5 SD). Per-draw seeding's apparent gain (confirmation raw p 0.030) fails Holm (p = 1.00) and its bootstrap lower bound is below 0.
**PREDICTIVE PERFORMANCE: no demonstrated harm or benefit. DIVERSITY / EXPERIMENT QUALITY: clearly harmed.** SL10 repeats 3.2 of 5 mains from one draw to the next (random 0.71), was identical in 29 consecutive pairs, and repeats its SB 88% of the time. Live V1 has played SB2 in all four draws #1753–#1756. The prospective V1 record is therefore close to one repeated ticket, not independent samples. A non-fixed slot should be predeclared for a future V1 revision as an experiment-quality fix, not as a predictive claim. Production V1 is unchanged here.

## 11. Jev top-1 stability (#1756)

| Call | Top | Top Choice | SL10 Choice | SL19 Choice | Confidence | Entropy (bits) |
|---|---|---|---|---|---|---|
| production | SL10 | 0.50 | 0.50 | 0.42 | 0.46 | 1.49 |
| replicate_1 | SL19 | 0.58 | 0.32 | 0.58 | 0.55 | 1.49 |
| replicate_2 | SL19 | 0.56 | 0.38 | 0.56 | 0.52 | 1.31 |
| replicate_3 | SL19 | 0.64 | 0.28 | 0.64 | 0.61 | 1.39 |
| replicate_4 | SL19 | 0.54 | 0.38 | 0.54 | 0.50 | 1.45 |
| replicate_5 | SL19 | 0.50 | 0.41 | 0.50 | 0.47 | 1.53 |

SL10 and SL19 midrank variance 0.17 each (1↔2 swap); production gap SL10 − SL19 = +0.08 (**near-tie**); mean pairwise top-3 overlap 2.67/3; overall Spearman 0.955 (min 0.924) as recorded in `jev_stability_1756`. The flip reflects a near-tie, not a change of overall view.

Aggregators on saved outcome sets (no new historical calls): #1755 first-valid / mean-Choice / median-rank / majority all SL04 (0/5); #1756 first-valid SL10 (0/5), mean / median / majority SL19 (0/5). n = 2 draws, so this cannot evaluate skill. In #1757 (post-freeze) production and all 5 replicates chose SL19 (0.80; mean Spearman 0.979). **Jev's first-response top-1 is stable when one candidate dominates and unstable in near-ties. Under the no-edge rule it never affects the ticket.**

## 12. Combined prospective record

| Draw | V1 | P0 challengers | Random control |
|---|---|---|---|
| #1753 | 1/5, SB miss | — | — |
| #1754 | 0/5, SB miss | shadow only | — |
| #1755 | 0/5, SB miss | 1/5 + 0/5, SB miss | 1 + 1 + 0, SB miss |
| #1756 | 0/5, SB miss | 0/5 + 1/5 (SB3 hit) | 0 + 0 + 1 (SB3 hit) |

V1: 1 main matches in 4 tickets (expected 2.86; P(≤1) = 0.18); SB 0/4. P0 3-ticket portfolio (#1755–#1756): 2 mains in 6 tickets (expected 4.29; P(≤2) = 0.16); 1 SB hit. The fixed-seed random control: 3 mains and 1 SB hit over the same two draws. **Everything is consistent with chance.**

## 13. Research family (see `p1_research/REPORT.md`)

144 variants in one Holm family: 16 orderings × 7 pool sizes plus AP, dynamic pool size, 10 SB rules/orderings, and V1 selection variants (SL10, per-draw seed, rotating slot, broader candidate union, pool SB coverage). Smallest Holm p = 1.00. **Passing: none. NO SUPER LOTTO V2/P1 REFINEMENT IS JUSTIFIED.** No P1 shadow ticket is produced.

