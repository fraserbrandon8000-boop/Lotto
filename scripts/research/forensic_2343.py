"""Lotto #2343 forensic (research only; Lotto data only). Outputs results/lotto/forensic_2343/."""
import sys,json,csv,math,hashlib,subprocess,itertools
from pathlib import Path
from collections import Counter
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'));sys.path.insert(0,str(R/'scripts/research'))
import analyze as a,p0,v1_history as V
D=R/'results/lotto/draw2343';O=R/'results/lotto/forensic_2343';O.mkdir(exist_ok=True)
J=lambda p:json.loads(Path(p).read_text());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *x:subprocess.run(['git',*x],cwd=R,capture_output=True,text=True,check=True).stdout.strip()
WIN=[4,7,13,23,33,35];BONUS=38;PREV=[5,11,16,24,27,34];DRAW_UTC='2026-10-04T01:25:00'
def save(n,o):a.OUT=O;a.save(n,o)
fz=J(D/'frozen.json');pool=J(D/'pool_frozen_pre_jev.json');pf=J(D/'p0/p0_frozen.json');pr=J(D/'p0/p0_result.json');rcp=J(D/'jev_receipt.json');resp=J(D/'jev_response.json')
st=J(R/'results/lotto/jev_stability_2343/stability_analysis.json');rr=J(R/'results/lotto/jev_stability_2343/replicates_receipt.json')
# ---------------- 1. integrity
led=[json.loads(l) for l in (R/'results/lotto/prospective_ledger.jsonl').read_text().splitlines() if l.strip()]
node=subprocess.run(['node','-e',"const fs=require('fs'),c=require('crypto');console.log(c.createHash('sha256').update(JSON.stringify(JSON.parse(fs.readFileSync(process.argv[1],'utf8')))).digest('hex'))",str(D/'jev_request.json')],capture_output=True,text=True).stdout.strip()
first=lambda p:git('log','--diff-filter=A','--format=%h %cI','--',p).splitlines()[-1]
e=[x for x in led if x.get('target_draw')==2343]
ver=dict(frozen_embedded={p:('exact' if sha(R/p)==h else 'DIFFERS') for p,h in fz['hashes'].items()},pool_freeze={p:('exact' if sha(D/p)==h else 'DIFFERS') for p,h in pool['hashes'].items()},
  p0_frozen={p:('exact' if sha(R/p if '/' in p else D/'p0'/p)==h else 'DIFFERS') for p,h in pf['hashes'].items()},
  protocol_hash_matches=sha(R/'results/lotto/p0_protocol/PROTOCOL.json')==pr['protocol_sha256'],
  ledger=[dict(track=x.get('track','V1'),sha_ok=sha(R/x['path'].replace('\\','/'))==x['sha256']) for x in e],
  jev=dict(state=rcp['state_file_sha256']==sha(D/'jev_state.json'),request_compact=rcp['request_sha256']==node,model=resp['model'],answers=len(resp['answers'])),
  frozen_fields_match=dict(choice_prob=fz['jev_choice_probability']==resp['answers']['overall']['probabilities'][fz['candidate_id']],confidence=fz['jev_choice_confidence']==resp['answers']['overall']['confidence'],preferred=fz['jev_preferred_candidate']==resp['answers']['overall']['choice']),
  ticket_in_pool=[c for c in J(D/'candidates.json') if c['id']==fz['candidate_id']][0]['numbers']==fz['numbers'],p0_ticket1_is_v1=pf['ticket_1_v1']['numbers']==fz['numbers'],
  replicates_identical_request=rr['identical_request_bytes'] and rr['request_sha256']==rcp['request_sha256'],
  commits={k:first(p) for k,p in dict(pool='results/lotto/draw2343/pool_frozen_pre_jev.json',v1_ticket='results/lotto/draw2343/frozen.json',p0_tickets='results/lotto/draw2343/p0/p0_frozen.json',random_control='results/lotto/random_control_2343/random_control_frozen.json',p0_audit='results/lotto/draw2343/p0_jev_audit/audit_response.json',stability='results/lotto/jev_stability_2343/replicates_receipt.json').items()},
  timestamps=dict(pool_frozen=pool['frozen_utc'],jev_receipt=rcp['created_utc'],v1_frozen=fz['created_utc'],p0_frozen=pf['created_utc'],first_replicate=rr['runs'][0]['created_utc'],scheduled_draw=DRAW_UTC+'Z'),
  pool_files_unchanged_after_pool_commit=git('diff','--name-only','9c6b80c','HEAD','--','results/lotto/draw2343/candidates.json','results/lotto/draw2343/jev_state.json','results/lotto/draw2343/pool_frozen_pre_jev.json')=='',
  tickets_unchanged_after_freeze=git('diff','--name-only','d83d77b','HEAD','--','results/lotto/draw2343/frozen.json','results/lotto/draw2343/p0/p0_frozen.json')=='',
  v1_code_unchanged=git('diff','--name-only','ba7c5a3','HEAD','--','scripts/analyze.py','scripts/jev.mjs','scripts/finalize.py','PROTOCOL.md')=='')
ver['frozen_before_draw']=max(fz['created_utc'],pf['created_utc'])<DRAW_UTC;ver['replicates_after_freeze']=rr['runs'][0]['created_utc'].replace('Z','')>pf['created_utc'][:23]
flat=[*ver['frozen_embedded'].values(),*ver['pool_freeze'].values(),*ver['p0_frozen'].values()]
ver['ALL_PASS']=bool(all(v=='exact' for v in flat) and ver['protocol_hash_matches'] and all(x['sha_ok'] for x in ver['ledger']) and ver['jev']['state'] and ver['jev']['request_compact'] and all(ver['frozen_fields_match'].values()) and ver['ticket_in_pool'] and ver['p0_ticket1_is_v1'] and ver['replicates_identical_request'] and ver['pool_files_unchanged_after_pool_commit'] and ver['tickets_unchanged_after_freeze'] and ver['v1_code_unchanged'] and ver['frozen_before_draw'] and ver['replicates_after_freeze'])
save('verification.json',ver)
# ---------------- 2. pool scoring
cands=J(D/'candidates.json');pr_=resp['answers']['overall']['probabilities'];an=resp['answers']
jr=lambda c:None if c not in pr_ else dict(best=1+sum(v>pr_[c] for v in pr_.values()),worst=sum(v>=pr_[c] for v in pr_.values()))
poolrows=[]
for c in cands:
    m=sorted(set(c['numbers'])&set(WIN));el=len(set(c['numbers'])&set(PREV))<=2
    poolrows.append(dict(id=c['id'],numbers=c['numbers'],generator=c['generator'],eligible=el,matches=len(m),matched=m,jev_choice=pr_.get(c['id']),jev_rank=jr(c['id']),
        sensitivity=dict(top_quartile=c['sensitivity_top_quartile_fraction'],mean_rank=c['sensitivity_mean_rank']),evidence=dict(model_ranks=c['model_ranks'],contributing=c['contributing_models'],ensemble_rank=c['ensemble_rank'],agreement=c['model_agreement_count'])))
dist=Counter(x['matches'] for x in poolrows);best=max(x['matches'] for x in poolrows);PM=a.PMF
pool_summary=dict(match_distribution={k:dist.get(k,0) for k in range(7)},best=best,best_candidates=[x['id'] for x in poolrows if x['matches']==best],v1_selected=fz['candidate_id'],v1_matches=len(set(fz['numbers'])&set(WIN)),
  jev_preferred=an['overall']['choice'],jev_preferred_matches=[x['matches'] for x in poolrows if x['id']==an['overall']['choice']][0],reached={k:any(x['matches']>=k for x in poolrows) for k in [3,4,5,6]},
  random_reference=dict(p_any_of_20_ge3=float(1-(1-PM[3:].sum())**20)),jev_vs_matches_spearman=float(np.corrcoef(np.argsort(np.argsort([x['jev_choice'] for x in poolrows if x['eligible']])),np.argsort(np.argsort([x['matches'] for x in poolrows if x['eligible']])))[0,1]))
save('pool_scores.json',dict(summary=pool_summary,candidates=poolrows))
# ---------------- 3. exact pre-draw evidence
rk=J(D/'refreshed_rankings.json');stats={int(x['number']):x for x in csv.DictReader(open(D/'number_statistics.csv'))}
records,d=V.load(D/'draws.json');assert records[-1]['draw_id']==2342
ft=a.model_features(a.indicator(d));mat=ft[1];hsc=np.random.default_rng(a.SEED+2343*3037).random(38)
R_={n:dict(scores=np.array(v['scores']),order=list(v['order']),informative=v['informative']) for n,v in rk.items()};R_['H_random']=dict(scores=hsc,order=(np.argsort(-hsc)+1).tolist(),informative=True)
def tie(s,i):v=s[i-1];return [int(np.sum(s>v+1e-12))+1,int(np.sum(s>v+1e-12)+np.sum(np.abs(s-v)<=1e-12))]
order=pr['pool_order_full'];M=pr['discovery_M'];EQ=pr['discovery_EQ']
FAM4=['A_long','B_recent','C_gap','D_trend']
def ev(n):
    m={k:dict(score=float(v['scores'][n-1]),rank=v['order'].index(n)+1,tie=tie(v['scores'],n),informative=v['informative']) for k,v in R_.items()}
    s=stats[n]
    return dict(models=m,F_structure='no number-level ranking (whole-ticket objective)',features={k:s[k] for k in ['frequency','appearance_rate','ew_rate','last_30_count','last_20_count','last_10_count','current_gap','current_gap_percentile','trend_20_vs_previous40']},
                pair_partners=[int(j+1) for j in np.nonzero(mat[n-1])[0]],ensemble=dict(G_proxy_rank=m['G_marginal_proxy']['rank']),family_top12=[f for f in FAM4 if m[f]['rank']<=12],
                P0_rank=order.index(n)+1,P0_M=M[str(n)],P0_EQ=EQ[str(n)])
evid={n:ev(n) for n in WIN}
# ---------------- 4. P0 pool audit (frozen pool, not inferred from tickets)
W=J(R/'results/lotto/p0_protocol/PROTOCOL.json')['frozen_constants']['weight_detail']
S=ft[0];inf=[j for j in range(5) if np.std(S[j])>1e-12];EQv=S[inf].mean(0)
ord_eq=sorted(range(38),key=lambda i:(-EQv[i],i));ord_unh=sorted(range(38),key=lambda i:(-(sum(max(0,W[f]['d'])*S[j][i] for j,f in enumerate(p0.FAM))),-EQv[i],i))
pool_audit=dict(K=pr['K'],pool=pr['pool'],winners_inside=sorted(set(pr['pool'])&set(WIN)),winners_outside=sorted(set(WIN)-set(pr['pool'])),missed={})
for n in pool_audit['winners_outside']:
    r4={f:evid[n]['models'][f]['rank'] for f in FAM4}
    pool_audit['missed'][n]=dict(P0_rank=order.index(n)+1,highest_support=min(r4.items(),key=lambda x:x[1]),lowest_support=max(r4.items(),key=lambda x:x[1]),
        in_top={K:order.index(n)+1<=K for K in [18,20,25]},equal_weight_rank=ord_eq.index(n-1)+1,no_stability_factor_rank=ord_unh.index(n-1)+1,
        suppressed=bool(min(ord_eq.index(n-1),ord_unh.index(n-1))+1<=15<order.index(n)+1))
pool_audit['note']='Frozen weights: B_recent 0.0314, D_trend 0.0238 (A, C, E zero). Shrinkage scales all weights by the same factor (n=130 for every family), so it does not change the ordering; the ordering is driven by which families have positive evidence. equal_weight_rank uses the equal A-D(E) mean; no_stability_factor_rank drops the halves factor h.'
# ---------------- 6. two-layer diagnosis + counterfactual
port=[fz['numbers'],pf['ticket_2'],pf['ticket_3']];covered=set(pf['ticket_2'])|set(pf['ticket_3'])
inpool=sorted(set(pr['pool'])&set(WIN));reached=sorted(set().union(*map(set,port))&set(WIN))
cf=[]
for wset in itertools.combinations(pr['pool'],6):
    m=[len(set(t)&set(wset)) for t in port];cf.append((max(m),sum(m),len(set().union(*map(set,port))&set(wset))))
cf=np.array(cf)
two=dict(A_winners_in_pool=inpool,B_reached_portfolio=sorted(set(inpool)&set().union(*map(set,port))),C_lost_before_construction=sorted(set(WIN)-set(pr['pool'])),D_lost_during_construction=sorted(set(inpool)-set().union(*map(set,port))),
  portfolio_captured=reached,v1_numbers_in_pool=sorted(set(fz['numbers'])&set(pr['pool'])),challengers_cover_pool=len(covered&set(pr['pool'])),
  counterfactual_all_six_in_pool=dict(method='all 5,005 6-subsets of the frozen Top-15 pool as hypothetical winner sets, scored against the frozen portfolio (no ticket built from the outcome)',
    mean_best=float(cf[:,0].mean()),p_best_ge3=float(np.mean(cf[:,0]>=3)),p_best_ge4=float(np.mean(cf[:,0]>=4)),p_best_ge5=float(np.mean(cf[:,0]>=5)),mean_total=float(cf[:,1].mean()),mean_unique_winners_covered=float(cf[:,2].mean())),
  random_reference=dict(p_capture_le3_top15=float(sum(math.comb(6,k)*math.comb(32,15-k) for k in range(4))/math.comb(38,15)),expected_capture_top15=6*15/38))
save('two_layer_diagnosis.json',two)
# ---------------- 10. Jev follow-up
jev=dict(production_favourite=resp['answers']['overall']['choice'],replicate_favourites=[x['top_choice'] for x in st['runs'][1:]],top_choice_agreement=st['top_choice_agreement_replicates'],mean_spearman=st['mean_pairwise_spearman'],
  mean_top3_overlap=st['mean_top3_overlap'],max_prob_range=st['max_abs_prob_range'],confidence=st['confidence'],aggregated_favourite=st['aggregated_top'],would_aggregation_change_v1='NO (no-edge rule: Jev has no role in selection)',
  jev_preferred_outcome={resp['answers']['overall']['choice']:[x for x in poolrows if x['id']==resp['answers']['overall']['choice']][0]['matches']},
  historical_aggregation_test=dict(feasible=False,reason='A historical first-valid vs 3/5-call aggregate comparison needs 3-5 Jev calls on each of ~110 reconstructed historical states (~550 calls at ~35k input tokens each). That is not a proportionate research cost, and Jev does not affect V1 selection under the no-edge rule. Prospective replicate data exist for #2342 only (and will for #2343); on #2342 first-valid and aggregate favourites were identical (C03, which scored 2/6 on #2342: 13 and 33).'))
save('jev_followup.json',jev)
# ---------------- 11. combined prospective record
def conv_tail(obs,n):
    q=np.array([1.])
    for _ in range(n):q=np.convolve(q,PM)
    return float(q[obs:].sum()),float(q[:obs+1].sum())
v1=[('2339',3),('2340',0),('2341',3),('2342',0),('2343',len(set(fz['numbers'])&set(WIN)))];tot=sum(x for _,x in v1);ge,le=conv_tail(tot,len(v1))
p3=float(PM[3:].sum())
pmc=np.random.default_rng(20261007);Dm=np.zeros((200000,38),bool);Dm[np.arange(200000)[:,None],np.argsort(pmc.random((200000,38)),1)[:,:6]]=True
Tm=np.zeros((3,38),int)
for k,t in enumerate(port):Tm[k,np.array(t)-1]=1
mm=Dm.astype(int)@Tm.T
pm2343=[len(set(t)&set(WIN)) for t in port]
record=dict(v1=v1,v1_tickets={'2339':[1,4,13,14,24,38],'2340':[5,11,16,24,27,34],'2341':[1,4,13,14,24,38],'2342':[5,11,16,24,27,34],'2343':fz['numbers']},
  v1_summary=dict(n=len(v1),total=tot,mean=tot/len(v1),expected=36/38,p_total_ge=ge,p_total_le=le,ge3_events=sum(x>=3 for _,x in v1),p_ge3_ge2_of_n=float(sum(math.comb(len(v1),k)*p3**k*(1-p3)**(len(v1)-k) for k in range(2,len(v1)+1))),
     note='01 04 13 14 24 38 played three times (3, 3, 2 matches); 05 11 16 24 27 34 twice (0, 0). Five plays of two tickets.'),
  p0_live={'2342':dict(per_ticket=[0,1,2],best=2,total=3),'2343':dict(per_ticket=pm2343,best=max(pm2343),total=sum(pm2343),p_best_ge_obs_null=float(np.mean(mm.max(1)>=max(pm2343))),p_total_ge_obs_null=float(np.mean(mm.sum(1)>=sum(pm2343)))),'expected_total_per_draw':3*36/38},
  p0_shadow_2341=dict(best=3,total=4,note='shadow, not prospective'))
save('prospective_record.json',record)
print(json.dumps(dict(ver=ver['ALL_PASS'],commits=ver['commits'],pool=pool_summary,evid={n:dict(p0=e['P0_rank'],ranks={k:v['rank'] for k,v in e['models'].items()},fam=e['family_top12']) for n,e in evid.items()},
      audit=pool_audit,two={k:two[k] for k in ['A_winners_in_pool','B_reached_portfolio','C_lost_before_construction','D_lost_during_construction','counterfactual_all_six_in_pool','random_reference']},record=record['v1_summary'],p0live=record['p0_live']),indent=1,default=str))
save('winner_evidence.json',dict(cutoff=2342,target=2343,winners=WIN,bonus=BONUS,evidence=evid,pool_audit=pool_audit,
     flat=['E_pairs (no Holm-retained pair)','F_structure (no number-level ranking)'],note='Exact frozen pre-draw values (refreshed_rankings.json, number_statistics.csv, P0 p0_result.json). H = V1 walk H ranking definition for target 2343.'))
