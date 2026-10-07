# M0 — Sequential Draw Reconstruction: research charter

Written and committed **before any M0 model is evaluated**.
- **Branch:** `claude/lotto-m0-reconstruction`, based exactly on `83f3ed1`.
- **Independence:** M0 is independent of V1, P0, Protocol 2344 and Super Lotto. No M0 code reads V1/P0 outputs, Super Lotto files or any #2344 artifact.
- **Disclosure:** the operator (this assistant session) also produced the separate #2344 production tickets on another branch, so their content is known to the operator. M0's design, grids and ticket-selection rule are fixed here, and its ticket is produced by code alone; no manual step exists through which that knowledge could enter.

## Target
The exact unordered six-number main set of the next Jamaica Lotto draw. Universe: C(38,6) = 2,760,681 combinations. The bonus is excluded everywhere.

## Allowed information
- **Data:** completed draws #2161–#2343 only. These are `results/lotto/draw2343/draws.json` (#2161–#2342) plus #2343 = 04 07 13 23 33 35 (bonus 38), the official result supplied by the user and recorded in the ledger.
- **Historical target t:** every quantity (features, parameters, hyperparameters, ensemble weights, rule choice) uses draws with index < t only.
- **Ordering:** extraction order is **unavailable**. Sorted positions are a representation, not physical draw order.

## Prohibited leakage
- Any use of draw t (or later) when ranking t.
- Hyperparameter or rule selection on outer-loop results.
- Global normalisation over the full dataset.
- Any choice made after seeing outer-loop results that is not written here.
- Any #2344 result.
- Any external or other-system #2344 prediction.

## Rolling design
- **Outer targets:** every draw index t ≥ 50, i.e. targets #2211–#2343 (n = 133).
- **Per target:** fit on draws < t, then freeze the scores. Then score all 2,760,681 combinations, rank them and record the primary ticket. Only then compare with draw t.
- **Inner tuning:** strictly before t. Each model's inner rule is in `MODEL_REGISTRY.json`.

## Model families (finite, pre-registered; exact grids in MODEL_REGISTRY.json)
| ID | Family |
|---|---|
| M0-A | Dynamic Bayesian frequency (discounted Beta state, shrinkage to 6/38) |
| M0-B | Gap / hazard (pooled hazard by gap bin, shrunk to 6/38) |
| M0-C | Draw-to-draw transition (pooled ridge logistic on t-1/t-2 relations: retained, ±1..±3 neighbours, mirror 39−x, t-2 membership) |
| M0-D | Co-occurrence graph (time-decayed shrunk pair lifts; number score = attraction to the previous draw + decayed centrality) |
| M0-E | Latent regime (Bernoulli-emission HMM, K ∈ {1,2,3} chosen by BIC on prior data; filtered predictive) |
| M0-F | Supervised next-draw (ridge logistic on 12 prior-only per-number features; λ by inner time-split) |
| M0-G | Complete-set energy (A log-odds + γ · shrunk pair PMI; γ by inner sampled-partition log-score) |
| M0-H | Ensemble of A–F number log-odds; weights ∝ positive prior mean log-score gain (≥20 prior targets, else null) |
| M0-X | Transformation search: 18 pre-listed low-complexity set transformations of t-1/t-2; rule chosen causally by best prior mean overlap |
| M0-R | Null controls (not in the family): uniform exact ranking, random number ranking, random rule from the X library, misaligned-target permutation null |

## Metrics
**Primary** (per target): EXACT_TARGET_RANK of the realised combination among all 2,760,681, with mid-ranks for ties, and its percentile u = (rank − 0.5)/C. Under any outcome-independent ranking u ~ U(0,1).

**Secondary:**
- Top-K hits (K = 1, 10, 100, 1,000, 10,000, 100,000; null K/C);
- primary-ticket matches 0–6 (null hypergeometric mean 36/38);
- best match within the top 10 / 100 / 1,000 tickets;
- exact log-score of the realised set, log P_model(S) + log C, for normalisable models (scores exponentiated and normalised over the full universe);
- number-level winner ranks; Top-6/10/15/20 capture; Bernoulli log loss and Brier.

## Multiple-testing policy
All nine M0 families (A–H, X) form **one family**. Three pre-specified one-sided tests per model:
1. mean u < 0.5 (normal, SD 1/√(12n));
2. primary-ticket mean matches > 36/38 (exact convolution);
3. mean exact log-score > 0 (t-test), for normalisable models.

Holm over all 27 tests (non-normalisable models contribute 2). Nulls are reported but are not in the family.

## Promotion rule (historical gate → "EDGE")
A model shows a historical reconstruction edge only if all of these hold:
- Holm-corrected p < 0.05 on test 1;
- mean u < 0.5 in both chronological halves;
- 5-block bootstrap 95% upper bound of mean u < 0.5;
- it beats the misaligned-permutation null (p < 0.05).

Otherwise the verdict is **M0 HAS NOT DEMONSTRATED A PREDICTIVE RECONSTRUCTION EDGE**. Because the Lotto history has been analysed extensively before, any historical result is **exploratory** only.

## Selection rule for the single prospective procedure (fixed now)
- The primary M0 procedure is the family member with the **lowest out-of-sample mean u**, with ties broken by fewer effective parameters, then alphabetical ID.
- It is chosen whether or not it passes the gate. If it fails, it is labelled NO EDGE.
- Its **primary shadow ticket** is its top-ranked complete combination for #2344 (X: the rule's output set). Ties in the ranking go to the lexicographically smallest combination.

## Prospective validation rule
- Historical results only choose what to test.
- Validity is judged on draws after the M0 protocol freeze, starting with #2344, by the same primary metric (u of the realised ticket) and the matches of the primary shadow ticket.
- The pre-declared check is a one-sided test of mean u < 0.5 at α = 0.05, evaluated at 50 prospective draws.
- M0 has no production influence unless that prospective test passes.
