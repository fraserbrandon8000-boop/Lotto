"""Generic prospective V1 wrapper, derived mechanically from lotto_2340.py (transport/invocation only).
Unchanged V1 functions from scripts/analyze.py. Target #2341, cutoff #2340."""
import sys,json,hashlib
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'))
import analyze as a
TARGET=2341;CUTOFF=2340;TARGET_DATE='2026-09-26';PREVIOUS={5,11,16,24,27,34}
O=R/f'results/lotto/draw{TARGET}';O.mkdir(exist_ok=True);a.OUT=O
if (O/'frozen.json').exists():
    print((O/'frozen.json').read_text());raise SystemExit
protocol=f'Unchanged V1 model functions, parameters, candidate generator and seed 20260919 (generic wrapper derived mechanically from lotto_2340.py). Append only #2340 (06 08 12 14 18 31, bonus 28; official result as supplied by user and recorded in the ledger). Refresh original rolling confirmation definition and sensitivity. Generate the original twenty candidates, then restrict final selection and Jev to candidates with <=2 shared numbers with previous V1 primary [5,11,16,24,27,34]. Do not minimize overlap further. Apply original empirical/Jev gate and composite score; if none qualify, seeded uniform selection among eligible diversified candidates sorted by ID, using original seed. Freeze first valid result for #{TARGET} on {TARGET_DATE}. No reselection. Jev judgments are not winning probabilities.'
if not (O/'PROTOCOL.txt').exists():(O/'PROTOCOL.txt').write_text(protocol,encoding='utf-8')
def verify_manifest():
    manifest=json.loads((R/'results/lotto/v1_manifest.json').read_text());out={}
    for p,v in manifest['files'].items():
        b=(R/p.replace('\\','/')).read_bytes()
        if hashlib.sha256(b).hexdigest()==v:out[p]='exact'
        elif hashlib.sha256(b.replace(b'\n',b'\r\n')).hexdigest()==v:out[p]='LF_to_CRLF'
        else:raise SystemExit(f'GENUINE V1 HASH MISMATCH: {p}')
    return out
integrity=verify_manifest()
records=json.loads((R/'results/lotto/draw2340/draws.json').read_text());assert records[-1]['draw_id']==2339
record=dict(draw_id=2340,date='2026-09-23',numbers=[6,8,12,14,18,31],bonus=28,origin='official_user_supplied',source='Official result supplied by user; recorded in results/lotto/prospective_ledger.jsonl (outcome_appended 2026-09-26T01:15:56Z)')
records.append(record);a.save('draws.json',records)
d=np.array([r['numbers'] for r in records])-1
nums,pairs,_=a.exploratory(d,records)
rows=a.walk(d,records,details=True);a.save('walk_forward_predictions.json',rows)
for r in rows:
    assert r['training_last_draw_id']<r['draw_id']
    for t,h in zip(r['tickets'],r['matches']):assert len(set(t))==6 and min(t)>=1 and max(t)<=38 and len(set(t)&set(records[r['index']]['numbers']))==h
summary=a.summaries(rows);a.save('model_performance.json',summary)
_,variants=a.sensitivity(d,records,rows);cs=a.candidates(d,records,summary,rows,variants,nums,pairs)
previous=PREVIOUS
for c in cs:c['overlap_previous_primary']=sorted(set(c['numbers'])&previous)
a.save('candidates.json',cs);eligible=[c for c in cs if len(c['overlap_previous_primary'])<=2];assert eligible
ft=a.model_features(a.indicator(d));weights=a.ensemble_weights([r['matches'] for r in rows]);scores={n:ft[0][i] for i,n in enumerate(a.NAMES[:5])};scores['G_marginal_proxy']=weights[:5]@ft[0]
a.save('refreshed_rankings.json',{n:dict(scores=s,order=(np.argsort(-(s+np.random.default_rng(a.SEED+TARGET).random(38)*1e-10))+1),informative=bool(np.std(s)>1e-12)) for n,s in scores.items()})
meta=dict(cutoff_draw=CUTOFF,target_draw=TARGET,target_date=TARGET_DATE,seed=a.SEED,qualifying_models=[r['model'] for r in summary if r['qualifies']],origins=len(rows),data_sha256=hashlib.sha256((O/'draws.json').read_bytes()).hexdigest(),v1_code_sha256=hashlib.sha256((R/'scripts/analyze.py').read_bytes()).hexdigest(),v1_manifest_integrity=integrity,limitations=['No candidate-specific or Jev policy predictive validation.','Reused retrospective confirmation; no new holdout.'])
a.save('metadata.json',meta)
a.save('jev_state.json',dict(task=f'Evaluate the refreshed empirical evidence for one additional Lotto #{TARGET} complete ticket.',metadata=meta,baseline=dict(expected_matches=a.BASE,jackpot_probability=1/2760681),methodology_confirmation=[r for r in summary if r['period']=='confirmation'],candidates=eligible,diversification=dict(previous_primary=sorted(previous),maximum_shared=2,do_not_prefer_zero_overlap=True),interpretation='No winning advantage without corrected evidence. Model agreement is correlated. Use only supplied Lotto evidence; never infer a signal from a single previous ticket result. Jev is advisory under the no-edge rule.'))
verify_manifest()
pool={p:hashlib.sha256((O/p).read_bytes()).hexdigest() for p in ['PROTOCOL.txt','draws.json','candidates.json','model_performance.json','candidate_sensitivity.json','refreshed_rankings.json','metadata.json','jev_state.json']}
from datetime import datetime,timezone
with (O/'pool_frozen_pre_jev.json').open('x') as h:json.dump(dict(frozen_utc=datetime.now(timezone.utc).isoformat(),note='Candidate pool frozen before any Jev call',hashes=pool,eligible_ids=[c['id'] for c in eligible]),h,indent=2)
print(json.dumps(dict(qualifiers=meta['qualifying_models'],candidate_count=len(cs),diversified_candidates=len(eligible),normalized_files=sum(v!='exact' for v in integrity.values()),v1_unchanged=True)))
