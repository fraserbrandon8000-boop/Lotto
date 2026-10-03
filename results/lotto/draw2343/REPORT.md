# Lotto #2343 prospective experiment

**Draw:** #2343, Saturday 2026-10-03, 8:25 PM Jamaica (2026-10-04 01:25 UTC).

**Cutoff:** #2342. The #2342 result (12 13 14 15 19 33, bonus 21) was appended as one ordinary observation. Nothing was favoured or suppressed, no repeat rule was added and no weight was changed.

**Publication check:** #2343 could not have been published. Every ticket was frozen about 18.7 h before the scheduled draw, and the system clock was checked first (2026-10-03T06:44Z). No #2343 result or prediction from any other system was looked up.

| Track | Ticket | Frozen (UTC) | Commit |
|---|---|---|---|
| **V1 Science** (C04, B_recent) | **01 · 04 · 13 · 14 · 24 · 38** | 2026-10-03T06:45:14 | fb9a473 |
| **P0 Coverage 1** | **02 · 06 · 07 · 08 · 12 · 22** | 2026-10-03T06:45:48 | d83d77b |
| **P0 Coverage 2** | **04 · 09 · 10 · 13 · 18 · 33** | 2026-10-03T06:45:48 | d83d77b |
| Random control (research only) | 12 · 14 · 15 · 17 · 20 · 29 / 13 · 19 · 25 · 26 · 28 · 29 / 01 · 08 · 20 · 21 · 33 · 36 | 2026-10-03T06:47:45 | 91557a7 |

The candidate pool was committed before Jev in 9c6b80c (06:44:55). The P0 Jev audit is aea1ae6. The Jev replicates are in the commit that adds this report.

Freeze record:
- **Dataset** `draw2343/draws.json`: sha256 `1a604b3c…fafb8`, 182 draws (2161–2342).
- **V1 pool** `pool_frozen_pre_jev.json`: sha256 `478ae68b…40f5c`.
- **P0 state** `p0/p0_frozen.json`: sha256 `ea30565e…9da3`.
- **Production Jev receipt** 2026-10-03T06:45:04.724Z: jev-1.13.0, 113 questions, request sha256 `47fa82f3…d9bf`.

## V1 Science track (unchanged V1)
- **Generation.** V1 code is unchanged since snapshot ba7c5a3. It produced 20 candidates, 16 of them eligible under the ≤2-overlap rule against the previous V1 ticket 05·11·16·24·27·34. No V1 model passed the evidence gate.
- **Jev.** One production Jev call (jev-latest → jev-1.13.0). The first valid response was preserved.
- **Selection.** No-edge seeded fallback (seed 20260919): index 3 of the 16 eligible candidates sorted by ID gives **C04**. **Validated V1 edge: NO.**
- **Jev scores.** Jev Choice for C04 was 0.86, with confidence 0.84. Jev also preferred C04, but the V1 rule does not use Jev under no-edge.
- **Repeat ticket.** This is the third time V1 has selected this ticket (#2339, #2341, #2343). The fixed-seed fallback plus the ≤2-overlap rule alternate between the same two tickets, as the #2341 and #2342 forensics predicted.
  - The #2342 forensic also tested a per-draw seed, a rotating index, no repeated position and dropping fixed candidates. None passes the corrected gate, so V1 stays unchanged.

## P0 portfolio track (frozen protocol 72e1c075, unchanged)
- **Weights.** Frozen at B_recent 0.0314, D_trend 0.0238, struct 0.0067; all others 0. No refinement passed the corrected gate (`forensic_2342/research_challengers.json`).
- **Discovery pool.** Top **15**: 13 04 12 14 24 02 01 22 07 18 10 06 08 09 33.
- **Universe.** All **5,005** combinations were enumerated and scored (`p0/universe_scores.csv`, sha256 `fa105dd1…5ebb`).

| Ticket | Raw T (rank of 5,005) | Incremental coverage | Contributions (B / D / struct) |
|---|---|---|---|
| 02 · 06 · 07 · 08 · 12 · 22 | −0.0407 (4084) | 0.993 | −0.033 / −0.005 / −0.002 |
| 04 · 09 · 10 · 13 · 18 · 33 | +0.0115 (1957) | 0.651 | −0.003 / +0.008 / +0.006 |

- **Overlap and coverage.** Pairwise overlap is 1–2 = 0, 1–3 = 2 (04, 13) and 2–3 = 0. There are **16** unique numbers, and all 15 pool numbers are covered.
- **Why the challengers have low T.** The V1 ticket already holds five of the top pool numbers (01 04 13 14 24). The coverage term therefore fills the rest of the pool, and the challengers have low evidence scores T.
- **Historical gate: FAIL.** The portfolio is a coverage experiment, not a demonstrated predictive edge.

## Jev evidence audit of the frozen portfolio (one call after the freeze; cannot change tickets)
| Question | Ticket 1 (V1) | Ticket 2 | Ticket 3 |
|---|---|---|---|
| Robustness (0–4) | 0.13 | 0.19 | 0.48 |
| Chance/overfitting is the better explanation (Noul) | 0.95 | 0.94 | 0.93 |
| Depends on weak/unvalidated evidence | 0.98 | 0.96 | 0.95 |
| Model-family concentration | 0.95 | 0.82 | 0.87 |
| Fragile to reasonable changes | 0.33 | 0.50 | 0.63 |

Portfolio-level judgments:
- robustness 0.69 / 4
- evidence of an edge over random 0.10
- chance/overfitting 0.92
- concentration 0.85
- coverage quality 2.82 / 4

These are evidence judgments, not winning probabilities.

## Research-only fragility check (computed; frozen tickets unchanged)
- **Shrinkage.** Both challenger tickets are identical under τ = 0.05 and τ = 0.18.
- **Pool size.** Under K = 12 and K = 20, ticket 2 shares 5 numbers with the frozen ticket and ticket 3 shares 3.
- **All evidence weights zero.** Each challenger shares 3 numbers with the frozen ticket.

## Random control
- **Generation.** Seed 20260930 and the method are the fixed P0 random-control settings, unchanged from #2342. The generator reads no data, so it reproduces the #2342 control tickets exactly. Those tickets were first generated on 2026-09-29, before #2342 was drawn.
- **Status.** It is a comparison baseline only.
