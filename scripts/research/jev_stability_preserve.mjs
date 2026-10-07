// RESEARCH ONLY (post-freeze). Copy of jev_stability_param.mjs that saves each response BEFORE checking, and compares
// answer-key SETS (the API may return keys in a different order). Usage: SRC OUT START END TARGET NOTE
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {TypeSafeClient} from '@typesafe-ai/sdk';
const [SRC,OUT,S,E,TG,NOTE]=process.argv.slice(2);
const req=JSON.parse(await readFile(`${SRC}/jev_request.json`,'utf8'));const rc=JSON.parse(await readFile(`${SRC}/jev_receipt.json`,'utf8'));
const h=createHash('sha256').update(JSON.stringify(req)).digest('hex');assert.equal(h,rc.request_sha256,'request differs from production bytes');
const client=new TypeSafeClient({baseURL:'https://api.typesafe.ai',logLevel:'off',timeout:60000});const runs=[];
for(let i=Number(S);i<=Number(E);i++){
  const r=await client.systemOne(req);await writeFile(`${OUT}/replicate_${i}_response.json`,JSON.stringify(r,null,2),{flag:'wx'});
  const same=JSON.stringify(Object.keys(r.answers).sort())===JSON.stringify(Object.keys(req.questions).sort());
  runs.push({replicate:i,created_utc:new Date().toISOString(),model:r.model,choice:r.answers.overall.choice,confidence:r.answers.overall.confidence,answer_key_set_matches:same,usage:r.usage});console.log(JSON.stringify(runs.at(-1)));
}
await writeFile(`${OUT}/replicates_receipt_${S}_${E}.json`,JSON.stringify({request_sha256:h,production_request_sha256:rc.request_sha256,identical_request_bytes:true,runs,note:NOTE},null,2),{flag:'wx'});
