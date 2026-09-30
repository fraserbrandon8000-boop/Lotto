"""Freeze Super Lotto P0 tickets 2-3 for a target after the V1 ticket is frozen (frozen protocol only)."""
import sys,json,hashlib,argparse
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts/research'))
import super_p0_apply as A
ap=argparse.ArgumentParser();[ap.add_argument(x,required=True) for x in ['--dir','--target','--deadline-utc']];a=ap.parse_args();T=int(a.target);O=R/a.dir
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
v1=json.loads((R/f'results/super_lotto/prospective/prediction_{T}.json').read_text());sel=v1['selection']
now=datetime.now(timezone.utc);assert now<datetime.fromisoformat(a.deadline_utc)
assert not (O/'p0'/'p0_frozen.json').exists(),'P0 already frozen'
res=A.apply(O/'draws.json',T-1,sel['main'],sel['super_ball'],O/'p0')
assert res['tickets'][0]['mains']==sorted(sel['main']) and res['tickets'][0]['super_ball']==sel['super_ball']
fz=dict(status='PRE-DRAW / SUPER LOTTO P0 PORTFOLIO FROZEN (research challenger; not V2)',created_utc=datetime.now(timezone.utc).isoformat(),target_draw=T,cutoff_draw=T-1,
        protocol_commit=res['protocol_commit'],protocol_sha256=res['protocol_sha256'],ticket_1_v1=dict(candidate=sel['candidate_id'],mains=sorted(sel['main']),super_ball=sel['super_ball'],prediction_sha256=sha(R/f'results/super_lotto/prospective/prediction_{T}.json')),
        ticket_2=dict(mains=res['tickets'][1]['mains'],super_ball=res['tickets'][1]['super_ball']),ticket_3=dict(mains=res['tickets'][2]['mains'],super_ball=res['tickets'][2]['super_ball']),
        K=res['K'],pool=res['pool'],universe_size=res['universe_size'],sb_rule=res['sb_rule'],pairwise_main_overlap=res['pairwise_main_overlap'],unique_mains=res['unique_mains'],distinct_sbs=res['distinct_sbs'],
        hashes={n:sha(O/'p0'/n) for n in ['p0_result.json','universe_scores.csv']}|{p:sha(R/p) for p in ['scripts/research/super_p0.py','scripts/research/super_p0_apply.py','scripts/research/super_p0_freeze.py']})
with open(O/'p0'/'p0_frozen.json','x') as h:json.dump(fz,h,indent=2)
L=R/'results/super_lotto/prospective/ledger.jsonl';prior=L.read_bytes()
with L.open('a',encoding='utf-8') as h:
    for k in (2,3):h.write(json.dumps(dict(event='research_prediction_frozen',track=f'P0_coverage_ticket_{k}',created_utc=fz['created_utc'],target_draw_id=T,selection=fz[f'ticket_{k}'],path=str((O/'p0'/'p0_frozen.json').relative_to(R)),sha256=sha(O/'p0'/'p0_frozen.json'),status='research_challenger_not_V1'))+'\n')
assert L.read_bytes().startswith(prior);print(json.dumps(fz,indent=1))
