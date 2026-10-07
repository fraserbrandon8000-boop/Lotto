"""M0 Phase 8 complexity/overfit audit: in-sample reconstruction (model fitted on ALL draws #2161-#2343, applied to its own
training targets) vs rolling out-of-sample. Flags HISTORICAL FIT, NOT PREDICTION."""
import sys,json,math
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent));import m0
O=m0.R/'results/lotto_m0/data';D,X,ids,_=m0.load_data();T=len(D);ST=json.load(open(O/'statistics.json'))
sample=list(range(50,T,3));U=m0.universe()
def pct(s,actual):
    i=m0.comb_index(actual);sa=s[i];return (1+(s>sa).sum()+((s==sa).sum()-1)/2-.5)/m0.CN
def pct_many(s,acts):
    ss=np.sort(s);out=[]
    for a in acts:
        sa=s[m0.comb_index(a)];lo=np.searchsorted(ss,sa,'left');hi=np.searchsorted(ss,sa,'right');out.append((1+(len(ss)-hi)+(hi-lo-1)/2-.5)/m0.CN)
    return out
acts=[D[u].tolist() for u in sample];res={}
ca=m0.a_cache(X);a=m0.model_A(X,T,ca);s=m0.additive(m0.logodds(a['p']));res['M0-A']=pct_many(s,acts)
cb=m0.b_cache(X);j=m0.B_K.index(m0.model_B(X,T,cb)['params']['k']);res['M0-B']=[pct(m0.additive(m0.logodds(cb['P'][j,u])),D[u].tolist()) for u in sample]   # hazard bins at u with final pooled rates? (cache uses rates < u)
hz=np.array(m0.model_B(X,T,cb)['hazard']);res['M0-B']=[pct(m0.additive(m0.logodds(hz[m0.b_bin(m0.gaps_before(X,u))])),D[u].tolist()) for u in sample]
us=list(range(2,T));F=np.vstack([m0.c_features(X,u) for u in us]);y=np.concatenate([X[u] for u in us]);w,mu,sd,lam=m0.fit_tuned(F,y,m0.C_GRID)
res['M0-C']=[pct(m0.additive(m0.logodds(m0.pred_logit(w,(m0.c_features(X,u)-mu)/sd))),D[u].tolist()) for u in sample]
fc=m0.f_cache(X);us=list(range(m0.F_START,T));F=np.vstack([fc[u] for u in us]);y=np.concatenate([X[u] for u in us]);w,mu,sd,lam=m0.fit_tuned(F,y,m0.F_GRID)
res['M0-F']=[pct(m0.additive(m0.logodds(m0.pred_logit(w,(fc[u]-mu)/sd))),D[u].tolist()) for u in sample]
# E: in-sample smoothed regime posteriors with K forced to 3 (most flexible member) and the BIC choice
eK={}
for Kst in [1,3]:
    f=max([m0.hmm_fit(X,Kst,s) for s in (11,22,33)],key=lambda z:z['ll']);eK[Kst]=[pct(m0.additive(m0.logodds(f['g'][u]@f['th'])),D[u].tolist()) for u in sample]
res['M0-E (BIC choice K=1)']=eK[1];res['M0-E forced K=3 (smoothed, sees target)']=eK[3]
g=m0.model_G(X,T,ca);sG=m0.additive(g['L'])+(g['gamma']*m0.pair_term(g['W']) if g['gamma']>0 else 0);res['M0-G']=pct_many(sG,acts)
# G with gamma forced to 1 (in-sample pair memorisation)
W=m0.pmi(X,T);sG1=m0.additive(g['L'])+m0.pair_term(W);res['M0-G forced gamma=1 (pairs include target)']=pct_many(sG1,acts)
xc=m0.x_cache(D);ov=np.array([xc['ov'][u] for u in range(2,T)]).mean(0);r=int(np.argmax(ov));res['M0-X']=[pct(m0.x_scores(xc['rules'][u][r]),D[u].tolist()) for u in sample]
oos={m:ST['models'][m]['mean_u'] for m in ST['models'] if m.startswith('M0')};nrm=1.96/math.sqrt(12*ST['n'])
audit={}
for k,v in res.items():
    base=k.split(' ')[0];o=oos.get(base)
    audit[k]=dict(in_sample_mean_u=float(np.mean(v)),n_in_sample=len(v),oos_mean_u=o,effective_params=ST and {'M0-A':2,'M0-B':8,'M0-C':8,'M0-D':3,'M0-E':39,'M0-F':13,'M0-G':3,'M0-H':6,'M0-X':1}.get(base),
                  flag='HISTORICAL FIT, NOT PREDICTION' if (np.mean(v)<.45 and (o is None or o>=.5-nrm)) else 'no overfit flag')
json.dump(dict(method='in-sample: parameters/state fitted on all draws through #2343 and applied to every 3rd training target; OOS: rolling results',audit=audit,
   grid_sensitivity_note='Hyper-parameters chosen at each target are recorded per target in rolling_results.json (params).'),open(O/'overfit_audit.json','w'),indent=1,default=float)
for k,v in audit.items():print(f"{k:45s} in={v['in_sample_mean_u']:.3f} oos={v['oos_mean_u']} {v['flag']}")
