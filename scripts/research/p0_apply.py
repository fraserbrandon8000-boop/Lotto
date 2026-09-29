"""Apply the FROZEN P0 protocol (results/lotto/p0_protocol/PROTOCOL.json) at a prospective cutoff.
No parameter is estimated here: weights and K are the frozen constants. Usage:
  python3 p0_apply.py DRAWS_JSON CUTOFF_ID V1_TICKET(comma) OUTDIR [OUTCOME(comma)]"""
import sys,json,hashlib,csv,itertools
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'));sys.path.insert(0,str(R/'scripts/research'))
import analyze as a
import p0,v1_history as V
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
PROT=R/'results/lotto/p0_protocol/PROTOCOL.json'

def apply(draws_path,cutoff,v1,outdir,outcome=None):
    P=json.loads(PROT.read_text());fc=P['frozen_constants'];W=fc['weight_detail'];K=fc['discovery_pool_K']
    assert all(P['code_sha256'][p]==sha(R/p) for p in ['scripts/research/p0.py','scripts/analyze.py']),'P0/V1 code changed since freeze'
    records,d=V.load(draws_path);assert records[-1]['draw_id']==cutoff
    ft=a.model_features(a.indicator(d));wsum=sum(v['w'] for v in W.values())
    M,EQ,order=p0.discovery(ft[0],W);pool=order[:K]
    U=p0.universe(pool,ft,W,M,EQ);U['wsum']=wsum;log=p0.portfolio(U,M,pool,v1,K)
    port=[list(v1)]+[l['ticket'] for l in log]
    O=Path(outdir);O.mkdir(parents=True,exist_ok=True);a.OUT=O
    C=U['C'];rows=[]
    with open(O/'universe_scores.csv','w',newline='') as f:
        w=csv.writer(f);w.writerow(['rank_by_T','numbers','T','EQ']+list(U['comp']))
        idx=np.lexsort((np.arange(len(C)),-np.round(U['EQ'],12),-np.round(U['T'],12)))
        for r,i in enumerate(idx,1):w.writerow([r,' '.join(f'{x+1:02}' for x in C[i]),f"{U['T'][i]:.8f}",f"{U['EQ'][i]:.8f}"]+[f"{U['comp'][k][i]:.6f}" for k in U['comp']])
    def contrib(t):
        i=int(np.nonzero((C==np.array(sorted(t))-1).all(1))[0][0]);return {k:float((W[k]['w'] if k in W else 0)*U['comp'][k][i]) for k in U['comp']},float(U['T'][i]),int(np.sum(U['T']>U['T'][i]))+1
    tickets=[]
    for k,t in enumerate(port):
        e=dict(ticket=k+1,role='V1 Science' if k==0 else 'P0 Coverage Challenger',numbers=sorted(t))
        if k>0:
            cb,T,rk=contrib(t);e.update(raw_T=T,T_rank_in_universe=rk,family_contributions=cb,J=log[k-1]['J'],incremental_coverage=log[k-1]['coverage'],
                                   overlap_limit=log[k-1]['overlap_limit'],evidence_exception=log[k-1]['evidence_exception'])
        else:
            inpool=sorted(set(t)&set(pool));e.update(numbers_inside_pool=inpool,T_if_in_universe=(contrib(t)[1] if len(inpool)==6 else None))
        tickets.append(e)
    ov={f'{i+1}-{j+1}':len(set(port[i])&set(port[j])) for i,j in itertools.combinations(range(3),2)}
    res=dict(protocol_sha256=sha(PROT),protocol_commit='72e1c075c6c09256b78aaa1c70dca2240796e1aa',cutoff=cutoff,target=cutoff+1,data_sha256=sha(draws_path),
             frozen_weights={k:v['w'] for k,v in W.items()},K=K,pool=pool,pool_order_full=order,discovery_M={i+1:float(M[i]) for i in range(38)},discovery_EQ={i+1:float(EQ[i]) for i in range(38)},
             retained_pairs=int(ft[-1]),universe_size=int(len(C)),universe_csv_sha256=sha(O/'universe_scores.csv'),tickets=tickets,pairwise_overlap=ov,
             unique_numbers=len(set().union(*map(set,port))),pool_numbers_covered=len(set().union(*map(set,port))&set(pool)),
             computed_utc=datetime.now(timezone.utc).isoformat())
    if outcome:
        s=p0.port_stats(port,outcome);res['outcome']=outcome;res['scores']=dict(per_ticket=s['matches'],best=s['best'],total=s['total'],
            unique_winners_captured=len(set().union(*map(set,port))&set(outcome)),winners_in_pool=len(set(pool)&set(outcome)))
    return res

if __name__=='__main__':
    dp,cut,v1,out=sys.argv[1],int(sys.argv[2]),[int(x) for x in sys.argv[3].split(',')],sys.argv[4]
    oc=[int(x) for x in sys.argv[5].split(',')] if len(sys.argv)>5 else None
    r=apply(dp,cut,v1,out,oc);a.OUT=Path(out);a.save('p0_result.json',r);print(json.dumps({k:r[k] for k in ['K','pool','tickets','pairwise_overlap','unique_numbers']+(['scores'] if oc else [])},indent=1,default=float))
