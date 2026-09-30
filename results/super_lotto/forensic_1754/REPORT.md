# Super Lotto #1754 forensic

Actual #1754: **03 · 04 · 21 · 23 · 31 + SB8**. Frozen V1 Science ticket: **01 · 02 · 18 · 34 · 35 + SB2** (SL10: D_trend mains, S_gap SB; seeded no-edge fallback). Result: **0/5, SB miss**.

## 1. Frozen record verification

- Ticket matches its frozen pool entry: True. Ledger hash of `prediction_1754.json`: LF_to_CRLF.
- Embedded hashes: {'LF_to_CRLF': 31, 'exact': 12, 'DIFFERS': 1}. The only mismatch is `scripts\research\super_jev.mjs`, the #1753 Jev caller; the #1754 call used `super_1754_jev.mjs`, which matches. Pre-Jev candidate freeze: {'LF_to_CRLF': 5, 'exact': 1}.
- Jev: a single HTTP attempt with retries disabled: True. Receipt state/response/request hashes match (request hashed as compact JSON).
- Chronology (UTC): unpublished check 2026-09-26T00:58:57 → pool frozen 2026-09-26T01:02:08 → unpublished check 2026-09-26T01:04:15 → Jev call 2026-09-26T01:04:15 → ticket frozen 2026-09-26T01:05:45 → draw 2026-09-26T01:30:00Z. Order valid: **True**. The Codex snapshot is a single commit, so there is no git chronology for #1754; ordering rests on the embedded UTC timestamps, the official-API unpublished checks at 00:58:57 and 01:04:15 UTC, and the hash chain.

## 2. Whole #1754 candidate pool

| ID | Mains | SB | Generators (main/SB) | Outcome | Matched | Jev Choice | Jev rank | Sensitivity rank range | Agreement |
|---|---|---|---|---|---|---|---|---|---|
| SL01 | 12 · 17 · 22 · 23 · 24 | 5 | A_long / S_long | 1/5 | 23 | 0.1 | 4 | 1–3 | 2 |
| SL02 | 09 · 11 · 12 · 17 · 24 | 5 | A_long / S_recent | 0/5 | — | 0.04 | 6–7 | 1–2 | 2 |
| SL03 | 03 · 06 · 12 · 17 · 24 | 2 | A_long / S_gap | 1/5 | 03 | 0 | 17–20 | 3–5 | 1 |
| SL04 | 01 · 05 · 11 · 12 · 18 | 3 | B_recent / S_trend | 0/5 | — | 0.11 | 3 | 1–2 | 2 |
| SL05 | 01 · 09 · 18 · 24 · 35 | 5 | B_recent / S_transition | 0/5 | — | 0.01 | 9–16 | 2–4 | 2 |
| SL06 | 01 · 12 · 18 · 23 · 25 | 2 | B_recent / S_ensemble | 1/5 | 23 | 0.24 | 2 | 1–3 | 3 |
| SL07 | 04 · 07 · 13 · 33 · 34 | 9 | C_gap / S_random | 1/5 | 04 | 0.07 | 5 | 1–1 | 1 |
| SL08 | 04 · 06 · 07 · 17 · 33 | 5 | C_gap / S_long | 1/5 | 04 | 0.01 | 9–16 | 2–2 | 1 |
| SL09 | 04 · 10 · 16 · 17 · 33 | 5 | C_gap / S_recent | 1/5 | 04 | 0.01 | 9–16 | 3–3 | 1 |
| SL10 | 01 · 02 · 18 · 34 · 35 | 2 | D_trend / S_gap | 0/5 | — | 0.01 | 9–16 | 2–4 | 1 |
| SL11 | 01 · 06 · 11 · 18 · 22 | 3 | D_trend / S_trend | 0/5 | — | 0.3 | 1 | 1–3 | 3 |
| SL12 | 01 · 22 · 32 · 34 · 35 | 5 | D_trend / S_transition | 0/5 | — | 0.01 | 9–16 | 2–8 | 1 |
| SL13 | 18 · 22 · 23 · 24 · 30 | 2 | E_pairs / S_ensemble | 1/5 | 23 | 0.02 | 8 | 13–13 | 1 |
| SL14 | 05 · 10 · 20 · 22 · 32 | 9 | E_pairs / S_random | 0/5 | — | 0.01 | 9–16 | 14–14 | 0 |
| SL15 | 03 · 08 · 12 · 20 · 32 | 5 | E_pairs / S_long | 1/5 | 03 | 0 | 17–20 | 15–15 | 0 |
| SL16 | 06 · 07 · 18 · 22 · 29 | 5 | F_structure / S_recent | 0/5 | — | 0 | 17–20 | 1–2 | 0 |
| SL17 | 06 · 07 · 18 · 25 · 28 | 2 | F_structure / S_gap | 0/5 | — | 0 | 17–20 | 1–2 | 0 |
| SL18 | 06 · 12 · 18 · 19 · 29 | 3 | F_structure / S_trend | 0/5 | — | 0.01 | 9–16 | 3–3 | 0 |
| SL19 | 10 · 11 · 16 · 21 · 22 | 5 | G_ensemble / S_transition | 1/5 | 21 | 0.01 | 9–16 | 10–19 | 0 |
| SL20 | 04 · 06 · 13 · 17 · 18 | 2 | H_random / S_ensemble | 1/5 | 04 | 0.04 | 6–7 | 13–20 | 1 |

Main matches: 0:10 · 1:10 · 2+:0. Best: 1/5 (SL01, SL03, SL06, SL07, SL08, SL09, SL13, SL15, SL19, SL20). V1 SL10: 0/5. Jev preferred **SL11** (Choice 0.3, confidence 0.25): 0/5. **Candidates with SB8: 0.** No candidate materially outperformed V1 (none reached 2/5). For reference, 20 *independent* random tickets would give P(any ≥2) = 0.95; the V1 pool is a correlated shortlist, so its all-≤1 result is a weak, single-draw signal of low diversity, not evidence of a flaw. Jev Choice vs matches: Spearman -0.11. No candidate is promoted retrospectively.

## 3. Exact pre-draw main-number evidence (cutoff #1753)

Rank [tie interval] from the frozen `complete_rankings.json`. E_pairs was flat (no Holm-retained pair) and the V1 G proxy was flat (the V1 learned main weights were A–D 0, E_pairs 1.0, F 0, and E_pairs was flat), so their orders are arbitrary; F_structure has no number-level ranking; H is a control.

| No. | Role | A_long | B_recent | C_gap | D_trend | H_random |
|---|---|---|---|---|---|---|
| 03 | winner | 16 [16–18] | 32 | 16 [16–19] | 32 [32–33] | 34 |
| 04 | winner | 7 [7–10] | 20 | 3 | 12 [12–15] | 26 |
| 21 | winner | 30 [29–31] | 30 | 14 [14–15] | 24 [22–27] | 28 |
| 23 | winner | 15 [11–15] | 9 | 19 [16–19] | 11 [10–11] | 11 |
| 31 | winner | 29 [29–31] | 19 | 20 [20–23] | 22 [22–27] | 6 |
| 01 | selected loser | 10 [7–10] | 3 | 34 [31–35] | 1 | 2 |
| 02 | selected loser | 8 [7–10] | 17 | 18 [16–19] | 4 [3–7] | 19 |
| 18 | selected loser | 12 [11–15] | 1 | 31 [31–35] | 2 | 3 |
| 34 | selected loser | 27 [26–28] | 23 | 4 | 9 [8–9] | 15 |
| 35 | selected loser | 32 [32–33] | 22 | 28 [27–30] | 3 [3–7] | 35 |

Winner coverage (point [tie range]); random expectation 5N/35.

| Model | Top 5 | Top 7 | Top 10 | Top 12 | Top 15 | Top 20 |
|---|---|---|---|---|---|---|
| A_long | 0 | 1 [0–1] | 1 | 1 [1–2] | 2 | 3 |
| B_recent | 0 | 0 | 1 | 1 | 1 | 3 |
| C_gap | 1 | 1 | 1 | 1 | 2 | 5 [4–5] |
| D_trend | 0 | 0 | 0 [0–1] | 2 [1–2] | 2 | 2 |
| H_random | 0 | 1 | 1 | 2 | 2 | 2 |
| random expectation | 0.71 | 1.00 | 1.43 | 1.71 | 2.14 | 2.86 |

No winner was in the Top 5 of A_long, B_recent or D_trend; the selected numbers 01, 18, 35, 02 were D_trend's ranks 1–4. C_gap held 04 at rank 3 and all five winners in its Top 20 (random 2.86), a single-draw observation.

## 4. Super Ball: SB8 (winner) vs SB2 (selected)

| SB model | Informative | Model pick | SB8 rank | SB2 rank |
|---|---|---|---|---|
| S_long | yes | 5 | 9 [8–9] | 8 [8–9] |
| S_recent | yes | 5 | 4 | 9 |
| S_gap | yes | 2 | 8 | 1 |
| S_trend | yes | 3 | 5 [4–6] | 10 |
| S_transition | flat | 5 | 8 [1–10] | 4 [1–10] |
| S_ensemble | yes | 2 | 8 | 1 |
| S_random | control | 9 | — | — |

SB2 was S_gap's and S_ensemble's first choice (it was the most overdue ball; the V1 SB ensemble weights were S_gap 0.35 and the flat S_transition 0.65, so the ensemble reduced to S_gap). SB8 ranked 4th under S_recent and 5th under S_trend, and no model ranked it first. **SB8 appeared in no frozen candidate** (pool SBs [2, 3, 5, 9]). In #1753 the pool carried SBs [2, 4, 5, 6] and omitted the winner SB3. **The SB coverage omission repeated.** It is structural: V1 assigns SBs cyclically from the seven SB models' single top picks, so a pool carries at most 7 and on average 4.4 distinct SBs. Historically the actual SB was in the pool at 46% of 121 targets, in line with that coverage (≈44%), so there is no SB skill beyond coverage.

## 5. Combined #1753 + #1754 diagnosis (descriptive; n = 2)

| | #1753 | #1754 |
|---|---|---|
| Frozen V1 | 01 · 22 · 32 · 34 · 35 + SB2 (SL10) | 01 · 02 · 18 · 34 · 35 + SB2 (SL10) |
| Actual | 01 · 05 · 08 · 14 · 18 + SB3 | 03 · 04 · 21 · 23 · 31 + SB8 |
| Result | 1/5, SB miss | 0/5, SB miss |
| Best candidate | 2/5 | 1/5 |
| Winners in the union of the 20 candidates | 4 of 5 (30 numbers) | 4 of 5 (30 numbers) |
| Winning SB in pool | no | no |

- **Main-number ranking quality:** in both draws the V1 selected numbers came from the top of D_trend/B_recent (recently frequent numbers), and the winners sat mostly mid-table. Historical capture is at random level (the #1753 forensic found all corrected coverage p = 1.0). There is no discovery signal to lose.
- **Candidate construction:** the 20 candidates span about 30.5 of the 35 numbers and contain 4.30 winners on average (random for that many numbers 4.36); the best candidate averages 2.06 matches. **Compression is not measurably losing information**: the shortlist holds winners at the rate its size implies, and it cannot hold more.
- **Repeated-number bias:** 01, 34, 35 and SB2 are in both frozen tickets because both are SL10 = D_trend's top ticket, and D_trend's top numbers move slowly.
- **Repeated SB behaviour:** S_gap picks the most overdue ball and keeps picking it until it is drawn. The V1 SB repeated on 89% of consecutive historical draws.
- **Fixed-seed effect (main driver of repetition):** V1 creates `default_rng(2026092109)` fresh each run, and with 20 candidates the index is always 9, so V1 **always** selects SL10 (D_trend top ticket + S_gap SB): 121 of 121 reconstructed cutoffs, 1 distinct candidate ID. Unlike Lotto there is no previous-ticket rule, so **every** fixed seed repeats the same slot 100% of the time; per-draw seeds would use 20 IDs. Realized results do not depend on it: production mean 0.636 main matches and 12 SB hits over 121 draws vs fixed-seed average 0.725 / 12.7 and per-draw 0.730 / 12.8 (random 0.714 / 12.1).
- **Jev behaviour:** diffuse and non-causal. #1754 Choice confidence 0.25, favourite SL11 at 0.30; Choice vs outcome Spearman −0.11 (#1753: +0.12). Under the no-edge rule Jev never affects the V1 ticket.

## 6. Is a Super Lotto V2 justified?

Causal V1 walk-forward through #1754 (128 origins; last 40 = confirmation), candidate refinements limited to existing V1 components:
- **Main and SB models as selectors:** none passes the V1 gate (lowest confirmation Holm p = 1.00).
- **V1 two-stage construction methods** (44 methods, Holm family): best raw result B_recent:pool15:uniform (mean 0.975, raw p 0.019), Holm p 0.83: fails correction.
- **Fallback seeding design:** changes which candidate is chosen, not expected matches (no gate possible).

**NO SUPER LOTTO V2 IS JUSTIFIED.** V1 is preserved unchanged.

## 7. Conclusion
- **Main-number issue:** winners were mid-ranked by every informative model. This is consistent with random-level historical discovery, not a new defect.
- **Candidate-construction issue:** a correlated shortlist that is persistent between draws (fixed 4,096-combination search pool). It covers winners at the rate its size implies.
- **Super Ball issue:** structural SB under-coverage (about 4.4 distinct SBs per pool, cyclic assignment), and the winning SB was absent in both #1753 and #1754. The final V1 SB is always S_gap's overdue pick.
- **Jev behaviour:** diffuse (confidence 0.25), unrelated to outcomes, no causal role.
- **Does #1754 justify changing V1? NO.**
