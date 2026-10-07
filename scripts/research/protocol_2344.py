"""Lotto Protocol 2344 — tickets 2-3 "ALIGNED COVERAGE" constructor (objective-alignment correction of P0).
Single parameterised entry point (no draw-specific constants). Uses unchanged V1 features (scripts/analyze.py),
unchanged P0 discovery/component definitions (scripts/research/p0.py) and the P0 weights frozen in
results/lotto/p0_protocol/PROTOCOL.json. Changes ONLY the construction objective:
  * every one of the C(38,6) = 2,760,681 combinations is scored (no Top-K cutoff);
  * components are Z-normalised over the full universe;
  * ticket 2 = highest-ranked combination sharing NO number with ticket 1;
    ticket 3 = highest-ranked combination sharing NO number with tickets 1 and 2;
  * ranking key: T desc, then EQ desc, then lexicographic enumeration order.
The score T is an UNVALIDATED tie-break (no predictive edge); the disjointness rule is the objective-aligned part.
Usage: python3 protocol_2344.py --draws DRAWS_JSON --cutoff ID --v1 a,b,c,d,e,f --out DIR [--shadow]"""
import sys,json,math,itertools,hashlib,argparse
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'));sys.path.insert(0,str(R/'scripts/research'))
import analyze as a,p0
CN=math.comb(38,6);_CALL=None
def universe_array():
    global _CALL
    if _CALL is None:_CALL=np.array(list(itertools.combinations(range(38),6)),dtype=np.int8)
    return _CALL
def frozen_weights():
    P=json.loads((R/'results/lotto/p0_protocol/PROTOCOL.json').read_text())['frozen_constants']['weight_detail']
    return {k:dict(w=float(v['w'])) for k,v in P.items()}
def score_universe(ft,W):
    """T for every combination (same components as p0.universe, Z over the full universe) and EQ(t)."""
    C=universe_array();scores,mat,means,sd,_=ft;T=np.zeros(CN)
    for j,f in enumerate(p0.FAM):
        if W[f]['w']>0:T+=W[f]['w']*p0.Z(scores[j][C].mean(1))
    if W['pair']['w']>0:
        I,Jj=np.triu_indices(6,1);T+=W['pair']['w']*p0.Z(2*mat[C[:,I],C[:,Jj]].sum(1)/30)
    if W['struct']['w']>0:T+=W['struct']['w']*p0.Z(-np.mean(((a.structure(C.astype(np.int64))-means)/sd)**2,axis=1))
    M,EQ,order=p0.discovery(scores,W);EQt=EQ[C].mean(1)
    return T,EQt,M,EQ,order
def ranking(T,EQt):
    return np.lexsort((np.arange(CN),-np.round(EQt,12),-np.round(T,12)))
def disjoint_tickets(rk,v1,n=2):
    C=universe_array();used=np.zeros(38,bool);used[np.array(v1)-1]=True;out=[];pos=[]
    for _ in range(n):
        ok=~used[C].any(1)
        cand=rk[ok[rk]];b=int(cand[0]);pos.append(int(np.nonzero(rk==b)[0][0])+1)
        t=(C[b]+1).tolist();out.append(t);used[np.array(t)-1]=True
    return out,pos
def construct(ft,W,v1):
    T,EQt,M,EQ,order=score_universe(ft,W);rk=ranking(T,EQt);tickets,pos=disjoint_tickets(rk,v1)
    return dict(tickets=tickets,full_universe_ranks=pos,T=[float(T[rk[p-1]]) for p in pos],order=order,T_arr=T,EQt=EQt,rk=rk,M=M,EQ=EQ)
def concentration_shadow(res):
    """P1 SHADOW (research only): the three highest-ranked distinct combinations, no diversity rule = jackpot-optimal IF T were a calibrated combination probability."""
    C=universe_array();return [(C[i]+1).tolist() for i in res['rk'][:3]]
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--draws',required=True);ap.add_argument('--cutoff',type=int,required=True);ap.add_argument('--v1',required=True);ap.add_argument('--out',required=True);ap.add_argument('--shadow',action='store_true')
    A=ap.parse_args();O=Path(A.out);O.mkdir(parents=True,exist_ok=True);v1=sorted(int(x) for x in A.v1.split(','))
    assert len(set(v1))==6 and all(1<=x<=38 for x in v1)
    recs=json.loads(Path(A.draws).read_text());assert recs[-1]['draw_id']==A.cutoff
    d=np.array([r['numbers'] for r in recs])-1;ft=a.model_features(a.indicator(d));W=frozen_weights()
    res=construct(ft,W,v1);C=universe_array();rk=res['rk']
    uh=hashlib.sha256(np.round(res['T_arr'],12).tobytes()+np.round(res['EQt'],12).tobytes()).hexdigest()
    top=[dict(rank=i+1,numbers=(C[j]+1).tolist(),T=float(res['T_arr'][j]),EQ=float(res['EQt'][j])) for i,j in enumerate(rk[:200])]
    out=dict(protocol='Lotto Protocol 2344 ALIGNED COVERAGE (tickets 2-3)',cutoff=A.cutoff,target=A.cutoff+1,data_sha256=hashlib.sha256(Path(A.draws).read_bytes()).hexdigest(),
      weights={k:v['w'] for k,v in W.items()},universe_size=CN,universe_score_sha256=uh,v1_ticket=v1,
      tickets=[dict(ticket=k+2,numbers=t,full_universe_rank=p,T=tt,overlap_with_previous=0) for k,(t,p,tt) in enumerate(zip(res['tickets'],res['full_universe_ranks'],res['T']))],
      number_order=res['order'],M={i+1:float(res['M'][i]) for i in range(38)},EQ={i+1:float(res['EQ'][i]) for i in range(38)},top200=top,computed_utc=datetime.now(timezone.utc).isoformat())
    if A.shadow:out['p1_shadow_concentration']=concentration_shadow(res)
    (O/'aligned_result.json').write_text(json.dumps(a.clean(out),indent=1))
    print(json.dumps({k:out[k] for k in ['cutoff','universe_score_sha256','tickets','weights']}|({'shadow':out['p1_shadow_concentration']} if A.shadow else {}),indent=1))
