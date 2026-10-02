# Super Lotto #1755 forensic

Actual #1755: **03 · 11 · 15 · 21 · 33 + SB1**.

| Frozen ticket | Result |
|---|---|
| V1 Science 01 · 02 · 18 · 34 · 35 + SB2 | 0/5, SB miss |
| P0 Coverage 1 06 · 11 · 12 · 22 · 23 + SB3 | 1/5 (11), SB miss |
| P0 Coverage 2 07 · 17 · 18 · 24 · 25 + SB7 | 0/5, SB miss |

This was **two separate misses: main-number discovery and Super Ball coverage.**

## 1. Frozen record

All checks pass: **True**. Pre-Jev pool freeze hashes {'candidates.json': 'exact', 'jev_state.json': 'exact', 'complete_rankings.json': 'exact', 'predraw_rankings_and_fit.json': 'exact', 'metadata.json': 'exact', 'PROTOCOL.md': 'exact'}; `prediction_1755.json` embedded hashes {'exact': 41}; P0 freeze hashes all exact; Jev receipt state/request/response match, with a single HTTP attempt; ledger hashes exact; the frozen ticket files are unchanged since the freeze commit.

Chronology (UTC): pool frozen 2026-09-30T00:50:53 (commit `7edb0dc 2026-09-30T00:50:53+00:00`) → Jev 2026-09-30T00:51:03 → V1 frozen 2026-09-30T00:51:16 → P0 frozen 2026-09-30T00:51:17 (commit `ef94b7b 2026-09-30T00:51:17+00:00`) → post-freeze research (commit `aeec3a4 2026-09-30T00:52:07+00:00`) → draw 01:30:00. **All three tickets were frozen 39 minutes before the draw.**

## 2. Whole V1 candidate pool

| ID | Mains | SB | Generator | Matches | Matched | SB1? | Jev Choice | Jev rank | Sens. range |
|---|---|---|---|---|---|---|---|---|---|
| SL01 | 03 · 06 · 12 · 17 · 24 | 5 | A_long | 1 | 03 | no | 0.05 | 3 | 1–5 |
| SL02 | 12 · 17 · 22 · 23 · 24 | 3 | A_long | 0 | — | no | 0.01 | 7–13 | 2–4 |
| SL03 | 09 · 11 · 12 · 17 · 24 | 2 | A_long | 1 | 11 | no | 0.01 | 7–13 | 1–3 |
| SL04 | 01 · 12 · 18 · 23 · 25 | 8 | B_recent | 0 | — | no | 0.44 | 1 | 1–2 |
| SL05 | 01 · 05 · 11 · 12 · 18 | 2 | B_recent | 1 | 11 | no | 0 | 14–20 | 1–3 |
| SL06 | 09 · 11 · 18 · 24 · 25 | 2 | B_recent | 1 | 11 | no | 0.01 | 7–13 | 2–5 |
| SL07 | 02 · 07 · 16 · 33 · 34 | 9 | C_gap | 1 | 33 | no | 0.04 | 4–5 | 1–1 |
| SL08 | 07 · 13 · 26 · 33 · 34 | 5 | C_gap | 1 | 33 | no | 0.01 | 7–13 | 2–2 |
| SL09 | 13 · 19 · 27 · 33 · 34 | 3 | C_gap | 1 | 33 | no | 0.01 | 7–13 | 3–3 |
| SL10 | 01 · 02 · 18 · 34 · 35 | 2 | D_trend | 0 | — | no | 0.01 | 7–13 | 1–7 |
| SL11 | 01 · 11 · 18 · 22 · 25 | 8 | D_trend | 1 | 11 | no | 0.33 | 2 | 1–5 |
| SL12 | 01 · 06 · 18 · 29 · 32 | 2 | D_trend | 0 | — | no | 0 | 14–20 | 4–9 |
| SL13 | 18 · 22 · 23 · 24 · 30 | 2 | E_pairs | 0 | — | no | 0.04 | 4–5 | 13–13 |
| SL14 | 05 · 10 · 20 · 22 · 32 | 9 | E_pairs | 0 | — | no | 0 | 14–20 | 14–14 |
| SL15 | 03 · 08 · 12 · 20 · 32 | 5 | E_pairs | 1 | 03 | no | 0 | 14–20 | 15–15 |
| SL16 | 06 · 07 · 18 · 22 · 29 | 3 | F_structure | 0 | — | no | 0.01 | 7–13 | 1–2 |
| SL17 | 06 · 07 · 18 · 25 · 28 | 2 | F_structure | 0 | — | no | 0 | 14–20 | 1–2 |
| SL18 | 06 · 12 · 18 · 19 · 29 | 8 | F_structure | 0 | — | no | 0 | 14–20 | 3–3 |
| SL19 | 10 · 11 · 16 · 21 · 22 | 2 | G_ensemble | 2 | 11 21 | no | 0 | 14–20 | 6–19 |
| SL20 | 04 · 06 · 13 · 17 · 18 | 2 | H_random | 0 | — | no | 0.03 | 6 | 13–20 |

Main matches 0:10 · 1:9 · 2:1 · 3+:0. Best: SL19 (2/5). V1 SL10: 0/5. Jev preferred SL04: 0/5. **No candidate carried SB1** (pool SBs [2, 3, 5, 8, 9]). Reached ≥2: True; ≥3/≥4/5: none. Jev Choice vs matches: Spearman -0.02. Nothing is promoted retrospectively.

## 3. Discovery failure: winners vs the frozen Top-12 pool

Frozen P0 pool: 01 · 02 · 06 · 07 · 11 · 12 · 17 · 18 · 22 · 23 · 24 · 25. Every P0 credibility weight was 0, so the P0 order is the declared equal-weight convention (EQ = mean of A–D z-scores); E_pairs and the G proxy were flat; F has no number-level score.

| Winner | A_long | B_recent | C_gap | D_trend | H (control) | P0 rank | Long-run count | Last 30 | EW rate | Gap | Trend | Top-12 support | A narrowly out? | B deep? | F: Top 15/18/20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 03 | 15 [12–16] | 24 | 34 [31–35] | 29 [27–31] | 8 | **29** | 27 | 3 | 0.138 | 0 | -0.075 | none | no | yes | n/n/n |
| 11 | 5 [4–5] | 8 | 24 [22–25] | 5 [3–7] | 30 | **5** | 31 | 5 | 0.179 | 2 | +0.100 | A_long, B_recent, D_trend | no | no | Y/Y/Y |
| 15 | 22 [19–22] | 18 | 18 [16–18] | 22 [15–22] | 3 | **20** | 25 | 4 | 0.150 | 4 | +0.000 | none | no | no | n/n/Y |
| 21 | 30 [29–30] | 22 | 35 [31–35] | 20 [15–22] | 19 | **32** | 21 | 4 | 0.118 | 0 | +0.000 | none | no | yes | n/n/n |
| 33 | 26 [26–28] | 34 | 1 | 35 | 22 | **25** | 22 | 2 | 0.082 | 22 | -0.175 | C_gap | no | yes | n/n/n |

- **03, 21:** no Top-12 support from any informative model (best ranks: 03 was 15th under A_long and 24–34 elsewhere; 21 was 20th under D_trend and 22–35 elsewhere). P0 ranks 29 and 32, outside even a Top 25.
- **15:** mid-table everywhere (ranks 18–22); P0 rank 20, so only a Top 20 pool would have held it.
- **33:** **C_gap's #1** (most overdue number), but A_long, B_recent and D_trend ranked it 26–35, and C_gap is anti-correlated with B and D. The equal-weight average put it at 25. A diagnostic ordering with unshrunk raw positive evidence weights would have put 33 at #2 and pushed 11 to #11. But that weighting has no corrected evidence (raw p ≈ 0.31), so this is a single-draw observation, not a suppressed signal.
- **11:** in the Top 12 of A_long, B_recent and D_trend; P0 rank 5; captured by P0 Coverage 1.
- **D (suppressed by shrinkage?):** only 33 would have entered the Top 12 under the unshrunk diagnostic ordering. **E (zero weights?):** yes, the order was the equal-weight convention; for 33 the averaging is what excluded it. No informative model supported 03, 15 or 21 at all.

## 4. Top-N winner coverage

| Ranking | Top 5 | Top 8 | Top 10 | Top 12 | Top 15 | Top 18 | Top 20 | Top 25 |
|---|---|---|---|---|---|---|---|---|
| A_long | 1 | 1 | 1 | 1 [1–2] | 2 [1–2] | 2 | 2 [2–3] | 3 |
| B_recent | 0 | 1 | 1 | 1 | 1 | 2 | 2 | 4 |
| C_gap | 1 | 1 | 1 | 1 | 1 | 2 | 2 | 3 |
| D_trend | 1 [0–1] | 1 | 1 | 1 | 1 [1–2] | 1 [1–3] | 2 [1–3] | 3 |
| H_random | 1 | 2 | 2 | 2 | 2 | 2 | 3 | 4 |
| P0_order | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 3 |
| random expectation 5N/35 | 0.71 | 1.14 | 1.43 | 1.71 | 2.14 | 2.57 | 2.86 | 3.57 |
| historical P0 mean (1652–1753) | 0.64 | 1.18 | 1.37 | 1.64 | 2.19 | 2.60 | 2.90 | 3.51 |

The P0 ordering captured 1 winner at Top 12 against 1.71 random and 1.64 historical. Capturing ≤1 happens in 43% of random Top-12 pools. A Top 20 would have held 2 (random 2.86) and a Top 25 would have held 3 (random 3.57). **This does not show a larger pool is better**: the historical P0 capture is at random level at every depth (see §8).

## 5. Construction diagnosis

- Winners in pool: 11. The challengers covered 10 of the 12 pool numbers and **captured the only in-pool winner (11)**.
- Historically (102 targets) the challengers captured 139 of 167 in-pool winners (83%), against 77% expected from the share of the pool they cover. Construction transmits whatever discovery provides.
- **Capability test** (no ticket built from the outcome): if the 5 winners had been any 5 of the 12 frozen pool numbers, the frozen challengers would have scored ≥2 with certainty, ≥3 with probability 0.62 and ≥4 with probability 0.09 (mean challenger total 4.17).
- **Classification: D, ordinary random variation, with a discovery shortfall.** It was not a construction failure.

## 6. Super Ball forensic (actual SB1; played 2, 3, 7)

| SB model | Model pick | SB1 rank | SB2 rank | SB3 rank | SB7 rank |
|---|---|---|---|---|---|
| S_long | 5 | 8 [7–8] | 9 | 5 | 4 |
| S_recent | 3 | 8 | 9 | 1 | 4 |
| S_gap | 2 | 3 | 1 | 9 | 4 |
| S_trend | 8 | 3 [3–4] | 10 | 2 | 4 [3–4] |
| S_transition (flat) | 2 | 6 [1–10] | 1 [1–10] | 4 [1–10] | 9 [1–10] |
| S_ensemble | 2 | 3 | 1 | 9 | 4 |
| S_random | 9 (control) | — | — | — | — |

- **SB1 in the V1 pool: no** (pool SBs [2, 3, 5, 8, 9]). It was **structurally excluded by V1**: V1 gives each candidate the single top pick of one of 7 SB models, and SB1 was no model's top pick. Its best ranks were 3rd under S_gap, S_trend (tied 3–4) and S_ensemble.
- **P0 SB order:** 3 7 5 4 8 6 1 2 9 10; **SB1 was 7th.** Rule C gave the challengers the top 2 SBs distinct from V1's SB2 (3 and 7). SB1 was not excluded by diversification itself; it lay outside the 3 SBs a 3-ticket portfolio can play.
- **Is the omission ordinary?** Yes. Three distinct SBs miss with probability 0.70; V1's single SB misses with probability 0.90 (0 hits in #1753–#1755 has probability 0.73).
- **Is Top-3 too narrow? Would Top-4/Top-5 help?** A 3-ticket portfolio can only play 3 SBs, so wider coverage means more tickets (cost grows in proportion to coverage). The real question is whether the SB ordering has skill. Historically it does not: in the confirmation period the P0 SB Top-3 contained the winner 22.5% of the time (random 30%), the Top-4 30% (random 40%) and the Top-5 32.5% (random 50%); all Holm p = 1.0. **Wider SB coverage only buys mechanical coverage at proportional cost; there is no basis to promote it.**
- #1753 (SB3), #1754 (SB8), #1755 (SB1): V1 played SB2 each time (S_gap's overdue pick) and no V1 pool contained the winning SB. With n = 3 no rule is inferred.

## 7. Combined prospective record

| Draw | V1 | P0 portfolio |
|---|---|---|
| #1753 | 1/5, SB miss | — |
| #1754 | 0/5, SB miss | shadow only: best 1/5, total 2, no SB |
| #1755 | 0/5, SB miss | best 1/5, total 1 (of 3 tickets), no SB |

V1: mean 0.33 main matches vs 0.714 random (P(total ≤ 1 in 3 tickets) = 0.33); SB 0/3 (95% CI 0–0.71; P(0/3) = 0.73); ≥2 mains 0/3 (P = 0.64). P0 has one prospective draw (expected portfolio total 2.14; observed 1). **The record is consistent with chance and tells us nothing yet about any edge.**

## 8. Research challengers (strict walk-forward through #1755; 104 targets, confirmation 1716–1755; Holm across 14 refinements)

| Refinement | Confirmation | Random | p | Holm p | Block LB (std) | Full-period |
|---|---|---|---|---|---|---|
| P0_order_top12 | 1.675 | 1.714 | 0.627 | 1.00 | -0.27 | 1.635 (p 0.81) |
| P0_order_top15 | 2.100 | 2.143 | 0.631 | 1.00 | -0.33 | 2.173 (p 0.40) |
| P0_order_top18 | 2.475 | 2.571 | 0.744 | 1.00 | -0.40 | 2.577 (p 0.50) |
| P0_order_top20 | 2.725 | 2.857 | 0.811 | 1.00 | -0.39 | 2.885 (p 0.41) |
| dynamic_pool_size | 1.675 | 1.671 | 0.521 | 1.00 | -0.18 | 2.067 (p 0.61) |
| less_shrinkage_top12 | 1.650 | 1.714 | 0.685 | 1.00 | -0.32 | 1.644 (p 0.78) |
| best_trailing_model_top12 | 1.725 | 1.714 | 0.502 | 1.00 | -0.24 | 1.673 (p 0.68) |
| SB_top1_coverage | 0.100 | 0.100 | 0.577 | 1.00 | -0.25 | 0.096 (p 0.60) |
| SB_top2_coverage | 0.125 | 0.200 | 0.924 | 1.00 | -0.38 | 0.183 (p 0.71) |
| SB_top3_coverage | 0.225 | 0.300 | 0.889 | 1.00 | -0.38 | 0.279 (p 0.71) |
| SB_top4_coverage | 0.300 | 0.400 | 0.929 | 1.00 | -0.41 | 0.365 (p 0.79) |
| SB_top5_coverage | 0.325 | 0.500 | 0.992 | 1.00 | -0.55 | 0.442 (p 0.90) |
| per_draw_seed_v1 | 0.925 | 0.714 | 0.047 | 0.66 | -0.12 | 0.784 (p 0.19) |
| broader_candidate_union | 4.425 | 4.379 | 0.385 | 1.00 | -0.34 | 4.278 (p 0.88) |

**NO SUPER LOTTO V2/P1 REFINEMENT IS JUSTIFIED.** Wider pools capture winners at exactly the rate their size implies; dynamic pool size, lighter shrinkage and best-trailing-model weighting show no excess; SB ordering coverage is at or below chance at every depth; per-draw V1 seeding (raw p 0.047) does not survive correction. The frozen #1756 rules are unchanged.

## Conclusion
- **Why were 03, 15, 21, 33 excluded?** 03 and 21 had no Top-12 support from any informative model (best ranks 15 and 20; P0 ranks 29 and 32); 15 was mid-table (P0 rank 20); 33 was C_gap's top number but was averaged down to 25 by the anti-correlated B/D models under the equal-weight convention.
- **Discovery or construction?** Ordinary variation with a discovery shortfall. Construction captured the only in-pool winner and would have performed well had the winners been in the pool.
- **SB1:** 3rd under S_gap/S_trend/S_ensemble, no model's top pick (so structurally absent from V1), 7th in the P0 SB order. A 3-SB miss is the expected outcome 70% of the time.
- **Refinements:** none passes. **NO SUPER LOTTO V2/P1 REFINEMENT IS JUSTIFIED.**
