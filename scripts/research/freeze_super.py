import json,hashlib,math
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
from common import clean
R=Path(__file__).resolve().parents[2];O=R/'results/super_lotto';P=O/'prospective';P.mkdir(exist_ok=True)
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
target=P/'prediction_1753.json'
if target.exists():
    print(json.dumps(load(target)['selection']));raise SystemExit
assert load(O/'verification.json')['passed']
meta=load(O/'metadata.json');cs=load(O/'candidates.json');jev=load(O/'jev_response.json');answers=jev['answers']
eligible=[c for c in cs if c['qualified_models']]
def strength(c):
    total=0
    for key,base,sd in [('main_support',5/7,math.sqrt(5*(5/35)*(30/35)*(30/34))),('SB_support',.1,.3)]:
        if c[key]['qualifies']:total+=(c[key]['mean']-base)/sd
    return (-total,-answers[c['id']+'_quality']['score'],-answers[c['id']+'_robustness']['score'],-answers['overall']['probabilities'][c['id']],c['id'])
if eligible:selected=sorted(eligible,key=strength)[0];policy='qualified evidence rule'
else:selected=cs[int(np.random.default_rng(meta['seed']).integers(len(cs)))];policy='predeclared seeded uniform candidate no-edge rule'
now=datetime.now(timezone.utc);deadline=datetime(2026,9,23,1,30,tzinfo=timezone.utc)
assert now<deadline,'Cannot label prediction PRE-DRAW after scheduled draw time'
assert meta['cutoff']['draw_id']==1752
paths=list((R/'scripts/research').glob('*.py'))+[R/'scripts/research/super_jev.mjs']+[O/n for n in ['PROTOCOL.md','metadata.json','candidates.json','jev_request.json','jev_response.json','predraw_rankings_and_fit.json','verification.json']]
# Only Super Lotto and generic code hashes are part of this prediction.
paths=[p for p in paths if p.name not in ['lotto_forensic.py']]
obj=dict(status='PRE-DRAW',created_utc=now.isoformat(),target_draw_id=1753,target_date='2026-09-22',scheduled_time_jamaica='20:30',selection=dict(candidate_id=selected['id'],main=selected['main'],super_ball=selected['super_ball']),selection_policy=policy,statistical_edge_detected=bool(eligible),model_version='super-lotto-v1',jev_model=jev['model'],seed=meta['seed'],data_cutoff=meta['cutoff'],configuration=meta['configuration'],source_sha256=meta['source_sha256'],full_predraw_fit_and_rankings=load(O/'predraw_rankings_and_fit.json'),jev_response=jev,hashes={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
with target.open('x',encoding='utf-8') as f:json.dump(clean(obj),f,indent=2,allow_nan=False)
digest=hashlib.sha256(target.read_bytes()).hexdigest()
with (P/'ledger.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(dict(event='prediction_frozen',created_utc=obj['created_utc'],target_draw_id=1753,path=target.name,sha256=digest,selection=obj['selection']))+'\n')
print(json.dumps(dict(selection=obj['selection'],created_utc=obj['created_utc'],policy=policy)))
