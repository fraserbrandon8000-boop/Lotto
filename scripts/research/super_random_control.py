"""Freeze a Super Lotto 3-ticket random control (research only; not a recommendation). Seed 2026093061, <=1 main overlap, uniform SBs."""
import sys,json,hashlib,argparse,itertools
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts/research'))
import super_p0 as P
ap=argparse.ArgumentParser();[ap.add_argument(x,required=True) for x in ['--target','--deadline-utc']];a=ap.parse_args();T=int(a.target)
O=R/f'results/super_lotto/random_control_{T}';O.mkdir(parents=True,exist_ok=True);now=datetime.now(timezone.utc);assert now<datetime.fromisoformat(a.deadline_utc)
r=np.random.default_rng(P.SEEDS['random_control']);mains=P.rdiv(r,[],3,limit=1);sbs=[int(r.integers(10))+1 for _ in range(3)]
rc=dict(status='PRE-DRAW RANDOM CONTROL FROZEN (research only; NOT a recommended playable portfolio)',created_utc=now.isoformat(),target_draw=T,seed=P.SEEDS['random_control'],
        method='uniform 5-of-35 by rejection sampling until pairwise main overlap <= 1 (P0 rule); independent uniform SBs; numpy default_rng(2026093061)',
        tickets=[dict(mains=m,super_ball=b) for m,b in zip(mains,sbs)],pairwise_main_overlap={f'{i+1}-{j+1}':len(set(mains[i])&set(mains[j])) for i,j in itertools.combinations(range(3),2)},
        unique_mains=len(set().union(*map(set,mains))),distinct_sbs=len(set(sbs)),code_sha256=hashlib.sha256((R/'scripts/research/super_p0.py').read_bytes()).hexdigest())
with open(O/'random_control_frozen.json','x') as h:json.dump(rc,h,indent=2)
s=hashlib.sha256((O/'random_control_frozen.json').read_bytes()).hexdigest();L=R/'results/super_lotto/prospective/ledger.jsonl';prior=L.read_bytes()
with L.open('a',encoding='utf-8') as h:
    for k,t in enumerate(rc['tickets'],1):h.write(json.dumps(dict(event='research_prediction_frozen',track=f'random_control_ticket_{k}',created_utc=rc['created_utc'],target_draw_id=T,selection=t,path=str((O/'random_control_frozen.json').relative_to(R)),sha256=s,status='research_control_not_recommended'))+'\n')
assert L.read_bytes().startswith(prior);print(json.dumps(rc,indent=1))
