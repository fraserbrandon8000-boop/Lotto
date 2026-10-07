"""Lotto #2344 system audit: data, prospective re-score, #2342/#2343 construction counterfactuals, V1 source pool,
structure distributions, Jev (saved calls only) and code/reproducibility facts. Research only; Lotto data only."""
import sys,json,math,itertools,csv,hashlib,subprocess,re
from pathlib import Path
from collections import Counter
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'));sys.path.insert(0,str(R/'scripts/research'))
import analyze as a,v1_history as V
O=R/'results/lotto/system_audit_2344/data';O.mkdir(parents=True,exist_ok=True);L=R/'results/lotto'
J=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *x:subprocess.run(['git',*x],cwd=R,capture_output=True,text=True).stdout.strip()
def save(n,o):(O/n).write_text(json.dumps(a.clean(o),indent=1,allow_nan=False))
CN=math.comb(38,6);HG=np.array([math.comb(6,k)*math.comb(32,6-k)/CN for k in range(7)])
W2343=[4,7,13,23,33,35]
# ------------------------------------------------------------------ A13 data audit
recs=J(L/'draw2343/draws.json')+[dict(draw_id=2343,date='2026-10-03',numbers=W2343,bonus=38,origin='official_user_supplied',source='User-supplied official result in the #2344 audit task (2026-10-07)')]
from datetime import date
ds=[date.fromisoformat(r['date']) for r in recs]
issues=[]
for i,r in enumerate(recs):
    n=r['numbers']
    if len(n)!=6 or len(set(n))!=6:issues.append((r['draw_id'],'not six unique'))
    if not all(1<=x<=38 for x in n):issues.append((r['draw_id'],'range'))
    if n!=sorted(n):issues.append((r['draw_id'],'unsorted'))
    b=r.get('bonus')
    if b is None or not 1<=b<=38:issues.append((r['draw_id'],'bonus invalid'))
    elif b in n:issues.append((r['draw_id'],'bonus duplicates a main'))
    if i and r['draw_id']!=recs[i-1]['draw_id']+1:issues.append((r['draw_id'],'id gap'))
    if i and ds[i]<=ds[i-1]:issues.append((r['draw_id'],'date order'))
wd=Counter(x.strftime('%a') for x in ds);gaps=Counter((ds[i]-ds[i-1]).days for i in range(1,len(ds)))
orig=Counter(r.get('origin','workbook' if 'row' in r else 'unknown') for r in recs)
rec2252=[dict(draw_id=r['draw_id'],origin=r.get('origin'),source=str(r.get('source'))[:120]) for r in recs if 2252<=r['draw_id']<=2261]
# power: draws needed to detect a per-ticket mean-match uplift delta at alpha .05 one-sided, power .8
sd=math.sqrt(6*(6/38)*(32/38)*(32/37))
power={str(dl):math.ceil(((1.645+0.842)*sd/dl)**2) for dl in [0.05,0.1,0.2,0.3]}
# jackpot-rate detection: draws needed for >=1 expected jackpot with 3 tickets
data=dict(n=len(recs),first=recs[0]['draw_id'],last=recs[-1]['draw_id'],first_date=recs[0]['date'],last_date=recs[-1]['date'],issues=issues,weekday_counts=dict(wd),day_gap_counts={str(k):v for k,v in sorted(gaps.items())},
  provenance=dict(orig),recovered_2252_2261=rec2252,bonus_used_by_models=False,
  bonus_check='grep of scripts/analyze.py and scripts/research/p0.py: model features use r["numbers"] only; bonus appears only in audit/ledger fields',
  rule_continuity='All 183 rows are 6 unique mains in 1-38 plus a separate bonus; Wednesday/Saturday cadence throughout; no format change inside the window.',
  deeper_history='Same-rule Lotto history before 2025-01-01 (#2161) is not in the repository. The official results service is unreachable from this environment (network policy), so it cannot be fetched or provenance-verified here.',
  power_draws_needed_per_ticket_mean_uplift=power,draws_for_one_expected_jackpot_3_tickets=CN/3,
  note_power='Detecting even a +0.1 mean-match uplift per ticket needs ~%s draws; the dataset has %d. A 6/6 rate can never be validated empirically (one expected 3-ticket jackpot per %.0f draws, ~%.0f years at 2 draws/week).'%(power['0.1'],len(recs),CN/3,CN/3/104))
save('data_audit.json',data)
# ------------------------------------------------------------------ A21 prospective re-score from frozen artifacts
OUT={2339:([1,4,6,13,23,28],20),2340:(None,None),2341:([1,4,6,22,33,38],34),2342:([12,13,14,15,19,33],21),2343:(W2343,38)}
for r in recs:
    if r['draw_id'] in OUT:OUT[r['draw_id']]=(r['numbers'],r['bonus'])
fd=J(R/'results/final_decision.json')
tickets={2339:[('V1_primary',fd['primary']['numbers'],fd['primary']['generator'],fd['primary']['id']),('V1_secondary',fd['secondary']['numbers'],fd['secondary']['generator'],fd['secondary']['id'])]}
jevfav={2339:J(R/'results/jev_response.json')['answers']['overall']['choice']}
cands={2339:J(R/'results/candidates.json')}
for t in [2340,2341,2342,2343]:
    f=J(L/f'draw{t}/frozen.json');tickets[t]=[('V1',f['numbers'],f['generator'],f['candidate_id'])];jevfav[t]=f['jev_preferred_candidate'];cands[t]=J(L/f'draw{t}/candidates.json')
    if (L/f'draw{t}/p0/p0_frozen.json').exists():
        p=J(L/f'draw{t}/p0/p0_frozen.json');pr=J(L/f'draw{t}/p0/p0_result.json');tickets[t]+=[('P0_coverage_1',p['ticket_2'],'P0','T2'),('P0_coverage_2',p['ticket_3'],'P0','T3')]
    if (L/f'random_control_{t}/random_control_frozen.json').exists():
        rc=J(L/f'random_control_{t}/random_control_frozen.json');tickets[t]+=[(f'random_control_{i+1}',x,'random','RC') for i,x in enumerate(rc['tickets'])]
pros=[]
for t,ts in tickets.items():
    w,b=OUT[t];jf=[c for c in cands[t] if c['id']==jevfav[t]][0]
    for track,nums,gen,cid in ts:
        pros.append(dict(draw=t,track=track,ticket=nums,generator=gen,candidate=cid,outcome=w,bonus=b,main_matches=len(set(nums)&set(w)),matched=sorted(set(nums)&set(w)),bonus_on_ticket=b in nums,
                         jev_favourite=jevfav[t],jev_favourite_ticket=jf['numbers'],jev_favourite_matches=len(set(jf['numbers'])&set(w))))
def portfolio_best(t,prefixes):
    m=[x['main_matches'] for x in pros if x['draw']==t and x['track'].startswith(prefixes)];return max(m) if m else None
summary=dict(v1=[(x['draw'],x['main_matches']) for x in pros if x['track'] in ('V1','V1_primary')],
  p0_portfolio_best={t:portfolio_best(t,('V1','P0')) for t in [2342,2343]},p0_challenger_best={t:portfolio_best(t,('P0',)) for t in [2342,2343]},
  random_control_best={t:portfolio_best(t,('random',)) for t in [2342,2343]},
  null=dict(single_ticket_pmf=HG.tolist(),p_ge3=float(HG[3:].sum()),p_ge4=float(HG[4:].sum()),p_ge5=float(HG[5:].sum()),p6=float(HG[6])))
v1m=[m for _,m in summary['v1']];q=np.array([1.])
for _ in v1m:q=np.convolve(q,HG)
summary['v1_total']=sum(v1m);summary['v1_expected']=len(v1m)*36/38;summary['v1_p_total_ge']=float(q[sum(v1m):].sum())
summary['v1_ge3']=sum(m>=3 for m in v1m);summary['v1_p_ge3_count_ge_obs']=float(sum(math.comb(len(v1m),k)*HG[3:].sum()**k*(1-HG[3:].sum())**(len(v1m)-k) for k in range(summary['v1_ge3'],len(v1m)+1)))
summary['v1_distinct_tickets']=len({tuple(x['ticket']) for x in pros if x['track'] in ('V1','V1_primary')})
save('prospective_rescore.json',dict(entries=pros,summary=summary))
# ------------------------------------------------------------------ A4 / A22 construction counterfactuals #2342, #2343
def universe_csv(t):
    rows=list(csv.DictReader(open(L/f'draw{t}/p0/universe_scores.csv')))
    return [(int(r['rank_by_T']),[int(x) for x in r['numbers'].split()],float(r['T']),float(r['EQ'])) for r in rows]
cf={}
for t,win in [(2342,[12,13,14,15,19,33]),(2343,W2343)]:
    U=universe_csv(t);pr=J(L/f'draw{t}/p0/p0_result.json');pool=pr['pool'];avail=sorted(set(pool)&set(win));pf=J(L/f'draw{t}/p0/p0_frozen.json');v1=J(L/f'draw{t}/frozen.json')['numbers']
    port=[v1,pf['ticket_2'],pf['ticket_3']]
    contain=[r for r in U if set(avail)<=set(r[1])];ranks=[r[0] for r in contain]
    order=pr['pool_order_full'] if 'pool_order_full' in pr else None
    conc=sorted(order[:6]) if order else None
    top=[r[1] for r in U[:3]]
    # how many in-pool winners each frozen ticket holds; best possible
    cf[t]=dict(pool=pool,available_winners=avail,n_combos=len(U),n_containing_all_available=len(contain),expected_if_random=math.comb(15-len(avail),6-len(avail)),
      rank_min=min(ranks),rank_median=float(np.median(ranks)),rank_max=max(ranks),rank_percentile_mean=float(np.mean(ranks)/len(U)),
      best_containing=dict(rank=contain[0][0],numbers=contain[0][1],T=contain[0][2]) if contain else None,
      frozen_portfolio_inpool_hits=[len(set(x)&set(avail)) for x in port],frozen_ticket_T_ranks=[next((r[0] for r in U if r[1]==sorted(x)),None) for x in port],
      standalone_top3=[dict(numbers=x,available_hits=len(set(x)&set(avail))) for x in top],
      concentration_top6_numbers=dict(numbers=conc,available_hits=len(set(conc)&set(avail)) if conc else None),
      v1_inpool_numbers=sorted(set(v1)&set(pool)),
      weights=pr.get('weights') or pr.get('frozen_weights'))
save('construction_counterfactual_2342_2343.json',cf)
# ------------------------------------------------------------------ A10 V1 source pool (cutoff 2342 state that built #2343; all families)
records=J(L/'draw2343/draws.json');d=np.array([r['numbers'] for r in records])-1;ft=a.model_features(a.indicator(d))
src=a.sample(np.random.default_rng(a.SEED+999),4096)
rng=np.random.default_rng(7);ref=a.sample(rng,200000)          # 200k uniform reference combinations for the objective distribution
vs=a.objectives(src,ft);vr=a.objectives(ref,ft)
# objectives() z-scores within its own input, so recompute raw objective values on a common scale
def raw(pool):
    scores,mat,means,sdv,_=ft;v=np.empty((6,len(pool)));v[:4]=scores[:4,pool].mean(2)
    v[4]=np.array([mat[x[:,None],x[None,:]].sum()/30 for x in pool]) if len(pool)<=5000 else 0
    v[5]=-np.mean(((a.structure(pool)-means)/sdv)**2,axis=1);return v
rs=raw(src);rr=raw(ref[:50000])
pct={a.NAMES[j]:float(np.mean(rr[j]<=rs[j].max())) for j in [0,1,2,3,5]}
cand_src=dict(source_pool_size=4096,universe=CN,fraction_of_universe=4096/CN,same_pool_every_cutoff=True,seed='SEED+999 (data-independent, identical at every cutoff)',
  best_source_ticket_percentile_in_universe=pct,
  note='Percentile of the best of the 4,096 fixed source tickets among 50,000 uniform tickets, per V1 objective (cutoff #2342). E_pairs is flat (no retained pair).',
  H_random_fixed_ticket=[c['numbers'] for c in J(L/'draw2343/candidates.json') if c['generator']=='H_random'],
  H_random_in_all_pools=all(any(c['generator']=='H_random' and c['numbers']==[5,7,14,21,33,38] for c in J(L/f'draw{t}/candidates.json')) for t in [2340,2341,2342,2343]))
save('v1_source_pool.json',cand_src)
# ------------------------------------------------------------------ A12 structure distributions
def struct_stats(T):
    T=np.sort(np.asarray(T),1)+0;dd=np.diff(T,axis=1);runs=[]
    for r in dd:
        best=cur=1
        for x in r:
            cur=cur+1 if x==1 else 1;best=max(best,cur)
        runs.append(best)
    runs=np.array(runs);span4=np.array([min(T[i,j+3]-T[i,j] for j in range(3)) for i in range(len(T))])
    return dict(n=len(T),run_ge2=float(np.mean(runs>=2)),run_ge3=float(np.mean(runs>=3)),run_ge4=float(np.mean(runs>=4)),adjacent_pairs=float((dd==1).sum(1).mean()),dense4_within6=float(np.mean(span4<=5)),
                odd=float((T%2).sum(1).mean()),low_le19=float((T<=19).sum(1).mean()),sum_mean=float(T.sum(1).mean()),sum_sd=float(T.sum(1).std()),max_gap=float(dd.max(1).mean()))
allc=np.array(list(itertools.combinations(range(1,39),6)),dtype=np.int16)
sets=dict(exact_null_all_combinations=struct_stats(allc),actual_draws_2161_2343=struct_stats([r['numbers'] for r in recs]),V1_fixed_source_4096=struct_stats(src+1),
  V1_frozen_candidates_2339_2343=struct_stats([c['numbers'] for t in cands for c in cands[t]]),
  final_V1_tickets_2339_2343=struct_stats([x['ticket'] for x in pros if x['track'] in ('V1','V1_primary')]))
pu=[]
for t in [2342,2343]:pu+= [r[1] for r in universe_csv(t)]
sets['P0_universes_2342_2343']=struct_stats(pu)
hist=J(L/'p0_protocol/historical_origins.json')['rows'];sets['P0_historical_challengers_2231_2340']=struct_stats([x for r in hist for x in r['byK']['15']['portfolio'][1:]])
save('structure_distributions.json',dict(sets=sets,note='run = longest run of consecutive values; dense4 = some 4 numbers within a span of 5; low = <=19.'))
# ------------------------------------------------------------------ A19 Jev (saved calls only)
jrows=[];per={}
for t in [2339,2340,2341,2342,2343]:
    resp=J(R/'results/jev_response.json') if t==2339 else J(L/f'draw{t}/jev_response.json');w,_=OUT[t]
    pr=resp['answers']['overall']['probabilities'];cs={c['id']:c for c in cands[t]}
    ids=[i for i in pr];ch=np.array([pr[i] for i in ids]);m=np.array([len(set(cs[i]['numbers'])&set(w)) for i in ids])
    er=np.array([cs[i].get('ensemble_rank',np.nan) for i in ids],float);ag=np.array([cs[i].get('model_agreement_count',np.nan) for i in ids],float)
    pos=np.array([int(i[1:]) for i in ids]);gen=[cs[i]['generator'] for i in ids]
    rk=lambda v:np.argsort(np.argsort(v,kind='stable'),kind='stable')
    sp=lambda x,y:float(np.corrcoef(rk(x),rk(y))[0,1]) if np.std(x)>0 and np.std(y)>0 else None
    per[t]=dict(n_options=len(ids),favourite=resp['answers']['overall']['choice'],fav_prob=float(ch.max()),confidence=resp['answers']['overall']['confidence'],
       spearman_choice_matches=sp(ch,m),spearman_choice_ensemble_rank=sp(ch,-er),spearman_choice_agreement=sp(ch,ag),spearman_choice_position=sp(ch,-pos),
       choice_by_generator={g:float(sum(c for c,gg in zip(ch,gen) if gg==g)) for g in sorted(set(gen))},fav_matches=int(m[np.argmax(ch)]),mean_matches=float(m.mean()),
       choice_weighted_matches=float((ch*m).sum()/ch.sum()))
    for i,c,mm in zip(ids,ch,m):jrows.append((t,c,mm))
def rep_top(t):
    p=L/f'jev_stability_{t}/stability_analysis.json'
    if not p.exists():return None
    s=J(p);return dict(agreement=s.get('top_choice_agreement_replicates'),spearman=s.get('mean_pairwise_spearman'),top3=s.get('mean_top3_overlap'),runs=[(x.get('run'),x.get('top_choice'),x.get('top_probability')) for x in s.get('runs',[])])
pooled=np.array(jrows);rkp=lambda v:np.argsort(np.argsort(v))
jev=dict(per_draw=per,replicates={t:rep_top(t) for t in [2342,2343]},
  pooled_spearman_choice_matches=float(np.corrcoef(rkp(pooled[:,1]),rkp(pooled[:,2]))[0,1]),pooled_n=len(jrows),
  favourite_mean_matches=float(np.mean([v['fav_matches'] for v in per.values()])),option_mean_matches=float(np.mean([v['mean_matches'] for v in per.values()])),
  untested=['candidate-order permutation','blinded IDs / generator labels'],note='Saved calls only (5 production calls; 10 replicates). No new historical calls.')
save('jev_audit.json',jev)
# ------------------------------------------------------------------ A20 code facts
py=sorted(str(p.relative_to(R)) for p in (R/'scripts').rglob('*.py'));mj=sorted(str(p.relative_to(R)) for p in (R/'scripts').rglob('*.mjs'))
lotto_specific=[p for p in py+mj if re.search(r'23[34]\d',p)]
hard=[]
for p in py+mj:
    s=(R/p).read_text(errors='ignore')
    if re.search(r'\b23[34]\d\b',s):hard.append(p)
crlf=[p for p in py+mj if b'\r\n' in (R/p).read_bytes()]
pkg=J(R/'package.json');lock=J(R/'package-lock.json')
code=dict(python_files=len(py),mjs_files=len(mj),draw_specific_named=lotto_specific,files_with_hard_coded_draw_ids=hard,crlf_files=crlf,
  production_entry_points=dict(V1='scripts/analyze.py (+ scripts/research/v1_prospective.py, lotto_prospective.py wrappers)',V1_jev='scripts/research/v1_prospective_jev.mjs / lotto_prospective_jev.mjs',P0='scripts/research/p0_apply.py + p0.py',freeze='scripts/research/v1_freeze.py, freeze_prospective.py'),
  dependencies=dict(package_json=pkg.get('dependencies'),lock_sdk=lock.get('packages',{}).get('node_modules/@typesafe-ai/sdk',{}).get('version')),
  python=sys.version.split()[0],numpy=np.__version__,
  ledger_append_only=all(git('show',f'{c}:results/lotto/prospective_ledger.jsonl') in (L/'prospective_ledger.jsonl').read_text() for c in git('log','--format=%h','--','results/lotto/prospective_ledger.jsonl').split()[:6]),
  v1_code_unchanged_since_snapshot=git('diff','--name-only','ba7c5a3','HEAD','--','scripts/analyze.py','scripts/jev.mjs','scripts/finalize.py','PROTOCOL.md')=='')
save('code_facts.json',code)
print(json.dumps(dict(data={k:data[k] for k in ['n','issues','weekday_counts','provenance']},pros=summary,cf={t:{k:v for k,v in x.items() if k not in ('pool',)} for t,x in cf.items()},src=cand_src,struct=sets,jev={k:jev[k] for k in ['pooled_spearman_choice_matches','favourite_mean_matches','option_mean_matches']},jevper=per,code={k:code[k] for k in ['draw_specific_named','crlf_files','dependencies','ledger_append_only','v1_code_unchanged_since_snapshot']}),indent=1,default=str)[:12000])
