"""M0 rolling pseudo-prospective reconstruction over targets #2211-#2343 (research only).
For each target t: models see X[:t] only -> full-universe scores frozen -> THEN actual draw t revealed and scored."""
import sys,json,math,time
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
import m0
R=m0.R;O=R/'results/lotto_m0/data';O.mkdir(parents=True,exist_ok=True)
D,X,ids,dh=m0.load_data();T=len(D);TARGETS=list(range(50,T));t0=time.time()
FAM=['M0-A','M0-B','M0-C','M0-D','M0-E','M0-F','M0-G','M0-H','M0-X']
def build_caches(D,X):return dict(A=m0.a_cache(X),B=m0.b_cache(X),D=m0.d_cache(X),F=m0.f_cache(X),X=m0.x_cache(D))
def run_models(D,X,t,cc,H_weights=None):
    """Returns per-model frozen outputs at target t using only X[:t]/D[:t] (caches are causal per index)."""
    out={}
    a=m0.model_A(X,t,cc['A']);out['M0-A']=dict(L=m0.logodds(a['p']),p=a['p'],params=a['params'])
    b=m0.model_B(X,t,cc['B']);out['M0-B']=dict(L=m0.logodds(b['p']),p=b['p'],params=b['params'])
    c=m0.model_C(X,t);out['M0-C']=dict(L=m0.logodds(c['p']),p=c['p'],params=c['params'])
    dd=m0.model_D(X,t,cc['D']);out['M0-D']=dict(L=m0.logodds(dd['p']),p=dd['p'],params=dd['params'])
    e=m0.model_E(X,t);out['M0-E']=dict(L=m0.logodds(e['p']),p=e['p'],params=e['params'],state=e['state_probs'])
    f=m0.model_F(X,t,cc['F']);out['M0-F']=dict(L=m0.logodds(f['p']),p=f['p'],params=f['params'])
    g=m0.model_G(X,t,cc['A']);out['M0-G']=dict(L=g['L'],W=g['W'],gamma=g['gamma'],params=g['params'])
    w=H_weights if H_weights is not None else {m:0. for m in ['M0-A','M0-B','M0-C','M0-D','M0-E','M0-F']}
    LH=np.full(m0.N,m0.LOGIT0)+sum(w[m]*(out[m]['L']-m0.LOGIT0) for m in w);out['M0-H']=dict(L=LH,p=1/(1+np.exp(-LH)),params=dict(weights=w))
    x=m0.model_X(D,t,cc['X']);out['M0-X']=dict(ticket=x['ticket'],params=x['params'])
    return out
def scores_of(name,o):
    if name=='M0-X':return m0.x_scores(o['ticket']),False
    s=m0.additive(o['L'])
    if name=='M0-G' and o['gamma']>0:s=s+o['gamma']*m0.pair_term(o['W'])
    return s,True
def h_weights(rows,t):
    prior=[r for r in rows if r['t']<t]
    if len(prior)<20:return None
    g={m:np.mean([r['res'][m]['logscore'] for r in prior]) for m in ['M0-A','M0-B','M0-C','M0-D','M0-E','M0-F']}
    pos={m:max(0.,v) for m,v in g.items()};s=sum(pos.values())
    return {m:(v/s if s>0 else 0.) for m,v in pos.items()}
if __name__=='__main__':
    cc=build_caches(D,X);U=m0.universe();actual_idx=[m0.comb_index(D[t].tolist()) for t in TARGETS]
    rows=[];MIS={m:np.zeros((len(TARGETS),len(TARGETS))) for m in FAM}
    print('caches',round(time.time()-t0,1),flush=True)
    for k,t in enumerate(TARGETS):
        hw=h_weights(rows,t);outs=run_models(D,X,t,cc,hw);rec=dict(t=t,draw_id=ids[t],actual=D[t].tolist(),training_end=ids[t-1],res={},frozen={},params={})
        for name in FAM:
            s,norm=scores_of(name,outs[name])
            # ---- freeze first (actual not passed), then reveal
            fr,_=m0.evaluate_scores(s,None,norm)
            _,res=m0.evaluate_scores(s,D[t].tolist(),norm,L=outs[name].get('L'),p=outs[name].get('p'))
            rec['frozen'][name]=fr;rec['res'][name]=res;rec['params'][name]=outs[name]['params']
            ss=np.sort(s);sa=s[actual_idx];lo=np.searchsorted(ss,sa,'left');hi=np.searchsorted(ss,sa,'right');rk=1+(len(ss)-hi)+(hi-lo-1)/2;MIS[name][k]=(rk-.5)/m0.CN
        if 'M0-E' in outs:rec['E_state']=outs['M0-E']['state']
        # ---- nulls (not in family)
        g1=np.random.default_rng(20261008+t);rk=int(g1.integers(1,m0.CN+1));pt=sorted((g1.choice(38,6,replace=False)+1).tolist())
        rec['res']['R1-uniform']=dict(rank=rk,u=(rk-.5)/m0.CN,top={kk:bool(rk<=kk) for kk in [1,10,100,1000,10000,100000]},primary_matches=len(set(pt)&set(D[t].tolist())))
        Lr=np.random.default_rng(20261009+t).random(m0.N);s=m0.additive(Lr);_,rec['res']['R2-random-numbers']=m0.evaluate_scores(s,D[t].tolist(),True,L=Lr)
        rr=int(np.random.default_rng(20261010+t).integers(18));s=m0.x_scores(cc['X']['rules'][t][rr]);_,rec['res']['R3-random-rule']=m0.evaluate_scores(s,D[t].tolist(),False)
        rows.append(rec)
        if k%10==0:print(ids[t],round(time.time()-t0,1),{m:round(rec['res'][m]['u'],3) for m in FAM},flush=True)
    json.dump(dict(dataset_sha256=dh,targets=[ids[TARGETS[0]],ids[TARGETS[-1]]],n=len(TARGETS),rows=rows),open(O/'rolling_results.json','w'),default=lambda o:o.tolist() if hasattr(o,'tolist') else float(o))
    np.savez_compressed(O/'misaligned_u.npz',**{m.replace('-','_'):v for m,v in MIS.items()})
    print('rolling done',round(time.time()-t0,1),flush=True)
    # ---------------- leakage mutation test
    leak=[]
    for t in [80,130,T-1]:
        D2=D.copy();X2=X.copy();g=np.random.default_rng(77+t)
        for u in range(t,T):
            v=np.sort(g.choice(38,6,replace=False));D2[u]=v+1;X2[u]=0;X2[u,v]=1
        c2=build_caches(D2,X2);hw=h_weights(rows,t)
        o1=run_models(D,X,t,cc,hw);o2=run_models(D2,X2,t,c2,hw)
        same={m:(o1[m]['ticket']==o2[m]['ticket'] if m=='M0-X' else bool(np.array_equal(o1[m]['L'],o2[m]['L']))) for m in FAM}
        leak.append(dict(target=ids[t],identical=same))
    json.dump(dict(method='draws at and after the target replaced with random draws; all frozen model outputs at the target must be identical',tests=leak,PASS=all(all(x['identical'].values()) for x in leak)),open(O/'leakage_mutation.json','w'),indent=1)
    print('leak',leak,round(time.time()-t0,1),flush=True)
