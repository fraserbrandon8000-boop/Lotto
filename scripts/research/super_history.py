"""Research-only reconstruction of Super Lotto V1 state at every historical cutoff.
Uses the unchanged V1 functions in scripts/research/super_lotto.py and the game-agnostic common.py only.
Validated against the frozen #1753 and #1754 candidate pools before use. Never modifies V1 files."""
import sys,json
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts/research'))
import super_lotto as sl
from common import holm,pmean,blockci,ind,sample,z

def load(path):
    records=json.loads(Path(path).read_text(encoding='utf-8-sig'))
    assert all(records[i]['draw_id']+1==records[i+1]['draw_id'] for i in range(len(records)-1))
    d=np.array([r['numbers'] for r in records])-1;sb=np.array([r['super_ball'] for r in records])-1;ids=[r['draw_id'] for r in records]
    return records,d,sb,ids

def origin(d,sb,ids,t,seed=sl.SEED):
    """Everything V1's walk() computes at origin t that does not depend on ensemble weights (identical code path)."""
    a=ind(d,35);b=ind(sb[:,None],10);n=len(a);aa=a[:t];bb=b[:t]
    s=sl.features(aa);ss=sl.features(bb);mat,_,_,_=sl.pairmat(aa);st=sl.structures(d[:t]);mean=st.mean(0);sd=np.maximum(st.std(0),1)
    transitions=bb[:-1].T@bb[1:];trials=int(bb[:-1,sb[t-1]].sum());last=sb[t-1]
    pp=[sl.bp(trials,.1,x) for x in transitions[last]] if trials else [1]*10;tv=np.where(holm(pp)<.05,transitions[last]/max(1,trials)-.1,0);ss=np.vstack([ss,z(tv)])
    targetid=ids[t] if t<n else ids[-1]+1
    pool=sample(np.random.default_rng(seed+targetid*101),512,35,5);v=sl.objective(pool,s,mat,mean,sd)
    h=sample(np.random.default_rng(seed+targetid*503),1,35,5)[0];jit=np.random.default_rng(seed+targetid*67).random(10)*1e-10
    srand=int(np.random.default_rng(seed+targetid*907).integers(10))
    o=dict(t=t,target=targetid,s=s,ss=ss,mat=mat,mean=mean,sd=sd,pool=pool,v=v,h=h,jit=jit,srand=srand,pair_informative=bool(np.std(mat.sum(0))>1e-10))
    if t<n:
        o['truth']=a[t];o['truth_sb']=int(sb[t])
        o['m6']=[int(a[t,pool[np.argmax(x)]].sum()) for x in v];o['mH']=int(a[t,h].sum())
        o['sb5']=[int(np.argmax(x+jit)) for x in ss];o['s5']=[int(p==sb[t]) for p in o['sb5']];o['sR']=int(srand==sb[t])
    return o

def cache(d,sb,ids,start=50):return [origin(d,sb,ids,t) for t in range(start,len(d)+1)]

def run_at_cutoff(C,c_index):
    """Replay V1 walk rows and final fit for a V1 run whose last draw has index c_index (dataset length n=c_index+1)."""
    n=c_index+1;mh=[];sh=[];mwf=None;swf=None;rows=[]
    for o in C:
        t=o['t']
        if t>n:break
        if t>=n-40 and mwf is None:mwf=sl.weights(mh,6,sl.BASE);swf=sl.weights(sh,5,.1)
        mw=mwf if mwf is not None else sl.weights(mh,6,sl.BASE);sw=swf if swf is not None else sl.weights(sh,5,.1)
        if t==n:
            sbpred=o['sbpred_final']=[int(np.argmax(x+o['jit'])) for x in np.vstack([o['ss'],sw@o['ss']])]+[o['srand']]
            return rows,dict(scores=o['s'],pair_matrix=o['mat'],mean=o['mean'],sd=o['sd'],main_weights=mw,sb_weights=sw,sb_scores=o['ss'],sb_predictions=sbpred,target=o['target'])
        g=o['pool'][np.argmax(mw@o['v'])];mg=int(o['truth'][g].sum());se=int(np.argmax(sw@o['ss']+o['jit']))
        hits=o['m6']+[mg,o['mH']];sbh=o['s5']+[int(se==o['truth_sb']),o['sR']];mh.append(hits);sh.append(sbh)
        rows.append(dict(t=t,draw_id=o['target'],period='confirmation' if t>=n-40 else 'development',main_hits=hits,SB_hits=sbh,SB_predictions=[x+1 for x in o['sb5']+[se,o['srand']]]))
    raise ValueError('cutoff beyond cache')

def gate(rows):
    """V1 qualifies rule (performance()) for main and SB, confirmation period only."""
    conf=[r for r in rows if r['period']=='confirmation'];out={'main':[],'SB':[]};minp={}
    for domain,names,key,NN,KK,base in [('main',sl.MN,'main_hits',35,5,sl.BASE),('SB',sl.SN,'SB_hits',10,1,.1)]:
        ys=[np.array([r[key][j] for r in conf]) for j in range(len(names))];ps=holm([pmean(y,NN,KK,KK) for y in ys]);minp[domain]=float(min(ps))
        for name,y,p in zip(names,ys,ps):
            if p<.05 and blockci(y)[0]>base and min(y[:len(y)//2].mean(),y[len(y)//2:].mean())>base:out[domain].append(name)
    return out,minp

POOL4096=None
def candidates(fit):
    """Exact copy of the selection lines of super_lotto.candidate_set() (tickets, generators, cyclic SB)."""
    global POOL4096
    if POOL4096 is None:POOL4096=sample(np.random.default_rng(sl.SEED+333),4096,35,5)
    pool=POOL4096;vals=sl.objective(pool,fit['scores'],fit['pair_matrix'],fit['mean'],fit['sd']);vals=np.vstack([vals,fit['main_weights']@vals]);selected=[];gens=[]
    for j in range(7):
        count=0
        for i in np.argsort(-vals[j],kind='stable'):
            t=pool[i]
            if all(len(set(t)&set(x))<=3 for x in selected):selected.append(t);gens.append(j);count+=1
            if count==(1 if j==6 else 3):break
    while len(selected)<20:
        x=sample(np.random.default_rng(sl.SEED+555+len(selected)),1,35,5)[0]
        if all(len(set(x)&set(y))<=3 for y in selected):selected.append(x);gens.append(7)
        else:return None   # V1 would raise 'Diversity fallback needs new seed counter'
    return [dict(id=f'SL{i+1:02}',main=(t+1).tolist(),super_ball=fit['sb_predictions'][i%7]+1,main_generator=sl.MN[j],SB_generator=sl.SN[i%7]) for i,(t,j) in enumerate(zip(selected,gens))]

def v1_fallback(cands):return cands[int(np.random.default_rng(sl.SEED).integers(len(cands)))]

def validate(C,ids):
    """Reconstruction must equal the frozen pools: #1753 (cutoff 1752) and #1754 (cutoff 1753)."""
    frozen={1752:R/'results/super_lotto/candidates.json',1753:R/'results/super_lotto/draw1754/candidates.json'};idx={d:i for i,d in enumerate(ids)};res={}
    for cut,p in frozen.items():
        if cut not in idx:continue
        rows,fit=run_at_cutoff(C,idx[cut]);cs=candidates(fit);f=json.loads(p.read_text(encoding='utf-8-sig'))
        res[cut]=dict(mains=[c['main'] for c in cs]==[c['main'] for c in f],super_balls=[c['super_ball'] for c in cs]==[c['super_ball'] for c in f],
                      generators=[(c['main_generator'],c['SB_generator']) for c in cs]==[(c['main_generator'],c['SB_generator']) for c in f],
                      gate=gate(rows)[0],fallback=v1_fallback(cs)['id'])
    return res

def v1_ticket(fit):
    """V1 Ticket 1 at a cutoff: the fixed-seed fallback pick. If V1's H fill would raise (V1 could not run),
    return the SL10 slot anyway (index 9 = D_trend's top ticket, fixed before the H fill) with a flag."""
    cs=candidates(fit)
    if cs is not None:return v1_fallback(cs),False
    global POOL4096
    pool=POOL4096;vals=sl.objective(pool,fit['scores'],fit['pair_matrix'],fit['mean'],fit['sd']);vals=np.vstack([vals,fit['main_weights']@vals]);selected=[];gens=[]
    for j in range(7):
        count=0
        for i in np.argsort(-vals[j],kind='stable'):
            t=pool[i]
            if all(len(set(t)&set(x))<=3 for x in selected):selected.append(t);gens.append(j);count+=1
            if count==(1 if j==6 else 3):break
    idx=int(np.random.default_rng(sl.SEED).integers(20));t=selected[idx]
    return dict(id=f'SL{idx+1:02}',main=(t+1).tolist(),super_ball=fit['sb_predictions'][idx%7]+1,main_generator=sl.MN[gens[idx]],SB_generator=sl.SN[idx%7]),True
