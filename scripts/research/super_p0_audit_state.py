"""Build the Jev audit state for a FROZEN Super Lotto P0 portfolio (evidence only; cannot change tickets)."""
import sys,json,argparse
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts/research'))
import super_history as S,super_p0 as P,super_p0_apply as A
from common import save
ap=argparse.ArgumentParser();ap.add_argument('--dir',required=True);ap.add_argument('--target',required=True);a=ap.parse_args();O=R/a.dir;T=int(a.target)
J=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
Pr=J(R/'results/super_lotto/p0_protocol/PROTOCOL.json');rel=J(R/'results/super_lotto/p0_protocol/reliability.json');ev=J(R/'results/super_lotto/p0_protocol/historical_evaluation.json')
sh=J(R/'results/super_lotto/p0_shadow/shadow_score.json');fz=J(O/'p0'/'p0_frozen.json');res=J(O/'p0'/'p0_result.json');v1=J(R/f'results/super_lotto/prospective/prediction_{T}.json')
cands={c['id']:c for c in J(O/'candidates.json')};sel=v1['selection']
records,d,sb,ids=S.load(O/'draws.json');o=S.origin(d,sb,ids,len(d));cred=A.frozen_cred(Pr['frozen_constants']);disc=P.discovery(o,cred)
frozen=[fz['ticket_2']['mains'],fz['ticket_3']['mains']];alts={}
for K in [8,10,15]:
    U=P.universe(o,disc,cred,K);t=[l['ticket'] for l in P.portfolio(U,disc,sel['main'],K)]
    alts[f'K{K}']=dict(ticket_2=t[0],ticket_3=t[1],max_overlap_with_frozen_ticket_2=max(len(set(x)&set(frozen[0])) for x in t),max_overlap_with_frozen_ticket_3=max(len(set(x)&set(frozen[1])) for x in t))
alts['SB_rule_B']=P.assign_sb('B',disc,sel['super_ball'],T);alts['SB_rule_A']=P.assign_sb('A',disc,sel['super_ball'],T)
conf=ev['confirmation']
state=dict(task=f'Audit the evidence quality of a FROZEN three-ticket Super Lotto research portfolio for draw #{T} (5 mains from 1-35 plus one Super Ball from 1-10). Judge only the supplied evidence. This audit cannot change, reorder or replace any ticket; outputs are evidence judgments, not winning probabilities.',
 game_facts=dict(expected_main_matches_per_ticket=5/7,p_sb_hit=0.1,jackpot_odds='1 in 3,246,320',note='Under a fair draw every fixed ticket has identical winning probability.'),
 v1_science_ticket=dict(mains=sorted(sel['main']),super_ball=sel['super_ball'],candidate=sel['candidate_id'],generators=[sel['main_generator'],sel['SB_generator']],selection=v1['selection_policy'],models_passing_V1_gate=[],
     candidate_evidence={k:cands[sel['candidate_id']][k] for k in ['model_agreement_count','sensitivity_rank_range','qualified_models','counterevidence']},
     forensic_note='V1 always selects SL10 (D_trend top ticket + S_gap SB) because a fresh fixed-seed generator picks index 9 of 20 every run.'),
 p0_protocol=dict(status='frozen before the #1754 shadow; history through #1753 only',historical_gate='FAIL',gate=Pr['historical_gate'],main_pool=dict(K=Pr['frozen_constants']['main_pool_K'],basis=Pr['frozen_constants']['pool_basis']),
     credibility=dict(main=Pr['frozen_constants']['main_credibility'],sb=Pr['frozen_constants']['sb_credibility'],ticket=Pr['frozen_constants']['ticket_credibility']),formula=rel['formula'],
     notes=['Every credibility weight is 0: no main, SB or ticket-level component has corrected, stable evidence.','Main ordering is therefore a declared non-evidential convention (equal-weight mean of model z-scores); tickets are chosen for coverage with <=1 shared main.','SB rule C: distinct SBs, which mechanically raises P(any SB hit) without raising expected SB hits.']),
 historical_confirmation_40_draws={m:{k:conf[m][k]['mean'] for k in conf[m] if not k.startswith('diff')}|({'P0_minus_C_ci95':conf[m]['diff_P0_minus_C']['ci95']} if 'diff_P0_minus_C' in conf[m] else {}) for m in ['best','ch_total','ge2','any_sb','ch_sb','unique']},
 shadow_1754=dict(best_main=sh['portfolio_best_main'],total_main=sh['portfolio_total_main'],any_sb=sh['any_sb'],note='one draw, descriptive only'),
 portfolio=[dict(ticket=1,role='V1 Science',mains=sorted(sel['main']),super_ball=sel['super_ball'])]+[dict(ticket=t['ticket'],role=t['role'],mains=t['mains'],super_ball=t['super_ball'],T_rank=t['T_rank'],raw_T=t['raw_T'],incremental_coverage=t['incremental_coverage'],family_contributions=t['family_contributions']) for t in res['tickets'][1:]],
 portfolio_facts=dict(pool=res['pool'],pairwise_main_overlap=res['pairwise_main_overlap'],unique_mains=res['unique_mains'],distinct_sbs=res['distinct_sbs'],sb_order=res['sb_order']),
 computed_sensitivity_research_only=dict(description='Tickets the same algorithm would produce under alternative settings (NOT used; frozen portfolio unchanged).',alternatives=alts))
(O/'p0_jev_audit').mkdir(exist_ok=True);save(O/'p0_jev_audit'/'audit_state.json',state);print(json.dumps(alts,indent=1))
