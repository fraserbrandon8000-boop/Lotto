# Changelog — Lotto Protocol 2344

| Component | Before (#2342–#2343) | Protocol 2344 | Class |
|---|---|---|---|
| Objective statement | implicit; coverage/capture reported as success | explicit P(≥1 6/6) = Σ P(ticket); metric classes | Objective alignment |
| Ticket 1 | V1 Science | **unchanged** | — |
| Tickets 2–3 universe | 5,005 combos of the Top-15 P0 pool | all 2,760,681 combinations | Objective alignment |
| Tickets 2–3 rule | max T + η·coverage, overlap ≤2 (relaxable), evidence exception | max T subject to **zero overlap** with all earlier tickets | Objective alignment |
| Component normalisation | Z within the pool | Z over the full universe | Correctness (design) |
| Evidence weights | frozen P0 constants | **same frozen constants** | — |
| Number ordering / discovery | P0 discovery | **unchanged** (reported, not used to truncate) | — |
| Entry point | draw-specific wrappers | `scripts/research/protocol_2344.py` (parameterised, hashed) | Reproducibility |
| Controls | fixed random portfolio | fixed (kept) + per-draw random + exact null pmfs | Research only |
| Shadows | — | concentration, V1 per-draw seed, legacy P0 | Research only |
| Promotion | historical Holm gate per batch | prospective-only, cumulative α budget | Research policy |
