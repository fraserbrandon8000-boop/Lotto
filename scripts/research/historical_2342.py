"""Lotto #2342 historical analyses (research only; Lotto data only; targets <= #2342 only).
Cluster/consecutive forensic, Top-N discovery audit, recurring core, fixed-seed follow-up.
Never computes the #2343 V1 candidate pool or the #2343 P0 pool. Outputs results/lotto/forensic_2342/."""
import sys,json,csv,math,itertools
from pathlib import Path
from collections import Counter
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'));sys.path.insert(0,str(R/'scripts/research'))
import analyze as a,p0,v1_history as V
D=R/'results/lotto/draw2342';O=R/'results/lotto/forensic_2342';O.mkdir(exist_ok=True)
J=lambda p:json.loads(Path(p).read_text())
def save(n,o):a.OUT=O;a.save(n,o)
WIN=[12,13,14,15,19,33];FAM=p0.FAM;CORE=[1,4,13,24,38,12,14];BOOT_SEED=20261003;MC_SEED=20261004
base=J(D/'draws.json');assert base[-1]['draw_id']==2341
records=base+[dict(draw_id=2342,date='2026-09-30',numbers=WIN,bonus=21,origin='official_user_supplied',source='Official result supplied by user in the #2342 forensic / #2343 task')]
assert all(records[i]['draw_id']+1==records[i+1]['draw_id'] for i in range(len(records)-1))
d=np.array([r['numbers'] for r in records])-1;A=a.indicator(d);idx={r['draw_id']:i for i,r in enumerate(records)}

def binom_two(k,n,p):
    pm=[math.comb(n,j)*p**j*(1-p)**(n-j) for j in range(n+1)];return float(min(1.,sum(q for q in pm if q<=pm[k]*(1+1e-9))))
def binom_ge(k,n,p):return float(sum(math.comb(n,j)*p**j*(1-p)**(n-j) for j in range(k,n+1)))

# ============================================================ historical V1 states (targets 2211..2342 only)
print('V1 reconstruction…',flush=True)
cache=V.walk_cache(d,records);val=V.validate(d,records,cache)
assert all(v['numbers_match'] and v['generators_match'] for v in val.values()),val
states=[V.state_at_cutoff(d,records,cache,c) for c in range(49,idx[2341]+1)]
assert states[-1]['target']==2342 and [c['numbers'] for c in states[-1]['candidates']]==[c['numbers'] for c in J(D/'candidates.json')],'cutoff-2341 reconstruction must equal the frozen #2342 pool'
val['2341']=dict(numbers_match=True,generators_match=True,qualifiers=states[-1]['qualifiers'])
OUTC={r['draw_id']:r['numbers'] for r in records}
for s in states:s['outcome']=OUTC[s['target']]
qualified=[s['target'] for s in states if s['qualifiers']]

# ============================================================ 5. cluster / consecutive forensic
def feats(X):
    X=np.sort(np.asarray(X,dtype=np.int16).reshape(-1,6),1);sp=np.diff(X,axis=1);run=np.ones(len(X),np.int16);cur=np.ones(len(X),np.int16)
    for j in range(5):cur=np.where(sp[:,j]==1,cur+1,1).astype(np.int16);run=np.maximum(run,cur)
    return dict(adj=(sp==1).sum(1),run=run,span4=np.min(X[:,3:]-X[:,:3],1),close=(sp<=2).sum(1))
MET=dict(run2=lambda f:f['run']>=2,run3=lambda f:f['run']>=3,run4=lambda f:f['run']>=4,adj2plus=lambda f:f['adj']>=2,dense4_window6=lambda f:f['span4']<=5)
def rates(X):
    f=feats(X);out={k:float(m(f).mean()) for k,m in MET.items()};out['mean_adjacent_pairs']=float(f['adj'].mean());out['n']=int(len(f['run']));return out
print('exact null over all C(38,6)…',flush=True)
ALL=np.fromiter(itertools.chain.from_iterable(itertools.combinations(range(1,39),6)),dtype=np.int16,count=math.comb(38,6)*6).reshape(-1,6)
NULL=rates(ALL);fa=feats(ALL);null_run_pmf={int(k):float(v) for k,v in zip(*np.unique(fa['run'],return_counts=True))};null_run_pmf={k:v/len(ALL) for k,v in null_run_pmf.items()}
f2342=feats([WIN]);draw2342=dict(numbers=WIN,adjacent_pairs=int(f2342['adj'][0]),longest_run=int(f2342['run'][0]),min_span_of_4=int(f2342['span4'][0]),
     null_p_longest_run_ge4=float((fa['run']>=4).mean()),null_p_adjacent_pairs_ge3=float((fa['adj']>=3).mean()))
del fa
def compare(X,independent=False):
    r=rates(X);out=dict(rates=r,ratio_to_null={k:(r[k]/NULL[k] if NULL[k]>0 else None) for k in MET})
    if independent:
        n=r['n'];ps={k:binom_two(int(round(r[k]*n)),n,NULL[k]) for k in MET};hp=a.holm(list(ps.values()))
        out['exact_binomial_two_sided_p']=ps;out['holm_p']=dict(zip(ps,map(float,hp)))
    return out
draws_all=d+1;hist_cmp=compare(draws_all,True);recent_cmp=compare(draws_all[-40:],True)
cand_all=[c['numbers'] for s in states for c in s['candidates']];by_gen={}
for s in states:
    for c in s['candidates']:by_gen.setdefault(c['generator'],[]).append(c['numbers'])
pool4096=V.POOL4096+1
# reconstructed V1 fallback chain (production seed, <=2 overlap) and the four real prospective V1 tickets
prev=None;chain=[]
for s in states:
    el=[c for c in s['candidates'] if prev is None or len(set(c['numbers'])&set(prev))<=2] or s['candidates'];el=sorted(el,key=lambda c:c['id'])
    c=el[int(np.random.default_rng(a.SEED).integers(len(el)))];chain.append(dict(target=s['target'],id=c['id'],numbers=c['numbers'],generator=c['generator'],n_eligible=len(el)));prev=c['numbers']
real_v1={2339:[1,4,13,14,24,38],2340:[5,11,16,24,27,34],2341:[1,4,13,14,24,38],2342:[5,11,16,24,27,34]}
HO=J(R/'results/lotto/p0_protocol/historical_origins.json')['rows']
p0_hist=[t for r in HO for t in r['byK']['15']['portfolio'][1:]]
sh=J(R/'results/lotto/p0_shadow_2341/p0_result.json');lv=J(D/'p0/p0_result.json')
p0_live=[t['numbers'] for t in sh['tickets'][1:]]+[t['numbers'] for t in lv['tickets'][1:]]
pools15=[r['order'][:15] for r in HO]+[sh['pool'],lv['pool']]
uni=np.vstack([np.array(list(itertools.combinations(sorted(p),6))) for p in pools15])
pool_adj=[sum(1 for x in p if x+1 in p) for p in pools15];rand_pool_adj=15*14/38
# F_structure: how it scores runs (cutoff 2341 = the #2342 V1 run)
ft41=a.model_features(a.indicator(d[:idx[2341]+1]));Fz=a.objectives(V.POOL4096,ft41)[5];fp=feats(pool4096)
Fby={int(k):dict(n=int((fp['run']==k).sum()),mean_F_z=float(Fz[fp['run']==k].mean()),mean_F_percentile=float(np.mean([np.mean(Fz<=v) for v in Fz[fp['run']==k]]))) for k in np.unique(fp['run'])}
win_struct=a.structure(np.array([WIN])-1)[0];zw=(win_struct-ft41[2])/ft41[3];Fwin=-np.mean(zw**2)
rawF=-np.mean(((a.structure(V.POOL4096)-ft41[2])/ft41[3])**2,axis=1)
F_cutoff2341=dict(feature_names=a.STRUCT,historical_means=ft41[2].tolist(),historical_sd=ft41[3].tolist(),actual_2342_feature_values=win_struct.tolist(),actual_2342_z=zw.tolist(),
    actual_2342_raw_F=float(Fwin),actual_2342_F_percentile_in_4096_pool=float(np.mean(rawF<=Fwin)),by_longest_run=Fby,
    top3_F_tickets=[(V.POOL4096[i]+1).tolist() for i in np.argsort(-Fz,kind='stable')[:3]],
    note='F_structure = -mean squared z-deviation of 10 structure features (incl. adjacent_pairs and close_spacings_le2) from the historical mean. A 4-run has adjacent_pairs=3 (mean ~0.8), so F ranks it near the bottom; it equally penalises any other atypical structure (sum, range, odd/low counts).')
# across all cutoffs: share of F_structure candidates (top-3 F) with a 3+ run, vs 4096-pool share
f_gen=feats(np.array(by_gen['F_structure']));pool_run3=float((fp['run']>=3).mean())
# G_ensemble weight on F at each cutoff
gF=[float(s['ensemble_weights'][5]) for s in states]
# P0: struct component in the frozen #2342 universe
U42=np.array(list(itertools.combinations(sorted(lv['pool']),6)));fu=feats(U42)
us=list(csv.DictReader(open(D/'p0/universe_scores.csv')));Tmap={tuple(int(x) for x in r['numbers'].split()):(float(r['T']),float(r['struct']),int(r['rank_by_T'])) for r in us}
Tv=np.array([Tmap[tuple(t)][0] for t in U42.tolist()]);Sv=np.array([Tmap[tuple(t)][1] for t in U42.tolist()]);Rv=np.array([Tmap[tuple(t)][2] for t in U42.tolist()])
p0_struct=dict(struct_weight=lv['frozen_weights']['struct'],B_weight=lv['frozen_weights']['B_recent'],D_weight=lv['frozen_weights']['D_trend'],
    mean_T_rank_by_longest_run={int(k):float(Rv[fu['run']==k].mean()) for k in np.unique(fu['run'])},n_by_longest_run={int(k):int((fu['run']==k).sum()) for k in np.unique(fu['run'])},
    corr_struct_component_vs_adjacent_pairs=float(np.corrcoef(Sv,fu['adj'])[0,1]),corr_T_vs_adjacent_pairs=float(np.corrcoef(Tv,fu['adj'])[0,1]),
    struct_share_of_T_variance=float(np.var(lv['frozen_weights']['struct']*Sv)/np.var(Tv)),
    note='Coverage term J-T is per-number mass (no structure). Overlap rules (<=2) count shared numbers only; no rule references adjacency.')
# causal check: do run-containing tickets score differently against real outcomes? (V1 candidates, all cutoffs)
mm=[];rr_=[]
for s in states:
    for c in s['candidates']:mm.append(len(set(c['numbers'])&set(s['outcome'])));rr_.append(int(feats([c['numbers']])['run'][0]>=3))
mm=np.array(mm);rr_=np.array(rr_);rng=np.random.default_rng(BOOT_SEED);obsdiff=mm[rr_==1].mean()-mm[rr_==0].mean()
perm=[(lambda z:mm[z==1].mean()-mm[z==0].mean())(rng.permutation(rr_)) for _ in range(5000)]
# draws: matches of a run-containing ticket ~ independent of structure under uniform draws -> check draw run rates (above)
cluster=dict(definitions=dict(run2='>=2 consecutive numbers',run3='>=3 consecutive',run4='>=4 consecutive',adj2plus='>=2 adjacent pairs',dense4_window6='4 numbers within any 6-number window (span<=5)'),
    exact_null_all_combinations=NULL,null_longest_run_pmf=null_run_pmf,draw_2342=draw2342,
    actual_draws_2161_2342=hist_cmp,actual_draws_last40=recent_cmp,
    v1_candidate_pools_2211_2342=compare(cand_all),v1_candidates_by_generator={g:compare(v) for g,v in by_gen.items()},v1_fixed_4096_pool=compare(pool4096),
    v1_reconstructed_fallback_chain=compare([c['numbers'] for c in chain]),v1_real_prospective_tickets_2339_2342=compare(list(real_v1.values())),
    p0_historical_challengers_K15_2231_2340=compare(p0_hist),p0_live_challengers_2341_2342=compare(p0_live),p0_pool_universes_all_6_subsets=compare(uni),
    p0_pool_adjacent_pairs=dict(mean=float(np.mean(pool_adj)),random_15_subset_expectation=rand_pool_adj,n_pools=len(pools15)),
    F_structure_cutoff_2341=F_cutoff2341,F_structure_candidates_run3_share=dict(F_candidates=float((f_gen['run']>=3).mean()),pool4096=pool_run3,n=int(len(f_gen['run']))),
    G_ensemble_weight_on_F=dict(mean=float(np.mean(gF)),at_cutoff_2341=gF[-1]),p0_struct_component=p0_struct,
    causal_check_v1_candidates=dict(mean_matches_with_run3=float(mm[rr_==1].mean()),mean_matches_without=float(mm[rr_==0].mean()),n_with=int(rr_.sum()),n_without=int((1-rr_).sum()),
        difference=float(obsdiff),permutation_p_two_sided=float(np.mean(np.abs(perm)>=abs(obsdiff)))))

# ============================================================ 7. Top-N historical discovery audit (causal P0 ordering)
print('P0 causal orderings through #2342…',flush=True)
Hh=p0.build_history(d,records);NS=[10,12,15,18,20,25];rows=[];mismatch=[]
hist_order={r['target']:r['order'] for r in HO}
for t in range(70,len(records)):
    tgt=records[t]['draw_id'];W=p0.weights_at(Hh,t);ft=p0.origin_features(d,t);M,EQ,order=p0.discovery(ft[0],W);win=np.nonzero(A[t])[0]+1
    if tgt in hist_order and hist_order[tgt]!=order:mismatch.append(tgt)
    rows.append(dict(target=tgt,order=order,weights={k:v['w'] for k,v in W.items()},capture={N:len(set(order[:N])&set(win.tolist())) for N in NS}))
assert not mismatch,mismatch
frozen_orders={2341:sh['pool_order_full'],2342:lv['pool_order_full']}
def topn_stats(rs,N,seed):
    c=np.array([r['capture'][N] for r in rs]);e0=6*N/38;pm=p0.hg_pmf(N);n=len(c);h=n//2
    return dict(n=n,mean=float(c.mean()),expected=e0,excess=float(c.mean()-e0),p_one_sided=p0.conv_p([pm]*n,int(c.sum())),bootstrap95_excess=p0.block_lb(c-e0,seed),
        half1_excess=float(c[:h].mean()-e0),half2_excess=float(c[h:].mean()-e0),
        p_ge={k:float(np.mean(c>=k)) for k in range(2,7)},p_ge_random={k:float(pm[k:].sum()) for k in range(2,7)})
full={N:topn_stats(rows,N,BOOT_SEED) for N in NS};conf={N:topn_stats(rows[-40:],N,BOOT_SEED+1) for N in NS}
for blk in (full,conf):
    hp=a.holm([blk[N]['p_one_sided'] for N in NS])
    for N,h_ in zip(NS,hp):blk[N]['holm_p']=float(h_);blk[N]['passes']=bool(h_<.05 and blk[N]['bootstrap95_excess'][0]>0 and blk[N]['half1_excess']>0 and blk[N]['half2_excess']>0)
topn=dict(targets=[rows[0]['target'],rows[-1]['target']],n_targets=len(rows),confirmation_targets=[rows[-40]['target'],rows[-1]['target']],
    ordering='causal P0 ordering (weights re-estimated from origins strictly before each target; identical to p0_protocol/historical_origins.json for 2231-2340, verified)',
    full_sample=full,confirmation=conf,
    target_2342=dict(causal_capture={N:rows[-1]['capture'][N] for N in NS},frozen_P0_capture={N:len(set(frozen_orders[2342][:N])&set(WIN)) for N in NS},
                     winner_ranks_frozen={w:frozen_orders[2342].index(w)+1 for w in WIN},winner_ranks_causal={w:rows[-1]['order'].index(w)+1 for w in WIN}),
    target_2341_frozen_capture={N:len(set(frozen_orders[2341][:N])&set(OUTC[2341])) for N in NS},
    any_N_passes=any(full[N]['passes'] for N in NS),
    note='Holm across the six N values. Pool size is not widened because of #2342; this audit decides nothing by itself.')
with open(O/'topN_per_target.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['target']+[f'top{N}' for N in NS])
    for r in rows:w.writerow([r['target']]+[r['capture'][N] for N in NS])

# ============================================================ 8. recurring core (01 04 13 24 38 + 12 14)
def ranks_of(s):
    out={}
    for j,f in enumerate(FAM):
        sc=s['family_scores'][j];o=np.argsort(-(sc+np.random.default_rng(a.SEED+s['target']).random(38)*1e-10))+1;out[f]=dict(order=o.tolist(),informative=bool(np.std(sc)>1e-12))
    g=s['g_proxy'];o=np.argsort(-(g+np.random.default_rng(a.SEED+s['target']).random(38)*1e-10))+1;out['G_marginal_proxy']=dict(order=o.tolist(),informative=bool(np.std(g)>1e-12))
    return out
fz={t:J(R/f'results/lotto/draw{t}/frozen.json') for t in (2340,2341,2342)}
prosp={2339:dict(final=real_v1[2339],final_id='C05',jev_pref_id='C02',previous=None),
       2340:dict(final=real_v1[2340],final_id=fz[2340]['candidate_id'],jev_pref_id=fz[2340]['jev_preferred_candidate'],previous=real_v1[2339]),
       2341:dict(final=real_v1[2341],final_id=fz[2341]['candidate_id'],jev_pref_id=fz[2341]['jev_preferred_candidate'],previous=real_v1[2340]),
       2342:dict(final=real_v1[2342],final_id=fz[2342]['candidate_id'],jev_pref_id=fz[2342]['jev_preferred_candidate'],previous=real_v1[2341])}
p0tick={2341:dict(kind='shadow',tickets=[t['numbers'] for t in sh['tickets'][1:]],pool=sh['pool']),2342:dict(kind='live',tickets=[t['numbers'] for t in lv['tickets'][1:]],pool=lv['pool'])}
st_by_t={s['target']:s for s in states};recent={}
for t,p in prosp.items():
    s=st_by_t[t];rr=ranks_of(s);cs=s['candidates'];el=[c for c in cs if p['previous'] is None or len(set(c['numbers'])&set(p['previous']))<=2]
    jp=[c['numbers'] for c in cs if c['id']==p['jev_pref_id']][0];per={}
    for x in CORE:
        per[x]=dict(ranks={f:rr[f]['order'].index(x)+1 for f in rr if rr[f]['informative']},in_candidates=[c['id']+':'+c['generator'] for c in cs if x in c['numbers']],
                    in_eligible=[c['id'] for c in el if x in c['numbers']],in_v1_final=x in p['final'],in_jev_preferred=x in jp,
                    in_p0_pool=(x in p0tick[t]['pool']) if t in p0tick else None,in_p0_tickets=(any(x in tk for tk in p0tick[t]['tickets'])) if t in p0tick else None,in_outcome=x in OUTC[t])
    recent[t]=dict(final_id=p['final_id'],jev_preferred_id=p['jev_pref_id'],n_eligible=len(el),core=per)
famtop={f:Counter() for f in FAM+['G_marginal_proxy']};inf=Counter();cand=Counter();gen_c={x:Counter() for x in CORE}
for s in states:
    rr=ranks_of(s)
    for f in rr:
        if rr[f]['informative']:
            inf[f]+=1
            for x in rr[f]['order'][:12]:famtop[f][x]+=1
    for c in s['candidates']:
        for x in c['numbers']:
            cand[x]+=1
            if x in CORE:gen_c[x][c['generator']]+=1
p0pool=Counter(x for r in rows for x in r['order'][:15]);nT=len(states)
corr={}
for i,j in itertools.combinations(range(5),2):
    v=[np.corrcoef(s['family_scores'][i],s['family_scores'][j])[0,1] for s in states if np.std(s['family_scores'][i])>1e-12 and np.std(s['family_scores'][j])>1e-12]
    corr[f'{FAM[i]}~{FAM[j]}']=dict(mean=float(np.mean(v)) if v else None,n=len(v))
reps=Counter(tuple(c['numbers']) for s in states for c in s['candidates'])
persist=[len({tuple(c['numbers']) for c in s0['candidates']}&{tuple(c['numbers']) for c in s1['candidates']}) for s0,s1 in zip(states,states[1:])]
ns=list(csv.DictReader(open(D/'number_statistics.csv')));fq={int(r['number']):float(r['frequency_holm_p']) for r in ns}
lw=[r['weights'] for r in rows]
attrib={}
for x in CORE:
    t2342=recent[2342]['core'][x]
    attrib[x]=dict(
        independent_evidence=dict(frequency_holm_p_at_cutoff_2341=fq[x],significant=fq[x]<.05),
        correlated_models=dict(top12_rate={f:famtop[f][x]/inf[f] for f in famtop if inf[f]},chance_top12=12/38,ranks_cutoff_2341=t2342['ranks']),
        p0_pool_membership_rate=p0pool[x]/len(rows),p0_pool_chance=15/38,
        construction=dict(mean_V1_candidates_containing=cand[x]/nT,uniform_expectation=20*6/38,generators=dict(gen_c[x])),
        random_filler_H_candidates=gen_c[x].get('H_random',0),
        v1_final_2339_2342=[t for t in prosp if x in prosp[t]['final']],jev_preferred_2339_2342=[t for t in prosp if recent[t]['core'][x]['in_jev_preferred']],
        p0_tickets=[t for t in p0tick if recent[t]['core'][x]['in_p0_tickets']])
core=dict(core=CORE,recent_runs=recent,driver_attribution=attrib,family_score_correlations=corr,
    p0_weight_history=dict(families_with_positive_weight_share={f:float(np.mean([w[f]>0 for w in lw])) for f in lw[0]}),
    construction=dict(fixed_pool='SEED+999: identical 4,096-combination pool at every cutoff',exact_ticket_01_04_13_14_24_38_in_pools=reps.get((1,4,13,14,24,38),0),
        exact_ticket_05_11_16_24_27_34_in_pools=reps.get((5,11,16,24,27,34),0),n_cutoffs=nT,mean_identical_candidates_consecutive_cutoffs=float(np.mean(persist)),
        most_repeated=[dict(numbers=list(k),pools=v) for k,v in reps.most_common(6)]),
    fixed_seed_index_map={n:int(np.random.default_rng(a.SEED).integers(n)) for n in range(10,21)},
    reading=('No core number is significant on frequency after Holm. Recurrence comes from (i) B_recent and D_trend being positively correlated and both rewarding recent hits, '
             '(ii) P0 using only B_recent and D_trend (plus a tiny struct weight), (iii) the fixed 4,096-combination candidate pool re-offering the same top B_recent ticket, '
             '(iv) the fixed fallback seed picking the same list position for a given eligible count, and (v) the <=2 overlap rule forcing alternation between two tickets.'))

# ============================================================ 9. fixed-seed follow-up (research only)
T=[s['target'] for s in states];C=[s['candidates'] for s in states];OUT=[s['outcome'] for s in states]
def run_chain(pick):
    prev=None;sel=[]
    for i,cs in enumerate(C):
        el=[c for c in cs if prev is None or len(set(c['numbers'])&set(prev))<=2] or cs;el=sorted(el,key=lambda c:c['id']);c=el[pick(i,len(el))];sel.append(c);prev=c['numbers']
    return sel
def metrics(sel):
    ids=[c['id'] for c in sel];nums=[c['numbers'] for c in sel];m=[len(set(n)&set(o)) for n,o in zip(nums,OUT)];numc=Counter(x for n in nums for x in n)
    return dict(same_id_consecutive=float(np.mean([x==y for x,y in zip(ids,ids[1:])])),top_id_share=Counter(ids).most_common(1)[0][1]/len(ids),distinct_ids=len(set(ids)),
        exact_ticket_repeat_lag2=float(np.mean([tuple(x)==tuple(y) for x,y in zip(nums,nums[2:])])),mean_consecutive_overlap=float(np.mean([len(set(x)&set(y)) for x,y in zip(nums,nums[1:])])),
        core_selection_rate=float(np.mean([len(set(n)&set(CORE)) for n in nums])/6),max_number_selection_rate=max(numc.values())/len(sel),
        mean_matches=float(np.mean(m)),total_matches=int(sum(m)),ge3=int(sum(v>=3 for v in m)),last40_mean=float(np.mean(m[-40:])))
KEYS=['same_id_consecutive','top_id_share','distinct_ids','exact_ticket_repeat_lag2','mean_consecutive_overlap','core_selection_rate','max_number_selection_rate','mean_matches','total_matches','ge3','last40_mean']
A_=metrics(run_chain(lambda i,n:int(np.random.default_rng(a.SEED).integers(n))))
B_=metrics(run_chain(lambda i,n:int(np.random.default_rng(a.SEED+T[i]).integers(n))))
D_=metrics(run_chain(lambda i,n:T[i]%n))
mc=np.random.default_rng(MC_SEED);Cs=[metrics(run_chain(lambda i,n,g=np.random.default_rng(mc.integers(2**63)):int(g.integers(n)))) for _ in range(2000)]
Fs=[metrics(run_chain(lambda i,n,s=s:int(np.random.default_rng(s).integers(n)))) for s in range(1,501)]
def dist(L,k):v=np.array([m[k] for m in L]);return dict(mean=float(v.mean()),p025=float(np.quantile(v,.025)),p975=float(np.quantile(v,.975)))
def pctl(L,k,x):v=np.array([m[k] for m in L]);return float(np.mean(v>=x))
mp=a.BASE;n=len(T)
seed=dict(targets=[T[0],T[-1]],n_targets=n,designs=dict(A_fixed_production_seed=A_,B_per_draw_seed=B_,D_rotating_index=D_),
    C_uniform_selection_2000_streams={k:dist(Cs,k) for k in KEYS},fixed_seed_family_500_seeds={k:dist(Fs,k) for k in KEYS},
    upper_tail_share_in_uniform={dn:{k:pctl(Cs,k,m[k]) for k in KEYS} for dn,m in dict(A=A_,B=B_,D=D_).items()},
    null_reference=dict(mean_matches=mp,total=mp*n,p_total_ge_A=None),
    definitions=dict(A='fresh default_rng(20260919).integers(n) each run (production)',B='default_rng(20260919 + target_id).integers(n)',
        C='independent uniform choice among eligible candidates (2000 Monte Carlo streams, seed 20261004)',D='index = target_id mod n'),
    qualified_targets_flagged=qualified,note='Research only. All designs keep the <=2 overlap rule and the same reconstructed pools. No seed is promoted.')
# exact null p for production total matches (sum of independent hypergeometric matches)
hg=np.array([math.comb(6,k)*math.comb(32,6-k)/math.comb(38,6) for k in range(7)])
seed['null_reference']['p_total_ge']={dn:p0.conv_p([hg]*n,m['total_matches']) for dn,m in dict(A=A_,B=B_,D=D_).items()}
seed['null_reference']['p_ge3_count_ge']={dn:binom_ge(m['ge3'],n,float(hg[3:].sum())) for dn,m in dict(A=A_,B=B_,D=D_).items()}

save('historical_2342.json',dict(validation=val,qualified_targets=qualified,cluster_consecutive=cluster,topN_audit=topn,recurring_core=core,fixed_seed=seed))
print(json.dumps(dict(cluster_draws=hist_cmp,F=F_cutoff2341['by_longest_run'],topN={N:(full[N]['mean'],full[N]['expected'],full[N]['holm_p']) for N in NS},
    seedA=A_,seedB=B_,seedD=D_),indent=1,default=float))
