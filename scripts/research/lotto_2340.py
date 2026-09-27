"""Refresh unchanged V1 functions into an isolated #2340 additional-ticket run."""
import sys,json,hashlib
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'))
import analyze as a
O=R/'results/lotto/draw2340';O.mkdir(exist_ok=True);a.OUT=O
if (O/'frozen.json').exists():
    print((O/'frozen.json').read_text());raise SystemExit
protocol='Unchanged V1 model functions, parameters, candidate generator and seed 20260919. Append only official #2339; no forensic V2 methods. Refresh original rolling confirmation definition and sensitivity. Generate the original twenty candidates, then restrict final selection and Jev to candidates with <=2 shared numbers with previous primary [1,4,13,14,24,38]. Do not minimize overlap further. Apply original empirical/Jev gate and composite score; if none qualify, seeded uniform selection among eligible diversified candidates sorted by ID, using original seed. Freeze first valid result for #2340 on 2026-09-23. No reselection. Neither V1 snapshot nor original data/results are overwritten. Jev judgments are not winning probabilities.'
if not (O/'PROTOCOL.txt').exists():(O/'PROTOCOL.txt').write_text(protocol,encoding='utf-8')
manifest=json.loads((R/'results/lotto/v1_manifest.json').read_text())
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==v for p,v in manifest['files'].items())
records=json.loads((R/'data/draws.json').read_text());assert records[-1]['draw_id']==2338
official=json.loads((R/'results/lotto/official-current.json').read_text())[0]['Evening'];assert official['drawNumber']=='2339'
record=dict(draw_id=2339,date=official['drawDate'],numbers=sorted(map(int,official['winNumber'].split())),bonus=int(official['bonusBall']),origin='official_archive',source='https://supremeventures.com/past-results/',raw_file='results/lotto/official-current.json')
assert record['numbers']==[1,4,6,13,23,28];records.append(record);a.save('draws.json',records)
d=np.array([r['numbers'] for r in records])-1
nums,pairs,_=a.exploratory(d,records)
rows=a.walk(d,records,details=True);a.save('walk_forward_predictions.json',rows)
for r in rows:
    assert r['training_last_draw_id']<r['draw_id']
    for t,h in zip(r['tickets'],r['matches']):assert len(set(t))==6 and min(t)>=1 and max(t)<=38 and len(set(t)&set(records[r['index']]['numbers']))==h
summary=a.summaries(rows);a.save('model_performance.json',summary)
_,variants=a.sensitivity(d,records,rows);cs=a.candidates(d,records,summary,rows,variants,nums,pairs)
previous={1,4,13,14,24,38}
for c in cs:c['overlap_previous_primary']=sorted(set(c['numbers'])&previous)
a.save('candidates.json',cs);eligible=[c for c in cs if len(c['overlap_previous_primary'])<=2];assert eligible
ft=a.model_features(a.indicator(d));weights=a.ensemble_weights([r['matches'] for r in rows]);scores={n:ft[0][i] for i,n in enumerate(a.NAMES[:5])};scores['G_marginal_proxy']=weights[:5]@ft[0]
a.save('refreshed_rankings.json',{n:dict(scores=s,order=(np.argsort(-(s+np.random.default_rng(a.SEED+2340).random(38)*1e-10))+1),informative=bool(np.std(s)>1e-12)) for n,s in scores.items()})
meta=dict(cutoff_draw=2339,target_draw=2340,target_date='2026-09-23',seed=a.SEED,qualifying_models=[r['model'] for r in summary if r['qualifies']],origins=len(rows),data_sha256=hashlib.sha256((O/'draws.json').read_bytes()).hexdigest(),v1_code_sha256=hashlib.sha256((R/'scripts/analyze.py').read_bytes()).hexdigest(),limitations=['No candidate-specific or Jev policy predictive validation.','Reused retrospective confirmation; no new holdout.'])
a.save('metadata.json',meta)
a.save('jev_state.json',dict(task='Evaluate the refreshed empirical evidence for one additional Lotto #2340 complete ticket.',metadata=meta,baseline=dict(expected_matches=a.BASE,jackpot_probability=1/2760681),methodology_confirmation=[r for r in summary if r['period']=='confirmation'],candidates=eligible,diversification=dict(previous_primary=sorted(previous),maximum_shared=2,do_not_prefer_zero_overlap=True),interpretation='No winning advantage without corrected evidence. Model agreement is correlated. Use only supplied Lotto evidence; never infer a signal from a single previous ticket result. Jev is advisory under the no-edge rule.'))
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==v for p,v in manifest['files'].items())
print(json.dumps(dict(qualifiers=meta['qualifying_models'],candidate_count=len(cs),diversified_candidates=len(eligible),v1_unchanged=True)))
