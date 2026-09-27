import {readFile,writeFile,appendFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {TypeSafeClient,choice} from '@typesafe-ai/sdk';

// Isolated experiment: only game rules, available options and this run's own
// saved selections are inputs. No analysis, dataset or prior experiment imports.
const base=new URL('./',import.meta.url);
const frozenUrl=new URL('frozen-result.json',base);
const journalUrl=new URL('decisions.jsonl',base);
async function optional(url){try{return await readFile(url,'utf8');}catch(e){if(e.code==='ENOENT')return null;throw e;}}
const frozen=await optional(frozenUrl);
if(frozen){console.log(frozen);process.exit(0);}
const saved=await optional(journalUrl);
const decisions=saved?saved.trim().split('\n').filter(Boolean).map(s=>JSON.parse(s)):[];
const selected=[];
function validate(entry){
  const a=entry.response.answers.number;
  const available=Array.from({length:38},(_,i)=>i+1).filter(n=>!selected.includes(n));
  assert.equal(a.type,'choice');
  assert.deepEqual(Object.keys(a.probabilities).map(Number).sort((a,b)=>a-b),available);
  assert.ok(Number.isInteger(Number(a.choice))&&available.includes(Number(a.choice)));
  assert.ok(Number.isFinite(a.confidence)&&a.confidence>=0&&a.confidence<=1);
  const ps=Object.values(a.probabilities);
  assert.ok(ps.every(p=>Number.isFinite(p)&&p>=0&&p<=1));
  // API probabilities may be rounded. Keep them exactly as returned.
  assert.ok(Math.abs(ps.reduce((s,p)=>s+p,0)-1)<.10);
  selected.push(Number(a.choice));
}
try{
  for(const d of decisions)validate(d);
  assert.ok(decisions.length<=6);
  const client=new TypeSafeClient({baseURL:'https://api.typesafe.ai',logLevel:'off',timeout:30000});
  while(selected.length<6){
    const remaining=Array.from({length:38},(_,i)=>i+1).filter(n=>!selected.includes(n));
    const request={model:'jev-latest',state:{game:'Jamaica Lotto',rules:'One ticket contains six distinct integers from 1 through 38.',evidence:'No historical data or selection preference criteria are supplied.'},questions:{number:choice('Choose one number from the available options for this ticket.',Object.fromEntries(remaining.map(n=>[String(n),null])))}};
    const response=await client.systemOne(request);
    const entry={step:selected.length+1,received_utc:new Date().toISOString(),request,response};
    // Persist the first returned response before interpretation; never optimize
    // or reselect because an outcome or its confidence seems unusual.
    await appendFile(journalUrl,JSON.stringify(entry)+'\n');
    validate(entry);decisions.push(entry);
    console.log(JSON.stringify({step:entry.step,selected:response.answers.number.choice,probability:response.answers.number.probabilities[response.answers.number.choice],confidence:response.answers.number.confidence}));
  }
  assert.equal(new Set(selected).size,6);
  const result={label:'JEV-ONLY / ZERO-DATA PICK',frozen:true,completed_utc:new Date().toISOString(),combination:[...selected].sort((a,b)=>a-b),model_requested:'jev-latest',decisions:decisions.map(d=>({step:d.step,model:d.response.model,selected:Number(d.response.answers.number.choice),selected_probability:d.response.answers.number.probabilities[d.response.answers.number.choice],confidence:d.response.answers.number.confidence,probabilities:d.response.answers.number.probabilities,usage:d.response.usage})),method:'Six sequential Jev Choice decisions. Remove each selected number from subsequent options. Numeric options are presented in ascending order, all with null descriptions. No random sampling, historical inputs, selection heuristics or reranking. First completed valid result frozen.'};
  await writeFile(frozenUrl,JSON.stringify(result,null,2),{flag:'wx'});
  console.log(JSON.stringify({label:result.label,combination:result.combination,frozen:true}));
}catch(e){console.error(JSON.stringify({errorType:e.name,status:e.status??null,code:e.cause?.code??null}));process.exitCode=1;}
