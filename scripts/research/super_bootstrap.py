"""Super Lotto bootstrap: verify frozen V1 hashes (exact, then LF->CRLF). Reads only results/super_lotto and Super Lotto scripts."""
import json,hashlib,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[2];V=R/'results/super_lotto';O=V/'bootstrap'
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def check(hashes,base=R):
    out={}
    for p,h in hashes.items():
        f=base/p.replace('\\','/')
        if not f.exists():out[p]='MISSING';continue
        b=f.read_bytes()
        if hashlib.sha256(b).hexdigest()==h:out[p]='exact'
        elif b'\r\n' not in b and hashlib.sha256(b.replace(b'\n',b'\r\n')).hexdigest()==h:out[p]='LF_to_CRLF'
        else:out[p]='DIFFERS'
    return out
res={}
p4=load(V/'prospective/prediction_1754.json');p3=load(V/'prospective/prediction_1753.json')
res['prediction_1754_embedded']=check(p4['hashes']);res['prediction_1753_embedded']=check(p3['hashes'])
led=[json.loads(l) for l in (V/'prospective/ledger.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]
res['ledger_prediction_hashes']={e['path']:check({'results/super_lotto/prospective/'+e['path']:e['sha256']})['results/super_lotto/prospective/'+e['path']] for e in led if e['event']=='prediction_frozen'}
res['candidate_freeze_1754']=check(load(V/'draw1754/candidate-freeze.json')['hashes'],V/'draw1754')
res['v1_preservation_1754']=check(load(V/'draw1754/v1-preservation.json'))
rc=load(V/'draw1754/jev_receipt.json')
res['jev_receipt_1754']=dict(state=check({'results/super_lotto/draw1754/jev_state.json':rc['state_file_sha256']}),response=check({'results/super_lotto/draw1754/jev_response.json':rc['response_sha256']}))
node=subprocess.run(['node','-e',"const fs=require('fs'),c=require('crypto');const b=fs.readFileSync(process.argv[1],'utf8').replace(/^\\uFEFF/,'');console.log(c.createHash('sha256').update(JSON.stringify(JSON.parse(b))).digest('hex'))",str(V/'draw1754/jev_request.json')],capture_output=True,text=True).stdout.strip()
fb=(V/'draw1754/jev_request.json').read_bytes()
res['jev_receipt_1754']['request']=dict(file_exact=hashlib.sha256(fb).hexdigest()==rc['request_sha256'],file_crlf=hashlib.sha256(fb.replace(b'\n',b'\r\n')).hexdigest()==rc['request_sha256'],compact_json=node==rc['request_sha256'])
from collections import Counter
res['summary']={k:dict(Counter(v.values())) for k,v in res.items() if isinstance(v,dict) and all(isinstance(x,str) for x in v.values())}
res['differs']={k:[p for p,s in v.items() if s in ('DIFFERS','MISSING')] for k,v in res.items() if isinstance(v,dict) and all(isinstance(x,str) for x in v.values())}
json.dump(res,open(O/'hash_verification.json','w'),indent=1);print(json.dumps({'summary':res['summary'],'differs':res['differs'],'jev':res['jev_receipt_1754']},indent=1))
