"""Super Lotto P0 historical walk-forward test and protocol freeze. Reads ONLY results/super_lotto/draw1754/draws.json
(history through #1753). Implements results/super_lotto/p0_protocol/DESIGN_PRECOMMIT.json. Writes results/super_lotto/p0_protocol/."""
import sys,json,math,hashlib
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts/research'))
import super_lotto as sl,super_history as S,super_p0 as P
from common import holm,save
O=R/'results/super_lotto/p0_protocol';DATA=R/'results/super_lotto/draw1754/draws.json'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
records,d,sb,ids=S.load(DATA);assert ids[-1]==1753 and 1754 not in ids,'P0 design must not see #1754'
C=S.cache(d,sb,ids);val=S.validate(C,ids);assert all(v['mains'] and v['super_balls'] and v['generators'] for v in val.values()),val
H=P.build_history(C);byt={o['t']:o for o in C}
# Ticket 1 history: V1 fallback (no overlap rule in Super Lotto V1)
v1={};flag=[];v1_unrunnable=[]
for ci in range(49,len(ids)):
    rows,fit=S.run_at_cutoff(C,ci);g,_=S.gate(rows);tgt=ids[ci]+1
    v1[tgt],broken=S.v1_ticket(fit)
    if broken:v1_unrunnable.append(tgt)
    if g['main'] or g['SB']:flag.append(tgt)
_,fit_design=S.run_at_cutoff(C,len(ids)-1)
sb_gate_design=S.gate(S.run_at_cutoff(C,len(ids)-1)[0])[0]['SB']
SB_RULE='A' if sb_gate_design else 'C'
conf_start=ids[len(ids)-40]            # V1 confirmation window of the design dataset: last 40 origins
targets=[o for o in C if 'truth' in o and o['t']>=50+P.MINPRIOR]
per=[]
for o in targets:
    tgt=o['target'];win=(np.nonzero(o['truth'])[0]+1).tolist();wsb=o['truth_sb']+1;cr=P.credibility(H,o['t']);disc=P.discovery(o,cr);t1=v1[tgt]
    row=dict(target=tgt,period='development' if tgt<conf_start else 'confirmation',winners=win,winning_sb=wsb,v1=dict(main=t1['main'],sb=t1['super_ball'],id=t1['id']),v1_gate_flag=tgt in flag,v1_unrunnable=tgt in v1_unrunnable,
             cred=dict(main={m:cr['main'][m]['c'] for m in P.MAIN},sb={m:cr['sb'][m]['c'] for m in P.SBM},ticket={k:v['c'] for k,v in cr['ticket'].items()}),
             order=disc['order'],sborder=disc['sborder'],capture={K:len(set(disc['order'][:K])&set(win)) for K in P.K_OPTIONS},
             sb_rank_of_winner=disc['sborder'].index(wsb)+1,byK={})
    rn=np.random.default_rng(P.SEEDS['null_mc_base']+tgt)
    for K in P.K_OPTIONS:
        U=P.universe(o,disc,cr,K);log=P.portfolio(U,disc,t1['main'],K);mains=[t1['main']]+[l['ticket'] for l in log]
        rules={r:P.assign_sb(r,disc,t1['super_ball'],tgt) for r in 'ABCD'};sbs=[t1['super_ball']]+rules[SB_RULE]
        D3=P.top3_standalone(U);dsb=[b for b in disc['sborder']][:3]
        nm=P.null_pmfs(mains,sbs,rn)
        row['byK'][K]=dict(mains=mains,sbs=sbs,log=log,stats=P.stats(mains,sbs,win,wsb),rules={r:P.stats(mains,[t1['super_ball']]+v,win,wsb) for r,v in rules.items()},
                           D=P.stats(D3,dsb,win,wsb),null={k:v.tolist() for k,v in nm.items()})
    rc=np.random.default_rng(P.SEEDS['comparators_base']+tgt);cp={k:[] for k in 'ABCE'}
    mainsK=row['byK'][P.K_DEFAULT]['mains']
    for _ in range(200):
        cp['A'].append(P.stats([P.rt(rc) for _ in range(3)],[int(rc.integers(10))+1 for _ in range(3)],win,wsb))
        cp['B'].append(P.stats(P.rdiv(rc,[],3),[int(rc.integers(10))+1 for _ in range(3)],win,wsb))
        cp['C'].append(P.stats([t1['main']]+P.rdiv(rc,[t1['main']],2),[t1['super_ball']]+[int(rc.integers(10))+1 for _ in range(2)],win,wsb))
    row['comparators']={k:{m:float(np.mean([s[m] for s in v])) for m in ['best','total','ch_total','ge2','ge3','ge4','five','any_sb','sb_total','ch_sb','any_ge2_sb','any_ge3_sb','unique','distinct_sbs','mean_overlap']} for k,v in cp.items() if v}
    row['E_random_sb']={}
    for K in P.K_OPTIONS:
        mk=row['byK'][K]['mains'];ee=[P.stats(mk,[t1['super_ball']]+[int(rc.integers(10))+1 for _ in range(2)],win,wsb) for _ in range(200)]
        row['E_random_sb'][K]={m:float(np.mean([s[m] for s in ee])) for m in ['any_sb','sb_total','ch_sb','any_ge2_sb','best_ticket_sb']}
    per.append(row)
dev=[r for r in per if r['period']=='development'];conf=[r for r in per if r['period']=='confirmation']
# ---- pool size (development only)
sel={}
for K in P.K_OPTIONS:
    c=np.array([r['capture'][K] for r in dev]);e0=5*K/35;pm=P.hg35(K);sdK=math.sqrt(K*(5/35)*(30/35)*(35-K)/34);h=len(c)//2
    sel[K]=dict(n=len(c),mean=float(c.mean()),expected=e0,excess=float(c.mean()-e0),z=float((c.mean()-e0)/(sdK/math.sqrt(len(c)))),p=P.conv_p([pm]*len(c),int(c.sum())),
                block95=P.block_ci(c-e0,P.SEEDS['pool_bootstrap']),half1=float(c[:h].mean()-e0),half2=float(c[h:].mean()-e0),variance=float(c.var(ddof=1)),
                p_ge={k:float(np.mean(c>=k)) for k in [2,3,4,5]},p_ge_random={k:float(pm[k:].sum()) for k in [2,3,4,5]},
                confirmation_excess=float(np.mean([r['capture'][K] for r in conf])-e0))
for K,hp in zip(P.K_OPTIONS,holm([sel[K]['p'] for K in P.K_OPTIONS])):sel[K]['holm_p']=float(hp);sel[K]['passes']=bool(hp<.05 and sel[K]['block95'][0]>0 and sel[K]['half1']>0 and sel[K]['half2']>0)
passing=[K for K in P.K_OPTIONS if sel[K]['passes']];K_star=max(passing,key=lambda K:sel[K]['z']) if passing else P.K_DEFAULT
pool_decision=dict(options=sel,passing=passing,selected_K=K_star,basis='passing K with largest z' if passing else 'NO EDGE: predeclared default K=12 (no pool size passed on development)')
# ---- evaluation, SB rule comparison, gate
MET=['best','total','ch_total','ge2','ge3','ge4','five','any_sb','sb_total','ch_sb','best_ticket_sb','any_ge2_sb','any_ge3_sb','unique','distinct_sbs','mean_overlap']
def summ(rows,K):
    out={}
    for m in MET:
        def s(f):v=np.array([f(r) for r in rows],float);return dict(mean=float(v.mean()),ci95=P.block_ci(v,P.SEEDS['gate_bootstrap']))
        e=dict(P0=s(lambda r:r['byK'][K]['stats'][m]),D_top3_standalone=s(lambda r:r['byK'][K]['D'][m]))
        for k in 'ABC':
            if m in rows[0]['comparators'][k]:e[{'A':'A_three_random','B':'B_three_random_overlap1','C':'C_v1_plus_two_random'}[k]]=s(lambda r,k=k:r['comparators'][k][m])
        if m in rows[0]['E_random_sb'][K]:e['E_p0_mains_random_sb']=s(lambda r:r['E_random_sb'][K][m])
        if 'C_v1_plus_two_random' in e:e['diff_P0_minus_C']=s(lambda r:r['byK'][K]['stats'][m]-r['comparators']['C'][m])
        out[m]=e
    return out
def sbrules(rows,K):return {rl:{m:float(np.mean([r['byK'][K]['rules'][rl][m] for r in rows])) for m in ['any_sb','sb_total','ch_sb','best_ticket_sb','any_ge2_sb','distinct_sbs']} for rl in 'ABCD'}
def gate(rows,K):
    ch=np.array([r['byK'][K]['stats']['ch_total'] for r in rows]);cs=[r['byK'][K]['stats']['ch_sb'] for r in rows];be=[r['byK'][K]['stats']['best'] for r in rows]
    p1=P.conv_p([np.array(r['byK'][K]['null']['ch_total']) for r in rows],int(ch.sum()));p2=P.conv_p([np.array(r['byK'][K]['null']['ch_sb']) for r in rows],int(sum(cs)))
    p3=P.conv_p([np.array(r['byK'][K]['null']['best']) for r in rows],int(sum(be)));hp=holm([p1,p2,p3]);ex=ch-10*5/35;lb=P.block_ci(ex,P.SEEDS['gate_bootstrap']);h=len(ex)//2
    return dict(n=len(rows),E1_ch_main=dict(observed=int(ch.sum()),expected=10*5/35*len(rows),p=p1,holm_p=float(hp[0]),mean_excess=float(ex.mean()),block95=lb,half1=float(ex[:h].mean()),half2=float(ex[h:].mean())),
                E2_ch_sb=dict(observed=int(sum(cs)),p=p2,holm_p=float(hp[1])),E3_best=dict(observed=int(sum(be)),p=p3,holm_p=float(hp[2])),
                PASS=bool(hp[0]<.05 and lb[0]>0 and ex[:h].mean()>0 and ex[h:].mean()>0))
G=gate(conf,K_star)
evaluation=dict(selected_K=K_star,sb_rule=SB_RULE,confirmation=summ(conf,K_star),development=summ(dev,K_star),gate=G,gate_development=gate(dev,K_star),
                sb_rule_comparison=dict(development=sbrules(dev,K_star),confirmation=sbrules(conf,K_star),null_reference=dict(ch_sb_expected=0.2,any_sb_distinct_three=0.3,any_sb_same_on_challengers='0.1 + 0.1 - overlap (<= 0.2)')),
                downstream_by_K={K:dict(development=gate(dev,K),confirmation=gate(conf,K)) for K in P.K_OPTIONS},
                sb_winner_rank_mean=dict(development=float(np.mean([r['sb_rank_of_winner'] for r in dev])),confirmation=float(np.mean([r['sb_rank_of_winner'] for r in conf])),random=5.5))
# ---- reliability report at the design cutoff (all origins through #1753) and frozen constants
cr_frozen=P.credibility(H,len(ids))
rel={}
for m in P.MAIN:
    e=[h['e'][m] for h in H if h['e'][m] is not None]
    if not e:rel[m]=dict(informative_origins=0,note='flat at every origin');continue
    caps={}
    for N in [5,8,10,12,15,20]:
        v=[]
        for h in H:
            if h['e'][m] is None:continue
            o=byt[h['t']];Sx,_=P.fam_scores(o);od=np.argsort(-(Sx[P.MAIN.index(m)]+np.random.default_rng(sl.SEED+o['target']*31).random(35)*1e-10))[:N];v.append(int(o['truth'][od].sum()))
        caps[N]=dict(mean=float(np.mean(v)),expected=5*N/35)
    ce=[h['e'][m] for h in H if h['e'][m] is not None and h['target']>=conf_start]
    rel[m]=dict(informative_origins=len(e),mean_AP=float(np.mean(e)+P.AP0),AP0=P.AP0,mean_AP_excess=float(np.mean(e)),z=float(np.mean(e)/(P.AP_SD/math.sqrt(len(e)))),topN_capture=caps,
                confirmation_AP_excess=float(np.mean(ce)) if ce else None,halves=[float(np.mean(e[:len(e)//2])),float(np.mean(e[len(e)//2:]))],block95=P.block_ci(e,P.SEEDS['gate_bootstrap']),frozen=cr_frozen['main'][m])
srel={}
for m in P.SBM:
    q=[h['q'][m] for h in H if h['q'][m] is not None]
    srel[m]=dict(informative_origins=len(q),mean_pct_excess=float(np.mean(q)) if q else None,frozen=cr_frozen['sb'][m])
cnt=np.bincount(sb,minlength=10);probs=(cnt+1)/(cnt.sum()+10)
logloss=[];b=np.zeros(10)
for i in range(len(sb)):
    if i>=50:logloss.append(-math.log((b[sb[i]]+1)/(b.sum()+10)))
    b[sb[i]]+=1
corr={}
Sall=[P.fam_scores(byt[h['t']])[0] for h in H]
for i in range(5):
    for j in range(i+1,5):
        v=[np.corrcoef(x[i],x[j])[0,1] for x in Sall if np.std(x[i])>1e-10 and np.std(x[j])>1e-10];corr[f'{P.MAIN[i]}~{P.MAIN[j]}']=float(np.mean(v)) if v else None
reliability=dict(main=rel,super_ball=srel,ticket_level=cr_frozen['ticket'],correlations=corr,
                 sb_calibration=dict(dirichlet_long_run_logloss=float(np.mean(logloss)),uniform_logloss=math.log(10),origins=len(logloss)),
                 formula='c = max(0, 1 - 2*p_Holm) * [both halves positive]; p from mean AP excess (main), mean SB percentile excess (SB), exact hypergeometric total hits (E/F tickets); minimum 25 prior origins',
                 AP0=P.AP0,AP_null_sd=P.AP_SD,SB_null_sd=P.SB_SD)
save(O/'reliability.json',reliability);save(O/'pool_size_selection.json',pool_decision);save(O/'historical_evaluation.json',evaluation)
save(O/'historical_origins.json',dict(validation=val,v1_gate_flagged_targets=flag,v1_unrunnable_targets_SL10_slot_used=v1_unrunnable,conf_start=conf_start,rows=per))
protocol=dict(id='SUPER-LOTTO-P0-protocol-v1',status='FROZEN before any Super Lotto P0 shadow evaluation',frozen_utc=datetime.now(timezone.utc).isoformat(),
  design_precommit=dict(path='results/super_lotto/p0_protocol/DESIGN_PRECOMMIT.json',sha256=sha(O/'DESIGN_PRECOMMIT.json'),commit='c3cbcd6'),
  design_dataset=dict(path=str(DATA.relative_to(R)),sha256=sha(DATA),last_draw=1753),
  frozen_constants=dict(main_credibility={m:cr_frozen['main'][m]['c'] for m in P.MAIN},sb_credibility={m:cr_frozen['sb'][m]['c'] for m in P.SBM},ticket_credibility={k:v['c'] for k,v in cr_frozen['ticket'].items()},
     credibility_detail=cr_frozen,main_pool_K=K_star,pool_basis=pool_decision['basis'],sb_rule=SB_RULE,sb_rule_basis='predeclared: C unless an SB model passes the V1 SB gate at the design cutoff (V1 SB gate passing models: %s)'%sb_gate_design,
     eta=P.ETA,overlap_limit=1,evidence_exception_T=P.EXCEPTION_T,min_prior=P.MINPRIOR,AP0=P.AP0,AP_null_sd=P.AP_SD,SB_null_sd=P.SB_SD),
  historical_gate=dict(PASS=G['PASS'],E1=G['E1_ch_main'],E2=G['E2_ch_sb'],E3=G['E3_best']),
  prospective_rules=dict(credibility='frozen constants above; later draws never update them',features='V1 origin quantities at the prospective cutoff',pool='top-K of the P0 main ordering',universe='all C(K,5) combinations',
     ticket_1='frozen V1 Science ticket of that draw',tickets_2_3='greedy J = T + Cov, overlap <= 1 (relax 2, 3 if infeasible)',super_balls='frozen SB rule applied to the P0 SB ordering'),
  seeds=P.SEEDS,code_sha256={p:sha(R/p) for p in ['scripts/research/super_p0.py','scripts/research/super_p0_design_test.py','scripts/research/super_history.py','scripts/research/super_lotto.py','scripts/research/common.py']},
  outputs_sha256={n:sha(O/n) for n in ['reliability.json','pool_size_selection.json','historical_evaluation.json','historical_origins.json']})
with open(O/'PROTOCOL.json','x') as f:json.dump(json.loads(json.dumps(protocol,default=float)),f,indent=1)
print(json.dumps(dict(K=K_star,basis=pool_decision['basis'],sb_rule=SB_RULE,cred=protocol['frozen_constants']['main_credibility'],sbcred=protocol['frozen_constants']['sb_credibility'],tick=protocol['frozen_constants']['ticket_credibility'],gate=protocol['historical_gate'],flag=flag,
      pool={K:(round(v['excess'],3),round(v['holm_p'],3)) for K,v in sel.items()},sbrules=evaluation['sb_rule_comparison']),indent=1,default=float))
