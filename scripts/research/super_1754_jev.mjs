import {verifiedFetch} from './super_1754_transport.mjs';
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {TypeSafeClient,choice,score,noul} from '@typesafe-ai/sdk';

const stateText=await readFile(new URL('../../results/super_lotto/draw1754/jev_state.json',import.meta.url),'utf8');
const state=JSON.parse(stateText);
// Round computed evidence only for compact transport; full precision remains in Python outputs.
const compact=JSON.parse(JSON.stringify(state,(_,v)=>typeof v==='number'?Number(v.toFixed(6)):v));
const candidates=compact.candidates;
const questions={overall:choice('Given the supplied pre-draw empirical evidence, which complete Super Lotto ticket has the strongest overall empirical case among these candidates? These are complete five-main-plus-Super-Ball tickets. Choice probabilities are preferences, not winning probabilities. Do not invent an edge.',Object.fromEntries(candidates.map(c=>[c.id,`Candidate ${c.id}, evidence at candidates entry with id ${c.id}.`])))};
const robustness=[
  'No empirical support beyond the random baseline; no methodology qualifies after corrected confirmation testing.',
  'Weak or fragile apparent support, from an unstable configuration or an uncorrected historical result.',
  'Some repeatable out-of-sample support but substantial uncertainty; convincing corrected confirmation is missing.',
  'Meaningful support across multiple out-of-sample tests including a corrected confirmation result and sensitivity stability.',
  'Unusually robust support across independent models and time windows, corrected random-control comparisons and independent prospective replication.'
];
const consensus=[
  'No independently validated methodology supports the candidate; agreement of unvalidated correlated heuristics does not count.',
  'One validated methodology supports the candidate; other approaches lack independent validation.',
  'Two meaningfully distinct validated approaches support the candidate, with shared-data uncertainty.',
  'Several distinct validated approaches support the candidate consistently across periods.',
  'Strong support from independently validated approaches and independent data replications.'
];
const quality=[
  'Evidence for an advantage is absent: results are compatible with random controls or no corrected validation supports the claim.',
  'Evidence for an advantage is weak: small samples, uncorrected comparisons, one window, instability or overfitting dominate.',
  'Evidence for an advantage has some credible validation but material sample-size or stability limitations remain.',
  'Evidence for an advantage is supported by corrected separated tests and robust sensitivity, with manageable limitations.',
  'Evidence for an advantage is supported by strong independent replications, adequate sample sizes, correction and stable sensitivity.'
];
for(const c of candidates){
  const ref=`For candidate ${c.id} in candidates, use only supplied computed evidence. Do not calculate new statistics or infer winning numbers. `;
  questions[`${c.id}_robustness`]=score(ref+'How robust is its empirical advantage over uniform selection?',robustness);
  questions[`${c.id}_consensus`]=score(ref+'How independently validated is its support across approaches?',consensus);
  questions[`${c.id}_quality`]=score(ref+'What is the quality of evidence FOR a predictive advantage? A rigorous experiment with a negative result is not positive support.',quality);
  questions[`${c.id}_stability`]=score(ref+'How stable is the candidate objective rank under the supplied modelling changes?',['No informative rank stability, or flat/random objective.','Usually weak rank with large changes.','Mixed top-five membership and material rank changes.','Usually top five with limited rank changes.','Consistently top five across all informative changes.']);
  questions[`${c.id}_overfit`]=noul(ref+'Is chance selection or overfitting a better-supported explanation of any apparent advantage than a reproducible predictive signal?',{true:'Random controls and corrected confirmation fail to support an edge; candidate optimization or retrospective selection can create apparent advantages.',false:'Corrected independent confirmation and stable sensitivity support an advantage beyond chance selection.'});
  questions[`${c.id}_stable`]=noul(ref+'Does this candidate remain competitive in objective rank under reasonable modelling perturbations?',{true:'Generator ranks stay near the top across informative perturbations; top-quartile fraction is high.',false:'Ranks change substantially or informative perturbation support is absent; a uniform fallback is not evidence of robustness.'});
  questions[`${c.id}_stronger`]=noul(ref+'Is the evidence for an advantage materially stronger than would commonly arise under random variation?',{true:'At least one qualifying corrected confirmation methodology supports this candidate, with consistent windows.',false:'No qualifying corrected confirmation methodology supports this candidate, or random variation remains sufficient.'});
  questions[`${c.id}_dependent`]=noul(ref+'Is the apparent support overly dependent on one model family?',{true:'Only one family supplies positive evidence or rank support; correlated frequency variants count as one family.',false:'Several distinct validated model families supply support, or this is explicitly a uniform random fallback without a claimed advantage.'});
}
const request={model:'jev-latest',state:compact,questions};
await writeFile(new URL('../../results/super_lotto/draw1754/jev_request.json',import.meta.url),JSON.stringify(request,null,2));
assert.ok(process.env.TYPESAFE_API_KEY?.trim(),'TYPESAFE_API_KEY unavailable');
try{
  const client=new TypeSafeClient({baseURL:'https://api.typesafe.ai',logLevel:'off',timeout:60000,retry:{maxRetries:0},fetch:verifiedFetch});
  const response=await client.systemOne(request);
  await writeFile(new URL('../../results/super_lotto/draw1754/jev_response.json',import.meta.url),JSON.stringify(response,null,2),{flag:'wx'});
  for(const [id,q] of Object.entries(questions)){
    const a=response.answers[id]; assert.ok(a,`Missing answer ${id}`); assert.equal(a.type,q.type);
    if(q.type==='noul'){assert.ok(Number.isFinite(a.noul)&&a.noul>=0&&a.noul<=1);continue;}
    assert.ok(Number.isFinite(a.confidence)&&a.confidence>=0&&a.confidence<=1);
    const p=Object.values(a.probabilities); assert.ok(p.every(v=>Number.isFinite(v)&&v>=0&&v<=1));assert.ok(Math.abs(p.reduce((a,b)=>a+b,0)-1)<.015);
    if(q.type==='choice'){assert.ok(candidates.some(c=>c.id===a.choice));assert.deepEqual(Object.keys(a.probabilities).sort(),candidates.map(c=>c.id).sort());}
    else{assert.ok(a.score>=0&&a.score<=4);assert.ok(Math.abs(a.score-Object.entries(a.probabilities).reduce((s,[k,p])=>s+Number(k)*p,0))<.03);}
  }

  await writeFile(new URL('../../results/super_lotto/draw1754/jev_receipt.json',import.meta.url),JSON.stringify({created_utc:new Date().toISOString(),model:response.model,questions:Object.keys(questions).length,state_file_sha256:createHash('sha256').update(stateText).digest('hex'),request_sha256:createHash('sha256').update(JSON.stringify(request)).digest('hex'),usage:response.usage},null,2));
  console.log(JSON.stringify({model:response.model,questions:Object.keys(questions).length,choice:response.answers.overall,usage:response.usage},null,2));
}catch(e){
  // Never serialize request/client/error objects: they can contain credentials.
  console.error(JSON.stringify({errorType:e.name,status:e.status??null,code:e.cause?.code??null}));
  process.exitCode=1;
}

