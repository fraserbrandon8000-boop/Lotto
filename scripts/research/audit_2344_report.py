"""Write the #2344 system-audit Markdown documents from saved JSON (no new evidence is computed here)."""
import json,math
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'results/lotto/system_audit_2344';D=O/'data'
J=lambda p:json.loads(Path(p).read_text())
a2=J(D/'a2_objective.json');a3=J(D/'a3_strategies.json')['strategies'];a5=J(D/'a5_conditional_efficiency.json')['by_strategy'];a6=J(D/'a6_discovery.json');a7=J(D/'a7_truncation.json')
a8=J(D/'a8_calibration.json');a9=J(D/'a9_combination_probability.json')['models'];a11=J(D/'a11_seed_designs.json')['designs'];cf=J(D/'construction_counterfactual_2342_2343.json')
da=J(D/'data_audit.json');pr=J(D/'prospective_rescore.json');st=J(D/'structure_distributions.json')['sets'];jv=J(D/'jev_audit.json');cd=J(D/'code_facts.json');src=J(D/'v1_source_pool.json')
lk=J(D/'leakage_mutation.json');reg=J(O/'RESEARCH_REGISTRY.json');FD=J(O/'AUDIT_FINDINGS.json')['findings'];wf=J(D/'walk_forward_rows.json')
f4=J(R/'results/lotto/forensic_2343/winner_evidence.json');f4p=J(R/'results/lotto/forensic_2343/pool_scores.json');f4t=J(R/'results/lotto/forensic_2343/two_layer_diagnosis.json');f4v=J(R/'results/lotto/forensic_2343/verification.json')
nn=lambda l:' · '.join(f'{x:02}' for x in l);CN=a2['universe']
def w(name,txt):(O/name).write_text(txt.strip()+'\n')
# ---------------------------------------------------------------- OBJECTIVE_AUDIT
P=a2['portfolios']
rows='\n'.join(f"| {k} | {v['distinct']} | {v['unique_numbers']} | {v['P_six']:.4e} | {v['P_ge5']:.3e} | {v['P_ge4']:.5f} | {v['P_ge3']:.5f} | {v['E_best']:.4f} | {v['E_total']:.3f} | {v['E_unique_winners']:.3f} |" for k,v in P.items())
s3='\n'.join(f"| {k} | {v['mean']:.3f} | {v['expected']:.3f} | {v['excess']:+.3f} | {v['p_one_sided']:.3f} | {v['holm_p']:.2f} | {v['count_ge3']} ({v['expected_ge3']:.1f}) | {v['count_ge4']} ({v['expected_ge4']:.2f}) | {v['count_ge5']} ({v['expected_ge5']:.3f}) | {v['count_ge6']} | {v['confirmation_excess']:+.3f} | {v['half1']:+.3f} / {v['half2']:+.3f} | [{v['block95'][0]:+.2f}, {v['block95'][1]:+.2f}] | {v['secondary']['total']:.2f} | {v['secondary']['unique_winners']:.2f} | {v['secondary']['unique_numbers']:.1f} |" for k,v in a3.items())
s5=''
for s,v in a5.items():
    s5+=f"\n**{s}**\n\n| K winners in pool | draws | E[best] | E[2nd] | E[portfolio in-pool winners] | max possible | efficiency | random: 1 pool ticket | best of 2 random | best of 3 random |\n|---|---|---|---|---|---|---|---|---|---|\n"
    s5+='\n'.join(f"| {k} | {x['n']} | {x['E_best']:.2f} | {x['E_second']:.2f} | {x['E_portfolio_inpool_winners']:.2f} | {x['max_possible']} | {x['efficiency'] if x['efficiency'] is None else round(x['efficiency'],2)} | {x['random_one_pool_ticket']:.2f} | {x['random_best_of_2']:.2f} | {x['random_best_of_3']:.2f} |" for k,x in v.items())+'\n'
c42,c43=cf['2342'],cf['2343']
w('OBJECTIVE_AUDIT.md',f"""
# Objective audit (A2, A3, A4, A5, A9, A22 construction)

**User objective:** at least one of three played tickets matches all six mains. Universe C(38,6) = {CN:,}.

## A2. The jackpot probability of a portfolio (exact)

For distinct tickets the events "draw = ticket i" are disjoint, so

P(at least one 6/6) = Σᵢ P(draw = ticketᵢ).

Under a uniform (no-edge) draw each term is 1/C(38,6), so **any three distinct tickets give exactly 3/C(38,6) = {3/CN:.4e}** (1 in {CN/3:,.0f}), whatever their overlap, number spread or coverage. Verified by enumerating all {CN:,} draws for seven structures (`data/a2_objective.json`, verified = {a2['verified_by_enumeration']}):

| Structure | distinct tickets | unique numbers | P(6/6) | P(best ≥5) | P(best ≥4) | P(best ≥3) | E[best] | E[total matches] | E[unique winners covered] |
|---|---|---|---|---|---|---|---|---|---|
{rows}

What this proves:
- **Maximising unique-number coverage, minimising overlap and spreading numbers do not change P(6/6).** They are not jackpot optimisation.
- **Expected total portfolio matches is identical (2.842) for every portfolio**, so it cannot be optimised at all; it is pure noise as a success metric.
- Unique winners covered rises with the union size, but a winner on another ticket does nothing for 6/6 (the #2342 random control covered 6 winners across tickets with a best of 3).
- Low overlap **does** maximise the secondary tiers: zero overlap gives the highest P(4+), P(3+) and E[best] of all structures; P(5+) is maximal for every structure with pairwise overlap ≤3. Concentration (five shared numbers) lowers every secondary tier without raising P(6/6).

## A9. Can P(exact combination) be estimated better than uniform?

Model: conditional-Bernoulli (exponential family on 6-subsets) P(S) ∝ Πᵢ∈S exp(β·sᵢ), β fitted by maximum likelihood on prior origins only. This is the defensible way to turn number scores into exact-ticket probabilities (it does not multiply uncalibrated marginals). Score = log P_model(realised combination) − log(1/C), averaged over {wf['n']} causal targets:

| Score vector | mean log-ratio vs uniform | implied multiplier on the realised ticket | p (one-sided) | causal β (mean / range) | confirmation mean | best in-sample (hindsight) mean |
|---|---|---|---|---|---|---|
""" + '\n'.join(f"| {k} | {v['mean_log_ratio_vs_uniform']:+.4f} | {v['implied_mean_multiplier']:.4f} | {v['p_one_sided'] if v['p_one_sided'] is None else round(v['p_one_sided'],3)} | {v['beta_path_summary']['mean']:+.3f} / [{v['beta_path_summary']['min']:+.2f}, {v['beta_path_summary']['max']:+.2f}] | {v['confirmation_mean_log_ratio']:+.4f} | {v['insample_max_mean_log_ratio']:+.4f} |" for k,v in a9.items()) + f"""

**No score assigns the realised combinations more probability than uniform.** The causally fitted β is near zero or negative, and even the best in-sample (hindsight) β gains ≤0.0023 nats per draw (a jackpot-probability multiplier of ≤1.002). **The defensible estimate of P(exact ticket) is 1/C(38,6) for every ticket.** So Σ P(ticket) cannot be raised by construction with present evidence.

## A3. Concentration vs coverage, historical (targets {wf['targets'][0]}–{wf['targets'][1]}, n = {wf['n']}, strictly causal)

Primary = best single-ticket matches against the **exact null of that portfolio's own overlap structure** (enumerated over all C(38,6) draws per origin). Secondary/diagnostic columns at the right. Holm across the 8 strategies.

| Strategy | best (obs) | best (null) | excess | p | Holm | ≥3 (exp) | ≥4 (exp) | ≥5 (exp) | 6/6 | conf. excess | halves | block 95% | total | unique winners | unique numbers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
{s3}

- A = current P0 (V1 + coverage challengers); B = top-3 standalone T; C = best T + 2 diversified (overlap ≤2); D = concentration on top-ranked numbers (Top-6, Top-5+7th, Top-5+8th); E = V1 + standardised T/coverage hybrid; F = V1 + 2 random; G = 3 random; H = V1 + 2 tickets with zero overlap, ranked by T.
- The no-edge P(6/6) per draw is **{a3['A_coverage_P0']['null_P_jackpot_per_draw']:.4e} for every strategy** (3 distinct tickets). No 5/6 or 6/6 occurred in any strategy.
- **No strategy beats its own null** (all Holm p = 1.0). Concentration strategies (B, D) have the lowest best-ticket means because their null expectation is lowest (they repeat numbers); they do not concentrate winners because the ranking that drives them has no skill (A6).
- Differences between A, C, F, H are what their overlap structures predict under the null.

## A5. Conditional construction efficiency (in-pool winners only)
{s5}
The current constructor (A) places in-pool winners on its best ticket at about the rate of the best of three random pool tickets, slightly above best-of-two. Concentration strategies (B, D) put **fewer** in-pool winners on their best ticket than one random pool ticket would at K = 2–4, because concentration follows the (skill-less) ranking. **Once discovery finds winners, no constructor can concentrate them without knowing which pool numbers won.** That information does not exist before the draw.

## A4 / A22. #2342 and #2343 construction counterfactuals (diagnosis only; nothing promoted)

| | #2342 | #2343 |
|---|---|---|
| available in-pool winners | {', '.join(f'{x:02}' for x in c42['available_winners'])} | {', '.join(f'{x:02}' for x in c43['available_winners'])} |
| pool tickets containing all of them | {c42['n_containing_all_available']} (random count {c42['expected_if_random']}) | {c43['n_containing_all_available']} (random count {c43['expected_if_random']}) |
| raw-T rank of those tickets: best / median / worst (of 5,005) | {c42['rank_min']} / {c42['rank_median']:.0f} / {c42['rank_max']} | {c43['rank_min']} / {c43['rank_median']:.0f} / {c43['rank_max']} |
| best such ticket | {nn(c42['best_containing']['numbers'])} | {nn(c43['best_containing']['numbers'])} |
| available winners on frozen V1 / T2 / T3 | {c42['frozen_portfolio_inpool_hits']} | {c43['frozen_portfolio_inpool_hits']} |
| frozen T2 / T3 raw-T rank | {c42['frozen_ticket_T_ranks'][1:]} | {c43['frozen_ticket_T_ranks'][1:]} |
| standalone top-3 tickets: available winners each | {[x['available_hits'] for x in c42['standalone_top3']]} | {[x['available_hits'] for x in c43['standalone_top3']]} |
| concentration (Top-6 numbers): available winners | {c42['concentration_top6_numbers']['available_hits']} | {c43['concentration_top6_numbers']['available_hits']} |

- **#2343:** 04 and 13 were P0 ranks 2 and 1, 07 rank 9, 33 rank 15. A 4-winner ticket needs 07 and 33 next to 04 and 13, but the T ordering ranks such tickets 159th at best. **No pre-draw objective (standalone, concentration or hybrid) would have chosen one**; each puts the top-ranked numbers (13, 04, 12, 14, 24) together, so they hold 2 available winners. The frozen portfolio split the four because V1 already held 04 and 13 (5 of its 6 numbers are pool numbers), and the coverage term (SD {a8['coverage_to_T_sd_ratio']:.1f}× the T SD) pushes the challengers onto other pool numbers.
- **#2342:** 220 pool tickets contained 12, 13 and 14; the best was ranked 22nd; the standalone top-3 held 1, 2 and 1.
- **Conclusion:** both "split" outcomes are what any objective without knowledge of the winners produces. The split is not a construction defect, and concentrating would not have helped before the draw.

## Rational 3-ticket policy
- **A. No predictive edge (current state):** P(6/6) = 3/C(38,6) for any 3 distinct tickets, so the jackpot objective is **indifferent** among them. The rational choice then maximises the secondary tiers exactly: **three pairwise-disjoint tickets** (maximal P(5+), P(4+), P(3+), E[best]). Ticket identity can be set by any pre-declared rule (evidence tie-break or seeded random) at zero jackpot cost.
- **B. Weak, unvalidated signal:** its value for 6/6 is bounded by its prospective likelihood ratio, measured here as ≤1 (A9). Use it **only as a tie-break inside the secondary-optimal set**, because following it costs nothing if it is noise but concentrating on it costs secondary tiers for no demonstrated jackpot gain.
- **C. Genuinely calibrated signal (P̂(S) validated prospectively):** maximise Σ P̂(Sᵢ), i.e. **the three highest-P̂ distinct combinations, with no diversity penalty** (diversity would trade jackpot probability for lower tiers). Switch rule: only when the A9 log-score passes the prospective gate (see `results/lotto/protocol_2344/PROTOCOL.md`).
""")
# ---------------------------------------------------------------- METRIC_AUDIT
w('METRIC_AUDIT.md',f"""
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
""")
# ---------------------------------------------------------------- STATISTICAL_AUDIT
t6='\n'.join(f"| {m} | {v['n']} | {v['mean_winner_rank']:.2f} | {v['p_rank']:.3f} | {v['mrr']:.4f} ({v['null_mrr']:.4f}) | {v['ap']:.4f} ({v['null_ap']:.4f}) | "+' | '.join(f"{v['capture'][str(N)]['excess']:+.2f}" for N in [5,10,12,15,18,20,25,30])+f" | {v['capture']['15']['p']:.3f} | {a6['holm'][m+':top15']:.2f} | {v['halves_rank_z'][0]:+.2f} / {v['halves_rank_z'][1]:+.2f} | [{v['block95_rank_z'][0]:+.2f}, {v['block95_rank_z'][1]:+.2f}] |" for m,v in a6['methods'].items())
p0c=a6['methods']['P0_order']['capture']
tp='\n'.join(f"| Top {N} | {p0c[str(N)]['mean']:.3f} | {p0c[str(N)]['random']:.3f} | {p0c[str(N)]['excess']:+.3f} | "+' / '.join(f"{p0c[str(N)]['ge'][str(k)]:.2f}" for k in range(2,7))+' | '+' / '.join(f"{p0c[str(N)]['ge_random'][str(k)]:.2f}" for k in range(2,7))+f" | {p0c[str(N)]['confirmation_excess']:+.3f} | {p0c[str(N)]['p']:.3f} | {a6['holm']['P0_order:top'+str(N)]:.2f} |" for N in [5,10,12,15,18,20,25,30])
w('STATISTICAL_AUDIT.md',f"""
# Statistical audit (A6, A7, A8, A11, A14, A15, A16, A18, A21)

## A6. Does the number ordering predict winners better than random?
Strictly causal origins {wf['targets'][0]}–{wf['targets'][1]} (n = {wf['n']}). Exact nulls: mean winner rank 19.5 (SD per draw {math.sqrt(((38**2-1)/12)/6*(32/37)):.2f}), hypergeometric Top-N capture, simulated MRR/AP. One Holm family of {a6['family_size']} tests.

| Ordering | n | mean winner rank | p | MRR (null) | AP (null) | Top5 | Top10 | Top12 | Top15 | Top18 | Top20 | Top25 | Top30 | Top-15 p | Top-15 Holm | halves (rank z) | block 95% (rank z) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
{t6}

(Top-N cells = excess winners captured over 6N/38.) Smallest raw p {a6['min_raw']:.3f} ({a6['argmin_raw']}); smallest Holm p {a6['min_holm']:.2f}. The uniform-random ordering's spread shows the noise level.

**THE CURRENT NUMBER ORDERING DOES NOT PREDICT WINNERS BETTER THAN RANDOM.** Calibration/Brier: the conditional-Bernoulli fit (A9) is the calibrated version of each ordering; its causal β is ≤ 0 on average, so calibrated inclusion probabilities collapse to 6/38 and the Brier skill is ≤ 0.

### P0 ordering by pool size (A6/A7)
| Pool | mean captured | random | excess | P(≥2/3/4/5/6) | random | conf. excess | p | Holm |
|---|---|---|---|---|---|---|---|---|
{tp}

No pool size captures more than its size implies. Larger pools only capture more mechanically.

## A7. Hard Top-15 cutoff
Full-universe scoring of all {CN:,} combinations takes {a7['full_universe_scoring_seconds']} s. At the {a7['origins_with_nonzero_weights']} origins where P0 weights were non-zero, the full-universe best ticket was always inside the Top-15 pool (best pool ticket = full rank {a7['full_rank_of_best_top15_ticket']['median']:.0f}). But only {a7['share_full_top1000_inside']['15']:.0%} of the full top-1,000 lie inside it ({a7['share_full_top1000_inside']['20']:.0%} at Top 20, {a7['share_full_top1000_inside']['25']:.0%} at Top 25). The cutoff does not hide the single best-scoring ticket. It does remove most near-best alternatives and **forces overlap** whenever ticket 1 occupies pool numbers (at #2343 V1 held 5 of the 15). A wider universe creates no skill; it removes an unnecessary constraint.

## A8. Score calibration
Family scores are z-scores over the 38 numbers (SDs {[round(x,2) for x in a8['family_score_sd']]}; E_pairs flat = 0), so families are commensurate. But: (i) universe components are Z-normalised **within the pool**, so their relative scale depends on K; (ii) frozen weights are tiny (B 0.031, D 0.024, struct 0.007), so T has SD {a8['T_sd']:.3f} while the coverage term has SD {a8['coverage_term_sd']:.3f} (**{a8['coverage_to_T_sd_ratio']:.1f}×**): coverage, not evidence, picks the tickets; (iii) T is not a probability. Sign conventions are consistent (C_gap: longer absence = higher score, an explicit "overdue" hypothesis). Ties are broken deterministically by EQ, then number.

## A11. Fixed-seed / repeated-ticket designs (V1 chain, targets {J(D/'a11_seed_designs.json')['targets']})
| Design | total matches (exp {a11['fixed_current_seed']['expected']:.0f}) | p(≥obs) | ≥3 (exp {a11['fixed_current_seed']['expected_ge3']:.1f}) | distinct tickets | distinct IDs | top-ticket share | consecutive overlap | lag-2 exact repeat |
|---|---|---|---|---|---|---|---|---|
""" + '\n'.join(f"| {k} | {v['total_matches']} | {v['p_total_ge']:.2f} | {v['ge3']} | {v['distinct_tickets']} | {v['distinct_ids']} | {v['top_ticket_share']:.3f} | {v['mean_consecutive_overlap']:.2f} | {v['lag2_exact_repeat']:.3f} |" for k,v in a11.items() if k!='uniform_candidate_expectation') + f"""
| uniform candidate (expectation) | {a11['uniform_candidate_expectation']['total_matches']:.1f} | — | — | — | — | — | — | — |

1. **Predictive performance:** no design differs from chance (all p ≥ 0.25). Repeating a ticket does not change its per-draw jackpot probability.
2. **Exploration:** the fixed seed concentrates on 5 candidate IDs, and with the overlap rule live V1 played only two distinct tickets in five draws. Per-draw seeding or rotation explore far more. This is an experiment-quality issue, not a predictive one.

## A14. Leakage
Mutation test (all draws at and after the target replaced by random draws) at 4 origins: features, P0 weights, P0 order and V1 candidates are identical. **PASS = {lk['PASS']}.** Code review: rolling windows, EW, gaps, trends, pair Holm tests, ensemble weights (prior walk rows only), structure means/SDs and P0 reliability weights (prior origins only) all use `d[:t]`.

## A15. Holdout contamination — CRITICAL
Draws 2299–2343 have each been used as "confirmation" by up to **{reg['draw_reuse']['max_times_used_as_confirmation']} separate studies** ({reg['draw_reuse']['draws_used_as_confirmation_3plus']} draws used ≥3 times), and every forensic inspected them. They are **not** a pristine holdout. Historical "confirmation" results are descriptive from now on.

**Validation hierarchy (adopted for future research):**
1. Development: rolling-origin walk-forward over the full history.
2. Historical pseudo-holdout: descriptive only, never sufficient for promotion.
3. **Prospective live draws after a protocol is frozen are the only promotion evidence.**

## A16. Cumulative multiple testing — CRITICAL
`RESEARCH_REGISTRY.json`: **{reg['cumulative_formal_tests']} formal tests** across 10 Lotto studies (plus about {reg['cumulative_exploratory_comparisons']:,} exploratory comparisons). Holm was applied within each batch only. Bonferroni at the cumulative family gives α = {reg['bonferroni_alpha_per_test_at_cumulative_family']:.1e} per test; **no result anywhere comes close**. Because every promotion test failed, no false discovery entered production, but batch-wise correction understates the risk.

**Policy:**
- Every new hypothesis is added to the registry before testing.
- Promotion requires a pre-registered prospective test with a fixed α budget (α = 0.05 split across all challengers alive at the time).
- Shadows accumulate live evidence only.
- No historical re-test can promote.

## A18. Random control
The fixed control (seed 20260930) repeats the same three tickets every draw. That is a valid but very noisy single-portfolio null. It is kept unchanged for continuity. From #2344 research also records:
- a per-draw seeded random portfolio;
- the exact null pmf of best-ticket matches for the played portfolio's overlap structure (enumerated).

Historical controls are not changed.

## A21. Prospective record (re-scored from frozen artifacts)
""" + '\n'.join(f"| {e['draw']} | {e['track']} | {nn(e['ticket'])} | {nn(e['outcome'])} + {e['bonus']} | {e['main_matches']} | {', '.join(f'{x:02}' for x in e['matched']) or '—'} | {'yes' if e['bonus_on_ticket'] else 'no'} | {e['generator']} | {e['jev_favourite']} ({e['jev_favourite_matches']}) |" for e in pr['entries']).join(['| Draw | Track | Ticket | Result | mains | matched | bonus on ticket (not a main match) | generator | Jev favourite (its matches) |\n|---|---|---|---|---|---|---|---|---|\n','']) + f"""

V1 (#2339–#2343): {', '.join(str(m) for _,m in pr['summary']['v1'])} = {pr['summary']['v1_total']} vs {pr['summary']['v1_expected']:.2f} expected (P(≥{pr['summary']['v1_total']}) = {pr['summary']['v1_p_total_ge']:.3f}). Two ≥3 tickets in 5 (nominal p {pr['summary']['v1_p_ge3_count_ge_obs']:.3f}, chosen after seeing the data). **Only {pr['summary']['v1_distinct_tickets']} distinct V1 tickets were played.** P0 best single ticket: #2342 {pr['summary']['p0_challenger_best']['2342']}, #2343 {pr['summary']['p0_challenger_best']['2343']}; fixed random control best: {pr['summary']['random_control_best']['2342']}, {pr['summary']['random_control_best']['2343']}. Exact single-ticket null: P(≥3) = {pr['summary']['null']['p_ge3']:.4f}, P(≥4) = {pr['summary']['null']['p_ge4']:.5f}, P(6) = {pr['summary']['null']['p6']:.3e}. **Everything is consistent with chance; the 3,0,3,0,2 sequence is two tickets played repeatedly.**
""")
# ---------------------------------------------------------------- DATA_AUDIT
w('DATA_AUDIT.md',f"""
# Data audit (A13)

- **Rows:** {da['n']} draws #{da['first']}–#{da['last']} ({da['first_date']} → {da['last_date']}).
- **Integrity:** issues found: {da['issues'] or 'none'}. Contiguous IDs, strictly increasing dates, six unique mains in 1–38 (sorted), bonus in 1–38 and never equal to a main.
- **Cadence:** {da['weekday_counts']} (day gaps {da['day_gap_counts']}).
- **Provenance:** {da['provenance']}. #2252–#2261 come from the official Supreme Ventures archive (`official_archive`); #2340–#2343 are official results supplied by the user (`official_user_supplied`). **#2343 (04 07 13 23 33 35, bonus 38)** was supplied by the user in this audit task and is not independently fetched, because the official service is blocked by this environment's network policy.
- **Bonus:** {da['bonus_check']}. **The bonus is not a feature and never a seventh main.** A bonus number on a ticket (e.g. 38 on the #2343 V1 ticket) is not counted as a main match.
- **Rule continuity:** {da['rule_continuity']}
- **Deeper history:** {da['deeper_history']} Even if it were available, it would not be added without first verifying rule continuity and provenance.
- **Statistical power:** detecting a per-ticket mean-match uplift of +0.1 needs about {da['power_draws_needed_per_ticket_mean_uplift']['0.1']} draws (+0.05: {da['power_draws_needed_per_ticket_mean_uplift']['0.05']}). The dataset has {da['n']}. {da['note_power']} More same-rule history would help detect lower-tier effects, but **no amount of history can validate a 6/6 rate directly**; only the A9 log-score can measure combination-level skill.
""")
# ---------------------------------------------------------------- CODE_AUDIT
w('CODE_AUDIT.md',f"""
# Code / reproducibility audit (A10, A20)

- **Entry points:** {json.dumps(cd['production_entry_points'])}.
- **V1 code:** unchanged since snapshot ba7c5a3: **{cd['v1_code_unchanged_since_snapshot']}**.
- **Draw-specific scripts with hard-coded draw IDs:** {len(cd['draw_specific_named'])} files ({', '.join(x.split('/')[-1] for x in cd['draw_specific_named'])}). Logic is copied between draws (RISK: copy-edit errors). The corrected protocol uses **one parameterised entry point** (`scripts/research/protocol_2344.py --target N`) with hashed inputs.
- **Line endings:** CRLF files now: {cd['crlf_files'] or 'none'}. Historical Windows-era hashes are verified with LF→CRLF tolerance where needed.
- **Dependencies:** `@typesafe-ai/sdk` {cd['dependencies']['package_json']} (lock {cd['dependencies']['lock_sdk']}); Python {cd['python']}, NumPy {cd['numpy']}. `jev-latest` resolves to jev-1.13.0 (receipts).
- **Ledger:** append-only verified against its last 6 committed versions: **{cd['ledger_append_only']}**.
- **Reproduction:**
  - The frozen live #2342 and #2343 P0 tickets reproduce exactly from the frozen protocol constants.
  - The historical P0 replay reproduces `p0_protocol/historical_origins.json` exactly for 2231–2340.
  - The V1 reconstruction reproduces the frozen candidate pools for #2341–#2343.
  - **No implementation bug was found.**
  - The replay differs from live P0 for #2342/#2343 only because the replay re-estimates weights causally while live P0 uses weights frozen at #2340, as the protocol specifies.
- **Post-freeze mutation risk:** tickets are protected by freeze commits and hashes; freeze scripts refuse to overwrite (`open(...,'x')`).

## A10. V1 candidate pool
- **Search space:** V1 searches one fixed sample of 4,096 tickets (seed SEED+999), identical at every cutoff, which is {src['fraction_of_universe']:.4%} of the universe. Within it, the best ticket for each objective sits at the {', '.join(f'{k} {v:.4f}' for k,v in src['best_source_ticket_percentile_in_universe'].items())} quantile of 50,000 uniform tickets. **The search-space limitation is real but immaterial to the objectives V1 optimises.** Because the objectives have no predictive skill, it is not a predictive limitation either.
- **Fixed control:** H_random is one fixed data-independent ticket ({nn(src['H_random_fixed_ticket'][0])}) present in every pool. It is a constant, not a per-draw random control.
- **Fixed E_pairs fallback:** when no pair is retained, E_pairs candidates are fixed data-independent tickets.
- **Structure:** see `STATISTICAL_AUDIT.md` and `data/structure_distributions.json`. F_structure candidates under-represent 3+ runs and dense spans; final V1 and P0 tickets do not.
""")
# ---------------------------------------------------------------- JEV_AUDIT
pj=jv['per_draw']
w('JEV_AUDIT.md',f"""
# Jev audit (A19)

Saved calls only: 5 production calls (#2339–#2343) and 10 research replicates (#2342, #2343). No new historical calls. The live TypeSafe docs were unreachable (egress blocked). Semantics are taken from the installed SDK 0.6.0 and the documented project usage: Choice returns a preference distribution and a confidence, not winning probabilities.

| Draw | options | favourite (P) | confidence | Spearman Choice~matches | Spearman Choice~ensemble rank | Spearman Choice~model agreement | Spearman Choice~ID position | favourite matches | mean option matches | Choice mass by generator |
|---|---|---|---|---|---|---|---|---|---|---|
""" + '\n'.join(f"| {t} | {v['n_options']} | {v['favourite']} ({v['fav_prob']:.2f}) | {v['confidence']:.2f} | {v['spearman_choice_matches']:+.2f} | {v['spearman_choice_ensemble_rank']:+.2f} | {v['spearman_choice_agreement']:+.2f} | {v['spearman_choice_position']:+.2f} | {v['fav_matches']} | {v['mean_matches']:.2f} | {', '.join(f'{g} {x:.2f}' for g,x in v['choice_by_generator'].items() if x>=.01)} |" for t,v in pj.items()) + f"""

1. **Does Choice correlate with realised matches?** Pooled Spearman {jv['pooled_spearman_choice_matches']:+.2f} over {jv['pooled_n']} options (5 draws, ties, repeated tickets). The favourite averaged {jv['favourite_mean_matches']:.1f} matches vs {jv['option_mean_matches']:.2f} for all options. With n = 5 draws, two of which are the same ticket (C04 = 01 04 13 14 24 38), this is not evidence of skill.
2. **Is top-1 stable?** Replicates: #2342 {jv['replicates']['2342']['agreement']} (Spearman {jv['replicates']['2342']['spearman']:.3f}); #2343 {jv['replicates']['2343']['agreement']} (Spearman {jv['replicates']['2343']['spearman']:.3f}). Stable when one option dominates.
3. **Candidate order / IDs.** Untested so far. The Choice~ID-position correlation is small except at #2340 (+0.57). A post-freeze order-permutation and blinded-ID test runs for #2344 (research only).
4. **Generator labels / presentation.** Choice mass concentrates on A_long (2339, 2340, 2342) or B_recent (2341, 2343) candidates, the families with the strongest-looking frequency evidence. This is consistent with Jev reading the presented evidence (Choice tracks ensemble rank and agreement, Spearman +0.2 to +0.5).
5. **First-valid vs aggregated.** Identical favourite in all 12 saved calls for #2342/#2343. Historical aggregation testing is not feasible (~550 calls).
6. **Signal beyond the candidate evidence?** **Not demonstrated.** The underlying evidence has no predictive value (A6, A9), and Jev's preferences follow that evidence.

**Production role:** under the no-edge rule Jev never changes the V1 ticket. Its single V1 call is kept unchanged for protocol continuity (it would matter only if a model passed the V1 gate). **Jev contributes no measurable predictive value.**
""")
# ---------------------------------------------------------------- REQUIREMENT_MATRIX
reqs=[('A1 requirement completeness','PASS','HIGH','Added A1 checks: P0 frozen-weight drift vs replay (F20), coverage-term dominance (F06), bonus-on-ticket counting rule, environment network limits'),
('A2 objective function','FAIL','CRITICAL','F01'),('A3 concentration vs coverage','RISK','HIGH','F02'),('A4 #2342/#2343 construction efficiency','PASS','MEDIUM','diagnosis: split is what any objective without outcome knowledge produces'),
('A5 conditional construction efficiency','PASS','MEDIUM','A ≈ best-of-3 random pool tickets; concentration worse'),('A6 discovery','FAIL','HIGH','F03'),('A7 hard pool cutoff','RISK','MEDIUM','F05'),('A8 score calibration','RISK','MEDIUM','F06'),
('A9 combination probability','FAIL','HIGH','F04'),('A10 V1 candidate pool','RISK','MEDIUM','F07'),('A11 fixed seed','RISK','MEDIUM','F08'),('A12 cluster/structure','PASS','LOW','F09'),('A13 data','PASS','LOW','F10'),
('A14 feature leakage','PASS','LOW','F11'),('A15 holdout contamination','FAIL','CRITICAL','F12'),('A16 cumulative multiple testing','FAIL','HIGH','F13'),('A17 metrics','FAIL','HIGH','F14'),('A18 random control','RISK','MEDIUM','F15'),
('A19 Jev','RISK','MEDIUM','F16'),('A20 code/reproducibility','RISK','MEDIUM','F17'),('A21 prospective results','PASS','LOW','F18'),('A22 #2343 forensic','PASS','MEDIUM','results/lotto/forensic_2343/'),
('Implementation correctness (added)','PASS','LOW','F19'),('P0 weight drift (added)','RISK','LOW','F20'),('Bonus influence (game rules)','PASS','LOW','bonus never used as a feature or main')]
w('REQUIREMENT_MATRIX.md','# Requirement matrix\n\n| Requirement | Status | Severity | Finding / evidence |\n|---|---|---|---|\n'+'\n'.join(f'| {a} | {b} | {c} | {d} |' for a,b,c,d in reqs)+
  '\n\nFull FAIL/RISK detail (current behaviour, why it matters, evidence, affected files, predictive impact, correction, validation test, safe-before-#2344, class): `AUDIT_FINDINGS.json`.\n')
# ---------------------------------------------------------------- AUDIT_REPORT
ev=f4['evidence']
w('AUDIT_REPORT.md',f"""
# Lotto system audit before #2344

**Scope:** the full Jamaica Lotto V1 + P0 system (branch `claude/lotto-2344-audit`, base `670a300`). Lotto data only. History #2161–#2343, with #2343 added as one ordinary observation. No #2344 work was started before this audit was committed.

## Headline
1. **The jackpot objective cannot currently be improved by construction.**
   - For distinct tickets, P(≥1 jackpot) = Σ P(ticket). No model assigns realised combinations more probability than uniform (A9), so every 3-distinct-ticket portfolio has **exactly 3/C(38,6) = 1/920,227**.
   - Coverage, overlap and number spread change only the lower tiers. Expected total matches is the same for every portfolio (A2).
2. **The current P0 objective and reporting are misaligned with 6/6.**
   - P0 maximises pool coverage, and the coverage term outweighs the evidence score 3.5:1.
   - Reports used union coverage and total matches as success measures.
   - Under no edge this does not hurt 6/6, but it optimises the wrong quantity. The Top-15 hard cut also forces overlap with V1, which reduces the secondary tiers.
3. **No predictive edge.**
   - No number ordering beats random (A6; smallest Holm p 1.0).
   - No construction strategy beats its exact null (A3).
   - No combination model beats uniform (A9).
4. **The validation evidence is compromised for any future historical promotion.**
   - 385 formal tests across 10 studies, with Holm applied per batch only.
   - The last ~45 draws were used as "confirmation" up to 7 times.
   - Only prospective draws can validate from now on.
5. **No implementation bug or leakage was found.**
   - The frozen live tickets reproduce exactly.
   - Future-mutation tests pass.
   - The data are clean.

## #2343 forensic (A22)

Integrity: all checks pass (`forensic_2343/verification.json`: {f4v['ALL_PASS']}).
- The pool was frozen 2026-10-03T06:44:55Z and the tickets at 06:45:21 / 06:45:48.
- The draw was at 2026-10-04T01:25Z; the replicates ran after the freeze.

| Winner | A_long | B_recent | C_gap | D_trend | E_pairs (flat) | G proxy | H | P0 rank | in frozen Top-15? |
|---|---|---|---|---|---|---|---|---|---|
""" + '\n'.join(f"| {int(n):02} | {e['models']['A_long']['rank']} | {e['models']['B_recent']['rank']} | {e['models']['C_gap']['rank']} | {e['models']['D_trend']['rank']} | {e['models']['E_pairs']['rank']} [1–38] | {e['models']['G_marginal_proxy']['rank']} | {e['models']['H_random']['rank']} | **{e['P0_rank']}** | {'yes' if e['P0_rank']<=15 else 'no'} |" for n,e in ev.items()) + f"""

- **Frozen pool (from `p0_result.json`, not inferred):** 13 04 12 14 24 02 01 22 07 18 10 06 08 09 33.
  - Inside: 04 (rank 2), 07 (9), 13 (1), 33 (15).
  - Outside: 23 (19), 35 (24).
  - Capturing 4 is better than typical: P(≥4 | random Top-15) = 0.15.
- **23:** best support B_recent 15, worst A_long 35. It enters a Top-20 pool but not a Top-18. **35:** best support C_gap 9, worst D_trend 33. It enters only a Top-25 pool.
  - Neither was suppressed by shrinkage. Equal weighting would rank them 30 and 17, so equal weights would admit neither into a Top-15 either.
  - Their exclusion reflects which families carry weight (B and D only). No family has validated skill, so this is neither "genuine evidence" nor an arbitrary error: it is noise.
- **Two layers:** discovery loss 2 (23, 35); construction loss 0 (all four available winners are on some ticket).
- **The four available winners were not concentrated.**
  - Only 55 pool tickets hold all four (exactly the random count); the best ranks 159th of 5,005.
  - Every pre-draw objective (standalone, concentration, hybrid) puts the top-ranked numbers together instead.
  - V1 already held 04 and 13, and the coverage term pushed the challengers elsewhere.
  - **Objective-alignment finding:** concentration would not have helped without knowledge of the winners. The real misalignment is in what the system claims and measures, and in forcing overlap.
- **Pool scoring:** V1 C04 scored 2/6 (it also carries bonus 38, which is not counted). The best candidates were C17 and C19 with 3/6. Jev's favourite was C04 (2/6). Distribution: {f4p['summary']['match_distribution']}. No candidate reached ≥4.

## Documents
- OBJECTIVE_AUDIT.md: A2, A3, A4, A5, A9 and the rational policy.
- METRIC_AUDIT.md
- STATISTICAL_AUDIT.md: A6, A7, A8, A11, A14, A15, A16, A18, A21.
- DATA_AUDIT.md
- CODE_AUDIT.md: A10, A20.
- JEV_AUDIT.md
- REQUIREMENT_MATRIX.md
- AUDIT_FINDINGS.json
- RESEARCH_REGISTRY.json
- `data/` (all computations)
- Scripts: `scripts/research/audit_2344_*.py` and `forensic_2343.py`.
""")
print('written')
