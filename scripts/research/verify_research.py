import json,hashlib,math
from pathlib import Path
import numpy as np
import super_lotto as sl
from common import save
R=Path(__file__).resolve().parents[2]
def load(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
manifest=load('results/lotto/v1_manifest.json')
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==v for p,v in manifest['files'].items())
rows=load('results/super_lotto/walk_forward.json')
records=load('results/super_lotto/draws.json')
d=np.array([r['numbers'] for r in records])-1;sb=np.array([r['super_ball'] for r in records])-1;ids=[r['draw_id'] for r in records]
assert len(rows)==126
for r in rows:
    assert r['training_cutoff']<r['draw_id']
    for t,h in zip(r['main_tickets'],r['main_hits']):
        assert len(t)==len(set(t))==5 and min(t)>=1 and max(t)<=35
        assert h==len(set(t)&set((d[r['index']]+1).tolist()))
    assert all(1<=x<=10 for x in r['SB_predictions'])
    assert r['SB_hits']==[int(x==sb[r['index']]+1) for x in r['SB_predictions']]
    assert all(sorted(v)==list(range(1,36)) for v in r['rankings'].values())
# Same horizon and seed; change target and every later outcome. Predictions at
# the mutation origin and earlier must remain identical.
cut=85;mut=d.copy();msb=sb.copy();mut[cut:]=(mut[cut:]+11)%35;msb[cut:]=(msb[cut:]+3)%10
changed,_,_=sl.walk(mut,msb,ids)
for a,b in zip(rows,changed):
    if a['index']>cut:break
    for k in ['main_tickets','SB_predictions','rankings','main_weights','SB_weights']:assert a[k]==b[k],(a['index'],k)
base=load('results/super_lotto/baseline.json');assert abs(sum(base['main_probabilities'])-1)<1e-12
assert abs(base['jackpot_probability']-1/3246320)<1e-15
assert hashlib.sha256(sl.SOURCE.read_bytes()).hexdigest()==load('results/super_lotto/audit.json')['sha256']
for c in load('results/super_lotto/candidates.json'):
    assert len(set(c['main']))==5 and min(c['main'])>=1 and max(c['main'])<=35 and 1<=c['super_ball']<=10
out=dict(passed=True,origins=126,mutation_origin=ids[cut],future_mutation_invariance=True,all_predictions_valid=True,baseline_verified=True,source_unchanged=True,lotto_v1_manifest_unchanged=True)
save(R/'results/super_lotto/verification.json',out);print(json.dumps(out))
