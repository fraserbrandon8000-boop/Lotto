# CLAUDE ONLY — LOTTO #2340

**01 · 04 · 13 · 18 · 24 · 25**

Candidate **C06** from the frozen clean-room pool. It was produced by `G_ensemble_equal|opt_top12`. Frozen at 2026-09-23T18:01:55Z (13:01 Jamaica time), before draw #2340.

**Validated predictive edge: No.** This ticket has the same chance as any other: 0.947 expected matches and a 3.87% chance of 3 or more matches. The rubric score measures how well the frozen evidence supports a candidate. It is not a probability and it is not a claim of a better chance to win.

---

## What this experiment is

This is a Claude-only choice of one ticket from the 21-candidate pool frozen at commit `91eae5d6aed8cdc45227e992949748c66c2bd52b`. TypeSafe and Jev were not involved. Nothing was recomputed: no dataset, walk-forward, models, rankers, candidates, random baselines or sensitivity analysis. The scorer only reads frozen JSON fields and ranks them.

## Order of operations

1. Created branch `claude/lotto-2340-claude-only` directly from `91eae5d`. No later commit was checked out, logged, diffed or shown.
2. Read `protocol.json` in full. Looked only at the key names and types of the output files, with values masked.
3. Wrote the rubric (`config/selection_rubric.json`) and the scorer (`code/select_claude_only.py`). Tested the scorer once on a purely synthetic fixture, then threw that output away.
4. Froze the rubric and scorer by recording their hashes in `config/rubric_freeze.json`, then committed (`9ca90af`) and pushed **before** any evaluation.
5. Ran the scorer once on the real frozen evidence. The first valid result is the experiment of record. It was committed (`5417592`) and pushed immediately.

**Incidental exposure before the freeze:** the masked schema dumps showed a few key names and list lengths. These were C01's generating-method name, the counterevidence item counts for C01–C04, and 0 methods surviving Holm correction. No candidate numbers or metric values were displayed. Details are in `config/rubric_freeze.json`.

## Rubric (frozen before selection)

| # | Criterion | Weight | Raw metric (from frozen fields only) |
|---|---|---|---|
| R1 | Multi-family support | 8 | Mean share of the 5 independent families (A_freq_all, B_ew_20, C_hazard, D_trend_20v40, E_transition) ranking each number top-12 |
| R2 | Confirmation-period evidence | 7 | z of the generating method's confirmation mean against the random 0.947 (n = 70) |
| R3 | Ranking consistency | 6 | The ticket's mean percentile under its *least* favourable of 8 core rankers |
| R4 | Ticket sensitivity / stability | 5 | Frozen "variants keeping 4+ numbers" fractions (lambda grid, sibling rankers) |
| R5 | Low dependence on one model | 4 | 1 − largest single-ranker share of the ticket's top-12 votes |
| R6 | Low overfitting | 3 | − standardized drop from development to confirmation |
| R7 | Candidate-level evidence | 2 | Ensemble percentile, and fewer counterevidence items |
| R8 | Robustness across assumptions | 1 | Share of the generating ranker's 64 lambda-grid variants beating random in confirmation |

Each criterion is converted to a rank-normalized score u in [0, 1] across all 21 candidates. The composite is S = Σ w·u / 36. The random controls are scored as calibration points but cannot be selected. Structure, balance, consecutive-number, recent-winner and "looks random" criteria are explicitly excluded.

## Candidate evaluation (all 21)

| Pos | ID | Eligible | Numbers | S | Generating method(s) |
|---|---|---|---|---|---|
| **1** | **C06** | yes | **01 04 13 18 24 25** | **0.821** | G_ensemble_equal\|opt_top12 |
| 2 | C09 | yes | 01 04 10 13 18 24 | 0.775 | consensus |
| 3 | C11 | yes | 04 08 09 13 24 35 | 0.726 | B_ew_40\|opt_top12 |
| 4 | C07 | yes | 01 02 06 18 25 35 | 0.703 | E_transition\|opt_top12 |
| 5 | C08 | yes | 01 04 09 10 13 24 | 0.699 | B_ew_10\|opt_top12 |
| 6 | C18 | yes | 04 09 10 13 24 35 | 0.689 | B_ew_20 + G_ensemble_adaptive \|opt_top12 |
| 7 | C12 | yes | 01 08 13 18 24 25 | 0.660 | A_freq_all\|opt_top12 |
| 8 | C20 | yes | 01 02 04 07 13 24 | 0.621 | B_roll_10 + B_roll_20 + D_trend_20v40 \|opt_top12 |
| 9 | C16 | yes | 06 09 10 31 35 38 | 0.601 | B_roll_50\|opt_top12 |
| 10 | C19 | yes | 08 09 13 15 22 24 | 0.554 | B_roll_30\|opt_top12 |
| 11 | C17 | yes | 01 04 06 13 18 29 | 0.453 | B_roll_10\|pair_top12 (dev-selected) |
| 12 | C13 | control | 01 21 26 31 34 36 | 0.449 | H_random\|top6 |
| 13 | C15 | yes | 01 04 13 18 28 29 | 0.441 | C_recent\|opt_top12 |
| 14 | C05 | yes | 01 06 08 13 35 38 | 0.412 | B_roll_100\|opt_top12 |
| 15 | C01 | yes | 03 04 13 18 24 29 | 0.390 | D_slope_50\|opt_top12 |
| 16 | C03 | yes | 03 09 16 17 24 26 | 0.292 | C_hazard\|opt_top12 |
| 17 | C21 | yes | 16 27 31 34 35 38 | 0.292 | C_own_gap_pct\|opt_top12 |
| 18 | C04 | control | 02 16 17 25 33 37 | 0.283 | random_ticket |
| 19 | C14 | yes | 05 11 16 31 32 34 | 0.269 | C_overdue\|opt_top12 |
| 20 | C02 | yes | 05 16 23 28 29 32 | 0.186 | A_inv_cold\|opt_top12 |
| 21 | C10 | yes | 11 14 18 21 25 34 | 0.185 | E_pair_centrality\|opt_top12 |

Raw and normalized values for every criterion are in `outputs/candidate_evaluation.csv` and `outputs/candidate_evaluation.json`.

## Selection basis

C06 has the highest composite score among the 19 eligible candidates. It ranks near the top on the four highest-priority criteria that measure breadth of support:

- **R1 multi-family support:** 0.733. 22 of 30 number-family slots are top-12, second only to the consensus ticket (0.767). Every number is top-12 in at least 2 families, and 24 is top-12 in all 5.
- **R3 consistency:** the worst core-ranker percentile is 0.48. Six of the eight core rankers place the ticket at a mean percentile of 0.80 or higher.
- **R5 low single-model dependence:** 0.829. The largest single-ranker share of its top-12 votes is 17%.
- **R6 overfitting:** the method did not decay from development to confirmation (0.900 → 1.014).
- **R4 / R8 stability:** the ticket keeps 4+ numbers in 16 of 16 lambda-grid variants. In 59 of the 64 lambda-grid variants of its generating ranker, confirmation performance was above random.

## Top supporting evidence

- The pre-registered equal-weight ensemble of the five independent model families supports the ticket, with a mean ensemble percentile of 0.92.
- The generating method's confirmation-period mean was 1.014 against 0.947 for random. It showed no development-to-confirmation decay and was robust across 59 of 64 construction assumptions.
- C06 scores above both random controls (C13 0.449, C04 0.283) and above the dev-selected method's ticket (C17 0.453).

## Main counterevidence

- **No validated edge.** All global randomness tests are consistent with an independent uniform draw (min Holm p = 1.0). No ticket method survives Holm correction. The pre-registered dev-selected method (B_roll_10|pair_top12) fell to 0.914 in confirmation (p = 0.65), and only 3 of its 8 sensitivity variants beat baseline.
- C06's own method is indistinguishable from chance:
  - full-period mean 0.957 against 0.947 (p = 0.46, Holm p = 1.0)
  - development mean 0.900, below random
  - confirmation excess +0.067 (p = 0.27), far under the 0.247 minimum detectable at 80% power
- A **random control beat C06 on the confirmation criterion.** H_random|top6 had a confirmation mean of 1.043 against C06's 1.014.
- The gap-hazard and pair-centrality rankers give the ticket only middling support (mean percentiles 0.55 and 0.48). Number 25 is top-12 in only 2 of 5 families. The sibling-ranker stability field is 0/1.
- Part of C06's margin over the consensus ticket C09 comes from R4. The frozen file marks C09's sensitivity as "n/a", so C09 scored 0 there under the pre-declared rule. That reflects non-applicability, not measured instability.

## Validity checks

173 checks ran and 24 failed, all of the same type. Candidate-level development and confirmation means were compared with `05_ticket_method_performance.json` at a tolerance of 1e-9. The candidate file stores those means rounded to 3 decimals (maximum difference 0.00043), so the two files agree to stored precision.

Because of the no-rerank rule, scoring was not repeated at full precision. Every other check passed: numbers valid, null SD matches, all ranks match the rankings file, and all family top-12 counts match. See `outputs/post_run_check_notes.json`.

## Isolation confirmations

- [x] Branch `claude/lotto-2340-claude-only` created from commit `91eae5d`
- [x] No later commit was checked out, logged, diffed, shown or read
- [x] No Jev response was accessed. The Jev-specific files at `91eae5d` were not opened: `jev/`, `06_build_jev_request.py`, `07_call_jev_once.py`, and the values of `decision_rule.json` (only its key names were seen, to classify it)
- [x] TypeSafe and Jev were not called
- [x] No Codex prediction and no other completed #2340 pick was inspected
- [x] The existing 21-candidate pool was used as-is and not regenerated or edited
- [x] No statistical model was rerun
- [x] The selection rubric was frozen, committed and pushed (`9ca90af`) before the final selection
- [x] This is Claude's first valid final choice (a single real run)
- [x] No number was manually changed (the stored order is already ascending)
- [x] The result was frozen and pushed (`5417592`) before draw #2340

## Files

| File | Contents |
|---|---|
| `config/selection_rubric.json` | Frozen rubric |
| `config/rubric_freeze.json` | Freeze record: hashes, what was and wasn't viewed |
| `code/select_claude_only.py` | Read-only scorer; refuses to run a second time |
| `outputs/candidate_evaluation.{json,csv}` | Evaluation of all 21 candidates |
| `outputs/final_prediction.json` | Final ticket, prediction hash |
| `outputs/post_run_check_notes.json` | Diagnosis of the failed tolerance checks |
| `prospective_ledger.jsonl` | Prospective ledger entry (pending draw) |
| `TIMESTAMP.json` | Freeze times and commits |
| `HASHES.sha256` | SHA-256 of every experiment file and every frozen input used |

Prediction SHA-256: `a821c1943ab96c5a4e095ce43456aed4396526afc4eb6e24ff4ca4fc75975d78`, computed over `LOTTO#2340|1-4-13-18-24-25|C06|<rubric sha256>|<source commit>`.
