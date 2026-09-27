import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {TypeSafeClient,choice} from '@typesafe-ai/sdk';

// No historical data, statistics, previous experiments or their responses are read.
const base=new URL('./',import.meta.url);
const SEED='jev-complete-ticket-zero-data-v1-684219';
const CENTRAL='With no historical Lotto data available and considering only these valid candidate combinations as alternative actions, which single ticket do you choose for the next Jamaica Lotto draw?';
const STATE={game:'Jamaica Lotto',rules:'Each ticket contains exactly six distinct integers from 1 through 38.',historical_data:'None supplied.',selection_criteria:'No additional preference criteria are supplied.'};
async function read(name){try{return JSON.parse(await readFile(new URL(name,base),'utf8'));}catch(e){if(e.code==='ENOENT')return null;throw e;}}
async function save(name,obj){await writeFile(new URL(name,base),JSON.stringify(obj,null,2),{flag:'wx'});}
// SHA-256 counter stream with domain-separated seeds and rejection sampling:
// no modulo bias in integer draws. Fisher-Yates makes each six-element subset
// equiprobable; duplicate-ticket rejection samples distinct tickets uniformly.
function stream(domain){let count=0;return()=>createHash('sha256').update(`${SEED}|${domain}|${count++}`).digest().readUInt32BE(0);}
function integer(next,n){const ceiling=Math.floor(4294967296/n)*n;let x;do{x=next();}while(x>=ceiling);return x%n;}
function shuffle(input,next){const a=[...input];for(let i=a.length-1;i>0;i--){const j=integer(next,i+1);[a[i],a[j]]=[a[j],a[i]];}return a;}
function validTicket(t){assert.equal(t.length,6);assert.equal(new Set(t).size,6);assert.ok(t.every(n=>Number.isInteger(n)&&n>=1&&n<=38));}
function anonymous(tickets,domain){
  const ordered=shuffle(tickets,stream(`${domain}-order`));const next=stream(`${domain}-labels`);const labels=new Set();
  return ordered.map(ticket=>{let id;do{id=`T_${next().toString(16).padStart(8,'0')}`;}while(labels.has(id));labels.add(id);return{id,ticket};});
}
function question(options){return choice(CENTRAL,Object.fromEntries(options.map(o=>[o.id,`Ticket: ${o.ticket.join(', ')}`])));}
function validateAnswer(answer,options){
  assert.equal(answer.type,'choice');
  const selected=options.find(o=>o.id===answer.choice);assert.ok(selected);validTicket(selected.ticket);
  assert.deepEqual(Object.keys(answer.probabilities).sort(),options.map(o=>o.id).sort());
  assert.ok(Object.values(answer.probabilities).every(p=>Number.isFinite(p)&&p>=0&&p<=1));
  assert.ok(Number.isFinite(answer.confidence)&&answer.confidence>=0&&answer.confidence<=1);
  // Keep API rounding as returned; do not normalize or modify the response.
  return selected.ticket;
}
try{
  const existing=await read('frozen-result.json');if(existing){console.log(JSON.stringify(existing));process.exit(0);}
  let pool=await read('pool.json');
  if(!pool){
    const next=stream('uniform-ticket-generation');const unique=new Map();
    while(unique.size<512){const t=shuffle(Array.from({length:38},(_,i)=>i+1),next).slice(0,6).sort((a,b)=>a-b);unique.set(t.join(','),t);}
    const tickets=shuffle([...unique.values()],stream('group-assignment'));
    pool={seed:SEED,generator:'SHA256-counter-domain-stream; unbiased bounded integer rejection; Fisher-Yates; reject duplicate tickets',count:512,groups:Array.from({length:4},(_,i)=>anonymous(tickets.slice(i*128,(i+1)*128),`group-${i}`))};
    await save('pool.json',pool);
  }
  const all=pool.groups.flat().map(o=>o.ticket);all.forEach(validTicket);assert.equal(new Set(all.map(t=>t.join(','))).size,512);
  const client=new TypeSafeClient({baseURL:'https://api.typesafe.ai',logLevel:'off',timeout:60000});
  let stage1=await read('stage1-response.json');
  if(!stage1){
    let req=await read('stage1-request.json');
    if(!req){req={model:'jev-latest',state:STATE,questions:Object.fromEntries(pool.groups.map((g,i)=>[`group_${i}`,question(g)]))};await save('stage1-request.json',req);}
    stage1=await client.systemOne(req);await save('stage1-response.json',stage1);
  }
  const winners=pool.groups.map((g,i)=>validateAnswer(stage1.answers[`group_${i}`],g));
  let finalists=await read('finalists.json');if(!finalists){finalists=anonymous(winners,'final');await save('finalists.json',finalists);}
  let response=await read('final-response.json');
  if(!response){
    let req=await read('final-request.json');if(!req){req={model:'jev-latest',state:STATE,questions:{ticket:question(finalists)}};await save('final-request.json',req);}
    response=await client.systemOne(req);await save('final-response.json',response);
  }
  const ticket=validateAnswer(response.answers.ticket,finalists);
  const result={label:'JEV-ONLY / ZERO-DATA PICK',combination:[...ticket].sort((a,b)=>a-b),final_choice_probability:response.answers.ticket.probabilities[response.answers.ticket.choice],final_confidence:response.answers.ticket.confidence,final_probabilities:response.answers.ticket.probabilities,selected_option:response.answers.ticket.choice,candidate_count:512,tournament:{required:true,reason:'Choice maximum 255 options',rounds:[{groups:4,tickets_per_group:128},{groups:1,tickets_per_group:4}]},seed:SEED,model:response.model,usage:{stage1:stage1.usage,final:response.usage},frozen:true,completed_utc:new Date().toISOString()};
  await save('frozen-result.json',result);
  console.log(JSON.stringify(result,null,2));
}catch(e){console.error(JSON.stringify({errorType:e.name,status:e.status??null,code:e.cause?.code??null}));process.exitCode=1;}
