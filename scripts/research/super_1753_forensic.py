"""Read-only V1 forensics; append one outcome; write separate post-draw research."""
import json,csv,hashlib,math
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
import super_lotto as sl
from common import save,csvsave,clean,table,holm,hg,pmean,blockci
R=Path(__file__).resolve().parents[2];V=R/'results/super_lotto';O=V/'forensic_1753';O.mkdir(exist_ok=True)
WIN={1,5,8,14,18};BALL=3
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def readcsv(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rankspan(x,j):return [1+int(np.sum(x>x[j]+1e-12)),int(np.sum(x>=x[j]-1e-12))]
def ranks(x):
    x=np.asarray(x);return np.array([(np.sum(x<v)+1+np.sum(x<=v))/2 for v in x])
def corr(x,y):return float(np.corrcoef(ranks(x),ranks(y))[0,1])
def binomtail(n,k,p):return float(sl.binomial(n,p)[k:].sum())
def pct(x):return f'{100*x:.2f}%'
def fmt(x):return f'{x:.3f}'
def ns(x):return ', '.join(f'{n:02}' for n in x) or '—'

protocol='Post-outcome forensic research for #1753; original V1 inputs are read-only. Winner/rank comparison uses frozen exact main orders and scores. SB orders were not saved: sort saved SB scores using original seed and target-specific jitter; reconcile saved argmax predictions. No #1753 input enters fitting. Recheck historical coverage from the saved 126 walk-forward predictions through #1752, including exact binomial tails for coverage events >=3,>=4,=5 with Holm correction across all model/pool/threshold tests. Reuse all 44 predeclared construction tests and eleven pre-draw sensitivity variants, without choosing favorable settings. Two new finite hypotheses address inactive ensemble components: (1) remove zero-variance main candidate objectives and renormalize existing training-only weights, equal active fallback if no weight remains; (2) same operation on SB score vectors. Use original 512 candidate pools, seed, prior-data weights and 40-draw confirmation split, evaluate all/development/confirmation, exact null tests and 5-draw block CIs. Holm across these two new hypotheses; require corrected p<.05, CI lower>random mean and both halves>random, plus positive paired improvement CI over V1 ensemble before proposing V2. #1753 is descriptive only; confirmation is reused research, not new validation. No new future tickets. Outcome ordering is main matches descending then SB match, tie intervals preserved; not a monetary payout ranking. Jev correlation is descriptive over one dependent candidate set; simulate whole uniform draws for context rather than pretend 20 tickets are independent trials.'
if not (O/'PROTOCOL.txt').exists():(O/'PROTOCOL.txt').write_text(protocol,encoding='utf-8')
frozen=V/'prospective/prediction_1753.json';f=load(frozen);fit=f['full_predraw_fit_and_rankings'];cs=load(V/'candidates.json');jev=f['jev_response'];probs=jev['answers']['overall']['probabilities'];ledger=V/'prospective/ledger.jsonl'
assert f['selection']==dict(candidate_id='SL10',main=[1,22,32,34,35],super_ball=2)
assert all(digest(R/p)==h for p,h in f['hashes'].items())
entries=[json.loads(s) for s in ledger.read_text().splitlines() if s.strip()];event=next(r for r in entries if r['event']=='prediction_frozen' and r['target_draw_id']==1753);assert digest(frozen)==event['sha256']
# Manifest all existing V1 artifacts without copying or altering them.
protected=[p for p in V.glob('*') if p.is_file() and not p.name.startswith('forensic_1753')]+[frozen]+[R/p for p in f['hashes']]
manifest={str(p.relative_to(R)):digest(p) for p in protected};save(O/'v1_preservation_manifest.json',dict(checked_utc=datetime.now(timezone.utc).isoformat(),files=manifest))
original_ledger=ledger.read_bytes()
outcome=dict(event='outcome_recorded',recorded_utc=datetime.now(timezone.utc).isoformat(),target_draw_id=1753,date='2026-09-22',winning_main=sorted(WIN),super_ball=BALL,source='Official result supplied by user in attached request, 2026-09-25',prediction_path=str(frozen.relative_to(R)),prediction_sha256=digest(frozen),frozen_selection=f['selection'],main_matches=1,matched_main=[1],super_ball_match=0)
old=[e for e in entries if e['event']=='outcome_recorded' and e['target_draw_id']==1753]
if old:assert all(old[0][k]==outcome[k] for k in ['winning_main','super_ball','frozen_selection','main_matches','super_ball_match'])
else:
    with ledger.open('a',encoding='utf-8') as h:h.write(json.dumps(outcome)+'\n')
assert ledger.read_bytes().startswith(original_ledger)
save(O/'outcome.json',outcome)
main_features={int(x['number']):x for x in readcsv(V/'main_features.csv')};sb_features={int(x['number']):x for x in readcsv(V/'super_ball_features.csv')}
orders={k:np.array(v)+1 for k,v in fit['rankings'].items()};scores={k:np.array(v) for k,v in fit['individual_scores'].items()};mainrows=[];coverage=[]
for n in sorted(WIN|{22,32,34,35}):
    e=dict(number=n,group='matched winner' if n==1 else 'missed winner' if n in WIN else 'selected miss',features=main_features[n],models={},candidate_memberships=[c['id'] for c in cs if n in c['main']],individual_sensitivity='Not saved; only complete-ticket sensitivity exists.')
    for m in sl.MN:
        if m in orders:e['models'][m]=dict(saved_rank=int(np.flatnonzero(orders[m]==n)[0])+1,score=float(scores[m][n-1]),score_tie_rank=rankspan(scores[m],n-1),informative=bool(np.std(scores[m])>1e-12))
        else:e['models'][m]=dict(saved_rank=None,score=0.0 if m=='E_pairs' else None,reason='No retained pair signal' if m=='E_pairs' else 'Combination-level structure objective; no individual rank')
    e['pair_network_score']=float(np.array(fit['pair_matrix'])[n-1].sum());mainrows.append(e)
for m in sl.MN:
    for k in [5,7,8,10,12,15,20]:
        winners=sorted(WIN&set(orders[m][:k])) if m in orders else None
        coverage.append(dict(model=m,pool=k,winners=winners,count=len(winners) if winners is not None else None,informative=m in scores and np.std(scores[m])>1e-12,random_mean=5*k/35))
save(O/'main_evidence.json',mainrows);csvsave(O/'draw_coverage.csv',coverage)
# Only saved score arrays and pre-existing tie-break formula, no new fitting.
ss=np.array(fit['sb_scores']);sw=np.array(fit['sb_weights']);sx=np.vstack([ss,sw@ss]);jitter=np.random.default_rng(sl.SEED+1753*67).random(10)*1e-10;sbrows=[]
for i,m in enumerate(sl.SN[:6]):
    order=np.argsort(-(sx[i]+jitter));assert int(order[0])==fit['sb_predictions'][i]
    for n in [2,3]:sbrows.append(dict(model=m,ball=n,derived_rank=int(np.flatnonzero(order==n-1)[0])+1,score_tie_rank=rankspan(sx[i],n-1),saved_score=float(sx[i,n-1]),informative=bool(np.std(sx[i])>1e-12),saved_model_prediction=fit['sb_predictions'][i]+1,features=sb_features[n],probability=None,provenance='Order derived from frozen scores and original deterministic tie-break; not an originally stored full SB order.'))
save(O/'super_ball_evidence.json',sbrows)
candidate=[]
for c in cs:
    hits=sorted(WIN&set(c['main']));candidate.append(dict(id=c['id'],main=c['main'],super_ball=c['super_ball'],main_matches=len(hits),matched_main=hits,SB_match=int(c['super_ball']==BALL),main_generator=c['main_generator'],SB_generator=c['SB_generator'],choice_probability=probs[c['id']],robustness=jev['answers'][c['id']+'_robustness']['score'],sensitivity_rank_range=c['sensitivity_rank_range'],sensitivity_top5_fraction=c['sensitivity_top5_fraction']))
for c in candidate:
    key=(c['main_matches'],c['SB_match']);c['outcome_rank_min']=1+sum((r['main_matches'],r['SB_match'])>key for r in candidate);c['outcome_rank_max']=sum((r['main_matches'],r['SB_match'])>=key for r in candidate)
save(O/'candidate_outcomes.json',candidate);csvsave(O/'candidate_outcomes.csv',candidate)
# Descriptive candidate-set correlation. Whole-draw simulation retains overlap.
xx=np.array([c['choice_probability'] for c in candidate]);yy=np.array([c['main_matches'] for c in candidate]);rho=corr(xx,yy);rng=np.random.default_rng(175320260925);null=sl.sample(rng,20000,35,5)+1;matrix=np.array([[int(n in c['main']) for n in range(1,36)] for c in candidate]);nullhits=matrix[:,null-1].sum(2).T;rx=ranks(xx);rx=rx-rx.mean();nullrho=[]
for row in nullhits:
    ry=ranks(row);ry-=ry.mean();den=np.linalg.norm(rx)*np.linalg.norm(ry);nullrho.append(float(rx@ry/den) if den else 0.)
nullrho=np.array(nullrho);jevstats=dict(spearman_choice_vs_main_matches=rho,null_whole_draw_replicates=20000,two_sided_mc_p=(1+np.sum(np.abs(nullrho)>=abs(rho)))/20001,weighted_main_matches=float(xx@yy),unweighted_main_matches=float(yy.mean()),best_main_matches=int(yy.max()),best_ids=[r['id'] for r in candidate if r['main_matches']==yy.max()],main_match_counts={str(k):int(np.sum(yy==k)) for k in range(6)},candidate_SB_values=sorted({c['super_ball'] for c in cs}),candidate_main_union=sorted({n for c in cs for n in c['main']}),winner_missing_from_all_candidates=sorted(WIN-{n for c in cs for n in c['main']}),no_candidate_correct_SB=True,interpretation='One correlated candidate set and one draw: descriptive, not evidence validating or invalidating Jev predictive skill.')
save(O/'jev_forensic.json',jevstats)
records=load(V/'draws.json');assert records[-1]['draw_id']==1752 and len(records)==176
wf=load(V/'walk_forward.json');cons=load(V/'construction_origins.json');hist=[]
for row in cons:
    assert row['draw_id']==records[row['index']]['draw_id']
    assert len(set(row['ticket']))==5 and min(row['ticket'])>=1 and max(row['ticket'])<=35
    assert row['hits']==len(set(row['ticket'])&set(records[row['index']]['numbers']))
for period in ['all','development','confirmation']:
    rr=[r for r in wf if period=='all' or r['period']==period]
    for m in sl.MN:
        sub=[r for r in rr if m in r['rankings']]
        if not sub:continue
        for k in [5,7,8,10,12,15,20]:
            y=[]
            for r in sub:
                truth=set(records[r['index']]['numbers']);assert r['training_cutoff']<r['draw_id']
                hit=len(truth&set(r['rankings'][m][:k]));assert hit==r['coverage'][m][str(k)];y.append(hit)
            y=np.array(y);pmf=hg(35,5,k);r=dict(period=period,model=m,pool=k,n=len(y),mean=float(y.mean()),median=float(np.median(y)),random_mean=5*k/35,mean_p=pmean(y,35,5,k),events={})
            for t in [3,4,5]:
                rate=float(pmf[t:].sum());ct=int(np.sum(y>=t));r['events'][str(t)]=dict(count=ct,rate=ct/len(y),random_rate=rate,p=binomtail(len(y),ct,rate))
            hist.append(r)
    sub=[r for r in hist if r['period']==period]
    for r,p in zip(sub,holm([r['mean_p'] for r in sub])):r['mean_holm_p']=p
    tests=[r['events'][str(t)] for r in sub for t in [3,4,5]]
    for r,p in zip(tests,holm([r['p'] for r in tests])):r['holm_p']=p
save(O/'historical_coverage.json',hist)
# Fixed two-hypothesis audit: removing inactive ensemble components.
d=np.array([r['numbers'] for r in records])-1;sb=np.array([r['super_ball'] for r in records])-1;a=sl.ind(d,35);b=sl.ind(sb[:,None],10);ref=[]
for row in wf:
    t=row['index'];target=row['draw_id'];aa=a[:t];bb=b[:t];s=sl.features(aa);ss=sl.features(bb);mat,*_=sl.pairmat(aa);st=sl.structures(d[:t]);mu=st.mean(0);sd=np.maximum(st.std(0),1);pool=sl.sample(np.random.default_rng(sl.SEED+target*101),512,35,5);v=sl.objective(pool,s,mat,mu,sd)
    def active_weights(weights,values):
        active=values.std(1)>1e-12;weights=np.array(weights)*active
        return weights/weights.sum() if weights.sum()>1e-12 else active/active.sum()
    mw=active_weights(row['main_weights'],v);chosen=pool[np.argmax(mw@v)]
    transitions=bb[:-1].T@bb[1:];last=sb[t-1];trials=int(bb[:-1,last].sum());ps=[sl.bp(trials,.1,x) for x in transitions[last]] if trials else [1]*10;tv=np.where(holm(ps)<.05,transitions[last]/max(1,trials)-.1,0);ss=np.vstack([ss,sl.z(tv)]);sw=active_weights(row['SB_weights'],ss);choice=int(np.argmax(sw@ss+np.random.default_rng(sl.SEED+target*67).random(10)*1e-10))
    # Reveal only after both predictions exist.
    ref.append(dict(draw_id=target,training_cutoff=row['training_cutoff'],period=row['period'],main_ticket=(chosen+1).tolist(),super_ball=choice+1,main_hits=int(a[t,chosen].sum()),SB_hits=int(choice==sb[t]),baseline_main_hits=row['main_hits'][6],baseline_SB_hits=row['SB_hits'][5],active_main_weights=mw,active_SB_weights=sw))
save(O/'refinement_origins.json',ref);refperf=[]
for period in ['all','development','confirmation']:
    rr=[r for r in ref if period=='all' or r['period']==period]
    for domain,NN,KK,base in [('main',35,5,5/7),('SB',10,1,.1)]:
        y=np.array([r[domain+'_hits'] for r in rr]);old=np.array([r['baseline_'+domain+'_hits'] for r in rr]);ci=blockci(y);diffci=blockci(y-old)
        refperf.append(dict(period=period,domain=domain,n=len(y),mean=float(y.mean()),rates=(np.bincount(y,minlength=KK+1)/len(y)),random_mean=base,p=pmean(y,NN,KK,KK),ci=ci,older=float(y[:len(y)//2].mean()),recent=float(y[len(y)//2:].mean()),paired_delta=float(np.mean(y-old)),paired_ci=diffci))
    sub=[r for r in refperf if r['period']==period]
    for r,p in zip(sub,holm([r['p'] for r in sub])):r['holm_p']=p;r['passes_gate']=bool(period=='confirmation' and p<.05 and r['ci'][0]>r['random_mean'] and min(r['older'],r['recent'])>r['random_mean'] and r['paired_ci'][0]>0)
save(O/'refinement_performance.json',refperf)
assert not any(r['passes_gate'] for r in refperf),'Positive refinement needs full V2 review, do not auto-dismiss'
assert all(digest(R/p)==h for p,h in manifest.items())
save(O/'verification.json',dict(v1_files_unchanged=True,prediction_sha256=digest(frozen),prediction_matches_original_ledger_hash=True,all_freeze_hashes_match=True,ledger_prior_bytes_preserved=True,no_1753_fitting=True,historical_origins=len(wf),saved_main_coverage_reconciled=True,SB_replay_argmax_reconciled=True,no_next_ticket_generated=True))
save(O/'v2_decision.json',dict(created=False,conclusion='No Super Lotto V2 is justified.',basis='No pre-existing construction/sensitivity gate or inactive-component refinement establishes a corrected advantage. Confirmation is reused, not fresh.'))
print(json.dumps(clean(dict(main_ranks={m:{n:int(np.flatnonzero(order==n)[0])+1 for n in sorted(WIN)} for m,order in orders.items()},super_ball_ranks=sbrows,jev=jevstats,refinement=refperf)),indent=2))
