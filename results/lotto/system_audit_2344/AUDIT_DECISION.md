# Audit decision (Phase B)

Audit commit: `83f3ed1adbe9b7a3ba14664e13805e8c0f8de052` (2026-10-07T15:21:55Z). All Phase A artifacts were committed before any production change.

## Classification: **F. MULTIPLE ISSUES**

| Class | Applies? | Basis |
|---|---|---|
| A. Sound as-is | No | — |
| B. Sound but research-limited | **Yes** | No predictive edge anywhere (A6, A3, A9). The data cannot validate a 6/6 rate (A13 power). |
| C. Objective misaligned | **Yes** | P0 optimises pool coverage; metrics used union coverage and total matches; the Top-15 cut forces overlap with ticket 1 (A2, A7, A8, A17). |
| D. Statistically compromised | **Yes (validation hierarchy)** | Confirmation windows reused up to 7×; 385 cumulative tests with batch-only correction (A15, A16). Nothing false was promoted because every gate failed. |
| E. Implementation bug exists | **No** | Exact reproduction of live and historical tickets; leakage mutation passes; data clean (A13, A14, A20). |

## Corrections and their classes

| # | Correction | Class | Applied before #2344? | Why |
|---|---|---|---|---|
| K1 | State the primary objective P(≥1 6/6) = Σ P(ticket) and reclassify metrics (PRIMARY / SECONDARY / DIAGNOSTIC / MISLEADING) | 3. OBJECTIVE-ALIGNMENT | **Yes** | Exact mathematics (A2); independent of any draw. |
| K2 | Tickets 2–3: replace the coverage-of-Top-15 constructor with the **ALIGNED COVERAGE** constructor: full 2,760,681-ticket universe, ticket 2 and 3 pairwise **disjoint** from each other and from ticket 1, ranked by the unchanged frozen P0 evidence score (tie-break only) | 3. OBJECTIVE-ALIGNMENT | **Yes** | Under no edge P(6/6) is fixed at 3/C(38,6). Disjointness exactly maximises P(4+), P(3+) and E[best] and keeps P(5+) maximal (A2 enumeration). Removes the forced overlap caused by the Top-15 cut (A7). No fitted parameter; weights are the P0 constants frozen 2026-09-29, before #2341/#2342/#2343. |
| K3 | Z-normalise score components over the full universe (not within a K-dependent pool) | 1. CORRECTNESS (design) | **Yes** (part of K2) | Removes K-dependence of the relative component scales (A8). |
| K4 | One parameterised entry point with hashed inputs (`protocol_2344.py`) instead of another draw-specific wrapper | 2. REPRODUCIBILITY | **Yes** | A20; deterministic, verified twice. |
| K5 | Validation hierarchy: prospective-only promotion, cumulative registry, fixed α budget | 5. RESEARCH-ONLY | Policy adopted | A15/A16. |
| K6 | Combination-level skill metric (conditional-Bernoulli log-score) recorded for every future draw | 5. RESEARCH-ONLY | Yes (reporting) | A9; the only metric aligned with exact-ticket probability. |
| K7 | Per-draw random control and exact null pmfs alongside the fixed control | 5. RESEARCH-ONLY | Yes (research) | A18. |
| N1 | V1 per-draw seed / rotation (exploration) | 5. RESEARCH-ONLY | **No**, P1 SHADOW | No predictive gain (A11, Holm 1.0). Changing V1 would break the prospective V1 record for an exploration-only benefit. |
| N2 | Jackpot concentration (top-3 combinations) | 4. PREDICTIVE REFINEMENT | **No**, P1 SHADOW | Rational only under a calibrated signal (policy C). A9 shows none, and concentration lowers every secondary tier (A2). |
| N3 | Wider pools / dynamic K / alternative shrinkage or weighting / best-trailing / Bayesian / voting | 4. PREDICTIVE REFINEMENT | **No** | None beats random (A6; Holm 1.0). |
| N4 | Jev aggregation / Jev changes | 4. PREDICTIVE REFINEMENT | **No** | Not testable; no measurable signal (A19). |
| N5 | V1 source-pool expansion, per-draw H control, cluster-neutral structure | 5. RESEARCH-ONLY | **No** | Search-space only (A10); no structure effect (A12). |

**No predictive correction is promoted. Nothing was chosen because of #2343.** K2 does not change the evidence weights, the number ordering or any parameter. It changes only the construction objective, as the user's stated goal requires mathematically.

## Production architecture for #2344 (decided before ticket generation)
1. **TICKET 1 — V1 SCIENCE.** V1 unchanged, including its single production Jev call and the no-edge seeded fallback with the ≤2-overlap rule. It is kept for continuity of the clean prospective V1 record; under no edge it has the same jackpot probability as any other distinct ticket.
2. **TICKETS 2–3 — ALIGNED COVERAGE** (Protocol 2344, replacing P0 Coverage 1/2). This is the P0 evidence score scored over the full universe with the disjointness objective.
3. **Not playable (research):**
   - P1 SHADOW concentration;
   - P1 SHADOW V1 per-draw seed;
   - the legacy P0 Coverage portfolio (frozen protocol 72e1c075) recomputed as a continuity SHADOW;
   - the fixed random control (seed 20260930) and a per-draw random control;
   - Jev stability (5 identical calls), order-permutation and blinded-ID calls.

## Validated predictive edge: **NO.**
