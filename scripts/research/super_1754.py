"""Unchanged Super Lotto V1 functions, isolated prospective artifacts for #1754."""
import json,hashlib,math
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
import super_lotto as sl
from common import save,clean,holm,pmean
R=Path(__file__).resolve().parents[2];V=R/'results/super_lotto';O=V/'draw1754';sl.OUT=O
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
assert datetime.now(timezone.utc)<datetime(2026,9,26,1,30,tzinfo=timezone.utc)
assert not (O/'candidate-freeze.json').exists(),'Never regenerate a frozen candidate pool'
check=load(O/'integrity-check.json');assert check['target']==1754 and not check['published']
f=load(V/'prospective/prediction_1753.json');assert all(sha(R/p)==h for p,h in f['hashes'].items())
protected={str(p.relative_to(R)):sha(p) for p in V.glob('*') if p.is_file()};protected.update({str(p.relative_to(R)):sha(p) for p in (V/'prospective').glob('prediction_*.json')});save(O/'v1-preservation.json',protected)
(O/'PROTOCOL.md').write_bytes((V/'PROTOCOL.md').read_bytes())
records=load(V/'draws.json');assert records[-1]['draw_id']==1752
official=load(O/'official-cutoff.json');assert len(official)==1;rr=official[0]['Evening'];assert rr['drawNumber']=='1753'
new=dict(draw_id=1753,date=rr['drawDate'],numbers=sorted(map(int,rr['winNumber'].split())),super_ball=int(rr['superBall']),source='https://supremeventures.com/past-results/',api_source=check['api_url'],raw_file='results/super_lotto/draw1754/official-cutoff.json')
assert new['numbers']==[1,5,8,14,18] and new['super_ball']==3;records.append(new)
assert len(records)==177 and len({r['draw_id'] for r in records})==177
for i,r in enumerate(records):
    assert len(r['numbers'])==len(set(r['numbers']))==5 and all(1<=n<=35 for n in r['numbers']) and 1<=r['super_ball']<=10
    if i:assert r['draw_id']==records[i-1]['draw_id']+1 and r['date']>records[i-1]['date']
save(O/'draws.json',records);save(O/'external-addition.json',new)
save(O/'audit.json',dict(records=177,first=records[0]['draw_id'],last=1753,duplicates=0,missing=0,valid=True,ordinary_observation=True,original_workbook_sha256=sha(sl.SOURCE),normalized_sha256=sha(O/'draws.json')))
d=np.array([r['numbers'] for r in records])-1;sb=np.array([r['super_ball'] for r in records])-1;ids=[r['draw_id'] for r in records];pmf=sl.hg(35,5,5)
baseline=dict(main_probabilities=pmf,expected_main=sl.BASE,SB_probability=.1,main_plus_SB_probabilities=pmf*.1,main_without_SB_probabilities=pmf*.9,jackpot_probability=1/(math.comb(35,5)*10),jackpot_denominator=math.comb(35,5)*10);save(O/'baseline.json',baseline)
sl.descriptive(records,d,sb);random=sl.randomness(d,sb);rows,construct,fit=sl.walk(d,sb,ids,build=True)
save(O/'walk_forward.json',rows);save(O/'construction_origins.json',construct);perf=sl.performance(rows,construct);save(O/'predraw_rankings_and_fit.json',fit)
# Record all saved/raw ranks, tie intervals and undefined model dimensions BEFORE the 20-ticket candidate pool.
main={};jitter=np.random.default_rng(sl.SEED+1754*31).random(35)*1e-10
for m in sl.MN:
    if m not in fit['individual_scores']:
        main[m]=dict(applicable=False,reason='Whole-ticket structure objective, no marginal score',numbers=[dict(number=n,score=None,rank=None) for n in range(1,36)]);continue
    x=np.array(fit['individual_scores'][m]);order=fit['rankings'].get(m,np.argsort(-(x+jitter)));informative=bool(np.std(x)>1e-12)
    main[m]=dict(applicable=True,informative=informative,random_control=m=='H_random',order=(order+1),order_used_by_V1=m in fit['rankings'],flat_ties_not_evidence=not informative,numbers=[dict(number=n+1,score=x[n],rank=int(np.flatnonzero(order==n)[0])+1,tie_min=int(1+sum(x>x[n]+1e-12)),tie_max=int(sum(x>=x[n]-1e-12))) for n in range(35)])
sx=np.vstack([fit['sb_scores'],fit['sb_weights']@fit['sb_scores']]);sjitter=np.random.default_rng(sl.SEED+1754*67).random(10)*1e-10;balls={}
for i,m in enumerate(sl.SN[:6]):
    x=sx[i];order=np.argsort(-(x+sjitter));assert order[0]==fit['sb_predictions'][i]
    balls[m]=dict(informative=bool(np.std(x)>1e-12),order=(order+1),selected=fit['sb_predictions'][i]+1,numbers=[dict(number=n+1,score=x[n],rank=int(np.flatnonzero(order==n)[0])+1,tie_min=int(1+sum(x>x[n]+1e-12)),tie_max=int(sum(x>=x[n]-1e-12))) for n in range(10)])
balls['S_random']=dict(informative=False,random_control=True,selected=fit['sb_predictions'][6]+1,order=None,numbers=[dict(number=n,score=None,rank=None,uniform_sampling_probability=.1) for n in range(1,11)])
save(O/'complete_rankings.json',dict(recorded_utc=now(),cutoff=1753,target=1754,main=main,super_ball=balls,main_weights=fit['main_weights'],SB_weights=fit['sb_weights'],note='Instrumentation only. Inactive components remain unchanged; undefined individual rankings stay null. No calibrated per-number probabilities are implied.'))
configs=[('window20',dict(w=20)),('window40',dict(w=40)),('half10',dict(half=10)),('half40',dict(half=40)),('trend10',dict(trend=10)),('trend30',dict(trend=30)),('history100',dict(cap=100)),('pair001',dict(alpha=.01)),('pair010',dict(alpha=.1)),('equal',dict(mode='equal')),('seed',dict(seed=sl.SEED+99))];sens=[];fits=[]
for name,cfg in configs:
    rr,_,ff=sl.walk(d,sb,ids,**cfg);fits.append(ff);sub=[r for r in rr if r['period']=='confirmation']
    for names,key,NN,KK in [(sl.MN,'main_hits',35,5),(sl.SN,'SB_hits',10,1)]:
        ps=[pmean([r[key][j] for r in sub],NN,KK,KK) for j in range(len(names))]
        for j,(model,p) in enumerate(zip(names,holm(ps))):sens.append(dict(variant=name,model=model,confirmation_mean=float(np.mean([r[key][j] for r in sub])),holm_p=p))
    print('V1 sensitivity',name,flush=True)
save(O/'sensitivity.json',sens);candidates=sl.candidate_set(records,d,sb,fit,perf,fits)
meta=dict(game='Super Lotto',seed=sl.SEED,cutoff=records[-1],origins=len(rows),qualifying_models=[r['model'] for r in perf if r['qualifies']],conclusion='No detectable edge in this dataset' if not any(r['qualifies'] for r in perf) else 'Suggestive retrospective evidence requiring prospective replication',configuration=dict(warmup=50,confirmation=40,search_pool=512,window=30,half_life=20,trend=20,pair_alpha=.05),source_sha256=sha(sl.SOURCE),protocol_sha256=sha(O/'PROTOCOL.md'),normalized_sha256=sha(O/'draws.json'),target=1754)
save(O/'metadata.json',meta)
save(O/'jev_state.json',dict(game='Super Lotto only',rules='Five distinct main numbers 1–35 plus one independent Super Ball 1–10.',baseline=baseline,metadata=meta,randomness=random,candidates=candidates,interpretation='Choice is a preference among full tickets, not a winning probability. Only qualified_models pass corrected retrospective confirmation; no prospective validation exists.'))
for row in rows:
    assert row['training_cutoff']<row['draw_id']<=1753
    for t,h in zip(row['main_tickets'],row['main_hits']):assert len(set(t))==5 and h==len(set(t)&set(records[row['index']]['numbers']))
    assert row['SB_hits']==[int(v==records[row['index']]['super_ball']) for v in row['SB_predictions']]
assert all(sha(R/p)==h for p,h in protected.items())
save(O/'verification.json',dict(passed=True,V1_unchanged=True,source_unchanged=sha(sl.SOURCE)==f['source_sha256'],origins=len(rows),cutoff=1753,valid_candidates=len(candidates)==20,no_other_prediction_inspected=True,no_research_refinement=True))
freeze=dict(frozen_utc=now(),target=1754,cutoff=1753,seed=sl.SEED,candidate_count=len(candidates),hashes={n:sha(O/n) for n in ['candidates.json','jev_state.json','complete_rankings.json','predraw_rankings_and_fit.json','metadata.json','PROTOCOL.md']})
with (O/'candidate-freeze.json').open('x',encoding='utf-8') as h:json.dump(clean(freeze),h,indent=2)
print(json.dumps(dict(qualifiers=meta['qualifying_models'],candidate_count=len(candidates),frozen_utc=freeze['frozen_utc'])))
