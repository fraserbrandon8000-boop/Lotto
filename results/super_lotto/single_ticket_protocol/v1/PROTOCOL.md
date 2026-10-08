# Super Lotto single-ticket protocol — version 1

Effective from Super Lotto #1758 (Friday 2026-10-09). Committed before any #1758 prediction exists. It does not change or overwrite any earlier prospective record (`results/super_lotto/prospective/ledger.jsonl` stays append-only).

## 1. Spending rule
- **Exactly ONE purchased ticket per Super Lotto draw** (Tuesday and Friday). Lotto (Wednesday and Saturday) is governed separately. Total across both games: four tickets a week.
- The single ticket carries the label **OFFICIAL PURCHASE TICKET**. Every other prediction is labelled **SHADOW — DO NOT PURCHASE**.
- **No extra purchases**: not after disappointing results, not because tracks disagree, not because a shadow "looks better".
- Under a fair draw one ticket wins the jackpot with probability 1/3,246,320. No current model (V1, P0, Jev or any selector) has validated evidence of improving that.

## 2. Incumbent primary track
**V1 Science**, unchanged (candidate pool frozen before Jev, exactly one production Jev call, frozen V1 selection rule). It is the incumbent **for continuity only**, not because it has shown better predictive performance.

The purchase designation is fixed before any candidate is generated. It may **not** switch because:
- another track's numbers look better;
- a Super Ball seems "overdue";
- a track matched more recently;
- Jev prefers another candidate;
- the V1 ticket repeats.

## 3. Shadow tracks (research only, never purchased)
- **P0 Coverage 1 and P0 Coverage 2**: unchanged frozen P0 protocol `5cce8a37` (built around V1 as a three-ticket portfolio).
- **S1 P0_standalone_top**: the best standalone ticket of the frozen P0 Top-12 universe, with the first P0 Super Ball (`scripts/research/super_single_shadows.py`).
- **S2 V1_pool_per_draw_seed**: the V1 candidate at index `default_rng(2026092109 + target)`. This tests the fixed-slot exploration issue.
- **Random controls**: the fixed-seed control (unchanged) is kept.

## 4. Freeze order (every draw)
1. Pre-draw check.
2. Append the previous result as one ordinary observation.
3. Run V1; freeze its candidate pool.
4. One Jev call.
5. Apply the V1 rule.
6. **Freeze the OFFICIAL PURCHASE TICKET.**
7. Generate the P0 shadows.
8. Generate the S1/S2 shadows.
9. Commit before any post-freeze research (Jev stability, P0 audit, random control).

No re-runs, substitutions or beautification. Post-freeze research cannot change any ticket.

## 5. Promotion of a challenger (replacing the incumbent)
A challenger can replace V1 as the purchase track only if **all** of these hold:
1. Its exact procedure was committed in a protocol version **before** the prospective draws used as evidence.
2. It has **at least 50 prospective draws** as a frozen shadow under this protocol. Historical replays are **exploratory only**: the history has been reused as "confirmation" many times.
3. A pre-registered one-sided test on those prospective draws passes at α = 0.05 / (number of live challengers). The test is either mean main matches vs the hypergeometric null 5/7, or SB hits vs 0.1, using exact tests.
4. Its prospective paired difference against the incumbent has a 95% lower bound > 0.
5. It still passes after excluding its single best draw.

A few recent good draws never qualify. A promotion is written as a new protocol version (v2, …), committed before the first draw it applies to, and records the evidence. The old version stays on file.

## 6. Logging and evaluation
- **ACTUAL FINANCIAL RESULTS** (purchased ticket only): `results/super_lotto/single_ticket_protocol/purchase_ledger.jsonl`.
  - Per draw: ticket, main matches, SB hit, jackpot (5+SB), prize amount (as reported by the user / official prize table), ticket cost, cumulative spend, cumulative winnings, net return.
  - Cost defaults to J$300 per play (full-jackpot ticket, from 2023–2024 public reports, **unverified for 2026**). The actual amount paid replaces it when supplied.
- **HYPOTHETICAL RESEARCH RESULTS** (all shadows): `results/super_lotto/prospective/ledger.jsonl`.
  - Per draw: counterfactual main matches and SB hits, compared with the purchased ticket, cumulative prospective performance and the exact random baseline.
  - **Shadow results are never counted as winnings or losses.**
- **Exact baselines:** main matches Hypergeometric(35, 5, 5) (mean 0.714); SB hit 0.1; jackpot 1/3,246,320; P(main ≥3) = 0.0258.
