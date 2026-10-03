# Jev stability study (#2343 V1 production request; research only)

Five replicates of the **byte-identical** production request were run **after** every #2343 ticket was frozen. The request bytes were verified by SHA-256 against the production receipt. The replicates changed nothing.

| Run | Top Choice | P(top) | Confidence | Entropy (bits) |
|---|---|---|---|---|
| production | C04 | 0.86 | 0.84 | 0.812 |
| replicate_1 | C04 | 0.85 | 0.83 | 0.863 |
| replicate_2 | C04 | 0.85 | 0.83 | 0.888 |
| replicate_3 | C04 | 0.87 | 0.85 | 0.802 |
| replicate_4 | C04 | 0.87 | 0.85 | 0.794 |
| replicate_5 | C04 | 0.84 | 0.82 | 0.947 |

- **Top choice.** The 5 replicates agree **5/5** (C04 every time).
- **Distributions.** The mean pairwise Spearman correlation of the Choice distributions is **0.994** (minimum 0.980). Top-3 overlap averages 2.67/3 (minimum 2).
- **Size of changes.** The largest change in any candidate's Choice probability is 0.03. Confidence is 0.84 ± 0.01 (range 0.82–0.85).
- **Other answers.** Per-candidate Score/Noul answers varied by at most 0.12.
- **Aggregation.** The aggregated (mean) Choice favourite is C04. A hypothetical edge-branch composite would pick C04 in every run.

**Would aggregation have changed the V1 ticket? NO.**
- Under the no-edge rule Jev has no role in selection.
- Jev's own favourite (C04) is the same in every run, and it happens to equal the fallback's pick.
- Historical first-valid vs aggregate testing was not feasible (`forensic_2342/jev_followup.json`).
