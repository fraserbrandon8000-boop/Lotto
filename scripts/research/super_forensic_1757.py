"""Super Lotto #1757 forensic (research only; Super Lotto data only). Outputs results/super_lotto/forensic_1757/."""
import sys,json,math,hashlib,subprocess,csv
from pathlib import Path
from collections import Counter
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts/research'))
from common import save,hg
V=R/'results/super_lotto';D=V/'draw1757';O=V/'forensic_1757';O.mkdir(exist_ok=True)
J=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *a:subprocess.run(['git',*a],cwd=R,capture_output=True,text=True).stdout
WIN=[4,23,29,31,32];WSB=9;INF=['A_long','B_recent','C_gap','D_trend']
pred=J(V/'prospective/prediction_1757.json');pf=J(D/'p0/p0_frozen.json');pr0=J(D/'p0/p0_result.json');rc=J(V/'random_control_1757/random_control_frozen.json')
cf=J(D/'candidate-freeze.json');att=J(D/'jev-attempt.json');rcp=J(D/'jev_receipt.json');srec=J(V/'jev_stability_1757/replicates_receipt.json')
man={l.split()[1]:l.split()[0] for l in (D/'HASHES.sha256').read_text().splitlines() if l.strip()}
okh=lambda p,h:'exact' if sha(V/p)==h else 'DIFFERS'
led_old=git('show','5f43523:results/super_lotto/prospective/ledger.jsonl')
first=lambda p:git('log','--diff-filter=A','--format=%h %cI','--',p).strip().splitlines()[-1]
ver=dict(manifest={p:okh(p,h) for p,h in man.items() if p!='prospective/ledger.jsonl'},
  ledger_manifest_prefix=('exact' if hashlib.sha256(led_old.encode()).hexdigest()==man['prospective/ledger.jsonl'] else 'DIFFERS'),
  ledger_append_only=(V/'prospective/ledger.jsonl').read_text().startswith(led_old),
  candidate_freeze={n:('exact' if sha(D/n)==h else 'DIFFERS') for n,h in cf['hashes'].items()},
  jev=dict(single_attempt=att['http_attempts']==1 and att['retries_disabled'],response=rcp['response_sha256']==sha(D/'jev_response.json'),state=rcp['state_file_sha256']==sha(D/'jev_state.json'),boundary=rcp.get('boundary')),
  chronology=dict(pool_frozen=cf['frozen_utc'],jev_attempt=att['started_utc'],v1_frozen=pred['created_utc'],p0_frozen=pf['created_utc'],first_replicate=srec['runs'][0]['created_utc'],scheduled_draw='2026-10-07T01:30:00Z'),
  commits=dict(pool=first('results/super_lotto/draw1757/candidates.json'),tickets=first('results/super_lotto/prospective/prediction_1757.json'),post_freeze=first('results/super_lotto/jev_stability_1757/replicate_1_response.json')),
  tickets_unchanged_since_freeze=git('diff','--name-only','dd2b47e','HEAD','--','results/super_lotto/prospective/prediction_1757.json','results/super_lotto/draw1757/p0/p0_frozen.json','results/super_lotto/draw1757/candidates.json','results/super_lotto/draw1757/jev_response.json').strip()=='')
ver['frozen_before_draw']=max(pred['created_utc'],pf['created_utc'])<'2026-10-07T01:30'
ver['ALL_PASS']=bool(all(v=='exact' for v in ver['manifest'].values()) and ver['ledger_manifest_prefix']=='exact' and ver['ledger_append_only'] and all(v=='exact' for v in ver['candidate_freeze'].values())
   and all(ver['jev'][k] for k in ['single_attempt','response','state']) and ver['tickets_unchanged_since_freeze'] and ver['frozen_before_draw'])
save(O/'verification.json',ver)
# ------------- V1 pool scored
cands=J(D/'candidates.json');runs=[J(D/'jev_response.json')]+[J(V/f'jev_stability_1757/replicate_{i}_response.json') for i in range(1,6)]
pr=runs[0]['answers']['overall']['probabilities']
crank=lambda p,c:(1+sum(v>p[c]+1e-12 for v in p.values()),sum(v>=p[c]-1e-12 for v in p.values()))
pool=[]
for c in cands:
    mm=sorted(set(c['main'])&set(WIN));pool.append(dict(id=c['id'],main=c['main'],super_ball=c['super_ball'],generator=c['main_generator'],sb_generator=c['SB_generator'],matches=len(mm),matched=mm,sb_hit=c['super_ball']==WSB,
        jev_choice=pr[c['id']],jev_rank=crank(pr,c['id']),replicate_mean_choice=float(np.mean([r['answers']['overall']['probabilities'][c['id']] for r in runs[1:]])),sensitivity=c['sensitivity_rank_range']))
md=Counter(x['matches'] for x in pool);pm=hg(35,5,5)
summary=dict(distribution={k:md.get(k,0) for k in range(6)},best=max(x['matches'] for x in pool),best_ids=[x['id'] for x in pool if x['matches']==max(x['matches'] for x in pool)],
   v1_selected=pred['selection']['candidate_id'],v1_matches=len(set(pred['selection']['main'])&set(WIN)),jev_production=runs[0]['answers']['overall']['choice'],
   jev_replicates=[r['answers']['overall']['choice'] for r in runs[1:]],jev_favourite_matches=[x['matches'] for x in pool if x['id']==runs[0]['answers']['overall']['choice']][0],
   pool_super_balls=sorted({x['super_ball'] for x in pool}),candidates_with_SB9=[x['id'] for x in pool if x['sb_hit']],p_any_of_20_ge2=float(1-(1-pm[2:].sum())**20))
save(O/'pool_scores.json',dict(summary=summary,candidates=pool,note='Scored after the draw; nothing promoted.'))
# ------------- winners pre-draw evidence (cutoff #1756)
cr=J(D/'complete_rankings.json');feat={int(r['number']):r for r in csv.DictReader(open(D/'main_features.csv',encoding='utf-8-sig'))}
order=pr0['main_order'];POOL=pr0['pool']
def mr(m,n):
    e=cr['main'][m]
    if not e.get('applicable'):return None
    x=[r for r in e['numbers'] if r['number']==n][0];return dict(rank=x['rank'],tie=[x['tie_min'],x['tie_max']],score=x['score'],informative=e['informative'])
win={}
for n in WIN:
    r={m:mr(m,n) for m in cr['main']};rk={m:r[m]['rank'] for m in INF};f=feat[n]
    win[n]=dict(models=r,P0_rank=order.index(n)+1,in_pool=n in POOL,best=min(rk.items(),key=lambda x:x[1]),worst=max(rk.items(),key=lambda x:x[1]),
               features={k:f[k] for k in ['count','ew_rate','last30','last10','current_gap','gap_percentile','trend']},top={K:order.index(n)+1<=K for K in [15,18,20,25]})
tick=[pred['selection']['main'],pf['ticket_2']['mains'],pf['ticket_3']['mains']];avail=sorted(set(POOL)&set(WIN));placed=sorted(set().union(*map(set,tick))&set(WIN))
layers=dict(pool=POOL,available=avail,absent=sorted(set(WIN)-set(POOL)),placed=placed,available_not_placed=sorted(set(avail)-set(placed)),
   per_ticket=[len(set(t)&set(WIN)) for t in tick],p_capture_le_obs_random_top12=float(hg(35,5,12)[:len(avail)+1].sum()))
# ------------- SB9
sbr={m:([x['rank'] for x in e['numbers'] if x['number']==9][0] if e.get('order') is not None else None) for m,e in cr['super_ball'].items()}
sbinfo=dict(actual=9,played=[pred['selection']['super_ball'],pf['ticket_2']['super_ball'],pf['ticket_3']['super_ball']],model_ranks_SB9=sbr,P0_sb_order=pr0['sb_order'],P0_rank_SB9=pr0['sb_order'].index(9)+1,
   in_v1_pool=9 in summary['pool_super_balls'],p_miss_3_distinct=.7)
save(O/'winner_evidence.json',dict(winners=win,layers=layers,super_ball=sbinfo))
# ------------- cumulative prospective record #1753-#1757 (from the ledger)
led=[json.loads(l) for l in (V/'prospective/ledger.jsonl').read_text().splitlines() if l.strip()]
v1=[(e['target_draw_id'],e['main_matches'],int(bool(e['super_ball_match']))) for e in led if e['event']=='outcome_recorded']
p0=[(e['target_draw_id'],e['track'],e['main_matches'],int(bool(e['super_ball_match']))) for e in led if e['event']=='research_outcome_recorded' and e['track'].startswith('P0')]
rcr=[(e['target_draw_id'],e['track'],e['main_matches'],int(bool(e['super_ball_match']))) for e in led if e['event']=='research_outcome_recorded' and e['track'].startswith('random')]
def tail(obs,k):
    q=np.array([1.])
    for _ in range(k):q=np.convolve(q,pm)
    return float(q[:obs+1].sum()),float(q[obs:].sum())
tv=sum(x[1] for x in v1);sv=sum(x[2] for x in v1)
record=dict(v1=v1,v1_total_main=tv,v1_tickets=len(v1),v1_expected=len(v1)*5/7,v1_p_le=tail(tv,len(v1))[0],v1_sb_hits=sv,v1_p_sb0=0.9**len(v1),
  v1_distinct_super_balls=sorted({json.loads(json.dumps(e['frozen_selection']['super_ball'] if 'frozen_selection' in e else e['selection']['super_ball'])) for e in led if e['event']=='outcome_recorded'}),
  p0=p0,p0_total_main=sum(x[2] for x in p0),p0_tickets=len(p0),p0_sb_hits=sum(x[3] for x in p0),random_control=rcr,rc_total_main=sum(x[2] for x in rcr),rc_sb_hits=sum(x[3] for x in rcr),
  single_ticket_null=dict(main_pmf=pm.tolist(),mean=5/7,p_sb=.1,p_jackpot=1/(math.comb(35,5)*10)))
save(O/'prospective_record.json',record)
print(json.dumps(dict(ver=ver['ALL_PASS'],chron=ver['chronology'],pool=summary,win={n:dict(p0=w['P0_rank'],best=w['best'],worst=w['worst'],ranks={m:w['models'][m]['rank'] for m in INF},top=w['top']) for n,w in win.items()},layers=layers,sb=sbinfo,record={k:v for k,v in record.items() if k not in ('single_ticket_null',)}),indent=1,default=str))
