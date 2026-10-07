# Code / reproducibility audit (A10, A20)

- **Entry points:** {"V1": "scripts/analyze.py (+ scripts/research/v1_prospective.py, lotto_prospective.py wrappers)", "V1_jev": "scripts/research/v1_prospective_jev.mjs / lotto_prospective_jev.mjs", "P0": "scripts/research/p0_apply.py + p0.py", "freeze": "scripts/research/v1_freeze.py, freeze_prospective.py"}.
- **V1 code:** unchanged since snapshot ba7c5a3: **True**.
- **Draw-specific scripts with hard-coded draw IDs:** 14 files (audit_2344_core.py, audit_2344_misc.py, forensic_2341.py, forensic_2341_report.py, forensic_2341_verify.py, forensic_2342.py, forensic_2343.py, freeze_lotto_2340.py, historical_2342.py, lotto_2340.py, lotto_2340_forensic.py, report_lotto_2340.py, research_2342.py, lotto_2340_jev.mjs). Logic is copied between draws (RISK: copy-edit errors). The corrected protocol uses **one parameterised entry point** (`scripts/research/protocol_2344.py --target N`) with hashed inputs.
- **Line endings:** CRLF files now: none. Historical Windows-era hashes are verified with LF→CRLF tolerance where needed.
- **Dependencies:** `@typesafe-ai/sdk` {'@typesafe-ai/sdk': '0.6.0'} (lock 0.6.0); Python 3.13.16, NumPy 2.5.3. `jev-latest` resolves to jev-1.13.0 (receipts).
- **Ledger:** append-only verified against its last 6 committed versions: **True**.
- **Reproduction:**
  - The frozen live #2342 and #2343 P0 tickets reproduce exactly from the frozen protocol constants.
  - The historical P0 replay reproduces `p0_protocol/historical_origins.json` exactly for 2231–2340.
  - The V1 reconstruction reproduces the frozen candidate pools for #2341–#2343.
  - **No implementation bug was found.**
  - The replay differs from live P0 for #2342/#2343 only because the replay re-estimates weights causally while live P0 uses weights frozen at #2340, as the protocol specifies.
- **Post-freeze mutation risk:** tickets are protected by freeze commits and hashes; freeze scripts refuse to overwrite (`open(...,'x')`).

## A10. V1 candidate pool
- **Search space:** V1 searches one fixed sample of 4,096 tickets (seed SEED+999), identical at every cutoff, which is 0.1484% of the universe. Within it, the best ticket for each objective sits at the A_long 0.9999, B_recent 1.0000, C_gap 1.0000, D_trend 0.9998, F_structure 0.9999 quantile of 50,000 uniform tickets. **The search-space limitation is real but immaterial to the objectives V1 optimises.** Because the objectives have no predictive skill, it is not a predictive limitation either.
- **Fixed control:** H_random is one fixed data-independent ticket (05 · 07 · 14 · 21 · 33 · 38) present in every pool. It is a constant, not a per-draw random control.
- **Fixed E_pairs fallback:** when no pair is retained, E_pairs candidates are fixed data-independent tickets.
- **Structure:** see `STATISTICAL_AUDIT.md` and `data/structure_distributions.json`. F_structure candidates under-represent 3+ runs and dense spans; final V1 and P0 tickets do not.
