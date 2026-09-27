"""Deterministic Lotto audit statistics, causal models, null controls and candidates."""
import json, math, csv, hashlib, itertools, argparse
from pathlib import Path
from functools import lru_cache
import numpy as np

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'results'; SEED=20260919; N=38; K=6; BASE=36/38
PAIRS=np.array(list(itertools.combinations(range(N),2))); PI,PJ=PAIRS.T
TRIPLES=list(itertools.combinations(range(N),3))
PAIR_LOOKUP=np.full((N,N),-1,int)
for z,(a,b) in enumerate(PAIRS): PAIR_LOOKUP[a,b]=PAIR_LOOKUP[b,a]=z
PP=30/(38*37)
PMF=np.array([math.comb(6,k)*math.comb(32,6-k)/math.comb(38,6) for k in range(7)])
NAMES=['A_long','B_recent','C_gap','D_trend','E_pairs','F_structure','G_ensemble','H_random']
def clean(o):
    if isinstance(o,dict): return {str(k):clean(v) for k,v in o.items()}
    if isinstance(o,(list,tuple)): return [clean(v) for v in o]
    if isinstance(o,np.ndarray): return clean(o.tolist())
    if isinstance(o,np.integer): return int(o)
    if isinstance(o,(np.floating,float)): return float(o) if math.isfinite(o) else None
    if isinstance(o,np.bool_): return bool(o)
    return o
def save(name,obj): (OUT/name).write_text(json.dumps(clean(obj),indent=2,allow_nan=False),encoding='utf-8')
def csvsave(name,rows):
    with (OUT/name).open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0])); writer.writeheader()
        writer.writerows([{k:json.dumps(clean(v)) if isinstance(v,(list,dict,np.ndarray)) else clean(v) for k,v in r.items()} for r in rows])
def holm(p):
    p=np.asarray(p); order=np.argsort(p); out=np.empty(len(p)); out[order]=np.minimum(1,np.maximum.accumulate(p[order]*(len(p)-np.arange(len(p))))); return out
def bh(p):
    p=np.asarray(p); order=np.argsort(p); out=np.empty(len(p)); out[order]=np.minimum(1,np.minimum.accumulate((p[order]*len(p)/(np.arange(len(p))+1))[::-1])[::-1]); return out
@lru_cache(None)
def binom_probs(n,p):
    return np.array([math.exp(math.lgamma(n+1)-math.lgamma(k+1)-math.lgamma(n-k+1)+k*math.log(p)+(n-k)*math.log1p(-p)) for k in range(n+1)])
def binom_p(n,p,k,two=False):
    mass=binom_probs(int(n),float(p)); return min(1,float(mass[mass<=mass[int(k)]+1e-15].sum() if two else mass[int(k):].sum()))
def fisher_upper(n,a,b,c):
    # Conditional count in b-success positions when sampling a positions.
    return min(1,sum(math.comb(b,k)*math.comb(n-b,a-k)/math.comb(n,a) for k in range(max(c,0,a-(n-b)),min(a,b)+1))) if a else 1.
@lru_cache(None)
def null_sum(n):
    p=np.array([1.])
    for _ in range(n): p=np.convolve(p,PMF)
    return p
def null_p(matches): return float(null_sum(len(matches))[int(sum(matches)):].sum())
def sample(rng,n): return np.sort(np.argpartition(rng.random((n,N)),K-1,axis=1)[:,:K],axis=1)
def indicator(draws):
    a=np.zeros((len(draws),N),dtype=np.int64); a[np.arange(len(draws))[:,None],draws]=1; return a
def zscore(v): return (v-np.mean(v))/(np.std(v)+1e-12)
def gaps(a):
    positions=np.where(a,np.arange(len(a))[:,None],-1).max(axis=0)
    return len(a)-1-positions
def structure(draws):
    d=draws+1; spaces=np.diff(d,axis=1)
    return np.column_stack([d.sum(1),np.median(d,axis=1),d[:,0],d[:,-1],d[:,-1]-d[:,0],(d%2).sum(1),(d<=19).sum(1),(spaces==1).sum(1),spaces.max(1),((spaces<=2)).sum(1)])
STRUCT=['sum','median','minimum','maximum','range','odd_count','low_count','adjacent_pairs','largest_spacing','close_spacings_le2']

def exploratory(draws,records):
    a=indicator(draws); n=len(a); freq=a.sum(0); gap=gaps(a); weights=2.**(-np.arange(n-1,-1,-1)/20)
    pvals=[binom_p(n,6/38,v,True) for v in freq]; hp=holm(pvals)
    nums=[]
    for j in range(N):
        pos=np.flatnonzero(a[:,j]); completed=np.diff(pos)-1
        blocks=np.array([a[t:t+10,j].mean() for t in range(0,n-9,10)])
        row=dict(number=j+1,frequency=int(freq[j]),expected=n*6/38,deviation=freq[j]-n*6/38,appearance_rate=freq[j]/n,ew_rate=float(weights@a[:,j]/weights.sum()),current_gap=int(gap[j]),mean_completed_gap=float(completed.mean()),median_completed_gap=float(np.median(completed)),gap_sd=float(completed.std(ddof=1)),current_gap_percentile=float(np.mean(completed<=gap[j])),longest_completed_gap=int(completed.max()),longest_observed_absence=int(max(completed.max(),pos[0],gap[j])),gap_complete_intervals=len(completed),trend_20_vs_previous40=float(a[-20:,j].mean()-a[-60:-20,j].mean()),short_long_ratio=float(a[-20:,j].mean()/(freq[j]/n)),block10_rate_volatility=float(blocks.std(ddof=1)),frequency_p_two_sided=pvals[j],frequency_holm_p=hp[j])
        for w in [100,50,30,20,10]: row[f'last_{w}_count']=int(a[-w:,j].sum())
        nums.append(row)
    csvsave('number_statistics.csv',nums)
    features=structure(draws); drawrows=[]
    for t,r in enumerate(records):
        row=dict(draw_id=r['draw_id'],date=r['date'],numbers=r['numbers'],**dict(zip(STRUCT,features[t])),mean=float(np.mean(draws[t]+1)),even_count=int(6-features[t,5]),high_count=int(6-features[t,6]),bands=[int(np.sum((draws[t]+1>=lo)&(draws[t]+1<=hi))) for lo,hi in [(1,10),(11,20),(21,30),(31,38)]],spacing=np.diff(draws[t]).tolist(),last_digits=np.bincount((draws[t]+1)%10,minlength=10).tolist())
        for lag in [1,2,3,5]: row[f'repeated_from_previous_{lag}']=int(np.sum(a[t]&np.any(a[max(0,t-lag):t],axis=0))) if t>=lag else None
        drawrows.append(row)
    csvsave('draw_structure.csv',drawrows)
    pc=(a.T@a)[PI,PJ]; pairp=np.array([binom_p(n,PP,v) for v in pc]); ph=holm(pairp); pq=bh(pairp); pairrows=[]
    for i,(x,y) in enumerate(PAIRS):
        hits=a[:,x]*a[:,y]; pos=np.flatnonzero(hits)
        pairrows.append(dict(a=x+1,b=y+1,count=pc[i],expected=n*PP,lift_uniform=pc[i]/(n*PP),lift_empirical=pc[i]*n/(freq[x]*freq[y]),p_enrichment=pairp[i],holm_p=ph[i],bh_q=pq[i],recency=int(n-1-pos[-1]) if len(pos) else None,last50=int(hits[-50:].sum()),last100=int(hits[-100:].sum()),first_half=int(hits[:n//2].sum()),second_half=int(hits[n//2:].sum()),survives_holm=ph[i]<.05))
    csvsave('pair_statistics.csv',pairrows)
    tripcount={p:0 for p in TRIPLES}
    for d in draws:
        for triple in itertools.combinations(d,3): tripcount[triple]+=1
    csvsave('triple_statistics.csv',[dict(numbers=[x+1 for x in key],count=value,expected=n*math.comb(6,3)/math.comb(38,3),inference='descriptive only: sparse expected cell counts; no triple predictor') for key,value in sorted(tripcount.items(),key=lambda x:-x[1])])
    prev=a[:-1]; nxt=a[1:]; cc=prev.T@nxt; cp=[]; cr=[]
    for x in range(N):
        for y in range(N):
            trials=int(prev[:,x].sum()); count=int(cc[x,y]); p=fisher_upper(n-1,trials,int(nxt[:,y].sum()),count); cp.append(p)
            cr.append(dict(previous_number=x+1,next_number=y+1,trigger_draws=trials,following_count=count,conditional_rate=count/trials,unconditional_next_rate=float(nxt[:,y].mean()),p_enrichment=p))
    for r,h in zip(cr,holm(cp)): r['holm_p']=h
    csvsave('conditional_statistics.csv',cr)
    return nums,pairrows,drawrows

def diagnostics(d):
    a=indicator(d); n=len(a); f=a.sum(0); pc=(a.T@a)[PI,PJ]; st=structure(d); repeats=np.sum(a[:-1]*a[1:],axis=1); rh=np.bincount(repeats,minlength=7)
    serial=max(np.max(np.abs(((a[:-lag]-6/38)*(a[lag:]-6/38)).mean(0)/(6/38*(1-6/38)))) for lag in [1,2,3])
    # Finite-window complete gaps compared to geometric CDF; null calibrated using same censoring.
    gs=np.concatenate([np.diff(np.flatnonzero(a[:,j]))-1 for j in range(N)])
    grid=np.arange(31); gapks=float(np.max(np.abs(np.array([(gs<=g).mean() for g in grid])-(1-(1-6/38)**(grid+1)))))
    return np.array([np.sum((f-n*6/38)**2/(n*6/38)),np.max(np.abs(f-n*6/38)),np.sum((pc-n*PP)**2/(n*PP)),pc.max(),serial,gapks,np.sum((rh-(n-1)*PMF)**2/((n-1)*PMF)),repeats.mean(),st[:,0].mean(),st[:,0].std(),st[:,5].mean(),st[:,7].mean(),st[:,4].mean(),st[:,9].mean()])

def randomness(draws,sims=10000):
    rng=np.random.default_rng(SEED+1); obs=diagnostics(draws); names=['marginal_dispersion','max_number_deviation','pair_dispersion','max_pair_count','max_abs_serial_lags1_3','complete_gap_CDF_distance','repeat_distribution','mean_repeats','mean_sum','sum_sd','mean_odd','mean_adjacent_pairs','mean_range','mean_clustering']
    null=np.empty((sims,len(obs)))
    for i in range(sims):
        null[i]=diagnostics(sample(rng,len(draws)))
        if (i+1)%2000==0: print(f'Uniform history simulations: {i+1}/{sims}',flush=True)
    p=[]
    for k in range(len(obs)):
        p.append((1+np.sum(null[:,k]>=obs[k]))/(sims+1) if k<7 else min(1,2*min((1+np.sum(null[:,k]>=obs[k]))/(sims+1),(1+np.sum(null[:,k]<=obs[k]))/(sims+1))))
    adj=holm(p); rows=[]
    for k,name in enumerate(names): rows.append(dict(test=name,observed=obs[k],null_mean=null[:,k].mean(),null_95=np.quantile(null[:,k],[.025,.975]),p_mc=p[k],holm_p=adj[k],classification='statistically meaningful evidence' if adj[k]<.05 else 'weak/suggestive evidence' if p[k]<.05 else 'consistent with randomness'))
    save('randomness.json',dict(simulations=sims,tests=rows)); return rows

def model_features(a,window=30,half=20,trend=20,pair_alpha=.05,cap=None):
    if cap: a=a[-cap:]
    n=len(a); freq=(a.sum(0)+20*6/38)/(n+20)
    w=2.**(-np.arange(n-1,-1,-1)/half); recent=.5*a[-window:].mean(0)+.5*(w@a/w.sum())
    gap=gaps(a).astype(float); trendv=a[-trend:].mean(0)-a[max(0,n-3*trend):n-trend].mean(0)
    count=(a.T@a)[PI,PJ]; p=np.array([binom_p(n,PP,v) for v in count]); sig=holm(p)<pair_alpha
    mat=np.zeros((N,N)); mat[PI,PJ]=np.where(sig,count/(n*PP)-1,0); mat+=mat.T
    scores=np.array([zscore(freq),zscore(recent),zscore(gap),zscore(trendv),zscore(mat.sum(0))])
    historical=np.sort(np.where(a)[1].reshape(n,6),axis=1); st=structure(historical)
    return scores,mat,st.mean(0),np.maximum(st.std(0),1),int(sig.sum())
def objectives(pool,features):
    scores,mat,means,sd,_=features; values=np.empty((6,len(pool)))
    values[:4]=scores[:4,pool].mean(2)
    values[4]=np.array([mat[d[:,None],d[None,:]].sum()/30 for d in pool])
    values[5]=-np.mean(((structure(pool)-means)/sd)**2,axis=1)
    return np.array([zscore(v) for v in values])
def ensemble_weights(previous,mode='learned'):
    if mode=='equal' or len(previous)<10: return np.ones(6)/6
    pseudo=40 if mode=='shrunk' else 20
    excess=np.maximum((np.array(previous)[:,:6].sum(0)+pseudo*BASE)/(len(previous)+pseudo)-BASE,0)
    return excess/excess.sum() if excess.sum()>1e-12 else np.ones(6)/6
def walk(draws,records,minimum=50,window=30,half=20,trend=20,pair_alpha=.05,cap=None,weight_mode='learned',seed=SEED,details=False):
    a=indicator(draws); boundary=len(a)-40; prior=[]; result=[]; frozen=None
    for t in range(minimum,len(a)):
        train=a[:t].copy(); ft=model_features(train,window,half,trend,pair_alpha,cap)
        pool=sample(np.random.default_rng(seed+records[t]['draw_id']*101),512); val=objectives(pool,ft)
        if t>=boundary and frozen is None: frozen=ensemble_weights(prior,weight_mode)
        ew=frozen if frozen is not None else ensemble_weights(prior,weight_mode)
        totals=np.vstack([val,ew@val]); tickets=[pool[np.argmax(s)] for s in totals]
        tickets.append(sample(np.random.default_rng(seed+records[t]['draw_id']*1009),1)[0])
        # Target is accessed ONLY after all tickets and training-derived scores exist.
        truth=a[t]; matches=[int(truth[d].sum()) for d in tickets]; prior.append(matches)
        row=dict(index=t,draw_id=records[t]['draw_id'],date=records[t]['date'],training_last_draw_id=records[t-1]['draw_id'],period='confirmation' if t>=boundary else 'development',matches=matches,tickets=[(d+1).tolist() for d in tickets],ensemble_weights=ew.tolist(),retained_training_pairs=ft[-1])
        if details:
            ap=[]; recall=[]
            # F has no individual ranking. G's rank is weighted marginal rank (not its structure objective).
            individual=list(ft[0]); individual.append(None); individual.append(ew[:5]@ft[0]); individual.append(np.random.default_rng(seed+records[t]['draw_id']*3037).random(N))
            for s in individual:
                if s is None or np.std(s)<1e-12: ap.append(None); recall.append(None); continue
                jitter=np.random.default_rng(seed+records[t]['draw_id']).random(N)*1e-10
                rank=np.argsort(-(s+jitter)); rel=truth[rank]; ap.append(float(np.sum(np.cumsum(rel)/np.arange(1,N+1)*rel)/6)); recall.append(float(rel[:12].sum()/6))
            row['average_precision']=ap; row['recall_at12']=recall
        result.append(row)
    return result
def block_ci(y,rng,reps=10000):
    n=len(y); starts=rng.integers(0,n,(reps,math.ceil(n/5))); ix=(starts[:,:,None]+np.arange(5))%n
    means=np.asarray(y)[ix.reshape(reps,-1)[:,:n]].mean(1)
    return np.quantile(means,[.025,.975]).tolist()
def summaries(rows):
    rng=np.random.default_rng(SEED+10); out=[]
    for period in ['all','development','confirmation']:
        rr=[r for r in rows if period=='all' or r['period']==period]; m=np.array([r['matches'] for r in rr]); ps=[null_p(m[:,j]) for j in range(8)]; adjusted=holm(ps)
        random_means=rng.hypergeometric(6,32,6,size=(20000,len(rr))).mean(1)
        for j,name in enumerate(NAMES):
            y=m[:,j]; ci=block_ci(y,rng); iid=np.quantile(y[rng.integers(0,len(y),(10000,len(y)))].mean(1),[.025,.975]); hist=np.bincount(y,minlength=7)
            older=float(y[:len(y)//2].mean()); recent=float(y[len(y)//2:].mean())
            r=dict(model=name,period=period,n=len(y),total_matches=int(y.sum()),mean=float(y.mean()),median=float(np.median(y)),sd=float(y.std(ddof=1)),counts=hist.tolist(),percentages=(hist/len(y)*100).tolist(),four_plus_pct=float(np.mean(y>=4)*100),best=int(y.max()),older_half_mean=older,recent_half_mean=recent,delta_random=float(y.mean()-BASE),block95=ci,iid95=iid,p_exact_one_sided=ps[j],holm_p=adjusted[j],random_control_mc_p=float((1+np.sum(random_means>=y.mean()))/(len(random_means)+1)),random_mean_95=np.quantile(random_means,[.025,.975]),qualifies=bool(period=='confirmation' and adjusted[j]<.05 and ci[0]>BASE and min(older,recent)>BASE))
            for key in ['average_precision','recall_at12']:
                vals=[x[key][j] for x in rr if key in x and x[key][j] is not None]; r[key]=float(np.mean(vals)) if vals else None
            out.append(r)
    return out

def sensitivity(draws,records,main):
    configs=[('window20',{'window':20}),('window40',{'window':40}),('decay10',{'half':10}),('decay40',{'half':40}),('trend10',{'trend':10}),('trend30',{'trend':30}),('pair001',{'pair_alpha':.01}),('pair010',{'pair_alpha':.1}),('warmup40',{'minimum':40}),('warmup60',{'minimum':60}),('history100',{'cap':100}),('equal_weights',{'weight_mode':'equal'}),('shrunk_weights',{'weight_mode':'shrunk'}),('pool_seed',{'seed':SEED+99})]
    rows=[]; base={r['draw_id']:r for r in main}; finalsets=[]
    for name,cfg in configs:
        rr=walk(draws,records,**cfg); conf=[r for r in rr if r['period']=='confirmation']; mat=np.array([r['matches'] for r in conf]); common=[r for r in rr if r['draw_id'] in base]
        ps=holm([null_p(mat[:,j]) for j in range(8)])
        for j,model in enumerate(NAMES): rows.append(dict(variant=name,model=model,confirmation_n=len(conf),confirmation_mean=float(mat[:,j].mean()),confirmation_holm_p=ps[j],mean_ticket_overlap=float(np.mean([len(set(r['tickets'][j])&set(base[r['draw_id']]['tickets'][j])) for r in common]))))
        finalsets.append((name,cfg,rr)); print('Sensitivity:',name,flush=True)
    csvsave('sensitivity.csv',rows); return rows,finalsets

def candidates(draws,records,modelrows,main,variants,nums,pairrows):
    a=indicator(draws); ft=model_features(a); ew=ensemble_weights([r['matches'] for r in main]); pool=sample(np.random.default_rng(SEED+999),4096); values=objectives(pool,ft); val=np.vstack([values,ew@values]); selected=[]; sources=[]
    for j in range(7):
        count=0
        for idx in np.argsort(-val[j],kind='stable'):
            d=pool[idx]
            if all(len(set(d)&set(old))<=3 for old in selected): selected.append(d); sources.append(NAMES[j]); count+=1
            if count==(1 if j==6 else 3): break
    rng=np.random.default_rng(SEED+555)
    while len(selected)<20:
        d=sample(rng,1)[0]
        if all(len(set(d)&set(old))<=3 for old in selected): selected.append(d); sources.append('H_random')
    tickets=np.array(selected); cv=objectives(tickets,ft); cv=np.vstack([cv,ew@cv]); score_ranks=np.argsort(np.argsort(-cv,axis=1),axis=1)+1
    confirms={r['model']:r for r in modelrows if r['period']=='confirmation'}
    # Fixed candidate pool perturbations: compare ranks, do not reselect parameters.
    pert=[]
    for name,cfg,rr in variants:
        opts={k:v for k,v in cfg.items() if k in ['window','half','trend','pair_alpha','cap']}; f=model_features(a,**opts); v=objectives(tickets,f); weights=ensemble_weights([r['matches'] for r in rr],cfg.get('weight_mode','learned')); pert.append((name,np.vstack([v,weights@v])))
    ranks=np.array([np.argsort(np.argsort(-v,axis=1),axis=1)+1 for _,v in pert]); result=[]
    for i,d in enumerate(tickets):
        j=NAMES.index(sources[i]); informative=j<7 and not (j==4 and ft[-1]==0)
        generator_ranks=ranks[:,min(j,6),i] if informative else np.full(len(ranks),10.5)
        pairlist=[pairrows[PAIR_LOOKUP[x,y]] for x,y in itertools.combinations(d,2)]
        supporting=[NAMES[k] for k in range(7) if score_ranks[k,i]<=5 and (k!=4 or ft[-1]>0)]
        validated=[m for m in supporting if confirms[m]['qualifies']]
        nstats=[nums[x] for x in d]; support=confirms[sources[i]]
        candidate=dict(id=f'C{i+1:02}',numbers=(d+1).tolist(),generator=sources[i],contributing_models=supporting,validated_models=validated,individual_scores=[dict(number=x+1,long_z=ft[0][0,x],recent_z=ft[0][1,x],gap_z=ft[0][2,x],trend_z=ft[0][3,x]) for x in d],ensemble_score=cv[6,i],ensemble_rank=int(score_ranks[6,i]),model_ranks={NAMES[k]:int(score_ranks[k,i]) for k in range(7)},long_frequency_mean=float(np.mean([s['appearance_rate'] for s in nstats])),recent30_mean=float(np.mean([s['last_30_count']/30 for s in nstats])),ew_frequency_mean=float(np.mean([s['ew_rate'] for s in nstats])),gap_mean=float(np.mean([s['current_gap'] for s in nstats])),trend_mean=float(np.mean([s['trend_20_vs_previous40'] for s in nstats])),pair_lift_mean=float(np.mean([p['lift_uniform'] for p in pairlist])),corrected_significant_pairs=int(sum(p['survives_holm'] for p in pairlist)),structure=dict(zip(STRUCT,structure(d[None,:])[0])),model_agreement_count=len(supporting),generator_sensitivity_rank_min=float(generator_ranks.min()),generator_sensitivity_rank_max=float(generator_ranks.max()),sensitivity_top_quartile_fraction=float(np.mean(generator_ranks<=5)) if j<7 else 0.,sensitivity_mean_rank=float(generator_ranks.mean()),latest_draw_overlap=int(a[-1,d].sum()),walk_forward_support={k:support[k] for k in ['model','n','mean','block95','holm_p','older_half_mean','recent_half_mean','qualifies']},evidence_against=['Exact ticket and candidate variants have not been backtested.','Frequency, gaps, pair lift and structure are descriptive, not independent predictive evidence.','Models share the same small dataset; agreement is correlated.']+([] if validated else ['No qualifying independent out-of-sample support for this ticket.']))
        if not informative:
            candidate['sensitivity_top_quartile_fraction']=0.
            candidate['evidence_against'].append('Uniform fallback has no informative objective rank; sensitivity ranks are marked neutral, not evidence of stability.')
        result.append(candidate)
    assert len(result)==20 and max(len(set(x['numbers'])&set(y['numbers'])) for x,y in itertools.combinations(result,2))<=3
    save('candidates.json',result); save('candidate_sensitivity.json',dict(variants=[name for name,_ in pert],ranks=ranks,models=NAMES[:7],ensemble_weights=ew))
    return result

def main():
    records=json.loads((ROOT/'data/draws.json').read_text()); draws=np.array([r['numbers'] for r in records])-1
    assert all(records[i]['draw_id']+1==records[i+1]['draw_id'] for i in range(len(records)-1))
    baseline=dict(population=38,ticket_size=6,expected_matches=BASE,total_combinations=math.comb(38,6),match_probabilities=PMF,probability_at_least_two=float(PMF[2:].sum()),probability_at_least_three=float(PMF[3:].sum()))
    save('baseline.json',baseline)
    nums,pairs,drawrows=exploratory(draws,records); randomtests=randomness(draws)
    mainrows=walk(draws,records,details=True); save('walk_forward_predictions.json',mainrows); summary=summaries(mainrows); save('model_performance.json',summary); csvsave('model_performance.csv',summary)
    sens,variants=sensitivity(draws,records,mainrows); cands=candidates(draws,records,summary,mainrows,variants,nums,pairs)
    # Original-source ablation preserves calendar gap: no false consecutive/gap features; only frequency models.
    originals=[r for r in records if r['origin']=='workbook']; orig_draws=np.array([r['numbers'] for r in originals])-1
    ablation=[]
    for i in range(50,len(originals)):
        train=indicator(orig_draws[:i]); ft=model_features(train); pool=sample(np.random.default_rng(SEED+originals[i]['draw_id']*101),512); vals=objectives(pool,ft)
        if originals[i]['draw_id']>=records[-40]['draw_id']:
            for j in [0,1,3]: ablation.append(dict(draw_id=originals[i]['draw_id'],model=NAMES[j],matches=int(np.isin(pool[np.argmax(vals[j])],orig_draws[i]).sum())))
    save('source_ablation.json',dict(note='Only gap-independent A/B/D evaluated on original observed rows; rolling windows count observed records; sensitivity only, not a substitute primary dataset.',rows=ablation))
    qualifiers=[r['model'] for r in summary if r['qualifies']]
    meta=dict(seed=SEED,n=len(records),first=records[0],last=records[-1],next_draw_id=records[-1]['draw_id']+1,confirmation_draws=40,minimum_training=50,qualifying_models=qualifiers,protocol_sha256=hashlib.sha256((ROOT/'PROTOCOL.md').read_bytes()).hexdigest(),data_sha256=hashlib.sha256((ROOT/'data/draws.json').read_bytes()).hexdigest(),conclusion='No detectable edge in this dataset' if not qualifiers else 'Some suggestive evidence, but not enough to establish an edge',limitations=['Retrospective data and multiple tested approaches; no prospective replication.','Only 40 confirmation draws; low power for small advantages.','Final candidates and Jev layer are not historically validated.','Absence of evidence does not prove the physical lottery is perfectly random.'])
    save('analysis_metadata.json',meta)
    # Compact evidence; numeric computations remain in Python, not in Jev.
    state=dict(task='Evaluate empirical evidence for lottery candidates, not predict winning numbers.',baseline=baseline,metadata=meta,randomness=randomtests,methodology_confirmation=[r for r in summary if r['period']=='confirmation'],candidates=cands,interpretation='All fixed valid tickets have equal theoretical winning probability under a fair draw. Only qualifying_models pass the predefined empirical edge gate. Correlated models do not count as independent replication. Candidate quality judgments cannot establish a predictive edge.')
    save('jev_state.json',state)
    print(json.dumps(clean(dict(conclusion=meta['conclusion'],qualifiers=qualifiers,confirmation=[{k:r[k] for k in ['model','mean','holm_p','block95']} for r in summary if r['period']=='confirmation'],global_tests=randomtests)),indent=2))
if __name__=='__main__': main()
