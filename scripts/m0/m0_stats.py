"""M0 statistics, null comparisons, Holm family, gate and mechanical model selection (charter rules)."""
import sys,json,math
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent));import m0
O=m0.R/'results/lotto_m0/data';RR=json.load(open(O/'rolling_results.json'));rows=RR['rows'];n=len(rows)
MIS=np.load(O/'misaligned_u.npz')
FAM=['M0-A','M0-B','M0-C','M0-D','M0-E','M0-F','M0-G','M0-H','M0-X'];NULLS=['R1-uniform','R2-random-numbers','R3-random-rule']
NORM={'M0-A','M0-B','M0-C','M0-D','M0-E','M0-F','M0-G','M0-H'}
EFF_PARAMS={'M0-A':2,'M0-B':8,'M0-C':8,'M0-D':3,'M0-E':39,'M0-F':13,'M0-G':3,'M0-H':6,'M0-X':1}
HG=np.array([math.comb(6,k)*math.comb(32,6-k)/m0.CN for k in range(7)])
def holm(p):
    p=np.asarray(p,float);o=np.argsort(p);m=len(p);adj=np.empty(m);run=0
    for i,j in enumerate(o):run=max(run,(m-i)*p[j]);adj[j]=min(1,run)
    return adj
def block_ci(y,seed=20261013,reps=10000,b=5):
    y=np.asarray(y,float);r=np.random.default_rng(seed);ix=(r.integers(0,len(y),(reps,math.ceil(len(y)/b)))[:,:,None]+np.arange(b))%len(y)
    return np.quantile(y[ix.reshape(reps,-1)[:,:len(y)]].mean(1),[.025,.975]).tolist()
def conv_ge(obs,k):
    q=np.array([1.])
    for _ in range(k):q=np.convolve(q,HG)
    return float(q[int(obs):].sum())
def tp(x):  # one-sided t-test p for mean > 0
    x=np.asarray(x,float);se=x.std(ddof=1)/math.sqrt(len(x));z=x.mean()/se if se>0 else 0;return float(0.5*math.erfc(z/math.sqrt(2)))
S={};tests=[]
for m in FAM+NULLS:
    res=[r['res'][m] for r in rows];u=np.array([x['u'] for x in res]);rk=np.array([x['rank'] for x in res]);h=n//2
    z=(0.5-u.mean())/(math.sqrt(1/12)/math.sqrt(n));pu=float(0.5*math.erfc(z/math.sqrt(2)))
    pm=np.array([x['primary_matches'] for x in res])
    st=dict(n=n,mean_u=float(u.mean()),median_rank=float(np.median(rk)),mean_rank=float(rk.mean()),expected_rank=(m0.CN+1)/2,rank_improvement_pct=float(100*(1-np.median(rk)/((m0.CN+1)/2))),
        p_u=pu,halves_u=[float(u[:h].mean()),float(u[h:].mean())],block95_u=block_ci(u),
        topK={K:dict(hits=int(sum(x['top'][str(K)] if str(K) in x['top'] else x['top'][K] for x in res)),expected=n*K/m0.CN,
                     p=float(1-sum(math.comb(n,j)*(K/m0.CN)**j*(1-K/m0.CN)**(n-j) for j in range(int(sum(x['top'][str(K)] if str(K) in x['top'] else x['top'][K] for x in res)))))) for K in [1,10,100,1000,10000,100000]},
        primary_matches_mean=float(pm.mean()),primary_matches_dist={k:int((pm==k).sum()) for k in range(7)},p_matches=conv_ge(pm.sum(),n),expected_matches=36/38)
    for key in ['best_top10','best_top100','best_top1000']:
        if key in res[0]:st[key]=float(np.mean([x[key] for x in res]))
    if m in NORM or m=='R2-random-numbers':
        ls=np.array([x['logscore'] for x in res]);st['mean_logscore']=float(ls.mean());st['p_logscore']=tp(ls);st['block95_logscore']=block_ci(ls)
    if 'winner_ranks' in res[0]:
        st['mean_winner_rank']=float(np.mean([np.mean(x['winner_ranks']) for x in res]));st['capture']={k:float(np.mean([x['capture'][str(k)] if str(k) in x['capture'] else x['capture'][k] for x in res])) for k in [6,10,15,20]}
        st['capture_null']={k:6*k/38 for k in [6,10,15,20]}
    if 'logloss' in res[0]:st['logloss']=float(np.mean([x['logloss'] for x in res]));st['brier']=float(np.mean([x['brier'] for x in res]));st['logloss_uniform']=float(-(6/38*math.log(6/38)+32/38*math.log(32/38)));st['brier_uniform']=float(6/38*32/38)
    if m in FAM:
        M=MIS[m.replace('-','_')];obs=float(np.mean(np.diag(M)));g=np.random.default_rng(20261011);perm=[]
        for _ in range(1000):
            pi=g.permutation(n);perm.append(float(M[np.arange(n),pi].mean()))
        st['permutation_null']=dict(observed_mean_u=obs,null_mean=float(np.mean(perm)),p=float((1+sum(v<=obs for v in perm))/1001))
        tests+= [(m,'u',pu),(m,'matches',st['p_matches'])]+([(m,'logscore',st['p_logscore'])] if m in NORM else [])
    S[m]=st
adj=holm([t[2] for t in tests]);HOLM={f'{a}:{b}':float(h) for (a,b,_),h in zip(tests,adj)}
for m in FAM:
    st=S[m];st['holm']={k.split(':')[1]:v for k,v in HOLM.items() if k.startswith(m+':')}
    st['gate']=dict(holm_u_lt_05=st['holm']['u']<.05,both_halves_lt_05=all(x<.5 for x in st['halves_u']),block95_upper_lt_05=st['block95_u'][1]<.5,beats_permutation=st['permutation_null']['p']<.05)
    st['PASS']=all(st['gate'].values())
passing=[m for m in FAM if S[m]['PASS']]
sel=sorted(FAM,key=lambda m:(round(S[m]['mean_u'],12),EFF_PARAMS[m],m))[0]
out=dict(n=n,targets=RR['targets'],dataset_sha256=RR['dataset_sha256'],family=FAM,holm_family_size=len(tests),holm=HOLM,models=S,passing=passing,
  verdict='EDGE' if passing else 'NO EDGE',statement=None if passing else 'M0 HAS NOT DEMONSTRATED A PREDICTIVE RECONSTRUCTION EDGE.',
  selection=dict(rule='lowest out-of-sample mean u; ties: fewer effective parameters, then ID (charter)',selected=sel,ranking=[(m,S[m]['mean_u']) for m in sorted(FAM,key=lambda m:S[m]['mean_u'])]))
json.dump(out,open(O/'statistics.json','w'),indent=1,default=float)
for m in FAM+NULLS:
    s=S[m];print(f"{m:18s} u={s['mean_u']:.4f} p={s['p_u']:.3f} medrank={s['median_rank']:.0f} top1e4={s['topK'][10000]['hits']} top1e5={s['topK'][100000]['hits']} pm={s['primary_matches_mean']:.3f} pmP={s['p_matches']:.3f} ls={s.get('mean_logscore','-')} perm={s.get('permutation_null',{}).get('p','-')} holm_u={s.get('holm',{}).get('u','-')} PASS={s.get('PASS','-')}")
print('passing',passing,'selected',sel)
