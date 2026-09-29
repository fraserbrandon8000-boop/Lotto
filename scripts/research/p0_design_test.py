"""P0 historical walk-forward test and protocol freeze. Reads ONLY history ending at #2340.
Implements results/lotto/p0_protocol/DESIGN_PRECOMMIT.json. Writes results/lotto/p0_protocol/."""
import sys,json,math,hashlib,csv
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'));sys.path.insert(0,str(R/'scripts/research'))
import analyze as a
import p0,v1_history as V
O=R/'results/lotto/p0_protocol';DATA=R/'results/lotto/draw2341/draws.json'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
records,d=V.load(DATA);assert records[-1]['draw_id']==2340 and all(r['draw_id']!=2341 for r in records),'P0 design must not see #2341'
A=a.indicator(d);idx={r['draw_id']:i for i,r in enumerate(records)}
print('building V1 history…',flush=True)
H=p0.build_history(d,records)                      # V1 origins index 50..179 (targets 2211..2340)
cache=V.walk_cache(d,records)
states={records[c+1]['draw_id']:V.state_at_cutoff(d,records,cache,c) for c in range(49,len(records)-1)}
# Ticket 1 history: V1 fallback chain (seed 20260919, <=2 overlap with previous reconstructed primary)
prev=None;v1t={};flag=[]
for tgt in sorted(states):
    cs=states[tgt]['candidates'];el=[c for c in cs if prev is None or len(set(c['numbers'])&set(prev))<=2] or cs
    el=sorted(el,key=lambda c:c['id']);c=el[int(np.random.default_rng(p0.SEEDS['V1']).integers(len(el)))];v1t[tgt]=c;prev=c['numbers']
    if states[tgt]['qualifiers']:flag.append(tgt)
actual={2339:[1,4,13,14,24,38],2340:[5,11,16,24,27,34]}
v1_agreement={t:dict(reconstructed=v1t[t]['numbers'],actual=actual[t],equal=v1t[t]['numbers']==actual[t]) for t in actual}
targets=list(range(70,len(records)));per=[];print('replaying P0 on',len(targets),'targets…',flush=True)
for t in targets:
    tgt=records[t]['draw_id'];win=np.nonzero(A[t])[0]+1;W=p0.weights_at(H,t);wsum=sum(v['w'] for v in W.values())
    ft=p0.origin_features(d,t);M,EQ,order=p0.discovery(ft[0],W);v1=v1t[tgt]['numbers']
    row=dict(target=tgt,index=t,period='development' if tgt<2301 else 'confirmation',winners=win.tolist(),v1_ticket=v1,v1_generator=v1t[tgt]['generator'],
             v1_gate_flag=tgt in flag,weights={k:v['w'] for k,v in W.items()},weight_detail=W,wsum=wsum,discovery_flat=bool(np.std(M)<1e-12),order=order,
             capture={K:len(set(order[:K])&set(win.tolist())) for K in p0.K_OPTIONS},byK={})
    rng_null=np.random.default_rng(p0.SEEDS['null_mc_base']+tgt)
    for K in p0.K_OPTIONS:
        pool=order[:K];U=p0.universe(pool,ft,W,M,EQ);U['wsum']=wsum;log=p0.portfolio(U,M,pool,v1,K)
        port=[v1]+[l['ticket'] for l in log];D3=p0.top3_standalone(U)
        nm=p0.null_pmfs(port,rng_null)
        row['byK'][K]=dict(portfolio=port,log=log,stats=p0.port_stats(port,win),D=dict(tickets=D3,stats=p0.port_stats(D3,win)),
                           null=dict(challengers_total=nm['challengers_total'].tolist(),best=nm['best'].tolist(),ge3=nm['ge3'].tolist()))
    rc=np.random.default_rng(p0.SEEDS['comparators_base']+tgt);comp={'A':[],'B':[],'C':[]}
    for _ in range(200):
        comp['A'].append(p0.port_stats([p0.random_ticket(rc) for _ in range(3)],win))
        comp['B'].append(p0.port_stats(p0.random_diverse(rc,[],3),win))
        comp['C'].append(p0.port_stats([v1]+p0.random_diverse(rc,[v1],2),win))
    row['comparators']={k:{m:float(np.mean([s[m] for s in v])) for m in ['best','total','challengers_total','ge3','ge4','ge5','six','unique','mean_overlap']} for k,v in comp.items()}
    per.append(row)
    if t%10==0:print(' ',tgt,flush=True)
dev=[r for r in per if r['period']=='development'];conf=[r for r in per if r['period']=='confirmation']
# ---------------- pool-size selection (development only)
sel={}
for K in p0.K_OPTIONS:
    c=[r['capture'][K] for r in dev];e0=6*K/38;pm=p0.hg_pmf(K);sdK=math.sqrt(K*(6/38)*(32/38)*(38-K)/37)
    pv=p0.conv_p([pm]*len(c),sum(c));lb=p0.block_lb(np.array(c)-e0,p0.SEEDS['pool_bootstrap'])
    h=len(c)//2;sel[K]=dict(n=len(c),mean=float(np.mean(c)),expected=e0,excess=float(np.mean(c)-e0),z=float((np.mean(c)-e0)/(sdK/math.sqrt(len(c)))),
        p_one_sided=pv,block95=lb,half1_excess=float(np.mean(c[:h])-e0),half2_excess=float(np.mean(c[h:])-e0),variance=float(np.var(c,ddof=1)),
        p_ge={k:float(np.mean(np.array(c)>=k)) for k in [3,4,5,6]},p_ge_random={k:float(pm[k:].sum()) for k in [3,4,5,6]})
hp=a.holm([sel[K]['p_one_sided'] for K in p0.K_OPTIONS])
for K,h_ in zip(p0.K_OPTIONS,hp):sel[K]['holm_p']=float(h_);sel[K]['passes']=bool(h_<.05 and sel[K]['block95'][0]>0 and sel[K]['half1_excess']>0 and sel[K]['half2_excess']>0)
passing=[K for K in p0.K_OPTIONS if sel[K]['passes']]
K_star=max(passing,key=lambda K:sel[K]['z']) if passing else p0.K_DEFAULT
pool_decision=dict(options=sel,passing=passing,selected_K=K_star,basis='passing K with largest z' if passing else 'NO EDGE: predeclared default K=15 (no pool size passed on the development period)')
# confirmation capture per K (reported only)
for K in p0.K_OPTIONS:
    c=[r['capture'][K] for r in conf];sel[K]['confirmation_mean']=float(np.mean(c));sel[K]['confirmation_excess']=float(np.mean(c)-6*K/38)
# ---------------- evaluation & gate
def summarize(rows,K):
    out={}
    def s(get):v=np.array([get(r) for r in rows],float);return dict(mean=float(v.mean()),ci95=p0.block_lb(v,p0.SEEDS['gate_bootstrap']))
    for m in ['best','total','challengers_total','ge3','ge4','ge5','six','unique','mean_overlap']:
        out[m]=dict(P0=s(lambda r:r['byK'][K]['stats'][m]),D_top3_standalone=s(lambda r:r['byK'][K]['D']['stats'][m]),
                    A_three_random=s(lambda r:r['comparators']['A'][m]),B_three_random_overlap2=s(lambda r:r['comparators']['B'][m]),
                    C_v1_plus_two_random=s(lambda r:r['comparators']['C'][m]),
                    diff_P0_minus_C=s(lambda r:r['byK'][K]['stats'][m]-r['comparators']['C'][m]),diff_P0_minus_D=s(lambda r:r['byK'][K]['stats'][m]-r['byK'][K]['D']['stats'][m]),
                    diff_P0_minus_B=s(lambda r:r['byK'][K]['stats'][m]-r['comparators']['B'][m]))
    return out
def gate(rows,K):
    ch=[r['byK'][K]['stats']['challengers_total'] for r in rows];be=[r['byK'][K]['stats']['best'] for r in rows];g3=[r['byK'][K]['stats']['ge3'] for r in rows]
    p1=p0.conv_p([np.array(r['byK'][K]['null']['challengers_total']) for r in rows],sum(ch))
    p2=p0.conv_p([np.array(r['byK'][K]['null']['best']) for r in rows],sum(be))
    p3=p0.conv_p([np.array(r['byK'][K]['null']['ge3']) for r in rows],sum(g3))
    hp=a.holm([p1,p2,p3]);ex=np.array(ch)-12*6/38;lb=p0.block_lb(ex,p0.SEEDS['gate_bootstrap']);h=len(ex)//2
    passed=bool(hp[0]<.05 and lb[0]>0 and ex[:h].mean()>0 and ex[h:].mean()>0)
    return dict(n=len(rows),E1_challengers_total=dict(observed=int(sum(ch)),expected=12*6/38*len(rows),p=p1,holm_p=float(hp[0]),mean_excess=float(ex.mean()),block95=lb,half1=float(ex[:h].mean()),half2=float(ex[h:].mean())),
                E2_best=dict(observed=int(sum(be)),p=p2,holm_p=float(hp[1])),E3_ge3=dict(observed=int(sum(g3)),p=p3,holm_p=float(hp[2])),PASS=passed)
G=gate(conf,K_star)
evaluation=dict(selected_K=K_star,confirmation=summarize(conf,K_star),development=summarize(dev,K_star),full=summarize(per,K_star),
                gate=G,gate_development_reported=gate(dev,K_star),downstream_by_K={K:dict(confirmation=gate(conf,K),development=gate(dev,K)) for K in p0.K_OPTIONS})
# ---------------- family reliability report (all V1 origins through #2340)
rel={};nH=len(H);confH=[h for h in H if h['draw_id']>=2301]
for f in p0.FAM:
    hs=[h for h in H if h['informative'][f]];xs=np.array([h['x'][f] for h in hs])
    if len(xs)==0:rel[f]=dict(informative_origins=0,note='flat at every origin');continue
    cap={}
    for N in [10,12,15,20]:
        v=[]
        for h in hs:
            o=np.argsort(-(h['scores'][p0.FAM.index(f)]+np.random.default_rng(a.SEED+h['draw_id']).random(38)*1e-10))[:N]+1
            v.append(len(set(o.tolist())&set(np.nonzero(A[h['index']])[0]+1)))
        cap[N]=dict(mean=float(np.mean(v)),expected=6*N/38)
    z=xs.mean()/(p0.SIGMA/math.sqrt(len(xs)));pz=0.5*math.erfc(z/math.sqrt(2));cx=[h['x'][f] for h in confH if h['informative'][f]];hh=len(xs)//2
    rel[f]=dict(informative_origins=len(xs),mean_winner_midrank=float(np.mean([h['winner_midrank'][f] for h in hs])),expected_midrank=19.5,topN_capture=cap,
                mean_excess_pct=float(xs.mean()),z=float(z),p_one_sided=float(pz),block95_excess=p0.block_lb(xs,p0.SEEDS['gate_bootstrap']),
                confirmation_mean_excess=float(np.mean(cx)) if cx else None,half1=float(xs[:hh].mean()),half2=float(xs[hh:].mean()))
hpf=a.holm([rel[f]['p_one_sided'] for f in p0.FAM if 'p_one_sided' in rel[f]])
for f,hv in zip([f for f in p0.FAM if 'p_one_sided' in rel[f]],hpf):rel[f]['holm_p']=float(hv)
corr={}
for i in range(5):
    for j in range(i+1,5):
        v=[np.corrcoef(h['scores'][i],h['scores'][j])[0,1] for h in H if np.std(h['scores'][i])>1e-12 and np.std(h['scores'][j])>1e-12]
        corr[f'{p0.FAM[i]}~{p0.FAM[j]}']=float(np.mean(v)) if v else None
W_frozen=p0.weights_at(H,len(records))    # formula output at cutoff #2340 (all V1 origins through #2340)
tau_sens={}
for tau in [0.05,0.18]:
    old=p0.TAU;p0.TAU=tau;tau_sens[str(tau)]={k:v['w'] for k,v in p0.weights_at(H,len(records)).items()};p0.TAU=old
v1sens=list(csv.DictReader(open(R/'results/lotto/draw2341/sensitivity.csv')))
reliability=dict(families=rel,correlations=corr,frozen_weights_at_cutoff_2340=W_frozen,weight_sensitivity_to_tau_reported_only=tau_sens,
                 v1_ticket_sensitivity_confirmation=v1sens,G_ensemble='derived from A-E; reported via V1 G proxy only; number-level weight 0',F_structure='no number-level representation; ticket-level weight from V1 F walk matches (see pair/struct in frozen weights)',
                 formula='w_f = max(0, d_f) * h_f; d_f = dbar_f * n tau^2/(n tau^2 + 1); dbar_f = mean(x_f,u)/sigma; tau = 0.09; sigma = %.6f; n >= 20'%p0.SIGMA)
a.OUT=O
a.save('reliability.json',reliability);a.save('pool_size_selection.json',pool_decision);a.save('historical_evaluation.json',evaluation)
a.save('historical_origins.json',dict(v1_reconstruction_agreement=v1_agreement,v1_gate_flagged_targets=flag,
      rows=[{k:v for k,v in r.items() if k not in ('weight_detail',)} for r in per]))
now=datetime.now(timezone.utc).isoformat()
protocol=dict(id='P0-portfolio-research-protocol-v1',status='FROZEN before any P0 #2341 shadow evaluation',frozen_utc=now,
    design_precommit=dict(path='results/lotto/p0_protocol/DESIGN_PRECOMMIT.json',sha256=sha(O/'DESIGN_PRECOMMIT.json'),commit='a0b2f39'),
    design_dataset=dict(path=str(DATA.relative_to(R)),sha256=sha(DATA),last_draw=2340),
    frozen_constants=dict(weights={k:v['w'] for k,v in W_frozen.items()},weight_detail=W_frozen,discovery_pool_K=K_star,pool_basis=pool_decision['basis'],
        tau=p0.TAU,sigma=p0.SIGMA,sd0=p0.SD0,min_prior=p0.MINPRIOR,eta=p0.ETA,overlap_limit=2,evidence_exception_sd=2.0,mass_floor=0.01),
    historical_gate=dict(PASS=G['PASS'],E1=G['E1_challengers_total'],E2=G['E2_best'],E3=G['E3_ge3']),
    prospective_rules=dict(weights='frozen constants above (formula output at cutoff #2340); #2341 never updates them',
        features='V1 model_features at the prospective cutoff (#2340 for the shadow, #2341 for #2342)',pool='top-K of the P0 ordering (M, then EQ, then number)',
        universe='all C(K,6) combinations enumerated',ticket_1='frozen V1 Science ticket of that draw',tickets_2_3='greedy portfolio objective J = T + eta*Cov with the <=2 overlap rule'),
    seeds=p0.SEEDS,code_sha256={p:sha(R/p) for p in ['scripts/research/p0.py','scripts/research/p0_design_test.py','scripts/research/v1_history.py','scripts/analyze.py']},
    outputs_sha256={n:sha(O/n) for n in ['reliability.json','pool_size_selection.json','historical_evaluation.json','historical_origins.json']})
with open(O/'PROTOCOL.json','x') as f:json.dump(json.loads(json.dumps(protocol,default=float)),f,indent=1)
print(json.dumps(dict(K=K_star,basis=pool_decision['basis'],weights=protocol['frozen_constants']['weights'],gate=protocol['historical_gate'],v1_agreement=v1_agreement,flag=flag),indent=1,default=float))
