"""Research challengers after #1755 (research only; does NOT change the frozen P0 protocol).
Strict causal walk-forward on Super Lotto history through #1755. Holm across all refinements; confirmation = last 40 targets."""
import sys,json,math
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts/research'))
import super_lotto as sl,super_history as S,super_p0 as P
from common import save,holm,hg,pmean
V=R/'results/super_lotto';O=V/'forensic_1755'
base=json.loads((V/'draw1755/draws.json').read_text());assert base[-1]['draw_id']==1754
full=base+[dict(draw_id=1755,date='2026-09-29',numbers=[3,11,15,21,33],super_ball=1)]
d=np.array([r['numbers'] for r in full])-1;sb=np.array([r['super_ball'] for r in full])-1;ids=[r['draw_id'] for r in full]
C=S.cache(d,sb,ids);val=S.validate(C,ids)
idx={x:i for i,x in enumerate(ids)};rows,fit=S.run_at_cutoff(C,idx[1754]);c1754=S.candidates(fit)
val[1754]=dict(mains=[c['main'] for c in c1754]==[c['main'] for c in json.loads((V/'draw1755/candidates.json').read_text())])
assert all(v.get('mains') for v in val.values()),val
H=P.build_history(C);byt={o['t']:o for o in C}
KS=[8,10,12,15,18,20];SD5=math.sqrt(5*(5/35)*(30/35)*(30/34));sdK=lambda K:math.sqrt(K*(5/35)*(30/35)*(35-K)/34)
targets=[o for o in C if 'truth' in o and o['t']>=50+P.MINPRIOR];conf_start=ids[len(ids)-40]
rec=[]
for o in targets:
    t=o['t'];tgt=o['target'];w=set((np.nonzero(o['truth'])[0]+1).tolist());cr=P.credibility(H,t);disc=P.discovery(o,cr);Sx,inf=P.fam_scores(o)
    prior=[h for h in H if h['t']<t]
    # R5 less aggressive shrinkage: raw positive AP z weights
    zw=[];
    for m in P.MAIN:
        e=[h['e'][m] for h in prior if h['e'][m] is not None];zw.append(max(0.,np.mean(e)/(P.AP_SD/math.sqrt(len(e)))) if len(e)>=25 else 0.)
    EQ=disc['EQ'];M5=np.array(zw)@Sx;ord5=sorted(range(35),key=lambda i:(-M5[i],-EQ[i],i))
    # R6 best trailing-30 model
    tr={m:np.mean([h['e'][m] for h in prior[-30:] if h['e'][m] is not None] or [-9]) for m in P.MAIN};bm=max(tr,key=tr.get);j=P.MAIN.index(bm)
    ord6=list(np.argsort(-(Sx[j]+np.random.default_rng(sl.SEED+tgt*31).random(35)*1e-10)))
    base_order=[x-1 for x in disc['order']]
    cap=lambda od,K:len(set((np.array(od[:K])+1).tolist())&w)
    # V1 at this cutoff (per-draw seed) and union
    _,ft=S.run_at_cutoff(C,t-1);cs=S.candidates(ft)
    if cs:
        pd=cs[int(np.random.default_rng(sl.SEED+tgt).integers(len(cs)))];union=set(x for c in cs for x in c['main'])
    else:pd=None;union=None
    wsb=o['truth_sb']+1
    rec.append(dict(target=tgt,period='confirmation' if tgt>=conf_start else 'development',
        cap_base={K:cap(base_order,K) for K in KS},cap_unshrunk12=cap(ord5,12),cap_best_model12=cap(ord6,12),best_model=bm,
        sb_rank=disc['sborder'].index(wsb)+1,pd_hits=(len(set(pd['main'])&w) if pd else None),union=(len(union) if union else None),union_hits=(len(union&w) if union else None)))
# per-origin statistics with exact nulls
def stat_capture(rows,getc,getK):
    c=np.array([getc(r) for r in rows]);K=np.array([getK(r) for r in rows]);mu=5*K/35;sd=np.array([sdK(k) for k in K])
    pm=[hg(35,5,int(k)) for k in K];p=1.;
    q=np.array([1.])
    for x in pm:q=np.convolve(q,x)
    return dict(z=(c-mu)/sd,p=float(q[int(c.sum()):].sum()),mean=float(c.mean()),expected=float(mu.mean()))
def dyn_K(rows,i):
    prev=rows[max(0,i-30):i]
    if len(prev)<10:return 12
    return max(KS,key=lambda K:np.mean([(r['cap_base'][K]-5*K/35)/sdK(K) for r in prev]))
for i,r in enumerate(rec):r['dynK']=dyn_K(rec,i);r['cap_dyn']=r['cap_base'][r['dynK']]
def evaluate(rows):
    out={}
    for K in [12,15,18,20]:out[f'P0_order_top{K}']=stat_capture(rows,lambda r,K=K:r['cap_base'][K],lambda r,K=K:K)
    out['dynamic_pool_size']=stat_capture(rows,lambda r:r['cap_dyn'],lambda r:r['dynK'])
    out['less_shrinkage_top12']=stat_capture(rows,lambda r:r['cap_unshrunk12'],lambda r:12)
    out['best_trailing_model_top12']=stat_capture(rows,lambda r:r['cap_best_model12'],lambda r:12)
    for k in range(1,6):
        h=np.array([int(r['sb_rank']<=k) for r in rows]);p0=k/10
        out[f'SB_top{k}_coverage']=dict(z=(h-p0)/math.sqrt(p0*(1-p0)),p=float(sum(math.comb(len(h),j)*p0**j*(1-p0)**(len(h)-j) for j in range(int(h.sum()),len(h)+1))),mean=float(h.mean()),expected=p0)
    rr=[r for r in rows if r['pd_hits'] is not None];y=np.array([r['pd_hits'] for r in rr]);out['per_draw_seed_v1']=dict(z=(y-5/7)/SD5,p=pmean(y,35,5,5),mean=float(y.mean()),expected=5/7)
    out['broader_candidate_union']=stat_capture([r for r in rows if r['union'] is not None],lambda r:r['union_hits'],lambda r:r['union'])
    return out
conf=[r for r in rec if r['period']=='confirmation'];dev=[r for r in rec if r['period']=='development']
E={'confirmation':evaluate(conf),'development':evaluate(dev),'full':evaluate(rec)}
names=list(E['confirmation']);hp=holm([E['confirmation'][n]['p'] for n in names])
res={}
for n,h in zip(names,hp):
    v=E['confirmation'][n];z=np.array(v['z'],float);lb=P.block_ci(z,P.SEEDS['gate_bootstrap']);half=len(z)//2
    res[n]=dict(confirmation_mean=v['mean'],expected=v['expected'],p=v['p'],holm_p=float(h),block95_std_excess=lb,halves=[float(z[:half].mean()),float(z[half:].mean())],
                development_mean=E['development'][n]['mean'],full_mean=E['full'][n]['mean'],full_p=E['full'][n]['p'],
                passes=bool(h<.05 and lb[0]>0 and z[:half].mean()>0 and z[half:].mean()>0))
passing=[n for n,v in res.items() if v['passes']]
out=dict(data_through=1755,validation=val,targets=[rec[0]['target'],rec[-1]['target']],n_targets=len(rec),confirmation_targets=[conf[0]['target'],conf[-1]['target']],family_size=len(names),
  refinements=res,passing=passing,conclusion='NO SUPER LOTTO V2/P1 REFINEMENT IS JUSTIFIED' if not passing else 'A refinement passed: candidate for a future predeclared challenger only (frozen #1756 rules unchanged)',
  notes=['Each refinement is evaluated causally with an exact null (hypergeometric capture for pools, binomial for SB top-k coverage, hypergeometric matches for V1 seeding).',
         'Capture excess is measured against 5K/35, removing the mechanical advantage of larger pools; SB top-k coverage against k/10.',
         'Wider SB coverage needs more tickets: within a 3-ticket portfolio at most 3 distinct SBs can be played. Top-4/Top-5 SB coverage is tested as ordering skill (hit rate above k/10), not as mechanical coverage.',
         '#1755 is one of %d targets; no refinement is chosen from #1755.'%len(rec)],
  dynamic_K_choices={str(k):int(sum(r['dynK']==k for r in rec)) for k in KS})
save(O/'research_challengers.json',out);save(O/'research_origins.json',rec)
print(json.dumps(dict(val=val,family=len(names),passing=passing,res={n:dict(m=round(v['confirmation_mean'],3),e=round(v['expected'],3),p=round(v['p'],3),h=round(v['holm_p'],3),lb=[round(x,2) for x in v['block95_std_excess']],full_m=round(v['full_mean'],3),full_p=round(v['full_p'],3)) for n,v in res.items()},dyn=out['dynamic_K_choices']),indent=1,default=str))
