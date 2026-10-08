"""Single-ticket suitability audit (research only; Super Lotto data only), strict causal replay through #1757.
For every target t (same origins as the P0 replay) each SELECTOR produces exactly ONE complete ticket (5 mains + SB)
from draws < t only. Outputs results/super_lotto/single_ticket_audit_1758/."""
import sys,json,math
from pathlib import Path
from collections import Counter
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts/research'))
import super_lotto as sl,super_history as S,super_p0 as P
from common import save,holm,hg,pmean
V=R/'results/super_lotto';O=V/'single_ticket_audit_1758';O.mkdir(exist_ok=True)
J=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
base=J(V/'draw1757/draws.json');assert base[-1]['draw_id']==1756
full=base+[dict(draw_id=1757,date='2026-10-06',numbers=[4,23,29,31,32],super_ball=9)]
d=np.array([r['numbers'] for r in full])-1;sb=np.array([r['super_ball'] for r in full])-1;ids=[r['draw_id'] for r in full]
C=S.cache(d,sb,ids);idx={x:i for i,x in enumerate(ids)};H=P.build_history(C)
for tgt in [1755,1756,1757]:   # reconstruction must equal the frozen V1 pools
    _,ft=S.run_at_cutoff(C,idx[tgt-1]);cs=S.candidates(ft);assert [c['main'] for c in cs]==[c['main'] for c in J(V/f'draw{tgt}/candidates.json')],tgt
SEED_RAND=2026100801   # research-only control seed, declared before evaluation
targets=[o for o in C if 'truth' in o and o['t']>=50+P.MINPRIOR];rows=[]
for o in targets:
    t=o['t'];tgt=o['target'];wins=set((np.nonzero(o['truth'])[0]+1).tolist());wsb=o['truth_sb']+1
    cr=P.credibility(H,t);disc=P.discovery(o,cr);_,ft=S.run_at_cutoff(C,t-1);cs=S.candidates(ft);v1,unrun=S.v1_ticket(ft)
    U=P.universe(o,disc,cr,12);lg=P.portfolio(U,disc,v1['main'],12);sbs=P.assign_sb('C',disc,v1['super_ball'],tgt)
    rk=np.lexsort((np.arange(len(U['C'])),-np.round(U['EQ'],12),-np.round(U['T'],12)));top=(U['C'][rk[0]]+1).tolist();pos=np.empty(len(rk),int);pos[rk]=np.arange(1,len(rk)+1)
    def rank_of(t_):
        i=[k for k,c in enumerate(U['C']) if sorted((c+1).tolist())==sorted(t_)];return int(pos[i[0]]) if i else None
    g=np.random.default_rng(SEED_RAND+tgt)
    sel={'V1_fixed_slot (incumbent)':(sorted(v1['main']),v1['super_ball']),
         'P0_coverage_1':(lg[0]['ticket'],sbs[0]),'P0_coverage_2':(lg[1]['ticket'],sbs[1]),
         'P0_standalone_top':(top,disc['sborder'][0]),
         'V1_pool_per_draw_seed':((cs[int(np.random.default_rng(sl.SEED+tgt).integers(len(cs)))]['main'],cs[int(np.random.default_rng(sl.SEED+tgt).integers(len(cs)))]['super_ball']) if cs else (sorted(v1['main']),v1['super_ball'])),
         'uniform_random_control':(sorted((g.choice(35,5,replace=False)+1).tolist()),int(g.integers(10))+1)}
    rows.append(dict(target=tgt,winners=sorted(wins),sb=wsb,period='confirmation' if t>=len(full)-40 else 'development',
        tickets={k:dict(main=m,sb=s,matches=len(set(m)&wins),sb_hit=int(s==wsb)) for k,(m,s) in sel.items()},
        standalone_rank_of_coverage=[rank_of(lg[0]['ticket']),rank_of(lg[1]['ticket'])],universe=len(U['C']),
        T_std=float(U['T'].std()),coverage_tickets_logged_T_rank=[lg[0]['T_rank'],lg[1]['T_rank']],weights_nonzero=bool(U['wsum']>0)))
n=len(rows);h=n//2;SD5=math.sqrt(5*(5/35)*(30/35)*(30/34));pm=hg(35,5,5)
def blk(y,seed):
    y=np.asarray(y,float);r=np.random.default_rng(seed);ix=(r.integers(0,len(y),(10000,math.ceil(len(y)/5)))[:,:,None]+np.arange(5))%len(y)
    return np.quantile(y[ix.reshape(10000,-1)[:,:len(y)]].mean(1),[.025,.975]).tolist()
NAMES=list(rows[0]['tickets']);res={};tests=[]
for k in NAMES:
    m=np.array([r['tickets'][k]['matches'] for r in rows]);s=np.array([r['tickets'][k]['sb_hit'] for r in rows])
    ps=float(sum(math.comb(n,j)*.1**j*.9**(n-j) for j in range(int(s.sum()),n+1)))
    v=np.array([r['tickets']['V1_fixed_slot (incumbent)']['matches'] for r in rows])
    res[k]=dict(n=n,mean_main=float(m.mean()),expected=5/7,p_main=float(pmean(m,35,5,5)),halves=[float(m[:h].mean()),float(m[h:].mean())],block95=blk(m-5/7,11),
        dist={j:int((m==j).sum()) for j in range(6)},ge2=int((m>=2).sum()),expected_ge2=float(n*pm[2:].sum()),ge3=int((m>=3).sum()),expected_ge3=float(n*pm[3:].sum()),
        sb_hits=int(s.sum()),sb_expected=n*.1,p_sb=ps,main2_plus_sb=int(((m>=2)&(s==1)).sum()),jackpots=int(((m==5)&(s==1)).sum()),
        diff_vs_incumbent=dict(mean=float((m-v).mean()),block95=blk(m-v,12)),
        distinct_tickets=len({(tuple(r['tickets'][k]['main']),r['tickets'][k]['sb']) for r in rows}),distinct_sb=len({r['tickets'][k]['sb'] for r in rows}),
        top_sb_share=Counter(r['tickets'][k]['sb'] for r in rows).most_common(1)[0][1]/n)
    if k!='uniform_random_control':tests+= [(k,'main',res[k]['p_main']),(k,'sb',ps)]
adj=holm([x[2] for x in tests]);H_={f'{a}:{b}':float(v) for (a,b,_),v in zip(tests,adj)}
for k in NAMES:res[k]['holm']={x.split(':')[1]:v for x,v in H_.items() if x.startswith(k+':')}
sac=[r['standalone_rank_of_coverage'] for r in rows if r['weights_nonzero']]
out=dict(targets=[rows[0]['target'],rows[-1]['target']],n=n,selectors=res,holm_family=len(tests),passing=[k for k in NAMES if res[k].get('holm',{}).get('main',1)<.05 or res[k].get('holm',{}).get('sb',1)<.05],
  coverage_standalone_ranks=dict(note='rank of each P0 coverage ticket among the 792 pool tickets by standalone score T (then EQ); 1 = top standalone',
     all_targets=dict(T1_median=float(np.median([r['standalone_rank_of_coverage'][0] for r in rows])),T2_median=float(np.median([r['standalone_rank_of_coverage'][1] for r in rows]))),
     targets_with_nonzero_weights=len(sac)),
  live_coverage_ranks={t:J(V/f'draw{t}/p0/p0_result.json')['tickets'][1:] for t in [1755,1756,1757]},
  null=dict(main_pmf=pm.tolist(),mean=5/7,sb=.1,jackpot=1/(math.comb(35,5)*10)),seed_control=SEED_RAND)
for t in out['live_coverage_ranks']:out['live_coverage_ranks'][t]=[dict(mains=x['mains'],T_rank=x.get('T_rank'),raw_T=x.get('raw_T')) for x in out['live_coverage_ranks'][t]]
save(O/'single_ticket_audit.json',out);save(O/'single_ticket_rows.json',rows)
for k,v in res.items():print(f"{k:28s} main {v['mean_main']:.3f} (p {v['p_main']:.3f} holm {v.get('holm',{}).get('main','-')}) SB {v['sb_hits']}/{n} (p {v['p_sb']:.3f}) ge3 {v['ge3']}/{v['expected_ge3']:.1f} 2+SB {v['main2_plus_sb']} diff {v['diff_vs_incumbent']['mean']:+.3f} distinct {v['distinct_tickets']} SBs {v['distinct_sb']} topSBshare {v['top_sb_share']:.2f}")
print(out['coverage_standalone_ranks'],out['live_coverage_ranks'],'passing',out['passing'])
