# M0 frozen protocol (for #2344 and later prospective draws)

**Selected procedure: M0-C — draw-to-draw transition model.** Historical verdict: **NO EDGE** (exploratory). It runs as a SHADOW experiment only and has no production influence.

## Exact procedure (code: `scripts/m0/m0.py` model_C + additive/top_list; hashes in FREEZE_MANIFEST.json)
1. **Data:** all completed draws through the cutoff (for #2344: #2161–#2343; dataset hash in manifest). Bonus excluded.
2. **Rows:** for every prior target index u ≥ 2 and every number i, seven features:
   - i in draw u−1;
   - i in draw u−2;
   - i±1 in u−1;
   - i±2 in u−1;
   - i±3 in u−1 (cyclic 1↔38);
   - 39−i in u−1;
   - i in both u−1 and u−2.

   Label = i in draw u.
3. **Fit:** pooled ridge logistic (no penalty on the intercept; IRLS). The ridge strength comes from the grid {1, 10, 100}: fit on the first 70% of prior rows (time order), pick the lowest log loss on the last 30%, then refit on all prior rows. Features are standardised on the training rows.
4. **Predict:** p_i for the next draw from the features of the last two draws. Number score Lᵢ = log(pᵢ/(1−pᵢ)).
5. **Score:** every one of the 2,760,681 combinations by S = Σ Lᵢ (exactly normalisable: conditional-Bernoulli).
6. **M0 PRIMARY SHADOW** = the top-ranked combination (ties → lexicographically smallest). The top-10 list is saved for research.
7. **No change** of structure, grid, features, selection or tie rule after this commit.
