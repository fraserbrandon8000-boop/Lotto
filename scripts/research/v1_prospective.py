"""Parameterized prospective V1 wrapper: lotto_prospective.py with its draw constants turned into arguments
(transport/invocation only; identical V1 calls). Usage: see argparse below."""
import sys,json,hashlib,argparse
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'))
import analyze as a
ap=argparse.ArgumentParser();ap.add_argument('--target',type=int,required=True);ap.add_argument('--date',required=True);ap.add_argument('--base',required=True)
ap.add_argument('--append-json',required=True);ap.add_argument('--previous',required=True);ap.add_argument('--out',required=True);ap.add_argument('--protocol-append-text',required=True)
ARGS=ap.parse_args();TARGET=ARGS.target;CUTOFF=TARGET-1;TARGET_DATE=ARGS.date;PREVIOUS=set(int(x) for x in ARGS.previous.split(','))
O=Path(ARGS.out);O.mkdir(parents=True,exist_ok=True);a.OUT=O
if (O/'frozen.json').exists():
    print((O/'frozen.json').read_text());raise SystemExit
protocol=f'Unchanged V1 model functions, parameters, candidate generator and seed 20260919 (generic wrapper derived mechanically from lotto_2340.py). {ARGS.protocol_append_text} Refresh original rolling confirmation definition and sensitivity. Generate the original twenty candidates, then restrict final selection and Jev to candidates with <=2 shared numbers with previous V1 primary [{",".join(map(str,sorted(PREVIOUS)))}]. Do not minimize overlap further. Apply original empirical/Jev gate and composite score; if none qualify, seeded uniform selection among eligible diversified candidates sorted by ID, using original seed. Freeze first valid result for #{TARGET} on {TARGET_DATE}. No reselection. Jev judgments are not winning probabilities.'
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
records=json.loads((R/ARGS.base).read_text());assert records[-1]['draw_id']==CUTOFF-1
record=json.loads(ARGS.append_json);assert record['draw_id']==CUTOFF
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
