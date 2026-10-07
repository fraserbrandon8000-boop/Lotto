"""A2 objective audit: exact enumeration over all C(38,6) equally likely draws of P(best ticket >= k) for 3-ticket
portfolios with different overlap structures. Pure combinatorics; no draw data. Output data/a2_objective.json"""
import json,math,itertools
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];O=R/'results/lotto/system_audit_2344/data'
CALL=np.array(list(itertools.combinations(range(38),6)),dtype=np.int8);CN=len(CALL)
def m(t):
    v=np.zeros(38,np.int8);v[np.array(t)-1]=1;return v[CALL].sum(1,dtype=np.int8)
T1=[1,2,3,4,5,6]
P={'zero_overlap (18 numbers)':[T1,[7,8,9,10,11,12],[13,14,15,16,17,18]],
   'one_shared_each (pairwise 1)':[T1,[6,7,8,9,10,11],[11,12,13,14,15,1]],
   'frozen_2343_structure (0,2,0)':[[1,4,13,14,24,38],[2,6,7,8,12,22],[4,9,10,13,18,33]],
   'pairwise 2 (coverage-style)':[T1,[5,6,7,8,9,10],[9,10,11,12,1,2]],
   'pairwise 3':[T1,[4,5,6,7,8,9],[7,8,9,1,2,3]],
   'concentration (5 shared)':[T1,[1,2,3,4,5,7],[1,2,3,4,5,8]],
   'three identical tickets':[T1,T1,T1]}
out={}
for k,ts in P.items():
    M=np.stack([m(t) for t in ts]);best=M.max(0);distinct=len({tuple(t) for t in ts})
    out[k]=dict(tickets=ts,distinct=distinct,unique_numbers=len(set().union(*map(set,ts))),
      P_six=float(np.mean(best==6)),P_six_formula=f'{distinct}/C(38,6)',P_ge5=float(np.mean(best>=5)),P_ge4=float(np.mean(best>=4)),P_ge3=float(np.mean(best>=3)),E_best=float(best.mean()),
      E_total=float(M.sum(0).mean()),E_unique_winners=float(np.mean((M>0).sum(0)) if False else np.mean(np.array([len(set(np.nonzero(np.isin(np.arange(38),np.array(list(set().union(*map(set,ts))))-1))[0])) for _ in [0]]))))
    # unique winners covered: number of drawn numbers inside the union
    U=np.zeros(38,np.int8);U[np.array(sorted(set().union(*map(set,ts))))-1]=1;out[k]['E_unique_winners']=float(U[CALL].sum(1).mean())
single=np.array([math.comb(6,j)*math.comb(32,6-j)/CN for j in range(7)])
res=dict(universe=CN,single_ticket_pmf=single.tolist(),portfolios=out,
  theorem='For distinct tickets the events {draw = ticket_i} are disjoint, so P(at least one 6/6) = sum_i P(draw = ticket_i). Under a uniform draw this is (number of distinct tickets)/C(38,6) for ANY overlap structure; overlap, coverage and number spread do not enter.',
  verified_by_enumeration=all(abs(v['P_six']-v['distinct']/CN)<1e-15 for v in out.values()))
(O/'a2_objective.json').write_text(json.dumps(res,indent=1))
for k,v in out.items():print(f"{k:34s} distinct={v['distinct']} uniq={v['unique_numbers']:2d} P6={v['P_six']:.4e} P5+={v['P_ge5']:.4e} P4+={v['P_ge4']:.5f} P3+={v['P_ge3']:.5f} Ebest={v['E_best']:.4f} Etotal={v['E_total']:.3f} Euniq={v['E_unique_winners']:.3f}")
print('verified',res['verified_by_enumeration'])
