// Jev EVIDENCE AUDIT of a frozen Super Lotto P0 portfolio. One call after the portfolio is frozen; cannot modify tickets.
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {pathToFileURL} from 'node:url';
import {resolve as resolvePath} from 'node:path';
import {TypeSafeClient,score,noul} from '@typesafe-ai/sdk';
const DIR=pathToFileURL(resolvePath(process.env.SL_DIR)+'/p0_jev_audit/');
const frozen=JSON.parse(await readFile(new URL('../p0/p0_frozen.json',DIR),'utf8'));
const stateText=await readFile(new URL('audit_state.json',DIR),'utf8');const state=JSON.parse(stateText);
assert.deepEqual(state.portfolio[1].mains,frozen.ticket_2.mains);assert.deepEqual(state.portfolio[2].mains,frozen.ticket_3.mains);
const levels=['No empirical support beyond random: every relevant model fails corrected testing and results match random controls.','Weak or fragile apparent support: small uncorrected differences, unstable across periods or settings.','Some repeatable out-of-sample support, but no corrected confirmation and substantial uncertainty.','Corrected confirmation-period support that is stable across sensitivity settings.','Strong support replicated across independent models, periods and prospective outcomes.'];
const q={};
for(const t of [1,2,3]){
  const ref=`Consider ONLY ticket ${t} at \`portfolio[${t-1}]\` (five mains plus one Super Ball) using only the supplied evidence. `;
  q[`t${t}_robustness`]=score(ref+'How robust is the empirical evidence that this complete ticket is better than a random Super Lotto ticket?',levels);
  q[`t${t}_overfit`]=noul(ref+'Is chance or overfitting a better explanation of any apparent support for this ticket than a reproducible predictive signal?',{true:'Apparent support is compatible with noise: corrected tests fail or gains vanish against random comparators.',false:'Support survives corrected out-of-sample tests and random-control comparisons.'});
  q[`t${t}_weak_models`]=noul(ref+'Does the selection of this ticket depend mainly on weak or unvalidated models, or on a mechanical rule (seeded fallback, coverage convention) rather than validated evidence?',{true:'Its selection rests on unvalidated models, zero-credibility weights, a coverage convention or a seeded fallback.',false:'Its selection rests mainly on evidence that passed corrected validation.'});
  q[`t${t}_concentration`]=noul(ref+'Is whatever support this ticket has concentrated in one model family or in correlated families rather than spread across genuinely independent evidence?',{true:'Support comes from one family or from correlated families.',false:'Support comes from several genuinely independent families.'});
  q[`t${t}_fragility`]=noul(ref+'Would modest, reasonable changes to the construction (main pool size, Super Ball rule, tie-break convention) likely replace most of this ticket? Use `computed_sensitivity_research_only` where it applies.',{true:'Most of the ticket changes under reasonable alternative settings.',false:'The ticket stays largely the same under reasonable alternative settings.'});
}
const p='Consider the WHOLE three-ticket portfolio at `portfolio` with `portfolio_facts`, `p0_protocol` and `historical_confirmation_40_draws`. ';
q.portfolio_robustness=score(p+'How robust is the evidence that this portfolio outperforms three diversified random Super Lotto tickets?',levels);
q.portfolio_edge=noul(p+'Does the supplied evidence show that this portfolio has a higher expected number of main or Super Ball matches than random diversified tickets?',{true:'A corrected historical gate passed and comparisons with random portfolios exclude zero.',false:'The historical gate failed or comparison intervals include zero.'});
q.portfolio_overfit=noul(p+'Is chance or overfitting a better explanation of any favourable historical or shadow result than a reproducible signal?',{true:'Favourable results are within random variation or rest on one draw.',false:'Favourable results are corrected, repeatable and exceed random variation.'});
q.portfolio_concentration=noul(p+'Is the evidence behind the challenger tickets concentrated in one model family or correlated families?',{true:'Challenger support comes mostly from one family or correlated families, or from no validated family at all.',false:'Challenger support is spread across independent validated families.'});
q.portfolio_coverage=score(p+'How well does the portfolio achieve its stated, non-predictive goal of covering many distinct main numbers and Super Balls with low redundancy?',['Poor: tickets largely duplicate each other.','Limited: substantial overlap in mains or repeated Super Balls.','Moderate: some overlap; coverage clearly broader than one ticket.','Good: low main overlap and distinct Super Balls.','Maximal: no main overlap and three distinct Super Balls.']);
const request={model:'jev-latest',state,questions:q};await writeFile(new URL('audit_request.json',DIR),JSON.stringify(request,null,2),{flag:'wx'});
assert.ok(process.env.TYPESAFE_API_KEY?.trim());const client=new TypeSafeClient({baseURL:'https://api.typesafe.ai',logLevel:'off',timeout:60000,retry:{maxRetries:0}});
const response=await client.systemOne(request);for(const [id,x] of Object.entries(q)){assert.ok(response.answers[id],id);assert.equal(response.answers[id].type,x.type);}
await writeFile(new URL('audit_response.json',DIR),JSON.stringify(response,null,2),{flag:'wx'});
await writeFile(new URL('audit_receipt.json',DIR),JSON.stringify({created_utc:new Date().toISOString(),model:response.model,questions:Object.keys(q).length,state_sha256:createHash('sha256').update(stateText).digest('hex'),request_sha256:createHash('sha256').update(JSON.stringify(request)).digest('hex'),frozen_portfolio_sha256:createHash('sha256').update(await readFile(new URL('../p0/p0_frozen.json',DIR))).digest('hex'),usage:response.usage,note:'Evidence audit only; cannot modify any ticket; not winning probabilities.'},null,2),{flag:'wx'});
console.log(JSON.stringify({model:response.model,answers:Object.fromEntries(Object.entries(response.answers).map(([k,v])=>[k,v.score??v.noul]))},null,1));
