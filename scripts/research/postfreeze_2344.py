"""Post-freeze research for #2344 (after commit f248e15; cannot change tickets): random controls, P1 shadows, exact nulls."""
import sys,json,math,itertools,hashlib
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'));sys.path.insert(0,str(R/'scripts/research'))
import analyze as a,p0,protocol_2344 as P
J=lambda p:json.loads((R/p).read_text());now=datetime.now(timezone.utc).isoformat()
pf=J('results/lotto/draw2344/portfolio_frozen.json');T=[t['numbers'] for t in pf['tickets']]
C=P.universe_array();CN=P.CN
def best_pmf(ts):
    M=[]
    for t in ts:
        v=np.zeros(38,np.int8);v[np.array(t)-1]=1;M.append(v[C].sum(1,dtype=np.int8))
    return (np.bincount(np.max(np.stack(M),0),minlength=7)/CN).tolist()
# random controls
fixed=p0.random_diverse(np.random.default_rng(20260930),[],3)
g=np.random.default_rng(20260930+2344);matched=[]
while len(matched)<3:
    t=sorted((g.choice(38,6,replace=False)+1).tolist())
    if all(not set(t)&set(x) for x in matched):matched.append(t)
rc=dict(status='PRE-DRAW RESEARCH CONTROLS (not playable)',created_utc=now,target_draw=2344,frozen_tickets_commit='f248e15',
  fixed_control=dict(seed=20260930,method='p0.random_diverse (unchanged; identical to #2342/#2343 controls)',tickets=fixed,best_null_pmf=best_pmf(fixed)),
  per_draw_matched_control=dict(seed=20260930+2344,method='3 uniformly random tickets, rejection-sampled to pairwise overlap 0 (matched to the playable structure)',tickets=matched,best_null_pmf=best_pmf(matched)),
  playable_portfolio=dict(tickets=T,best_null_pmf=best_pmf(T),P_six=3/CN))
(R/'results/lotto/random_control_2344/random_control_frozen.json').write_text(json.dumps(rc,indent=1))
# P1 shadows
al=J('results/lotto/draw2344/aligned/aligned_result.json');conc=[x['numbers'] for x in al['top200'][:3]]
st=J('results/lotto/draw2344/jev_state.json');el=sorted(st['candidates'],key=lambda c:c['id']);pd=el[int(np.random.default_rng(a.SEED+2344).integers(len(el)))]
lp=J('results/lotto/p1_shadow_2344/legacy_p0/p0_result.json')
sh=dict(status='P1 SHADOW RESEARCH (not playable)',created_utc=now,target_draw=2344,frozen_tickets_commit='f248e15',
  concentration=dict(rule='three highest-ranked distinct combinations of the same full-universe ranking, no diversity rule (jackpot-rational only under a calibrated signal)',tickets=conc,best_null_pmf=best_pmf(conc)),
  v1_per_draw_seed=dict(rule='V1 eligible candidates sorted by ID; index default_rng(20259019... SEED+2344)',seed=a.SEED+2344,candidate=pd['id'],numbers=pd['numbers'],generator=pd['generator']),
  legacy_p0_coverage=dict(rule='frozen P0 protocol 72e1c075 (Top-15 pool, coverage objective) around the frozen V1 ticket',tickets=[t['numbers'] for t in lp['tickets'][1:]] if 'numbers' in lp['tickets'][0] else lp['tickets'],pool=lp['pool']))
(R/'results/lotto/p1_shadow_2344/p1_shadow_frozen.json').write_text(json.dumps(sh,indent=1))
with (R/'results/lotto/prospective_ledger.jsonl').open('a') as h:
    for k,ts in [('random_control_fixed',fixed),('random_control_matched',matched),('P1_shadow_concentration',conc)]:
        for i,t in enumerate(ts):h.write(json.dumps(dict(event='research_prediction_frozen',track=f'{k}_{i+1}',created_utc=now,target_draw=2344,numbers=t,status='research_not_playable'))+'\n')
    h.write(json.dumps(dict(event='research_prediction_frozen',track='P1_shadow_v1_per_draw_seed',created_utc=now,target_draw=2344,numbers=pd['numbers'],status='research_not_playable'))+'\n')
print(json.dumps(dict(fixed=fixed,matched=matched,conc=conc,pd=(pd['id'],pd['numbers']),legacy=sh['legacy_p0_coverage']['tickets'],playable_null=rc['playable_portfolio']['best_null_pmf']),indent=0))
