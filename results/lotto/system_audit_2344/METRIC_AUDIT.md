# Metric audit (A17)

| Metric | Class | Reason |
|---|---|---|
| P(at least one 6/6) = Σ P(ticket) | **PRIMARY** | The user's objective. Equals (distinct tickets)/C(38,6) unless a calibrated combination model exists. |
| Best single-ticket matches (per draw), 6/6 events | **PRIMARY** (realised) | The only realised quantity on the path to a jackpot. |
| Conditional-Bernoulli log-score of the realised combination vs uniform (A9) | **PRIMARY** (skill) | Proper scoring rule for exact-ticket probability; > 0 is required before any jackpot-oriented concentration. |
| P(best ≥5), P(best ≥4), P(best ≥3) | SECONDARY | Lower prize tiers; maximised by pairwise-disjoint tickets under no edge. |
| Discovery-pool winner capture, Top-N capture | DIAGNOSTIC | Measures number ranking only; tells nothing about one ticket holding six. |
| Unique winners covered by the portfolio | DIAGNOSTIC / **MISLEADING FOR JACKPOT** | Winners on different tickets do not combine (the #2342 random control covered 6 with best 3). |
| Total portfolio matches | **MISLEADING FOR JACKPOT** | Expected value is 2.842 for **every** 3-ticket portfolio (A2); cannot be optimised; noise. |
| Number coverage / unique numbers played | DIAGNOSTIC | Affects lower tiers via overlap only. |
| Pairwise overlap | DIAGNOSTIC (structural) | Enters secondary tiers; irrelevant to P(6/6). |
| Jev Choice / confidence | DIAGNOSTIC | Evidence judgment, not a probability of winning (A19). |
| Random-control scores on one draw | DIAGNOSTIC | A single fixed portfolio is a very noisy null; use exact null pmfs. |

Previously reported as success measures and now reclassified: "winners captured by the P0 pool", "portfolio captured N unique winners" and "portfolio total". None may drive production unless a link to the primary objective is shown; A2 shows there is none for total matches and union coverage.
