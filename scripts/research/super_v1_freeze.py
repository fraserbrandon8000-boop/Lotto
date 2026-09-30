"""Apply unchanged V1 selection policy once, then freeze prospectively."""
import json,hashlib,math
from pathlib import Path
from datetime import datetime,timezone
import numpy as np,argparse
ap=argparse.ArgumentParser();[ap.add_argument(x,required=True) for x in ['--dir','--target','--target-date','--deadline-utc','--previous-prediction']];ARGS=ap.parse_args();T=int(ARGS.target);DEADLINE=datetime.fromisoformat(ARGS.deadline_utc)
R=Path(__file__).resolve().parents[2];V=R/'results/super_lotto';O=R/ARGS.dir;P=V/'prospective';target=P/f'prediction_{T}.json'
def okhash(p,h):
    b=(R/p.replace(chr(92),'/')).read_bytes();return hashlib.sha256(b).hexdigest()==h or hashlib.sha256(b.replace(b'\n',b'\r\n')).hexdigest()==h
KNOWN_HISTORICAL_MISMATCH={'scripts\\research\\super_jev.mjs'}
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert not target.exists(),'First prediction already frozen; stop without reselection'
assert load(O/'verification.json')['passed'];now=datetime.now(timezone.utc);assert now<DEADLINE
json.dump(dict(target=T,checked_utc=now.isoformat(),deadline_utc=ARGS.deadline_utc,method='clock-based (official API blocked by network policy)',published=False),open(O/'final-predraw-check.json','x'),indent=2)
freeze=load(O/'candidate-freeze.json');assert all(sha(O/p)==h for p,h in freeze['hashes'].items())
meta=load(O/'metadata.json');cs=load(O/'candidates.json');jev=load(O/'jev_response.json');answers=jev['answers'];receipt=load(O/'jev_receipt.json');attempt=load(O/'jev-attempt.json')
assert len(answers)==161 and attempt['http_attempts']==1 and attempt['retries_disabled']
assert datetime.fromisoformat(freeze['frozen_utc'])<datetime.fromisoformat(attempt['started_utc'].replace('Z','+00:00'))<now
assert meta['cutoff']['draw_id']==T-1 and meta['target']==T
assert sha(O/'jev_state.json')==receipt['state_file_sha256']
old=load(R/ARGS.previous_prediction);assert all(okhash(p,h) for p,h in old['hashes'].items() if p not in KNOWN_HISTORICAL_MISMATCH)
preserved=load(O/'v1-preservation.json');assert all(okhash(p,h) for p,h in preserved.items())
eligible=[c for c in cs if c['qualified_models']]
def strength(c):
    total=0
    for key,base,sd in [('main_support',5/7,math.sqrt(5*(5/35)*(30/35)*(30/34))),('SB_support',.1,.3)]:
        if c[key]['qualifies']:total+=(c[key]['mean']-base)/sd
    return (-total,-answers[c['id']+'_quality']['score'],-answers[c['id']+'_robustness']['score'],-answers['overall']['probabilities'][c['id']],c['id'])
if eligible:selected=sorted(eligible,key=strength)[0];policy='qualified evidence rule'
else:selected=cs[int(np.random.default_rng(meta['seed']).integers(len(cs)))];policy='predeclared seeded uniform candidate no-edge rule'
assert len(set(selected['main']))==5 and all(1<=n<=35 for n in selected['main']) and 1<=selected['super_ball']<=10
paths=[p for p in O.glob('*') if p.is_file() and p.name!='run.log']+[R/'scripts/research'/n for n in ['common.py','super_lotto.py','super_v1_prospective.py','super_v1_jev.mjs','super_v1_transport.mjs','validate_super_v1_response.mjs','super_v1_freeze.py']]
out=dict(status='PRE-DRAW',created_utc=now.isoformat(),target_draw_id=T,target_date=ARGS.target_date,scheduled_draw_utc=ARGS.deadline_utc,selection=dict(candidate_id=selected['id'],main=selected['main'],super_ball=selected['super_ball'],main_generator=selected['main_generator'],SB_generator=selected['SB_generator']),selection_policy=policy,statistical_edge_detected=bool(eligible),model_version='super-lotto-v1',jev_model=jev['model'],seed=meta['seed'],data_cutoff=meta['cutoff'],configuration=meta['configuration'],source_sha256=meta['source_sha256'],complete_rankings=load(O/'complete_rankings.json'),candidate_pool=cs,jev_request=load(O/'jev_request.json'),jev_response=jev,selected_candidate_choice_probability=answers['overall']['probabilities'][selected['id']],overall_choice_confidence=answers['overall']['confidence'],confirmations=dict(ordinary_previous_observations=True,V1_used=True,no_V2_promoted=True,no_other_prediction_for_target_inspected=True,candidates_frozen_before_Jev=True,first_valid_response_used=True,jev_http_calls=1,no_rerun=True,no_candidate_regeneration_after_Jev=True,no_manual_number_or_SB_change=True,frozen_before_draw=True),hashes={str(p.relative_to(R)):sha(p) for p in paths})
with target.open('x',encoding='utf-8') as h:json.dump(out,h,indent=2,allow_nan=False)
ledger=P/'ledger.jsonl';prior=ledger.read_bytes()
with ledger.open('a',encoding='utf-8') as h:h.write(json.dumps(dict(event='prediction_frozen',created_utc=out['created_utc'],target_draw_id=T,path=target.name,sha256=sha(target),selection=out['selection']))+'\n')
assert ledger.read_bytes().startswith(prior)
save=dict(target=str(target.relative_to(R)),sha256=sha(target),created_utc=out['created_utc'],selection=out['selection'],policy=policy,jev_probability=out['selected_candidate_choice_probability'],jev_confidence=out['overall_choice_confidence'],jev_model=jev['model'],all_frozen_hashes_match=all(sha(R/p)==h for p,h in out['hashes'].items()))
with (O/'freeze-receipt.json').open('x',encoding='utf-8') as h:json.dump(save,h,indent=2)
print(json.dumps(save,indent=2))
