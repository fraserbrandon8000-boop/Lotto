import sys,json,csv,hashlib,shutil,itertools
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
from common import *
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'results/lotto';SNAP=OUT/'v1_snapshot'
sys.path.insert(0,str(ROOT/'scripts'));import analyze as v1

def snapshot():
    manifest={}
    for folder in ['results','data','scripts']:
        for f in (ROOT/folder).iterdir():
            if f.is_file():
                dest=SNAP/folder/f.name;dest.parent.mkdir(parents=True,exist_ok=True)
                if not dest.exists():shutil.copy2(f,dest)
                digest=hashlib.sha256(f.read_bytes()).hexdigest();assert digest==hashlib.sha256(dest.read_bytes()).hexdigest();manifest[str(f.relative_to(ROOT))]=digest
    for f in (ROOT/'experiments').rglob('*.json'):
        dest=SNAP/f.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists():shutil.copy2(f,dest)
        digest=hashlib.sha256(f.read_bytes()).hexdigest();assert digest==hashlib.sha256(dest.read_bytes()).hexdigest();manifest[str(f.relative_to(ROOT))]=digest
    path=OUT/'v1_manifest.json'
    if not path.exists():save(path,dict(captured_utc=datetime.now(timezone.utc).isoformat(),files=manifest))
    return manifest
def load(name):return json.loads((SNAP/name).read_text())
def run():
    manifest=snapshot();records=load('data/draws.json');d=np.array([r['numbers'] for r in records])-1;assert records[-1]['draw_id']==2338
    official=json.loads((OUT/'official-current.json').read_text(encoding='utf-8-sig'))[0]['Evening'];win=np.array(list(map(int,official['winNumber'].split())))-1;assert int(official['drawNumber'])==2339
    truth=set(map(int,win+1));old=load('results/walk_forward_predictions.json');cands=load('results/candidates.json');final=load('results/final_decision.json');jev=load('results/jev_response.json')
    tracks=[]
    def track(name,t,kind,source):tracks.append(dict(track=name,numbers=t,matches=len(set(t)&truth),matched=sorted(set(t)&truth),status=kind,source=source))
    for k in ['primary','secondary']:track('V1_'+k,final[k]['numbers'],'frozen_pre_draw','results/final_decision.json')
    jw=next(c for c in cands if c['id']==jev['answers']['overall']['choice']);track('Jev_evidence_preference',jw['numbers'],'pre_draw_analysis_not_primary','results/jev_response.json')
    for c in cands:track('candidate_'+c['id'],c['numbers'],'pre_draw_candidate_not_separate_prospective_track','results/candidates.json')
    for folder,label in [('jev-only-zero-data','sequential_invalidated'),('jev-complete-ticket-zero-data','Jev_Challenger')]:
        x=load(f'experiments/{folder}/frozen-result.json');track(label,x['combination'],'invalidated_before_draw' if label.startswith('sequential') else 'frozen_pre_draw',f'experiments/{folder}/frozen-result.json')
    ledger=OUT/'prospective_ledger.jsonl'
    if not ledger.exists() or ledger.stat().st_size==0:
        with ledger.open('a',encoding='utf-8') as f:
            for t in tracks:f.write(json.dumps(dict(event='outcome_appended',recorded_utc=datetime.now(timezone.utc).isoformat(),draw_id=2339,draw_date=official['drawDate'],outcome=sorted(truth),bonus=int(official['bonusBall']),**t))+'\n')
    a=ind(d,38);ft=v1.model_features(a);weights=load('results/candidate_sensitivity.json')['ensemble_weights'];scores={name:ft[0][i] for i,name in enumerate(v1.NAMES[:5])};scores['G_marginal_proxy']=np.array(weights[:5])@ft[0]
    # Reconcile reconstruction to every score that was actually persisted.
    for c in cands:
        for row in c['individual_scores']:
            for j,key in enumerate(['long_z','recent_z','gap_z','trend_z']):assert abs(row[key]-ft[0][j,row['number']-1])<1e-10
    rankings=[];coverage=[]
    for name,s in scores.items():
        applicable=np.std(s)>1e-10
        for number in range(1,39):
            x=s[number-1];better=np.sum(s>x+1e-9);equal=np.sum(np.abs(s-x)<=1e-9)
            rankings.append(dict(model=name,number=number,score=x,rank_min=int(better+1) if applicable else None,rank_max=int(better+equal) if applicable else None,provenance='reconstructed_from_frozen_pre_draw_inputs' if applicable else 'flat_unranked'))
        for size in [5,6,8,10,12,15,20]:
            cutoff=np.sort(s)[::-1][size-1];above=s>cutoff+1e-9;tied=np.abs(s-cutoff)<=1e-9;slots=size-int(above.sum());certain=int(above[win].sum());tw=int(tied[win].sum());tn=int(tied.sum())
            coverage.append(dict(model=name,pool=size,minimum_winners=certain+max(0,slots-(tn-tw)),maximum_winners=certain+min(slots,tw),tie_averaged_winners=certain+slots*tw/tn,applicable=applicable))
    csvsave(OUT/'predraw_reconstructed_rankings.csv',rankings);csvsave(OUT/'draw2339_topN_coverage.csv',coverage)
    stored=list(csv.DictReader((SNAP/'results/number_statistics.csv').open()));groups={1:'hit',4:'hit',13:'hit',14:'selected_miss',24:'selected_miss',38:'selected_miss',6:'missed_winner',23:'missed_winner',28:'missed_winner'};evidence=[]
    for r in stored:
        n=int(r['number'])
        if n in groups:
            evidence.append(dict(group=groups[n],**r,stored_candidate_occurrences=sum(n in c['numbers'] for c in cands),candidate_memberships=[c['id'] for c in cands if n in c['numbers']],rankings={s:[x['rank_min'],x['rank_max']] for s in scores for x in rankings if x['number']==n and x['model']==s},pair_network_score=float(ft[0][4,n-1]),ensemble_marginal_score=float(scores['G_marginal_proxy'][n-1]),sensitivity='Stored at ticket level only; no pre-draw number-level sensitivity was persisted.'))
    save(OUT/'hit_miss_predraw_evidence.json',evidence)
    # Historical test; #2339 is absent by construction.
    rank_records=[];construction=[];M=['A_long','B_recent','C_gap','D_trend','G_marginal_proxy','G_equal_proxy'];sizes=[5,6,8,10,12,15,20]
    for ix,t in enumerate(range(50,len(d))):
        f=v1.model_features(a[:t]);w=np.array(old[ix]['ensemble_weights']);ss=[*f[0][:4],w[:5]@f[0],np.mean(f[0],axis=0)];tickets={};ranks={}
        for name,s in zip(M,ss):
            jitter=np.random.default_rng(v1.SEED+records[t]['draw_id']).random(38)*1e-10;order=np.argsort(-(s+jitter));ranks[name]=order
            tickets[f'{name}:top6']=order[:6]
            for m in [8,10,12,15]:
                combinations=np.array(list(itertools.combinations(order[:m],6)));merit=s[combinations].mean(1);strpen=np.mean(((v1.structure(combinations)-f[2])/f[3])**2,axis=1)
                # sorted structures are required when candidate order follows rank.
                strpen=np.mean(((v1.structure(np.sort(combinations,axis=1))-f[2])/f[3])**2,axis=1)
                for penalty in [.25,1.]:tickets[f'{name}:top{m}:structure{penalty}']=combinations[np.argmax(merit-penalty*strpen)]
                tickets[f'{name}:top{m}:uniform']=np.random.default_rng(20260921+records[t]['draw_id']*97+m).choice(order[:m],6,replace=False)
        pool=v1.sample(np.random.default_rng(v1.SEED+records[t]['draw_id']*101),4096);values=v1.objectives(pool,f);tickets['G_4096']=pool[np.argmax(w@values)]
        # Reveal target only after constructing ranks and every ticket.
        actual=a[t]
        for name,order in ranks.items():
            rel=actual[order];ap=float(np.sum(rel*np.cumsum(rel)/np.arange(1,39))/6)
            for m in sizes:rank_records.append(dict(index=t,draw_id=records[t]['draw_id'],model=name,pool=m,hits=int(actual[order[:m]].sum()),average_precision=ap))
        for name,ticket in tickets.items():construction.append(dict(index=t,draw_id=records[t]['draw_id'],method=name,ticket=(np.sort(ticket)+1).tolist(),matches=int(actual[ticket].sum())))
        if ix%30==0:print('Lotto forensic historical origin',ix,flush=True)
    save(OUT/'ranking_origins.json',rank_records);save(OUT/'construction_origins.json',construction)
    covsummary=[];perform=[];rng=np.random.default_rng(20260921)
    for period in ['all','development','confirmation']:
        inperiod=lambda t:period=='all' or (t>=len(d)-40 if period=='confirmation' else t<len(d)-40)
        for name in M:
            for m in sizes:
                rr=[r for r in rank_records if r['model']==name and r['pool']==m and inperiod(r['index'])];y=np.array([r['hits'] for r in rr]);pmf=hg(38,6,m)
                covsummary.append(dict(period=period,model=name,pool=m,n=len(y),mean=y.mean(),median=np.median(y),random_mean=6*m/38,p=pmean(y,38,6,m),average_precision=np.mean([r['average_precision'] for r in rr]),rates={str(k):float(np.mean(y>=k)) for k in range(2,7)},random_rates={str(k):float(pmf[k:].sum()) for k in range(2,7)}))
        for method in sorted({r['method'] for r in construction}):
            rr=[r for r in construction if r['method']==method and inperiod(r['index'])];y=np.array([r['matches'] for r in rr]);baseline=np.array([old[r['index']-50]['matches'][1] for r in rr]);ci=blockci(y);diffci=blockci(y-baseline)
            perform.append(dict(period=period,method=method,n=len(y),mean=y.mean(),total=int(y.sum()),rates=(np.bincount(y,minlength=7)/len(y)).tolist(),three_plus=float(np.mean(y>=3)),four_plus=float(np.mean(y>=4)),p=pmean(y,38,6,6),ci=ci,older=y[:len(y)//2].mean(),recent=y[len(y)//2:].mean(),paired_delta_vs_B=float(np.mean(y-baseline)),paired_ci_vs_B=diffci))
    for rows in [covsummary,perform]:
        for period in ['all','development','confirmation']:
            subset=[r for r in rows if r['period']==period]
            for r,p in zip(subset,holm([r['p'] for r in subset])):r['holm_p']=p
    qualifying=[r for r in perform if r['period']=='confirmation' and r['holm_p']<.05 and r['ci'][0]>36/38 and min(r['older'],r['recent'])>36/38 and r['paired_ci_vs_B'][0]>0]
    sim=rng.hypergeometric(6,32,6,(20000,40)).mean(1)
    save(OUT/'random_controls.json',dict(replicates=20000,confirmation_mean_95=np.quantile(sim,[.025,.975]),single_ticket_exact3=hg(38,6,6)[3],single_ticket_atleast3=hg(38,6,6)[3:].sum()))
    save(OUT/'ranking_coverage.json',covsummary);save(OUT/'construction_performance.json',perform);save(OUT/'v2_decision.json',dict(qualified_methods=qualifying,created=False if not qualifying else True,reason='No refinement passed the gate.' if not qualifying else 'Research challenger only; reused confirmation and post-outcome hypotheses require prospective validation.',no_next_lotto_ticket_generated=True))
    for path,digest in manifest.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest
    save(OUT/'forensic_summary.json',dict(tracks=tracks,winning_ranks=[r for r in rankings if r['number'] in truth],coverage=coverage,qualifying_refinements=len(qualifying),score_reconstruction_matches_stored=True,v1_files_unchanged=True,ranking_limit='Full final ranks and tie-break order were not persisted. Scores reconstructed from frozen data/code and reconciled; tied intervals reported. F_structure and final no-edge selection have no number ranking.'))
    print(json.dumps(clean(dict(tracks=tracks[:3]+tracks[-2:],winning_ranks=[r for r in rankings if r['number'] in truth],qualifiers=qualifying)),indent=2))
if __name__=='__main__':run()
