"""Write results/super_lotto/forensic_1754/REPORT.md from the forensic outputs (Super Lotto only)."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'results/super_lotto/forensic_1754'
J=lambda n:json.loads((O/n).read_text(encoding='utf-8'))
v=J('verification.json');p=J('pool_scores.json');n=J('number_evidence.json');s=J('seed_and_construction.json');v2=J('v2_decision.json')
S=p['summary'];t=lambda x:' · '.join(f'{i:02}' for i in x)
L=['# Super Lotto #1754 forensic\n','Actual #1754: **03 · 04 · 21 · 23 · 31 + SB8**. Frozen V1 Science ticket: **01 · 02 · 18 · 34 · 35 + SB2** (SL10: D_trend mains, S_gap SB; seeded no-edge fallback). Result: **0/5, SB miss**.\n',
'## 1. Frozen record verification\n']
c=v['chronology_utc']
L.append(f"- Ticket matches its frozen pool entry: {v['ticket_matches_pool']}. Ledger hash of `prediction_1754.json`: {v['ledger_hash_matches']}.")
L.append(f"- Embedded hashes: {v['embedded_hashes']}. The only mismatch is `{v['embedded_mismatch'][0]}`, the #1753 Jev caller; the #1754 call used `super_1754_jev.mjs`, which matches. Pre-Jev candidate freeze: {v['candidate_freeze_hashes']}.")
L.append(f"- Jev: a single HTTP attempt with retries disabled: {v['jev_single_attempt']}. Receipt state/response/request hashes match (request hashed as compact JSON).")
L.append(f"- Chronology (UTC): unpublished check {c['preflight_unpublished_check'][:19]} → pool frozen {c['candidate_pool_frozen'][:19]} → unpublished check {c['final_unpublished_check'][:19]} → Jev call {c['jev_call_started'][:19]} → ticket frozen {c['ticket_frozen'][:19]} → draw {c['scheduled_draw']}. Order valid: **{v['order_ok']}**. {v['note']}\n")
L.append('## 2. Whole #1754 candidate pool\n\n| ID | Mains | SB | Generators (main/SB) | Outcome | Matched | Jev Choice | Jev rank | Sensitivity rank range | Agreement |\n|---|---|---|---|---|---|---|---|---|---|')
for x in p['candidates']:
    jr=x['jev_rank'];L.append(f"| {x['id']} | {t(x['main'])} | {x['super_ball']} | {x['main_generator']} / {x['SB_generator']} | {x['outcome']} | {' '.join(f'{i:02}' for i in x['matched']) or '—'} | {x['jev_choice']} | {jr['best'] if jr['best']==jr['worst'] else str(jr['best'])+'–'+str(jr['worst'])} | {x['sensitivity']['rank_range'][0]}–{x['sensitivity']['rank_range'][1]} | {x['evidence']['model_agreement_count']} |")
md=S['main_match_distribution'];rr=S['random_reference']
L.append(f"\nMain matches: 0:{md['0']} · 1:{md['1']} · 2+:0. Best: 1/5 ({', '.join(S['best_candidates'])}). V1 SL10: 0/5. Jev preferred **{S['jev_preferred']['id']}** (Choice {S['jev_preferred']['probability']}, confidence {S['jev_preferred']['confidence']}): 0/5. **Candidates with SB8: {S['candidates_with_correct_sb']}.** No candidate materially outperformed V1 (none reached 2/5). For reference, 20 *independent* random tickets would give P(any ≥2) = {rr['p_any_of_20_ge2']:.2f}; the V1 pool is a correlated shortlist, so its all-≤1 result is a weak, single-draw signal of low diversity, not evidence of a flaw. Jev Choice vs matches: Spearman {S['jev_choice_vs_matches_spearman']:.2f}. No candidate is promoted retrospectively.\n")
L.append('## 3. Exact pre-draw main-number evidence (cutoff #1753)\n\nRank [tie interval] from the frozen `complete_rankings.json`. E_pairs was flat (no Holm-retained pair) and the V1 G proxy was flat (the V1 learned main weights were A–D 0, E_pairs 1.0, F 0, and E_pairs was flat), so their orders are arbitrary; F_structure has no number-level ranking; H is a control.\n\n| No. | Role | A_long | B_recent | C_gap | D_trend | H_random |\n|---|---|---|---|---|---|---|')
for x,e in n['main'].items():
    f=lambda m:f"{e['models'][m]['rank']}"+('' if e['models'][m]['tie_interval'][0]==e['models'][m]['tie_interval'][1] else f" [{e['models'][m]['tie_interval'][0]}–{e['models'][m]['tie_interval'][1]}]")
    L.append(f"| {int(x):02} | {e['role'].replace('_',' ')} | {f('A_long')} | {f('B_recent')} | {f('C_gap')} | {f('D_trend')} | {f('H_random')} |")
NS=['5','7','10','12','15','20']
L.append('\nWinner coverage (point [tie range]); random expectation 5N/35.\n\n| Model | '+' | '.join('Top '+N for N in NS)+' |\n|---|'+'---|'*len(NS))
for m in ['A_long','B_recent','C_gap','D_trend','H_random']:
    cv=n['coverage'][m];L.append(f"| {m} | "+' | '.join(f"{cv[N]['point']}"+('' if cv[N]['min']==cv[N]['max'] else f" [{cv[N]['min']}–{cv[N]['max']}]") for N in NS)+' |')
L.append('| random expectation | '+' | '.join(f'{5*int(N)/35:.2f}' for N in NS)+' |')
L.append("\nNo winner was in the Top 5 of A_long, B_recent or D_trend; the selected numbers 01, 18, 35, 02 were D_trend's ranks 1–4. C_gap held 04 at rank 3 and all five winners in its Top 20 (random 2.86), a single-draw observation.\n")
L.append('## 4. Super Ball: SB8 (winner) vs SB2 (selected)\n\n| SB model | Informative | Model pick | SB8 rank | SB2 rank |\n|---|---|---|---|---|')
for m,e in n['super_ball'].items():
    if e.get('random_control'):L.append(f"| {m} | control | {e['selected']} | — | — |");continue
    L.append(f"| {m} | {'yes' if e['informative'] else 'flat'} | {e['selected']} | {e['SB8']['rank']}"+('' if e['SB8']['tie'][0]==e['SB8']['tie'][1] else f" [{e['SB8']['tie'][0]}–{e['SB8']['tie'][1]}]")+f" | {e['SB2']['rank']}"+('' if e['SB2']['tie'][0]==e['SB2']['tie'][1] else f" [{e['SB2']['tie'][0]}–{e['SB2']['tie'][1]}]")+' |')
L.append(f"\nSB2 was S_gap's and S_ensemble's first choice (it was the most overdue ball; the V1 SB ensemble weights were S_gap 0.35 and the flat S_transition 0.65, so the ensemble reduced to S_gap). SB8 ranked 4th under S_recent and 5th under S_trend, and no model ranked it first. **SB8 appeared in no frozen candidate** (pool SBs {n['pool_super_balls_1754']}). In #1753 the pool carried SBs {n['pool_super_balls_1753']} and omitted the winner SB3. **The SB coverage omission repeated.** It is structural: V1 assigns SBs cyclically from the seven SB models' single top picks, so a pool carries at most 7 and on average {s['sb_pool_coverage']['mean_distinct_sbs']:.1f} distinct SBs. Historically the actual SB was in the pool at {s['sb_pool_coverage']['actual_sb_in_pool_rate']:.0%} of 121 targets, in line with that coverage (≈{s['sb_pool_coverage']['mean_distinct_sbs']*10:.0f}%), so there is no SB skill beyond coverage.\n")
pr=s['production'];f=s['fixed_seed_designs'];pd=s['per_draw_seed_designs'];cp=s['compression']
L.append(f"""## 5. Combined #1753 + #1754 diagnosis (descriptive; n = 2)

| | #1753 | #1754 |
|---|---|---|
| Frozen V1 | 01 · 22 · 32 · 34 · 35 + SB2 (SL10) | 01 · 02 · 18 · 34 · 35 + SB2 (SL10) |
| Actual | 01 · 05 · 08 · 14 · 18 + SB3 | 03 · 04 · 21 · 23 · 31 + SB8 |
| Result | 1/5, SB miss | 0/5, SB miss |
| Best candidate | 2/5 | 1/5 |
| Winners in the union of the 20 candidates | {cp['targets_1753_1754'][0]['winners_in_union']} of 5 ({cp['targets_1753_1754'][0]['union']} numbers) | {cp['targets_1753_1754'][1]['winners_in_union']} of 5 ({cp['targets_1753_1754'][1]['union']} numbers) |
| Winning SB in pool | no | no |

- **Main-number ranking quality:** in both draws the V1 selected numbers came from the top of D_trend/B_recent (recently frequent numbers), and the winners sat mostly mid-table. Historical capture is at random level (the #1753 forensic found all corrected coverage p = 1.0). There is no discovery signal to lose.
- **Candidate construction:** the 20 candidates span about {cp['mean_union_of_20_candidates']:.1f} of the 35 numbers and contain {cp['mean_winners_in_union']:.2f} winners on average (random for that many numbers {cp['expected_winners_in_union']:.2f}); the best candidate averages {cp['mean_best_candidate']:.2f} matches. **Compression is not measurably losing information**: the shortlist holds winners at the rate its size implies, and it cannot hold more.
- **Repeated-number bias:** 01, 34, 35 and SB2 are in both frozen tickets because both are SL10 = D_trend's top ticket, and D_trend's top numbers move slowly.
- **Repeated SB behaviour:** S_gap picks the most overdue ball and keeps picking it until it is drawn. The V1 SB repeated on {pr['same_sb_consecutive']:.0%} of consecutive historical draws.
- **Fixed-seed effect (main driver of repetition):** V1 creates `default_rng(2026092109)` fresh each run, and with 20 candidates the index is always 9, so V1 **always** selects SL10 (D_trend top ticket + S_gap SB): 121 of 121 reconstructed cutoffs, 1 distinct candidate ID. Unlike Lotto there is no previous-ticket rule, so **every** fixed seed repeats the same slot 100% of the time; per-draw seeds would use {pd['distinct_ids']['mean']:.0f} IDs. Realized results do not depend on it: production mean {pr['mean_main']:.3f} main matches and {pr['sb_hits']} SB hits over 121 draws vs fixed-seed average {f['mean_main']['mean']:.3f} / {f['sb_hits']['mean']:.1f} and per-draw {pd['mean_main']['mean']:.3f} / {pd['sb_hits']['mean']:.1f} (random 0.714 / 12.1).
- **Jev behaviour:** diffuse and non-causal. #1754 Choice confidence 0.25, favourite SL11 at 0.30; Choice vs outcome Spearman −0.11 (#1753: +0.12). Under the no-edge rule Jev never affects the V1 ticket.
""")
best=v2['construction_methods'][0];sel=sorted(v2['selectors'],key=lambda r:r['holm_p'])
L.append(f"""## 6. Is a Super Lotto V2 justified?

Causal V1 walk-forward through #1754 ({v2['origins']} origins; last 40 = confirmation), candidate refinements limited to existing V1 components:
- **Main and SB models as selectors:** none passes the V1 gate (lowest confirmation Holm p = {sel[0]['holm_p']:.2f}).
- **V1 two-stage construction methods** ({v2['construction_family_size']} methods, Holm family): best raw result {best['method']} (mean {best['mean']:.3f}, raw p {best['p']:.3f}), Holm p {best['holm_p']:.2f}: fails correction.
- **Fallback seeding design:** changes which candidate is chosen, not expected matches (no gate possible).

**NO SUPER LOTTO V2 IS JUSTIFIED.** V1 is preserved unchanged.

## 7. Conclusion
- **Main-number issue:** winners were mid-ranked by every informative model. This is consistent with random-level historical discovery, not a new defect.
- **Candidate-construction issue:** a correlated shortlist that is persistent between draws (fixed 4,096-combination search pool). It covers winners at the rate its size implies.
- **Super Ball issue:** structural SB under-coverage (about {s['sb_pool_coverage']['mean_distinct_sbs']:.1f} distinct SBs per pool, cyclic assignment), and the winning SB was absent in both #1753 and #1754. The final V1 SB is always S_gap's overdue pick.
- **Jev behaviour:** diffuse (confidence 0.25), unrelated to outcomes, no causal role.
- **Does #1754 justify changing V1? NO.**
""")
(O/'REPORT.md').write_text('\n'.join(L),encoding='utf-8');print('ok')
