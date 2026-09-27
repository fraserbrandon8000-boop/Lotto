import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
R=Path(__file__).resolve().parents[2];O=R/'results/lotto/draw2341'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
f=O/'frozen.json'
if f.exists():print(f.read_text());raise SystemExit
state=load(O/'jev_state.json');meta=load(O/'metadata.json');response=load(O/'jev_response.json');answers=response['answers'];qualifiers=meta['qualifying_models'];conf={r['model']:r for r in state['methodology_confirmation']};ranked=[]
advmax=max([max(conf[m]['delta_random'],0) for m in qualifiers],default=0)
for c in state['candidates']:
    a={k:answers[c['id']+'_'+k] for k in ['robustness','consensus','quality','overfit','stable','stronger','dependent']}
    validated=max([max(conf[m]['delta_random'],0) for m in c['validated_models']],default=0)/(advmax or 1)
    score=.35*validated+.20*c['sensitivity_top_quartile_fraction']+.10*(20-c['ensemble_rank'])/19+.10*a['robustness']['score']/4+.05*a['consensus']['score']/4+.10*a['quality']['score']/4+.10*answers['overall']['probabilities'][c['id']]-.10*a['overfit']['noul']-.05*a['dependent']['noul']
    ranked.append(dict(**c,policy_score=score,eligible=bool(c['validated_models'] and a['stronger']['noul']>=.5 and a['stable']['noul']>=.5)))
eligible=sorted([c for c in ranked if c['eligible']],key=lambda c:(-c['policy_score'],c['id']))
if qualifiers and eligible:selected=eligible[0];rule='edge: original qualified evidence and Jev risk-gated composite rule'
else:
    ordered=sorted(ranked,key=lambda c:c['id']);selected=ordered[int(np.random.default_rng(meta['seed']).integers(len(ordered)))];rule='no-edge: original seeded uniform candidate rule, subject to <=2 overlap constraint'
assert len(set(selected['numbers']))==6 and min(selected['numbers'])>=1 and max(selected['numbers'])<=38
overlap=sorted(set(selected['numbers'])&{5,11,16,24,27,34});assert len(overlap)<=2
now=datetime.now(timezone.utc);assert now<datetime(2026,9,27,1,25,tzinfo=timezone.utc)
manifest=load(R/'results/lotto/v1_manifest.json');assert all(hashlib.sha256((R/p.replace(chr(92),'/')).read_bytes()).hexdigest()==v or hashlib.sha256((R/p.replace(chr(92),'/')).read_bytes().replace(b'\n',b'\r\n')).hexdigest()==v for p,v in manifest['files'].items())
paths=[O/n for n in ['PROTOCOL.txt','draws.json','metadata.json','candidates.json','refreshed_rankings.json','model_performance.json','candidate_sensitivity.json','jev_state.json','jev_request.json','jev_response.json','jev_receipt.json','pool_frozen_pre_jev.json']]+[R/'scripts/analyze.py',R/'scripts/jev.mjs',R/'scripts/research/lotto_prospective.py',R/'scripts/research/lotto_prospective_jev.mjs',Path(__file__)]
out=dict(status='PRE-DRAW / FIRST VALID SELECTION FROZEN',created_utc=now.isoformat(),target_draw=2341,target_date=meta['target_date'],cutoff_draw=2340,numbers=selected['numbers'],candidate_id=selected['id'],generator=selected['generator'],pipeline='V1 unchanged functions and parameters; refreshed data; additional-ticket diversification',rule=rule,overlap=overlap,seed=meta['seed'],jev_model=response['model'],jev_choice_probability=answers['overall']['probabilities'][selected['id']],jev_choice_confidence=answers['overall']['confidence'],jev_preferred_candidate=answers['overall']['choice'],eligible_candidate_count=len(ranked),v1_unchanged=True,hashes={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
with f.open('x',encoding='utf-8') as h:json.dump(out,h,indent=2)
with (R/'results/lotto/prospective_ledger.jsonl').open('a',encoding='utf-8') as h:h.write(json.dumps(dict(event='additional_prediction_frozen',created_utc=out['created_utc'],target_draw=2341,path=str(f.relative_to(R)),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),numbers=out['numbers']))+'\n')
print(json.dumps(out,indent=2))
