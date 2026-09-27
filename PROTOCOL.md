# Jamaica Lotto experiment protocol

Frozen before calculating model performance or asking Jev. Seed: **20260919**.

## Data and target

Read the original workbook without changes. Merge only verified official additions, preserving provenance and rejecting conflicts. Main target is the six main balls in 1–38. Bonus is audited but is not a seventh main ball or a prediction feature. Sort chronologically. Reject incomplete sequences before serial/gap modelling. Latest available draw is the information cutoff; never use the upcoming draw.

The uniform reference is Hypergeometric(N=38,K=6,n=6), with expected matches 36/38. Every fixed six-number ticket has jackpot probability 1/C(38,6). A common-looking sum or parity does not make a specific ticket more likely.

## Models and time separation

Use an expanding training prefix, minimum 50 draws. Predictions are generated before reading the target row. A: smoothed full frequency. B: equal mixture of last-30 frequency and EW frequency with half-life 20. C: increasing current absence (explicit overdue hypothesis, not a fact). D: last-20 minus previous-40 frequency trend. E: positive pair relationships passing training-only Holm 0.05; otherwise a uniform random fallback. F: combination structure distance from training means and standard deviations. G: ensemble of A–F with weights learned only from earlier walk-forward predictions. H: uniform random control.

Each A–G optimizes over the same seeded pool of 512 uniformly drawn combinations at each origin; H is a separate uniform ticket. This is a bounded combination search, not exhaustive optimization. A–D maximize mean standardized number score, E mean retained pair lift, F minimizes standardized structure distance, G uses past-performance-weighted A–F objectives. If a score is constant, selection falls back to the first uniformly sampled combination. Ties use stable pool order.

Final 40 target draws are the confirmation period. G's weights are frozen at the first of those origins, using earlier out-of-sample matches, with 20 pseudo-draws at the random mean and positive excess-score weighting; absent positive scores it uses equal weights. Individual-model features continue updating causally. All historical testing is retrospective: this is a separated confirmation period, not a prospectively registered independent study.

Primary metric: mean main-ball matches. One-sided exact null p-values use repeated convolution of the hypergeometric distribution. Holm correction covers all eight model tests within each declared period. Bootstrap CIs are descriptive; use circular five-draw block bootstrap for the edge gate. Also report match distribution, all-number average precision and recall@12 for applicable models, chronological halves, and random-ticket Monte Carlo controls. Candidate variants, Jev, and the final selection rule have NOT themselves been walk-forward validated; do not transfer a generator's performance to a particular ticket.

Exploratory sensitivity: recent windows 20/40, decay half-lives 10/40, trend window 10/30, pair threshold 0.01/0.10, training minimum 40/60, training history cap 100, ensemble uniform/more-shrunk weights, original-only source ablation, and alternate candidate-pool seed. These are stability checks, never options to cherry-pick. Do not use them to change baseline model definitions.

## Multiple testing and randomness

Use 10,000 synthetic uniform histories of the same length for global marginal, pair, serial, gap and structural diagnostics. Calibrate the actual six-without-replacement process; do not pretend all six balls are independent multinomial observations. Holm-adjust global tests. Report two-sided exact marginal binomial tests for 38 numbers, Holm and BH-adjusted positive pair tests for 703 pairs, and Holm-adjusted conditional transition enrichment tests for 1,444 ordered relationships. Triple counts are descriptive when expected counts are sparse; no triple model.

## Edge gate and final decision rule

A methodology qualifies only if its confirmation-period Holm p < 0.05, block-bootstrap 95% lower bound > 36/38, and both confirmation halves exceed the random mean. A statistically unusual history alone does not pass this gate. Robustness across sensitivity runs must also be reported; unstable positives remain suggestive.

Generate 20 candidates from A–H with maximum overlap of three numbers between any two. Store all computed evidence, ranks, methodology support and sensitivity before Jev runs. Three per A–F, one G, one H, with shortages filled by H. Their variants are exploratory.

Use `jev-latest` for one Choice across all candidates and per-candidate Scores (robustness, independent consensus, evidence quality) plus Nouls (overfitting explanation, assumption stability, stronger-than-random evidence, single-model dependence). Questions share one state where token limits permit. Code supplies statistics; Jev judges the supplied evidence. Its probabilities describe its judgments, NEVER lottery-winning probabilities. Noul causal overfitting judgments are heuristic, not a statistical probability estimate established by the data.

If no methodology passes the gate, all tickets have equal established expected return. Choose primary with seeded uniform selection among the 20, then secondary among minimum-overlap candidates using the same seed. Still display Jev judgments and hypothetical composite ranks, but do not allow them to invent a predictive edge.

If a methodology passes, eligible candidates must have support from it. Rank by: 35% normalized validated method advantage, 20% computed perturbation stability, 10% ensemble rank, 10% Jev robustness/4, 5% Jev consensus/4, 10% Jev evidence quality/4, 10% Jev Choice probability; subtract 10% Jev overfitting Noul and 5% single-model Noul. Require stronger-than-random Noul >=0.5 and stability Noul >=0.5; if none pass revert to diversification and report why. Secondary minimizes overlap among the five highest remaining eligible composite scores. Tie-break by candidate ID. These decision weights express policy, not fitted predictive coefficients.

If no edge passes, conclusion: **No detectable edge in this dataset**, unless corrected or consistently positive sensitivity evidence warrants **Some suggestive evidence, but not enough to establish an edge**. Never claim predictive validation for Jev without future recorded outcomes.
