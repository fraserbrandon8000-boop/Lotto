# Lotto #2342 prospective experiment

Frozen before draw #2342 (Wednesday 2026-09-30, 8:25 PM Jamaica = 2026-10-01 01:25 UTC). Cutoff #2341; #2341 (01 04 06 22 33 38, bonus 34) was appended as one ordinary observation.

| Track | Ticket | Frozen (UTC) |
|---|---|---|
| **V1 Science** (C07, C_gap) | **05 · 11 · 16 · 24 · 27 · 34** | 2026-09-29T02:40:23 |
| **P0 Coverage 1** | **01 · 02 · 04 · 13 · 22 · 38** | 2026-09-29T02:40:45 |
| **P0 Coverage 2** | **08 · 09 · 10 · 12 · 14 · 18** | 2026-09-29T02:40:45 |
| Random control (research only) | 12 · 14 · 15 · 17 · 20 · 29 / 13 · 19 · 25 · 26 · 28 · 29 / 01 · 08 · 20 · 21 · 33 · 36 | 2026-09-29T02:41:16 |

## V1 Science track (unchanged V1)
- Parameterized wrapper `scripts/research/v1_prospective.py`, proven byte-identical to the frozen #2341 run on all 15 outputs.
- 20 candidates; 16 eligible under the ≤2-overlap rule against the previous V1 ticket 01·04·13·14·24·38. No V1 model passed the evidence gate.
- The pool was frozen and committed (`fd3b724`) before the single production Jev call (jev-latest → jev-1.13.0, 113 questions).
- Selection: **no-edge seeded fallback** (seed 20260919), index 3 of the 16 eligible candidates sorted by ID → **C07**. Validated V1 edge: **NO**.
- Jev Choice for C07: 0. Jev confidence: 0.68. Jev preferred C03 (0.71), which the V1 rule does not use.
- **This is the same ticket V1 selected for #2340.** The #2341 forensic predicted this mechanically: the fixed-seed fallback plus the previous-ticket overlap rule alternate between the same candidate slots (#2340 C07 → #2341 C04 → #2342 C07).

## P0 portfolio track (frozen protocol `72e1c075`)
- Frozen weights: B_recent 0.0314, D_trend 0.0238, struct 0.0067; all others 0. The weights were not updated with #2341.
- Discovery pool: Top **15** (predeclared no-edge default): 04 13 24 02 01 22 10 14 12 07 38 18 08 09 06.
- All **5,005** combinations were enumerated and scored (`p0/universe_scores.csv`, SHA-256 `19740fcf3708dd4b…`).

| Ticket | Raw T (rank of 5,005) | Incremental coverage | Contributions (B / D / struct) |
|---|---|---|---|
| 01 · 02 · 04 · 13 · 22 · 38 | +0.0889 (116) | 1.016 | +0.045 / +0.039 / +0.005 |
| 08 · 09 · 10 · 12 · 14 · 18 | -0.0878 (4952) | 0.985 | -0.041 / -0.035 / -0.012 |

- Pairwise overlap: 1–2 = 0, 1–3 = 0, 2–3 = 0. Unique numbers: **18**. The V1 ticket has only 24 inside the pool, so the challengers cover 12 of the other 14 pool numbers (07 and 06 are left out).
- Historical gate: **FAIL**. **The portfolio is a coverage experiment, not a demonstrated predictive edge.**
- Ticket 2 contains 01, 04, 13 and 38 because B_recent and D_trend carry the only positive (statistically null) weights. It contains 22 because #2341 raised its recent frequency as ordinary history. No number was favoured or avoided by hand.

## Jev evidence audit of the frozen portfolio (one call; cannot change tickets)
| Question | Ticket 1 (V1) | Ticket 2 | Ticket 3 |
|---|---|---|---|
| Robustness (0–4) | 0.06 | 0.59 | 0.20 |
| Chance/overfitting better explanation (Noul) | 0.95 | 0.92 | 0.94 |
| Depends on weak/unvalidated evidence | 0.97 | 0.95 | 0.96 |
| Model-family concentration | 0.95 | 0.91 | 0.90 |
| Fragile to reasonable changes | 0.35 | 0.22 | 0.50 |

Portfolio level: robustness 0.92/4; evidence of an edge over random 0.10; chance/overfitting 0.91; concentration 0.89; coverage quality 3.17/4. These are evidence judgments, not winning probabilities. The TypeSafe live docs were unreachable from this environment; the audit was built from the installed skill and the SDK 0.6.0 types.

## Research-only fragility check (computed; frozen tickets unchanged)
Ticket 2 is identical under pool sizes 12 and 20 and under shrinkage τ = 0.05 and 0.18; it changes (4 of 6 shared) only if every evidence weight is set to zero. Ticket 3 is identical under both τ variants and shares 4–5 numbers under the other pool sizes.
