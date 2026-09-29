# Lotto #2341 forensic

Actual #2341: **01 · 04 · 06 · 22 · 33 · 38** (bonus 34, not scored). Frozen V1 Science ticket: **01 · 04 · 13 · 14 · 24 · 38** (C04, B_recent, seeded no-edge fallback), **3/6** (01, 04, 38).

## 1. Frozen record verification

All checks pass: **True**. 17/17 embedded hashes and 8/8 pre-Jev pool hashes match exactly; the ledger hash of `frozen.json` matches; the Jev receipt's state and request hashes match the saved files; V1 code and data are unchanged since the Codex snapshot.

Chronology (UTC): pool frozen 2026-09-27T01:15:00 and committed `c5abf27 2026-09-27T01:15:13+00:00`; Jev receipt 2026-09-27T01:15:14; ticket frozen 2026-09-27T01:15:46, committed `28c78bd 2026-09-27T01:15:53+00:00`, pushed 01:15:55. Scheduled draw 01:25:00 (8:25 PM Jamaica). The freeze script itself asserted `now < 01:25Z`. **The ticket was frozen before the draw.**

## 2. Whole #2341 candidate pool

| ID | Numbers | Generator | Eligible | Matches | Matched | Jev Choice | Jev rank | Sens. top-quartile | Ensemble rank |
|---|---|---|---|---|---|---|---|---|---|
| C01 | 01 · 08 · 15 · 18 · 24 · 25 | A_long | yes | 1 | 01 | 0.04 | 2 | 1.00 | 4 |
| C02 | 02 · 06 · 08 · 12 · 18 · 25 | A_long | yes | 1 | 06 | 0 | 6–16 | 1.00 | 8 |
| C03 | 02 · 10 · 13 · 18 · 24 · 33 | A_long | yes | 1 | 33 | 0.02 | 3 | 0.93 | 2 |
| C04 | 01 · 04 · 13 · 14 · 24 · 38 | B_recent | yes | 3 | 01 04 38 | 0.92 | 1 | 1.00 | 1 |
| C05 | 06 · 08 · 12 · 13 · 24 · 30 | B_recent | yes | 1 | 06 | 0 | 6–16 | 0.93 | 7 |
| C06 | 04 · 09 · 12 · 13 · 24 · 25 | B_recent | yes | 1 | 04 | 0 | 6–16 | 1.00 | 5 |
| C07 | 05 · 11 · 16 · 24 · 27 · 34 | C_gap | no | 0 | — | — | — | 1.00 | 20 |
| C08 | 16 · 26 · 27 · 34 · 35 · 38 | C_gap | no | 1 | 38 | — | — | 1.00 | 19 |
| C09 | 11 · 16 · 21 · 22 · 25 · 34 | C_gap | no | 1 | 22 | — | — | 1.00 | 18 |
| C10 | 01 · 02 · 04 · 07 · 10 · 19 | D_trend | yes | 2 | 01 04 | 0 | 6–16 | 0.93 | 10 |
| C11 | 04 · 07 · 10 · 22 · 24 · 31 | D_trend | yes | 2 | 04 22 | 0 | 6–16 | 0.93 | 6 |
| C12 | 02 · 04 · 07 · 13 · 31 · 32 | D_trend | yes | 1 | 04 | 0 | 6–16 | 0.93 | 9 |
| C13 | 01 · 05 · 08 · 12 · 26 · 34 | E_pairs | yes | 1 | 01 | 0.01 | 4–5 | 0.00 | 14 |
| C14 | 08 · 10 · 11 · 15 · 21 · 24 | E_pairs | yes | 0 | — | 0 | 6–16 | 0.00 | 12 |
| C15 | 06 · 08 · 15 · 17 · 19 · 38 | E_pairs | yes | 2 | 06 38 | 0 | 6–16 | 0.00 | 13 |
| C16 | 04 · 16 · 17 · 21 · 26 · 33 | F_structure | yes | 2 | 04 33 | 0 | 6–16 | 1.00 | 16 |
| C17 | 06 · 07 · 13 · 24 · 32 · 35 | F_structure | yes | 1 | 06 | 0 | 6–16 | 1.00 | 11 |
| C18 | 05 · 11 · 14 · 22 · 23 · 34 | F_structure | no | 1 | 22 | — | — | 1.00 | 17 |
| C19 | 02 · 04 · 08 · 13 · 24 · 34 | G_ensemble | yes | 1 | 04 | 0.01 | 4–5 | 1.00 | 3 |
| C20 | 05 · 07 · 14 · 21 · 33 · 38 | H_random | yes | 2 | 33 38 | 0 | 6–16 | 0.00 | 15 |

Match distribution (20 candidates): 0:2 · 1:12 · 2:5 · 3:1 · 4+:0. Best: **C04** (3/6), which is also the V1 selection and the Jev preference (Choice 0.92). No candidate exceeded 3/6. For 20 independent random tickets, P(at least one ≥3) = 0.55 and P(at least one ≥4) = 0.054, so the pool result is ordinary. Jev Choice vs matches across the 16 eligible candidates: Spearman 0.06. No candidate is promoted retrospectively.

## 3. Exact pre-draw number evidence (cutoff #2340)

Ranks from the frozen `refreshed_rankings.json` (V1 jitter tie-break); `[a–b]` = tie interval. E_pairs was **flat** (0 Holm-retained pairs), so its ranks are arbitrary (tie interval 1–38). F_structure has no number-level ranking. H = V1 walk H ranking for target 2341.

| No. | Role | A_long | B_recent | C_gap | D_trend | E_pairs | G proxy | H | Family top-12 | Freq | Last 30 | Gap | Trend |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 | winner | 6 | 8 | 29 [28–32] | 6 [6–8] | flat | 7 | 16 | A_long, B_recent, D_trend | 33 | 6 | 1 | +0.100 |
| 04 | winner | 10 [7–12] | 4 | 31 [28–32] | 1 | flat | 2 | 7 | A_long, B_recent, D_trend | 32 | 7 | 1 | +0.250 |
| 06 | winner | 13 [13–15] | 13 | 35 [33–38] | 18 [17–24] | flat | 14 | 9 | — | 31 | 5 | 0 | -0.025 |
| 22 | winner | 19 [17–20] | 14 | 11 [10–11] | 16 [12–16] | flat | 15 | 15 | C_gap | 28 | 6 | 8 | +0.050 |
| 33 | winner | 4 [4–5] | 29 | 9 | 13 [12–16] | flat | 16 | 5 | A_long, C_gap | 34 | 3 | 9 | +0.050 |
| 38 | winner | 3 | 7 | 4 | 27 [25–27] | flat | 9 | 35 | A_long, B_recent, C_gap | 35 | 7 | 14 | -0.050 |
| 13 | selected loser | 7 [7–12] | 2 | 28 [28–32] | 3 | flat | 3 | 1 | A_long, B_recent, D_trend | 32 | 8 | 1 | +0.175 |
| 14 | selected loser | 18 [17–20] | 5 | 34 [33–38] | 14 [12–16] | flat | 11 | 23 | B_recent | 28 | 8 | 0 | +0.050 |
| 24 | selected loser | 5 [4–5] | 1 | 20 [18–21] | 4 [4–5] | flat | 1 | 8 | A_long, B_recent, D_trend | 34 | 9 | 4 | +0.150 |

Winner coverage (point value [tie range]; random expectation 6N/38). Historical mean capture over 130 targets (2211–2340) in brackets after the slash.

| Model | Top 5 | Top 7 | Top 10 | Top 12 | Top 15 | Top 20 | Top 25 |
|---|---|---|---|---|---|---|---|
| A_long | 2 / 0.82 | 3 [3–4] / 1.15 | 4 [3–4] / 1.57 | 4 / 1.90 | 5 / 2.37 | 6 / 3.17 | 6 / 3.92 |
| B_recent | 1 / 0.82 | 2 / 1.13 | 3 / 1.68 | 3 / 1.93 | 5 / 2.42 | 5 / 3.32 | 5 / 4.01 |
| C_gap | 1 / 0.79 | 1 / 1.07 | 2 [2–3] / 1.48 | 3 / 1.76 | 3 / 2.29 | 3 / 3.05 | 3 / 3.91 |
| D_trend | 1 / 0.85 | 2 [1–2] / 1.18 | 2 / 1.68 | 2 [2–3] / 1.95 | 3 [3–4] / 2.43 | 5 [4–5] / 3.23 | 5 [5–6] / 3.94 |
| G_marginal_proxy | 1 / 0.78 | 2 / 1.22 | 3 / 1.63 | 3 / 1.94 | 5 / 2.46 | 6 / 3.16 | 6 / 3.99 |
| H_random | 1 / 0.78 | 2 / 1.08 | 3 / 1.57 | 3 / 1.84 | 4 / 2.32 | 5 / 3.09 | 5 / 3.89 |
| random expectation | 0.79 | 1.11 | 1.58 | 1.89 | 2.37 | 3.16 | 3.95 |

A_long and the G proxy put all six #2341 winners in their Top 20 (one-draw hypergeometric p = 0.014). Over the 130 historical targets, all six fell in the Top 20 for A_long 3 times, G proxy 3 times and the H random control 1 times, against 1.8 expected by chance, and the historical mean Top-20 capture was A 3.17, G 3.16, H 3.09 vs 3.16 expected. #2341's broad capture is a single-draw observation, not a validated discovery property.

## 4. Recurring core (01, 04, 13, 24, 38)

| No. | #2339 ranks A/B/C/D/G | #2340 | #2341 | Long-run top-10 rate A / B / D / G | Mean candidates containing it | In V1 final (2339/2340/2341) | In Jev preferred |
|---|---|---|---|---|---|---|---|
| 01 | 6/10/34/8/6 | 6/8/33/3/4 | 6/8/29/6/7 | 0.69 / 0.27 / 0.27 / 0.34 | 3.81 | Y/n/Y | n/n/Y |
| 04 | 13/9/32/4/5 | 9/4/35/1/2 | 10/4/31/1/2 | 0.50 / 0.44 / 0.44 / 0.44 | 4.27 | Y/n/Y | n/n/Y |
| 13 | 12/4/37/2/2 | 12/2/38/2/1 | 7/2/28/3/3 | 0.02 / 0.52 / 0.37 / 0.40 | 2.77 | Y/n/Y | Y/Y/Y |
| 24 | 4/1/26/1/1 | 4/1/21/6/3 | 5/1/20/4/1 | 0.83 / 0.34 / 0.22 / 0.33 | 4.26 | Y/Y/Y | Y/Y/Y |
| 38 | 3/6/5/26/11 | 3/7/4/27/8 | 3/7/4/27/9 | 0.48 / 0.56 / 0.39 / 0.54 | 4.37 | Y/n/Y | n/n/Y |

Top-10 base rate is 10/38 = 0.26. Family score correlations across all cutoffs: A~B 0.58, B~D 0.48, A~D 0.00, B~C -0.48: A, B and D are not independent confirmations.

**Decomposition**
- **A. Model-family support (real but correlated, not predictive evidence):** 01, 24, 38 (and 33) are among the most frequent numbers in the whole history, so the cumulative A_long ranks them top-10 most of the time (24: 83%, 01: 69%). 04 and 13 are recently hot: B_recent/D_trend rank them near the top, while A_long almost never ranks 13 top-10 (2%). "Agreement" between A, B and D is largely shared information.
- **B. Candidate-construction mechanics:** every V1 run searches the same fixed 4,096-combination pool (seed SEED+999) and the H fill uses a fixed seed (SEED+555), so on average 14.0 of the 20 candidates are identical between consecutive cutoffs; 36 tickets appear in 10+ of the 131 reconstructed pools. The H fill ticket 05·07·14·21·33·38 is in all 131 pools; with E_pairs flat, its "top" tickets are the pool's first entries and repeat too. The fixed pool is not itself enriched for the core (0.0073 of pool tickets hold 3+ of 01/04/13/24 vs 0.0088 for random 4-sets).
- **C. Fixed-seed mechanics (the main driver of the FINAL ticket):** V1 creates a fresh `default_rng(20260919)` every run, so the fallback index depends only on the number of eligible candidates n: n=13–16 → index 3, n=17–20 → index 4. Candidates are ordered by generator (C01–C03 A_long, C04–C06 B_recent, C07–C09 C_gap, …), so whenever the first candidates are eligible, V1 lands on a **B_recent** slot: #2339 C05 (index 4 of 20) and #2341 C04 (index 3 of 16) are the **same ticket**. Replayed over 131 historical cutoffs, the production chain used only 5 distinct candidate IDs, B_recent 62% of the time (uniform ≈15%).
- **D. Overlap constraint:** the ≤2-overlap rule excluded 4 candidates in #2340 (including every candidate holding 3+ of 01/04/13/14/24/38), shifting index 3 onto C07 (C_gap); in #2341 it excluded the C_gap tickets C07–C09 and C18 instead, returning index 3 to C04. Together with C this creates an alternating cycle (ticket X, excluded next draw, back two draws later).
- **E. Generator behaviour:** B_recent's top-ranked ticket is stable across cutoffs because its features (last-30 and EW frequency) move slowly; 04, 13 and 24 are in B_recent's top 10 in all three runs (24 is its rank 1 each time).
- **F. Jev:** no causal role. Under the no-edge fallback Jev never affects the selection. Jev preferred C02 in #2339 and #2340 and C04 in #2341.

## 5. Fixed-seed sensitivity (research only; production seed unchanged)

| Metric | Production 20260919 | 1,000 fixed seeds (mean [5–95%]) | Per-draw seeds seed+draw_id (mean [5–95%]) |
|---|---|---|---|
| distinct candidate IDs (131 draws) | 5.000 | 4.780 [2.000–7.000] | 19.968 [20.000–20.000] |
| same ID on consecutive draws | 0.100 | 0.086 [0.000–0.185] | 0.013 [0.000–0.031] |
| share of most-used ID | 0.481 | 0.414 [0.282–0.527] | 0.089 [0.076–0.115] |
| exact ticket repeat 2 draws later | 0.124 | 0.360 [0.070–0.791] | 0.038 [0.016–0.070] |
| mean overlap with previous ticket | 0.723 | 1.001 [0.346–1.623] | 0.907 [0.800–1.023] |
| max selection rate of any number | 0.305 | 0.501 [0.252–0.916] | 0.337 [0.290–0.389] |
| mean matches | 0.855 | 0.938 [0.824–1.053] | 0.943 [0.832–1.053] |
| SD of matches | 0.904 | 0.834 [0.752–0.907] | 0.830 [0.751–0.912] |
| 3+ results (count) | 7.000 | 5.271 [2.000–9.000] | 4.903 [2.000–9.000] |

Without the overlap rule, every fixed seed picks the **same candidate ID at every draw** (100%). **Yes, the fixed-seed fallback mechanically revisits the same region of candidate space**: the cause is the design (a fresh generator with the same seed each run makes the pick a deterministic function of n), not the particular seed value; the production seed is typical among fixed seeds (percentiles distinct_ids 0.61, exact_ticket_repeat_lag2 0.75, mean_matches 0.87). Realized matches do not differ between designs (fixed 0.938, per-draw 0.943, random 0.947), so no seed choice is supported; any change would need a predeclared prospective test. G_ensemble passed the V1 gate at four very early cutoffs (targets 2249, 2250, 2251, 2252, three computed on short histories); those origins are flagged.

## 6. Three-match forensic

Random ticket: P(exactly 3) = 0.03593 (1 in 27.8); P(≥3) = 0.03870; P(≥4) = 0.00276.

Prospective V1 primary tickets: #2339 3, #2340 0, #2341 3 (n=3, total 6, mean 2.0 vs 0.947). Exact P(total ≥6) = 0.039; P(two or more 3+ results in 3) = 0.0044; 3+ rate 2/3 with Clopper–Pearson 95% CI [0.09, 0.99]. Including the #2339 secondary (1 match): P(total ≥7 in 4) = 0.057.

These are uncorrected and **do not establish an edge**: (i) n=3 with an interval spanning almost everything; (ii) #2339 and #2341 are the **same ticket** re-selected by the fixed-seed mechanism, so this is one combination hitting twice, not two method successes; (iii) the question is asked because 3/6 happened, and the ledger tracks many tickets per draw; (iv) over the 131-draw historical replay the same V1 fallback chain averaged 0.855 matches with 7 results of 3+ (5.3% vs 3.9% expected), i.e. no excess where the sample is larger. The cumulative prospective record does not materially depart from random expectation once these points are considered.

## 7. Conclusion

- **Number discovery:** broad but unvalidated. A_long/G put all six winners in their Top 20 and A_long 4 in its Top 12, but historical capture is near random and the H control also reached 5/6 in its Top 20. E_pairs was flat.
- **Candidate construction:** heavily persistent (fixed search pool, fixed H fill, flat E_pairs fallback), so the candidate set changes little between draws. The best candidate (3/6) was in the pool; no candidate reached 4.
- **Final selection:** the seeded no-edge fallback is not uniform over time; with a fresh fixed-seed generator it repeatedly lands on B_recent slots, which produced the same ticket in #2339 and #2341. The 3/6 is consistent with chance.
- **Jev:** preferred the selected ticket (0.92) but had no causal role; its Choice is unrelated to outcomes across the pool (Spearman 0.06, n=16).
- **Recurring core:** long-run frequency (01, 24, 38) and recent frequency (04, 13) surfaced by correlated models, then locked in by construction persistence, the fixed-seed index and the overlap alternation. Recurrence is not predictive evidence.
- **Fixed seed:** a real mechanical artefact of the fallback design, with no measurable effect on realized matches.

**Does #2341 alone justify changing V1? NO.** No corrected historical evidence supports a change. The fixed-seed artefact is documented for a possible future predeclared V1 revision, but it does not affect expected performance and is not changed here.
