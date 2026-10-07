"""M0 Phase 1: legitimate draw representations and their behaviour vs exact nulls (descriptive; causal where state-based).
Extraction (physical draw) order is NOT available in the data: sorted positions are a representation only."""
import sys,json,math,itertools
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent));import m0
D,X,ids,dh=m0.load_data();T=len(D);O=m0.R/'results/lotto_m0/data'
hg=lambda k,n=6,K=6,N=38:math.comb(K,k)*math.comb(N-K,n-k)/math.comb(N,n)
allc=np.array(list(itertools.combinations(range(1,39),6)))
rep={}
# A/B/C/D: set, binary, sorted, gap vector
gv=np.diff(D,axis=1);gnull=np.diff(allc,axis=1)
rep['C_sorted_vector']=dict(mean_by_position=D.mean(0).tolist(),null_mean_by_position=allc.mean(0).tolist())
rep['D_gap_vector']=dict(mean=gv.mean(0).tolist(),null_mean=gnull.mean(0).tolist(),sd=gv.std(0).tolist(),null_sd=gnull.std(0).tolist())
rep['B_binary_vector']=dict(number_frequency=X.sum(0).tolist(),expected=T*6/38,chi2=float(((X.sum(0)-T*6/38)**2/(T*6/38)).sum()),df=37)
# E: transition vs previous draw
ret=np.array([len(set(D[t])&set(D[t-1])) for t in range(1,T)]);nn=[]
for t in range(1,T):nn+= [min(abs(x-y) for y in D[t-1]) for x in D[t]]
nnull=[];rng=np.random.default_rng(1)
for _ in range(20000):
    a=np.sort(rng.choice(38,6,replace=False))+1;b=np.sort(rng.choice(38,6,replace=False))+1;nnull+= [min(abs(x-y) for y in b) for x in a]
rep['E_transition_prev']=dict(retained_counts={k:int((ret==k).sum()) for k in range(7)},retained_expected={k:(T-1)*hg(k) for k in range(7)},mean_retained=float(ret.mean()),null_mean=36/38,
   nearest_distance_dist={d:float(np.mean(np.array(nn)==d)) for d in range(0,6)},nearest_distance_null={d:float(np.mean(np.array(nnull)==d)) for d in range(0,6)})
# F: transitions vs last K draws (union coverage)
for Kk in [2,3,5,10]:
    ov=[len(set(D[t])&set(D[t-Kk:t].ravel())) for t in range(Kk,T)];U=[len(set(D[t-Kk:t].ravel())) for t in range(Kk,T)]
    rep[f'F_overlap_with_last_{Kk}']=dict(mean=float(np.mean(ov)),null_mean=float(np.mean([6*u/38 for u in U])))
# G: number-rank state (causal frequency rank at the time of the draw)
pr=[]
for t in range(30,T):
    f=X[:t].sum(0)+np.random.default_rng(t).random(38)*1e-6;rk=np.argsort(np.argsort(-f))+1;pr+= [rk[x-1] for x in D[t]]
rep['G_rank_state']=dict(mean_rank_of_drawn=float(np.mean(pr)),null=19.5,n=len(pr))
# H: co-occurrence state (causal mean prior lift among drawn pairs)
lifts=[]
for t in range(30,T):
    c=X[:t].T@X[:t];E=t*(6/38)*(5/37);lifts.append(np.mean([c[i-1,j-1]/E for i,j in itertools.combinations(D[t],2)]))
rep['H_cooccurrence_state']=dict(mean_prior_pair_lift_of_drawn_pairs=float(np.mean(lifts)),null_approx=1.0)
# I: rolling latent state (HMM K by BIC at the last cutoff)
e=m0.model_E(X,T);rep['I_latent_state']=dict(K_selected_by_BIC=e['params']['K'],note='K=1 means no latent regime structure is supported by BIC on the full history')
# J: set-to-set transformations (X library mean overlap over all transitions, descriptive)
xc=m0.x_cache(D);ovs=np.array([xc['ov'][u] for u in range(2,T)]);rep['J_set_transformations']=dict(rule_mean_overlap=ovs.mean(0).tolist(),null=36/38,best_rule=int(np.argmax(ovs.mean(0))),best_mean=float(ovs.mean(0).max()))
rep['extraction_order']='Not available: the source provides each draw as an unordered/sorted set. No representation uses physical ball order.'
json.dump(rep,open(O/'representations.json','w'),indent=1,default=float)
print(json.dumps({k:(v if len(json.dumps(v,default=float))<300 else '...') for k,v in rep.items()},indent=1,default=float))
