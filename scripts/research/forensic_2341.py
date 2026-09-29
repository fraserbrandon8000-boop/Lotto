"""Lotto #2341 forensic (research only). Reads frozen artifacts; never modifies them.
Outputs go to results/lotto/forensic_2341/."""
import sys,json,csv,math,itertools
from pathlib import Path
from collections import Counter
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'));sys.path.insert(0,str(R/'scripts/research'))
import analyze as a
import v1_history as H
O=R/'results/lotto/forensic_2341';D=R/'results/lotto/draw2341'
OUTCOME=[1,4,6,22,33,38];BONUS=34;SELECTED=[1,4,13,14,24,38]
WIN=OUTCOME;LOSERS=[13,14,24];CORE=[1,4,13,24,38];NS=[5,7,10,12,15,20,25]
FAM=['A_long','B_recent','C_gap','D_trend','E_pairs']
def J(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def save(name,obj):a.OUT=O;a.save(name,obj)
PMF=a.PMF

# ------------------------------------------------------------------ step 3: score the pool
cands=J(D/'candidates.json');resp=J(D/'jev_response.json');ans=resp['answers'];fz=J(D/'frozen.json')
probs=ans['overall']['probabilities'];order=sorted(probs,key=lambda k:-probs[k])
def jrank(cid):
    if cid not in probs:return None
    p=probs[cid];return dict(best=1+sum(v>p for v in probs.values()),worst=sum(v>=p for v in probs.values()))
pool=[]
for c in cands:
    m=sorted(set(c['numbers'])&set(OUTCOME));el=len(c['overlap_previous_primary'])<=2
    row=dict(id=c['id'],numbers=c['numbers'],generator=c['generator'],eligible=el,matches=len(m),matched=m,
             jev_choice_probability=probs.get(c['id']),jev_rank=jrank(c['id']),
             sensitivity=dict(top_quartile_fraction=c['sensitivity_top_quartile_fraction'],mean_rank=c['sensitivity_mean_rank'],generator_rank_min=c['generator_sensitivity_rank_min'],generator_rank_max=c['generator_sensitivity_rank_max']),
             model_evidence=dict(model_ranks=c['model_ranks'],contributing_models=c['contributing_models'],validated_models=c['validated_models'],model_agreement_count=c['model_agreement_count'],ensemble_rank=c['ensemble_rank']),
             jev_scores={k:ans[f"{c['id']}_{k}"].get('score',ans[f"{c['id']}_{k}"].get('noul')) for k in ['robustness','consensus','quality','overfit','stable','stronger','dependent']} if el else None)
    pool.append(row)
dist=Counter(r['matches'] for r in pool);best=max(r['matches'] for r in pool)
elig=[r for r in pool if r['eligible']]
jp=[r['jev_choice_probability'] for r in elig];mm=[r['matches'] for r in elig]
def spearman(x,y):
    rx=np.argsort(np.argsort(x));ry=np.argsort(np.argsort(y));return float(np.corrcoef(rx,ry)[0,1])
pool_summary=dict(outcome=OUTCOME,bonus=BONUS,n_candidates=len(pool),n_eligible=len(elig),
    match_distribution={k:dist.get(k,0) for k in range(7)},eligible_match_distribution={k:Counter(mm).get(k,0) for k in range(7)},
    best_matches=best,best_candidates=[r['id'] for r in pool if r['matches']==best],
    v1_selected=dict(id=fz['candidate_id'],numbers=fz['numbers'],matches=len(set(fz['numbers'])&set(OUTCOME))),
    jev_preferred=dict(id=ans['overall']['choice'],probability=probs[ans['overall']['choice']],matches=[r['matches'] for r in pool if r['id']==ans['overall']['choice']][0]),
    any_candidate_above_3=best>3,
    random_reference=dict(p_ticket_ge3=float(PMF[3:].sum()),expected_candidates_ge3_of_20=float(20*PMF[3:].sum()),p_at_least_one_ge3_of_20_independent=float(1-(1-PMF[3:].sum())**20),p_at_least_one_ge4_of_20_independent=float(1-(1-PMF[4:].sum())**20)),
    jev_choice_vs_matches_spearman_eligible=spearman(jp,mm),
    note='Descriptive only. No candidate is promoted retrospectively.')
save('pool_scores.json',dict(summary=pool_summary,candidates=pool))
with open(O/'pool_scores.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['id','numbers','generator','eligible','matches','matched','jev_choice','jev_rank_best','sens_topq','ensemble_rank','agreement'])
    for r in pool:w.writerow([r['id'],' '.join(f'{x:02}' for x in r['numbers']),r['generator'],r['eligible'],r['matches'],' '.join(map(str,r['matched'])),r['jev_choice_probability'],(r['jev_rank'] or {}).get('best'),r['sensitivity']['top_quartile_fraction'],r['model_evidence']['ensemble_rank'],r['model_evidence']['model_agreement_count']])

# ------------------------------------------------------------------ step 4: exact pre-draw number evidence
rk=J(D/'refreshed_rankings.json');stats={int(r['number']):r for r in csv.DictReader(open(D/'number_statistics.csv'))}
records,d=H.load(D/'draws.json');assert records[-1]['draw_id']==2340
ft=a.model_features(a.indicator(d));mat=ft[1]
hscore=np.random.default_rng(a.SEED+2341*3037).random(38)  # V1 walk H ranking definition for target 2341
rankings={}
for name in FAM+['G_marginal_proxy']:
    s=np.array(rk[name]['scores']);rankings[name]=dict(scores=s,order=list(rk[name]['order']),informative=rk[name]['informative'])
rankings['H_random']=dict(scores=hscore,order=(np.argsort(-hscore)+1).tolist(),informative=True)
assert np.allclose(rankings['A_long']['scores'],ft[0][0]) and np.allclose(rankings['E_pairs']['scores'],ft[0][4])
def tie_interval(s,i):
    v=s[i-1];better=int(np.sum(s>v+1e-12));equal=int(np.sum(np.abs(s-v)<=1e-12));return [better+1,better+equal]
def topn(name,N):
    s=rankings[name]['scores'];o=rankings[name]['order'][:N];pt=len(set(o)&set(WIN))
    v=np.sort(s)[::-1][N-1];inside=[i for i in range(1,39) if s[i-1]>v+1e-12];tied=[i for i in range(1,39) if abs(s[i-1]-v)<=1e-12]
    slots=N-len(inside);dw=len(set(inside)&set(WIN));tw=len(set(tied)&set(WIN));tn=len(tied)-tw
    return dict(point=pt,min=dw+max(0,slots-tn),max=dw+min(slots,tw),random_expected=6*N/38,
                p_ge_point=float(sum(math.comb(6,k)*math.comb(32,N-k) for k in range(pt,min(6,N)+1))/math.comb(38,N)))
numbers={}
for x in WIN+LOSERS:
    e=dict(role='winner' if x in WIN else 'selected_loser',in_v1_ticket=x in SELECTED,models={})
    for name,rr in rankings.items():
        s=rr['scores'];e['models'][name]=dict(score=float(s[x-1]),rank=rr['order'].index(x)+1,tie_interval=tie_interval(s,x),informative=rr['informative'])
    e['models']['F_structure']='not applicable: V1 F is a whole-ticket structure objective with no number-level ranking'
    st=stats[x];e['features']={k:st[k] for k in ['frequency','appearance_rate','ew_rate','last_30_count','last_20_count','last_10_count','current_gap','current_gap_percentile','trend_20_vs_previous40','frequency_holm_p']}
    e['features']['retained_pair_partners']=[int(j+1) for j in np.nonzero(mat[x-1])[0]]
    e['family_top12_support']=[f for f in FAM if rankings[f]['informative'] and rankings[f]['order'].index(x)<12]
    numbers[x]=e
coverage={name:{N:topn(name,N) for N in NS} for name in rankings if rankings[name]['informative']}
flat=[n for n in rankings if not rankings[n]['informative']]
save('number_evidence.json',dict(cutoff=2340,target=2341,outcome=OUTCOME,numbers=numbers,flat_or_non_informative=flat+['F_structure (no number-level ranking)'],retained_pairs_at_cutoff=int(ft[-1]),coverage=coverage,
     note='Scores/ranks are the exact frozen pre-draw values (refreshed_rankings.json); H uses the V1 walk H definition for target 2341. Tie intervals give the rank range among exactly equal scores.'))
with open(O/'coverage_2341.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['model']+[f'top{N}' for N in NS])
    for name,cv in coverage.items():w.writerow([name]+[f"{c['point']} [{c['min']}-{c['max']}] (exp {c['random_expected']:.2f})" for c in cv.values()])

# ------------------------------------------------------------------ historical states (validated reconstruction)
cache=H.walk_cache(d,records);val=H.validate(d,records,cache)
assert all(v['numbers_match'] and v['generators_match'] for v in val.values()),val
states=[H.state_at_cutoff(d,records,cache,c) for c in range(49,len(records))]   # targets 2211..2341
out_by_target={r['draw_id']:r['numbers'] for r in records};out_by_target[2341]=OUTCOME
for s in states:s['outcome']=out_by_target.get(s['target'])
qualified=[s['target'] for s in states if s['qualifiers']];approx_gate_cutoffs=list(H.APPROX)
save('v1_history_states.json',dict(validation=val,approx_gate_cutoffs=approx_gate_cutoffs,targets=[s['target'] for s in states],qualified_targets=qualified,
     states=[dict(target=s['target'],cutoff=s['cutoff'],candidates=s['candidates'],qualifiers=s['qualifiers'],min_conf_holm_p=s['min_conf_holm_p'],outcome=s['outcome']) for s in states]))

# ------------------------------------------------------------------ step 5: recurring core
def ranks_of(s):
    out={}
    for j,f in enumerate(FAM):
        sc=s['family_scores'][j];inf=bool(np.std(sc)>1e-12);o=np.argsort(-(sc+np.random.default_rng(a.SEED+s['target']).random(38)*1e-10))+1
        out[f]=dict(order=o.tolist(),informative=inf)
    g=s['g_proxy'];o=np.argsort(-(g+np.random.default_rng(a.SEED+s['target']).random(38)*1e-10))+1;out['G_marginal_proxy']=dict(order=o.tolist(),informative=bool(np.std(g)>1e-12))
    return out
prosp={2339:dict(final=[1,4,13,14,24,38],final_id='C05',secondary=[2,6,8,12,18,25],jev_pref_id='C02',previous=None,outcome=[1,4,6,13,23,28]),
       2340:dict(final=[5,11,16,24,27,34],final_id='C07',jev_pref_id=J(R/'results/lotto/draw2340/frozen.json')['jev_preferred_candidate'],previous=[1,4,13,14,24,38],outcome=[6,8,12,14,18,31]),
       2341:dict(final=SELECTED,final_id='C04',jev_pref_id='C04',previous=[5,11,16,24,27,34],outcome=OUTCOME)}
st_by_t={s['target']:s for s in states}
recent_runs={}
for t,p in prosp.items():
    s=st_by_t[t];rr=ranks_of(s);cs=s['candidates'];el=[c for c in cs if p['previous'] is None or len(set(c['numbers'])&set(p['previous']))<=2]
    jp=[c['numbers'] for c in cs if c['id']==p['jev_pref_id']][0]
    per={}
    for x in CORE:
        per[x]=dict(ranks={f:rr[f]['order'].index(x)+1 for f in rr if rr[f]['informative']},
                    top={N:[f for f in rr if rr[f]['informative'] and rr[f]['order'].index(x)<N] for N in [5,10,15,20]},
                    in_candidates=[c['id'] for c in cs if x in c['numbers']],in_eligible=[c['id'] for c in el if x in c['numbers']],
                    in_v1_final=x in p['final'],in_jev_preferred=x in jp,in_outcome=x in p['outcome'])
    recent_runs[t]=dict(n_eligible=len(el),eligible_ids=[c['id'] for c in el],final_id=p['final_id'],jev_preferred_id=p['jev_pref_id'],jev_preferred_numbers=jp,
                        generators={c['id']:c['generator'] for c in cs},core=per,
                        e_pairs_informative=rr['E_pairs']['informative'])
# long-run frequencies across all reconstructed cutoffs
lr={x:Counter() for x in CORE};allnum=Counter();nT=len(states)
famtop={f:{N:Counter() for N in [5,10,15,20]} for f in FAM+['G_marginal_proxy']};infcount=Counter()
cand_contain=Counter();gen_contain={x:Counter() for x in CORE}
for s in states:
    rr=ranks_of(s)
    for f in rr:
        if not rr[f]['informative']:continue
        infcount[f]+=1
        for N in [5,10,15,20]:
            for x in rr[f]['order'][:N]:famtop[f][N][x]+=1
    for c in s['candidates']:
        for x in c['numbers']:
            cand_contain[x]+=1
            if x in CORE:gen_contain[x][c['generator']]+=1
long_run={}
for x in CORE:
    long_run[x]=dict(top_rate={f:{N:famtop[f][N][x]/infcount[f] for N in [5,10,15,20]} for f in famtop if infcount[f]},
                     mean_candidates_containing=cand_contain[x]/nT,candidate_generators=dict(gen_contain[x]))
cand_rank=sorted(range(1,39),key=lambda x:-cand_contain[x])
# family independence: correlation of number scores across all cutoffs
corr={}
for i,j in itertools.combinations(range(5),2):
    v=[np.corrcoef(s['family_scores'][i],s['family_scores'][j])[0,1] for s in states if np.std(s['family_scores'][i])>1e-12 and np.std(s['family_scores'][j])>1e-12]
    corr[f'{FAM[i]}~{FAM[j]}']=dict(mean=float(np.mean(v)) if v else None,n=len(v))
# construction mechanics: fixed 4096 pool
pool4096=H.POOL4096+1
core4=set([1,4,13,24]);k3=np.array([len(set(t)&core4)>=3 for t in pool4096]).mean()
rng=np.random.default_rng(1);base=[np.mean([len(set(t)&set(rng.choice(38,4,replace=False)+1))>=3 for t in pool4096]) for _ in range(200)]
persist=[]
for s0,s1 in zip(states,states[1:]):
    a0={tuple(c['numbers']) for c in s0['candidates']};a1={tuple(c['numbers']) for c in s1['candidates']};persist.append(len(a0&a1))
exact_repeat_tickets=Counter(tuple(c['numbers']) for s in states for c in s['candidates'])
# fixed-seed index map
idxmap={n:int(np.random.default_rng(a.SEED).integers(n)) for n in range(1,21)}
save('recurring_core.json',dict(core=CORE,recent_runs=recent_runs,long_run=long_run,
    candidate_membership_rank_all_numbers=[dict(number=x,mean_candidates_containing=cand_contain[x]/nT) for x in cand_rank],
    family_score_correlations=corr,
    construction=dict(fixed_pool_seed='SEED+999 (identical 4,096-combination pool at every cutoff)',
                      share_of_pool_with_3plus_of_1_4_13_24=float(k3),same_for_random_4sets_mean=float(np.mean(base)),
                      mean_identical_candidate_tickets_between_consecutive_cutoffs=float(np.mean(persist)),
                      tickets_reappearing_in_10plus_pools=sum(v>=10 for v in exact_repeat_tickets.values()),
                      most_repeated_tickets=[dict(numbers=list(k),pools=v) for k,v in exact_repeat_tickets.most_common(8)]),
    fixed_seed_index_map=dict(description='V1 fallback: index = default_rng(20260919).integers(n) with a FRESH generator each run, so the chosen position depends only on the number of eligible candidates n',map=idxmap)))

# ------------------------------------------------------------------ step 6: fixed-seed sensitivity (research only)
T=[s['target'] for s in states];C=[s['candidates'] for s in states];OUT=[s['outcome'] for s in states]
def chain(pick,overlap=True):
    prev=None;sel=[]
    for i,cs in enumerate(C):
        el=[c for c in cs if prev is None or not overlap or len(set(c['numbers'])&set(prev))<=2] or cs
        el=sorted(el,key=lambda c:c['id']);c=el[pick(i,len(el))];sel.append(c);prev=c['numbers']
    return sel
def metrics(sel):
    ids=[c['id'] for c in sel];nums=[c['numbers'] for c in sel];gens=Counter(c['generator'] for c in sel)
    m=[len(set(n)&set(o)) for n,o in zip(nums,OUT)];ov=[len(set(x)&set(y)) for x,y in zip(nums,nums[1:])]
    lag2=[tuple(x)==tuple(y) for x,y in zip(nums,nums[2:])];numc=Counter(x for n in nums for x in n)
    return dict(same_id_consecutive=float(np.mean([x==y for x,y in zip(ids,ids[1:])])),top_id_share=Counter(ids).most_common(1)[0][1]/len(ids),
                distinct_ids=len(set(ids)),generator_shares={g:v/len(sel) for g,v in gens.items()},mean_consecutive_overlap=float(np.mean(ov)),
                exact_ticket_repeat_lag2=float(np.mean(lag2)),core_numbers_selection_rate={x:numc[x]/len(sel) for x in CORE},
                max_number_selection_rate=max(numc.values())/len(sel),mean_matches=float(np.mean(m)),sd_matches=float(np.std(m,ddof=1)),ge3=int(sum(v>=3 for v in m)))
SEEDS=[a.SEED]+list(range(1,1001))
fixed={s:metrics(chain(lambda i,n,s=s:int(np.random.default_rng(s).integers(n)))) for s in SEEDS}
perdraw={s:metrics(chain(lambda i,n,s=s:int(np.random.default_rng(s+T[i]).integers(n)))) for s in SEEDS}
fixed_noov={s:metrics(chain(lambda i,n,s=s:int(np.random.default_rng(s).integers(n)),overlap=False)) for s in SEEDS[:201]}
def dist_of(dd,key,sub=None):
    v=np.array([m[key] if sub is None else m[key].get(sub,0) for m in dd.values()]);return dict(mean=float(v.mean()),p05=float(np.quantile(v,.05)),p95=float(np.quantile(v,.95)))
def pct(dd,key,val):
    v=np.array([m[key] for k,m in dd.items() if k!=a.SEED]);return float(np.mean(v>=val))
keys=['same_id_consecutive','top_id_share','distinct_ids','mean_consecutive_overlap','exact_ticket_repeat_lag2','max_number_selection_rate','mean_matches','sd_matches','ge3']
seed_study=dict(targets=[T[0],T[-1]],n_targets=len(T),qualified_targets_flagged=qualified,
    production_seed=fixed[a.SEED],
    fixed_seed_designs={k:dist_of(fixed,k) for k in keys},per_draw_seed_designs={k:dist_of(perdraw,k) for k in keys},
    fixed_seed_no_overlap_rule={k:dist_of(fixed_noov,k) for k in keys},
    production_percentile_among_1000_fixed_seeds={k:pct(fixed,k,fixed[a.SEED][k]) for k in keys},
    b_recent_share=dict(production=fixed[a.SEED]['generator_shares'].get('B_recent',0),fixed_mean=dist_of(fixed,'generator_shares','B_recent'),per_draw_mean=dist_of(perdraw,'generator_shares','B_recent'),uniform_reference=3/20),
    note='Research only. Production seed unchanged. Fixed-seed designs re-create a fresh generator each run (as V1 does); per-draw designs use seed + target draw_id. Outcomes: reconstructed history through #2340 plus the user-supplied #2341 result.')
save('seed_sensitivity.json',seed_study)

# ------------------------------------------------------------------ step 7: three-match forensic
p3=math.comb(6,3)*math.comb(32,3)/math.comb(38,6);pge3=float(PMF[3:].sum())
def conv_p(obs):
    pm=np.array([1.]);
    for _ in obs:pm=np.convolve(pm,PMF)
    return float(pm[sum(obs):].sum())
def cp(k,n,alpha=.05):
    from math import comb
    def cdf(p,k):return sum(comb(n,j)*p**j*(1-p)**(n-j) for j in range(k+1))
    lo=0. if k==0 else _bisect(lambda p:1-cdf(p,k-1)-alpha/2);hi=1. if k==n else _bisect(lambda p:cdf(p,k)-alpha/2,dec=True)
    return [lo,hi]
def _bisect(f,dec=False):
    lo,hi=0.,1.
    for _ in range(80):
        mid=(lo+hi)/2;v=f(mid)
        if (v>0)!=dec:hi=mid
        else:lo=mid
    return (lo+hi)/2
primary=[3,0,3];withsec=[3,1,0,3]
def binom_ge(k,n,p):return float(sum(math.comb(n,j)*p**j*(1-p)**(n-j) for j in range(k,n+1)))
three=dict(p_exactly_3=p3,p_at_least_3=pge3,p_at_least_4=float(PMF[4:].sum()),expected_matches=36/38,sd_matches=float(math.sqrt(6*(6/38)*(32/38)*(32/37))),
    prospective_v1=dict(primary_series={'2339':3,'2340':0,'2341':3},secondary_2339=1,
        primary=dict(n=3,total=6,mean=2.0,p_total_ge_observed=conv_p(primary),ge3_events=2,p_ge3_events_ge2=binom_ge(2,3,pge3),ge3_rate_clopper_pearson95=cp(2,3)),
        including_2339_secondary=dict(n=4,total=7,mean=1.75,p_total_ge_observed=conv_p(withsec),ge3_events=2,p_ge3_events_ge2=binom_ge(2,4,pge3),ge3_rate_clopper_pearson95=cp(2,4))),
    caveats=['n = 3 prospective primary tickets; any interval is extremely wide.',
             'The #2339 and #2341 primary tickets are the SAME combination (01 04 13 14 24 38), chosen both times by the fixed-seed fallback at a B_recent slot; the two 3/6 results are one ticket hitting twice, not two independent method successes.',
             'Attention is post hoc (the question is asked because 3/6 occurred) and the ledger tracks many tickets per draw (20 candidates, Jev preference, challengers), which inflates the chance that some tracked ticket looks unusual.',
             'No multiplicity correction is applied to these p-values; they are descriptive.'])
save('three_match.json',three)
print(json.dumps(dict(pool=pool_summary['match_distribution'],best=pool_summary['best_candidates'],validation=val,qualified=qualified,idxmap=idxmap,
     prod=fixed[a.SEED],three=three['prospective_v1']),indent=1,default=str))
