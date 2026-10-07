# Requirement matrix

| Requirement | Status | Severity | Finding / evidence |
|---|---|---|---|
| A1 requirement completeness | PASS | HIGH | Added A1 checks: P0 frozen-weight drift vs replay (F20), coverage-term dominance (F06), bonus-on-ticket counting rule, environment network limits |
| A2 objective function | FAIL | CRITICAL | F01 |
| A3 concentration vs coverage | RISK | HIGH | F02 |
| A4 #2342/#2343 construction efficiency | PASS | MEDIUM | diagnosis: split is what any objective without outcome knowledge produces |
| A5 conditional construction efficiency | PASS | MEDIUM | A ≈ best-of-3 random pool tickets; concentration worse |
| A6 discovery | FAIL | HIGH | F03 |
| A7 hard pool cutoff | RISK | MEDIUM | F05 |
| A8 score calibration | RISK | MEDIUM | F06 |
| A9 combination probability | FAIL | HIGH | F04 |
| A10 V1 candidate pool | RISK | MEDIUM | F07 |
| A11 fixed seed | RISK | MEDIUM | F08 |
| A12 cluster/structure | PASS | LOW | F09 |
| A13 data | PASS | LOW | F10 |
| A14 feature leakage | PASS | LOW | F11 |
| A15 holdout contamination | FAIL | CRITICAL | F12 |
| A16 cumulative multiple testing | FAIL | HIGH | F13 |
| A17 metrics | FAIL | HIGH | F14 |
| A18 random control | RISK | MEDIUM | F15 |
| A19 Jev | RISK | MEDIUM | F16 |
| A20 code/reproducibility | RISK | MEDIUM | F17 |
| A21 prospective results | PASS | LOW | F18 |
| A22 #2343 forensic | PASS | MEDIUM | results/lotto/forensic_2343/ |
| Implementation correctness (added) | PASS | LOW | F19 |
| P0 weight drift (added) | RISK | LOW | F20 |
| Bonus influence (game rules) | PASS | LOW | bonus never used as a feature or main |

Full FAIL/RISK detail (current behaviour, why it matters, evidence, affected files, predictive impact, correction, validation test, safe-before-#2344, class): `AUDIT_FINDINGS.json`.
