"""Super Lotto #1755 forensic (research only). Super Lotto data/code only. Outputs results/super_lotto/forensic_1755/."""
import sys,json,math,itertools,hashlib,subprocess,csv
from pathlib import Path
from collections import Counter
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts/research'))
import super_lotto as sl,super_history as S,super_p0 as P
from common import save,hg
V=R/'results/super_lotto';D=V/'draw1755';O=V/'forensic_1755';O.mkdir(exist_ok=True)
J=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *a:subprocess.run(['git',*a],cwd=R,capture_output=True,text=True,check=True).stdout.strip()
WIN=[3,11,15,21,33];WSB=1;NS=[5,8,10,12,15,18,20,25]
pred=J(V/'prospective/prediction_1755.json');pf=J(D/'p0/p0_frozen.json');pr0=J(D/'p0/p0_result.json');rc=J(V/'random_control_1755/random_control_frozen.json')
def okh(p,h):
    b=(R/p.replace('\\','/')).read_bytes();return 'exact' if hashlib.sha256(b).hexdigest()==h else ('LF_to_CRLF' if hashlib.sha256(b.replace(b'\n',b'\r\n')).hexdigest()==h else 'DIFFERS')
# ------------------------------------------------ 1. verification
cf=J(D/'candidate-freeze.json');att=J(D/'jev-attempt.json');rcp=J(D/'jev_receipt.json')
led=[json.loads(l) for l in (V/'prospective/ledger.jsonl').read_text().splitlines() if l.strip()]
node=subprocess.run(['node','-e',"const fs=require('fs'),c=require('crypto');console.log(c.createHash('sha256').update(JSON.stringify(JSON.parse(fs.readFileSync(process.argv[1],'utf8')))).digest('hex'))",str(D/'jev_request.json')],capture_output=True,text=True).stdout.strip()
first=lambda p:git('log','--diff-filter=A','--format=%h %cI','--',p).splitlines()[-1]
ver=dict(candidate_freeze={n:okh(f'results/super_lotto/draw1755/{n}',h) for n,h in cf['hashes'].items()},
  prediction_embedded=dict(Counter(okh(p,h) for p,h in pred['hashes'].items())),prediction_mismatches=[p for p,h in pred['hashes'].items() if okh(p,h)=='DIFFERS'],
  p0_frozen_hashes={p:okh(p if '/' in p else f'results/super_lotto/draw1755/p0/{p}',h) for p,h in pf['hashes'].items()},
  jev=dict(state=rcp['state_file_sha256']==sha(D/'jev_state.json'),request_compact=rcp['request_sha256']==node,single_attempt=att['http_attempts']==1 and att['retries_disabled']),
  ledger={e.get('track') or e['event']:dict(sha_ok=okh(e['path'] if '/' in e['path'] else 'results/super_lotto/prospective/'+e['path'],e['sha256'])) for e in led if e.get('target_draw_id')==1755 and 'sha256' in e},
  v1_ticket_in_pool=[c for c in J(D/'candidates.json') if c['id']==pred['selection']['candidate_id']][0]['main']==pred['selection']['main'],
  p0_ticket1_equals_v1=pf['ticket_1_v1']['mains']==sorted(pred['selection']['main']) and pf['ticket_1_v1']['super_ball']==pred['selection']['super_ball'],
  chronology_utc=dict(pool_frozen=cf['frozen_utc'],jev_attempt=att['started_utc'],jev_receipt=rcp['created_utc'],v1_frozen=pred['created_utc'],p0_frozen=pf['created_utc'],random_control=rc['created_utc'],scheduled_draw='2026-09-30T01:30:00Z'),
  commits=dict(pool=first('results/super_lotto/draw1755/candidates.json'),tickets=first('results/super_lotto/prospective/prediction_1755.json'),p0=first('results/super_lotto/draw1755/p0/p0_frozen.json'),post_freeze=first('results/super_lotto/draw1755/p0_jev_audit/audit_response.json')),
  tickets_unchanged_after_freeze_commit=git('diff','--name-only','ef94b7b','HEAD','--','results/super_lotto/prospective/prediction_1755.json','results/super_lotto/draw1755/p0/p0_frozen.json','results/super_lotto/draw1755/candidates.json')=='')
ver['frozen_before_draw']=max(pred['created_utc'],pf['created_utc'])<'2026-09-30T01:30'
ver['ALL_PASS']=bool(all(v in ('exact','LF_to_CRLF') for v in ver['candidate_freeze'].values()) and all(v=='exact' for v in ver['p0_frozen_hashes'].values()) and all(ver['jev'].values()) and all(x['sha_ok']=='exact' for x in ver['ledger'].values()) and ver['v1_ticket_in_pool'] and ver['p0_ticket1_equals_v1'] and ver['tickets_unchanged_after_freeze_commit'] and ver['frozen_before_draw'] and not [p for p in ver['prediction_mismatches'] if 'super_jev.mjs' not in p])
save(O/'verification.json',ver)
# ------------------------------------------------ 2. pool scoring
cands=J(D/'candidates.json');an=J(D/'jev_response.json')['answers'];pr=an['overall']['probabilities']
jr=lambda c:dict(best=1+sum(v>pr[c] for v in pr.values()),worst=sum(v>=pr[c] for v in pr.values()))
pool=[dict(id=c['id'],main=c['main'],super_ball=c['super_ball'],generator=c['main_generator'],sb_generator=c['SB_generator'],main_matches=len(set(c['main'])&set(WIN)),matched=sorted(set(c['main'])&set(WIN)),
           sb_hit=c['super_ball']==WSB,jev_choice=pr[c['id']],jev_rank=jr(c['id']),sensitivity=dict(rank_range=c['sensitivity_rank_range'],top5_fraction=c['sensitivity_top5_fraction']),
           evidence=dict(model_agreement=c['model_agreement_count'],ensemble_score=c['ensemble_score'],qualified=c['qualified_models'])) for c in cands]
md=Counter(x['main_matches'] for x in pool);best=max(x['main_matches'] for x in pool);pm=hg(35,5,5)
pool_summary=dict(main_match_distribution={k:md.get(k,0) for k in range(6)},best=best,best_candidates=[x['id'] for x in pool if x['main_matches']==best],v1_selected=pred['selection']['candidate_id'],
  v1_matches=len(set(pred['selection']['main'])&set(WIN)),jev_preferred=an['overall']['choice'],jev_preferred_matches=[x['main_matches'] for x in pool if x['id']==an['overall']['choice']][0],
  any_sb1=any(x['sb_hit'] for x in pool),pool_super_balls=sorted({x['super_ball'] for x in pool}),reached={k:any(x['main_matches']>=k for x in pool) for k in [2,3,4,5]},
  random_reference=dict(expected_candidates_ge2=float(20*pm[2:].sum()),p_any_of_20_independent_ge2=float(1-(1-pm[2:].sum())**20)),
  jev_choice_vs_matches_spearman=float(np.corrcoef(np.argsort(np.argsort([x['jev_choice'] for x in pool])),np.argsort(np.argsort([x['main_matches'] for x in pool])))[0,1]))
save(O/'pool_scores.json',dict(summary=pool_summary,candidates=pool))
# ------------------------------------------------ 3/4. discovery failure and Top-N coverage
cr=J(D/'complete_rankings.json');feat={int(r['number']):r for r in csv.DictReader(open(D/'main_features.csv',encoding='utf-8-sig'))}
POOL=pr0['pool'];order=pr0['main_order'];EQ={int(k):v for k,v in pr0['EQ'].items()};rel=J(V/'p0_protocol/reliability.json')
records,d,sb,ids=S.load(D/'draws.json');assert ids[-1]==1754
o=S.origin(d,sb,ids,len(d));Sx,inf=P.fam_scores(o)
# alternative orderings for the shrinkage question (diagnostic only)
zraw={m:max(0.,rel['main'][m]['z']) if 'z' in rel['main'][m] else 0. for m in P.MAIN}
unshr=np.array([zraw[m] for m in P.MAIN])@Sx;ord_unshr=sorted(range(35),key=lambda i:(-unshr[i],-Sx[[j for j in range(5) if inf[j]]].mean(0)[i],i));ord_unshr=[i+1 for i in ord_unshr]
def mrank(m,n):
    e=cr['main'][m]
    if not e.get('applicable'):return None
    x=[r for r in e['numbers'] if r['number']==n][0];return dict(score=x['score'],rank=x['rank'],tie=[x['tie_min'],x['tie_max']],informative=e['informative'])
INF=['A_long','B_recent','C_gap','D_trend']
def ev(n):
    f=feat[n];r={m:mrank(m,n) for m in sl.MN}
    sup=[m for m in INF if r[m]['rank']<=12];p0r=order.index(n)+1
    return dict(models=r,features=dict(long_run_count=f['count'],expected=f['expected'],ew_rate=f['ew_rate'],last30=f['last30'],last20=f['last20'],last10=f['last10'],current_gap=f['current_gap'],gap_percentile=f['gap_percentile'],trend=f['trend']),
                pair_partners='none: E_pairs had no Holm-retained pair (flat)',ensemble='G proxy flat (V1 learned main weight 1.0 on flat E_pairs)',P0_rank=p0r,P0_EQ=EQ[n],unshrunk_rank=ord_unshr.index(n)+1,
                answers=dict(A_narrowly_outside_top12=13<=p0r<=15,B_deeply_ranked=p0r>20,C_supporting_models_top12=sup,D_suppressed_by_shrinkage=ord_unshr.index(n)+1<=12<p0r,
                             E_excluded_because_weights_zero='ordering is the equal-weight convention; '+('a single model had it in its Top 12 but the average did not' if sup and p0r>12 else 'no informative model had it in its Top 12' if not sup else 'inside Top 12'),
                             F_in_top={N:p0r<=N for N in [15,18,20]}))
winners={n:ev(n) for n in WIN};poolev={n:ev(n) for n in POOL}
def cov(rank_of,N):return len([n for n in WIN if rank_of(n)<=N])
def tie_cov(m,N):
    e=cr['main'][m];sc={r['number']:r['score'] for r in e['numbers']};v=sorted(sc.values(),reverse=True)[N-1]
    inside=[i for i in sc if sc[i]>v+1e-12];tied=[i for i in sc if abs(sc[i]-v)<=1e-12];slots=N-len(inside);dw=len(set(inside)&set(WIN));tw=len(set(tied)&set(WIN))
    return [dw+max(0,slots-(len(tied)-tw)),dw+min(slots,tw)]
coverage={}
for m in INF+['H_random']:
    coverage[m]={N:dict(point=cov(lambda n:cr['main'][m]['order'].index(n)+1,N),tie_range=tie_cov(m,N)) for N in NS}
coverage['P0_order']={N:dict(point=cov(lambda n:order.index(n)+1,N)) for N in NS}
# historical P0 ordering capture (P0 historical replay, targets 1652-1753) and prospective/shadow
hrows=J(V/'p0_protocol/historical_origins.json')['rows']
hist_p0={N:float(np.mean([len(set(r['order'][:N])&set(r['winners'])) for r in hrows])) for N in NS}
topn=dict(observed=coverage,random_expected={N:5*N/35 for N in NS},historical_P0_mean_capture_1652_1753=hist_p0,
          p_capture_le_observed_random={N:float(hg(35,5,N)[:coverage['P0_order'][N]['point']+1].sum()) for N in NS})
save(O/'discovery_evidence.json',dict(winners=winners,pool_numbers=poolev,pool=POOL,p0_order=order,unshrunk_diagnostic_order=ord_unshr,
     note='P0 credibilities were all 0, so the P0 order is the declared equal-weight convention (EQ). The unshrunk order uses the raw positive design-cutoff AP z of each family (diagnostic only, not a protocol).',topN=topn))
# ------------------------------------------------ 5. construction diagnosis
ch=[pf['ticket_2']['mains'],pf['ticket_3']['mains']];v1m=sorted(pred['selection']['main'])
inpool=sorted(set(POOL)&set(WIN));covered=sorted(set(ch[0])|set(ch[1]))
caps=[];eff=[]
for r in hrows:
    b=r['byK']['12'];pool12=set(r['order'][:12]);w=set(r['winners']);c=len(pool12&w);cov2=set(b['mains'][1])|set(b['mains'][2])
    caps.append(c);eff.append((c,len(cov2&w),len(cov2&pool12)))
tot_in=sum(e[0] for e in eff);tot_ch=sum(e[1] for e in eff);mean_cov=np.mean([e[2] for e in eff])
sim=[];allp=list(itertools.combinations(POOL,5))
for wset in allp:
    m=[len(set(t)&set(wset)) for t in ch];sim.append((max(m),sum(m)))
sb_=np.array(sim)
construction=dict(winners_in_pool=inpool,challengers_cover_pool_numbers=len(set(covered)&set(POOL)),challengers_captured_in_pool_winners=sorted(set(covered)&set(WIN)),
  historical_efficiency=dict(winners_in_pool_total=tot_in,captured_by_challengers=tot_ch,ratio=tot_ch/tot_in if tot_in else None,mean_pool_numbers_covered_by_challengers=float(mean_cov),expected_ratio_if_blind=float(mean_cov/12)),
  capability_if_all_winners_in_pool=dict(method='all 792 equally likely 5-subsets of the frozen Top-12 pool as hypothetical winner sets, scored against the frozen challenger tickets (no ticket constructed from the outcome)',
     p_best_ge2=float(np.mean(sb_[:,0]>=2)),p_best_ge3=float(np.mean(sb_[:,0]>=3)),p_best_ge4=float(np.mean(sb_[:,0]>=4)),mean_challenger_total=float(sb_[:,1].mean())),
  p_capture_le1_random_top12=float(hg(35,5,12)[:2].sum()),
  classification='D (ordinary random variation) with a discovery shortfall: the Top-12 pool captured 1 winner (random expectation 1.71; P(<=1) = %.2f). Construction captured the only in-pool winner (11). With every credibility 0 the construction is coverage-driven and cannot concentrate winners beyond chance.'%float(hg(35,5,12)[:2].sum()))
save(O/'construction_diagnosis.json',construction)
# ------------------------------------------------ 6. Super Ball forensic
sbr={}
for m,e in cr['super_ball'].items():
    if e.get('order') is None:sbr[m]=dict(random_control=True,selected=e['selected']);continue
    sbr[m]=dict(informative=e['informative'],selected=e['selected'],**{f'SB{b}':dict(rank=[r for r in e['numbers'] if r['number']==b][0]['rank'],tie=[[r for r in e['numbers'] if r['number']==b][0]['tie_min'],[r for r in e['numbers'] if r['number']==b][0]['tie_max']],score=[r for r in e['numbers'] if r['number']==b][0]['score']) for b in [1,2,3,7]})
sbf=J(D/'super_ball_features.csv') if False else list(csv.DictReader(open(D/'super_ball_features.csv',encoding='utf-8-sig')))
p0sb=pr0['sb_order'];ev_p=J(V/'p0_protocol/historical_evaluation.json')['sb_rule_comparison']
sb_forensic=dict(actual=WSB,playable=[pred['selection']['super_ball'],pf['ticket_2']['super_ball'],pf['ticket_3']['super_ball']],models=sbr,sb1_features=[r for r in sbf if int(r['number'])==1],
  sb1_in_v1_pool=WSB in pool_summary['pool_super_balls'],v1_pool_super_balls=pool_summary['pool_super_balls'],
  sb1_structurally_excluded_by_v1=dict(answer=all(sbr[m].get('selected')!=WSB for m in sbr),reason='V1 assigns each candidate the single top pick of one of the 7 SB models (cyclic); SB1 was no model\'s top pick, so no V1 candidate could carry it'),
  p0_sb_order=p0sb,sb1_p0_rank=p0sb.index(WSB)+1,
  excluded_by_p0_rule=dict(answer=True,reason='rule C gives the challengers the top-2 SBs of the P0 order distinct from V1 SB2 (SB3, SB7); SB1 was 7th, so even 3-ticket distinct coverage reaches only the top 3 SBs. SB1 was not excluded by diversification itself (diversification widened coverage to 3 distinct SBs); it was outside the coverage the 3-ticket budget allows.'),
  historical_rule_comparison=ev_p,p_miss_three_distinct=0.7,p_miss_single_sb=0.9,
  sb_history=dict(**{'1753':dict(actual=3,v1_sb=2,in_v1_pool=False),'1754':dict(actual=8,v1_sb=2,in_v1_pool=False),'1755':dict(actual=1,v1_sb=2,in_v1_pool=False,p0_sbs=[3,7])}),
  note='n = 3 draws: SB misses are expected (V1 single SB misses with probability 0.9 each; P(0/3) = 0.729). No rule is inferred.')
save(O/'super_ball_forensic.json',sb_forensic)
# ------------------------------------------------ 7. combined prospective record
v1=[dict(draw=1753,main=1,sb=0),dict(draw=1754,main=0,sb=0),dict(draw=1755,main=0,sb=0)]
def conv_le(obs,n):
    p=np.array([1.])
    for _ in range(n):p=np.convolve(p,pm)
    return float(p[:obs+1].sum()),float(p[obs:].sum())
def cp(k,n,a=.05):
    from math import comb
    cdf=lambda p,k:sum(comb(n,j)*p**j*(1-p)**(n-j) for j in range(k+1))
    def bis(f,dec=False):
        lo,hi=0.,1.
        for _ in range(80):
            mid=(lo+hi)/2;v=f(mid)
            if (v>0)!=dec:hi=mid
            else:lo=mid
        return (lo+hi)/2
    return [0. if k==0 else bis(lambda p:1-cdf(p,k-1)-a/2),1. if k==n else bis(lambda p:cdf(p,k)-a/2,dec=True)]
tot=sum(x['main'] for x in v1);lo,hi=conv_le(tot,3)
p0_1755=dict(tickets=[[0,0],[1,0],[0,0]],best_main=1,total_main=1,any_sb=0)
record=dict(v1=v1,v1_summary=dict(n=3,mean_main=tot/3,expected=5/7,p_total_le_observed=lo,p_total_ge_observed=hi,sb_hits=0,sb_rate_ci95=cp(0,3),p_zero_sb_in_3=0.729,ge2_rate=0.,ge2_ci95=cp(0,3),p_ticket_ge2=float(pm[2:].sum()),p_no_ge2_in_3=float((1-pm[2:].sum())**3)),
  p0_prospective_1755=dict(portfolio=p0_1755,expected_total_main=3*5/7,p_portfolio_best_ge1_random='~%.2f'%(1-(pm[0])**3),note='one prospective P0 draw; the #1754 shadow is not prospective evidence'),
  shadow_1754=dict(best_main=1,total_main=2,any_sb=False),
  conclusion='V1 is below the random mean so far (1 match in 15 main numbers vs 2.14 expected; P(total <= 1) = %.3f), which is not unusual for n = 3 and is no evidence of either edge or defect.'%lo)
save(O/'prospective_record.json',record)
print(json.dumps(dict(ver=ver['ALL_PASS'],verdetail={k:ver[k] for k in ['prediction_embedded','prediction_mismatches','jev','commits']},pool=pool_summary,winners={n:dict(p0=w['P0_rank'],unshr=w['unshrunk_rank'],sup=w['answers']['C_supporting_models_top12'],ranks={m:w['models'][m]['rank'] for m in INF+['H_random']}) for n,w in winners.items()},
      topN={m:{N:v['point'] for N,v in c.items()} for m,c in coverage.items()},hist_p0=hist_p0,construction={k:construction[k] for k in ['winners_in_pool','challengers_captured_in_pool_winners','historical_efficiency','capability_if_all_winners_in_pool','p_capture_le1_random_top12']},
      sb={m:{k:v for k,v in x.items() if k.startswith('SB') or k=='selected'} for m,x in sbr.items()},sb1_p0_rank=sb_forensic['sb1_p0_rank'],record=record['v1_summary']),indent=1,default=str))
