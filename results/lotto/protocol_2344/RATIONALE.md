# Rationale

1. **Jackpot mathematics (exact).** Distinct tickets are disjoint events, so P(≥1 6/6) = Σ P(ticket). Without a calibrated combination model every term is 1/C(38,6) (audit A2, verified by full enumeration). No construction can raise P(6/6) above 3/2,760,681 with the present evidence.
2. **There is no calibrated combination model.** The conditional-Bernoulli log-score of the realised combinations vs uniform is ≤ 0 for every score with causal fitting (A9). Number orderings do not beat random (A6). Construction strategies do not beat their exact nulls (A3).
3. **Therefore the rational policy is policy A/B** (`system_audit_2344/OBJECTIVE_AUDIT.md`):
   - keep P(6/6) at its maximum (three distinct tickets);
   - then maximise the secondary tiers exactly. Pairwise-disjoint tickets do this: they give the highest P(4+), P(3+) and E[best], and P(5+) stays at its maximum (A2).
   - Use the unvalidated evidence score only to choose among disjoint tickets. That costs nothing if it is noise and keeps a prospective test of it alive.
4. **Why not concentration?** It is the jackpot-rational choice only under a calibrated signal (policy C). Without one, it lowers every secondary tier and leaves P(6/6) unchanged. It is tracked as a P1 SHADOW.
5. **Why the full universe?** The Top-15 cut never held the single best-scoring ticket back (A7). But when ticket 1 occupies pool numbers it makes disjoint tickets impossible, forcing overlap (#2343: V1 held 5 of 15 pool numbers). Full scoring takes about 9 s.
6. **Why keep V1 unchanged?** Its ticket has the same jackpot probability as any other. Changing its fallback has no predictive basis (A11) and would break the clean prospective record.
7. **Why this is not hindsight.**
   - No rule refers to #2343's numbers or to the #2342/#2343 split.
   - The argument is pure combinatorics.
   - The only data-derived quantities are the P0 weights frozen on 2026-09-29.
   - Historical replay (113 causal origins) shows the corrected constructor at its exact null (no claimed skill), with overlap 0 everywhere.
