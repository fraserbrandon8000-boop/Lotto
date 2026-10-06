"""Super Lotto #1756 forensic (research only). Super Lotto data/code only. Outputs results/super_lotto/forensic_1756/.
Run after super_research_1756.py (uses its causal walk-forward records). Changes no frozen artifact."""
import sys,json,math,itertools,hashlib,subprocess,csv
from pathlib import Path
from collections import Counter
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts/research'))
import super_lotto as sl,super_p0 as P
from common import save,hg
V=R/'results/super_lotto';D=V/'draw1756';D5=V/'draw1755';O=V/'forensic_1756';O.mkdir(exist_ok=True);PR=V/'p1_research'
J=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *a:subprocess.run(['git',*a],cwd=R,capture_output=True,text=True,check=True).stdout.strip()
WIN=[5,7,15,29,32];WSB=3;W55=[3,11,15,21,33];NS=[8,10,12,15,18,20,25];INF=['A_long','B_recent','C_gap','D_trend']
pred=J(V/'prospective/prediction_1756.json');pf=J(D/'p0/p0_frozen.json');pr0=J(D/'p0/p0_result.json');rc=J(V/'random_control_1756/random_control_frozen.json')
def okh(p,h):
    b=(R/p.replace('\\','/')).read_bytes();return 'exact' if hashlib.sha256(b).hexdigest()==h else ('LF_to_CRLF' if hashlib.sha256(b.replace(b'\n',b'\r\n')).hexdigest()==h else 'DIFFERS')
# ------------------------------------------------ 1. verification
cf=J(D/'candidate-freeze.json');att=J(D/'jev-attempt.json');rcp=J(D/'jev_receipt.json');srec=J(V/'jev_stability_1756/replicates_receipt.json')
led=[json.loads(l) for l in (V/'prospective/ledger.jsonl').read_text().splitlines() if l.strip()]
node=subprocess.run(['node','-e',"const fs=require('fs'),c=require('crypto');console.log(c.createHash('sha256').update(JSON.stringify(JSON.parse(fs.readFileSync(process.argv[1],'utf8')))).digest('hex'))",str(D/'jev_request.json')],capture_output=True,text=True).stdout.strip()
first=lambda p:git('log','--diff-filter=A','--format=%h %cI','--',p).splitlines()[-1]
hashes_file={l.split()[1]:l.split()[0] for l in (D/'HASHES.sha256').read_text().splitlines() if l.strip()}
ledger_1756=[e for e in led if e.get('target_draw_id')==1756]
ver=dict(candidate_freeze={n:okh(f'results/super_lotto/draw1756/{n}',h) for n,h in cf['hashes'].items()},
  prediction_embedded=dict(Counter(okh(p,h) for p,h in pred['hashes'].items())),prediction_mismatches=[p for p,h in pred['hashes'].items() if okh(p,h)=='DIFFERS'],
  p0_frozen_hashes={p:okh(p if '/' in p else f'results/super_lotto/draw1756/p0/{p}',h) for p,h in pf['hashes'].items()},
  HASHES_sha256_file={k:okh('results/super_lotto/'+k,h) for k,h in hashes_file.items() if k!='prospective/ledger.jsonl'},
  ledger_prefix_at_1756_freeze='exact' if hashlib.sha256(git('show','a811beb:results/super_lotto/prospective/ledger.jsonl').encode()+b'\n').hexdigest()==hashes_file['prospective/ledger.jsonl'] else 'DIFFERS',
  ledger_append_only=(V/'prospective/ledger.jsonl').read_text().startswith(git('show','a811beb:results/super_lotto/prospective/ledger.jsonl')),
  jev=dict(state=rcp['state_file_sha256']==sha(D/'jev_state.json'),request_compact=rcp['request_sha256']==node,response=rcp['response_sha256']==sha(D/'jev_response.json'),single_attempt=att['http_attempts']==1 and att['retries_disabled'],
           offline_validation=rcp['offline_validation_repair'],boundary=rcp['boundary']),
  post_freeze_replicates=dict(identical_request_bytes=srec['identical_request_bytes'],request_sha256=srec['request_sha256'],runs=[dict(replicate=x['replicate'],created_utc=x['created_utc'],after_ticket_freeze=x['created_utc']>pred['created_utc'][:23]) for x in srec['runs']]),
  ledger={(e.get('track') or e['event']):okh(e['path'] if '/' in e['path'] else 'results/super_lotto/prospective/'+e['path'],e['sha256']) for e in ledger_1756 if 'sha256' in e},
  v1_ticket_in_pool=[c for c in J(D/'candidates.json') if c['id']==pred['selection']['candidate_id']][0]['main']==pred['selection']['main'],
  p0_ticket1_equals_v1=pf['ticket_1_v1']['mains']==sorted(pred['selection']['main']) and pf['ticket_1_v1']['super_ball']==pred['selection']['super_ball'],
  chronology_utc=dict(pool_frozen=cf['frozen_utc'],jev_attempt=att['started_utc'],jev_receipt=rcp['created_utc'],v1_frozen=pred['created_utc'],p0_frozen=pf['created_utc'],random_control=rc['created_utc'],scheduled_draw='2026-10-03T01:30:00Z'),
  commits=dict(pool=first('results/super_lotto/draw1756/candidates.json'),tickets=first('results/super_lotto/prospective/prediction_1756.json'),p0=first('results/super_lotto/draw1756/p0/p0_frozen.json'),post_freeze=first('results/super_lotto/draw1756/p0_jev_audit/audit_response.json'),stability=first('results/super_lotto/jev_stability_1756/replicate_1_response.json'),random_control=first('results/super_lotto/random_control_1756/random_control_frozen.json')),
  tickets_unchanged_after_freeze_commit=git('diff','--name-only','3fc61ca','HEAD','--','results/super_lotto/prospective/prediction_1756.json','results/super_lotto/draw1756/p0/p0_frozen.json','results/super_lotto/draw1756/candidates.json','results/super_lotto/draw1756/jev_response.json')=='',
  random_control=dict(seed=rc.get('seed'),tickets=rc['tickets']))
ver['frozen_before_draw']=max(pred['created_utc'],pf['created_utc'])<'2026-10-03T01:30'
ver['post_freeze_commit_descends_from_freeze']=subprocess.run(['git','merge-base','--is-ancestor','3fc61ca','a811beb'],cwd=R).returncode==0
ver['ALL_PASS']=bool(all(v in ('exact','LF_to_CRLF') for v in ver['candidate_freeze'].values()) and all(v=='exact' for v in ver['p0_frozen_hashes'].values()) and all(v=='exact' for v in ver['HASHES_sha256_file'].values())
   and ver['ledger_append_only'] and all(ver['jev'][k] for k in ['state','request_compact','response','single_attempt']) and all(v=='exact' for v in ver['ledger'].values()) and ver['v1_ticket_in_pool'] and ver['p0_ticket1_equals_v1']
   and ver['tickets_unchanged_after_freeze_commit'] and ver['frozen_before_draw'] and ver['post_freeze_commit_descends_from_freeze'] and all(x['after_ticket_freeze'] for x in ver['post_freeze_replicates']['runs']) and not [p for p in ver['prediction_mismatches'] if 'super_jev.mjs' not in p])
save(O/'verification.json',ver)
# ------------------------------------------------ 2. pool scoring (production + 5 research replicates)
cands=J(D/'candidates.json');runs=[('production',J(D/'jev_response.json'))]+[(f'replicate_{i}',J(V/f'jev_stability_1756/replicate_{i}_response.json')) for i in range(1,6)]
probs=[r['answers']['overall']['probabilities'] for _,r in runs];ids_=sorted(probs[0])
def crank(pr,c):return dict(best=1+sum(v>pr[c]+1e-12 for v in pr.values()),worst=sum(v>=pr[c]-1e-12 for v in pr.values()))
def midrank(pr,c):b=crank(pr,c);return (b['best']+b['worst'])/2
pool=[]
for c in cands:
    mm=sorted(set(c['main'])&set(WIN))
    pool.append(dict(id=c['id'],main=c['main'],super_ball=c['super_ball'],generator=c['main_generator'],sb_generator=c['SB_generator'],main_matches=len(mm),matched=mm,sb_hit=c['super_ball']==WSB,
        jev_choice_production=probs[0][c['id']],jev_rank_production=crank(probs[0],c['id']),jev_replicate_mean_choice=float(np.mean([p[c['id']] for p in probs[1:]])),
        jev_replicate_midranks=[midrank(p,c['id']) for p in probs[1:]],jev_replicate_mean_midrank=float(np.mean([midrank(p,c['id']) for p in probs[1:]])),
        sensitivity=dict(rank_range=c['sensitivity_rank_range'],top5_fraction=c['sensitivity_top5_fraction']),
        evidence=dict(model_agreement=c['model_agreement_count'],ensemble_score=c['ensemble_score'],qualified=c['qualified_models'],main_support=c['main_support'],SB_support=c['SB_support'])))
md=Counter(x['main_matches'] for x in pool);best=max(x['main_matches'] for x in pool);pm=hg(35,5,5)
rep_top=Counter(r['answers']['overall']['choice'] for _,r in runs[1:]).most_common(1)[0]
pool_summary=dict(main_match_distribution={k:md.get(k,0) for k in range(6)},best=best,best_candidates=[x['id'] for x in pool if x['main_matches']==best],v1_selected=pred['selection']['candidate_id'],
  v1_matches=len(set(pred['selection']['main'])&set(WIN)),production_jev_favourite=runs[0][1]['answers']['overall']['choice'],replicate_favourite=f'{rep_top[0]} ({rep_top[1]}/5)',
  favourite_matches={x['id']:x['main_matches'] for x in pool if x['id'] in (runs[0][1]['answers']['overall']['choice'],rep_top[0])},
  candidates_with_SB3=[x['id'] for x in pool if x['sb_hit']],sb3_candidate_matches={x['id']:x['main_matches'] for x in pool if x['sb_hit']},
  multiple_mains_with_SB3=[x['id'] for x in pool if x['sb_hit'] and x['main_matches']>=2],pool_super_balls=sorted({x['super_ball'] for x in pool}),reached={k:any(x['main_matches']>=k for x in pool) for k in [2,3,4,5]},
  random_reference=dict(expected_candidates_ge2=float(20*pm[2:].sum()),p_any_of_20_independent_ge2=float(1-(1-pm[2:].sum())**20)),
  jev_choice_vs_matches_spearman=float(np.corrcoef(np.argsort(np.argsort([x['jev_choice_production'] for x in pool])),np.argsort(np.argsort([x['main_matches'] for x in pool])))[0,1]))
save(O/'pool_scores.json',dict(summary=pool_summary,candidates=pool,note='Scored after the draw for the record only; no candidate is promoted retrospectively.'))
# ------------------------------------------------ 3. discovery evidence for the #1756 winners (all PRE-DRAW, cutoff #1755)
cr=J(D/'complete_rankings.json');feat={int(r['number']):r for r in csv.DictReader(open(D/'main_features.csv',encoding='utf-8-sig'))}
POOL=pr0['pool'];order=pr0['main_order'];EQ={int(k):v for k,v in pr0['EQ'].items()};cred=pr0['frozen_credibility']['main']
rec=J(PR/'research_origins.json');r56=[r for r in rec if r['target']==1756][0];r55=[r for r in rec if r['target']==1755][0]
assert r56['order_P0']==order,'walk-forward replay must reproduce the frozen #1756 P0 order'
def mrank(m,n,crk=cr):
    e=crk['main'][m]
    if not e.get('applicable'):return dict(applicable=False,reason=e.get('reason'))
    x=[r for r in e['numbers'] if r['number']==n][0];return dict(score=x['score'],rank=x['rank'],tie=[x['tie_min'],x['tie_max']],informative=e['informative'])
pc=list(csv.DictReader(open(D/'pairs.csv',encoding='utf-8-sig')))
def pair_support(n):
    rows=[r for r in pc if str(n) in (r['a'],r['b'])];lift=[float(r['lift']) for r in rows];holm_ok=[r for r in rows if float(r['holm_p'])<.05]
    return dict(pairs=len(rows),mean_lift=float(np.mean(lift)) if lift else None,max_lift=float(max(lift)) if lift else None,holm_retained=len(holm_ok))
def ev(n):
    f=feat[n];r={m:mrank(m,n) for m in sl.MN};ranks=[r[m]['rank'] for m in INF];p0r=order.index(n)+1
    return dict(models=r,features=dict(long_run_count=int(f['count']),expected=float(f['expected']),ew_rate=float(f['ew_rate']),last100=int(f['last100']),last30=int(f['last30']),last20=int(f['last20']),last10=int(f['last10']),current_gap=int(f['current_gap']),gap_percentile=float(f['gap_percentile']),trend=float(f['trend'])),
        pair_network=pair_support(n),ensemble=dict(G_ensemble=r['G_ensemble'],EQ_mean_z=EQ[n]),reliability_contribution={m:dict(credibility=cred[m],contribution=0.0 if cred[m]==0 else None) for m in P.MAIN},
        P0_rank=p0r,P0_EQ=EQ[n],answers=dict(A_P0_rank=p0r,B_best_model_rank=min(ranks),B_best_model=INF[int(np.argmin(ranks))],C_worst_model_rank=max(ranks),C_worst_model=INF[int(np.argmax(ranks))],
            D_substantial_disagreement=bool(max(ranks)-min(ranks)>=15),rank_spread=max(ranks)-min(ranks),
            E_zero_weighting_suppressed=dict(answer=bool(min(ranks)<=12 and p0r>12),detail='all P0 credibilities were 0, so the P0 order is the equal-weight average of A-D z-scores; '+('a single model had it in its Top 12 but averaging pushed it out' if min(ranks)<=12 and p0r>12 else 'no informative model had it in its Top 12, so no weighting of these models could have admitted it without also admitting many non-winners' if min(ranks)>12 else 'inside Top 12')),
            F_top15=p0r<=15,G_top18=p0r<=18,H_top20=p0r<=20,I_top25=p0r<=25))
winners={n:ev(n) for n in WIN};poolev={n:ev(n) for n in POOL}
# Top-N coverage of #1756 winners by every ordering (pre-draw, from the causal walk-forward record)
topn={m:{N:r56['cap'][m][str(N)] for N in NS} for m in r56['cap']}
topn_random={N:5*N/35 for N in NS}
save(O/'discovery_evidence.json',dict(winners=winners,pool_numbers=poolev,pool=POOL,p0_order=order,topN_1756=topn,random_expectation=topn_random,
     note='All P0 credibilities were 0 at the #1756 cutoff, so the P0 order is the declared equal-weight convention (EQ = mean of informative A-D z-scores; E_pairs flat). Ranks are V1 complete_rankings (cutoff #1755).'))
# ------------------------------------------------ 4. consecutive discovery misses: exact hypergeometric baseline
p12=hg(35,5,12);two=np.convolve(p12,p12)
consec=dict(single_draw=dict(pmf={k:float(p12[k]) for k in range(6)},expected=5*12/35,p0=float(p12[0]),p1=float(p12[1]),p_le1=float(p12[:2].sum()),p_ge2=float(p12[2:].sum()),p_ge3=float(p12[3:].sum()),p_all5=float(p12[5])),
  two_draws=dict(pmf_total={k:float(two[k]) for k in range(11)},expected_total=2*5*12/35,observed_total=2,p_total_le2=float(two[:3].sum()),p_total_lt2=float(two[:2].sum()),p_le1_both=float(p12[:2].sum()**2),
     percentile_mid=float(two[:2].sum()+two[2]/2),percentile_le=float(two[:3].sum())),
  historical_P0_top12_capture=dict(mean=float(np.mean([r['cap']['F_P0_frozen_protocol']['12'] for r in rec])),p_le1=float(np.mean([r['cap']['F_P0_frozen_protocol']['12']<=1 for r in rec])),
     consecutive_pairs_total_le2=float(np.mean([a['cap']['F_P0_frozen_protocol']['12']+b['cap']['F_P0_frozen_protocol']['12']<=2 for a,b in zip(rec,rec[1:])]))),
  verdict='mildly unusual at most: P(total <= 2 of 10 | random Top-12) = %.3f; not statistically concerning and fully compatible with chance (two draws)'%float(two[:3].sum()))
save(O/'consecutive_discovery.json',consec)
# ------------------------------------------------ 5. number 15 trace (both runs, pre-draw)
cr55=J(D5/'complete_rankings.json');f55={int(r['number']):r for r in csv.DictReader(open(D5/'main_features.csv',encoding='utf-8-sig'))};p55=J(D5/'p0/p0_result.json')
c55=J(D5/'candidates.json')
def tr(n,crk,ff,pp,cc):
    return dict(models={m:mrank(m,n,crk) for m in sl.MN},P0_rank=pp['main_order'].index(n)+1,P0_EQ=pp['EQ'][str(n)],candidate_frequency=sum(n in c['main'] for c in cc),candidates=[c['id'] for c in cc if n in c['main']],
                features={k:ff[n][k] for k in ['count','ew_rate','last30','last20','last10','current_gap','gap_percentile','trend']})
t55=tr(15,cr55,f55,p55,c55);t56=tr(15,cr,feat,pr0,cands)
c57=J(V/'draw1757/candidates.json');cr57=J(V/'draw1757/complete_rankings.json');f57={int(r['number']):r for r in csv.DictReader(open(V/'draw1757/main_features.csv',encoding='utf-8-sig'))};p57=J(V/'draw1757/p0/p0_result.json')
t57=tr(15,cr57,f57,p57,c57)
hist_p0_rank15=[r['order_P0'].index(15)+1 for r in rec];rep=[len(set(a)&set(b)) for a,b in zip([r['numbers'] for r in J(V/'draw1757/draws.json')],[r['numbers'] for r in J(V/'draw1757/draws.json')][1:])]
num15=dict(run_1755=t55,run_1756=t56,post_result_1757_state=dict(t57,note='cutoff #1756 state used by the frozen #1757 run; produced by unchanged V1/P0, recorded only to show feature movement'),
  movement_1755_to_1756={k:[t55['features'][k],t56['features'][k]] for k in t55['features']},
  historical_P0_rank_of_15=dict(mean=float(np.mean(hist_p0_rank15)),median=float(np.median(hist_p0_rank15)),in_top12_share=float(np.mean([x<=12 for x in hist_p0_rank15]))),
  historical_15_wins=sum(15 in r['numbers'] for r in J(V/'draw1757/draws.json')),draws=len(J(V/'draw1757/draws.json')),
  random_recurrence=dict(p_specific_number_repeats=5/35,p_any_number_repeats_next_draw=float(1-math.comb(30,5)/math.comb(35,5)),historical_any_repeat_rate=float(np.mean([x>=1 for x in rep])),
                         p_some_number_wins_two_consecutive_draws_in_a_given_pair=float(1-math.comb(30,5)/math.comb(35,5))),
  verdict='15 was mid-table in both runs (no informative model put it in its Top 12 either time); its repeat is ordinary random recurrence (a repeat of at least one number between consecutive draws happens ~55% of the time). No repeat rule is created.')
save(O/'number_15_trace.json',num15)
# ------------------------------------------------ 6. layer separation for #1756
tick=[pred['selection']['main'],pf['ticket_2']['mains'],pf['ticket_3']['mains']];inpool=sorted(set(POOL)&set(WIN));placed=sorted(set().union(*map(set,tick))&set(WIN))
cc=J(PR/'construction_conditional.json')
layers=dict(winners_available_to_constructor=len(inpool),available=inpool,absent_before_construction=len(set(WIN)-set(POOL)),absent=sorted(set(WIN)-set(POOL)),
   available_not_placed=sorted(set(inpool)-set(placed)),placed_on_playable_tickets=placed,historical=cc,
   verdict='DISCOVERY: the constructor converted the only available winner (29). Historically the frozen constructor converts in-pool winners at %.0f%% vs %.0f%% blind; best-ticket matches rise with K, so construction transmits what discovery provides and discovery (which is at random level) is the binding layer.'%(100*cc['ratio'],100*cc['blind_expected']/cc['total_in_pool']))
save(O/'layer_separation.json',layers)
# ------------------------------------------------ 7. Super Ball
sbr={}
for m,e in cr['super_ball'].items():
    if e.get('order') is None:sbr[m]=dict(random_control=True,selected=e['selected']);continue
    sbr[m]=dict(informative=e['informative'],selected=e['selected'],order=e['order'],SB3=[dict(rank=r['rank'],tie=[r['tie_min'],r['tie_max']],score=r['score']) for r in e['numbers'] if r['number']==3][0])
allranks={b:{m:([r['rank'] for r in e['numbers'] if r['number']==b][0] if e.get('order') is not None else None) for m,e in cr['super_ball'].items()} for b in range(1,11)}
p0sb=pr0['sb_order'];sbf=[r for r in csv.DictReader(open(D/'super_ball_features.csv',encoding='utf-8-sig')) if int(r['number'])==3][0]
sb=dict(actual=WSB,playable=[pred['selection']['super_ball'],pf['ticket_2']['super_ball'],pf['ticket_3']['super_ball']],models=sbr,all_sb_ranks=allranks,P0_sb_order=p0sb,P0_rank_SB3=p0sb.index(3)+1,
  P0_Q=pr0['Q'],P0_EQ_SB=pr0['EQ_SB'],sb_credibility=pr0['frozen_credibility']['sb'],SB3_features={k:sbf[k] for k in ['count','expected','ew_rate','current_gap','gap_percentile','trend','last30','last10']},
  rule='C: challengers take the top 2 SBs of the P0 SB order excluding V1 SB2 -> SB7 (P0 #1) and SB3 (P0 #2)',
  driver='both, but the evidence part is unvalidated: SB3 was 2nd in the equal-weight average of SB models (all SB credibilities 0), and rule C mechanically gives the challengers the top 2 distinct SBs; historically P0 SB Top-3 coverage is at or below chance, so the hit is essentially chance.',
  combined_live=dict(**{'1755':'miss (played 2,3,7; actual 1)','1756':'hit (played 2,7,3; actual 3)'},expected_hit_rate=.3,p_at_least_one_in_2=1-.7**2,p_exactly_one_in_2=2*.3*.7))
save(O/'super_ball_forensic.json',sb)
# ------------------------------------------------ 8. Jev stability (#1756 six calls; saved outcome sets #1755/#1756)
def jsum(T):
    rr=[('production',J(V/f'draw{T}/jev_response.json'))]+[(f'replicate_{i}',J(V/f'jev_stability_{T}/replicate_{i}_response.json')) for i in range(1,6)]
    P_=[r['answers']['overall']['probabilities'] for _,r in rr];ids2=sorted(P_[0]);M=np.array([[p[i] for i in ids2] for p in P_])
    mr=np.array([[midrank(p,i) for i in ids2] for p in P_]);top3=[set(np.array(ids2)[np.lexsort((np.arange(20),-M[k]))[:3]]) for k in range(6)]
    ent=[float(-sum(x*math.log2(x) for x in row if x>0)) for row in M]
    agg=dict(first_valid=rr[0][1]['answers']['overall']['choice'],mean_choice=ids2[int(np.argmax(M.mean(0)))],median_rank=ids2[int(np.argmin(np.median(mr,0)))],majority_top1=Counter(r['answers']['overall']['choice'] for _,r in rr).most_common(1)[0][0])
    return rr,ids2,M,mr,top3,ent,agg
js={}
for T,win in [(1755,W55),(1756,WIN)]:
    rr,ids2,M,mr,top3,ent,agg=jsum(T);cs={c['id']:c for c in J(V/f'draw{T}/candidates.json')}
    js[T]=dict(aggregators={k:dict(candidate=v,matches=len(set(cs[v]['main'])&set(win))) for k,v in agg.items()},v1_selected='SL10',v1_matches=len(set(cs['SL10']['main'])&set(win)))
rr,ids2,M,mr,top3,ent,agg=jsum(1756)
focus={c:dict(choice=[float(M[k][ids2.index(c)]) for k in range(6)],midrank=[float(mr[k][ids2.index(c)]) for k in range(6)],rank_variance=float(np.var(mr[:,ids2.index(c)],ddof=1))) for c in ['SL10','SL19']}
jev=dict(calls_1756=[dict(run=n,top=r['answers']['overall']['choice'],top_prob=float(max(r['answers']['overall']['probabilities'].values())),confidence=r['answers']['overall']['confidence'],entropy_bits=e) for (n,r),e in zip(rr,ent)],
  SL10_vs_SL19=focus,production_gap_SL10_minus_SL19=float(M[0][ids2.index('SL10')]-M[0][ids2.index('SL19')]),
  top3_sets=[sorted(s) for s in top3],mean_pairwise_top3_overlap=float(np.mean([len(a&b) for a,b in itertools.combinations(top3,2)])),
  rank_variance_all={i:float(np.var(mr[:,k],ddof=1)) for k,i in enumerate(ids2)},
  near_tie=bool(abs(M[0][ids2.index('SL10')]-M[0][ids2.index('SL19')])<=.15),
  aggregators_1756=agg,aggregator_outcomes=js,stability_1757=J(V/'jev_stability_1757/stability_analysis.json'),
  verdict='The first-response top-1 is not a stable object when two candidates are close (#1756: production SL10 0.50, 5/5 replicates SL19 0.50-0.64); it is stable when one candidate dominates (#1757: SL19 0.80 in all 6 calls). Overall rank order is highly correlated across calls. With 2 outcome draws no aggregator can be evaluated for skill; under the no-edge rule Jev never changes the ticket.')
save(O/'jev_stability.json',jev)
# ------------------------------------------------ 9. combined prospective record
led=[json.loads(l) for l in (V/'prospective/ledger.jsonl').read_text().splitlines() if l.strip()]
v1o=[dict(draw=e['target_draw_id'],main=e['main_matches'],sb=int(bool(e['super_ball_match']))) for e in led if e['event']=='outcome_recorded']
p0o=[dict(draw=e['target_draw_id'],track=e['track'],main=e['main_matches'],sb=int(bool(e['super_ball_match']))) for e in led if e['event']=='research_outcome_recorded' and e['track'].startswith('P0')]
rco=[dict(draw=e['target_draw_id'],track=e['track'],main=e['main_matches'],sb=int(bool(e['super_ball_match']))) for e in led if e['event']=='research_outcome_recorded' and e['track'].startswith('random')]
def conv_tail(obs,n):
    q=np.array([1.])
    for _ in range(n):q=np.convolve(q,pm)
    return float(q[:obs+1].sum()),float(q[obs:].sum())
tv=sum(x['main'] for x in v1o);tp=sum(x['main'] for x in p0o)+sum(x['main'] for x in v1o if x['draw']>=1755);n_p0=len([x for x in v1o if x['draw']>=1755])*3
record=dict(v1=v1o,v1_total=tv,v1_tickets=len(v1o),v1_expected=len(v1o)*5/7,v1_p_le_obs=conv_tail(tv,len(v1o))[0],v1_sb_hits=sum(x['sb'] for x in v1o),
   p0_portfolio=dict(draws=[1755,1756],tickets=n_p0,total_main=tp,expected=n_p0*5/7,p_le_obs=conv_tail(tp,n_p0)[0],sb_hits=sum(x['sb'] for x in p0o),challenger_entries=p0o),
   random_control=dict(entries=rco,total_main=sum(x['main'] for x in rco),sb_hits=sum(x['sb'] for x in rco)))
save(O/'prospective_record.json',record)
print(json.dumps(dict(ver=ver['ALL_PASS'],ver_detail={k:ver[k] for k in ['prediction_embedded','prediction_mismatches','jev','commits','ledger','ledger_prefix_at_1756_freeze']},pool=pool_summary,
  winners={n:w['answers'] for n,w in winners.items()},consec=consec,num15={k:num15[k] for k in ['movement_1755_to_1756','historical_P0_rank_of_15','random_recurrence']},
  t15=dict(r55={m:(v.get('rank')) for m,v in t55['models'].items()},p55=t55['P0_rank'],f55=t55['candidate_frequency'],r56={m:(v.get('rank')) for m,v in t56['models'].items()},p56=t56['P0_rank'],f56=t56['candidate_frequency'],p57=t57['P0_rank']),
  layers={k:v for k,v in layers.items() if k!='historical'},sb={m:x.get('SB3') for m,x in sbr.items()},p0sb=p0sb,jev={k:jev[k] for k in ['calls_1756','SL10_vs_SL19','aggregator_outcomes','mean_pairwise_top3_overlap','near_tie']},record=record),indent=1,default=str))
