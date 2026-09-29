"""#2341 forensic step 2: verify the frozen #2341 V1 record. Read-only; writes forensic_2341/verification.json."""
import json,hashlib,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[2];D=R/'results/lotto/draw2341';O=R/'results/lotto/forensic_2341'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *a:subprocess.run(['git',*a],cwd=R,capture_output=True,text=True,check=True).stdout.strip()
out={}
fz=json.loads((D/'frozen.json').read_text())
out['frozen_embedded_hashes']={p:('exact' if sha(R/p)==h else 'DIFFERS') for p,h in fz['hashes'].items()}
pool=json.loads((D/'pool_frozen_pre_jev.json').read_text())
out['pool_freeze_hashes']={p:('exact' if sha(D/p)==h else 'DIFFERS') for p,h in pool['hashes'].items()}
led=[json.loads(l) for l in (R/'results/lotto/prospective_ledger.jsonl').read_text().splitlines() if l.strip()]
e=[x for x in led if x.get('target_draw')==2341]
out['ledger_entries_2341']=e
out['ledger_sha_matches_frozen_json']=bool(e) and e[-1]['sha256']==sha(D/'frozen.json')
out['ledger_numbers_match']=bool(e) and e[-1]['numbers']==fz['numbers']
rc=json.loads((D/'jev_receipt.json').read_text())
out['receipt_state_sha_matches']=rc['state_file_sha256']==sha(D/'jev_state.json')
node=subprocess.run(['node','-e',"const fs=require('fs'),c=require('crypto');const r=JSON.parse(fs.readFileSync(process.argv[1],'utf8'));console.log(c.createHash('sha256').update(JSON.stringify(r)).digest('hex'))",str(D/'jev_request.json')],capture_output=True,text=True,check=True).stdout.strip()
out['receipt_request_sha_matches_saved_request']=rc['request_sha256']==node
req=json.loads((D/'jev_request.json').read_text());resp=json.loads((D/'jev_response.json').read_text())
out['request_model']=req['model'];out['response_model']=resp['model'];out['n_questions']=len(req['questions']);out['n_answers']=len(resp['answers'])
st=json.loads((D/'jev_state.json').read_text())
out['request_state_equals_jev_state_candidates']=[c['id'] for c in req['state']['candidates']]==[c['id'] for c in st['candidates']]
ov=resp['answers']['overall']
out['frozen_fields_match_response']=dict(choice_prob=fz['jev_choice_probability']==ov['probabilities'][fz['candidate_id']],confidence=fz['jev_choice_confidence']==ov['confidence'],preferred=fz['jev_preferred_candidate']==ov['choice'],model=fz['jev_model']==resp['model'])
cands=json.loads((D/'candidates.json').read_text());sel=[c for c in cands if c['id']==fz['candidate_id']][0]
out['frozen_ticket_matches_pool']=sel['numbers']==fz['numbers'] and sel['generator']==fz['generator']
# commit chronology
def first_commit(path):return git('log','--diff-filter=A','--format=%h %cI','--',path).splitlines()[-1]
out['commit_chronology']={p:first_commit(p) for p in ['results/lotto/draw2341/candidates.json','results/lotto/draw2341/pool_frozen_pre_jev.json','results/lotto/draw2341/jev_request.json','results/lotto/draw2341/jev_response.json','results/lotto/draw2341/frozen.json']}
out['pool_files_unchanged_after_pool_commit']=git('diff','--name-only','c5abf27','28c78bd','--','results/lotto/draw2341/candidates.json','results/lotto/draw2341/jev_state.json','results/lotto/draw2341/pool_frozen_pre_jev.json')==''
out['v1_code_unchanged_since_snapshot']=git('diff','--name-only','ba7c5a3','HEAD','--','scripts/analyze.py','scripts/jev.mjs','scripts/finalize.py','scripts/audit.py','PROTOCOL.md','data')==''
out['timestamps_utc']=dict(pool_frozen=pool['frozen_utc'],jev_receipt=rc['created_utc'],ticket_frozen=fz['created_utc'],scheduled_draw='2026-09-27T01:25:00Z (8:25 PM Jamaica, per user)',freeze_script_deadline_assert='now < 2026-09-27T01:25:00Z',push_of_28c78bd_observed='2026-09-27T01:15:55Z (session transcript)')
out['frozen_before_draw']=fz['created_utc']<'2026-09-27T01:25:00'
flat=[v for k,v in out.items() if isinstance(v,bool)]+[v=='exact' for d in ('frozen_embedded_hashes','pool_freeze_hashes') for v in out[d].values()]+list(out['frozen_fields_match_response'].values())
out['ALL_CHECKS_PASS']=all(flat)
json.dump(out,open(O/'verification.json','w'),indent=1);print(json.dumps({k:v for k,v in out.items() if k!='ledger_entries_2341'},indent=1))
