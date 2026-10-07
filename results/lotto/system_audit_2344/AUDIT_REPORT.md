# Lotto system audit before #2344

**Scope:** the full Jamaica Lotto V1 + P0 system (branch `claude/lotto-2344-audit`, base `670a300`). Lotto data only. History #2161–#2343, with #2343 added as one ordinary observation. No #2344 work was started before this audit was committed.

## Headline
1. **The jackpot objective cannot currently be improved by construction.**
   - For distinct tickets, P(≥1 jackpot) = Σ P(ticket). No model assigns realised combinations more probability than uniform (A9), so every 3-distinct-ticket portfolio has **exactly 3/C(38,6) = 1/920,227**.
   - Coverage, overlap and number spread change only the lower tiers. Expected total matches is the same for every portfolio (A2).
2. **The current P0 objective and reporting are misaligned with 6/6.**
   - P0 maximises pool coverage, and the coverage term outweighs the evidence score 3.5:1.
   - Reports used union coverage and total matches as success measures.
   - Under no edge this does not hurt 6/6, but it optimises the wrong quantity. The Top-15 hard cut also forces overlap with V1, which reduces the secondary tiers.
3. **No predictive edge.**
   - No number ordering beats random (A6; smallest Holm p 1.0).
   - No construction strategy beats its exact null (A3).
   - No combination model beats uniform (A9).
4. **The validation evidence is compromised for any future historical promotion.**
   - 385 formal tests across 10 studies, with Holm applied per batch only.
   - The last ~45 draws were used as "confirmation" up to 7 times.
   - Only prospective draws can validate from now on.
5. **No implementation bug or leakage was found.**
   - The frozen live tickets reproduce exactly.
   - Future-mutation tests pass.
   - The data are clean.

## #2343 forensic (A22)

Integrity: all checks pass (`forensic_2343/verification.json`: True).
- The pool was frozen 2026-10-03T06:44:55Z and the tickets at 06:45:21 / 06:45:48.
- The draw was at 2026-10-04T01:25Z; the replicates ran after the freeze.

| Winner | A_long | B_recent | C_gap | D_trend | E_pairs (flat) | G proxy | H | P0 rank | in frozen Top-15? |
|---|---|---|---|---|---|---|---|---|---|
| 04 | 7 | 3 | 28 | 1 | 13 [1–38] | 2 | 34 | **2** | yes |
| 07 | 23 | 19 | 18 | 5 | 36 [1–38] | 16 | 26 | **9** | yes |
| 13 | 9 | 1 | 37 | 2 | 31 [1–38] | 1 | 31 | **1** | yes |
| 23 | 35 | 15 | 23 | 22 | 24 [1–38] | 24 | 6 | **19** | no |
| 33 | 4 | 18 | 38 | 12 | 35 [1–38] | 9 | 28 | **15** | yes |
| 35 | 11 | 20 | 9 | 33 | 12 [1–38] | 20 | 3 | **24** | no |

- **Frozen pool (from `p0_result.json`, not inferred):** 13 04 12 14 24 02 01 22 07 18 10 06 08 09 33.
  - Inside: 04 (rank 2), 07 (9), 13 (1), 33 (15).
  - Outside: 23 (19), 35 (24).
  - Capturing 4 is better than typical: P(≥4 | random Top-15) = 0.15.
- **23:** best support B_recent 15, worst A_long 35. It enters a Top-20 pool but not a Top-18. **35:** best support C_gap 9, worst D_trend 33. It enters only a Top-25 pool.
  - Neither was suppressed by shrinkage. Equal weighting would rank them 30 and 17, so equal weights would admit neither into a Top-15 either.
  - Their exclusion reflects which families carry weight (B and D only). No family has validated skill, so this is neither "genuine evidence" nor an arbitrary error: it is noise.
- **Two layers:** discovery loss 2 (23, 35); construction loss 0 (all four available winners are on some ticket).
- **The four available winners were not concentrated.**
  - Only 55 pool tickets hold all four (exactly the random count); the best ranks 159th of 5,005.
  - Every pre-draw objective (standalone, concentration, hybrid) puts the top-ranked numbers together instead.
  - V1 already held 04 and 13, and the coverage term pushed the challengers elsewhere.
  - **Objective-alignment finding:** concentration would not have helped without knowledge of the winners. The real misalignment is in what the system claims and measures, and in forcing overlap.
- **Pool scoring:** V1 C04 scored 2/6 (it also carries bonus 38, which is not counted). The best candidates were C17 and C19 with 3/6. Jev's favourite was C04 (2/6). Distribution: {'0': 6, '1': 4, '2': 8, '3': 2, '4': 0, '5': 0, '6': 0}. No candidate reached ≥4.

## Documents
- OBJECTIVE_AUDIT.md: A2, A3, A4, A5, A9 and the rational policy.
- METRIC_AUDIT.md
- STATISTICAL_AUDIT.md: A6, A7, A8, A11, A14, A15, A16, A18, A21.
- DATA_AUDIT.md
- CODE_AUDIT.md: A10, A20.
- JEV_AUDIT.md
- REQUIREMENT_MATRIX.md
- AUDIT_FINDINGS.json
- RESEARCH_REGISTRY.json
- `data/` (all computations)
- Scripts: `scripts/research/audit_2344_*.py` and `forensic_2343.py`.
