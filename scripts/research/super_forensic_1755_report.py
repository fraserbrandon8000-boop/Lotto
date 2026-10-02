"""Write results/super_lotto/forensic_1755/REPORT.md from the #1755 forensic outputs."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'results/super_lotto/forensic_1755';J=lambda n:json.loads((O/n).read_text())
v=J('verification.json');p=J('pool_scores.json');de=J('discovery_evidence.json');c=J('construction_diagnosis.json');s=J('super_ball_forensic.json');rec=J('prospective_record.json');rs=J('research_challengers.json')
t=lambda x:' · '.join(f'{i:02}' for i in x);S=p['summary']
L=['# Super Lotto #1755 forensic\n','Actual #1755: **03 · 11 · 15 · 21 · 33 + SB1**.\n',
'| Frozen ticket | Result |\n|---|---|\n| V1 Science 01 · 02 · 18 · 34 · 35 + SB2 | 0/5, SB miss |\n| P0 Coverage 1 06 · 11 · 12 · 22 · 23 + SB3 | 1/5 (11), SB miss |\n| P0 Coverage 2 07 · 17 · 18 · 24 · 25 + SB7 | 0/5, SB miss |\n',
'This was **two separate misses: main-number discovery and Super Ball coverage.**\n','## 1. Frozen record\n']
ch=v['chronology_utc'];cm=v['commits']
L.append(f"All checks pass: **{v['ALL_PASS']}**. Pre-Jev pool freeze hashes {v['candidate_freeze']}; `prediction_1755.json` embedded hashes {v['prediction_embedded']}; P0 freeze hashes all exact; Jev receipt state/request/response match, with a single HTTP attempt; ledger hashes exact; the frozen ticket files are unchanged since the freeze commit.")
L.append(f"\nChronology (UTC): pool frozen {ch['pool_frozen'][:19]} (commit `{cm['pool']}`) → Jev {ch['jev_attempt'][:19]} → V1 frozen {ch['v1_frozen'][:19]} → P0 frozen {ch['p0_frozen'][:19]} (commit `{cm['tickets']}`) → post-freeze research (commit `{cm['post_freeze']}`) → draw 01:30:00. **All three tickets were frozen 39 minutes before the draw.**\n")
L.append('## 2. Whole V1 candidate pool\n\n| ID | Mains | SB | Generator | Matches | Matched | SB1? | Jev Choice | Jev rank | Sens. range |\n|---|---|---|---|---|---|---|---|---|---|')
for x in p['candidates']:
    jr=x['jev_rank'];L.append(f"| {x['id']} | {t(x['main'])} | {x['super_ball']} | {x['generator']} | {x['main_matches']} | {' '.join(f'{i:02}' for i in x['matched']) or '—'} | {'yes' if x['sb_hit'] else 'no'} | {x['jev_choice']} | {jr['best'] if jr['best']==jr['worst'] else str(jr['best'])+'–'+str(jr['worst'])} | {x['sensitivity']['rank_range'][0]}–{x['sensitivity']['rank_range'][1]} |")
md=S['main_match_distribution']
L.append(f"\nMain matches 0:{md['0']} · 1:{md['1']} · 2:{md['2']} · 3+:0. Best: {', '.join(S['best_candidates'])} (2/5). V1 SL10: 0/5. Jev preferred {S['jev_preferred']}: {S['jev_preferred_matches']}/5. **No candidate carried SB1** (pool SBs {S['pool_super_balls']}). Reached ≥2: {S['reached']['2']}; ≥3/≥4/5: none. Jev Choice vs matches: Spearman {S['jev_choice_vs_matches_spearman']:.2f}. Nothing is promoted retrospectively.\n")
L.append('## 3. Discovery failure: winners vs the frozen Top-12 pool\n')
L.append(f"Frozen P0 pool: {t(de['pool'])}. Every P0 credibility weight was 0, so the P0 order is the declared equal-weight convention (EQ = mean of A–D z-scores); E_pairs and the G proxy were flat; F has no number-level score.\n")
L.append('| Winner | A_long | B_recent | C_gap | D_trend | H (control) | P0 rank | Long-run count | Last 30 | EW rate | Gap | Trend | Top-12 support | A narrowly out? | B deep? | F: Top 15/18/20 |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for n,w in de['winners'].items():
    m=w['models'];f=w['features'];a=w['answers'];r=lambda k:f"{m[k]['rank']}"+('' if m[k]['tie'][0]==m[k]['tie'][1] else f" [{m[k]['tie'][0]}–{m[k]['tie'][1]}]")
    L.append(f"| {int(n):02} | {r('A_long')} | {r('B_recent')} | {r('C_gap')} | {r('D_trend')} | {r('H_random')} | **{w['P0_rank']}** | {f['long_run_count']} | {f['last30']} | {float(f['ew_rate']):.3f} | {f['current_gap']} | {float(f['trend']):+.3f} | {', '.join(a['C_supporting_models_top12']) or 'none'} | {'yes' if a['A_narrowly_outside_top12'] else 'no'} | {'yes' if a['B_deeply_ranked'] else 'no'} | {'/'.join('Y' if a['F_in_top'][k] else 'n' for k in ['15','18','20'])} |")
L.append("""
- **03, 21:** no Top-12 support from any informative model (best ranks: 03 was 15th under A_long and 24–34 elsewhere; 21 was 20th under D_trend and 22–35 elsewhere). P0 ranks 29 and 32, outside even a Top 25.
- **15:** mid-table everywhere (ranks 18–22); P0 rank 20, so only a Top 20 pool would have held it.
- **33:** **C_gap's #1** (most overdue number), but A_long, B_recent and D_trend ranked it 26–35, and C_gap is anti-correlated with B and D. The equal-weight average put it at 25. A diagnostic ordering with unshrunk raw positive evidence weights would have put 33 at #2 and pushed 11 to #11. But that weighting has no corrected evidence (raw p ≈ 0.31), so this is a single-draw observation, not a suppressed signal.
- **11:** in the Top 12 of A_long, B_recent and D_trend; P0 rank 5; captured by P0 Coverage 1.
- **D (suppressed by shrinkage?):** only 33 would have entered the Top 12 under the unshrunk diagnostic ordering. **E (zero weights?):** yes, the order was the equal-weight convention; for 33 the averaging is what excluded it. No informative model supported 03, 15 or 21 at all.
""")
NS=['5','8','10','12','15','18','20','25'];tn=de['topN']
L.append('## 4. Top-N winner coverage\n\n| Ranking | '+' | '.join('Top '+N for N in NS)+' |\n|---|'+'---|'*len(NS))
for m,cv in tn['observed'].items():L.append(f"| {m} | "+' | '.join(f"{cv[N]['point']}"+(f" [{cv[N]['tie_range'][0]}–{cv[N]['tie_range'][1]}]" if 'tie_range' in cv[N] and cv[N]['tie_range'][0]!=cv[N]['tie_range'][1] else '') for N in NS)+' |')
L.append('| random expectation 5N/35 | '+' | '.join(f"{tn['random_expected'][N]:.2f}" for N in NS)+' |')
L.append('| historical P0 mean (1652–1753) | '+' | '.join(f"{tn['historical_P0_mean_capture_1652_1753'][N]:.2f}" for N in NS)+' |')
L.append(f"\nThe P0 ordering captured 1 winner at Top 12 against 1.71 random and 1.64 historical. Capturing ≤1 happens in {c['p_capture_le1_random_top12']:.0%} of random Top-12 pools. A Top 20 would have held 2 (random 2.86) and a Top 25 would have held 3 (random 3.57). **This does not show a larger pool is better**: the historical P0 capture is at random level at every depth (see §8).\n")
he=c['historical_efficiency'];cap=c['capability_if_all_winners_in_pool']
L.append(f"""## 5. Construction diagnosis

- Winners in pool: {', '.join(f'{i:02}' for i in c['winners_in_pool'])}. The challengers covered {c['challengers_cover_pool_numbers']} of the 12 pool numbers and **captured the only in-pool winner (11)**.
- Historically (102 targets) the challengers captured {he['captured_by_challengers']} of {he['winners_in_pool_total']} in-pool winners ({he['ratio']:.0%}), against {he['expected_ratio_if_blind']:.0%} expected from the share of the pool they cover. Construction transmits whatever discovery provides.
- **Capability test** (no ticket built from the outcome): if the 5 winners had been any 5 of the 12 frozen pool numbers, the frozen challengers would have scored ≥2 with certainty, ≥3 with probability {cap['p_best_ge3']:.2f} and ≥4 with probability {cap['p_best_ge4']:.2f} (mean challenger total {cap['mean_challenger_total']:.2f}).
- **Classification: D, ordinary random variation, with a discovery shortfall.** It was not a construction failure.
""")
sbm=s['models']
L.append('## 6. Super Ball forensic (actual SB1; played 2, 3, 7)\n\n| SB model | Model pick | SB1 rank | SB2 rank | SB3 rank | SB7 rank |\n|---|---|---|---|---|---|')
for m,x in sbm.items():
    if x.get('random_control'):L.append(f"| {m} | {x['selected']} (control) | — | — | — | — |");continue
    rr=lambda b:f"{x[b]['rank']}"+('' if x[b]['tie'][0]==x[b]['tie'][1] else f" [{x[b]['tie'][0]}–{x[b]['tie'][1]}]")
    L.append(f"| {m}{'' if x['informative'] else ' (flat)'} | {x['selected']} | {rr('SB1')} | {rr('SB2')} | {rr('SB3')} | {rr('SB7')} |")
L.append(f"""
- **SB1 in the V1 pool: no** (pool SBs {s['v1_pool_super_balls']}). It was **structurally excluded by V1**: V1 gives each candidate the single top pick of one of 7 SB models, and SB1 was no model's top pick. Its best ranks were 3rd under S_gap, S_trend (tied 3–4) and S_ensemble.
- **P0 SB order:** {' '.join(map(str,s['p0_sb_order']))}; **SB1 was 7th.** Rule C gave the challengers the top 2 SBs distinct from V1's SB2 (3 and 7). SB1 was not excluded by diversification itself; it lay outside the 3 SBs a 3-ticket portfolio can play.
- **Is the omission ordinary?** Yes. Three distinct SBs miss with probability 0.70; V1's single SB misses with probability 0.90 (0 hits in #1753–#1755 has probability 0.73).
- **Is Top-3 too narrow? Would Top-4/Top-5 help?** A 3-ticket portfolio can only play 3 SBs, so wider coverage means more tickets (cost grows in proportion to coverage). The real question is whether the SB ordering has skill. Historically it does not: in the confirmation period the P0 SB Top-3 contained the winner 22.5% of the time (random 30%), the Top-4 30% (random 40%) and the Top-5 32.5% (random 50%); all Holm p = 1.0. **Wider SB coverage only buys mechanical coverage at proportional cost; there is no basis to promote it.**
- #1753 (SB3), #1754 (SB8), #1755 (SB1): V1 played SB2 each time (S_gap's overdue pick) and no V1 pool contained the winning SB. With n = 3 no rule is inferred.
""")
vs=rec['v1_summary']
L.append(f"""## 7. Combined prospective record

| Draw | V1 | P0 portfolio |
|---|---|---|
| #1753 | 1/5, SB miss | — |
| #1754 | 0/5, SB miss | shadow only: best 1/5, total 2, no SB |
| #1755 | 0/5, SB miss | best 1/5, total 1 (of 3 tickets), no SB |

V1: mean {vs['mean_main']:.2f} main matches vs 0.714 random (P(total ≤ 1 in 3 tickets) = {vs['p_total_le_observed']:.2f}); SB 0/3 (95% CI 0–{vs['sb_rate_ci95'][1]:.2f}; P(0/3) = 0.73); ≥2 mains 0/3 (P = {vs['p_no_ge2_in_3']:.2f}). P0 has one prospective draw (expected portfolio total 2.14; observed 1). **The record is consistent with chance and tells us nothing yet about any edge.**

## 8. Research challengers (strict walk-forward through #1755; {rs['n_targets']} targets, confirmation {rs['confirmation_targets'][0]}–{rs['confirmation_targets'][1]}; Holm across {rs['family_size']} refinements)

| Refinement | Confirmation | Random | p | Holm p | Block LB (std) | Full-period |
|---|---|---|---|---|---|---|""")
for n,x in rs['refinements'].items():L.append(f"| {n} | {x['confirmation_mean']:.3f} | {x['expected']:.3f} | {x['p']:.3f} | {x['holm_p']:.2f} | {x['block95_std_excess'][0]:+.2f} | {x['full_mean']:.3f} (p {x['full_p']:.2f}) |")
L.append(f"""
**{rs['conclusion']}.** Wider pools capture winners at exactly the rate their size implies; dynamic pool size, lighter shrinkage and best-trailing-model weighting show no excess; SB ordering coverage is at or below chance at every depth; per-draw V1 seeding (raw p 0.047) does not survive correction. The frozen #1756 rules are unchanged.

## Conclusion
- **Why were 03, 15, 21, 33 excluded?** 03 and 21 had no Top-12 support from any informative model (best ranks 15 and 20; P0 ranks 29 and 32); 15 was mid-table (P0 rank 20); 33 was C_gap's top number but was averaged down to 25 by the anti-correlated B/D models under the equal-weight convention.
- **Discovery or construction?** Ordinary variation with a discovery shortfall. Construction captured the only in-pool winner and would have performed well had the winners been in the pool.
- **SB1:** 3rd under S_gap/S_trend/S_ensemble, no model's top pick (so structurally absent from V1), 7th in the P0 SB order. A 3-SB miss is the expected outcome 70% of the time.
- **Refinements:** none passes. **NO SUPER LOTTO V2/P1 REFINEMENT IS JUSTIFIED.**
""")
(O/'REPORT.md').write_text('\n'.join(L),encoding='utf-8');print('ok')
