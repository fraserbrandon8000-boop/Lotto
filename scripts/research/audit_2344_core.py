"""Lotto #2344 system audit: historical, strictly causal computations (research only; Lotto data only).
Reuses unchanged V1 (scripts/analyze.py), v1_history.py and p0.py. Changes no production file.
History: draws 2161..2343 (#2343 appended as one ordinary observation). Targets 2231..2343 (same origin rule as P0).
Outputs results/lotto/system_audit_2344/data/*.json"""
import sys,json,math,itertools,time
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'));sys.path.insert(0,str(R/'scripts/research'))
import analyze as a,p0,v1_history as V
O=R/'results/lotto/system_audit_2344/data';O.mkdir(parents=True,exist_ok=True)
J=lambda p:json.loads(Path(p).read_text())
def save(n,o):(O/n).write_text(json.dumps(a.clean(o),indent=1,allow_nan=False))
W2343=[4,7,13,23,33,35]
base=J(R/'results/lotto/draw2343/draws.json');assert base[-1]['draw_id']==2342
records=base+[dict(draw_id=2343,date='2026-10-03',numbers=W2343,bonus=38)]
d=np.array([r['numbers'] for r in records])-1;A=a.indicator(d);idx={r['draw_id']:i for i,r in enumerate(records)};NREC=len(records)
CN=math.comb(38,6);HG=np.array([math.comb(6,k)*math.comb(32,6-k)/CN for k in range(7)])
SEED_AUDIT=20261007   # research-only seed for random comparator portfolios, declared in AUDIT_PLAN before computation
t0=time.time()
# ------------------------------------------------------------------ full universe (once)
CALL=np.array(list(itertools.combinations(range(38),6)),dtype=np.int8);assert len(CALL)==CN
def matches_all(ticket):
    m=np.zeros(38,np.int8);m[np.array(ticket)-1]=1;return m[CALL].sum(1,dtype=np.int8)
NULLCACHE={}
def best_null(tickets):
    """Exact null pmf of best single-ticket matches over all C(38,6) equally likely draws."""
    s=[set(t) for t in tickets];key=tuple(sorted(len(x&y) for x,y in itertools.combinations(s,2)))+(len(set.intersection(*s)) if len(s)>2 else -1,len(s))
    if key not in NULLCACHE:
        b=np.max(np.stack([matches_all(t) for t in tickets]),0);NULLCACHE[key]=np.bincount(b,minlength=7)/CN
    return NULLCACHE[key]
print('universe ready',round(time.time()-t0,1),flush=True)
# ------------------------------------------------------------------ V1 reconstructed chain (validated)
cache=V.walk_cache(d,records);states=[V.state_at_cutoff(d,records,cache,c,with_gate=False) for c in range(49,NREC-1)]
for tgt,p in {2341:'draw2341',2342:'draw2342',2343:'draw2343'}.items():
    s=[x for x in states if x['target']==tgt][0];assert [c['numbers'] for c in s['candidates']]==[c['numbers'] for c in J(R/f'results/lotto/{p}/candidates.json')],tgt
ST={s['target']:s for s in states};T1=sorted(ST)
def v1_chain(pick):
    prev=None;out={}
    for i,t in enumerate(T1):
        cs=ST[t]['candidates'];el=[c for c in cs if prev is None or len(set(c['numbers'])&set(prev))<=2] or cs
        el=sorted(el,key=lambda c:c['id']);c=el[pick(i,t,len(el))];out[t]=c;prev=c['numbers']
    return out
v1prod=v1_chain(lambda i,t,n:int(np.random.default_rng(a.SEED).integers(n)))
for t,f in [(2342,'draw2342'),(2343,'draw2343')]:assert v1prod[t]['numbers']==J(R/f'results/lotto/{f}/frozen.json')['numbers'],t
print('V1 chain ok',round(time.time()-t0,1),flush=True)
# ------------------------------------------------------------------ P0 machinery
Hh=p0.build_history(d,records)
def build(pool,ft,W,M,EQ):
    U=p0.universe(pool,ft,W,M,EQ);U['wsum']=sum(v['w'] for v in W.values());return U
def coverage_portfolio(U,M,pool,v1,K,eta=1.,L0=2,hybrid=False):
    C=U['C'];T=U['T'];EQt=U['EQ'];selected=[np.array(v1)-1];out=[]
    mass=np.zeros(38);pn=np.array(sorted(pool))-1;mm=np.maximum(.01,1+M[pn]);mass[pn]=mm/mm.sum()
    inC=np.zeros((len(C),38),bool);inC[np.arange(len(C))[:,None],C]=True
    for k in range(2):
        cov_=np.zeros(38,bool)
        for s in selected:cov_[s]=True
        cov=(inC&~cov_).astype(float)@mass/(6/K)
        Jv=(p0.Z(T)+p0.Z(cov)) if hybrid else T+eta*cov
        ov=np.stack([inC[:,s].sum(1) for s in selected],1).max(1);L=L0
        while L<=6 and not (ov<=L).any():L+=1
        feas=np.nonzero(ov<=L)[0];exc=bool(U['wsum']>0 and not hybrid and T.max()-T[feas].max()>2*T.std())
        b=p0._best(np.arange(len(C)) if exc else feas,Jv,EQt);selected.append(C[b]);out.append((C[b]+1).tolist())
    return out
def ranked(U):return np.lexsort((np.arange(len(U['C'])),-np.round(U['EQ'],12),-np.round(U['T'],12)))
def diversified(U,first=None,limit=2,n=3):
    out=[] if first is None else [list(first)]
    for i in ranked(U):
        t=(U['C'][i]+1).tolist()
        if all(len(set(t)&set(x))<=limit for x in out):out.append(t)
        if len(out)==n:break
    return out
def rand_tickets(rng,n,fixed=()):
    out=[]
    while len(out)<n:
        t=sorted((rng.choice(38,6,replace=False)+1).tolist())
        if t not in out and t not in fixed:out.append(t)
    return out
# ------------------------------------------------------------------ causal walk-forward
targets=list(range(70,NREC));rows=[];FAMS=['A_long','B_recent','C_gap','D_trend','E_pairs']
for t in targets:
    tgt=records[t]['draw_id'];win=set(np.nonzero(A[t])[0]+1);ft=p0.origin_features(d,t);v1=v1prod[tgt]['numbers']
    W=p0.weights_at(Hh,t);M,EQ,order=p0.discovery(ft[0],W);pool=order[:15];U=build(pool,ft,W,M,EQ);rng=np.random.default_rng(SEED_AUDIT+tgt)
    rk=ranked(U);top=[(U['C'][i]+1).tolist() for i in rk[:3]]
    conc=[sorted(order[:6]),sorted(order[:5]+[order[6]]),sorted(order[:5]+[order[7]])]
    S={'A_coverage_P0':[v1]+coverage_portfolio(U,M,pool,v1,15),
       'B_top3_standalone':top,
       'C_best_plus_2_diversified':diversified(U),
       'D_concentration_top_numbers':conc,
       'E_hybrid_score_coverage':[v1]+coverage_portfolio(U,M,pool,v1,15,hybrid=True),
       'F_V1_plus_2_random':[v1]+rand_tickets(rng,2,[v1]),
       'G_3_random':rand_tickets(np.random.default_rng(SEED_AUDIT+10**6+tgt),3),
       'H_V1_plus_2_zero_overlap_by_T':diversified(U,first=v1,limit=0) if len(diversified(U,first=v1,limit=0))==3 else None}
    if S['H_V1_plus_2_zero_overlap_by_T'] is None:   # pool of 15 minus V1 numbers may not hold 12 disjoint numbers: fill from full ranking
        rest=[x for x in order if x not in v1];S['H_V1_plus_2_zero_overlap_by_T']=[v1,sorted(rest[:6]),sorted(rest[6:12])]
    ev={}
    for k,ts in S.items():
        m=sorted((len(set(x)&win) for x in ts),reverse=True);nb=best_null(ts)
        ev[k]=dict(tickets=ts,matches=m,best=m[0],second=m[1],unique_winners=len(set().union(*map(set,ts))&win),total=sum(m),unique_numbers=len(set().union(*map(set,ts))),
                   null_best_pmf=nb.tolist(),null_best_mean=float(nb@np.arange(7)))
    # construction efficiency (A): winners in pool, best challenger in-pool matches
    inpool=set(pool)&win;ch=S['A_coverage_P0'][1:];chm=sorted((len(set(x)&inpool) for x in ch),reverse=True)
    # ranking metrics
    ranks={}
    inf=[j for j in range(5) if np.std(ft[0][j])>1e-12]
    fam_orders={f:sorted(range(38),key=lambda i:(-round(ft[0][j][i],12),i)) for j,f in enumerate(FAMS) if j in inf}
    fam_orders['P0_order']=[x-1 for x in order];fam_orders['equal_weight']=sorted(range(38),key=lambda i:(-round(EQ[i],12),i))
    fam_orders['G_proxy']=sorted(range(38),key=lambda i:(-round(float(ST[tgt]['g_proxy'][i]),12),i))
    fam_orders['uniform_random']=list(np.random.default_rng(SEED_AUDIT+2*10**6+tgt).permutation(38))
    prior=[h for h in Hh if h['index']<t]
    tr={f:np.mean([h['x'][f] for h in prior[-30:] if h['informative'][f]] or [-9]) for f in FAMS};bm=max(tr,key=tr.get)
    fam_orders['best_trailing30']=fam_orders.get(bm,fam_orders['equal_weight'])
    xs={f:[h['x'][f] for h in prior if h['informative'][f]] for f in FAMS};mu={f:np.mean(v) if v else 0. for f,v in xs.items()};se={f:p0.SIGMA/math.sqrt(len(v)) if v else 1. for f,v in xs.items()}
    act=[f for f in FAMS if len(xs[f])>=20];tau2=max(0.,float(np.var([mu[f] for f in act],ddof=1))-float(np.mean([se[f]**2 for f in act]))) if len(act)>1 else 0.
    wb=np.array([max(0.,mu[f]*tau2/(tau2+se[f]**2)) if f in act else 0. for f in FAMS]);sb=wb@ft[0]
    fam_orders['bayes_empirical']=sorted(range(38),key=lambda i:(-round(sb[i],12),-round(EQ[i],12),i))
    for k,o in fam_orders.items():
        pos=np.empty(38,int);pos[np.array(o)]=np.arange(1,39);wr=[int(pos[w-1]) for w in win]
        ranks[k]=dict(winner_ranks=sorted(wr),capture={N:sum(r<=N for r in wr) for N in [5,10,12,15,18,20,25,30]},mrr=float(np.mean([1/r for r in wr])),
                      ap=float(np.mean([sum(1 for q in wr if q<=r)/r for r in wr])))
    # truncation audit (full-universe T with identical weights, Z over the full universe)
    trunc=None
    if t%4==0 or tgt>=2340:
        scores,mat,means,sd,_=ft;comp={}
        Tf=np.zeros(CN)
        for j,f in enumerate(FAMS):
            if W[f]['w']>0:Tf+=W[f]['w']*p0.Z(scores[j][CALL].mean(1))
        if W['pair']['w']>0:
            I,Jj=np.triu_indices(6,1);Tf+=W['pair']['w']*p0.Z(2*mat[CALL[:,I],CALL[:,Jj]].sum(1)/30)
        if W['struct']['w']>0:Tf+=W['struct']['w']*p0.Z(-np.mean(((a.structure(CALL.astype(np.int64))-means)/sd)**2,axis=1))
        topf=np.argsort(-Tf,kind='stable')[:1000];posn=np.empty(38,int);posn[np.array(order)-1]=np.arange(1,39)
        maxrank=posn[CALL[topf]].max(1)
        bestpool=np.max(Tf[np.all(posn[CALL]<=15,axis=1)]) if np.std(Tf)>0 else 0.
        trunc=dict(weights_nonzero=bool(np.std(Tf)>0),full_top1=(CALL[topf[0]]+1).tolist(),full_top1_max_rank=int(maxrank[0]),
                   share_top1000_inside={K:float(np.mean(maxrank<=K)) for K in [15,18,20,25,30]},
                   full_rank_of_best_top15_ticket=int(np.sum(Tf>bestpool+1e-12))+1)
    # combination-probability inputs: per-number score vectors (for CB likelihood later)
    rows.append(dict(target=tgt,t=t,period='confirmation' if t>=NREC-40 else 'development',winners=sorted(win),v1=v1,pool=pool,order=order,
        weights={k:W[k]['w'] for k in W},strategies=ev,K_in_pool=len(inpool),challenger_inpool_matches=chm,ranks=ranks,best_trailing=bm,truncation=trunc,
        cb_scores=dict(P0_M=M.tolist(),equal_weight=EQ.tolist(),**{f:ft[0][j].tolist() for j,f in enumerate(FAMS)})))
    if tgt%20==0:print(' ',tgt,round(time.time()-t0,1),flush=True)
# sanity: strategy A reproduces the frozen live/historical P0 portfolios
HO={r['target']:r['byK']['15']['portfolio'][1:] for r in J(R/'results/lotto/p0_protocol/historical_origins.json')['rows']}
live={2342:J(R/'results/lotto/draw2342/p0/p0_frozen.json'),2343:J(R/'results/lotto/draw2343/p0/p0_frozen.json')}
mism=[r['target'] for r in rows if r['target'] in HO and [sorted(x) for x in r['strategies']['A_coverage_P0']['tickets'][1:]]!=[sorted(x) for x in HO[r['target']]]]
for t,f in live.items():
    r=[x for x in rows if x['target']==t][0]
    if [r['strategies']['A_coverage_P0']['tickets'][1],r['strategies']['A_coverage_P0']['tickets'][2]]!=[f['ticket_2'],f['ticket_3']]:mism.append(t)
save('walk_forward_rows.json',dict(targets=[rows[0]['target'],rows[-1]['target']],n=len(rows),reproduction_mismatches=mism,seed=SEED_AUDIT,rows=rows))
print('done rows',len(rows),'mismatches',mism,round(time.time()-t0,1))
# ------------------------------------------------------------------ leakage mutation test (A14)
leak=[]
for t in [80,120,160,NREC-1]:
    d2=d.copy();rng=np.random.default_rng(99+t)
    for u in range(t,NREC):d2[u]=np.sort(rng.choice(38,6,replace=False))
    H2=p0.build_history(d2,records)
    ft1=p0.origin_features(d,t);ft2=p0.origin_features(d2,t);W1=p0.weights_at(Hh,t);W2=p0.weights_at(H2,t)
    o1=p0.discovery(ft1[0],W1)[2];o2=p0.discovery(ft2[0],W2)[2]
    c2=V.walk_cache(d2,records);s1=V.state_at_cutoff(d,records,cache,t-1,with_gate=False);s2=V.state_at_cutoff(d2,records,c2,t-1,with_gate=False)
    leak.append(dict(target=records[t]['draw_id'],features_identical=bool(all(np.allclose(x,y) for x,y in zip(ft1[:4],ft2[:4]))),weights_identical=all(abs(W1[k]['w']-W2[k]['w'])<1e-15 for k in W1),
                     p0_order_identical=o1==o2,v1_candidates_identical=[c['numbers'] for c in s1['candidates']]==[c['numbers'] for c in s2['candidates']]))
save('leakage_mutation.json',dict(method='All draws at and after the target index replaced with random draws; every pre-target artifact must be identical.',tests=leak,PASS=all(all(v for k,v in x.items() if k!='target') for x in leak)))
print('leakage',leak,round(time.time()-t0,1))
