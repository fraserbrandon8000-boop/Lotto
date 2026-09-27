// Offline validation of the FIRST saved response. No SDK import or network call.
import {readFile,writeFile,stat} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const root=new URL('../../results/super_lotto/draw1754/',import.meta.url);
const raw=await readFile(new URL('jev_response.json',root),'utf8');
const response=JSON.parse(raw),request=JSON.parse(await readFile(new URL('jev_request.json',root),'utf8'));
const stateText=await readFile(new URL('jev_state.json',root),'utf8');
const candidates=JSON.parse(stateText).candidates;const boundary=[];
assert.equal(Object.keys(response.answers).length,Object.keys(request.questions).length);
for(const [id,q] of Object.entries(request.questions)){
  const a=response.answers[id];assert.ok(a,`Missing ${id}`);assert.equal(a.type,q.type);
  if(q.type==='noul'){assert.ok(Number.isFinite(a.noul)&&a.noul>=0&&a.noul<=1);continue;}
  assert.ok(Number.isFinite(a.confidence)&&a.confidence>=0&&a.confidence<=1);
  const ps=Object.values(a.probabilities);assert.ok(ps.every(p=>Number.isFinite(p)&&p>=0&&p<=1));assert.ok(Math.abs(ps.reduce((a,b)=>a+b,0)-1)<.015);
  if(q.type==='choice'){
    assert.ok(candidates.some(c=>c.id===a.choice));assert.deepEqual(Object.keys(a.probabilities).sort(),candidates.map(c=>c.id).sort());
  }else{
    assert.ok(a.score>=0&&a.score<=4);
    const delta=Math.abs(a.score-Object.entries(a.probabilities).reduce((s,[k,p])=>s+Number(k)*p,0));
    assert.ok(delta<=.03+1e-12,`${id}: rounded Score discrepancy ${delta}`);
    if(delta>=.03)boundary.push({question:id,score:a.score,delta});
  }
}
const originalStat=await stat(new URL('jev_response.json',root));
const receipt={created_utc:originalStat.mtime.toISOString(),validated_utc:new Date().toISOString(),model:response.model,questions:Object.keys(request.questions).length,state_file_sha256:createHash('sha256').update(stateText).digest('hex'),request_sha256:createHash('sha256').update(JSON.stringify(request)).digest('hex'),response_sha256:createHash('sha256').update(raw).digest('hex'),usage:response.usage,http_attempts:1,offline_validation_repair:'Inclusive 0.03 rounded-score boundary plus 1e-12 floating-point epsilon; no response modification or network retry.',boundary};
await writeFile(new URL('jev_receipt.json',root),JSON.stringify(receipt,null,2),{flag:'wx'});
console.log(JSON.stringify({valid:true,model:receipt.model,answers:receipt.questions,offline_boundary_fix:boundary}));
