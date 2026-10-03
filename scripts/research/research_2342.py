"""Lotto research challengers after #2342 (research only; Lotto data only; targets 2231..2342, strict walk-forward).
Every challenger is evaluated causally (only draws before each target) on the same targets as the frozen P0 baseline,
with one Holm family across all challengers. Nothing here changes V1 or the frozen P0. Output: results/lotto/forensic_2342/research_challengers.json"""
import sys,json,math,itertools
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'));sys.path.insert(0,str(R/'scripts/research'))
import analyze as a,p0,v1_history as V
D=R/'results/lotto/draw2342';O=R/'results/lotto/forensic_2342'
J=lambda p:json.loads(Path(p).read_text())
WIN=[12,13,14,15,19,33];BOOT=20261005
base=J(D/'draws.json');records=base+[dict(draw_id=2342,date='2026-09-30',numbers=WIN,bonus=21)]
d=np.array([r['numbers'] for r in records])-1;A=a.indicator(d);idx={r['draw_id']:i for i,r in enumerate(records)}
HG=np.array([math.comb(6,k)*math.comb(32,6-k)/math.comb(38,6) for k in range(7)])
def pair_pmf(o):
    """Exact null pmf of total matches of two tickets sharing o numbers."""
    p=np.zeros(13)
    for s in range(o+1):
        for x in range(7-o):
            for y in range(7-o):
                r=6-s-x-y
                if 0<=r<=26+o:p[2*s+x+y]+=math.comb(o,s)*math.comb(6-o,x)*math.comb(6-o,y)*math.comb(26+o,r)
    return p/math.comb(38,6)

# ---------------- V1 reconstructed chain + V1 pools (targets 2211..2342)
cache=V.walk_cache(d,records);states=[V.state_at_cutoff(d,records,cache,c,with_gate=False) for c in range(49,idx[2341]+1)]
assert [c['numbers'] for c in states[-1]['candidates']]==[c['numbers'] for c in J(D/'candidates.json')]
ST={s['target']:s for s in states};T1=sorted(ST)
def v1_chain(pick,filt=None):
    prev=None;prev_id=None;out={}
    for i,t in enumerate(T1):
        cs=ST[t]['candidates'];el=[c for c in cs if prev is None or len(set(c['numbers'])&set(prev))<=2] or cs
        if filt:el=filt(el,prev_id,ST[t]) or el
        el=sorted(el,key=lambda c:c['id']);c=el[pick(i,t,len(el))];out[t]=c;prev=c['numbers'];prev_id=c['id']
    return out
prod=lambda i,t,n:int(np.random.default_rng(a.SEED).integers(n))
v1prod=v1_chain(prod)
def fixed_cands(st):
    ein=bool(np.std(st['family_scores'][4])>1e-12)
    return {c['id'] for c in st['candidates'] if c['generator']=='H_random' or (c['generator']=='E_pairs' and not ein)}
V1VAR=dict(per_draw_seed=v1_chain(lambda i,t,n:int(np.random.default_rng(a.SEED+t).integers(n))),
           rotating_index=v1_chain(lambda i,t,n:t%n),
           no_repeat_position=v1_chain(prod,lambda el,pid,st:[c for c in el if c['id']!=pid]),
           drop_fixed_data_independent_candidates=v1_chain(prod,lambda el,pid,st:[c for c in el if c['id'] not in fixed_cands(st)]))

# ---------------- P0 machinery (generalised copy of p0.portfolio; p0.py itself unchanged)
Hh=p0.build_history(d,records)
def weights(t,tau=p0.TAU,use_h=True):
    W=p0.weights_at(Hh,t)
    for k,v in W.items():
        if v['dbar'] is None:continue
        n=v['n'];dd=v['dbar'] if tau is None else v['dbar']*n*tau**2/(n*tau**2+1);v['d']=dd;v['w']=max(0.,dd)*(v['h'] if use_h else 1.)
    return W
def build(pool,ft,W,M,EQ):
    U=p0.universe(pool,ft,W,M,EQ);U['wsum']=sum(v['w'] for v in W.values());return U
def portfolio(U,M,pool,v1,K,eta=1.,L0=2,t_weight=1.):
    C=U['C'];T=U['T']*t_weight;EQt=U['EQ'];selected=[np.array(v1)-1];out=[]
    mass=np.zeros(38);pn=np.array(sorted(pool))-1;mm=np.maximum(.01,1+M[pn]);mass[pn]=mm/mm.sum()
    inC=np.zeros((len(C),38),bool);inC[np.arange(len(C))[:,None],C]=True
    for k in range(2):
        cov_=np.zeros(38,bool)
        for s in selected:cov_[s]=True
        cov=(inC&~cov_).astype(float)@mass/(6/K);Jv=T+eta*cov
        ov=np.stack([inC[:,s].sum(1) for s in selected],1).max(1);L=L0
        while L<=6 and not (ov<=L).any():L+=1
        feas=np.nonzero(ov<=L)[0];allidx=np.arange(len(C))
        exc=bool(U['wsum']>0 and t_weight>0 and U['T'].max()-U['T'][feas].max()>2*U['T'].std())
        b=p0._best(allidx if exc else feas,Jv,EQt);selected.append(C[b]);out.append((C[b]+1).tolist())
    return out
def equal_W(ft):
    inf=[f for j,f in enumerate(p0.FAM) if np.std(ft[0][j])>1e-12];W={f:dict(w=(1/len(inf) if f in inf else 0.)) for f in p0.FAM};W['pair']=dict(w=0.);W['struct']=dict(w=0.);return W
targets=list(range(70,len(records)));NAMES=['P0_baseline_K15','K18','K20','K25','dynamic_K','tau_0.05','tau_0.20','no_shrinkage','equal_weights','no_stability_factor',
       'overlap_le1','overlap_le3','cluster_neutral_struct0','exhaustive_top2_standalone_T','exhaustive_coverage_only','exhaustive_evidence_only']
res={n:{} for n in NAMES};capt={K:[] for K in [10,12,15,20]};print('walk-forward over',len(targets),'targets…',flush=True)
for t in targets:
    tgt=records[t]['draw_id'];win=set(np.nonzero(A[t])[0]+1);ft=p0.origin_features(d,t);v1=v1prod[tgt]['numbers']
    W=weights(t);M,EQ,order=p0.discovery(ft[0],W)
    def run(name,W_=W,M_=M,EQ_=EQ,order_=order,K=15,**kw):
        pool=order_[:K];U=build(pool,ft,W_,M_,EQ_);res[name][tgt]=portfolio(U,M_,pool,v1,K,**kw);return U
    U15=run('P0_baseline_K15')
    for K in (18,20,25):run(f'K{K}',K=K)
    # dynamic K: causal choice by best prior capture z among {10,12,15,20} (needs >=20 prior targets; else 15)
    if len(capt[15])>=20:
        z={K:(np.mean(capt[K])-6*K/38)/math.sqrt(K*(6/38)*(32/38)*(38-K)/37/len(capt[K])) for K in capt};Kd=max(z,key=z.get)
    else:Kd=15
    run('dynamic_K',K=Kd)
    for K in capt:capt[K].append(len(set(order[:K])&win))
    for name,tau in (('tau_0.05',.05),('tau_0.20',.20),('no_shrinkage',None)):
        W2=weights(t,tau=tau);M2,EQ2,o2=p0.discovery(ft[0],W2);run(name,W2,M2,EQ2,o2)
    We=equal_W(ft);Me=EQ.copy();oe=sorted(range(38),key=lambda i:(-round(Me[i],12),i));oe=[i+1 for i in oe];run('equal_weights',We,Me,EQ,oe)
    Wh=weights(t,use_h=False);Mh,EQh,oh=p0.discovery(ft[0],Wh);run('no_stability_factor',Wh,Mh,EQh,oh)
    run('overlap_le1',L0=1);run('overlap_le3',L0=3)
    Ws={k:dict(v) for k,v in W.items()};Ws['struct']['w']=0.;run('cluster_neutral_struct0',Ws)
    res['exhaustive_top2_standalone_T'][tgt]=p0.top3_standalone(U15)[:2]
    run('exhaustive_coverage_only',t_weight=0.);run('exhaustive_evidence_only',eta=0.)
    if t%20==0:print(' ',tgt,flush=True)

# ---------------- evaluation
TG=[records[t]['draw_id'] for t in targets];OUTC={r['draw_id']:set(r['numbers']) for r in records}
def evaluate(series,kind,baseline):
    tg=sorted(series);obs=[];pm=[];exp=[];bl=[]
    for t in tg:
        if kind=='p0':
            t2,t3=series[t];obs.append(len(set(t2)&OUTC[t])+len(set(t3)&OUTC[t]));pm.append(pair_pmf(len(set(t2)&set(t3))));exp.append(2*36/38)
            b2,b3=baseline[t];bl.append(len(set(b2)&OUTC[t])+len(set(b3)&OUTC[t]))
        else:
            obs.append(len(set(series[t]['numbers'])&OUTC[t]));pm.append(HG);exp.append(36/38);bl.append(len(set(baseline[t]['numbers'])&OUTC[t]))
    obs=np.array(obs);exp=np.array(exp);bl=np.array(bl);n=len(obs);h=n//2;ex=obs-exp
    keep=np.array([t!=2342 for t in tg])
    out=dict(n=n,observed=int(obs.sum()),expected=float(exp.sum()),mean_excess=float(ex.mean()),p_one_sided=p0.conv_p(pm,int(obs.sum())),
        block95_excess=p0.block_lb(ex,BOOT),half1=float(ex[:h].mean()),half2=float(ex[h:].mean()),confirmation_last40_excess=float(ex[-40:].mean()),
        vs_baseline=dict(mean_diff=float((obs-bl).mean()),block95=p0.block_lb(obs-bl,BOOT+1)),
        without_2342=dict(observed=int(obs[keep].sum()),p_one_sided=p0.conv_p([q for q,k in zip(pm,keep) if k],int(obs[keep].sum()))),
        ticket_ge3=int((obs>=3).sum()) if kind=='v1' else None)
    if kind=='p0':
        m=[max(len(set(x)&OUTC[t]) for x in series[t]) for t in tg];out['challenger_best_ge3']=int(sum(v>=3 for v in m));out['challenger_best_ge4']=int(sum(v>=4 for v in m))
    return out
base_p0=res['P0_baseline_K15'];ev={}
for n_ in NAMES[1:]:ev[n_]=dict(track='P0 tickets 2-3',**evaluate(res[n_],'p0',base_p0))
for n_,s in V1VAR.items():ev[n_]=dict(track='V1 ticket 1',**evaluate(s,'v1',v1prod))
names=list(ev);hp=a.holm([ev[n]['p_one_sided'] for n in names]);hp2=a.holm([ev[n]['without_2342']['p_one_sided'] for n in names])
for n_,h_,h2 in zip(names,hp,hp2):
    e=ev[n_];e['holm_p']=float(h_);e['without_2342']['holm_p']=float(h2)
    e['PASS']=bool(h_<.05 and e['block95_excess'][0]>0 and e['half1']>0 and e['half2']>0 and e['vs_baseline']['block95'][0]>0 and h2<.05)
baseline_eval=dict(P0_baseline_K15=evaluate(base_p0,'p0',base_p0),V1_production_chain=evaluate(v1prod,'v1',v1prod))
passing=[n for n in names if ev[n]['PASS']]
out=dict(targets=[TG[0],TG[-1]],n_targets=len(TG),holm_family_size=len(names),
    gate='PASS requires: Holm-corrected one-sided exact p < 0.05 (all challengers one family), block-bootstrap 95% lower bound of mean excess over the exact null > 0, both chronological halves > 0, '
         'block-bootstrap 95% lower bound of the paired difference vs the baseline (frozen P0 for tickets 2-3; production V1 chain for ticket 1) > 0, and Holm p < 0.05 again with #2342 removed.',
    baselines=baseline_eval,challengers=ev,passing=passing,
    not_testable=dict(jev_aggregation='Not testable historically: 3-5 Jev calls on each of ~110 reconstructed states (~550 calls). Prospective replicates exist for #2342 (and will for #2343) only.',
                      cluster_rule='No cluster rule tested as a promotion candidate beyond struct0: actual draws match the exact run-length null (historical_2342.json), so no cluster rule has a causal basis.'),
    verdict=('NO LOTTO V2/P1 REFINEMENT IS JUSTIFIED.' if not passing else 'P1 CHALLENGER(S) PASSED: '+', '.join(passing)),
    notes=['V1 ticket 1 inside every P0 portfolio is the reconstructed production fallback chain (seed 20260919, <=2 overlap).',
           'P0 weights are re-estimated causally at every target (origins strictly before the target), exactly as in p0_protocol/historical_origins.json.',
           'dynamic_K picks K among {10,12,15,20} by the best prior capture z-score (>=20 prior targets; otherwise 15).',
           'equal_weights: discovery by the equal mean z over informative families; T uses equal family weights, no pair/struct term.'])
a.OUT=O;a.save('research_challengers.json',out)
print(json.dumps({n:dict(obs=ev[n]['observed'],exp=round(ev[n]['expected'],2),p=round(ev[n]['p_one_sided'],4),holm=round(ev[n]['holm_p'],3),vs=round(ev[n]['vs_baseline']['mean_diff'],3),PASS=ev[n]['PASS']) for n in names},indent=0))
print('baseline',json.dumps(baseline_eval,default=float)[:600]);print(out['verdict'])
# sanity: baseline must reproduce the frozen-protocol historical portfolios (2231-2340) and the live #2342 challengers' numbers when V1 matches
HO={r['target']:r['byK']['15']['portfolio'][1:] for r in J(R/'results/lotto/p0_protocol/historical_origins.json')['rows']}
mism=[t for t in HO if [sorted(x) for x in base_p0[t]]!=[sorted(x) for x in HO[t]]]
print('baseline vs p0_protocol/historical_origins mismatches:',mism)
out['baseline_reproduces_p0_protocol_historical_origins_2231_2340']=not mism;a.save('research_challengers.json',out)
