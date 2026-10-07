# Jev audit (A19)

Saved calls only: 5 production calls (#2339–#2343) and 10 research replicates (#2342, #2343). No new historical calls. The live TypeSafe docs were unreachable (egress blocked). Semantics are taken from the installed SDK 0.6.0 and the documented project usage: Choice returns a preference distribution and a confidence, not winning probabilities.

| Draw | options | favourite (P) | confidence | Spearman Choice~matches | Spearman Choice~ensemble rank | Spearman Choice~model agreement | Spearman Choice~ID position | favourite matches | mean option matches | Choice mass by generator |
|---|---|---|---|---|---|---|---|---|---|---|
| 2339 | 20 | C02 (0.90) | 0.89 | +0.14 | +0.31 | +0.21 | +0.05 | 1 | 1.20 | A_long 0.92, D_trend 0.05, E_pairs 0.03 |
| 2340 | 16 | C02 (0.89) | 0.88 | +0.06 | +0.22 | +0.48 | +0.57 | 1 | 1.19 | A_long 0.92, D_trend 0.07, E_pairs 0.01 |
| 2341 | 16 | C04 (0.92) | 0.90 | +0.18 | +0.49 | +0.38 | +0.28 | 3 | 1.38 | A_long 0.06, B_recent 0.92, E_pairs 0.01, G_ensemble 0.01 |
| 2342 | 16 | C03 (0.71) | 0.68 | +0.26 | +0.51 | +0.33 | +0.08 | 2 | 0.94 | A_long 0.86, D_trend 0.13, E_pairs 0.01 |
| 2343 | 16 | C04 (0.86) | 0.84 | +0.09 | +0.27 | +0.25 | +0.00 | 2 | 1.44 | A_long 0.11, B_recent 0.86, D_trend 0.01, E_pairs 0.01, G_ensemble 0.01 |

1. **Does Choice correlate with realised matches?** Pooled Spearman +0.18 over 84 options (5 draws, ties, repeated tickets). The favourite averaged 1.8 matches vs 1.23 for all options. With n = 5 draws, two of which are the same ticket (C04 = 01 04 13 14 24 38), this is not evidence of skill.
2. **Is top-1 stable?** Replicates: #2342 5/5 (Spearman 0.997); #2343 5/5 (Spearman 0.994). Stable when one option dominates.
3. **Candidate order / IDs.** Untested so far. The Choice~ID-position correlation is small except at #2340 (+0.57). A post-freeze order-permutation and blinded-ID test runs for #2344 (research only).
4. **Generator labels / presentation.** Choice mass concentrates on A_long (2339, 2340, 2342) or B_recent (2341, 2343) candidates, the families with the strongest-looking frequency evidence. This is consistent with Jev reading the presented evidence (Choice tracks ensemble rank and agreement, Spearman +0.2 to +0.5).
5. **First-valid vs aggregated.** Identical favourite in all 12 saved calls for #2342/#2343. Historical aggregation testing is not feasible (~550 calls).
6. **Signal beyond the candidate evidence?** **Not demonstrated.** The underlying evidence has no predictive value (A6, A9), and Jev's preferences follow that evidence.

**Production role:** under the no-edge rule Jev never changes the V1 ticket. Its single V1 call is kept unchanged for protocol continuity (it would matter only if a model passed the V1 gate). **Jev contributes no measurable predictive value.**
