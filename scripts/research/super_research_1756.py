"""Super Lotto research after #1756 (research only; does NOT change frozen V1 or P0).
Strict causal walk-forward on Super Lotto history through #1756: at every origin only draws before the target are used.
One multiple-testing family (Holm) over every variant. Outputs results/super_lotto/p1_research/.
Super Lotto data/code only (unchanged super_lotto.py, super_history.py, super_p0.py, common.py)."""
import sys,json,math,itertools
from pathlib import Path
from collections import Counter
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts/research'))
import super_lotto as sl,super_history as S,super_p0 as P
from common import save,holm,hg,pmean
V=R/'results/super_lotto';O=V/'p1_research';O.mkdir(exist_ok=True)
J=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
full=J(V/'draw1757/draws.json');assert full[-1]['draw_id']==1756 and full[-1]['numbers']==[5,7,15,29,32]
d=np.array([r['numbers'] for r in full])-1;sb=np.array([r['super_ball'] for r in full])-1;ids=[r['draw_id'] for r in full]
C=S.cache(d,sb,ids);idx={x:i for i,x in enumerate(ids)}
# --- reconstruction must equal every frozen V1 pool (#1753..#1757) before any use
val=S.validate(C,ids)
for tgt,p in {1755:V/'draw1755/candidates.json',1756:V/'draw1756/candidates.json',1757:V/'draw1757/candidates.json'}.items():
    _,ft=S.run_at_cutoff(C,idx[tgt-1]);cs=S.candidates(ft);f=J(p)
    val[tgt-1]=dict(mains=[c['main'] for c in cs]==[c['main'] for c in f],super_balls=[c['super_ball'] for c in cs]==[c['super_ball'] for c in f])
assert all(v['mains'] and v.get('super_balls',True) for v in val.values()),val
H=P.build_history(C)
KS=[8,10,12,15,18,20,25];SD5=math.sqrt(5*(5/35)*(30/35)*(30/34));sdK=lambda K:math.sqrt(K*(5/35)*(30/35)*(35-K)/34)
SEED_R=2026100601   # research-only seed for the explicit random-ranking null (declared here, before evaluation)
targets=[o for o in C if 'truth' in o and o['t']>=50+P.MINPRIOR];conf_start=ids[len(ids)-40]
hist=J(V/'p0_protocol/historical_origins.json');hbyt={r['target']:r for r in hist['rows']}
def ap(order,w):
    rel=np.array([int(i in w) for i in order]);return float(np.sum(rel*np.cumsum(rel)/np.arange(1,36))/5)
def rankorder(score,tie,jit=None):
    score=np.asarray(score,float);tie=np.asarray(tie,float);jit=np.zeros(35) if jit is None else jit
    return sorted(range(35),key=lambda i:(-round(float(score[i]+jit[i]),12),-round(float(tie[i]),12),i))
rec=[];mismatch=[]
for o in targets:
    t=o['t'];tgt=o['target'];w=set(np.nonzero(o['truth'])[0].tolist());wsb=o['truth_sb']+1
    cr=P.credibility(H,t);disc=P.discovery(o,cr);Sx,inf=P.fam_scores(o);EQ=disc['EQ'];prior=[h for h in H if h['t']<t]
    jit=np.random.default_rng(sl.SEED+tgt*31).random(35)*1e-10;I=[j for j in range(5) if inf[j]]
    od={}
    od['A_random']=list(np.random.default_rng(SEED_R+tgt).permutation(35))
    for j,m in [(0,'B_long'),(1,'C_recent'),(3,'D_trend'),(2,'E_gap')]:od[m]=rankorder(Sx[j],np.zeros(35),jit)
    od['F_P0_frozen_protocol']=[x-1 for x in disc['order']]
    od['G_equal_weight']=rankorder(EQ,np.zeros(35))
    stats_e={m:[h['e'][m] for h in prior if h['e'][m] is not None] for m in P.MAIN}
    mean_e={m:(np.mean(v) if len(v)>=P.MINPRIOR else 0.) for m,v in stats_e.items()};se_e={m:(P.AP_SD/math.sqrt(len(v)) if len(v)>=P.MINPRIOR else 1.) for m,v in stats_e.items()}
    zr={m:mean_e[m]/se_e[m] for m in P.MAIN}
    w_un=np.array([max(0.,zr[m]) for m in P.MAIN]);od['H_unshrunk_reliability']=rankorder(w_un@Sx,EQ)
    praw={m:0.5*math.erfc(zr[m]/math.sqrt(2)) for m in P.MAIN}
    halves={m:(len(v)>=P.MINPRIOR and np.mean(v[:len(v)//2])>0 and np.mean(v[len(v)//2:])>0) for m,v in stats_e.items()}
    w_light=np.array([max(0.,1-2*praw[m])*halves[m] if len(stats_e[m])>=P.MINPRIOR else 0. for m in P.MAIN]);od['I_light_shrinkage']=rankorder(w_light@Sx,EQ)
    act=[m for m in P.MAIN if len(stats_e[m])>=P.MINPRIOR]
    if act:
        mm=np.array([mean_e[m] for m in act]);ss2=np.array([se_e[m]**2 for m in act]);tau2=max(0.,float(np.var(mm,ddof=1) if len(mm)>1 else 0.)-float(ss2.mean()))
        post={m:mean_e[m]*tau2/(tau2+se_e[m]**2) for m in act}
    else:post={}
    w_b=np.array([max(0.,post.get(m,0.)) for m in P.MAIN]);od['L_bayes_empirical']=rankorder(w_b@Sx,EQ)
    for drop,name in [(0,'J_lofo_minus_A'),(1,'J_lofo_minus_B'),(2,'J_lofo_minus_C'),(3,'J_lofo_minus_D')]:
        keep=[j for j in I if j!=drop];od[name]=rankorder(Sx[keep].mean(0) if keep else np.zeros(35),np.zeros(35))
    tr={m:np.mean([h['e'][m] for h in prior[-30:] if h['e'][m] is not None] or [-9]) for m in P.MAIN};bm=max(tr,key=tr.get);od['K_best_trailing_model']=rankorder(Sx[P.MAIN.index(bm)],np.zeros(35),jit)
    ranks=np.array([np.argsort(np.argsort(-(Sx[j]+jit),kind='stable')) for j in I]);od['M_family_vote_borda']=rankorder(-ranks.mean(0),EQ)
    cap={m:{K:len(set(v[:K])&w) for K in KS} for m,v in od.items()};aps={m:ap(v,w) for m,v in od.items()}
    # frozen constructor at this origin (causal credibility, K=12, rule C) and V1 at this cutoff
    _,ft=S.run_at_cutoff(C,t-1);cs=S.candidates(ft);v1,unrun=S.v1_ticket(ft)
    U=P.universe(o,disc,cr,12);lg=P.portfolio(U,disc,v1['main'],12);port=[sorted(v1['main'])]+[l['ticket'] for l in lg];sbs=[v1['super_ball']]+P.assign_sb('C',disc,v1['super_ball'],tgt)
    if tgt in hbyt and port!=hbyt[tgt]['byK']['12']['mains']:mismatch.append(tgt)
    wins={i+1 for i in w};pool12=set(U['pool'])
    m=[len(set(x)&wins) for x in port];chcov=set(port[1])|set(port[2])
    pdi=int(np.random.default_rng(sl.SEED+tgt).integers(20));rot=tgt%20
    v1rec=dict(unrunnable=unrun,sl10=dict(main=v1['main'],sb=v1['super_ball'],hits=len(set(v1['main'])&wins),sb_hit=int(v1['super_ball']==wsb)))
    if cs:
        ch=[len(set(c['main'])&wins) for c in cs]
        v1rec.update(all_hits=ch,uniform_mean=float(np.mean(ch)),per_draw_seed=dict(idx=pdi,main=cs[pdi]['main'],sb=cs[pdi]['super_ball'],hits=ch[pdi],sb_hit=int(cs[pdi]['super_ball']==wsb)),
                     rotating_slot=dict(idx=rot,main=cs[rot]['main'],sb=cs[rot]['super_ball'],hits=ch[rot],sb_hit=int(cs[rot]['super_ball']==wsb)),
                     union=sorted({x for c in cs for x in c['main']}),union_hits=len({x for c in cs for x in c['main']}&wins),pool_sbs=sorted({c['super_ball'] for c in cs}),pool_sb_hit=int(wsb in {c['super_ball'] for c in cs}))
    rec.append(dict(target=tgt,t=t,period='confirmation' if tgt>=conf_start else 'development',winners=sorted(wins),winning_sb=wsb,cap=cap,ap=aps,best_model=bm,
        nonzero_credibility={m:cr['main'][m]['c'] for m in P.MAIN if cr['main'][m]['c']>0},order_P0=[i+1 for i in od['F_P0_frozen_protocol']],
        sb_rank_P0=disc['sborder'].index(wsb)+1,sb_rank_EQ=disc['sb_eq_order'].index(wsb)+1,sborder=disc['sborder'],
        sbs_ruleB=[v1['super_ball']]+P.assign_sb('B',disc,v1['super_ball'],tgt),sbs_ruleC=sbs,
        construction=dict(pool12=sorted(pool12),K_in_pool=len(pool12&wins),portfolio=port,main=m,best=max(m),total=sum(m),unique=len(set().union(*map(set,port))&wins),
                          challengers_unique=len(chcov&wins),challenger_pool_coverage=len(chcov&pool12),challengers_inpool_captured=len(chcov&pool12&wins),v1_hits=m[0],sb_hit=int(wsb in sbs)),v1=v1rec))
# ---------------------------------------------------------------- statistics
def capture_stats(rows,m,K):
    c=np.array([r['cap'][m][K] for r in rows]);mu=5*K/35;z=(c-mu)/sdK(K);q=np.array([1.]);pm=hg(35,5,K)
    for _ in rows:q=np.convolve(q,pm)
    ge={k:float(np.mean(c>=k)) for k in range(1,6)};ge_null={k:float(pm[k:].sum()) for k in range(1,6)}
    return dict(mean=float(c.mean()),expected=mu,excess=float(c.mean()-mu),p=float(q[int(c.sum()):].sum()),z=z,ge=ge,ge_null=ge_null)
def ap_stats(rows,m):
    a=np.array([r['ap'][m] for r in rows]);z=(a-P.AP0)/P.AP_SD;zz=z.mean()*math.sqrt(len(z));return dict(mean=float(a.mean()),expected=P.AP0,excess=float(a.mean()-P.AP0),p=float(0.5*math.erfc(zz/math.sqrt(2))),z=z)
def binom_stats(h,p0):
    h=np.asarray(h,int);n=len(h);k=int(h.sum());return dict(mean=float(h.mean()),expected=p0,excess=float(h.mean()-p0),p=float(sum(math.comb(n,j)*p0**j*(1-p0)**(n-j) for j in range(k,n+1))),z=(h-p0)/math.sqrt(p0*(1-p0)))
def match_stats(y):
    y=np.asarray(y,float);return dict(mean=float(y.mean()),expected=5/7,excess=float(y.mean()-5/7),p=float(pmean(y,35,5,5)),z=(y-5/7)/SD5)
def dyn_K(rows,i):
    prev=rows[max(0,i-30):i]
    if len(prev)<10:return 12
    return max(KS,key=lambda K:np.mean([(r['cap']['F_P0_frozen_protocol'][K]-5*K/35)/sdK(K) for r in prev]))
for i,r in enumerate(rec):r['dynK']=dyn_K(rec,i);r['cap_dyn']=r['cap']['F_P0_frozen_protocol'][r['dynK']]
def var_capture(c,K):
    c=np.asarray(c);mu=np.array([5*k/35 for k in K]);q=np.array([1.])
    for k in K:q=np.convolve(q,hg(35,5,k))
    return dict(mean=float(c.mean()),expected=float(mu.mean()),excess=float((c-mu).mean()),p=float(q[int(c.sum()):].sum()),z=(c-mu)/np.array([sdK(k) for k in K]))
def dyn_stats(rows):return var_capture([r['cap_dyn'] for r in rows],[r['dynK'] for r in rows])
METHODS=list(rec[0]['cap'])
def variants(rows):
    out={}
    for m in METHODS:
        for K in KS:out[f'order:{m}:top{K}']=capture_stats(rows,m,K)
        out[f'order:{m}:AP']=ap_stats(rows,m)
    out['pool:dynamic_size_P0']=dyn_stats(rows)
    for k in range(1,6):out[f'SB:P0_order_top{k}']=binom_stats([int(r['sb_rank_P0']<=k) for r in rows],k/10)
    for k in range(1,4):out[f'SB:equal_weight_top{k}']=binom_stats([int(r['sb_rank_EQ']<=k) for r in rows],k/10)
    out['SB:rule_C_portfolio_any']=binom_stats([int(r['winning_sb'] in r['sbs_ruleC']) for r in rows],.3)
    out['SB:rule_B_portfolio_any']=binom_stats([int(r['winning_sb'] in r['sbs_ruleB']) for r in rows],.3)
    vr=[r for r in rows if 'per_draw_seed' in r['v1']]
    out['V1:SL10_fixed_slot']=match_stats([r['v1']['sl10']['hits'] for r in rows])
    out['V1:per_draw_seed']=match_stats([r['v1']['per_draw_seed']['hits'] for r in vr])
    out['V1:rotating_slot']=match_stats([r['v1']['rotating_slot']['hits'] for r in vr])
    out['V1:broader_candidate_union']=var_capture([r['v1']['union_hits'] for r in vr],[len(r['v1']['union']) for r in vr])
    out['V1:pool_contains_winning_SB']=binom_stats([r['v1']['pool_sb_hit'] for r in vr],float(np.mean([len(r['v1']['pool_sbs'])/10 for r in vr])))
    return out
conf=[r for r in rec if r['period']=='confirmation'];dev=[r for r in rec if r['period']=='development']
E={'confirmation':variants(conf),'development':variants(dev),'full':variants(rec)}
names=list(E['confirmation']);hp=holm([E['confirmation'][n]['p'] for n in names]);hpf=holm([E['full'][n]['p'] for n in names])
res={}
for n,h,hf in zip(names,hp,hpf):
    v=E['confirmation'][n];z=np.asarray(v['z'],float);lb=P.block_ci(z,P.SEEDS['gate_bootstrap']);half=len(z)//2;zf=np.asarray(E['full'][n]['z'],float);hf2=len(zf)//2
    res[n]=dict(confirmation=dict(mean=v['mean'],expected=v['expected'],excess=v['excess'],p=v['p'],holm_p=float(h),block95_std_excess=lb,halves_std_excess=[float(z[:half].mean()),float(z[half:].mean())],**({'ge':v['ge'],'ge_null':v['ge_null']} if 'ge' in v else {})),
                development=dict(mean=E['development'][n]['mean'],expected=E['development'][n]['expected'],excess=E['development'][n]['excess'],p=E['development'][n]['p']),
                full=dict(mean=E['full'][n]['mean'],expected=E['full'][n]['expected'],excess=E['full'][n]['excess'],p=E['full'][n]['p'],holm_p=float(hf),halves_std_excess=[float(zf[:hf2].mean()),float(zf[hf2:].mean())],block95_std_excess=P.block_ci(zf,P.SEEDS['gate_bootstrap']),**({'ge':E['full'][n]['ge']} if 'ge' in E['full'][n] else {})),
                passes=bool(h<.05 and v['excess']>0 and lb[0]>0 and z[:half].mean()>0 and z[half:].mean()>0 and E['development'][n]['excess']>0))
passing=[n for n,v in res.items() if v['passes']]
# ---------------------------------------------------------------- construction conditional on discovery (frozen constructor, K=12)
byK={}
for r in rec:
    c=r['construction'];byK.setdefault(c['K_in_pool'],[]).append(c)
cond={k:dict(n=len(v),mean_best=float(np.mean([c['best'] for c in v])),mean_total=float(np.mean([c['total'] for c in v])),mean_unique=float(np.mean([c['unique'] for c in v])),
             challengers_inpool_captured=float(np.mean([c['challengers_inpool_captured'] for c in v])),blind_expectation=float(np.mean([k*c['challenger_pool_coverage']/12 for c in v])),
             conversion=float(sum(c['challengers_inpool_captured'] for c in v)/max(1,k*len(v)))) for k,v in sorted(byK.items())}
tot_in=sum(r['construction']['K_in_pool'] for r in rec);tot_cap=sum(r['construction']['challengers_inpool_captured'] for r in rec)
blind=sum(r['construction']['K_in_pool']*r['construction']['challenger_pool_coverage']/12 for r in rec)
construction=dict(by_K_in_pool=cond,total_in_pool=tot_in,captured_by_challengers=tot_cap,blind_expected=float(blind),ratio=tot_cap/tot_in,
   corr_K_vs_best=float(np.corrcoef([r['construction']['K_in_pool'] for r in rec],[r['construction']['best'] for r in rec])[0,1]),
   random_K_distribution=dict(zip(range(6),hg(35,5,12).tolist())),observed_K_distribution={k:len(v)/len(rec) for k,v in sorted(byK.items())},historical_replay_mismatch_targets=mismatch)
# ---------------------------------------------------------------- SL10 fixed slot vs alternatives
vr=[r for r in rec if 'per_draw_seed' in r['v1']]
def recurrence(sel):
    ov=[len(set(a['main'])&set(b['main'])) for a,b in zip(sel,sel[1:])];sbr=[int(a['sb']==b['sb']) for a,b in zip(sel,sel[1:])];cnt=Counter(x for s in sel for x in s['main']);sbc=Counter(s['sb'] for s in sel)
    p=np.array(list(cnt.values()))/sum(cnt.values());ps=np.array(list(sbc.values()))/sum(sbc.values())
    return dict(mean_consecutive_overlap=float(np.mean(ov)),random_overlap=25/35,consecutive_identical=int(sum(o==5 for o in ov)),sb_repeat_rate=float(np.mean(sbr)),random_sb_repeat=.1,
                distinct_numbers=len(cnt),top_numbers=cnt.most_common(6),number_entropy_bits=float(-(p*np.log2(p)).sum()),max_entropy_bits=math.log2(35),sb_counts=dict(sorted(sbc.items())),sb_entropy_bits=float(-(ps*np.log2(ps)).sum()))
sl10=dict(selected_share_of_no_edge_draws=1.0,targets=len(rec),targets_with_full_pool=len(vr),gate_qualified_targets=hist['v1_gate_flagged_targets'],
   mean_matches=dict(SL10=float(np.mean([r['v1']['sl10']['hits'] for r in vr])),uniform_candidate=float(np.mean([r['v1']['uniform_mean'] for r in vr])),per_draw_seed=float(np.mean([r['v1']['per_draw_seed']['hits'] for r in vr])),rotating_slot=float(np.mean([r['v1']['rotating_slot']['hits'] for r in vr])),random=5/7),
   sb_hit_rate=dict(SL10=float(np.mean([r['v1']['sl10']['sb_hit'] for r in vr])),per_draw_seed=float(np.mean([r['v1']['per_draw_seed']['sb_hit'] for r in vr])),rotating_slot=float(np.mean([r['v1']['rotating_slot']['sb_hit'] for r in vr])),random=.1),
   per_slot_mean_matches=[float(np.mean([r['v1']['all_hits'][i] for r in vr])) for i in range(20)],
   recurrence=dict(SL10=recurrence([r['v1']['sl10'] for r in vr]),per_draw_seed=recurrence([r['v1']['per_draw_seed'] for r in vr]),rotating_slot=recurrence([r['v1']['rotating_slot'] for r in vr])),
   note='Under the no-edge rule every V1 run selects index int(default_rng(2026092109).integers(20)) = 9 = SL10 = D_trend top ticket with the S_gap SB.')
# ---------------------------------------------------------------- outputs
out=dict(data_through=1756,validation={str(k):v for k,v in val.items()},targets=[rec[0]['target'],rec[-1]['target']],n_targets=len(rec),confirmation_targets=[conf[0]['target'],conf[-1]['target']],
  family_size=len(names),correction='Holm over every variant in one family (orderings x pool sizes x AP, dynamic pool, SB rules, V1 selection variants)',random_null_seed=SEED_R,
  pass_rule='Holm p<.05 in confirmation AND positive confirmation excess AND block-bootstrap 95% lower bound > 0 AND both confirmation halves > 0 AND positive development excess',
  refinements=res,passing=passing,conclusion='NO SUPER LOTTO V2/P1 REFINEMENT IS JUSTIFIED' if not passing else 'P1 RESEARCH CHALLENGER candidate(s): '+', '.join(passing),
  dynamic_K_choices={str(k):int(sum(r['dynK']==k for r in rec)) for k in KS},credibility_nonzero_targets=[r['target'] for r in rec if r['nonzero_credibility']],
  jev_aggregation='Not testable: saved Jev replicate sets with known outcomes exist only for #1755 and #1756 (n=2); reported descriptively in forensic_1756/jev_stability.json, excluded from inference.')
save(O/'research_challengers.json',out);save(O/'research_origins.json',rec);save(O/'construction_conditional.json',construction);save(O/'sl10_fixed_slot.json',sl10)
print(json.dumps(dict(val=val,n=len(rec),family=len(names),passing=passing,mismatch=mismatch,minholm=min(v['confirmation']['holm_p'] for v in res.values()),
  top=sorted(((n,round(v['confirmation']['p'],3),round(v['full']['p'],3)) for n,v in res.items()),key=lambda x:x[1])[:10],construction={k:construction[k] for k in ['total_in_pool','captured_by_challengers','blind_expected','ratio']},sl10=sl10['mean_matches']),indent=1,default=str))
