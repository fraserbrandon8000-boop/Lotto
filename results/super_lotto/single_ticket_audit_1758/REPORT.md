# Single-ticket suitability audit (strict causal replay, targets 1652–1757, n = 106)

Each selector produces **one complete ticket per target** from earlier draws only. The V1 reconstruction is verified equal to the frozen #1755–#1757 pools. Null: 5/7 mains per ticket, SB hit 0.1, jackpot 1/3,246,320. Holm across the 5 non-control selectors × (main, SB) = 10 tests.

| Selector | mean mains | p | Holm | SB hits | p | Holm | ≥3 mains (exp) | ≥2 + SB | diff vs incumbent (95% block CI) | distinct tickets | distinct SBs / top-SB share |
|---|---|---|---|---|---|---|---|---|---|---|---|
| V1_fixed_slot (incumbent) | 0.585 | 0.972 | 1.0 | 12/106 | 0.370 | 1.0 | 0 (1.5) | 1 | +0.000 [+0.00, +0.00] | 68 | 9 / 0.32 |
| P0_coverage_1 | 0.726 | 0.454 | 1.0 | 9/106 | 0.744 | 1.0 | 2 (1.5) | 1 | +0.142 [-0.08, +0.35] | 86 | 10 / 0.23 |
| P0_coverage_2 | 0.774 | 0.221 | 1.0 | 12/106 | 0.370 | 1.0 | 1 (1.5) | 4 | +0.189 [+0.00, +0.38] | 104 | 10 / 0.16 |
| P0_standalone_top | 0.632 | 0.890 | 1.0 | 10/106 | 0.624 | 1.0 | 0 (1.5) | 1 | +0.047 [-0.13, +0.22] | 74 | 10 / 0.20 |
| V1_pool_per_draw_seed | 0.755 | 0.305 | 1.0 | 19/106 | 0.009 | 0.08683819045284992 | 1 (1.5) | 3 | +0.170 [+0.01, +0.33] | 90 | 10 / 0.20 |
| uniform_random_control | 0.755 | 0.305 | — | 14/106 | 0.172 | — | 0 (1.5) | 5 | +0.170 [+0.00, +0.34] | 106 | 10 / 0.16 |

1. **Do P0 Coverage 1/2 sacrifice standalone score to cover non-V1 numbers?**
   - Yes, by design. Their median standalone rank among the 792 pool tickets is 154 and 418 (1 = best).
   - But in Super Lotto every P0 credibility weight is 0 at **every** origin (0 origins with non-zero weights). The "standalone score" is therefore only the equal-weight tie-break, not validated evidence. There is no evidence-based standalone score to sacrifice.
2. **Would a single-ticket P0 selector rank tickets differently?** Yes. The top standalone ticket is the five highest equal-weight numbers, not a coverage ticket.
3. **Would it beat V1 historically?** It averaged 0.632 mains vs V1 0.585 (difference CI includes 0). Neither differs from the random null.
4. **Does any advantage survive correction?** **No.** All Holm p ≥ 0.09. The per-draw seed's SB hits (raw p 0.009) do not survive. The uniform random control is as good as any selector.
5. **Is a per-draw randomized selection more defensible when every gate fails?**
   - For prediction it is **equivalent** (same expected value under the null).
   - For the experiment it is **more defensible**: the fixed slot repeats SL10's S_gap Super Ball (SB2 in all 5 live draws; top-SB share 0.32 historically). Per-draw seeding spreads selection over all candidates and SBs.
   - This is a research-quality issue, not a predictive one. The incumbent stays V1 for #1758 (protocol), and per-draw seeding runs as a SHADOW challenger.
