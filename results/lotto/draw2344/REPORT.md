# Lotto #2344 prospective experiment (Wednesday 2026-10-07, 8:25 PM Jamaica = 2026-10-08T01:25Z)

**Order of work:**
1. Audit `83f3ed1` (15:21:55Z).
2. Protocol 2344 `d4e5886` (15:34:46Z) and transport Addendum 1 `84e2226` (15:36:13Z).
3. V1 pool frozen before Jev `87552f6` (15:35:27Z).
4. One production Jev call (15:36:21Z).
5. **All three tickets frozen `f248e15` (15:37:10Z, 10:37 Jamaica), about 9 h 48 min before the draw.**

The pre-draw check found #2344 unpublished: clock check; the official service is unreachable from this environment; a web search found no result. No other #2344 prediction was inspected.

| Ticket | Track | Numbers | Method |
|---|---|---|---|
| 1 | V1 SCIENCE | **16 · 21 · 26 · 32 · 34 · 36** | Unchanged V1. No model qualifies, so the seeded no-edge fallback applies (index 4 of 17 eligible candidates sorted by ID). Candidate C08, generator C_gap (null selection, not evidence). |
| 2 | ALIGNED COVERAGE | **04 · 07 · 12 · 13 · 24 · 33** | Rank 1 of all 2,760,681 combinations under the frozen P0 score; disjoint from ticket 1. |
| 3 | ALIGNED COVERAGE | **01 · 02 · 14 · 18 · 22 · 31** | Highest-ranked combination disjoint from tickets 1–2 (full-universe rank 66,269). |

Pairwise overlap 0 / 0 / 0; 18 unique numbers.

**Primary objective:** P(at least one 6/6) = 3/2,760,681 = 1.0867e-6 (1 in 920,227). That is the maximum attainable with three tickets and no validated edge, and every distinct 3-ticket portfolio shares it.

**Secondary tiers (exact enumeration):** best-ticket pmf for this portfolio:
- P(≥3) = 0.1157
- P(≥4) = 0.00829
- P(≥5) = 2.10e-4

These are the maxima over 3-ticket overlap structures (the two P0 Coverage tickets of #2343 gave P(≥3) = 0.1123).

**Evidence:** the system has **no evidence** that these exact tickets exceed the no-edge baseline. The score that ranked ticket 2 first is an unvalidated tie-break.
- Ticket 2 contains 04, 07, 13 and 33 (four #2343 winners) because the frozen weights (2026-09-29) score only recent frequency and trend (B_recent 0.031, D_trend 0.024), and #2343 raised those numbers.
- No rule refers to #2343. The protocol forbids substitution.

## V1 / Jev
- Production Jev (jev-latest → jev-1.13.0): 120 questions; first response valid under the unchanged V1 checks; preserved (response sha256 `720fb121…`).
- Jev favourite: C02 (0.93, confidence 0.93). Choice for the selected C08: 0.00. Under the no-edge rule Jev has no role in selection.

## Post-freeze research (cannot change tickets)
- **Jev stability:** 5 replicates of the byte-identical request; C02 in 5/5; mean Spearman 0.998; confidence 0.89–0.94. One extra research call was lost: the inherited stability script asserted answer-key order before saving. It was replaced by a save-first copy and is documented in `jev_stability_2344/replicates_receipt.json`.
- **Order / blinded-ID test** (3 Choice-only calls): C02 under the original order (0.91), reversed order (0.92) and shuffled blinded IDs without generator labels (0.96). Jev's preference follows evidence content, not position, ID or label.
- **Random controls:**
  - fixed (seed 20260930, unchanged): 12 14 15 17 20 29 / 13 19 25 26 28 29 / 01 08 20 21 33 36;
  - per-draw, matched to zero overlap (seed 20263274): 10 18 21 29 32 36 / 02 03 14 15 26 35 / 06 08 11 16 19 24.
- **P1 shadows (not playable):**
  - concentration 04 07 12 13 24 33 / 02 04 12 13 24 33 / 01 04 12 13 24 33;
  - V1 per-draw seed C01 01 08 15 18 24 25;
  - legacy P0 Coverage (frozen 72e1c075): 01 04 07 12 13 24 / 02 06 14 22 23 33.
