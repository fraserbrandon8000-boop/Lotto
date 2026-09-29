"""Build the Jev audit state for the FROZEN #2342 P0 portfolio (evidence only; cannot change tickets)."""
import sys,json,copy
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'));sys.path.insert(0,str(R/'scripts/research'))
import analyze as a,p0,v1_history as V
J=lambda p:json.loads((R/p).read_text())
P=J('results/lotto/p0_protocol/PROTOCOL.json');rel=J('results/lotto/p0_protocol/reliability.json');ev=J('results/lotto/p0_protocol/historical_evaluation.json')
fz=J('results/lotto/draw2342/p0/p0_frozen.json');res=J('results/lotto/draw2342/p0/p0_result.json');v1=J('results/lotto/draw2342/frozen.json');sh=J('results/lotto/p0_shadow_2341/shadow_score.json')
cands={c['id']:c for c in J('results/lotto/draw2342/candidates.json')}
W0=P['frozen_constants']['weight_detail'];records,d=V.load(R/'results/lotto/draw2342/draws.json');ft=a.model_features(a.indicator(d))
frozen=[fz['ticket_2'],fz['ticket_3']];v1t=v1['numbers']
def run(W,K):
    M,EQ,order=p0.discovery(ft[0],W);pool=order[:K];U=p0.universe(pool,ft,W,M,EQ);U['wsum']=sum(v['w'] for v in W.values());return [l['ticket'] for l in p0.portfolio(U,M,pool,v1t,K)]
alts={}
for name,(Wd,K) in {'K12':(W0,12),'K20':(W0,20),'tau0.05':({k:{'w':v} for k,v in rel['weight_sensitivity_to_tau_reported_only']['0.05'].items()},15),
                    'tau0.18':({k:{'w':v} for k,v in rel['weight_sensitivity_to_tau_reported_only']['0.18'].items()},15),'all_weights_zero':({k:{'w':0.} for k in W0},15)}.items():
    t=run(Wd,K);alts[name]=dict(ticket_2=t[0],ticket_3=t[1],max_overlap_with_frozen_ticket_2=max(len(set(x)&set(frozen[0])) for x in t),max_overlap_with_frozen_ticket_3=max(len(set(x)&set(frozen[1])) for x in t),
                                identical_tickets=sum(sorted(x) in [sorted(f) for f in frozen] for x in t))
fam={f:{k:v[k] for k in ['mean_excess_pct','z','holm_p','confirmation_mean_excess','half1','half2'] if k in v} for f,v in rel['families'].items()}
conf=ev['confirmation']
state=dict(
 task='Audit the evidence quality of a FROZEN three-ticket research portfolio for Jamaica Lotto draw #2342 (6 main numbers from 1-38). Judge only the supplied evidence. This audit cannot change, reorder or replace any ticket, and its outputs are evidence judgments, not winning probabilities.',
 game_facts=dict(fair_draw_expected_matches_per_ticket=36/38,p_ticket_at_least_3=0.0387,p_ticket_at_least_4=0.00186,jackpot_odds='1 in 2,760,681',note='Under a fair draw every fixed ticket has identical winning probability.'),
 v1_science_ticket=dict(numbers=v1t,candidate=v1['candidate_id'],generator=v1['generator'],selection='V1 seeded no-edge fallback (no V1 methodology passed the corrected evidence gate)',
     v1_models_passing_gate=[],candidate_evidence={k:cands[v1['candidate_id']][k] for k in ['contributing_models','validated_models','ensemble_rank','sensitivity_top_quartile_fraction','evidence_against']},
     forensic_note='This exact ticket was also the V1 ticket for #2340. The fixed-seed fallback with a <=2-overlap rule against the previous ticket mechanically alternates between the same candidate slots.'),
 p0_protocol=dict(status='frozen before the #2341 shadow; historical data through #2340 only',historical_gate='FAIL',gate_detail=P['historical_gate'],
     discovery_pool=dict(K=15,basis=P['frozen_constants']['pool_basis']),frozen_weights=P['frozen_constants']['weights'],weight_formula=rel['formula'],
     family_reliability_130_origins=fam,family_score_correlations=rel['correlations'],
     notes=['E_pairs had no Holm-significant pair at any historical origin (flat).','Positive weights for B_recent and D_trend come from statistically null evidence after shrinkage (Holm p about 0.97).','Ticket score T = sum of weight x standardized component; portfolio objective J = T + incremental coverage of the pool, with pairwise overlap <= 2.']),
 historical_confirmation_40_draws={m:{k:conf[m][k]['mean'] for k in ['P0','A_three_random','B_three_random_overlap2','C_v1_plus_two_random','D_top3_standalone']}|{'P0_minus_C_ci95':conf[m]['diff_P0_minus_C']['ci95']} for m in ['best','total','challengers_total','ge3','unique','mean_overlap']},
 shadow_2341=dict(v1=sh['v1_matches'],ticket_2=sh['p0_ticket2_matches'],ticket_3=sh['p0_ticket3_matches'],unique_winners_covered=len(sh['unique_winners_captured']),note='one draw, descriptive only'),
 portfolio=[dict(ticket=1,role='V1 Science',numbers=v1t),
            dict(ticket=2,role='P0 Coverage Challenger',numbers=fz['ticket_2'],T_rank_in_5005=res['tickets'][1]['T_rank_in_universe'],family_contributions=res['tickets'][1]['family_contributions'],incremental_coverage=res['tickets'][1]['incremental_coverage']),
            dict(ticket=3,role='P0 Coverage Challenger',numbers=fz['ticket_3'],T_rank_in_5005=res['tickets'][2]['T_rank_in_universe'],family_contributions=res['tickets'][2]['family_contributions'],incremental_coverage=res['tickets'][2]['incremental_coverage'])],
 portfolio_facts=dict(pairwise_overlap=fz['pairwise_overlap'],unique_numbers=fz['unique_numbers'],discovery_pool=res['pool'],v1_numbers_inside_pool=res['tickets'][0]['numbers_inside_pool']),
 computed_sensitivity_research_only=dict(description='Tickets 2-3 that the same algorithm would produce under alternative settings (NOT used; the frozen portfolio is unchanged).',alternatives=alts))
a.OUT=R/'results/lotto/draw2342/p0_jev_audit';a.save('audit_state.json',state);print(json.dumps(alts,indent=1))
