# Jev stability study (#2342 V1 production request; research only)

Five replicates of the **byte-identical** production request (SHA-256 verified against the production receipt) were run **after** every #2342 ticket was frozen. They changed nothing.

| Run | Top Choice | P(top) | Confidence | Entropy (bits) |
|---|---|---|---|---|
| production | C03 | 0.71 | 0.68 | 1.210 |
| replicate_1 | C03 | 0.77 | 0.75 | 1.056 |
| replicate_2 | C03 | 0.76 | 0.73 | 1.085 |
| replicate_3 | C03 | 0.68 | 0.65 | 1.262 |
| replicate_4 | C03 | 0.70 | 0.67 | 1.232 |
| replicate_5 | C03 | 0.77 | 0.74 | 1.056 |

- Top-choice agreement across the 5 replicates: **5/5** (C03 every time).
- Mean pairwise Spearman correlation of the Choice distributions: **0.997** (minimum 0.995). Top-3 overlap: 3/3 in every pair.
- Largest change in any candidate's Choice probability: 0.09. Confidence 0.70 ± 0.04 (range 0.65–0.75).
- Per-candidate Score/Noul answers varied by at most 0.09.
- Aggregated (mean) Choice favourite: C03. A hypothetical edge-branch composite would pick C03 in every run.

**Would aggregation have changed the V1 ticket? NO.** Using the first valid response or an aggregate of all six responses would not have changed the V1 ticket: under the no-edge rule Jev has no role in selection, and even Jev's own favourite (C03) is identical in every run.
