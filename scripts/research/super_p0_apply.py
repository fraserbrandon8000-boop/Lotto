"""Apply the FROZEN Super Lotto P0 protocol at a prospective cutoff (no estimation; frozen constants only).
Usage: python3 super_p0_apply.py DRAWS_JSON CUTOFF_ID V1_MAINS(comma) V1_SB OUTDIR"""
import sys,json,csv,hashlib,itertools
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts/research'))
import super_history as S,super_p0 as P
from common import save
PROT=R/'results/super_lotto/p0_protocol/PROTOCOL.json'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def frozen_cred(fc):
    return dict(main={m:dict(c=fc['main_credibility'][m]) for m in P.MAIN},sb={m:dict(c=fc['sb_credibility'][m]) for m in P.SBM},ticket={k:dict(c=v) for k,v in fc['ticket_credibility'].items()})
def apply(draws,cutoff,v1_main,v1_sb,outdir):
    Pr=json.loads(PROT.read_text());fc=Pr['frozen_constants'];K=fc['main_pool_K'];rule=fc['sb_rule']
    for p in ['scripts/research/super_p0.py','scripts/research/super_history.py','scripts/research/super_lotto.py','scripts/research/common.py']:assert Pr['code_sha256'][p]==sha(R/p),f'{p} changed since freeze'
    records,d,sb,ids=S.load(draws);assert ids[-1]==cutoff
    o=S.origin(d,sb,ids,len(d));cred=frozen_cred(fc);disc=P.discovery(o,cred);U=P.universe(o,disc,cred,K);log=P.portfolio(U,disc,v1_main,K)
    sbs=P.assign_sb(rule,disc,v1_sb,cutoff+1);mains=[sorted(v1_main)]+[l['ticket'] for l in log];balls=[v1_sb]+sbs
    O=Path(outdir);O.mkdir(parents=True,exist_ok=True)
    with open(O/'universe_scores.csv','w',newline='') as f:
        w=csv.writer(f);w.writerow(['rank','mains','T','EQ_sum']+list(U['comp']));C=U['C']
        for r,i in enumerate(np.lexsort((np.arange(len(C)),-np.round(U['EQ'],12),-np.round(U['T'],12))),1):w.writerow([r,' '.join(f'{x+1:02}' for x in C[i]),f"{U['T'][i]:.8f}",f"{U['EQ'][i]:.8f}"]+[f"{U['comp'][k][i]:.6f}" for k in U['comp']])
    ov={f'{i+1}-{j+1}':len(set(mains[i])&set(mains[j])) for i,j in itertools.combinations(range(3),2)}
    res=dict(protocol_commit='5cce8a374ab3f9f3c4cf10780628c0ba0ff581fd',protocol_sha256=sha(PROT),cutoff=cutoff,target=cutoff+1,data_sha256=sha(draws),K=K,sb_rule=rule,
             frozen_credibility=dict(main=fc['main_credibility'],sb=fc['sb_credibility'],ticket=fc['ticket_credibility']),
             main_order=disc['order'],pool=U['pool'],M={i+1:float(disc['M'][i]) for i in range(35)},EQ={i+1:float(disc['EQ'][i]) for i in range(35)},
             sb_order=disc['sborder'],Q={b+1:float(disc['Q'][b]) for b in range(10)},EQ_SB={b+1:float(disc['EQS'][b]) for b in range(10)},
             universe_size=len(U['C']),universe_csv_sha256=sha(O/'universe_scores.csv'),
             tickets=[dict(ticket=1,role='V1 Science',mains=mains[0],super_ball=balls[0],mains_inside_pool=sorted(set(mains[0])&set(U['pool'])))]+
                     [dict(ticket=k+2,role='P0 Coverage Challenger',mains=l['ticket'],super_ball=balls[k+1],raw_T=l['T'],T_rank=l['T_rank'],J=l['J'],incremental_coverage=l['coverage'],
                           overlap_limit=l['overlap_limit'],evidence_exception=l['evidence_exception'],family_contributions=l['contributions']) for k,l in enumerate(log)],
             pairwise_main_overlap=ov,unique_mains=len(set().union(*map(set,mains))),distinct_sbs=len(set(balls)),computed_utc=datetime.now(timezone.utc).isoformat())
    save(O/'p0_result.json',res);return res
if __name__=='__main__':
    a=sys.argv;r=apply(a[1],int(a[2]),[int(x) for x in a[3].split(',')],int(a[4]),a[5])
    print(json.dumps({k:r[k] for k in ['K','sb_rule','pool','sb_order','tickets','pairwise_main_overlap','unique_mains','distinct_sbs']},indent=1,default=float))
