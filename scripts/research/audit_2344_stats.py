"""Lotto #2344 system audit: statistics over the causal walk-forward rows (audit_2344_core.py output).
A3 portfolio strategies (primary = best single ticket), A5 conditional construction efficiency, A6 discovery,
A7 truncation, A9 combination-probability (conditional-Bernoulli) log scores with causal ML beta, A11 seed designs.
Research only; Lotto data only; outputs results/lotto/system_audit_2344/data/."""
import sys,json,math,itertools,time
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'));sys.path.insert(0,str(R/'scripts/research'))
import analyze as a,p0,v1_history as V
O=R/'results/lotto/system_audit_2344/data';J=lambda p:json.loads(Path(p).read_text())
def save(n,o):(O/n).write_text(json.dumps(a.clean(o),indent=1,allow_nan=False))
W=J(O/'walk_forward_rows.json');rows=W['rows'];n=len(rows);BOOT=20261008
CN=math.comb(38,6);HG=np.array([math.comb(6,k)*math.comb(32,6-k)/CN for k in range(7)])
conf=np.array([r['period']=='confirmation' for r in rows]);half=n//2
def conv_ge(pmfs,obs):
    q=np.array([1.])
    for p in pmfs:q=np.convolve(q,p)
    return float(q[int(round(obs)):].sum())
def summ(x,exp,pmfs=None,p=None):
    x=np.asarray(x,float);exp=np.asarray(exp,float);ex=x-exp
    out=dict(n=len(x),mean=float(x.mean()),expected=float(exp.mean()),excess=float(ex.mean()),block95=p0.block_lb(ex,BOOT),half1=float(ex[:half].mean()),half2=float(ex[half:].mean()),
             confirmation_excess=float(ex[conf].mean()),development_excess=float(ex[~conf].mean()))
    if pmfs is not None:out['p_one_sided']=conv_ge(pmfs,x.sum())
    if p is not None:out['p_one_sided']=p
    return out
# ------------------------------------------------------------------ A3 strategies
STRATS=list(rows[0]['strategies'])
a3={}
for s in STRATS:
    best=[r['strategies'][s]['best'] for r in rows];pm=[np.array(r['strategies'][s]['null_best_pmf']) for r in rows];ex=[r['strategies'][s]['null_best_mean'] for r in rows]
    st=summ(best,ex,pmfs=pm)
    for k in [3,4,5,6]:
        obs=sum(b>=k for b in best);expk=sum(p[k:].sum() for p in pm);st[f'count_ge{k}']=obs;st[f'expected_ge{k}']=float(expk)
        st[f'p_ge{k}']=float(conv_ge([np.array([1-p[k:].sum(),p[k:].sum()]) for p in pm],obs))
    st['secondary']=dict(total=float(np.mean([r['strategies'][s]['total'] for r in rows])),unique_winners=float(np.mean([r['strategies'][s]['unique_winners'] for r in rows])),
                         unique_numbers=float(np.mean([r['strategies'][s]['unique_numbers'] for r in rows])))
    st['paired_vs_A_best']=dict(mean_diff=float(np.mean(np.array(best)-np.array([r['strategies']['A_coverage_P0']['best'] for r in rows]))),
                                block95=p0.block_lb(np.array(best)-np.array([r['strategies']['A_coverage_P0']['best'] for r in rows]),BOOT+1))
    st['null_P_jackpot_per_draw']=float(np.mean([r['strategies'][s]['null_best_pmf'][6] for r in rows]))
    a3[s]=st
hp=a.holm([a3[s]['p_one_sided'] for s in STRATS])
for s,h in zip(STRATS,hp):a3[s]['holm_p']=float(h)
save('a3_strategies.json',dict(primary='best single-ticket matches vs the exact per-origin null pmf of that portfolio (all C(38,6) draws)',strategies=a3,n=n,targets=W['targets']))
# ------------------------------------------------------------------ A5 conditional construction efficiency (strategy A, B, D, H)
def hpool(K,k):return np.array([math.comb(k,j)*math.comb(15-k,6-j)/math.comb(15,6) for j in range(7)])
a5={}
for s in ['A_coverage_P0','B_top3_standalone','D_concentration_top_numbers','C_best_plus_2_diversified']:
    byk={}
    for r in rows:
        pool=set(r['pool']);win=set(r['winners']);k=len(pool&win);ts=r['strategies'][s]['tickets']
        inm=sorted((len(set(t)&pool&win) for t in ts),reverse=True)
        byk.setdefault(k,[]).append((inm[0],inm[1],len(set().union(*map(set,ts))&pool&win)))
    out={}
    for k,v in sorted(byk.items()):
        v=np.array(v);h=hpool(15,k);cdf=np.cumsum(h);b2=np.array([cdf[j]**2-(cdf[j-1]**2 if j else 0) for j in range(7)]);b3=np.array([cdf[j]**3-(cdf[j-1]**3 if j else 0) for j in range(7)])
        out[k]=dict(n=len(v),E_best=float(v[:,0].mean()),E_second=float(v[:,1].mean()),E_portfolio_inpool_winners=float(v[:,2].mean()),max_possible=min(k,6),
                    efficiency=float(v[:,0].mean()/min(k,6)) if k else None,random_one_pool_ticket=float(h@np.arange(7)),random_best_of_2=float(b2@np.arange(7)),random_best_of_3=float(b3@np.arange(7)))
    a5[s]=out
save('a5_conditional_efficiency.json',dict(note='In-pool winners only (V1 numbers outside the pool excluded). random_* = exact expectation for independent uniformly chosen pool tickets.',by_strategy=a5))
# ------------------------------------------------------------------ A6 discovery ranking
METH=list(rows[0]['ranks']);NS=[5,10,12,15,18,20,25,30]
rng=np.random.default_rng(BOOT+2);sims=np.sort(np.argsort(rng.random((50000,38)),1)[:,:6]+1,1)
mrr0=float(np.mean((1/sims).mean(1)));mrrsd=float(np.std((1/sims).mean(1)));ap0=float(np.mean([np.mean([(i+1)/r for i,r in enumerate(s)]) for s in sims[:20000]]))
apsd=float(np.std([np.mean([(i+1)/r for i,r in enumerate(s)]) for s in sims[:20000]]))
RSD=math.sqrt(((38**2-1)/12)/6*(32/37))
a6={};pvals={}
for m in METH:
    rr=[r for r in rows if m in r['ranks']];ii=np.array([r['period']=='confirmation' for r in rr])
    mr=np.array([np.mean(r['ranks'][m]['winner_ranks']) for r in rr]);mrr=np.array([r['ranks'][m]['mrr'] for r in rr]);apv=np.array([r['ranks'][m]['ap'] for r in rr])
    z=(19.5-mr)/RSD;pz=0.5*math.erfc(z.sum()/math.sqrt(len(z))/math.sqrt(2))
    e=dict(n=len(rr),mean_winner_rank=float(mr.mean()),null_mean_rank=19.5,p_rank=pz,mrr=float(mrr.mean()),null_mrr=mrr0,p_mrr=0.5*math.erfc(((mrr.mean()-mrr0)/(mrrsd/math.sqrt(len(rr))))/math.sqrt(2)),
           ap=float(apv.mean()),null_ap=ap0,block95_rank_z=p0.block_lb(z,BOOT+3),halves_rank_z=[float(z[:len(z)//2].mean()),float(z[len(z)//2:].mean())],confirmation_rank_z=float(z[ii].mean()) if ii.any() else None,capture={})
    for N in NS:
        c=np.array([r['ranks'][m]['capture'][str(N)] for r in rr]);hN=np.array([math.comb(6,k)*math.comb(32,N-k)/math.comb(38,N) if N>=k else 0. for k in range(7)])
        e['capture'][N]=dict(mean=float(c.mean()),random=6*N/38,excess=float(c.mean()-6*N/38),p=conv_ge([hN]*len(c),c.sum()),confirmation_excess=float((c[ii]-6*N/38).mean()) if ii.any() else None,
                             ge={k:float(np.mean(c>=k)) for k in range(2,7)},ge_random={k:float(hN[k:].sum()) for k in range(2,7)})
        pvals[f'{m}:top{N}']=e['capture'][N]['p']
    pvals[f'{m}:rank']=pz;pvals[f'{m}:mrr']=e['p_mrr'];a6[m]=e
keys=list(pvals);hh=a.holm([pvals[k] for k in keys]);holm6=dict(zip(keys,map(float,hh)))
save('a6_discovery.json',dict(methods=a6,holm=holm6,family_size=len(keys),min_holm=min(holm6.values()),min_raw=min(pvals.values()),argmin_raw=min(pvals,key=pvals.get)))
# ------------------------------------------------------------------ A9 conditional-Bernoulli combination probabilities, causal ML beta
def esym(w,k=6):
    E=np.zeros(k+1);E[0]=1.
    for x in w:
        E[1:]=E[1:]+x*E[:-1]
    return E
BET=np.linspace(-3,3,601);LNC=math.log(CN)
def ll_matrix(key):
    Lm=np.zeros((n,len(BET)));LR=np.zeros((n,len(BET)));E0=np.zeros((n,len(BET)));V0=np.zeros((n,len(BET)))
    for i,r in enumerate(rows):
        s=np.asarray(r['cb_scores'][key],float);ws=sum(s[x-1] for x in r['winners']);mu=6*s.mean();var=6*(32/37)*s.var()
        for j,b in enumerate(BET):
            le6=math.log(esym(np.exp(b*(s-s.max())))[6])+6*b*s.max()
            Lm[i,j]=b*ws-le6;LR[i,j]=Lm[i,j]+LNC;E0[i,j]=b*mu-le6+LNC;V0[i,j]=b*b*var
    return Lm,LR,E0,V0
a9={}
for key in ['P0_M','equal_weight','A_long','B_recent','C_gap','D_trend']:
    Lm,LR,E0,V0=ll_matrix(key);lr=[];e0=[];v0=[];beta=[]
    for i in range(n):
        if i<20:j=int(np.argmin(np.abs(BET)))
        else:j=int(np.argmax(Lm[:i].sum(0)))
        beta.append(float(BET[j]));lr.append(LR[i,j]);e0.append(E0[i,j]);v0.append(V0[i,j])
    lr=np.array(lr);e0=np.array(e0);v0=np.array(v0);zz=(lr.sum()-e0.sum())/math.sqrt(max(v0.sum(),1e-12))
    jfull=int(np.argmax(Lm.sum(0)))
    a9[key]=dict(causal_beta_first_last=[beta[20],beta[-1]],beta_path_summary=dict(mean=float(np.mean(beta[20:])),min=float(np.min(beta[20:])),max=float(np.max(beta[20:]))),
        mean_log_ratio_vs_uniform=float(lr.mean()),total_log_ratio=float(lr.sum()),implied_mean_multiplier=float(math.exp(lr.mean())),
        null_expected_total=float(e0.sum()),z=float(zz) if v0.sum()>0 else None,p_one_sided=float(0.5*math.erfc(zz/math.sqrt(2))) if v0.sum()>0 else None,
        confirmation_mean_log_ratio=float(lr[conf].mean()),insample_ml_beta_all=float(BET[jfull]),insample_max_mean_log_ratio=float(LR[:,jfull].mean()))
save('a9_combination_probability.json',dict(model='P(S) = prod_{i in S} exp(beta*s_i) / e6(exp(beta*s)) (conditional Bernoulli / exponential-family on 6-subsets); beta fitted by maximum likelihood on prior origins only (uniform for the first 20 targets)',
     metric='log P_model(realized combination) - log(1/C(38,6)); > 0 means the model assigned the realized jackpot combination more probability than uniform',models=a9))
# ------------------------------------------------------------------ A7 truncation summary + feasibility timing
tr=[r['truncation'] for r in rows if r['truncation'] and r['truncation']['weights_nonzero']]
CALL=np.array(list(itertools.combinations(range(38),6)),dtype=np.int8);s=np.random.default_rng(1).random((5,38))
t1=time.time();Tf=sum(w*p0.Z(s[j][CALL].mean(1)) for j,w in enumerate([.03,.02,.01,.0,.0]));Tst=-np.mean(((a.structure(CALL.astype(np.int64))-117)/25)**2,axis=1);el=time.time()-t1
a7=dict(origins_with_nonzero_weights=len(tr),share_full_top1000_inside={K:float(np.mean([x['share_top1000_inside'][str(K)] for x in tr])) for K in [15,18,20,25,30]},
        full_top1_inside={K:float(np.mean([x['full_top1_max_rank']<=K for x in tr])) for K in [15,18,20,25,30]},
        full_rank_of_best_top15_ticket=dict(median=float(np.median([x['full_rank_of_best_top15_ticket'] for x in tr])),max=int(max(x['full_rank_of_best_top15_ticket'] for x in tr))),
        full_universe_scoring_seconds=round(el,2),universe=CN,
        note='Full-universe T uses the same weights but Z-normalizes each component over all 2.76M combinations (the pool T normalizes within the pool, so the relative component scale depends on K).')
save('a7_truncation.json',a7)
# ------------------------------------------------------------------ A11 seed designs (V1 chain; 2211..2343)
J2=lambda p:json.loads(Path(p).read_text())
base=J2(R/'results/lotto/draw2343/draws.json');records=base+[dict(draw_id=2343,date='2026-10-03',numbers=[4,7,13,23,33,35],bonus=38)]
d=np.array([r['numbers'] for r in records])-1;cache=V.walk_cache(d,records);states={s['target']:s for s in (V.state_at_cutoff(d,records,cache,c,with_gate=False) for c in range(49,len(records)-1))}
T1=sorted(states);OUT={r['draw_id']:set(r['numbers']) for r in records}
def chain(pick,norepeat=False,overlap=True):
    prev=None;pid=None;out={}
    for i,t in enumerate(T1):
        cs=states[t]['candidates'];el=[c for c in cs if not overlap or prev is None or len(set(c['numbers'])&set(prev))<=2] or cs
        if norepeat:el=[c for c in el if c['id']!=pid] or el
        el=sorted(el,key=lambda c:c['id']);c=el[pick(i,t,len(el))];out[t]=c;prev=c['numbers'];pid=c['id']
    return out
designs=dict(fixed_current_seed=chain(lambda i,t,k:int(np.random.default_rng(a.SEED).integers(k))),per_draw_seed=chain(lambda i,t,k:int(np.random.default_rng(a.SEED+t).integers(k))),
             rotating_index=chain(lambda i,t,k:t%k),no_repeated_position=chain(lambda i,t,k:int(np.random.default_rng(a.SEED).integers(k)),norepeat=True),
             fixed_seed_without_overlap_rule=chain(lambda i,t,k:int(np.random.default_rng(a.SEED).integers(k)),overlap=False))
a11={}
for k,ch in designs.items():
    ts=[ch[t] for t in T1];m=np.array([len(set(c['numbers'])&OUT[t]) for c,t in zip(ts,T1)]);ids=[c['id'] for c in ts];tk=[tuple(c['numbers']) for c in ts]
    from collections import Counter
    a11[k]=dict(n=len(ts),total_matches=int(m.sum()),expected=len(ts)*36/38,p_total_ge=conv_ge([HG]*len(m),m.sum()),ge3=int((m>=3).sum()),expected_ge3=float(len(m)*HG[3:].sum()),
       distinct_tickets=len(set(tk)),distinct_ids=len(set(ids)),top_ticket_share=Counter(tk).most_common(1)[0][1]/len(tk),
       mean_consecutive_overlap=float(np.mean([len(set(x)&set(y)) for x,y in zip(tk,tk[1:])])),lag2_exact_repeat=float(np.mean([x==y for x,y in zip(tk,tk[2:])])),
       last5=[list(x) for x in tk[-5:]])
uni=np.array([np.mean([len(set(c['numbers'])&OUT[t]) for c in states[t]['candidates']]) for t in T1])
a11['uniform_candidate_expectation']=dict(n=len(T1),total_matches=float(uni.sum()),expected=len(T1)*36/38)
save('a11_seed_designs.json',dict(targets=[T1[0],T1[-1]],designs=a11,note='Repeating a ticket does not change its per-draw jackpot probability (draws are independent); designs differ in exploration only.'))
print(json.dumps(dict(a3={s:dict(best=round(v['mean'],3),exp=round(v['expected'],3),p=round(v['p_one_sided'],3),holm=round(v['holm_p'],2),ge3=(v['count_ge3'],round(v['expected_ge3'],1)),ge4=(v['count_ge4'],round(v['expected_ge4'],2)),ge5=v['count_ge5'],six=v['count_ge6'],conf=round(v['confirmation_excess'],3),uniq=round(v['secondary']['unique_numbers'],1),tot=round(v['secondary']['total'],2)) for s,v in a3.items()},
  a5={s:{k:(x['n'],round(x['E_best'],2),round(x['random_best_of_2'],2),round(x['E_portfolio_inpool_winners'],2)) for k,x in v.items()} for s,v in a5.items()},
  a6_min=(min(holm6.values()),min(pvals,key=pvals.get),min(pvals.values())),a6={m:dict(rank=round(v['mean_winner_rank'],2),p=round(v['p_rank'],3),c15=round(v['capture'][15]['excess'],3),p15=round(v['capture'][15]['p'],3)) for m,v in a6.items()},
  a9={k:dict(lr=round(v['mean_log_ratio_vs_uniform'],4),p=v['p_one_sided'],beta=v['beta_path_summary'],conf=round(v['confirmation_mean_log_ratio'],4),insample=round(v['insample_max_mean_log_ratio'],4)) for k,v in a9.items()},
  a7=a7,a11={k:{x:y for x,y in v.items() if x!='last5'} for k,v in a11.items()}),indent=1,default=str))
