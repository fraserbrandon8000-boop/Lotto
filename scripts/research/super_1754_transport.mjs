import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const root=new URL('../../results/super_lotto/draw1754/',import.meta.url);
const freeze=JSON.parse(await readFile(new URL('candidate-freeze.json',root),'utf8'));
for(const [name,hash] of Object.entries(freeze.hashes)){
  assert.equal(createHash('sha256').update(await readFile(new URL(name,root))).digest('hex'),hash);
}
let attempts=0;
export async function verifiedFetch(input,init){
  assert.equal(attempts,0,'Only one Jev HTTP attempt is authorized');
  assert.ok(Date.now()<Date.parse('2026-09-26T01:30:00Z'),'Draw deadline passed');
  await writeFile(new URL('jev-attempt.json',root),JSON.stringify({started_utc:new Date().toISOString(),http_attempts:1,retries_disabled:true,candidate_freeze_utc:freeze.frozen_utc},null,2),{flag:'wx'});
  attempts++;
  return fetch(input,init);
}
