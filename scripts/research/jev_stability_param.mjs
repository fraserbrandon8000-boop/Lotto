// Parameterized copy of jev_stability.mjs (unchanged for #2342). RESEARCH ONLY: repeat the EXACT frozen V1 production Jev request N times after all tickets are frozen.
// Proves byte-identity of the request via the production receipt; cannot change any ticket.
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {TypeSafeClient} from '@typesafe-ai/sdk';
const [SRC,OUT,N,TG]=[process.argv[2],process.argv[3],Number(process.argv[4]||5),process.argv[5]];if(!TG)throw new Error('usage: SRC OUT N TARGET');
const req=JSON.parse(await readFile(`${SRC}/jev_request.json`,'utf8'));const rc=JSON.parse(await readFile(`${SRC}/jev_receipt.json`,'utf8'));
const h=createHash('sha256').update(JSON.stringify(req)).digest('hex');assert.equal(h,rc.request_sha256,'request differs from production bytes');
assert.ok(process.env.TYPESAFE_API_KEY?.trim());const client=new TypeSafeClient({baseURL:'https://api.typesafe.ai',logLevel:'off',timeout:60000});
const runs=[];
for(let i=1;i<=N;i++){
  const r=await client.systemOne(req);assert.equal(JSON.stringify(Object.keys(r.answers)),JSON.stringify(Object.keys(req.questions)));
  await writeFile(`${OUT}/replicate_${i}_response.json`,JSON.stringify(r,null,2));
  runs.push({replicate:i,created_utc:new Date().toISOString(),model:r.model,choice:r.answers.overall.choice,confidence:r.answers.overall.confidence,usage:r.usage});
  console.log(JSON.stringify(runs.at(-1)));
}
await writeFile(`${OUT}/replicates_receipt.json`,JSON.stringify({request_sha256:h,production_request_sha256:rc.request_sha256,identical_request_bytes:true,runs,
  note:`Research-only replicates after all #${TG} tickets were frozen. No ticket is changed by these calls.`},null,2));
