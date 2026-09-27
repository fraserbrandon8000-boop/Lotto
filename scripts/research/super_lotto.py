import json,csv,math,itertools,hashlib,sys
from pathlib import Path
from datetime import datetime,timezone,timedelta
from collections import Counter
from functools import lru_cache
import openpyxl,numpy as np
from common import *
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'results/super_lotto';SOURCE=Path(r'C:\Data_Unbackupped\FRASEB01\Downloads\super_lotto_draw_history.xlsx');SEED=2026092109
N=35;K=5;P=K/N;BASE=K*K/N;PAIRS=np.array(list(itertools.combinations(range(N),2)));PI,PJ=PAIRS.T;PP=K*(K-1)/(N*(N-1))
MN=['A_long','B_recent','C_gap','D_trend','E_pairs','F_structure','G_ensemble','H_random'];SN=['S_long','S_recent','S_gap','S_trend','S_transition','S_ensemble','S_random']
@lru_cache(None)
def binomial(n,p):return np.array([math.exp(math.lgamma(n+1)-math.lgamma(j+1)-math.lgamma(n-j+1)+j*math.log(p)+(n-j)*math.log1p(-p)) for j in range(n+1)])
def bp(n,p,k):return float(binomial(int(n),float(p))[int(k):].sum())
def fisher(n,a,b,c):return sum(math.comb(b,j)*math.comb(n-b,a-j)/math.comb(n,a) for j in range(max(c,0,a+b-n),min(a,b)+1)) if a else 1.
def gap(a):return len(a)-1-np.where(a,np.arange(len(a))[:,None],-1).max(0)
def features(a,w=30,half=20,trend=20):
    n=len(a);ew=2.**(-np.arange(n-1,-1,-1)/half);return np.array([z(a.mean(0)),z(.5*a[-w:].mean(0)+.5*ew@a/ew.sum()),z(gap(a)),z(a[-trend:].mean(0)-a[max(0,n-3*trend):n-trend].mean(0))])
def structures(d):
    v=np.sort(d,axis=1)+1;s=np.diff(v,axis=1)
    return np.column_stack([v.sum(1),np.median(v,axis=1),v[:,0],v[:,-1],v[:,-1]-v[:,0],(v%2).sum(1),(v<=18).sum(1),(s==1).sum(1),s.max(1),(s<=2).sum(1)])
ST=['sum','median','min','max','range','odd','low_1_18','adjacent','largest_spacing','clustering_le2']
def pairmat(a,alpha=.05):
    n=len(a);counts=(a.T@a)[PI,PJ];ps=np.array([bp(n,PP,x) for x in counts]);adjust=holm(ps);mat=np.zeros((35,35));mat[PI,PJ]=np.where(adjust<alpha,counts/(n*PP)-1,0);return mat+mat.T,counts,ps,adjust
def weights(history,width,baseline,mode='learned'):
    if len(history)<10 or mode=='equal':return np.ones(width)/width
    x=np.maximum((np.array(history)[:,:width].sum(0)+20*baseline)/(len(history)+20)-baseline,0);return x/x.sum() if x.sum()>1e-12 else np.ones(width)/width
def objective(pool,s,mat,mean,sd):
    values=[*s[:,pool].mean(2),np.array([mat[t[:,None],t[None,:]].sum()/20 for t in pool]),-np.mean(((structures(pool)-mean)/sd)**2,axis=1)]
    return np.array([z(x) for x in values])
def audit():
    digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest();wb=openpyxl.load_workbook(SOURCE,read_only=True,data_only=True);raw=list(wb['Draws'].values);rr=raw[1:];problems=[];derived=[];records=[]
    for line,r in enumerate(rr,2):
        if any(v is None for v in r[:8]):problems.append(f'Missing required value row {line}')
        if not isinstance(r[0],int) or not isinstance(r[1],datetime):problems.append(f'Invalid ID/date row {line}');continue
        nums=list(r[2:7]);sb=r[7]
        if len(set(nums))!=5 or any(not isinstance(v,int) or not 1<=v<=35 for v in nums):problems.append(f'Invalid main row {line}')
        if not isinstance(sb,int) or not 1<=sb<=10:problems.append(f'Invalid SB row {line}')
        if r[1].weekday() not in [1,4]:problems.append(f'Unexpected draw weekday row {line}')
        for key,col,expected in [('sum',8,sum(nums)),('odd_count',9,sum(n%2 for n in nums)),('low_1_18',10,sum(n<=18 for n in nums)),('spread',11,max(nums)-min(nums))]:
            if r[col]!=expected:derived.append(dict(row=line,field=key,stored=r[col],calculated=expected))
        records.append(dict(draw_id=r[0],date=r[1].date().isoformat(),numbers=sorted(nums),super_ball=sb,source=str(SOURCE),sheet='Draws',row=line))
    ids=[r['draw_id'] for r in records];dates=[r['date'] for r in records];duplicates=[k for k,v in Counter(ids).items() if v>1];dup_records=[list(k) for k,v in Counter((r['date'],tuple(r['numbers']),r['super_ball']) for r in records).items() if v>1];missing=sorted(set(range(min(ids),max(ids)+1))-set(ids));records.sort(key=lambda r:r['draw_id'])
    for i,r in enumerate(records[1:],1):
        expected=len(set(r['numbers'])&set(records[i-1]['numbers']));stored=rr[r['row']-2][12]
        if expected!=stored:derived.append(dict(row=r['row'],field='carried_over',stored=stored,calculated=expected))
    freq=Counter(n for r in records for n in r['numbers']);sbcount=Counter(r['super_ball'] for r in records);freqdiff=[]
    for row in list(wb['Frequency'].values)[1:]:
        if isinstance(row[0],int) and row[1]!=freq[row[0]]:freqdiff.append(dict(field='main_count',number=row[0],stored=row[1],calculated=freq[row[0]]))
        if isinstance(row[5],int) and row[6]!=sbcount[row[5]]:freqdiff.append(dict(field='SB_count',number=row[5],stored=row[6],calculated=sbcount[row[5]]))
    official=json.loads((OUT/'official-current.json').read_text(encoding='utf-8-sig'));external=[]
    for item in official:
        r=item['Evening'];x=dict(draw_id=int(r['drawNumber']),date=r['drawDate'],numbers=sorted(map(int,r['winNumber'].split())),super_ball=int(r['superBall']),source='https://supremeventures.com/past-results/',api_source='https://test-results.supremeventures.com/public/game/9/from/2026-09-18/to/2026-09-21')
        old=next((v for v in records if v['draw_id']==x['draw_id']),None)
        if old:assert all(old[k]==x[k] for k in ['date','numbers','super_ball'])
        else:external.append(x);records.append(x)
    wb.close();records.sort(key=lambda r:r['draw_id']);assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==digest
    result=dict(workbook=str(SOURCE),sha256=digest,original_records=len(rr),id_range=[min(ids),max(ids)],date_range=[min(dates),max(dates)],order='descending' if ids==sorted(ids,reverse=True) else 'other',dates_descending=dates==sorted(dates,reverse=True),missing_ids=missing,duplicate_ids=duplicates,duplicate_records=dup_records,invalid_or_missing=problems,derived_column_discrepancies=derived,frequency_discrepancies=freqdiff,summary_rounding='Expected main frequency 176*5/35=25.142857, workbook rounds to 25.1; all models recompute raw rows.',new_official_draws=external,cutoff=records[-1],provenance_limit='Workbook states screenshot transcription; only latest overlapping draw independently checked against official feed.')
    save(OUT/'audit.json',result);save(OUT/'draws.json',records);save(OUT/'external_draws.json',external)
    assert not (problems or duplicates or dup_records or missing)
    return records,result
def descriptive(records,d,sb):
    a=ind(d,35);b=ind(sb[:,None],10);n=len(a)
    for name,x,prob in [('main',a,5/35),('super_ball',b,.1)]:
        rows=[]
        for j in range(x.shape[1]):
            pos=np.flatnonzero(x[:,j]);g=np.diff(pos)-1;cg=gap(x)[j];w=2.**(-np.arange(n-1,-1,-1)/20)
            r=dict(number=j+1,count=int(x[:,j].sum()),expected=n*prob,deviation=x[:,j].sum()-n*prob,ew_rate=float(w@x[:,j]/w.sum()),current_gap=int(cg),mean_gap=float(g.mean()),median_gap=float(np.median(g)),gap_sd=float(g.std(ddof=1)),gap_percentile=float(np.mean(g<=cg)),longest_absence=int(max(g.max(),cg,pos[0])),trend=float(x[-20:,j].mean()-x[-60:-20,j].mean()),short_long_ratio=float(x[-20:,j].mean()/x[:,j].mean()),volatility=float(np.std([x[i:i+10,j].mean() for i in range(0,n-9,10)])),complete_gaps=g.tolist())
            for w0 in [100,50,30,20,10]:r[f'last{w0}']=int(x[-w0:,j].sum())
            rows.append(r)
        csvsave(OUT/f'{name}_features.csv',rows)
    mat,counts,ps,adj=pairmat(a);pairrows=[]
    for i,(x,y) in enumerate(PAIRS):
        h=a[:,x]*a[:,y];where=np.flatnonzero(h);pairrows.append(dict(a=x+1,b=y+1,count=counts[i],expected=n*PP,lift=counts[i]/(n*PP),p=ps[i],holm_p=adj[i],first_half=int(h[:n//2].sum()),second_half=int(h[n//2:].sum()),last50=int(h[-50:].sum()),last100=int(h[-100:].sum()),gap=int(n-1-where[-1]) if len(where) else None))
    csvsave(OUT/'pairs.csv',pairrows)
    triples=Counter(t for row in d for t in itertools.combinations(row,3));csvsave(OUT/'triples.csv',[dict(numbers=[i+1 for i in t],count=triples[t],expected=n*math.comb(5,3)/math.comb(35,3)) for t in itertools.combinations(range(35),3)])
    for name,x in [('main',a),('super_ball',b)]:
        trans=x[:-1].T@x[1:];rows=[]
        for i in range(x.shape[1]):
            for j in range(x.shape[1]):
                trials=int(x[:-1,i].sum());cnt=int(trans[i,j]);rows.append(dict(previous=i+1,next=j+1,trials=trials,count=cnt,rate=cnt/trials,p=fisher(n-1,trials,int(x[1:,j].sum()),cnt)))
        for r,p in zip(rows,holm([r['p'] for r in rows])):r['holm_p']=p
        csvsave(OUT/f'{name}_transitions.csv',rows)
    rows=[];st=structures(d)
    for i,r in enumerate(records):
        row=dict(draw_id=r['draw_id'],date=r['date'],**dict(zip(ST,st[i])),mean=float(np.mean(d[i]+1)),even=5-int(st[i,5]),high=5-int(st[i,6]),spacing=np.diff(d[i]).tolist(),bands=[int(np.sum((d[i]+1>=lo)&(d[i]+1<=hi))) for lo,hi in [(1,10),(11,20),(21,30),(31,35)]],last_digits=np.bincount((d[i]+1)%10,minlength=10).tolist())
        for lag in [1,2,3,5]:row[f'repeat_prior{lag}']=int(np.sum(a[i]&np.any(a[i-lag:i],axis=0))) if i>=lag else None
        rows.append(row)
    csvsave(OUT/'draw_structure.csv',rows)
def stats(d,sb):
    a=ind(d,35);n=len(a);f=a.sum(0);co=(a.T@a)[PI,PJ];b=np.bincount(sb,minlength=10);g=np.concatenate([np.diff(np.flatnonzero(a[:,j]))-1 for j in range(35)]);grid=np.arange(25)
    return np.array([np.sum((f-n*P)**2/(n*P)),np.sum((co-n*PP)**2/(n*PP)),co.max(),max(np.max(np.abs(((a[:-lag]-P)*(a[lag:]-P)).mean(0)/(P*(1-P)))) for lag in [1,2,3]),np.max(np.abs(np.array([(g<=i).mean() for i in grid])-(1-(1-P)**(grid+1)))),np.sum(a[:-1]*a[1:],axis=1).mean(),(d+1).sum(1).mean(),((d+1)%2).sum(1).mean(),np.sum((b-n/10)**2/(n/10)),np.mean(sb[:-1]==sb[1:])])
def randomness(d,sb):
    obs=stats(d,sb);r=np.random.default_rng(SEED+1);null=np.empty((10000,len(obs)))
    for i in range(10000):
        null[i]=stats(sample(r,len(d),35,5),r.integers(10,size=len(d)))
        if (i+1)%2500==0:print('Super Lotto simulations',i+1,flush=True)
    names=['main_dispersion','pair_dispersion','max_pair','serial_max_lag1_3','gap_CDF','repeat_mean','sum_mean','odd_mean','SB_dispersion','SB_repeat_rate'];ps=[]
    for k in range(len(obs)):
        upper=(1+np.sum(null[:,k]>=obs[k]))/10001;lower=(1+np.sum(null[:,k]<=obs[k]))/10001;ps.append(upper if k in [2,3,4] else min(1,2*min(upper,lower)))
    tests=[dict(test=name,observed=obs[i],null_mean=null[:,i].mean(),null95=np.quantile(null[:,i],[.025,.975]),p=ps[i],holm_p=h,classification='statistically meaningful evidence' if h<.05 else 'suggestive but insufficient evidence' if ps[i]<.05 else 'consistent with randomness') for i,(name,h) in enumerate(zip(names,holm(ps)))];save(OUT/'randomness.json',dict(simulations=10000,tests=tests));return tests
def walk(d,sb,ids,w=30,half=20,trend=20,cap=None,alpha=.05,mode='learned',seed=SEED,build=False):
    a=ind(d,35);b=ind(sb[:,None],10);n=len(a);mh=[];sh=[];mwfreeze=None;swfreeze=None;rows=[];buildrows=[]
    for t in range(50,n+1):
        aa=a[max(0,t-cap):t] if cap else a[:t];bb=b[max(0,t-cap):t] if cap else b[:t];s=features(aa,w,half,trend);ss=features(bb,w,half,trend);mat,_,_,_=pairmat(aa,alpha);hist=d[max(0,t-cap):t] if cap else d[:t];st=structures(hist);mean=st.mean(0);sd=np.maximum(st.std(0),1)
        transitions=bb[:-1].T@bb[1:];trials=int(bb[:-1,sb[t-1]].sum());last=sb[t-1];pp=[bp(trials,.1,x) for x in transitions[last]] if trials else [1]*10;tv=np.where(holm(pp)<alpha,transitions[last]/max(1,trials)-.1,0);ss=np.vstack([ss,z(tv)])
        if t>=n-40 and mwfreeze is None:mwfreeze=weights(mh,6,BASE,mode);swfreeze=weights(sh,5,.1,mode)
        mw=mwfreeze if mwfreeze is not None else weights(mh,6,BASE,mode);sw=swfreeze if swfreeze is not None else weights(sh,5,.1,mode)
        targetid=ids[t] if t<n else ids[-1]+1;r=np.random.default_rng(seed+targetid*101);pool=sample(r,512,35,5);v=objective(pool,s,mat,mean,sd);tickets=[pool[np.argmax(x)] for x in np.vstack([v,mw@v])];tickets.append(sample(np.random.default_rng(seed+targetid*503),1,35,5)[0]);jitter=np.random.default_rng(seed+targetid*67).random(10)*1e-10;sbpred=[int(np.argmax(x+jitter)) for x in np.vstack([ss,sw@ss])]+[int(np.random.default_rng(seed+targetid*907).integers(10))]
        individual=[*s,z(mat.sum(0)),None,mw[:4]@s+mw[4]*z(mat.sum(0)),np.random.default_rng(seed+targetid*911).random(35)];ranks={}
        for name,x in zip(MN,individual):
            if x is not None and (np.std(x)>1e-10 or name=='G_ensemble'):ranks[name]=np.argsort(-(x+np.random.default_rng(seed+targetid*31).random(35)*1e-10))
        if t==n:return rows,buildrows,dict(scores=s,pair_matrix=mat,mean=mean,sd=sd,main_weights=mw,sb_weights=sw,sb_scores=ss,sb_predictions=sbpred,rankings=ranks,individual_scores={name:x for name,x in zip(MN,individual) if x is not None},tickets=tickets)
        constructed={}
        if build:
            for name in ['A_long','B_recent','D_trend','G_ensemble']:
                order=ranks[name];x=individual[MN.index(name)];constructed[name+':top5']=order[:5]
                for m in [7,8,10,12,15]:
                    combos=np.sort(np.array(list(itertools.combinations(order[:m],5))),axis=1);merit=x[combos].mean(1);pen=np.mean(((structures(combos)-mean)/sd)**2,axis=1)
                    constructed[f'{name}:pool{m}:structure']=combos[np.argmax(merit-.25*pen)]
                    constructed[f'{name}:pool{m}:uniform']=np.random.default_rng(seed+targetid*113+m).choice(order[:m],5,replace=False)
        # Reveal outcome only after predictions and constructed tickets exist.
        hits=[int(a[t,x].sum()) for x in tickets];sbh=[int(x==sb[t]) for x in sbpred];mh.append(hits);sh.append(sbh)
        coverage={name:{str(m):int(a[t,order[:m]].sum()) for m in [5,7,8,10,12,15,20]} for name,order in ranks.items()};ap={name:float(np.sum(a[t,order]*np.cumsum(a[t,order])/np.arange(1,36))/5) for name,order in ranks.items()}
        rows.append(dict(index=t,draw_id=targetid,training_cutoff=ids[t-1],period='confirmation' if t>=n-40 else 'development',main_tickets=[(x+1).tolist() for x in tickets],SB_predictions=[x+1 for x in sbpred],main_hits=hits,SB_hits=sbh,rankings={k:(v+1).tolist() for k,v in ranks.items()},coverage=coverage,AP=ap,main_weights=mw.tolist(),SB_weights=sw.tolist()))
        for name,x in constructed.items():buildrows.append(dict(index=t,draw_id=targetid,method=name,ticket=(np.sort(x)+1).tolist(),hits=int(a[t,x].sum())))
def performance(rows,buildrows):
    perf=[];coverage=[];joint=[]
    for period in ['all','development','confirmation']:
        rr=[r for r in rows if period=='all' or r['period']==period]
        for domain,names,key,NN,KK in [('main',MN,'main_hits',35,5),('SB',SN,'SB_hits',10,1)]:
            for j,name in enumerate(names):
                y=np.array([r[key][j] for r in rr]);ci=blockci(y);perf.append(dict(domain=domain,model=name,period=period,n=len(y),mean=y.mean(),total=int(y.sum()),rates=np.bincount(y,minlength=KK+1)/len(y),p=pmean(y,NN,KK,KK),ci=ci,older=y[:len(y)//2].mean(),recent=y[len(y)//2:].mean()))
        for name in MN:
            for m in [5,7,8,10,12,15,20]:
                sub=[r for r in rr if name in r['coverage']];y=np.array([r['coverage'][name][str(m)] for r in sub]);pmf=hg(35,5,m)
                if len(y):coverage.append(dict(model=name,pool=m,period=period,n=len(y),mean=y.mean(),median=np.median(y),random_mean=5*m/35,three_plus=np.mean(y>=3),four_plus=np.mean(y>=4),all5=np.mean(y==5),random_three_plus=pmf[3:].sum(),random_four_plus=pmf[4:].sum(),random_all5=pmf[5],AP=np.mean([r['AP'][name] for r in sub]),p=pmean(y,35,5,m)))
        for j,m in enumerate(MN):
            for k,s in enumerate(SN):
                ct=np.zeros((6,2),int)
                for r in rr:ct[r['main_hits'][j],r['SB_hits'][k]]+=1
                joint.append(dict(period=period,main_model=m,SB_model=s,n=len(rr),counts_main_by_SB=ct))
    for domain in ['main','SB']:
        for period in ['all','development','confirmation']:
            sub=[r for r in perf if r['domain']==domain and r['period']==period];base=BASE if domain=='main' else .1
            for r,p in zip(sub,holm([r['p'] for r in sub])):r['holm_p']=p;r['qualifies']=bool(period=='confirmation' and p<.05 and r['ci'][0]>base and min(r['older'],r['recent'])>base)
    for period in ['all','development','confirmation']:
        sub=[r for r in coverage if r['period']==period]
        for r,p in zip(sub,holm([r['p'] for r in sub])):r['holm_p']=p
    cons=[]
    for period in ['all','confirmation']:
        for method in sorted({r['method'] for r in buildrows}):
            sub=[r for r in buildrows if r['method']==method and (period=='all' or r['index']>=rows[-1]['index']-39)];y=np.array([r['hits'] for r in sub]);cons.append(dict(period=period,method=method,n=len(y),mean=y.mean(),ci=blockci(y),p=pmean(y,35,5,5),rates=np.bincount(y,minlength=6)/len(y)))
        subset=[r for r in cons if r['period']==period]
        for r,p in zip(subset,holm([r['p'] for r in subset])):r['holm_p']=p
    save(OUT/'performance.json',perf);save(OUT/'coverage.json',coverage);save(OUT/'combined_performance.json',joint);save(OUT/'construction_performance.json',cons);return perf
def candidate_set(records,d,sb,fit,perf,sensfits):
    pool=sample(np.random.default_rng(SEED+333),4096,35,5);vals=objective(pool,fit['scores'],fit['pair_matrix'],fit['mean'],fit['sd']);vals=np.vstack([vals,fit['main_weights']@vals]);selected=[];generators=[]
    for j in range(7):
        count=0
        for i in np.argsort(-vals[j],kind='stable'):
            t=pool[i]
            if all(len(set(t)&set(x))<=3 for x in selected):selected.append(t);generators.append(j);count+=1
            if count==(1 if j==6 else 3):break
    while len(selected)<20:
        x=sample(np.random.default_rng(SEED+555+len(selected)),1,35,5)[0]
        if all(len(set(x)&set(y))<=3 for y in selected):selected.append(x);generators.append(7)
        else:raise ValueError('Diversity fallback needs new seed counter')
    a=ind(d,35);b=ind(sb[:,None],10);out=[]
    def support(name):return next(r for r in perf if r['model']==name and r['period']=='confirmation')
    tickets=np.array(selected);basev=objective(tickets,fit['scores'],fit['pair_matrix'],fit['mean'],fit['sd']);basev=np.vstack([basev,fit['main_weights']@basev]);variant_ranks=[]
    for ff in sensfits:
        v=objective(tickets,ff['scores'],ff['pair_matrix'],ff['mean'],ff['sd']);v=np.vstack([v,ff['main_weights']@v]);variant_ranks.append(np.argsort(np.argsort(-v,axis=1),axis=1)+1)
    for i,(t,j) in enumerate(zip(tickets,generators)):
        sj=i%len(SN);ball=fit['sb_predictions'][sj];ms=support(MN[j]);bs=support(SN[sj]);rankmap={name:[int(np.flatnonzero(order==x)[0])+1 for x in t] for name,order in fit['rankings'].items()};vr=np.array(variant_ranks)[:,min(j,6),i];qualified=[r['model'] for r in [ms,bs] if r['qualifies']]
        out.append(dict(id=f'SL{i+1:02}',main=(t+1).tolist(),super_ball=ball+1,main_generator=MN[j],SB_generator=SN[sj],main_ranks=rankmap,long_mean=float(a[:,t].mean()),recent30_mean=float(a[-30:,t].mean()),gap_mean=float(gap(a)[t].mean()),trend_mean=float((a[-20:,t].mean(0)-a[-60:-20,t].mean(0)).mean()),pair_evidence=float(fit['pair_matrix'][t[:,None],t[None,:]].sum()),structure=dict(zip(ST,structures(t[None,:])[0])),ensemble_score=float(basev[6,i]),sensitivity_rank_range=[int(vr.min()),int(vr.max())],sensitivity_top5_fraction=float(np.mean(vr<=5)) if j not in [4,7] else 0.,model_agreement_count=sum(sum(r<=12 for r in ranks)>=4 for ranks in rankmap.values()),main_support=ms,SB_support=bs,SB_evidence=dict(full_count=int(b[:,ball].sum()),recent30_count=int(b[-30:,ball].sum()),gap=int(gap(b)[ball]),scores=fit['sb_scores'][:,ball].tolist()),qualified_models=qualified,counterevidence=['Candidate itself and final Jev policy are not walk-forward validated.','Main and SB evidence are separate; no unsupported cross-game or joint dependence.','Agreement among same-data models is not independent replication.','Flat pair/random objectives do not prove stability.']))
    save(OUT/'candidates.json',out);return out
def main():
    records,auditresult=audit();d=np.array([r['numbers'] for r in records])-1;sb=np.array([r['super_ball'] for r in records])-1;ids=[r['draw_id'] for r in records];pmf=hg(35,5,5)
    baseline=dict(main_probabilities=pmf,expected_main=BASE,SB_probability=.1,main_plus_SB_probabilities=pmf*.1,main_without_SB_probabilities=pmf*.9,jackpot_probability=1/(math.comb(35,5)*10),jackpot_denominator=math.comb(35,5)*10);save(OUT/'baseline.json',baseline)
    descriptive(records,d,sb);random=randomness(d,sb);rows,construct,fit=walk(d,sb,ids,build=True);save(OUT/'walk_forward.json',rows);save(OUT/'construction_origins.json',construct);perf=performance(rows,construct);save(OUT/'predraw_rankings_and_fit.json',fit)
    configs=[('window20',dict(w=20)),('window40',dict(w=40)),('half10',dict(half=10)),('half40',dict(half=40)),('trend10',dict(trend=10)),('trend30',dict(trend=30)),('history100',dict(cap=100)),('pair001',dict(alpha=.01)),('pair010',dict(alpha=.1)),('equal',dict(mode='equal')),('seed',dict(seed=SEED+99))];sens=[];fits=[]
    for name,cfg in configs:
        rr,_,ff=walk(d,sb,ids,**cfg);fits.append(ff);sub=[r for r in rr if r['period']=='confirmation']
        for names,key,NN,KK in [(MN,'main_hits',35,5),(SN,'SB_hits',10,1)]:
            ps=[pmean([r[key][j] for r in sub],NN,KK,KK) for j in range(len(names))]
            for j,(model,p) in enumerate(zip(names,holm(ps))):sens.append(dict(variant=name,model=model,confirmation_mean=float(np.mean([r[key][j] for r in sub])),holm_p=p))
        print('Super Lotto sensitivity',name,flush=True)
    save(OUT/'sensitivity.json',sens);candidates=candidate_set(records,d,sb,fit,perf,fits)
    r=np.random.default_rng(SEED+777);save(OUT/'random_controls.json',dict(replicates=20000,main_confirmation95=np.quantile(r.hypergeometric(5,30,5,(20000,40)).mean(1),[.025,.975]),SB_confirmation95=np.quantile(r.binomial(1,.1,(20000,40)).mean(1),[.025,.975])))
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==auditresult['sha256']
    meta=dict(game='Super Lotto',seed=SEED,cutoff=records[-1],origins=len(rows),qualifying_models=[r['model'] for r in perf if r['qualifies']],conclusion='No detectable edge in this dataset' if not any(r['qualifies'] for r in perf) else 'Suggestive retrospective evidence requiring prospective replication',configuration=dict(warmup=50,confirmation=40,search_pool=512,window=30,half_life=20,trend=20,pair_alpha=.05),source_sha256=auditresult['sha256'],protocol_sha256=hashlib.sha256((OUT/'PROTOCOL.md').read_bytes()).hexdigest());save(OUT/'metadata.json',meta)
    save(OUT/'jev_state.json',dict(game='Super Lotto only',rules='Five distinct main numbers 1–35 plus one independent Super Ball 1–10.',baseline=baseline,metadata=meta,randomness=random,candidates=candidates,interpretation='Choice is a preference among full tickets, not a winning probability. Only qualified_models pass corrected retrospective confirmation; no prospective validation exists.'))
    print(json.dumps(clean(dict(audit=auditresult,qualifiers=meta['qualifying_models'],confirmation=[r for r in perf if r['period']=='confirmation'])),indent=2))
if __name__=='__main__':main()
