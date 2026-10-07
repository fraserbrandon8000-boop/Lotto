# M0 validation protocol

1. **Data.** `draw2343/draws.json` (#2161–#2342) plus #2343, asserted contiguous, with six unique mains in 1–38. Bonus dropped. Dataset sha256 recorded.
2. **Outer loop.** For t = 50…182 (#2211…#2343):
   - (a) slice history d[:t];
   - (b) run each model's inner tuning on d[:t] only;
   - (c) produce per-number probabilities and/or set scores;
   - (d) score all 2,760,681 combinations and freeze the scores (top-1000 list and primary ticket recorded);
   - (e) only then read d[t] and compute rank, matches and log-score.

   Code asserts that no function receives d[t:] before step (e).
3. **Leakage mutation test.** For three targets, replace d[t:] with random draws; the frozen scores at t must be bit-identical.
4. **Rank computation.**
   - rank = 1 + #(score > s*) + (#(score = s*) − 1)/2;
   - u = (rank − 0.5)/C;
   - Top-K hit = rank ≤ K.
5. **Statistics.**
   - Mean u with normal null SD 1/√(12n), plus the misaligned-permutation null.
   - Top-K counts vs Binomial(n, K/C).
   - Primary-ticket matches vs exact hypergeometric convolution.
   - Log-score mean with a t-test and a 5-block bootstrap CI.
   - Halves by chronological split.
   - Holm over the M0 family as in the charter.
6. **Overfit audit.** Every model is also fitted once on all draws < 182 and used to score its own training targets (in-sample percentile). It is flagged HISTORICAL FIT, NOT PREDICTION when in-sample mean u < 0.45 while out-of-sample mean u ≥ 0.5 − 1.96/√(12n). Each model also reports parameters, effective degrees of freedom and fixed-grid sensitivity.
7. **Selection and freeze.** Apply the charter's selection rule mechanically, write `protocol/`, commit, and only then run the frozen procedure on #2161–#2343 for #2344.
