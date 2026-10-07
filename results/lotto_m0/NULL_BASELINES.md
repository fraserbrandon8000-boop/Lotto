# Null baselines (exact)

- **Universe:** C = C(38,6) = 2,760,681. Under any ranking independent of the outcome, the realised ticket's rank is uniform on 1..C.
- **Expected rank:** (C+1)/2 = 1,380,341. Percentile u ~ U(0,1), so mean u = 0.5 with SD 0.2887/√n (n = 133 gives SD 0.0250).
- **Top-K hit probability:** K/C per target.

| K | P(hit) | Expected hits in 133 |
|---|---|---|
| 1 | 3.62e-7 | 4.8e-5 |
| 10 | 3.62e-6 | 4.8e-4 |
| 100 | 3.62e-5 | 0.0048 |
| 1,000 | 3.62e-4 | 0.048 |
| 10,000 | 0.00362 | 0.48 |
| 100,000 | 0.0362 | 4.82 |

- **Primary-ticket matches:** Hypergeometric(38,6,6), mean 36/38 = 0.947. P(≥3) = 0.0387, P(≥4) = 0.00276, P(5) = 6.95e-5, P(6) = 3.62e-7.
- **Best match within the top K tickets:** depends on how the K tickets overlap. The null is obtained by scoring the same frozen top-K list against the realised draws of other targets (misaligned null).
- **Exact log-score:** log P(S) + log C has mean ≤ 0 for any outcome-independent model (Gibbs). Uniform gives 0.
- **Number level:** mean winner rank 19.5; Top-N capture Hypergeometric(38,6,N).
