"""Build results/lotto/forensic_2341/REPORT.md (and historical_coverage.json) from the forensic outputs."""
import sys,json,math
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'));sys.path.insert(0,str(R/'scripts/research'))
import analyze as a
import v1_history as H
O=R/'results/lotto/forensic_2341';J=lambda n:json.loads((O/n).read_text())
v=J('verification.json');p=J('pool_scores.json');n=J('number_evidence.json');rc=J('recurring_core.json');ss=J('seed_sensitivity.json');t3=J('three_match.json')
FAM=['A_long','B_recent','C_gap','D_trend','E_pairs']
# historical Top-N capture context (targets 2211-2340, validated reconstruction; forensic context only)
records,d=H.load(R/'results/lotto/draw2341/draws.json');cache=H.walk_cache(d,records)
NS=[5,7,10,12,15,20,25];hist={}
for c in range(49,len(records)-1):
    s=H.state_at_cutoff(d,records,cache,c,with_gate=False);win=set(records[c+1]['numbers'])
    rk={f:s['family_scores'][j] for j,f in enumerate(FAM)};rk['G_marginal_proxy']=s['g_proxy'];rk['H_random']=np.random.default_rng(a.SEED+s['target']*3037).random(38)
    for f,sc in rk.items():
        if np.std(sc)<1e-12:continue
        o=np.argsort(-(sc+np.random.default_rng(a.SEED+s['target']).random(38)*1e-10))+1
        h=hist.setdefault(f,{N:[] for N in NS})
        for N in NS:h[N].append(len(set(o[:N].tolist())&win))
hc={f:{N:dict(n=len(v_),mean=float(np.mean(v_)),expected=6*N/38,all6=int(sum(x==6 for x in v_)),expected_all6=len(v_)*math.comb(N,6)/math.comb(38,6) if N>=6 else 0.) for N,v_ in h.items()} for f,h in hist.items()}
a.OUT=O;a.save('historical_coverage.json',dict(targets='2211-2340',note='Forensic context from the validated V1 reconstruction; V1 jitter tie-break; not used for any P0 decision.',coverage=hc))
S=p['summary'];ps=ss['production_seed'];f=ss['fixed_seed_designs'];pd=ss['per_draw_seed_designs']
def t(n_):return ' · '.join(f'{x:02}' for x in n_)
L=[]
L.append('# Lotto #2341 forensic\n')
L.append('Actual #2341: **01 · 04 · 06 · 22 · 33 · 38** (bonus 34, not scored). Frozen V1 Science ticket: **01 · 04 · 13 · 14 · 24 · 38** (C04, B_recent, seeded no-edge fallback), **3/6** (01, 04, 38).\n')
L.append('## 1. Frozen record verification\n')
L.append(f"All checks pass: **{v['ALL_CHECKS_PASS']}**. 17/17 embedded hashes and 8/8 pre-Jev pool hashes match exactly; the ledger hash of `frozen.json` matches; the Jev receipt's state and request hashes match the saved files; V1 code and data are unchanged since the Codex snapshot.\n")
ch=v['commit_chronology'];ts=v['timestamps_utc']
L.append(f"Chronology (UTC): pool frozen {ts['pool_frozen'][:19]} and committed `{ch['results/lotto/draw2341/candidates.json']}`; Jev receipt {ts['jev_receipt'][:19]}; ticket frozen {ts['ticket_frozen'][:19]}, committed `{ch['results/lotto/draw2341/frozen.json']}`, pushed 01:15:55. Scheduled draw 01:25:00 (8:25 PM Jamaica). The freeze script itself asserted `now < 01:25Z`. **The ticket was frozen before the draw.**\n")
L.append('## 2. Whole #2341 candidate pool\n')
L.append('| ID | Numbers | Generator | Eligible | Matches | Matched | Jev Choice | Jev rank | Sens. top-quartile | Ensemble rank |\n|---|---|---|---|---|---|---|---|---|---|')
for c in p['candidates']:
    jr=c['jev_rank'];jrs='—' if jr is None else (str(jr['best']) if jr['best']==jr['worst'] else f"{jr['best']}–{jr['worst']}")
    L.append(f"| {c['id']} | {t(c['numbers'])} | {c['generator']} | {'yes' if c['eligible'] else 'no'} | {c['matches']} | {' '.join(f'{x:02}' for x in c['matched']) or '—'} | {'—' if c['jev_choice_probability'] is None else c['jev_choice_probability']} | {jrs} | {c['sensitivity']['top_quartile_fraction']:.2f} | {c['model_evidence']['ensemble_rank']} |")
md=S['match_distribution']
L.append(f"\nMatch distribution (20 candidates): 0:{md['0']} · 1:{md['1']} · 2:{md['2']} · 3:{md['3']} · 4+:0. Best: **{', '.join(S['best_candidates'])}** (3/6), which is also the V1 selection and the Jev preference (Choice 0.92). No candidate exceeded 3/6. For 20 independent random tickets, P(at least one ≥3) = {S['random_reference']['p_at_least_one_ge3_of_20_independent']:.2f} and P(at least one ≥4) = {S['random_reference']['p_at_least_one_ge4_of_20_independent']:.3f}, so the pool result is ordinary. Jev Choice vs matches across the 16 eligible candidates: Spearman {S['jev_choice_vs_matches_spearman_eligible']:.2f}. No candidate is promoted retrospectively.\n")
L.append('## 3. Exact pre-draw number evidence (cutoff #2340)\n')
L.append('Ranks from the frozen `refreshed_rankings.json` (V1 jitter tie-break); `[a–b]` = tie interval. E_pairs was **flat** (0 Holm-retained pairs), so its ranks are arbitrary (tie interval 1–38). F_structure has no number-level ranking. H = V1 walk H ranking for target 2341.\n')
L.append('| No. | Role | A_long | B_recent | C_gap | D_trend | E_pairs | G proxy | H | Family top-12 | Freq | Last 30 | Gap | Trend |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for x,e in n['numbers'].items():
    def r(m):
        z=e['models'][m];ti=z['tie_interval'];return f"{z['rank']}"+('' if ti[0]==ti[1] else f" [{ti[0]}–{ti[1]}]")
    fe=e['features']
    L.append(f"| {int(x):02} | {e['role'].replace('_',' ')} | {r('A_long')} | {r('B_recent')} | {r('C_gap')} | {r('D_trend')} | flat | {r('G_marginal_proxy')} | {r('H_random')} | {', '.join(e['family_top12_support']) or '—'} | {fe['frequency']} | {fe['last_30_count']} | {fe['current_gap']} | {float(fe['trend_20_vs_previous40']):+.3f} |")
L.append('\nWinner coverage (point value [tie range]; random expectation 6N/38). Historical mean capture over 130 targets (2211–2340) in brackets after the slash.\n')
L.append('| Model | '+' | '.join(f'Top {N}' for N in NS)+' |\n|---|'+'---|'*len(NS))
for m,cv in n['coverage'].items():
    L.append(f"| {m} | "+' | '.join(f"{cv[str(N)]['point']}"+('' if cv[str(N)]['min']==cv[str(N)]['max'] else f" [{cv[str(N)]['min']}–{cv[str(N)]['max']}]")+f" / {hc[m][N]['mean']:.2f}" for N in NS)+' |')
L.append('| random expectation | '+' | '.join(f'{6*N/38:.2f}' for N in NS)+' |')
a20=hc['A_long'][20];g20=hc['G_marginal_proxy'][20];h20=hc['H_random'][20]
L.append(f"\nA_long and the G proxy put all six #2341 winners in their Top 20 (one-draw hypergeometric p = 0.014). Over the 130 historical targets, all six fell in the Top 20 for A_long {a20['all6']} times, G proxy {g20['all6']} times and the H random control {h20['all6']} times, against {a20['expected_all6']:.1f} expected by chance, and the historical mean Top-20 capture was A {a20['mean']:.2f}, G {g20['mean']:.2f}, H {h20['mean']:.2f} vs 3.16 expected. #2341's broad capture is a single-draw observation, not a validated discovery property.\n")
L.append('## 4. Recurring core (01, 04, 13, 24, 38)\n')
L.append('| No. | #2339 ranks A/B/C/D/G | #2340 | #2341 | Long-run top-10 rate A / B / D / G | Mean candidates containing it | In V1 final (2339/2340/2341) | In Jev preferred |\n|---|---|---|---|---|---|---|---|')
for x in ['1','4','13','24','38']:
    rr=[rc['recent_runs'][tt]['core'][x] for tt in ['2339','2340','2341']]
    def rs(c):return '/'.join(str(c['ranks'].get(m,'–')) for m in ['A_long','B_recent','C_gap','D_trend','G_marginal_proxy'])
    lr=rc['long_run'][x]['top_rate']
    L.append(f"| {int(x):02} | {rs(rr[0])} | {rs(rr[1])} | {rs(rr[2])} | {lr['A_long']['10']:.2f} / {lr['B_recent']['10']:.2f} / {lr['D_trend']['10']:.2f} / {lr['G_marginal_proxy']['10']:.2f} | {rc['long_run'][x]['mean_candidates_containing']:.2f} | {'/'.join('Y' if c['in_v1_final'] else 'n' for c in rr)} | {'/'.join('Y' if c['in_jev_preferred'] else 'n' for c in rr)} |")
co=rc['construction'];im=rc['fixed_seed_index_map']['map']
L.append(f"""
Top-10 base rate is 10/38 = 0.26. Family score correlations across all cutoffs: A~B {rc['family_score_correlations']['A_long~B_recent']['mean']:.2f}, B~D {rc['family_score_correlations']['B_recent~D_trend']['mean']:.2f}, A~D {rc['family_score_correlations']['A_long~D_trend']['mean']:.2f}, B~C {rc['family_score_correlations']['B_recent~C_gap']['mean']:.2f}: A, B and D are not independent confirmations.

**Decomposition**
- **A. Model-family support (real but correlated, not predictive evidence):** 01, 24, 38 (and 33) are among the most frequent numbers in the whole history, so the cumulative A_long ranks them top-10 most of the time (24: 83%, 01: 69%). 04 and 13 are recently hot: B_recent/D_trend rank them near the top, while A_long almost never ranks 13 top-10 (2%). "Agreement" between A, B and D is largely shared information.
- **B. Candidate-construction mechanics:** every V1 run searches the same fixed 4,096-combination pool (seed SEED+999) and the H fill uses a fixed seed (SEED+555), so on average {co['mean_identical_candidate_tickets_between_consecutive_cutoffs']:.1f} of the 20 candidates are identical between consecutive cutoffs; {co['tickets_reappearing_in_10plus_pools']} tickets appear in 10+ of the 131 reconstructed pools. The H fill ticket 05·07·14·21·33·38 is in all 131 pools; with E_pairs flat, its "top" tickets are the pool's first entries and repeat too. The fixed pool is not itself enriched for the core ({co['share_of_pool_with_3plus_of_1_4_13_24']:.4f} of pool tickets hold 3+ of 01/04/13/24 vs {co['same_for_random_4sets_mean']:.4f} for random 4-sets).
- **C. Fixed-seed mechanics (the main driver of the FINAL ticket):** V1 creates a fresh `default_rng(20260919)` every run, so the fallback index depends only on the number of eligible candidates n: n=13–16 → index 3, n=17–20 → index 4. Candidates are ordered by generator (C01–C03 A_long, C04–C06 B_recent, C07–C09 C_gap, …), so whenever the first candidates are eligible, V1 lands on a **B_recent** slot: #2339 C05 (index 4 of 20) and #2341 C04 (index 3 of 16) are the **same ticket**. Replayed over 131 historical cutoffs, the production chain used only {ps['distinct_ids']} distinct candidate IDs, B_recent {ps['generator_shares'].get('B_recent',0):.0%} of the time (uniform ≈15%).
- **D. Overlap constraint:** the ≤2-overlap rule excluded 4 candidates in #2340 (including every candidate holding 3+ of 01/04/13/14/24/38), shifting index 3 onto C07 (C_gap); in #2341 it excluded the C_gap tickets C07–C09 and C18 instead, returning index 3 to C04. Together with C this creates an alternating cycle (ticket X, excluded next draw, back two draws later).
- **E. Generator behaviour:** B_recent's top-ranked ticket is stable across cutoffs because its features (last-30 and EW frequency) move slowly; 04, 13 and 24 are in B_recent's top 10 in all three runs (24 is its rank 1 each time).
- **F. Jev:** no causal role. Under the no-edge fallback Jev never affects the selection. Jev preferred C02 in #2339 and #2340 and C04 in #2341.
""")
L.append('## 5. Fixed-seed sensitivity (research only; production seed unchanged)\n')
L.append('| Metric | Production 20260919 | 1,000 fixed seeds (mean [5–95%]) | Per-draw seeds seed+draw_id (mean [5–95%]) |\n|---|---|---|---|')
for k,lab in [('distinct_ids','distinct candidate IDs (131 draws)'),('same_id_consecutive','same ID on consecutive draws'),('top_id_share','share of most-used ID'),('exact_ticket_repeat_lag2','exact ticket repeat 2 draws later'),('mean_consecutive_overlap','mean overlap with previous ticket'),('max_number_selection_rate','max selection rate of any number'),('mean_matches','mean matches'),('sd_matches','SD of matches'),('ge3','3+ results (count)')]:
    L.append(f"| {lab} | {ps[k]:.3f} | {f[k]['mean']:.3f} [{f[k]['p05']:.3f}–{f[k]['p95']:.3f}] | {pd[k]['mean']:.3f} [{pd[k]['p05']:.3f}–{pd[k]['p95']:.3f}] |")
L.append(f"\nWithout the overlap rule, every fixed seed picks the **same candidate ID at every draw** (100%). **Yes, the fixed-seed fallback mechanically revisits the same region of candidate space**: the cause is the design (a fresh generator with the same seed each run makes the pick a deterministic function of n), not the particular seed value; the production seed is typical among fixed seeds (percentiles {', '.join(f'{k} {v:.2f}' for k,v in ss['production_percentile_among_1000_fixed_seeds'].items() if k in ('distinct_ids','exact_ticket_repeat_lag2','mean_matches'))}). Realized matches do not differ between designs (fixed {f['mean_matches']['mean']:.3f}, per-draw {pd['mean_matches']['mean']:.3f}, random 0.947), so no seed choice is supported; any change would need a predeclared prospective test. G_ensemble passed the V1 gate at four very early cutoffs (targets {', '.join(map(str,ss['qualified_targets_flagged']))}, three computed on short histories); those origins are flagged.\n")
pr=t3['prospective_v1']['primary'];ws=t3['prospective_v1']['including_2339_secondary']
L.append('## 6. Three-match forensic\n')
L.append(f"Random ticket: P(exactly 3) = {t3['p_exactly_3']:.5f} (1 in {1/t3['p_exactly_3']:.1f}); P(≥3) = {t3['p_at_least_3']:.5f}; P(≥4) = {t3['p_at_least_4']:.5f}.\n")
L.append(f"Prospective V1 primary tickets: #2339 3, #2340 0, #2341 3 (n=3, total 6, mean 2.0 vs 0.947). Exact P(total ≥6) = {pr['p_total_ge_observed']:.3f}; P(two or more 3+ results in 3) = {pr['p_ge3_events_ge2']:.4f}; 3+ rate 2/3 with Clopper–Pearson 95% CI [{pr['ge3_rate_clopper_pearson95'][0]:.2f}, {pr['ge3_rate_clopper_pearson95'][1]:.2f}]. Including the #2339 secondary (1 match): P(total ≥7 in 4) = {ws['p_total_ge_observed']:.3f}.\n")
L.append("These are uncorrected and **do not establish an edge**: (i) n=3 with an interval spanning almost everything; (ii) #2339 and #2341 are the **same ticket** re-selected by the fixed-seed mechanism, so this is one combination hitting twice, not two method successes; (iii) the question is asked because 3/6 happened, and the ledger tracks many tickets per draw; (iv) over the 131-draw historical replay the same V1 fallback chain averaged "+f"{ps['mean_matches']:.3f} matches with {ps['ge3']} results of 3+ ({ps['ge3']/131:.1%} vs 3.9% expected), i.e. no excess where the sample is larger. The cumulative prospective record does not materially depart from random expectation once these points are considered.\n")
L.append('## 7. Conclusion\n')
L.append("""- **Number discovery:** broad but unvalidated. A_long/G put all six winners in their Top 20 and A_long 4 in its Top 12, but historical capture is near random and the H control also reached 5/6 in its Top 20. E_pairs was flat.
- **Candidate construction:** heavily persistent (fixed search pool, fixed H fill, flat E_pairs fallback), so the candidate set changes little between draws. The best candidate (3/6) was in the pool; no candidate reached 4.
- **Final selection:** the seeded no-edge fallback is not uniform over time; with a fresh fixed-seed generator it repeatedly lands on B_recent slots, which produced the same ticket in #2339 and #2341. The 3/6 is consistent with chance.
- **Jev:** preferred the selected ticket (0.92) but had no causal role; its Choice is unrelated to outcomes across the pool (Spearman 0.06, n=16).
- **Recurring core:** long-run frequency (01, 24, 38) and recent frequency (04, 13) surfaced by correlated models, then locked in by construction persistence, the fixed-seed index and the overlap alternation. Recurrence is not predictive evidence.
- **Fixed seed:** a real mechanical artefact of the fallback design, with no measurable effect on realized matches.

**Does #2341 alone justify changing V1? NO.** No corrected historical evidence supports a change. The fixed-seed artefact is documented for a possible future predeclared V1 revision, but it does not affect expected performance and is not changed here.
""")
(O/'REPORT.md').write_text('\n'.join(L),encoding='utf-8');print('written',len(L))
