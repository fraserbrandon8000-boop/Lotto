"""Write results/super_lotto/forensic_1756/REPORT.md and p1_research/REPORT.md from saved JSON (no computation of new evidence)."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[2];V=R/'results/super_lotto';O=V/'forensic_1756';PR=V/'p1_research'
J=lambda p:json.loads(Path(p).read_text())
ver=J(O/'verification.json');ps=J(O/'pool_scores.json');de=J(O/'discovery_evidence.json');cs=J(O/'consecutive_discovery.json');n15=J(O/'number_15_trace.json')
ly=J(O/'layer_separation.json');sb=J(O/'super_ball_forensic.json');jv=J(O/'jev_stability.json');rec=J(O/'prospective_record.json')
rc=J(PR/'research_challengers.json');cc=J(PR/'construction_conditional.json');s10=J(PR/'sl10_fixed_slot.json');r=rc['refinements']
f2=lambda x:f'{x:.2f}';f3=lambda x:f'{x:.3f}';nn=lambda l:' · '.join(f'{x:02}' for x in l)
KS=[8,10,12,15,18,20,25]
L=[]
A=L.append
A('# Super Lotto #1756 forensic\n')
A('Actual #1756: **05 · 07 · 15 · 29 · 32 + SB3**.\n')
A('| Frozen ticket | Result |\n|---|---|\n| V1 Science 01 · 06 · 11 · 18 · 22 + SB2 | 0/5, SB miss |\n| P0 Coverage 1 02 · 09 · 12 · 23 · 24 + SB7 | 0/5, SB miss |\n| P0 Coverage 2 01 · 12 · 17 · 18 · 29 + SB3 | 1/5 (29), **SB3 hit** |\n')
c=ver['chronology_utc'];cm=ver['commits']
A(f"## 1. Frozen record\n\nAll checks pass: **{ver['ALL_PASS']}**. Pre-Jev pool freeze hashes all {'/'.join(sorted(set(ver['candidate_freeze'].values())))}; `prediction_1756.json` embedded hashes {ver['prediction_embedded']}; P0 freeze hashes all exact; all {len(ver['HASHES_sha256_file'])} other entries of `draw1756/HASHES.sha256` exact; the ledger at the #1756 freeze is an exact prefix of today's ledger (append-only). Jev receipt: state, request (compact), response all match; one HTTP attempt, retries disabled. Offline validation: inclusive 0.03 Score boundary on SL08/SL09 stability (no response edit, no retry). The 5 replicate Jev calls used byte-identical request bytes and all ran after the ticket freeze. Ticket files are unchanged since the freeze commit.\n")
A(f"Chronology (UTC): pool frozen {c['pool_frozen'][:19]} (commit `{cm['pool']}`) → Jev {c['jev_attempt'][:19]} → V1 frozen {c['v1_frozen'][:19]} → P0 frozen {c['p0_frozen'][:19]} (commit `{cm['tickets']}`) → post-freeze audit, replicates, random control (commit `{cm['post_freeze']}`) → draw 2026-10-03T01:30. **All three tickets were frozen about 8 hours before the draw.** Random control (seed {ver['random_control']['seed']}): " + ' / '.join(f"{nn(t['mains'])} + SB{t['super_ball']}" for t in ver['random_control']['tickets'])+'.\n')
A('## 2. Whole V1 candidate pool (scored after the draw; nothing promoted)\n')
A('| ID | Mains | SB | Generator | Matches | Matched | SB3 | Prod. Jev Choice | Prod. rank | Replicate mean rank | Sens. range | Agreement | Ensemble |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for x in ps['candidates']:
    jr=x['jev_rank_production'];A(f"| {x['id']} | {nn(x['main'])} | {x['super_ball']} | {x['generator']} | {x['main_matches']} | {' '.join(f'{m:02}' for m in x['matched']) or '—'} | {'yes' if x['sb_hit'] else 'no'} | {x['jev_choice_production']} | {jr['best'] if jr['best']==jr['worst'] else str(jr['best'])+'–'+str(jr['worst'])} | {x['jev_replicate_mean_midrank']:.1f} | {x['sensitivity']['rank_range'][0]}–{x['sensitivity']['rank_range'][1]} | {x['evidence']['model_agreement']} | {x['evidence']['ensemble_score']:.2f} |")
s=ps['summary']
A(f"\nMain matches {' · '.join(f'{k}:{v}' for k,v in s['main_match_distribution'].items())}. Best: {', '.join(s['best_candidates'])} ({s['best']}/5). V1 selected SL10: {s['v1_matches']}/5. Production Jev favourite {s['production_jev_favourite']} (0/5); five-replicate favourite {s['replicate_favourite']} (0/5). Candidates carrying SB3: {', '.join(s['candidates_with_SB3'])}; **SL14 (05 32 + SB3) and SL16 (07 29 + SB3) paired two mains with SB3**; both had production Choice ≤ 0.02. Reached ≥2: yes (3 candidates; random expectation {s['random_reference']['expected_candidates_ge2']:.2f}); ≥3: none. Jev Choice vs matches Spearman {s['jev_choice_vs_matches_spearman']:.2f}. E_pairs ranks are flat (no Holm-retained pair), so E_pairs candidates are effectively unranked.\n")
A('## 3. Pre-draw evidence for the #1756 winners (cutoff #1755)\n')
A('Every P0 credibility was 0, so the P0 order is the declared equal-weight average of the informative A–D z-scores (E_pairs flat; F has no number score). Model reliability contribution = credibility × score = 0 for every family.\n')
A('| Winner | A_long | B_recent | C_gap | D_trend | E_pairs (flat) | G_ensemble | H (control) | EQ z | **P0 rank** | Count (exp 25.6) | Last 30 | EW rate | Gap (pct) | Trend | Max pair lift (Holm-retained) |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
def mr(m):
    if m.get('rank') is None:return '—'
    t=m['tie'];return f"{m['rank']}" if t[0]==t[1] else f"{m['rank']} [{t[0]}–{t[1]}]"
for n,w in de['winners'].items():
    f=w['features'];M=w['models'];pn=w['pair_network']
    A(f"| {int(n):02} | {mr(M['A_long'])} | {mr(M['B_recent'])} | {mr(M['C_gap'])} | {mr(M['D_trend'])} | {mr(M['E_pairs'])} | {mr(M['G_ensemble'])} | {mr(M['H_random'])} | {w['P0_EQ']:+.3f} | **{w['P0_rank']}** | {f['long_run_count']} | {f['last30']} | {f['ew_rate']:.3f} | {f['current_gap']} ({f['gap_percentile']:.2f}) | {f['trend']:+.3f} | {pn['max_lift']:.2f} ({pn['holm_retained']}) |")
A('\n| Missed winner | A. P0 rank | B. Best model | C. Worst model | D. Disagreement (spread ≥15) | E. Zero/weak credibility weighting suppressed useful support? | F. Top 15 | G. Top 18 | H. Top 20 | I. Top 25 |\n|---|---|---|---|---|---|---|---|---|---|')
for n in ['5','7','15','32']:
    a=de['winners'][n]['answers'];yn=lambda b:'yes' if b else 'no'
    A(f"| {int(n):02} | {a['A_P0_rank']} | {a['B_best_model']} {a['B_best_model_rank']} | {a['C_worst_model']} {a['C_worst_model_rank']} | {yn(a['D_substantial_disagreement'])} ({a['rank_spread']}) | {'no — a single unvalidated model had it in its Top 12 and equal-weight averaging pushed it out' if a['E_zero_weighting_suppressed']['answer'] else 'no — no informative model had it in its Top 12'} | {yn(a['F_top15'])} | {yn(a['G_top18'])} | {yn(a['H_top20'])} | {yn(a['I_top25'])} |")
A("""
- **05** (P0 24): no informative model had it in a Top 12 (best A_long/B_recent 15). Nothing to suppress.
- **07** (P0 14): **C_gap's #1** (19-draw absence, most overdue), but B_recent ranked it 34th and D_trend 27th. Equal-weight averaging put it at 14. Same pattern as 33 in #1755: C_gap is anti-correlated with B/D, so its top pick is averaged away. Over 105 causal origins C_gap alone has no corrected skill (full-period AP excess p = %s), so this is not a suppressed validated signal.
- **15** (P0 13): D_trend 7, B_recent 8, but C_gap 31 (it had just been drawn). Missed the pool by one place.
- **32** (P0 17): C_gap 9 was its only Top-12 support.
- **E (zero weighting):** the zero credibilities did not hide a validated model. The unshrunk, lightly shrunk and Bayesian reliability weightings each capture *fewer* or equal #1756 winners in their Top 12 (1, 1, 1) than the frozen order (1). The only single orderings with 2 in their Top 12 were D_trend, C_gap (E_gap), K_best_trailing, LOFO-minus-B and the **random control** (2).
""" % f3(r['order:E_gap:AP']['full']['p']))
A('Top-N winners captured for #1756 by each pre-draw ordering:\n\n| Ordering | '+' | '.join(f'Top {K}' for K in KS)+' |\n|---|'+'---|'*len(KS))
for m,v in de['topN_1756'].items():A(f"| {m} | "+' | '.join(str(v[str(K)]) for K in KS)+' |')
A('| random expectation 5N/35 | '+' | '.join(f2(5*K/35) for K in KS)+' |\n')
s1=cs['single_draw'];s2=cs['two_draws']
A(f"""## 4. Two consecutive discovery misses: exact random baseline

Top-12 pool from 35, 5 winners: X ~ Hypergeometric(35, 5, 12).

| One draw | Value |
|---|---|
| expected winners captured | {s1['expected']:.4f} |
| P(0) | {s1['p0']:.4f} |
| P(1) | {s1['p1']:.4f} |
| P(≤1) | {s1['p_le1']:.4f} |
| P(≥2) | {s1['p_ge2']:.4f} |
| P(≥3) | {s1['p_ge3']:.4f} |
| P(all 5) | {s1['p_all5']:.5f} |

| Two independent draws | Value |
|---|---|
| expected total captured (of 10) | {s2['expected_total']:.4f} |
| observed | 2 |
| P(total ≤ 2) | **{s2['p_total_le2']:.4f}** |
| P(total ≤ 1) | {s2['p_total_lt2']:.4f} |
| P(≤1 in both draws) | {s2['p_le1_both']:.4f} |
| percentile of 2/10 (P(<2) + ½P(=2)) | {s2['percentile_mid']:.3f} (≈ {100*s2['percentile_mid']:.0f}th percentile) |

Historical P0 Top-12 capture (105 causal origins): mean {cs['historical_P0_top12_capture']['mean']:.3f}, ≤1 in {100*cs['historical_P0_top12_capture']['p_le1']:.0f}% of draws; two consecutive draws totalling ≤2 in {100*cs['historical_P0_top12_capture']['consecutive_pairs_total_le2']:.0f}% of consecutive pairs.

**Verdict: mildly unusual at most (about 1 in 4 random Top-12 pools do this badly or worse over two draws). Not statistically concerning, and fully compatible with chance.** Two observations carry almost no information.
""")
A('## 5. Strict causal walk-forward: P0 order by pool size (targets %d–%d, n = %d; confirmation %d–%d)\n'%(rc['targets'][0],rc['targets'][1],rc['n_targets'],rc['confirmation_targets'][0],rc['confirmation_targets'][1]))
A('Excess is measured against the exact random capture 5N/35, which removes the mechanical advantage of larger pools. ≥k coverage is shown observed / random. Holm across the whole family of %d variants.\n'%rc['family_size'])
A('| Pool | Mean captured | Random | Excess | ≥1 | ≥2 | ≥3 | ≥4 | 5/5 | Development | Confirmation | Halves (std excess, full) | Block 95% (std, full) | raw p (full) | raw p (conf) | Holm p |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for K in KS:
    v=r[f'order:F_P0_frozen_protocol:top{K}'];f=v['full'];cf=v['confirmation'];g=f['ge'];gn=cf['ge_null']
    A(f"| Top {K} | {f['mean']:.3f} | {f['expected']:.3f} | {f['excess']:+.3f} | "+' | '.join(f"{g[str(k)]:.2f} / {gn[str(k)]:.2f}" for k in range(1,6))+f" | {v['development']['mean']:.3f} | {cf['mean']:.3f} | {f['halves_std_excess'][0]:+.2f} / {f['halves_std_excess'][1]:+.2f} | [{f['block95_std_excess'][0]:+.2f}, {f['block95_std_excess'][1]:+.2f}] | {f['p']:.3f} | {cf['p']:.3f} | {cf['holm_p']:.2f} |")
A('\nAt every size the P0 order captures winners at the rate its size implies. Larger pools capture more winners only mechanically. **Top 12 is not shown to be too narrow, and no other size is better.** The production pool is not widened.\n')
A('## 6. Does P0 rank winners better than a random ordering?\n')
A('Every method is computed causally at each origin. AP = average precision of the full 35-number ordering against the 5 winners (exact random mean %.4f).\n'%r['order:A_random:AP']['full']['expected'])
A('| Method | Top 8 | Top 10 | Top 12 | Top 15 | Top 18 | Top 20 | Top 25 | AP excess (full) | AP p (full) | Top-12 p (full) | Top-12 conf mean |\n|---|---|---|---|---|---|---|---|---|---|---|---|')
lab={'A_random':'A. random ranking (explicit null)','B_long':'B. long-run frequency','C_recent':'C. recent frequency','D_trend':'D. trend','E_gap':'E. gap','F_P0_frozen_protocol':'F. frozen P0 ordering','G_equal_weight':'G. equal weight','H_unshrunk_reliability':'H. unshrunk reliability','I_light_shrinkage':'I. lightly shrunk (unadjusted p)','L_bayes_empirical':'regularized (empirical Bayes)','J_lofo_minus_A':'J. leave out A_long','J_lofo_minus_B':'J. leave out B_recent','J_lofo_minus_C':'J. leave out C_gap','J_lofo_minus_D':'J. leave out D_trend','K_best_trailing_model':'K. best trailing-30 model','M_family_vote_borda':'family vote (Borda)'}
for m,lb in lab.items():
    A(f"| {lb} | "+' | '.join(f"{r[f'order:{m}:top{K}']['full']['excess']:+.3f}" for K in KS)+f" | {r[f'order:{m}:AP']['full']['excess']:+.4f} | {r[f'order:{m}:AP']['full']['p']:.3f} | {r[f'order:{m}:top12']['full']['p']:.3f} | {r[f'order:{m}:top12']['confirmation']['mean']:.3f} |")
A(f"""
(Cells are mean excess winners captured over random, full period.) No P0 credibility was ever non-zero at any origin, so F and G are identical by construction.

The frozen P0 ordering's AP excess is {r['order:F_P0_frozen_protocol:AP']['full']['excess']:+.4f} (p = {r['order:F_P0_frozen_protocol:AP']['full']['p']:.2f}); its Top-12 capture is {r['order:F_P0_frozen_protocol:top12']['full']['mean']:.3f} against 1.714 random (p = {r['order:F_P0_frozen_protocol:top12']['full']['p']:.2f}). No method beats random after correction. Note the **explicit random control itself reached raw p = {r['order:A_random:top12']['full']['p']:.3f} at Top 12** over the full period. That is what noise looks like in a family this size, and it is why only the corrected gate counts.

**THE CURRENT P0 MAIN-NUMBER DISCOVERY ORDER HAS NO DEMONSTRATED PREDICTIVE VALUE.**
""")
t5,t6=n15['run_1755'],n15['run_1756']
A('## 7. Number 15 (won #1755 and #1756)\n\n| Model | #1755 run rank | #1756 run rank |\n|---|---|---|')
for m in t5['models']:A(f"| {m} | {t5['models'][m].get('rank','—') if t5['models'][m].get('rank') is not None else '—'} | {t6['models'][m].get('rank') if t6['models'][m].get('rank') is not None else '—'} |")
A(f"| **P0 rank** | **{t5['P0_rank']}** | **{t6['P0_rank']}** |\n| V1 candidates containing 15 | {t5['candidate_frequency']} | {t6['candidate_frequency']} ({', '.join(t6['candidates'])}) |\n")
A('Feature movement #1755 run → #1756 run: '+'; '.join(f"{k} {float(a):.3g} → {float(b):.3g}" for k,(a,b) in n15['movement_1755_to_1756'].items())+'.\n')
h=n15['historical_P0_rank_of_15'];rr=n15['random_recurrence']
A(f"Before #1755, 15 was mid-table everywhere (ranks 18–22). After winning #1755, B_recent and D_trend moved it to 8 and 7, while C_gap dropped it to 31 (just drawn). The average put it at 13, one place outside the pool. Historically its P0 rank averaged {h['mean']:.1f} (Top 12 in {100*h['in_top12_share']:.0f}% of origins, expected 34%); it has won {n15['historical_15_wins']} of {n15['draws']} draws (expected {n15['draws']/7:.1f}). A specific number repeats with probability 5/35 = 0.143. At least one number repeats between consecutive draws with probability {rr['p_any_number_repeats_next_draw']:.3f} (historically {rr['historical_any_repeat_rate']:.3f}). **15 was not systematically under-ranked; its repeat is ordinary random recurrence. No repeat rule is created.** In the frozen #1757 run, unchanged V1/P0 rank 15 at P0 position {n15['post_result_1757_state']['P0_rank']}, inside the pool, purely from its updated recent-frequency/trend features, not from any rule.\n")
A(f"""## 8. Discovery vs construction

**#1756:** winners available to the constructor: **{ly['winners_available_to_constructor']}** ({', '.join(f'{x:02}' for x in ly['available'])}); absent before construction: **{ly['absent_before_construction']}** ({', '.join(f'{x:02}' for x in ly['absent'])}); available but not placed: **{len(ly['available_not_placed'])}**; placed on playable tickets: **{', '.join(f'{x:02}' for x in ly['placed_on_playable_tickets'])}**.

**Historical conditional analysis** (frozen constructor replayed causally at every origin, K = 12, rule C; reproduces the frozen historical P0 portfolios exactly, mismatches {cc['historical_replay_mismatch_targets']}):

| Winners in pool (K) | Draws | Share (random) | Mean best-ticket matches | Mean total portfolio matches | Mean unique winners covered | Challenger in-pool captures | Blind expectation |
|---|---|---|---|---|---|---|---|""")
for k,v in cc['by_K_in_pool'].items():
    A(f"| {k} | {v['n']} | {cc['observed_K_distribution'][k]:.2f} ({cc['random_K_distribution'][k]:.2f}) | {v['mean_best']:.2f} | {v['mean_total']:.2f} | {v['mean_unique']:.2f} | {v['challengers_inpool_captured']:.2f} | {v['blind_expectation']:.2f} |")
A(f"""
The challengers captured {cc['captured_by_challengers']} of {cc['total_in_pool']} in-pool winners ({100*cc['ratio']:.0f}%), against {cc['blind_expected']:.1f} ({100*cc['blind_expected']/cc['total_in_pool']:.0f}%) expected from the share of the pool they cover. Best-ticket matches track K closely (correlation {cc['corr_K_vs_best']:.2f}). **The binding layer is DISCOVERY**: construction converts whatever reaches the pool, and discovery is at random level. Because discovery has no skill, a better constructor cannot create an edge either.
""")
A('## 9. Super Ball (actual SB3; played 2, 7, 3)\n\n| SB | S_long | S_recent | S_gap | S_trend | S_transition (flat) | S_ensemble | P0 rank |\n|---|---|---|---|---|---|---|---|')
for b in range(1,11):
    x=sb['all_sb_ranks'][str(b)];A(f"| {b}{' **(actual)**' if b==3 else ''} | {x['S_long']} | {x['S_recent']} | {x['S_gap']} | {x['S_trend']} | {x['S_transition']} | {x['S_ensemble']} | {sb['P0_sb_order'].index(b)+1} |")
cl=sb['combined_live']
A(f"""
SB3: S_long 5, **S_recent 1**, S_gap 8, **S_trend 2**, S_transition 4 (flat; tie 1–10), S_ensemble 8, **P0 SB rank 2**. All SB credibilities were 0, so the P0 SB order is the equal-weight average of the SB model z-scores (SB7 0.463, SB3 0.426). Rule C gave the two challengers the top two P0 SBs other than V1's SB2, which were SB7 and SB3.

**Driver: both.** SB3 reached rank 2 through unvalidated equal-weight model evidence (S_recent and S_trend), and rule C's diversification placed it. Historically the P0 SB Top-3 contains the winner {100*r['SB:P0_order_top3']['full']['mean']:.1f}% of the time vs 30% random (p = {r['SB:P0_order_top3']['full']['p']:.2f}), so in practice **the hit was essentially chance.**

Combined live P0 SB record: #1755 miss, #1756 hit. With 3 distinct SBs from 10 the hit rate is 0.30 per draw; P(≥1 hit in 2) = {cl['p_at_least_one_in_2']:.2f}, P(exactly 1) = {cl['p_exactly_one_in_2']:.2f}. 1/2 is the single most likely outcome. **No SB predictive skill is claimed.**
""")
sm=s10['mean_matches'];sr=s10['sb_hit_rate'];rc10=s10['recurrence']
A(f"""## 10. V1 fixed slot (SL10)

Under the no-edge rule V1 selects `default_rng(2026092109).integers(20)` = 9 every time, i.e. **SL10 (D_trend's top ticket with S_gap's SB) in 100% of no-edge runs** ({s10['targets_with_full_pool']} reconstructable origins; V1 never passed its gate).

| Selection rule | Mean main matches | SB hit rate | Consecutive main overlap | Identical consecutive tickets | SB repeats next draw | SB entropy (bits, max 3.32) |
|---|---|---|---|---|---|---|
| SL10 fixed slot | {sm['SL10']:.3f} | {sr['SL10']:.3f} | {rc10['SL10']['mean_consecutive_overlap']:.2f} | {rc10['SL10']['consecutive_identical']} | {100*rc10['SL10']['sb_repeat_rate']:.0f}% | {rc10['SL10']['sb_entropy_bits']:.2f} |
| per-draw seed | {sm['per_draw_seed']:.3f} | {sr['per_draw_seed']:.3f} | {rc10['per_draw_seed']['mean_consecutive_overlap']:.2f} | {rc10['per_draw_seed']['consecutive_identical']} | {100*rc10['per_draw_seed']['sb_repeat_rate']:.0f}% | {rc10['per_draw_seed']['sb_entropy_bits']:.2f} |
| rotating slot (target mod 20) | {sm['rotating_slot']:.3f} | {sr['rotating_slot']:.3f} | {rc10['rotating_slot']['mean_consecutive_overlap']:.2f} | {rc10['rotating_slot']['consecutive_identical']} | {100*rc10['rotating_slot']['sb_repeat_rate']:.0f}% | {rc10['rotating_slot']['sb_entropy_bits']:.2f} |
| uniform candidate (expectation) | {sm['uniform_candidate']:.3f} | — | — | — | — | — |
| random ticket | {sm['random']:.3f} | 0.100 | 0.71 | ≈0 | 10% | 3.32 |

SL10's mean ({sm['SL10']:.3f}) is below random and below the other slots, but the shortfall is within noise (one-sided p for excess {r['V1:SL10_fixed_slot']['full']['p']:.2f}; the lower-tail deviation is about 1.5 SD). Per-draw seeding's apparent gain (confirmation raw p {r['V1:per_draw_seed']['confirmation']['p']:.3f}) fails Holm (p = {r['V1:per_draw_seed']['confirmation']['holm_p']:.2f}) and its bootstrap lower bound is below 0.
**PREDICTIVE PERFORMANCE: no demonstrated harm or benefit. DIVERSITY / EXPERIMENT QUALITY: clearly harmed.** SL10 repeats {rc10['SL10']['mean_consecutive_overlap']:.1f} of 5 mains from one draw to the next (random 0.71), was identical in {rc10['SL10']['consecutive_identical']} consecutive pairs, and repeats its SB {100*rc10['SL10']['sb_repeat_rate']:.0f}% of the time. Live V1 has played SB2 in all four draws #1753–#1756. The prospective V1 record is therefore close to one repeated ticket, not independent samples. A non-fixed slot should be predeclared for a future V1 revision as an experiment-quality fix, not as a predictive claim. Production V1 is unchanged here.
""")
A('## 11. Jev top-1 stability (#1756)\n\n| Call | Top | Top Choice | SL10 Choice | SL19 Choice | Confidence | Entropy (bits) |\n|---|---|---|---|---|---|---|')
for i,cl_ in enumerate(jv['calls_1756']):A(f"| {cl_['run']} | {cl_['top']} | {cl_['top_prob']:.2f} | {jv['SL10_vs_SL19']['SL10']['choice'][i]:.2f} | {jv['SL10_vs_SL19']['SL19']['choice'][i]:.2f} | {cl_['confidence']:.2f} | {cl_['entropy_bits']:.2f} |")
ag=jv['aggregator_outcomes'];st=jv['stability_1757']
A(f"""
SL10 and SL19 midrank variance {jv['SL10_vs_SL19']['SL10']['rank_variance']:.2f} each (1↔2 swap); production gap SL10 − SL19 = {jv['production_gap_SL10_minus_SL19']:+.2f} (**near-tie**); mean pairwise top-3 overlap {jv['mean_pairwise_top3_overlap']:.2f}/3; overall Spearman 0.955 (min 0.924) as recorded in `jev_stability_1756`. The flip reflects a near-tie, not a change of overall view.

Aggregators on saved outcome sets (no new historical calls): #1755 first-valid / mean-Choice / median-rank / majority all SL04 (0/5); #1756 first-valid SL10 (0/5), mean / median / majority SL19 (0/5). n = 2 draws, so this cannot evaluate skill. In #1757 (post-freeze) production and all 5 replicates chose SL19 (0.80; mean Spearman {st['mean_pairwise_spearman']:.3f}). **Jev's first-response top-1 is stable when one candidate dominates and unstable in near-ties. Under the no-edge rule it never affects the ticket.**
""")
A(f"""## 12. Combined prospective record

| Draw | V1 | P0 challengers | Random control |
|---|---|---|---|
| #1753 | 1/5, SB miss | — | — |
| #1754 | 0/5, SB miss | shadow only | — |
| #1755 | 0/5, SB miss | 1/5 + 0/5, SB miss | 1 + 1 + 0, SB miss |
| #1756 | 0/5, SB miss | 0/5 + 1/5 (SB3 hit) | 0 + 0 + 1 (SB3 hit) |

V1: {rec['v1_total']} main matches in {rec['v1_tickets']} tickets (expected {rec['v1_expected']:.2f}; P(≤{rec['v1_total']}) = {rec['v1_p_le_obs']:.2f}); SB 0/4. P0 3-ticket portfolio (#1755–#1756): {rec['p0_portfolio']['total_main']} mains in {rec['p0_portfolio']['tickets']} tickets (expected {rec['p0_portfolio']['expected']:.2f}; P(≤2) = {rec['p0_portfolio']['p_le_obs']:.2f}); 1 SB hit. The fixed-seed random control: {rec['random_control']['total_main']} mains and 1 SB hit over the same two draws. **Everything is consistent with chance.**

## 13. Research family (see `p1_research/REPORT.md`)

{rc['family_size']} variants in one Holm family: 16 orderings × 7 pool sizes plus AP, dynamic pool size, 10 SB rules/orderings, and V1 selection variants (SL10, per-draw seed, rotating slot, broader candidate union, pool SB coverage). Smallest Holm p = {min(v['confirmation']['holm_p'] for v in r.values()):.2f}. **Passing: none. NO SUPER LOTTO V2/P1 REFINEMENT IS JUSTIFIED.** No P1 shadow ticket is produced.
""")
(O/'REPORT.md').write_text('\n'.join(L)+'\n')
# ---------------------------------------------------------------- p1_research REPORT
P_=['# Super Lotto P1 research after #1756 (research only)\n',f"Strict causal walk-forward on history through #1756: {rc['n_targets']} targets ({rc['targets'][0]}–{rc['targets'][1]}), confirmation {rc['confirmation_targets'][0]}–{rc['confirmation_targets'][1]} (last 40). Reconstruction verified against every frozen V1 pool (#1753–#1757) and every frozen historical P0 portfolio before use. Random-ranking null seed {rc['random_null_seed']} declared before evaluation.\n",
    f"**One family, Holm-corrected:** {rc['family_size']} variants. Pass rule: {rc['pass_rule']}.\n",'| Variant | Conf. mean | Random | Excess | raw p | Holm p | Block 95% (std) | Conf. halves | Dev. excess | Full mean | Full p | Pass |\n|---|---|---|---|---|---|---|---|---|---|---|---|']
for n,v in sorted(r.items(),key=lambda kv:kv[1]['confirmation']['p']):
    c_=v['confirmation'];P_.append(f"| {n} | {c_['mean']:.3f} | {c_['expected']:.3f} | {c_['excess']:+.3f} | {c_['p']:.3f} | {c_['holm_p']:.2f} | [{c_['block95_std_excess'][0]:+.2f}, {c_['block95_std_excess'][1]:+.2f}] | {c_['halves_std_excess'][0]:+.2f} / {c_['halves_std_excess'][1]:+.2f} | {v['development']['excess']:+.3f} | {v['full']['mean']:.3f} | {v['full']['p']:.3f} | {'PASS' if v['passes'] else 'no'} |")
P_.append(f"\nDynamic pool-size choices: {rc['dynamic_K_choices']}. Jev aggregation: {rc['jev_aggregation']}\n\n**{rc['conclusion']}.** No P1 RESEARCH CHALLENGER exists; no P1 shadow ticket is generated for #1757. Production V1 and P0 remain frozen and unchanged.\n")
(PR/'REPORT.md').write_text('\n'.join(P_)+'\n')
print('reports written')
