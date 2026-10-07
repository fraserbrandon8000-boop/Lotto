// RESEARCH ONLY (post-freeze): Jev option-order and blinded-ID sensitivity for the frozen V1 production state.
// Three Choice-only calls on the SAME evidence: (A) original order, (B) reversed candidate order, (C) shuffled blinded IDs
// with the generator label removed. Responses saved before any check. Usage: SRC OUT SEED
import {readFile,writeFile} from 'node:fs/promises';
import {TypeSafeClient} from '@typesafe-ai/sdk';
const [SRC,OUT,SEED]=process.argv.slice(2);
const req=JSON.parse(await readFile(`${SRC}/jev_request.json`,'utf8'));const q0=req.questions.overall;const ids=Object.keys(q0.criteria);
let s=Number(SEED);const rnd=()=>{s=(s*1103515245+12345)%2147483648;return s/2147483648;};
const perm=[...ids];for(let i=perm.length-1;i>0;i--){const j=Math.floor(rnd()*(i+1));[perm[i],perm[j]]=[perm[j],perm[i]];}
const blind=Object.fromEntries(ids.map((id,k)=>[id,'K'+String(Number(perm.indexOf(id))+1).padStart(2,'0')]));
function build(kind){
  const st=JSON.parse(JSON.stringify(req.state));let cands=st.candidates;let order=[...ids];let map=Object.fromEntries(ids.map(i=>[i,i]));
  if(kind==='reversed'){cands=[...cands].reverse();order=[...ids].reverse();}
  if(kind==='blinded'){map=blind;cands=cands.map(c=>{const x={...c,id:blind[c.id]};delete x.generator;return x;}).sort((a,b)=>a.id.localeCompare(b.id));order=ids.map(i=>blind[i]).sort();}
  st.candidates=cands;const criteria=Object.fromEntries(order.map(o=>[o,`Candidate ${o}, evidence at candidates entry with id ${o}.`]));
  return {req:{model:'jev-latest',state:st,questions:{overall:{...q0,criteria}}},map};
}
const client=new TypeSafeClient({baseURL:'https://api.typesafe.ai',logLevel:'off',timeout:60000});const out={};
for(const kind of ['original_order','reversed','blinded']){
  const {req:r,map}=build(kind);const resp=await client.systemOne(r);await writeFile(`${OUT}/${kind}_response.json`,JSON.stringify(resp,null,2),{flag:'wx'});
  const inv=Object.fromEntries(Object.entries(map).map(([a,b])=>[b,a]));const p=resp.answers.overall.probabilities;
  out[kind]={created_utc:new Date().toISOString(),model:resp.model,choice_original_id:inv[resp.answers.overall.choice],confidence:resp.answers.overall.confidence,probabilities_original_ids:Object.fromEntries(Object.entries(p).map(([k,v])=>[inv[k],v]))};
  console.log(kind,out[kind].choice_original_id,out[kind].confidence);
}
await writeFile(`${OUT}/order_blind_summary.json`,JSON.stringify({seed:Number(SEED),blind_map:blind,results:out,note:'Research only, after the #2344 freeze (f248e15). Choice-only requests on the frozen V1 evidence; cannot change tickets.'},null,2),{flag:'wx'});
