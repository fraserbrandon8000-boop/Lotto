// Jev EVIDENCE AUDIT of the frozen #2342 P0 portfolio. Called once, after the portfolio is frozen.
// The audit cannot modify, reorder or replace any ticket. Built with the installed TypeSafe skill and
// @typesafe-ai/sdk 0.6.0 types (live docs unreachable from this environment).
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {TypeSafeClient,score,noul} from '@typesafe-ai/sdk';

const DIR=new URL('../../results/lotto/draw2342/p0_jev_audit/',import.meta.url);
const frozen=JSON.parse(await readFile(new URL('../p0/p0_frozen.json',DIR),'utf8'));
const stateText=await readFile(new URL('audit_state.json',DIR),'utf8');
const state=JSON.parse(stateText);
assert.deepEqual(state.portfolio[1].numbers,frozen.ticket_2);assert.deepEqual(state.portfolio[2].numbers,frozen.ticket_3);

const robustLevels=[
  'No empirical support beyond random: every relevant methodology fails corrected testing and results match random controls.',
  'Weak or fragile apparent support: small uncorrected differences, unstable across periods or settings.',
  'Some repeatable out-of-sample support, but no corrected confirmation and substantial uncertainty.',
  'Corrected confirmation-period support that is stable across sensitivity settings.',
  'Strong support replicated across independent models, time periods and prospective outcomes.'];
const questions={};
for(const t of [1,2,3]){
  const ref=`Consider ONLY ticket ${t} at \`portfolio[${t-1}]\` in the context of the supplied evidence. `;
  questions[`t${t}_robustness`]=score(ref+'How robust is the empirical evidence that this specific ticket is better than a random ticket?',robustLevels);
  questions[`t${t}_overfit`]=noul(ref+'Is chance or overfitting a better explanation of any apparent support for this ticket than a reproducible predictive signal?',
    {true:'Apparent support is compatible with noise: corrected tests fail, gains vanish against random comparators, or support comes from in-sample fitting.',false:'Support survives corrected, out-of-sample tests and random-control comparisons.'});
  questions[`t${t}_weak_evidence`]=noul(ref+'Does the selection of this ticket depend mainly on evidence that failed corrected statistical validation (or on a mechanical rule rather than evidence)?',
    {true:'Its selection rests on unvalidated weights, shrunk null evidence, coverage mechanics or a seeded fallback.',false:'Its selection rests mainly on evidence that passed corrected validation.'});
  questions[`t${t}_concentration`]=noul(ref+'Is whatever support this ticket has concentrated in one model family or in correlated families (for example B_recent and D_trend, which are correlated), rather than spread across genuinely independent evidence?',
    {true:'Support comes from one family or from families that share information.',false:'Support comes from several genuinely independent families.'});
  questions[`t${t}_fragility`]=noul(ref+'Would modest, reasonable changes to the construction (pool size, shrinkage strength, removing the weak evidence weights, tie-breaks) likely replace most of this ticket? Use `computed_sensitivity_research_only` where it applies.',
    {true:'Most of the ticket changes under reasonable alternative settings.',false:'The ticket stays largely the same under reasonable alternative settings.'});
}
const pref='Consider the WHOLE three-ticket portfolio at `portfolio` together with `portfolio_facts`, `p0_protocol` and `historical_confirmation_40_draws`. ';
questions.portfolio_robustness=score(pref+'How robust is the evidence that this portfolio as a whole outperforms three diversified random tickets?',robustLevels);
questions.portfolio_edge=noul(pref+'Does the supplied evidence show that this portfolio has a higher expected number of matches than random diversified tickets?',
  {true:'A corrected historical test passed and the comparison with random portfolios excludes zero.',false:'The historical gate failed or the comparison intervals include zero.'});
questions.portfolio_overfit=noul(pref+'Is chance or overfitting a better explanation of any favourable historical or shadow result of this portfolio than a reproducible signal?',
  {true:'Favourable results are within random variation or depend on one draw.',false:'Favourable results are corrected, repeatable and exceed random variation.'});
questions.portfolio_concentration=noul(pref+'Is the evidence behind the challenger tickets concentrated in one model family or correlated families?',
  {true:'Challenger support comes mostly from one family or correlated families.',false:'Challenger support is spread across independent families.'});
questions.portfolio_coverage=score(pref+'How well does the portfolio achieve its stated, non-predictive goal of covering many distinct model-supported numbers with low redundancy?',[
  'Poor: tickets largely duplicate each other and cover few distinct numbers.',
  'Limited: substantial overlap; coverage little better than a single ticket plus noise.',
  'Moderate: some overlap; coverage clearly broader than a single ticket.',
  'Good: low overlap and broad coverage of the discovery pool.',
  'Maximal: no overlap and the widest feasible coverage of the discovery pool.']);

const request={model:'jev-latest',state,questions};
await writeFile(new URL('audit_request.json',DIR),JSON.stringify(request,null,2));
assert.ok(process.env.TYPESAFE_API_KEY?.trim(),'TYPESAFE_API_KEY unavailable');
const client=new TypeSafeClient({baseURL:'https://api.typesafe.ai',logLevel:'off',timeout:60000});
const response=await client.systemOne(request);
for(const [id,q] of Object.entries(questions)){const a=response.answers[id];assert.ok(a,`Missing ${id}`);assert.equal(a.type,q.type);}
await writeFile(new URL('audit_response.json',DIR),JSON.stringify(response,null,2));
await writeFile(new URL('audit_receipt.json',DIR),JSON.stringify({created_utc:new Date().toISOString(),model:response.model,questions:Object.keys(questions).length,
  state_sha256:createHash('sha256').update(stateText).digest('hex'),request_sha256:createHash('sha256').update(JSON.stringify(request)).digest('hex'),
  frozen_portfolio_sha256:createHash('sha256').update(await readFile(new URL('../p0/p0_frozen.json',DIR))).digest('hex'),usage:response.usage,
  note:'Evidence audit only. Cannot modify, reorder or replace any ticket. Probabilities are judgments about the supplied evidence, not winning probabilities.'},null,2));
console.log(JSON.stringify({model:response.model,usage:response.usage,answers:Object.fromEntries(Object.entries(response.answers).map(([k,v])=>[k,v.score??v.noul]))},null,1));
