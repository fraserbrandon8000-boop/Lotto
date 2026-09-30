import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {pathToFileURL} from 'node:url';
import {resolve as resolvePath} from 'node:path';
const root=pathToFileURL(resolvePath(process.env.SL_DIR)+'/');const DEADLINE=process.env.SL_DEADLINE;assert.ok(process.env.SL_DIR&&DEADLINE,'SL_DIR and SL_DEADLINE required');
const freeze=JSON.parse(await readFile(new URL('candidate-freeze.json',root),'utf8'));
for(const [name,hash] of Object.entries(freeze.hashes)){
  const b=await readFile(new URL(name,root));const hx=createHash('sha256').update(b).digest('hex');const hc=createHash('sha256').update(Buffer.from(b.toString('latin1').replace(/\r?\n/g,'\r\n'),'latin1')).digest('hex');
  assert.ok(hx===hash||hc===hash,`frozen file changed: ${name}`);
}
let attempts=0;
export async function verifiedFetch(input,init){
  assert.equal(attempts,0,'Only one Jev HTTP attempt is authorized');
  assert.ok(Date.now()<Date.parse(DEADLINE),'Draw deadline passed');
  await writeFile(new URL('jev-attempt.json',root),JSON.stringify({started_utc:new Date().toISOString(),http_attempts:1,retries_disabled:true,candidate_freeze_utc:freeze.frozen_utc},null,2),{flag:'wx'});
  attempts++;
  return fetch(input,init);
}
