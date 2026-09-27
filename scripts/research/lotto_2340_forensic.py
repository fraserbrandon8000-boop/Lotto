"""Frozen Codex Lotto #2340 forensics; no Jev call or future prediction."""
import sys,json,csv,hashlib,itertools,math
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
from common import save,csvsave,clean,holm,hg,pmean,blockci
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'));import analyze as v1
V=R/'results/lotto/draw2340';O=R/'results/lotto/forensic_2340';O.mkdir(exist_ok=True)
W={6,8,12,14,18,31};LOSERS={5,11,16,24,27,34};SIZES=[6,8,10,12,15,20,25];MODELS=['A_long','B_recent','C_gap','D_trend','G_marginal_proxy'];SEED=234020260926
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def csvread(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def avg_ranks(x):
    x=np.asarray(x);return np.array([(np.sum(x<v)+1+np.sum(x<=v))/2 for v in x])
def corr(x,y):return float(np.corrcoef(avg_ranks(x),avg_ranks(y))[0,1])
f=load(V/'frozen.json');assert f['target_draw']==2340 and f['cutoff_draw']==2339 and set(f['numbers'])==LOSERS
assert all(sha(R/p)==h for p,h in f['hashes'].items())
ledger=R/'results/lotto/prospective_ledger.jsonl';oldbytes=ledger.read_bytes();events=[json.loads(x) for x in oldbytes.decode().splitlines()];prediction=next(e for e in events if e.get('event')=='additional_prediction_frozen' and e.get('target_draw')==2340);assert prediction['sha256']==sha(V/'frozen.json')
protected={str(p.relative_to(R)):sha(p) for p in V.iterdir() if p.is_file()};protected.update(f['hashes']);save(O/'integrity.json',dict(verified=True,target=2340,cutoff=2339,seed=f['seed'],prediction=f['numbers'],frozen_sha256=sha(V/'frozen.json'),embedded_hash_count=len(f['hashes']),protected_hashes=protected))
protocol='Post-#2340 forensic only; no other-system work inspected and no new Jev request. Freeze verified before analysis. Historical training stops at #2339, 129 targets, original 50-draw warmup and 40-target reused confirmation. Current ranks are exact saved orders; no fabricated EW/transition/hazard/structure individual ranks. Reconstruct only the original 4096 source sample and H fallback using frozen code/seed, reconcile all twenty candidates exactly, distinguish source union from actual ticket tuples. Finite historical hypotheses: A/B/C/D/G marginal ranking; direct top6; exact maximum of additive mean score minus .25 standardized structure penalty within top8/10/12/15/20; seeded uniform six within top6/8/10/12/15/20/25; plus G 4096 search, G equal-weight512 and G active-component512. Use stored training-only weights, no target to construct ranks or tickets. E if flat is not informative; H random rank is a control. Number-discovery tests: mean and >=3/4/5/6 rates against exact same-size hypergeometric baseline, Holm across models/pools and across model/pool/event families. Construction uses existing corrected confirmation gate p<.05, block CI lower>36/38, both halves>random; additionally require positive paired CI vs original G and stable development direction for a V2 research challenger. Correct across unique construction rules. Discovery-to-construction loss is oracle pool capture minus actual hits; oracle uses hindsight and is not an executable forecast. Compare with random pool+uniform six baseline 6*(m-6)/38; condition on observed pool capture q to calculate expected hits 6*q/m and expected compression loss q*(1-6/m). Test whether actual ticket hits exceed conditional uniform construction with exact convolutions, Holm corrected. Report historical and confirmation periods separately. No #2340 fitting; no promoted parameter from this draw. No #2341 output.'
if not (O/'PROTOCOL.txt').exists():(O/'PROTOCOL.txt').write_text(protocol,encoding='utf-8')
outcome=dict(event='outcome_appended',recorded_utc=datetime.now(timezone.utc).isoformat(),draw_id=2340,date='2026-09-23',outcome=sorted(W),bonus=28,bonus_predicted=False,bonus_score=None,frozen_prediction=f['numbers'],main_matches=0,matched=[],prediction_sha256=sha(V/'frozen.json'),source='Official result supplied by user in attached request; no independent result fetch in this forensic task.')
old=[e for e in events if e.get('event')=='outcome_appended' and e.get('draw_id')==2340]
if old:assert all(old[0][k]==outcome[k] for k in ['outcome','bonus','frozen_prediction','main_matches'])
else:
    with ledger.open('a',encoding='utf-8') as h:h.write(json.dumps(outcome)+'\n')
assert ledger.read_bytes().startswith(oldbytes);save(O/'outcome.json',outcome)
records=load(V/'draws.json');assert records[-1]['draw_id']==2339 and len(records)==179
d=np.array([r['numbers'] for r in records])-1;a=v1.indicator(d);ranks=load(V/'refreshed_rankings.json');cs=load(V/'candidates.json');jev=load(V/'jev_response.json');ans=jev['answers'];probs=ans['overall']['probabilities'];wf=load(V/'walk_forward_predictions.json');weights=np.array(load(V/'candidate_sensitivity.json')['ensemble_weights']);ft=v1.model_features(a)
for c in cs:
    for e in c['individual_scores']:
        assert all(abs(e[k]-ft[0][i,e['number']-1])<1e-10 for i,k in enumerate(['long_z','recent_z','gap_z','trend_z']))
features={int(x['number']):x for x in csvread(V/'number_statistics.csv')};pairrows=csvread(V/'pair_statistics.csv');trans=csvread(V/'conditional_statistics.csv');evidence=[];coverage=[];minimum=[]
for n in sorted(W|LOSERS):
    models={m:dict(saved_rank=r['order'].index(n)+1,score=r['scores'][n-1],informative=r['informative'],score_tie_rank=[1+sum(s>r['scores'][n-1]+1e-12 for s in r['scores']),sum(s>=r['scores'][n-1]-1e-12 for s in r['scores'])]) for m,r in ranks.items()}
    memberships=[c for c in cs if n in c['numbers']]
    evidence.append(dict(number=n,group='winner' if n in W else 'selected loser',features=features[n],models=models,candidate_appearances=len(memberships),candidate_memberships=[c['id'] for c in memberships],eligible_candidate_memberships=[c['id'] for c in memberships if c['id'] in probs],candidate_generators=sorted({c['generator'] for c in memberships}),top12_informative_families=[m for m in MODELS if models[m]['informative'] and models[m]['saved_rank']<=12],candidate_sensitivity=[{k:c[k] for k in ['id','generator','sensitivity_top_quartile_fraction','generator_sensitivity_rank_min','generator_sensitivity_rank_max']} for c in memberships],transition_rows_from_latest=[r for r in trans if int(r['previous_number']) in records[-1]['numbers'] and int(r['next_number'])==n],limitations='No standalone EW, transition, hazard, structure, random-control or alternate adaptive marginal rank persisted. Per-number sensitivity not stored; candidate-level evidence remains labelled.'))
for m,r in ranks.items():
    winner_positions=sorted(r['order'].index(n)+1 for n in W)
    minimum.append(dict(model=m,informative=r['informative'],top_for3=winner_positions[2],top_for4=winner_positions[3],top_for5=winner_positions[4],top_for6=winner_positions[5]))
    for size in SIZES:
        winners=sorted(W&set(r['order'][:size]));coverage.append(dict(model=m,pool=size,informative=r['informative'],count=len(winners),winners=winners,random_mean=6*size/38))
save(O/'number_evidence.json',evidence);csvsave(O/'coverage_2340.csv',coverage);save(O/'minimum_discovery_pool.json',minimum)
scored=[]
for c in cs:
    match=sorted(set(c['numbers'])&W);scored.append(dict(id=c['id'],numbers=c['numbers'],generator=c['generator'],matches=len(match),matched=match,eligible_for_additional_ticket=c['id'] in probs,choice_probability=probs.get(c['id']),model_agreement=c['contributing_models'],saved_jev={k:ans[c['id']+'_'+k] for k in ['robustness','consensus','quality','overfit','stable','stronger','dependent']} if c['id'] in probs else None))
for c in scored:
    c['rank_all']=[1+sum(x['matches']>c['matches'] for x in scored),sum(x['matches']>=c['matches'] for x in scored)]
    c['rank_eligible']=[1+sum(x['matches']>c['matches'] for x in scored if x['eligible_for_additional_ticket']),sum(x['matches']>=c['matches'] for x in scored if x['eligible_for_additional_ticket'])] if c['eligible_for_additional_ticket'] else None
save(O/'candidate_outcomes.json',scored);save(O/'frozen_jev_analysis.json',dict(model=jev['model'],overall=ans['overall'],per_candidate={c['id']:c['saved_jev'] for c in scored},response_sha256=sha(V/'jev_response.json'),new_Jev_calls=0))
# Replay exact source tuples, not a fitted retrospective constructor.
pool=v1.sample(np.random.default_rng(v1.SEED+999),4096);values=v1.objectives(pool,ft);val=np.vstack([values,weights@values]);selected=[];sources=[];indices=[]
for j in range(7):
    count=0
    for idx in np.argsort(-val[j],kind='stable'):
        ticket=pool[idx]
        if all(len(set(ticket)&set(old))<=3 for old in selected):selected.append(ticket);sources.append(v1.NAMES[j]);indices.append(int(idx));count+=1
        if count==(1 if j==6 else 3):break
rng=np.random.default_rng(v1.SEED+555);fallback=[]
while len(selected)<20:
    t=v1.sample(rng,1)[0];fallback.append((t+1).tolist())
    if all(len(set(t)&set(old))<=3 for old in selected):selected.append(t);sources.append('H_random');indices.append(None)
assert all((t+1).tolist()==c['numbers'] and source==c['generator'] for t,source,c in zip(selected,sources,cs))
actual=sorted(W);found=np.flatnonzero(np.all(pool+1==np.array(actual),axis=1));union=set((pool+1).ravel().tolist());fallbackfound=actual in fallback
reachable=dict(replay_all20_exact=True,source_pool_size=4096,source_pool_unique=len(np.unique(pool,axis=0)),source_seed=v1.SEED+999,source_union_contains_all_winners=W<=union,exact_winning_tuple_in_source=bool(len(found)),exact_indices=found.tolist(),fallback_draw_count=len(fallback),exact_in_fallback=fallbackfound,exact_in_candidates=any(c['numbers']==actual for c in cs),winning_previous_primary_overlap=sorted(W&{1,4,13,14,24,38}),topN_pools_used_by_active_V1=False,post_C03_diversity_conflict=sorted(W&set(cs[2]['numbers'])),candidate_union_missing_winners=sorted(W-{n for c in cs for n in c['numbers']}),reason='Active V1 copies complete tuples from a fixed uniform sample; individual source-pool union coverage does not allow arbitrary assembly. Diagnostic top-N pools were not active V1 constructors. If the exact tuple is absent, it was not scored or displaced by structure/diversity; later hypothetical constraints are not its actual exclusion cause.')
save(O/'source_replay.json',dict(source_pool=(pool+1),selected_indices=indices,fallback=fallback));save(O/'reachability.json',reachable)
# Association among the actual 16 Jev options only; excluded options are missing, not zero.
evaluated=[c for c in scored if c['eligible_for_additional_ticket']];px=np.array([c['choice_probability'] for c in evaluated]);hits=np.array([c['matches'] for c in evaluated]);rho=corr(px,hits);r=np.random.default_rng(SEED);null=v1.sample(r,20000)+1;membership=np.array([[n in c['numbers'] for n in range(1,39)] for c in evaluated],int);simhits=membership[:,null-1].sum(2).T;rx=avg_ranks(px);rx-=rx.mean();rhos=[]
for row in simhits:
    ry=avg_ranks(row);ry-=ry.mean();den=np.linalg.norm(rx)*np.linalg.norm(ry);rhos.append(float(rx@ry/den) if den else 0.)
save(O/'jev_association.json',dict(n=16,spearman=rho,whole_draw_null_replicates=20000,two_sided_mc_p=(1+np.sum(np.abs(rhos)>=abs(rho)))/20001,choice_weighted_matches=float(px@hits),unweighted_matches=float(hits.mean()),interpretation='One overlapping candidate set, one draw; descriptive only. Omitted options are not assigned zero probabilities.'))

# Historical discovery and finite construction tests. Target #2340 never enters d.
comb_ix={m:np.array(list(itertools.combinations(range(m),6))) for m in [8,10,12,15,20]};hist=[];construction=[];loss=[]
for wi,row in enumerate(wf):
    t=row['index'];drawid=row['draw_id'];f0=v1.model_features(a[:t]);w=np.array(row['ensemble_weights']);ss={name:f0[0][i] for i,name in enumerate(v1.NAMES[:4])};ss['G_marginal_proxy']=w[:5]@f0[0];ss['H_random']=np.random.default_rng(v1.SEED+drawid*3037).random(38)
    orders={m:np.argsort(-(s+np.random.default_rng(v1.SEED+drawid).random(38)*1e-10)) for m,s in ss.items()};made={};pooltickets=[]
    for m in MODELS:
        order=orders[m];s=ss[m];made[m+':top6']=order[:6]
        for size in SIZES:
            uniform=np.sort(np.random.default_rng(SEED+drawid*97+size).choice(order[:size],6,replace=False));made[f'{m}:top{size}:uniform']=uniform
            pooltickets.extend([(m,size,'direct_top6',order[:6]),(m,size,'uniform',uniform)])
            if size in comb_ix:
                combos=np.sort(order[:size][comb_ix[size]],axis=1);merit=s[combos].mean(1);pen=np.mean(((v1.structure(combos)-f0[2])/f0[3])**2,axis=1);best=combos[np.argmax(merit-.25*pen)];made[f'{m}:top{size}:structure025']=best;pooltickets.append((m,size,'structure025',best))
    p512=v1.sample(np.random.default_rng(v1.SEED+drawid*101),512);v=v1.objectives(p512,f0);active=v.std(1)>1e-12;aw=w*active;aw=aw/aw.sum() if aw.sum()>1e-12 else active/active.sum();made['G_active512']=p512[np.argmax(aw@v)];made['G_equal512']=p512[np.argmax(v.mean(0))]
    p4096=v1.sample(np.random.default_rng(v1.SEED+drawid*101),4096);vv=v1.objectives(p4096,f0);made['G_4096']=p4096[np.argmax(w@vv)]
    # Only now reveal the current target for scoring.
    truth=a[t]
    for m,order in orders.items():
        for size in SIZES:hist.append(dict(index=t,draw_id=drawid,period=row['period'],model=m,pool=size,hits=int(truth[order[:size]].sum())))
    for method,ticket in made.items():construction.append(dict(index=t,draw_id=drawid,training_cutoff=row['training_last_draw_id'],period=row['period'],method=method,numbers=(np.sort(ticket)+1),hits=int(truth[ticket].sum()),v1_G=row['matches'][6]))
    for m,size,method,ticket in pooltickets:
        q=int(truth[orders[m][:size]].sum());hit=int(truth[ticket].sum());loss.append(dict(index=t,draw_id=drawid,period=row['period'],model=m,pool=size,constructor=method,oracle=q,actual=hit,loss=q-hit,conditional_uniform_expected_hits=6*q/size,conditional_expected_loss=q*(1-6/size)))
    if wi%30==0:print('Historical target',wi+1,'of',len(wf),flush=True)
save(O/'historical_discovery_origins.json',hist);save(O/'construction_origins.json',construction);save(O/'compression_origins.json',loss)
coverage_summary=[];cp=[];lp=[]
for period in ['all','development','confirmation']:
    subset=lambda data:[x for x in data if period=='all' or x['period']==period]
    hh=subset(hist);co=subset(construction);lo=subset(loss)
    for m in ss:
        for size in SIZES:
            yy=np.array([x['hits'] for x in hh if x['model']==m and x['pool']==size]);pmf=hg(38,6,size);events={}
            for k in [3,4,5,6]:
                prob=float(pmf[k:].sum());count=int(np.sum(yy>=k));events[str(k)]=dict(count=count,rate=count/len(yy),random_rate=prob,p=float(v1.binom_probs(len(yy),prob)[count:].sum()))
            coverage_summary.append(dict(period=period,model=m,pool=size,n=len(yy),mean=float(yy.mean()),random_mean=6*size/38,p=pmean(yy,38,6,size),events=events))
    sub=[x for x in coverage_summary if x['period']==period]
    for x,p in zip(sub,holm([x['p'] for x in sub])):x['holm_p']=p
    ev=[e for x in sub for e in x['events'].values()]
    for x,p in zip(ev,holm([x['p'] for x in ev])):x['holm_p']=p
    for method in sorted({x['method'] for x in co}):
        yy=[x for x in co if x['method']==method];y=np.array([x['hits'] for x in yy]);base=np.array([x['v1_G'] for x in yy]);cp.append(dict(period=period,method=method,n=len(y),mean=float(y.mean()),rates=np.bincount(y,minlength=7)/len(y),ci=blockci(y),p=pmean(y,38,6,6),older=float(y[:len(y)//2].mean()),recent=float(y[len(y)//2:].mean()),paired_delta=float(np.mean(y-base)),paired_ci=blockci(y-base)))
    sub=[x for x in cp if x['period']==period]
    for x,p in zip(sub,holm([x['p'] for x in sub])):x['holm_p']=p;x['passes_gate']=bool(period=='confirmation' and p<.05 and x['ci'][0]>36/38 and min(x['older'],x['recent'])>36/38 and x['paired_ci'][0]>0)
    for m,size,method in sorted({(x['model'],x['pool'],x['constructor']) for x in lo}):
        rr=[x for x in lo if x['model']==m and x['pool']==size and x['constructor']==method];q=np.array([x['oracle'] for x in rr]);hit=np.array([x['actual'] for x in rr]);expected=6*q/size;dist=np.array([1.])
        for count in q:dist=np.convolve(dist,hg(size,int(count),6))
        conditional_p=float(dist[int(hit.sum()):].sum());lp.append(dict(period=period,model=m,pool=size,constructor=method,n=len(rr),oracle_mean=float(q.mean()),actual_mean=float(hit.mean()),oracle_loss_mean=float(np.mean(q-hit)),random_pool_uniform_ticket_loss=6*(size-6)/38,conditional_uniform_hits_mean=float(expected.mean()),conditional_uniform_loss_mean=float(np.mean(q-expected)),conditional_excess_hits=float(np.mean(hit-expected)),conditional_excess_ci=blockci(hit-expected),conditional_uniform_p=conditional_p))
    sub=[x for x in lp if x['period']==period]
    for x,p in zip(sub,holm([x['conditional_uniform_p'] for x in sub])):x['holm_p']=p
save(O/'historical_discovery.json',coverage_summary);save(O/'construction_performance.json',cp);save(O/'compression_analysis.json',lp)
# Equivalent random pool + uniform ticket nulls, preserving nesting.
rng=np.random.default_rng(SEED+1);controls=[]
for size in SIZES:
    q=rng.hypergeometric(6,32,size,(20000,40));hits=rng.hypergeometric(q,size-q,6);controls.append(dict(pool=size,replicates=20000,origins=40,mean_loss=float((q-hits).mean()),theoretical_loss=6*(size-6)/38,mean_loss95=np.quantile((q-hits).mean(1),[.025,.975])))
save(O/'random_compression_controls.json',controls)
passed=[x for x in cp if x['passes_gate']];save(O/'v2_decision.json',dict(created=False,qualified_methods=passed,conclusion='No Lotto V2 is justified.' if not passed else 'Additional stability review required before creating a challenger',no_2341_generated=True))
assert all(sha(R/p)==h for p,h in protected.items())
save(O/'verification.json',dict(all_frozen_files_unchanged=True,ledger_append_only=True,bonus_not_scored=True,source_replay_matches_all20=True,historical_cutoff=2339,origins=len(wf),fresh_Jev_calls=0,other_systems_inspected=False,no_2341_generated=True))
print(json.dumps(clean(dict(reachability=reachable,best_candidates=[c['id'] for c in scored if c['matches']==max(x['matches'] for x in scored)],distribution={str(i):sum(c['matches']==i for c in scored) for i in range(7)},qualified=passed)),indent=2))
