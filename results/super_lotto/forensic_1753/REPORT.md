# SUPER LOTTO #1753 FORENSIC RESULTS

**No Super Lotto V2 is justified.** The one-main-match/no-Super-Ball result is compatible with ordinary random variation. There are concrete ranking and candidate-coverage limitations, but no tested change establishes an out-of-sample advantage. V1 and all frozen prediction/Jev artifacts remain unchanged. No next ticket has been generated.

## Outcome and integrity

Draw #1753, September 22, 2026: **01, 05, 08, 14, 18 + SB 3**, as supplied by the user. Frozen primary SL10: **01, 22, 32, 34, 35 + SB 2**. Score: **one main match (01), no Super Ball match**. The outcome is appended once to the separate Super Lotto prospective ledger; the original prediction record and prior ledger bytes are preserved. This analysis does not claim an independent new official-results fetch.

The frozen prediction remains SHA-256 `902d875951c679d1e8b4738b80542ec4a7eca7e5e30e524b3e8d00d4c4395203`. Every hash embedded in the original freeze agrees with the current file. The separately saved preservation manifest covers the remaining existing V1 artifacts. Data fitting stops at #1752; #1753 appears only in retrospective scoring, never model training.

## A. Exact saved main-number rankings

| Number | Role | A_long | B_recent | C_gap | D_trend | G_ensemble | H_random |
|---|---|---|---|---|---|---|---|
| 01 | matched winner | 13 | 5 | 18 | 2 | 32 | 4 |
| 05 | missed winner | 14 | 17 | 27 | 32 | 8 | 30 |
| 08 | missed winner | 25 | 33 | 11 | 31 | 6 | 1 |
| 14 | missed winner | 34 | 28 | 12 | 26 | 20 | 15 |
| 18 | missed winner | 18 | 1 | 35 | 7 | 34 | 34 |
| 22 | selected miss | 6 | 13 | 17 | 1 | 13 | 16 |
| 32 | selected miss | 23 | 18 | 13 | 3 | 1 | 10 |
| 34 | selected miss | 27 | 22 | 4 | 9 | 26 | 11 |
| 35 | selected miss | 33 | 21 | 34 | 6 | 33 | 28 |

These main-number positions are the actual stored full orders, converted from zero-based number IDs to 1–35. Ties use the original saved order. The full score tie intervals are retained in main_evidence.json. E_pairs has no informative individual ordering: all pair-network scores are zero. F_structure is a whole-combination objective and has no individual-number ordering. There is no separate final marginal ranking: final selection was the seeded no-edge choice among complete candidates.

**G caveat:** the saved main ensemble weights were [0, 0, 0, 0, 1, 0] for A–F. All weight fell on E_pairs, which was flat. Every main ensemble score was therefore zero, and the stored G order is a seeded tie-break only. Its top-N positions must not be interpreted as learned preference. H is also a random reference, not evidence. This degeneracy was present before the outcome; it is not repaired in V1.

## B. #1753 top-N coverage, with exact winners

| Model | Top 5 | Top 7 | Top 8 | Top 10 | Top 12 | Top 15 | Top 20 |
|---|---|---|---|---|---|---|---|
| A_long | 0 (—) | 0 (—) | 0 (—) | 0 (—) | 0 (—) | 2 (01, 05) | 3 (01, 05, 18) |
| B_recent | 2 (01, 18) | 2 (01, 18) | 2 (01, 18) | 2 (01, 18) | 2 (01, 18) | 2 (01, 18) | 3 (01, 05, 18) |
| C_gap | 0 (—) | 0 (—) | 0 (—) | 0 (—) | 2 (08, 14) | 2 (08, 14) | 3 (01, 08, 14) |
| D_trend | 1 (01) | 2 (01, 18) | 2 (01, 18) | 2 (01, 18) | 2 (01, 18) | 2 (01, 18) | 2 (01, 18) |
| G_ensemble | 0 (—) | 1 (08) | 2 (05, 08) | 2 (05, 08) | 2 (05, 08) | 2 (05, 08) | 3 (05, 08, 14) |
| H_random | 2 (01, 08) | 2 (01, 08) | 2 (01, 08) | 2 (01, 08) | 2 (01, 08) | 3 (01, 08, 14) | 3 (01, 08, 14) |

Each cell is count (winning numbers). E_pairs and F_structure are not applicable as individual rankings. Compare like-sized pools: expected capture under randomness is top 5: 0.714, top 7: 1.000, top 8: 1.143, top 10: 1.429, top 12: 1.714, top 15: 2.143, top 20: 2.857. A broader pool capturing more winners is not in itself evidence of useful ranking.

B_recent identified 18 and 01 at ranks 1 and 5, but ranked the other winners 17, 33 and 28. D_trend identified 01 and 18 at ranks 2 and 7, but ranked 05, 08 and 14 at 32, 31 and 26. Neither had all winners concentrated near the top. The three winners in G’s top 20 are not an ensemble success because its scores were flat.

## C. Hit-versus-miss evidence and construction

| Number | Role | Count | Last30 | EW rate | Gap | Raw trend | Long z | Recent z | Gap z | Trend z |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | matched winner | 27 | 6 | 0.190 | 4 | 0.125 | 0.409 | 1.097 | -0.265 | 1.494 |
| 05 | missed winner | 26 | 4 | 0.156 | 1 | -0.125 | 0.189 | 0.036 | -0.869 | -1.494 |
| 08 | missed winner | 23 | 2 | 0.098 | 7 | -0.100 | -0.472 | -1.275 | 0.339 | -1.195 |
| 14 | missed winner | 17 | 3 | 0.093 | 7 | -0.050 | -1.792 | -0.976 | 0.339 | -0.598 |
| 18 | missed winner | 26 | 9 | 0.252 | 0 | 0.100 | 0.189 | 2.809 | -1.070 | 1.195 |
| 22 | selected miss | 30 | 5 | 0.163 | 4 | 0.175 | 1.069 | 0.463 | -0.265 | 2.092 |
| 32 | selected miss | 23 | 4 | 0.137 | 6 | 0.100 | -0.472 | -0.162 | 0.138 | 1.195 |
| 34 | selected miss | 22 | 4 | 0.108 | 12 | 0.075 | -0.692 | -0.472 | 1.346 | 0.896 |
| 35 | selected miss | 19 | 4 | 0.124 | 0 | 0.100 | -1.352 | -0.305 | -1.070 | 1.195 |

SL10 was generated by D_trend. Its selected losers 22, 32, 34 and 35 had positive raw trends (+0.175, +0.100, +0.075, +0.100) and trend ranks 1, 3, 9 and 6. Missed winners 05, 08 and 14 had negative trends (−0.125, −0.100, −0.050) and ranks 32, 31 and 26. Thus the saved trend objective explains which candidates were favored; it does not prove that trend should be reversed. Missed winner 18 had positive trend and rank 7, and appeared in many other candidates. The finite search and diversity requirements can omit a high-ranked number from any one candidate. SL10 itself was selected by the no-edge seeded rule, not promoted by validated trend performance.

All nine examined numbers had zero retained pair-network and ensemble scores. Pair evidence therefore did not distinguish winners from selected losers. Long/recent/EW evidence was mixed: 18 was strongly favored recently (nine occurrences in the last 30 and EW rate 0.2517), whereas 14 was weak across frequency/trend. No saved feature cleanly separates every hit from every miss.

| Number | Candidate appearances | Candidate IDs |
|---|---|---|
| 01 | 3 | SL06, SL10, SL11 |
| 05 | 1 | SL14 |
| 08 | 1 | SL15 |
| 14 | 0 | None |
| 18 | 9 | SL04, SL05, SL06, SL11, SL13, SL16, SL17, SL18, SL20 |
| 22 | 8 | SL03, SL10, SL11, SL12, SL13, SL14, SL16, SL19 |
| 32 | 4 | SL10, SL12, SL14, SL15 |
| 34 | 2 | SL07, SL10 |
| 35 | 2 | SL10, SL12 |

The shortlist contained 31 distinct main numbers but **omitted 14 entirely**. It covered the other four winners individually, but no candidate held more than two of them. This is a realized candidate-coverage limitation, not proof that an alternative construction is predictively superior. Exact saved feature records additionally include rolling 10/20/50/100 counts, complete gap distributions, percentiles, volatility, and short/long ratios in main_evidence.json.

Only complete-ticket sensitivity was saved; there is no number-level stability series to retrieve. SL10 ranked 1–8 under its generator perturbations and was top-five in 10/11 variants, yet its generator failed corrected historical validation. Stability of an unvalidated heuristic is not predictive robustness. The full frozen candidate profiles and sensitivity are preserved; no number-specific stability was invented.

## D. Super Ball forensic

| Model | SB 3 rank | SB 3 tie interval | SB 3 score | SB 2 rank | SB 2 tie interval | SB 2 score | Saved model choice |
|---|---|---|---|---|---|---|---|
| S_long | 6 | 5–6 | -0.148 | 8 | 8–9 | -0.641 | 5 |
| S_recent | 2 | 2 | 0.928 | 9 | 9 | -1.250 | 5 |
| S_gap | 9 | 9 | -0.822 | 1 | 1 | 2.681 | 2 |
| S_trend | 4 | 4–6 | 0.316 | 10 | 10 | -2.530 | 5 |
| S_transition | 4 | 1–10 | 0.000 | 7 | 1–10 | 0.000 | 6 |
| S_ensemble | 9 | 9 | -0.290 | 1 | 1 | 0.946 | 2 |

The full SB order was not originally stored. The table derives it only from the **saved pre-draw scores and original deterministic tie-break**, and its top choice is checked against each saved SB prediction. No #1753 fitting occurs. Score tie intervals avoid attributing meaningful differences to arbitrary tie-breaks. S_transition is entirely zero; its apparent positions 1–10 carry no evidence. The scores are standardized heuristic scores, not calibrated probabilities. No per-ball winning-probability distribution was saved.

SB 3 was **second under S_recent**, but S_recent supplied only its top value (5) to candidate construction. SB 2 was first under S_gap and the ensemble. The saved SB ensemble gave 35.294% weight to gap and 64.706% to the flat transition component; its active ordering therefore reduced to gap, putting SB 3 ninth. SB 2 had a current gap of 27 versus 1 for SB 3. Their EW rates were 0.0683 versus 0.1397, and last-30 counts were 1 versus 4. This exposes conflicting heuristics and loss of second-ranked SB coverage, not evidence that recent weighting would reliably win.

Candidates used only SB values **2, 4, 5 and 6**. No candidate used SB 3, so Jev could not select the correct Super Ball. There was no separate final SB rank: SB values were paired with complete candidates from the seven existing generator outputs. Merely spreading SB values across more candidates increases portfolio coverage; it does not establish an advantage for one final ticket.

## E–F. Frozen candidates and Jev

Outcome rank means descending main matches, then SB match, preserving tie intervals. It is not a prize-money ordering. Every candidate missed SB, so this convention does not affect ordering here.

| ID | Frozen mains | SB | Main hits | Matched mains | SB hit | Outcome rank | Jev Choice |
|---|---|---|---|---|---|---|---|
| SL01 | 09, 11, 12, 17, 24 | 5 | 0 | — | 0 | 13–20 | 35.00% |
| SL02 | 03, 06, 12, 17, 24 | 5 | 0 | — | 0 | 13–20 | 1.00% |
| SL03 | 12, 17, 22, 23, 24 | 2 | 0 | — | 0 | 13–20 | 0.00% |
| SL04 | 09, 11, 18, 24, 25 | 5 | 1 | 18 | 0 | 3–12 | 7.00% |
| SL05 | 06, 09, 18, 24, 29 | 6 | 1 | 18 | 0 | 3–12 | 0.00% |
| SL06 | 01, 12, 18, 23, 25 | 2 | 2 | 01, 18 | 0 | 1–2 | 27.00% |
| SL07 | 04, 07, 13, 33, 34 | 4 | 0 | — | 0 | 13–20 | 12.00% |
| SL08 | 04, 06, 07, 17, 33 | 5 | 0 | — | 0 | 13–20 | 1.00% |
| SL09 | 04, 10, 16, 17, 33 | 5 | 0 | — | 0 | 13–20 | 1.00% |
| SL10 | 01, 22, 32, 34, 35 | 2 | 1 | 01 | 0 | 3–12 | 2.00% |
| SL11 | 01, 06, 11, 18, 22 | 5 | 2 | 01, 18 | 0 | 1–2 | 7.00% |
| SL12 | 02, 19, 22, 32, 35 | 6 | 0 | — | 0 | 13–20 | 0.00% |
| SL13 | 18, 22, 23, 24, 30 | 2 | 1 | 18 | 0 | 3–12 | 0.00% |
| SL14 | 05, 10, 20, 22, 32 | 4 | 1 | 05 | 0 | 3–12 | 0.00% |
| SL15 | 03, 08, 12, 20, 32 | 5 | 1 | 08 | 0 | 3–12 | 0.00% |
| SL16 | 06, 07, 18, 22, 29 | 5 | 1 | 18 | 0 | 3–12 | 0.00% |
| SL17 | 06, 07, 18, 25, 28 | 2 | 1 | 18 | 0 | 3–12 | 0.00% |
| SL18 | 06, 12, 18, 19, 29 | 5 | 1 | 18 | 0 | 3–12 | 2.00% |
| SL19 | 10, 11, 16, 21, 22 | 6 | 0 | — | 0 | 13–20 | 0.00% |
| SL20 | 04, 06, 13, 17, 18 | 2 | 1 | 18 | 0 | 3–12 | 4.00% |

**Best:** SL06 and SL11 tied, each matching 01 and 18 (2/5 mains), with no SB. **SL10:** 1/5, SB miss, tied positions 3–12. **Jev preferred SL01:** 0/5, SB miss, tied positions 13–20. Candidate match distribution: eight with zero, ten with one, two with two; none with three, four or five. No correct-SB candidate existed.

The saved `jev-1.13.0` Choice favored SL01 at 35.00%, confidence 0.310; SL10 had 2.00%. No new Jev request was made and no original response was changed. Across the 20 candidates, tie-aware Spearman association of Choice probability with main hits was **0.121**. Whole-draw random simulation (20,000 draws, retaining candidate overlaps) gave descriptive two-sided p **0.637**. Weighted-by-Choice main hits were 0.83 versus an unweighted candidate average of 0.70. This weak one-draw association does not demonstrate predictive skill; SL01’s miss does not establish that Jev is systematically worse either.

TypeSafe Choice probabilities describe the response across supplied alternatives; confidence describes distribution concentration. The supplied question asked about empirical evidence, so these probabilities are not lottery-winning probabilities. [Current Choice documentation](https://docs.typesafe.ai/primitives/choice) and [confidence documentation](https://docs.typesafe.ai/confidence) were consulted for this interpretation.

## G. Diagnosis

The strongest overall classification is **ordinary random variation, with observed main-ranking, shortlist-coverage and SB-selection limitations** (E with descriptive elements of A/B/C). A fixed uniform ticket has probability 42.21% of exactly one main match, 37.99% of exactly one main plus no SB, and 86.11% of at most one main. One main match is above the random expected mean 0.7143; a jackpot miss is not an unusual failure event.

The data do not support a pure combination-construction diagnosis: several missed mains were already low-ranked, 14 was absent from the shortlist, and the ensemble ranking was flat. There was a partial recent-model signal for 01/18 and SB 3, but no historical corrected evidence that this partial observation is repeatable. A single realized result cannot distinguish a weak forecasting method from ordinary luck; the pre-draw pipeline had already declared no detected edge.

## H. Historical number-discovery recheck

The saved 126 walk-forward targets end at #1752, after 50 warmup draws. We independently recomputed coverage from stored rankings and target outcomes and reconciled every stored count. The 40-draw confirmation segment has been inspected before; it is reused retrospective evidence, not a fresh holdout. The underlying data exclude #1753.

| Pool | Random mean | Random 3+ | Random 4+ | Random all5 |
|---|---|---|---|---|
| 5 | 0.714 | 1.39% | 0.05% | 0.00% |
| 7 | 1.000 | 4.38% | 0.31% | 0.01% |
| 8 | 1.143 | 6.65% | 0.60% | 0.02% |
| 10 | 1.429 | 12.78% | 1.69% | 0.08% |
| 12 | 1.714 | 20.90% | 3.75% | 0.24% |
| 15 | 2.143 | 35.96% | 9.33% | 0.93% |
| 20 | 2.857 | 64.04% | 27.16% | 4.78% |

Confirmation coverage rates (40 draws):

| Model | Pool | Mean | Random mean | 3+ | 4+ | All5 | Mean Holm p | Best event Holm p |
|---|---|---|---|---|---|---|---|---|
| A_long | 5 | 0.725 | 0.714 | 2.50% | 0.00% | 0.00% | 1.000 | 1.000 |
| A_long | 7 | 1.000 | 1.000 | 2.50% | 2.50% | 0.00% | 1.000 | 1.000 |
| A_long | 8 | 1.125 | 1.143 | 5.00% | 2.50% | 0.00% | 1.000 | 1.000 |
| A_long | 10 | 1.525 | 1.429 | 12.50% | 5.00% | 0.00% | 1.000 | 1.000 |
| A_long | 12 | 1.725 | 1.714 | 15.00% | 7.50% | 0.00% | 1.000 | 1.000 |
| A_long | 15 | 2.125 | 2.143 | 27.50% | 12.50% | 0.00% | 1.000 | 1.000 |
| A_long | 20 | 2.875 | 2.857 | 65.00% | 22.50% | 5.00% | 1.000 | 1.000 |
| B_recent | 5 | 0.775 | 0.714 | 0.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| B_recent | 7 | 1.000 | 1.000 | 5.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| B_recent | 8 | 1.050 | 1.143 | 5.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| B_recent | 10 | 1.250 | 1.429 | 5.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| B_recent | 12 | 1.625 | 1.714 | 20.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| B_recent | 15 | 2.125 | 2.143 | 30.00% | 12.50% | 0.00% | 1.000 | 1.000 |
| B_recent | 20 | 2.775 | 2.857 | 60.00% | 27.50% | 5.00% | 1.000 | 1.000 |
| C_gap | 5 | 0.750 | 0.714 | 0.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| C_gap | 7 | 1.050 | 1.000 | 5.00% | 2.50% | 0.00% | 1.000 | 1.000 |
| C_gap | 8 | 1.225 | 1.143 | 7.50% | 2.50% | 2.50% | 1.000 | 0.866 |
| C_gap | 10 | 1.550 | 1.429 | 17.50% | 5.00% | 2.50% | 1.000 | 1.000 |
| C_gap | 12 | 1.725 | 1.714 | 20.00% | 5.00% | 2.50% | 1.000 | 1.000 |
| C_gap | 15 | 2.350 | 2.143 | 50.00% | 15.00% | 5.00% | 1.000 | 1.000 |
| C_gap | 20 | 2.975 | 2.857 | 72.50% | 32.50% | 7.50% | 1.000 | 1.000 |
| D_trend | 5 | 0.725 | 0.714 | 0.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| D_trend | 7 | 1.000 | 1.000 | 2.50% | 0.00% | 0.00% | 1.000 | 1.000 |
| D_trend | 8 | 1.200 | 1.143 | 10.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| D_trend | 10 | 1.425 | 1.429 | 12.50% | 0.00% | 0.00% | 1.000 | 1.000 |
| D_trend | 12 | 1.825 | 1.714 | 25.00% | 5.00% | 0.00% | 1.000 | 1.000 |
| D_trend | 15 | 2.225 | 2.143 | 37.50% | 10.00% | 2.50% | 1.000 | 1.000 |
| D_trend | 20 | 2.950 | 2.857 | 70.00% | 25.00% | 7.50% | 1.000 | 1.000 |
| G_ensemble | 5 | 0.775 | 0.714 | 2.50% | 0.00% | 0.00% | 1.000 | 1.000 |
| G_ensemble | 7 | 1.175 | 1.000 | 7.50% | 0.00% | 0.00% | 1.000 | 1.000 |
| G_ensemble | 8 | 1.325 | 1.143 | 12.50% | 0.00% | 0.00% | 1.000 | 1.000 |
| G_ensemble | 10 | 1.575 | 1.429 | 17.50% | 2.50% | 0.00% | 1.000 | 1.000 |
| G_ensemble | 12 | 1.850 | 1.714 | 25.00% | 5.00% | 2.50% | 1.000 | 1.000 |
| G_ensemble | 15 | 2.225 | 2.143 | 40.00% | 15.00% | 2.50% | 1.000 | 1.000 |
| G_ensemble | 20 | 3.000 | 2.857 | 65.00% | 37.50% | 12.50% | 1.000 | 1.000 |
| H_random | 5 | 0.825 | 0.714 | 0.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| H_random | 7 | 1.125 | 1.000 | 0.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| H_random | 8 | 1.250 | 1.143 | 5.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| H_random | 10 | 1.625 | 1.429 | 17.50% | 2.50% | 0.00% | 1.000 | 1.000 |
| H_random | 12 | 1.875 | 1.714 | 25.00% | 5.00% | 0.00% | 1.000 | 1.000 |
| H_random | 15 | 2.350 | 2.143 | 42.50% | 10.00% | 2.50% | 1.000 | 1.000 |
| H_random | 20 | 3.150 | 2.857 | 70.00% | 40.00% | 10.00% | 1.000 | 1.000 |

No model demonstrates corrected repeatable discovery. Across all 126 targets, the minimum event-family Holm p was 0.561; in confirmation it was 0.866. All corrected mean-coverage p-values were 1.000. historical_coverage.json contains exact counts/rates, medians, random baselines, mean tests and coverage-event tests for all/development/confirmation periods. Event tails use exact binomial null probabilities from the same-size hypergeometric pool reference; Holm spans model × pool × threshold. E/F remain not applicable as number rankings.

## Historical construction, sensitivity and bounded new hypotheses

The pre-draw tests already cover broader top 7/8/10/12/15 pools, direct top five versus structure penalties, uniform construction within pools, frequency/recent/gap/trend alternatives, equal ensemble weights, eleven sensitivity variants, and separate SB models. Their saved outputs were reused rather than tuned against #1753. All 44 construction methods’ per-origin tickets were independently rescored against historical targets.

| Historical family | Scope | Best confirmation corrected p | Result |
|---|---|---|---|
| Construction | 44 rules | 0.500 | No gate pass |
| Sensitivity | 11 variants × main/SB models | 0.697 | No corrected positive even within a variant |
| Original main models | 8 models | 1.000 | No gate pass |
| Original SB models | 7 models | 1.000 | No gate pass |

Two narrowly defined new hypotheses were fixed in PROTOCOL.txt before their historical testing: remove flat objectives from the main ensemble, and remove flat SB score vectors from the SB ensemble. Remaining original training-only weights are renormalized; if all surviving weights vanish, use equal active weights. The original seed, candidate pools, cutoff and stored pre-target weights are retained. Historical predictions are made before each target is scored. This tests inactive-component handling, not a rule that rewards the actual #1753 winners.

| Domain | Period | n | Mean/accuracy | 95% block CI | Holm p | Δ vs V1 | Paired Δ CI | Pass |
|---|---|---|---|---|---|---|---|---|
| main | all | 126 | 0.706 | 0.571 to 0.857 | 1.000 | 0.087 | -0.008 to 0.206 | False |
| SB | all | 126 | 0.095 | 0.056 to 0.143 | 1.000 | 0.000 | 0.000 to 0.000 | False |
| main | development | 86 | 0.628 | 0.488 to 0.779 | 0.879 | 0.012 | -0.023 to 0.058 | False |
| SB | development | 86 | 0.116 | 0.058 to 0.174 | 0.714 | 0.000 | 0.000 to 0.000 | False |
| main | confirmation | 40 | 0.875 | 0.625 to 1.175 | 0.206 | 0.250 | -0.025 to 0.575 | False |
| SB | confirmation | 40 | 0.050 | 0.000 to 0.100 | 0.920 | 0.000 | 0.000 to 0.000 | False |

On confirmation, the active-component main ensemble improved from 0.625 to 0.875 matches, but corrected p=0.206, mean CI 0.625–1.175 includes the 0.7143 baseline, and paired improvement CI −0.025–0.575 includes zero. The SB change retained the same decisions and 5% accuracy, below the 10% random expectation. Both fail the existing gate. Their outputs are research artifacts, not a promoted V2. No claim is made to have exhaustively tested every imaginable weighting or diversity rule.

## I. Decision and files

**No Super Lotto V2 is justified.** V1 remains frozen. More fresh, predeclared prospective observations are needed before claiming predictive improvement. This task did not generate a next Super Lotto ticket or mix any Lotto data into this analysis.

Saved separately under results/super_lotto/forensic_1753/: REPORT.md, outcome.json, main_evidence.json, draw_coverage.csv, super_ball_evidence.json, candidate_outcomes.json/csv, jev_forensic.json, historical_coverage.json, refinement_origins.json, refinement_performance.json, v2_decision.json, PROTOCOL.txt, v1_preservation_manifest.json and verification.json. Only an outcome event was appended to the existing prospective ledger.

Reproduce from the project root with `python scripts/research/super_1753_forensic.py` then `python scripts/research/report_super_1753.py`. The forensic runner verifies existing freeze hashes, avoids duplicate outcome events and writes only the forensic outputs plus the authorized ledger append. It never calls the V1 main entry point or requests a new Jev response.
