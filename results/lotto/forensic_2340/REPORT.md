# LOTTO #2340 FORENSIC RESULTS

**No Lotto V2 is justified.** V1 preserved all six winners within the saved ensemble marginal top 20, and candidate C03 matched four. But the exact winning tuple was absent from the sampled source tickets, and the seeded no-edge final selection C07 matched zero. Historical tests do not show corrected repeatable ranking skill or construction advantage. No fresh Jev call, other-system comparison, or #2341 ticket was produced.

## Integrity and recorded outcome

Official result supplied by the user: **06, 08, 12, 14, 18, 31**, bonus **28**, draw #2340 on September 23, 2026. Frozen Codex primary **05, 11, 16, 24, 27, 34**: **0/6 mains**. Bonus is recorded only as an official outcome; V1 did not predict it and no retrospective bonus score is assigned.

Verified before analysis: all **14 hashes** embedded in the #2340 freeze, plus the ledger checksum of frozen.json. Target #2340, cutoff #2339, seed 20260919, candidate pool, saved rankings, Jev request/response and original code all match. Every file in the #2340 directory was additionally hashed for preservation during this forensic run. Auxiliary CSVs not individually covered by the original freeze are identified by their present preservation hashes; these hashes do not retroactively create original checksums.

The result was appended once to the Lotto ledger without altering prior entries. No Claude, other branch, other session or other system #2340 prediction/analysis was inspected. The outcome is treated as user-supplied official information; no claim is made of a new independent archive fetch.

## A. Exact saved pre-draw positions

| Number | Role | A_long | B_recent | C_gap | D_trend | G_marginal_proxy |
|---|---|---|---|---|---|---|
| 05 | selected loser | 38 | 38 | 8 | 26 | 38 |
| 06 | winner | 15 | 19 | 36 | 17 | 19 |
| 08 | winner | 2 | 6 | 24 | 33 | 10 |
| 11 | selected loser | 21 | 37 | 2 | 28 | 33 |
| 12 | winner | 14 | 18 | 14 | 14 | 15 |
| 14 | winner | 22 | 12 | 6 | 18 | 18 |
| 16 | selected loser | 34 | 27 | 1 | 38 | 37 |
| 18 | winner | 1 | 21 | 31 | 15 | 7 |
| 24 | selected loser | 4 | 1 | 21 | 6 | 3 |
| 27 | selected loser | 33 | 34 | 5 | 34 | 36 |
| 31 | winner | 24 | 17 | 7 | 11 | 20 |
| 34 | selected loser | 27 | 32 | 3 | 32 | 31 |

These are actual stored orders from refreshed_rankings.json, not post-draw ranks. Exact-score tie intervals and scores are retained in number_evidence.json. **G_marginal_proxy is not the complete G_ensemble ticket objective**: it is the weighted individual-score proxy and omits the structure component. The active G ticket objective combines standardized whole-ticket values. The no-edge final selection itself used no marginal-number ranking.

E_pairs had all-zero scores. Its saved tie order for winners 06/08/12/14/18/31 was 27/15/11/29/25/10; those positions are arbitrary and non-informative. F_structure ranks whole combinations, not individual numbers. B_recent blends last-30 frequency and EW frequency; no standalone EW ranking was frozen. Transition statistics were descriptive, not a predictive model. There was no hazard model, separate adaptive-ensemble ranking, or saved final H_random 38-number ordering. Do not substitute newly invented positions for these unavailable fields. The existing learned ensemble is G, not an additional model.

## B. Exact #2340 top-N winner coverage

| Model | Top 6 | Top 8 | Top 10 | Top 12 | Top 15 | Top 20 | Top 25 |
|---|---|---|---|---|---|---|---|
| A_long | 2 (08, 18) | 2 (08, 18) | 2 (08, 18) | 2 (08, 18) | 4 (06, 08, 12, 18) | 4 (06, 08, 12, 18) | 6 (06, 08, 12, 14, 18, 31) |
| B_recent | 1 (08) | 1 (08) | 1 (08) | 2 (08, 14) | 2 (08, 14) | 5 (06, 08, 12, 14, 31) | 6 (06, 08, 12, 14, 18, 31) |
| C_gap | 1 (14) | 2 (14, 31) | 2 (14, 31) | 2 (14, 31) | 3 (12, 14, 31) | 3 (12, 14, 31) | 4 (08, 12, 14, 31) |
| D_trend | 0 (—) | 0 (—) | 0 (—) | 1 (31) | 3 (12, 18, 31) | 5 (06, 12, 14, 18, 31) | 5 (06, 12, 14, 18, 31) |
| G_marginal_proxy | 0 (—) | 1 (18) | 2 (08, 18) | 2 (08, 18) | 3 (08, 12, 18) | 6 (06, 08, 12, 14, 18, 31) | 6 (06, 08, 12, 14, 18, 31) |

Cells show count (exact winner identities). The full file includes the flat E tie order, clearly marked uninformative. E/F are not meaningful discovery rankings. Expected random coverage for the seven pool sizes is 0.947, 1.263, 1.579, 1.895, 2.368, 3.158, 3.947.

| Model | Smallest N for 3 | For 4 | For 5 | For all 6 |
|---|---|---|---|---|
| A_long | 14 | 15 | 22 | 24 |
| B_recent | 17 | 18 | 19 | 21 |
| C_gap | 14 | 24 | 31 | 36 |
| D_trend | 15 | 17 | 18 | 33 |
| G_marginal_proxy | 15 | 18 | 19 | 20 |

## C–E. Discovery, construction and mechanical reachability

**Yes, the saved G marginal top 20 contained all six winners.** A_long needed top 24, B_recent top 21, D_trend top 33 and C_gap top 36. Top 20 is computationally enumerable (38,760 six-number combinations), but it was a diagnostic pool, not an active V1 source constructor or a validated shortlist.

Mechanical answers:

A. All six numbers were individually present in the shared 4,096-tuple source sample, which covered 1–38. All six were also represented somewhere across the final 20 candidates.

B. V1 did **not** use top-N marginal pools as its active final construction source. G top 20 is a saved diagnostic, not evidence that V1 enumerated those 38,760 combinations.

C. With the exact frozen seed/sample, V1 could not produce the winning combination: it was absent from all 4,096 source tuples (4,095 unique) and the one H fallback sample. V1 copies complete sampled tuples; it does not freely recombine their component numbers. The generic uniform sampler permits the combination in principle, but that is different from reachability in this frozen run.

D. Its actual absence occurred before scoring: there is no basis to claim structure optimization, ranking score or diversity rejected that exact tuple. Hypothetically, after C03 was accepted, its four shared winning numbers would conflict with V1’s maximum-three inter-candidate overlap rule; that is a later counterfactual constraint, not the recorded cause of omission. The requested additional-ticket overlap rule would have allowed the winning tuple because it shares only 14 with the previous primary.

Source replay used only the frozen code, seed and #2339-cutoff inputs and reproduced **all 20 candidates exactly**, including generating method. Replayed source tuples and selected indices are saved separately. No candidate was inserted, changed or generated for a future draw.

## J. Why the six selected losers were favored

| Number | Role | Full count | Last30 | EW rate | Gap | Gap percentile | Gap rank | Trend z | G score |
|---|---|---|---|---|---|---|---|---|---|
| 05 | selected loser | 19 | 1 | 0.059 | 11 | 0.833 | 8 | -0.230 | -1.244 |
| 06 | winner | 30 | 4 | 0.189 | 0 | 0.172 | 36 | 0.000 | 0.117 |
| 08 | winner | 37 | 7 | 0.212 | 3 | 0.639 | 24 | -1.152 | 0.489 |
| 11 | selected loser | 27 | 1 | 0.068 | 17 | 0.962 | 2 | -0.461 | -0.845 |
| 12 | winner | 30 | 5 | 0.168 | 6 | 0.724 | 14 | 0.230 | 0.227 |
| 14 | winner | 27 | 7 | 0.151 | 12 | 0.885 | 6 | 0.000 | 0.127 |
| 16 | selected loser | 23 | 4 | 0.117 | 21 | 1.000 | 1 | -2.073 | -1.166 |
| 18 | winner | 38 | 4 | 0.174 | 1 | 0.432 | 31 | 0.230 | 0.600 |
| 24 | selected loser | 34 | 9 | 0.233 | 3 | 0.545 | 21 | 1.152 | 1.330 |
| 27 | selected loser | 23 | 2 | 0.098 | 12 | 0.864 | 5 | -1.152 | -1.114 |
| 31 | winner | 26 | 5 | 0.171 | 11 | 0.880 | 7 | 0.461 | 0.086 |
| 34 | selected loser | 26 | 3 | 0.102 | 16 | 0.960 | 3 | -0.691 | -0.683 |

C07 was generated by **C_gap**. Selected numbers 16, 11, 34, 27 and 05 had long gaps (21, 17, 16, 12 and 11 draws) and gap ranks 1, 2, 3, 5 and 8. Winners 06 and 18 had gaps 0 and 1 and ranked 36 and 31 under gap. Thus the gap objective favored long-absent losing numbers over those recent winners. This explains the pre-draw heuristic’s behavior; it does not establish that absence is predictive or that reversing gap scores would help.

The final system did **not** establish that C07 was superior to the winners or other candidates. No method passed the empirical gate, so C07 was selected uniformly from the 16 diversified eligible candidates using the fixed seed. Its G ranks were 38, 33, 37, 3, 36 and 31; most selected losers were actually weak under the ensemble proxy. Number 24 was the exception, with strong frequency/recent evidence but no realized hit. Candidate optimization over a finite sample and diversification explain why C07 is not simply the six highest gap ranks.

C07 had complete-ticket support labels C_gap, F_structure; those correlated, unvalidated labels are not independent model confirmation. Its saved sensitivity rank range was 1–1, with top-quartile fraction 100.00%. Number-level sensitivity was not saved. All twelve examined numbers had zero corrected pair/network score. The saved transition rows from latest-draw triggers to these numbers all had Holm p=1; no transition signal drove V1 selection.

| Number | Top-12 ranking labels | Candidate appearances | Candidate IDs |
|---|---|---|---|
| 05 | C_gap | 5 | C07, C09, C13, C18, C20 |
| 06 | None | 4 | C03, C10, C15, C17 |
| 08 | A_long, B_recent, G_marginal_proxy | 6 | C01, C03, C13, C14, C15, C19 |
| 11 | C_gap | 3 | C07, C14, C18 |
| 12 | None | 3 | C03, C06, C13 |
| 14 | B_recent, C_gap | 3 | C04, C18, C20 |
| 16 | C_gap | 4 | C07, C08, C09, C16 |
| 18 | A_long, G_marginal_proxy | 3 | C01, C02, C03 |
| 24 | A_long, B_recent, D_trend, G_marginal_proxy | 9 | C01, C02, C04, C06, C07, C12, C14, C17, C19 |
| 27 | C_gap | 3 | C07, C08, C09 |
| 31 | C_gap, D_trend | 3 | C09, C11, C12 |
| 34 | C_gap | 5 | C07, C08, C13, C18, C19 |

The model labels above share data and are not independent families. number_evidence.json retains all saved rolling frequencies, EW rate, current/complete gaps, percentile, volatility, trend, scores, exact rank/tie positions, candidate memberships, candidate-level sensitivity and relevant saved transition rows. No new hazard score, causal account, or per-number stability series is invented.

## F–H. Complete frozen candidate scoring

Four of the 20 frozen candidates were excluded by the requested additional-ticket overlap limit before Jev. Their missing Choice probabilities are **N/A**, not zero. Jev evaluated the remaining 16 complete tickets.

| ID | Frozen numbers | Generator | Hits | Matched | Jev Choice | Eligible |
|---|---|---|---|---|---|---|
| C01 | 01, 08, 15, 18, 24, 25 | A_long | 2 | 08, 18 | 3.00% | True |
| C02 | 02, 10, 13, 18, 24, 33 | A_long | 1 | 18 | 89.00% | True |
| C03 | 02, 06, 08, 12, 18, 25 | A_long | 4 | 06, 08, 12, 18 | 0.00% | True |
| C04 | 01, 04, 13, 14, 24, 38 | B_recent | 1 | 14 | N/A | False |
| C05 | 01, 02, 04, 10, 13, 35 | B_recent | 0 | — | N/A | False |
| C06 | 04, 09, 12, 13, 24, 25 | B_recent | 1 | 12 | N/A | False |
| C07 | 05, 11, 16, 24, 27, 34 | C_gap | 0 | — | 0.00% | True |
| C08 | 16, 26, 27, 34, 35, 38 | C_gap | 0 | — | 0.00% | True |
| C09 | 05, 16, 19, 27, 31, 38 | C_gap | 1 | 31 | 0.00% | True |
| C10 | 02, 04, 06, 13, 28, 29 | D_trend | 1 | 06 | 1.00% | True |
| C11 | 02, 04, 07, 13, 31, 32 | D_trend | 1 | 31 | 0.00% | True |
| C12 | 04, 07, 10, 22, 24, 31 | D_trend | 1 | 31 | 6.00% | True |
| C13 | 01, 05, 08, 12, 26, 34 | E_pairs | 2 | 08, 12 | 1.00% | True |
| C14 | 08, 10, 11, 15, 21, 24 | E_pairs | 1 | 08 | 0.00% | True |
| C15 | 06, 08, 15, 17, 19, 38 | E_pairs | 2 | 06, 08 | 0.00% | True |
| C16 | 04, 16, 17, 21, 26, 33 | F_structure | 0 | — | 0.00% | True |
| C17 | 06, 07, 13, 24, 32, 35 | F_structure | 1 | 06 | 0.00% | True |
| C18 | 05, 11, 14, 22, 23, 34 | F_structure | 1 | 14 | 0.00% | True |
| C19 | 02, 04, 08, 13, 24, 34 | G_ensemble | 1 | 08 | N/A | False |
| C20 | 05, 07, 14, 21, 33, 38 | H_random | 1 | 14 | 0.00% | True |

| Main matches | Candidate count |
|---|---|
| 0 | 4 |
| 1 | 12 |
| 2 | 3 |
| 3 | 0 |
| 4 | 1 |
| 5 | 0 |
| 6 | 0 |

**Best: C03**, matching **06, 08, 12 and 18** (4/6). It was eligible for the additional ticket and received Jev Choice probability 0%. **Final C07:** zero matches, tied positions **17–20 of all 20**, or **14–16 among the 16 eligible candidates**. All six eventual winners appeared somewhere in the full shortlist; none was completely missing. No candidate held five or six winners.

**Jev preferred C02**, matching **18** (1/6). Frozen model `jev-1.13.0`, Choice probability **89.00%**, confidence **0.880**. The final C07 was not Jev’s selection: the no-edge fallback overrode model preference by design. Neither Jev nor the policy chose the hindsight-best C03.

## I. Frozen Jev judgments and realized association

| ID | Robustness | Consensus | Quality | Overfit/chance | Stable | Stronger than random | Single-model dependence |
|---|---|---|---|---|---|---|---|
| C01 | 0.290 | 0.010 | 0.060 | 95.00% | 36.00% | 5.00% | 84.00% |
| C02 | 0.250 | 0.040 | 0.050 | 95.00% | 39.00% | 5.00% | 59.00% |
| C03 | 0.060 | 0.010 | 0.060 | 95.00% | 29.00% | 4.00% | 84.00% |
| C07 | 0.010 | 0.010 | 0.000 | 96.00% | 19.00% | 3.00% | 80.00% |
| C08 | 0.010 | 0.010 | 0.000 | 95.00% | 22.00% | 4.00% | 88.00% |
| C09 | 0.010 | 0.010 | 0.000 | 95.00% | 19.00% | 4.00% | 81.00% |
| C10 | 0.150 | 0.030 | 0.020 | 95.00% | 24.00% | 5.00% | 80.00% |
| C11 | 0.190 | 0.030 | 0.040 | 95.00% | 37.00% | 5.00% | 75.00% |
| C12 | 0.260 | 0.040 | 0.060 | 94.00% | 39.00% | 5.00% | 36.00% |
| C13 | 0.010 | 0.000 | 0.000 | 95.00% | 7.00% | 3.00% | 13.00% |
| C14 | 0.020 | 0.000 | 0.010 | 96.00% | 8.00% | 4.00% | 19.00% |
| C15 | 0.020 | 0.000 | 0.010 | 95.00% | 9.00% | 4.00% | 25.00% |
| C16 | 0.040 | 0.020 | 0.010 | 95.00% | 30.00% | 4.00% | 84.00% |
| C17 | 0.190 | 0.030 | 0.030 | 94.00% | 44.00% | 4.00% | 59.00% |
| C18 | 0.030 | 0.040 | 0.010 | 95.00% | 30.00% | 4.00% | 61.00% |
| C20 | 0.020 | 0.010 | 0.010 | 96.00% | 9.00% | 4.00% | 72.00% |

For the 16 evaluated options, tie-aware Spearman correlation of Choice probability with realized matches is **0.266**. Whole-uniform-draw simulation preserving ticket overlap (20,000 draws) gives descriptive two-sided p **0.346**. Choice-weighted matches were 1.040, versus unweighted eligible-candidate mean 1.188. This is not a meaningful demonstrated relationship in one draw. It does not establish that Jev is systematically good or bad at forecasting.

The complete frozen Choice distribution is shown in the candidate table. Raw Score distributions/confidences and Nouls are preserved in frozen_jev_analysis.json. Choice probabilities reflect the supplied evidence-preference question, not lottery-winning probabilities; confidence describes distribution concentration. [Current TypeSafe confidence documentation](https://docs.typesafe.ai/confidence) was consulted. No new Jev request was made.

## What happened versus what is repeatable

For this draw, the broad G ranking contained all winners, the sampled source omitted their complete tuple, a four-hit candidate existed, and the seeded final rule picked a zero-hit candidate. These are realized construction/selection limitations, not proof of a predictive ranking edge. A fixed uniform six-number ticket has zero-main-match probability **32.82%**, so 0/6 is ordinary under the random null.

Descriptively this combines partial number discovery, complete-ticket source coverage failure, and hindsight selection loss, with ordinary random variation. It is not a failure to represent the winners individually, nor can the final miss be attributed to Jev choosing C07. The historical tests below address repeatability rather than explaining the result with a newly invented rule.

## Historical number discovery through #2339

129 strict expanding-window targets after 50 warmup draws. All features use prior targets only; learned ensemble weights are taken from the corresponding saved pre-target V1 record. Ranking orders for historical targets were reconstructed from frozen prior data and original tie rules; they are not mislabeled as originally saved full orders. #2340 is excluded. Final 40 targets are reused retrospective confirmation, not a fresh holdout.

| Pool | Random mean | Random 3+ | Random 4+ | Random 5+ | Random all6 |
|---|---|---|---|---|---|
| 6 | 0.947 | 3.87% | 0.28% | 0.01% | 0.00% |
| 8 | 1.263 | 9.40% | 1.16% | 0.06% | 0.00% |
| 10 | 1.579 | 17.38% | 3.14% | 0.26% | 0.01% |
| 12 | 1.895 | 27.33% | 6.61% | 0.78% | 0.03% |
| 15 | 2.368 | 44.38% | 15.19% | 2.68% | 0.18% |
| 20 | 3.158 | 72.06% | 38.36% | 11.51% | 1.40% |
| 25 | 3.947 | 91.00% | 67.18% | 31.43% | 6.42% |

| Model | Pool | Confirmation mean | 3+ | 4+ | 5+ | All6 | Mean Holm p | Best event Holm p |
|---|---|---|---|---|---|---|---|---|
| A_long | 6 | 0.950 | 2.50% | 0.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| A_long | 8 | 1.300 | 10.00% | 0.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| A_long | 10 | 1.625 | 15.00% | 0.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| A_long | 12 | 1.900 | 27.50% | 5.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| A_long | 15 | 2.425 | 50.00% | 17.50% | 0.00% | 0.00% | 1.000 | 1.000 |
| A_long | 20 | 3.250 | 70.00% | 50.00% | 12.50% | 5.00% | 1.000 | 1.000 |
| A_long | 25 | 3.875 | 87.50% | 60.00% | 32.50% | 7.50% | 1.000 | 1.000 |
| B_recent | 6 | 0.950 | 5.00% | 0.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| B_recent | 8 | 1.350 | 15.00% | 0.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| B_recent | 10 | 1.675 | 27.50% | 0.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| B_recent | 12 | 1.875 | 35.00% | 7.50% | 0.00% | 0.00% | 1.000 | 1.000 |
| B_recent | 15 | 2.425 | 47.50% | 17.50% | 2.50% | 0.00% | 1.000 | 1.000 |
| B_recent | 20 | 3.300 | 82.50% | 45.00% | 12.50% | 0.00% | 1.000 | 1.000 |
| B_recent | 25 | 3.925 | 95.00% | 67.50% | 32.50% | 0.00% | 1.000 | 1.000 |
| C_gap | 6 | 0.825 | 5.00% | 0.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| C_gap | 8 | 1.050 | 7.50% | 0.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| C_gap | 10 | 1.350 | 10.00% | 0.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| C_gap | 12 | 1.575 | 15.00% | 0.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| C_gap | 15 | 2.150 | 32.50% | 12.50% | 2.50% | 0.00% | 1.000 | 1.000 |
| C_gap | 20 | 2.900 | 60.00% | 32.50% | 7.50% | 2.50% | 1.000 | 1.000 |
| C_gap | 25 | 3.900 | 85.00% | 67.50% | 27.50% | 10.00% | 1.000 | 1.000 |
| D_trend | 6 | 1.100 | 5.00% | 0.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| D_trend | 8 | 1.475 | 10.00% | 0.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| D_trend | 10 | 1.800 | 27.50% | 2.50% | 0.00% | 0.00% | 1.000 | 1.000 |
| D_trend | 12 | 1.975 | 40.00% | 2.50% | 0.00% | 0.00% | 1.000 | 1.000 |
| D_trend | 15 | 2.400 | 47.50% | 20.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| D_trend | 20 | 3.325 | 70.00% | 50.00% | 15.00% | 0.00% | 1.000 | 1.000 |
| D_trend | 25 | 3.875 | 85.00% | 67.50% | 30.00% | 5.00% | 1.000 | 1.000 |
| G_marginal_proxy | 6 | 1.100 | 10.00% | 0.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| G_marginal_proxy | 8 | 1.350 | 12.50% | 2.50% | 0.00% | 0.00% | 1.000 | 1.000 |
| G_marginal_proxy | 10 | 1.600 | 17.50% | 5.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| G_marginal_proxy | 12 | 1.875 | 27.50% | 7.50% | 0.00% | 0.00% | 1.000 | 1.000 |
| G_marginal_proxy | 15 | 2.600 | 45.00% | 17.50% | 7.50% | 0.00% | 1.000 | 1.000 |
| G_marginal_proxy | 20 | 3.175 | 77.50% | 32.50% | 12.50% | 0.00% | 1.000 | 1.000 |
| G_marginal_proxy | 25 | 4.175 | 97.50% | 70.00% | 45.00% | 5.00% | 1.000 | 1.000 |
| H_random | 6 | 0.975 | 5.00% | 0.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| H_random | 8 | 1.225 | 7.50% | 0.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| H_random | 10 | 1.600 | 12.50% | 0.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| H_random | 12 | 1.950 | 25.00% | 5.00% | 0.00% | 0.00% | 1.000 | 1.000 |
| H_random | 15 | 2.500 | 50.00% | 10.00% | 5.00% | 0.00% | 1.000 | 1.000 |
| H_random | 20 | 3.325 | 80.00% | 42.50% | 10.00% | 0.00% | 1.000 | 1.000 |
| H_random | 25 | 4.075 | 95.00% | 62.50% | 42.50% | 7.50% | 1.000 | 1.000 |

No corrected repeatable discovery advantage was found. All full-period and confirmation mean-coverage and event-family Holm p-values were 1.000. Exact hypergeometric pool-size references and exact event-tail tests account for larger pools mechanically capturing more winners. Full/development/confirmation counts and rates are in historical_discovery.json. Random ordering is a control; flat E and combination-only F are not counted as serious number-discovery models.

## K. Historical discovery-to-construction loss

For a pool capturing q eventual winners, the hindsight best possible six-number ticket captures q. This oracle is **not an executable forecast**. A uniformly chosen six from that same m-number pool captures 6q/m on average and loses q(1−6/m) relative to the oracle. Under a random pool plus random nested ticket, expected loss is 6(m−6)/38. Therefore a large oracle-to-ticket gap arises even when rankings contain no usable information.

For the G marginal proxy, confirmation results were:

| Pool | Constructor | Pool winners | Ticket hits | Oracle loss | Conditional random loss | Excess hits vs conditional random | Holm p |
|---|---|---|---|---|---|---|---|
| 6 | direct_top6 | 1.100 | 1.100 | 0.000 | 0.000 | 0.000 | 1.000 |
| 6 | uniform | 1.100 | 1.100 | 0.000 | 0.000 | 0.000 | 1.000 |
| 8 | direct_top6 | 1.350 | 1.100 | 0.250 | 0.338 | 0.087 | 1.000 |
| 8 | structure025 | 1.350 | 1.025 | 0.325 | 0.338 | 0.013 | 1.000 |
| 8 | uniform | 1.350 | 0.950 | 0.400 | 0.338 | -0.062 | 1.000 |
| 10 | direct_top6 | 1.600 | 1.100 | 0.500 | 0.640 | 0.140 | 1.000 |
| 10 | structure025 | 1.600 | 1.000 | 0.600 | 0.640 | 0.040 | 1.000 |
| 10 | uniform | 1.600 | 0.950 | 0.650 | 0.640 | -0.010 | 1.000 |
| 12 | direct_top6 | 1.875 | 1.100 | 0.775 | 0.938 | 0.163 | 1.000 |
| 12 | structure025 | 1.875 | 0.975 | 0.900 | 0.938 | 0.037 | 1.000 |
| 12 | uniform | 1.875 | 1.000 | 0.875 | 0.938 | 0.062 | 1.000 |
| 15 | direct_top6 | 2.600 | 1.100 | 1.500 | 1.560 | 0.060 | 1.000 |
| 15 | structure025 | 2.600 | 0.975 | 1.625 | 1.560 | -0.065 | 1.000 |
| 15 | uniform | 2.600 | 1.050 | 1.550 | 1.560 | 0.010 | 1.000 |
| 20 | direct_top6 | 3.175 | 1.100 | 2.075 | 2.223 | 0.148 | 1.000 |
| 20 | structure025 | 3.175 | 0.975 | 2.200 | 2.223 | 0.023 | 1.000 |
| 20 | uniform | 3.175 | 0.900 | 2.275 | 2.223 | -0.052 | 1.000 |
| 25 | direct_top6 | 4.175 | 1.100 | 3.075 | 3.173 | 0.098 | 1.000 |
| 25 | uniform | 4.175 | 1.050 | 3.125 | 3.173 | 0.048 | 1.000 |

Example: G top 20 captured 3.175 winners per confirmation draw. Its structure constructor retained 0.975, an oracle gap of 2.200. Uniform construction conditional on that same pool coverage would lose 2.2225 on average. Thus the large raw gap is almost exactly what ordinary compression predicts; it does not demonstrate discarded predictive information. Direct top six retained 1.100, but its conditional excess also failed correction.

All models, pools and constructors are reported for full/development/confirmation in compression_analysis.json, with conditional exact convolution tests, corrected p-values and block CIs. Random_compression_controls.json contains 20,000 nested random-pool/random-ticket 40-target simulations per pool size. No corrected conditional construction advantage is established. These corresponding constructors always select inside their discovery pool; the original V1 512-sample tickets are not falsely treated as constrained top-N constructions.

## L–M. Predeclared refinements and V2 decision

Before the historical tests, PROTOCOL.txt fixed a finite family: direct top six, uniform selection within top 6/8/10/12/15/20/25, exact additive-plus-structure search within top 8/10/12/15/20, larger G source search, equal ensemble weights and exclusion of inactive G components. The raw audit has 68 method labels; five top6-uniform labels are algebraically identical to direct top6 and are removed for the **63-rule primary Holm correction**. None uses #2340 to fit parameters. Pure additive maximization within any larger pool is already direct top six, so it is not counted as a new success.

| Method | Confirmation mean | 95% block CI | Raw p | Holm p | Δ vs V1 G | Paired CI | Pass |
|---|---|---|---|---|---|---|---|
| D_trend:top10:structure025 | 1.225 | 0.950 to 1.500 | 0.024 | 1.000 | 0.350 | 0.100 to 0.600 | False |
| D_trend:top12:structure025 | 1.175 | 0.925 to 1.475 | 0.053 | 1.000 | 0.300 | 0.025 to 0.550 | False |
| D_trend:top15:structure025 | 1.150 | 0.900 to 1.425 | 0.076 | 1.000 | 0.275 | 0.025 to 0.525 | False |
| D_trend:top20:structure025 | 1.150 | 0.900 to 1.425 | 0.076 | 1.000 | 0.275 | 0.025 to 0.525 | False |
| D_trend:top8:uniform | 1.150 | 1.000 to 1.325 | 0.076 | 1.000 | 0.275 | 0.075 to 0.450 | False |
| D_trend:top8:structure025 | 1.125 | 0.875 to 1.375 | 0.106 | 1.000 | 0.250 | 0.025 to 0.475 | False |
| B_recent:top15:uniform | 1.100 | 0.900 to 1.275 | 0.143 | 1.000 | 0.225 | -0.050 to 0.475 | False |
| B_recent:top8:uniform | 1.100 | 0.825 to 1.375 | 0.143 | 1.000 | 0.225 | -0.100 to 0.575 | False |
| D_trend:top6 | 1.100 | 0.850 to 1.350 | 0.143 | 1.000 | 0.225 | 0.025 to 0.450 | False |
| G_marginal_proxy:top6 | 1.100 | 0.875 to 1.325 | 0.143 | 1.000 | 0.225 | 0.050 to 0.425 | False |
| D_trend:top15:uniform | 1.075 | 0.825 to 1.375 | 0.189 | 1.000 | 0.200 | -0.075 to 0.500 | False |
| B_recent:top10:uniform | 1.050 | 0.850 to 1.275 | 0.244 | 1.000 | 0.175 | -0.125 to 0.475 | False |

The strongest raw result was D_trend within top 10 with structure penalty 0.25: mean 1.225, raw p=0.024, but Holm p=1.000 after the declared search. A positive paired contrast against a weak V1 G benchmark does not override the failed corrected random-null gate. No method passed the gate, so no favorable post-hoc stability search was used to rescue it. Existing frozen sensitivity variants also remain exploratory rather than promoted models.

**No Lotto V2 is justified.** V1 remains unchanged. No #2341 prediction, candidate recommendation or fresh prospective Jev call was generated.

## Files and reproducibility

All forensic outputs are separate under results/lotto/forensic_2340/. The only change outside that directory is the requested append-only outcome event in results/lotto/prospective_ledger.jsonl and new forensic scripts/log. integrity.json records verified original hashes; verification.json confirms preservation, exact candidate replay, cutoff and zero new Jev calls. Main evidence, exact coverage, minimum pool sizes, every candidate outcome, original Jev judgments, reachability, historical discovery, construction, compression and random controls are saved as machine-readable artifacts.

From the project root run `python scripts/research/lotto_2340_forensic.py`, then `python scripts/research/report_lotto_2340.py`. These never run the original analysis main entry point, overwrite the frozen run, or call Jev. The ledger outcome append is idempotent. Supporting input preservation is checked again after report rendering.
