"""Validation of Protocol 2344 ALIGNED COVERAGE (research only). Strict causal replay at every P0 origin 2231..2343
(weights re-estimated causally from prior origins, exactly as the frozen P0 historical replay did), determinism,
future-mutation leakage test and parameter provenance. Output results/lotto/protocol_2344/VALIDATION.json"""
import sys,json,math,itertools,hashlib,subprocess,time
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'));sys.path.insert(0,str(R/'scripts/research'))
import analyze as a,p0,protocol_2344 as P
O=R/'results/lotto/protocol_2344';O.mkdir(parents=True,exist_ok=True);D=R/'results/lotto/system_audit_2344/data'
J=lambda p:json.loads(Path(p).read_text());git=lambda *x:subprocess.run(['git',*x],cwd=R,capture_output=True,text=True).stdout.strip()
WF=J(D/'walk_forward_rows.json');rows=WF['rows']
base=J(R/'results/lotto/draw2343/draws.json');records=base+[dict(draw_id=2343,date='2026-10-03',numbers=[4,7,13,23,33,35],bonus=38)]
d=np.array([r['numbers'] for r in records])-1;Hh=p0.build_history(d,records);C=P.universe_array();CN=P.CN
NC={}
def best_null(ts):
    s=[set(t) for t in ts];key=tuple(sorted(len(x&y) for x,y in itertools.combinations(s,2)))+(len(set.intersection(*s)),)
    if key not in NC:
        M=[];
        for t in ts:
            v=np.zeros(38,np.int8);v[np.array(t)-1]=1;M.append(v[C].sum(1,dtype=np.int8))
        NC[key]=np.bincount(np.max(np.stack(M),0),minlength=7)/CN
    return NC[key]
t0=time.time();out=[]
for r in rows:
    t=r['t'];ft=p0.origin_features(d,t);W=p0.weights_at(Hh,t);W={k:dict(w=v['w']) for k,v in W.items()}
    res=P.construct(ft,W,r['v1']);ts=[r['v1']]+res['tickets'];win=set(r['winners']);m=sorted((len(set(x)&win) for x in ts),reverse=True);nb=best_null(ts)
    out.append(dict(target=r['target'],tickets=ts,matches=m,best=m[0],null_pmf=nb.tolist(),null_mean=float(nb@np.arange(7)),pairwise=[len(set(x)&set(y)) for x,y in itertools.combinations(ts,2)],
                    A_best=r['strategies']['A_coverage_P0']['best'],A_null_mean=r['strategies']['A_coverage_P0']['null_best_mean'],full_ranks=res['full_universe_ranks']))
    if r['target']%20==0:print(r['target'],round(time.time()-t0,1),flush=True)
def conv_ge(pmfs,obs):
    q=np.array([1.])
    for p in pmfs:q=np.convolve(q,np.asarray(p))
    return float(q[int(obs):].sum())
b=np.array([x['best'] for x in out]);nm=np.array([x['null_mean'] for x in out]);ab=np.array([x['A_best'] for x in out]);an=np.array([x['A_null_mean'] for x in out]);n=len(out);h=n//2
ev=dict(n=n,targets=[out[0]['target'],out[-1]['target']],best_mean=float(b.mean()),null_best_mean=float(nm.mean()),excess=float((b-nm).mean()),p_one_sided=conv_ge([x['null_pmf'] for x in out],b.sum()),
  halves=[float((b-nm)[:h].mean()),float((b-nm)[h:].mean())],block95=p0.block_lb(b-nm,20261009),
  ge={k:dict(observed=int((b>=k).sum()),expected=float(sum(sum(x['null_pmf'][k:]) for x in out))) for k in [3,4,5,6]},
  vs_current_P0=dict(best_diff=float((b-ab).mean()),block95=p0.block_lb(b-ab,20261010),null_mean_diff=float((nm-an).mean()),
                     note='The expected best-ticket gain from disjointness alone (null_mean_diff) is mechanical; the realised difference should match it if neither has skill.'),
  all_pairwise_overlaps_zero=all(max(x['pairwise'])==0 for x in out),P_six_per_draw=3/CN)
# determinism: two independent constructions at the #2343 cutoff (frozen weights) must hash identically
recs2=J(R/'results/lotto/draw2343/draws.json');d2=np.array([r['numbers'] for r in recs2])-1;ft2=a.model_features(a.indicator(d2));W2=P.frozen_weights()
h=[]
for _ in range(2):
    rs=P.construct(ft2,W2,[1,4,13,14,24,38]);h.append(hashlib.sha256(np.round(rs['T_arr'],12).tobytes()+np.round(rs['EQt'],12).tobytes()).hexdigest()+':'+json.dumps(rs['tickets']))
# leakage: replace all draws at/after the target with random draws; the construction at that origin must not change
lk=[]
for t in [100,len(records)-1]:
    d3=d.copy();g=np.random.default_rng(5+t)
    for u in range(t,len(d3)):d3[u]=np.sort(g.choice(38,6,replace=False))
    H3=p0.build_history(d3,records);r1=P.construct(p0.origin_features(d,t),{k:dict(w=v['w']) for k,v in p0.weights_at(Hh,t).items()},[1,2,3,4,5,6])
    r2=P.construct(p0.origin_features(d3,t),{k:dict(w=v['w']) for k,v in p0.weights_at(H3,t).items()},[1,2,3,4,5,6]);lk.append(dict(target=records[t]['draw_id'],identical=r1['tickets']==r2['tickets'] and np.array_equal(r1['rk'][:1000],r2['rk'][:1000])))
prov=dict(weights_source='results/lotto/p0_protocol/PROTOCOL.json frozen_constants.weight_detail',weights=P.frozen_weights(),
  protocol_json_first_commit=git('log','--diff-filter=A','--format=%h %cI','--','results/lotto/p0_protocol/PROTOCOL.json').splitlines()[-1],
  protocol_json_unchanged_since=git('log','--format=%h %cI','-1','--','results/lotto/p0_protocol/PROTOCOL.json'),
  new_numeric_parameters='none (disjointness rule and full-universe scope are structural; no value was estimated from data)',
  draw_2343_used_for_tuning=False)
V=dict(protocol='Lotto Protocol 2344 ALIGNED COVERAGE',historical_replay=ev,determinism=dict(identical=h[0]==h[1],hash=h[0][:64]),leakage_mutation=dict(tests=lk,PASS=all(x['identical'] for x in lk)),parameter_provenance=prov,
  objective_proof='results/lotto/system_audit_2344/data/a2_objective.json (exact enumeration)',
  conclusion='The corrected constructor reproduces its exact null (no predictive skill, as expected), places every portfolio at pairwise overlap 0, is deterministic and leakage-free, and introduces no fitted parameter. Its advantage is the exact, mechanical improvement of the secondary tiers (A2) at unchanged P(6/6) = 3/C(38,6).',
  per_origin=out)
(O/'VALIDATION.json').write_text(json.dumps(a.clean(V),indent=1))
print(json.dumps({k:v for k,v in V.items() if k!='per_origin'},indent=1,default=str))
