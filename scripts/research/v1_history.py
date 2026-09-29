"""Research-only reconstruction of V1 state at every historical cutoff.

Uses the unchanged V1 functions in scripts/analyze.py. For each cutoff it rebuilds:
  - the five V1 family number scores (A_long..E_pairs) and the V1 G marginal proxy,
  - the V1 walk-forward rows as a V1 run at that cutoff would see them (G re-frozen at
    that run's own confirmation boundary),
  - whether any model passes the V1 evidence gate at that cutoff,
  - the 20 V1 candidate tickets (exact copy of the selection lines of analyze.candidates()).
Validated against the frozen #2339, #2340 and #2341 candidate pools before use.
Never modifies V1 files.
"""
import sys,json
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'))
import analyze as a

def load(path):
    records=json.loads(Path(path).read_text());d=np.array([r['numbers'] for r in records])-1
    assert all(records[i]['draw_id']+1==records[i+1]['draw_id'] for i in range(len(records)-1))
    return records,d

def walk_cache(d,records,minimum=50,seed=a.SEED):
    """Per-origin V1 walk internals (identical to analyze.walk defaults): pools, objective values, A-F/H tickets."""
    A=a.indicator(d);out=[]
    for t in range(minimum,len(A)):
        ft=a.model_features(A[:t].copy());pool=a.sample(np.random.default_rng(seed+records[t]['draw_id']*101),512);val=a.objectives(pool,ft)
        tick=[pool[np.argmax(val[j])] for j in range(6)];h=a.sample(np.random.default_rng(seed+records[t]['draw_id']*1009),1)[0]
        truth=A[t];out.append(dict(index=t,draw_id=records[t]['draw_id'],pool=pool,val=val,
            m6=[int(truth[x].sum()) for x in tick],mH=int(truth[h].sum()),truth=truth,retained=ft[-1]))
    return out

def rows_for_cutoff(cache,c):
    """Walk rows a V1 run with last draw index c would produce (G frozen at its own boundary)."""
    n=c+1;boundary=n-40;prior=[];rows=[];frozen=None
    for w in cache:
        if w['index']>c:break
        t=w['index']
        if t>=boundary and frozen is None:frozen=a.ensemble_weights(prior)
        ew=frozen if frozen is not None else a.ensemble_weights(prior)
        g=w['pool'][np.argmax(ew@w['val'])];mg=int(w['truth'][g].sum())
        m=w['m6']+[mg,w['mH']];prior.append(m)
        rows.append(dict(draw_id=w['draw_id'],period='confirmation' if t>=boundary else 'development',matches=m))
    return rows

def gate(rows):
    """V1 evidence gate at this cutoff. Cheap Holm pre-check; full analyze.summaries only if needed."""
    conf=[r for r in rows if r['period']=='confirmation']
    if not conf:return [],1.0
    m=np.array([r['matches'] for r in conf]);ps=[a.null_p(m[:,j]) for j in range(8)];hp=a.holm(ps)
    if min(hp)>=.05:return [],float(min(hp))
    if len(conf)<len(rows):
        s=a.summaries(rows);return [r['model'] for r in s if r['qualifies']],float(min(hp))
    # Short history: no development rows, so analyze.summaries cannot run. Apply the V1 qualifies formula
    # directly (own seeded bootstrap stream); flagged as approximate by the caller via APPROX.
    rng=np.random.default_rng(a.SEED+10);q=[]
    for j,name in enumerate(a.NAMES):
        y=m[:,j];ci=a.block_ci(y,rng);older=y[:len(y)//2].mean();recent=y[len(y)//2:].mean()
        if hp[j]<.05 and ci[0]>a.BASE and min(older,recent)>a.BASE:q.append(name)
    APPROX.append(rows[-1]['draw_id']);return q,float(min(hp))
APPROX=[]

POOL4096=None
def candidate_tickets(ft,ew):
    """Exact copy of the ticket-selection lines of analyze.candidates()."""
    global POOL4096
    if POOL4096 is None:POOL4096=a.sample(np.random.default_rng(a.SEED+999),4096)
    pool=POOL4096;values=a.objectives(pool,ft);val=np.vstack([values,ew@values]);selected=[];sources=[]
    for j in range(7):
        count=0
        for idx in np.argsort(-val[j],kind='stable'):
            d=pool[idx]
            if all(len(set(d)&set(old))<=3 for old in selected):selected.append(d);sources.append(a.NAMES[j]);count+=1
            if count==(1 if j==6 else 3):break
    rng=np.random.default_rng(a.SEED+555)
    while len(selected)<20:
        d=a.sample(rng,1)[0]
        if all(len(set(d)&set(old))<=3 for old in selected):selected.append(d);sources.append('H_random')
    return [dict(id=f'C{i+1:02}',numbers=(d+1).tolist(),generator=s) for i,(d,s) in enumerate(zip(selected,sources))]

def state_at_cutoff(d,records,cache,c,with_gate=True):
    A=a.indicator(d[:c+1]);ft=a.model_features(A);rows=rows_for_cutoff(cache,c)
    ew=a.ensemble_weights([r['matches'] for r in rows]);cands=candidate_tickets(ft,ew)
    q,minholm=gate(rows) if with_gate else ([],None)
    return dict(cutoff=records[c]['draw_id'],target=records[c]['draw_id']+1,family_scores=ft[0],g_proxy=ew[:5]@ft[0],
                ensemble_weights=ew,retained_pairs=ft[-1],candidates=cands,qualifiers=q,min_conf_holm_p=minholm,n_walk_rows=len(rows))

def validate(d,records,cache):
    """Reconstruction must equal the frozen V1 pools for #2339 (cutoff 2338), #2340, #2341."""
    frozen={2338:R/'results/candidates.json',2339:R/'results/lotto/draw2340/candidates.json',2340:R/'results/lotto/draw2341/candidates.json'}
    idx={r['draw_id']:i for i,r in enumerate(records)};res={}
    for cut,p in frozen.items():
        if cut not in idx:continue
        s=state_at_cutoff(d,records,cache,idx[cut]);f=json.loads(p.read_text())
        res[cut]=dict(numbers_match=[c['numbers'] for c in s['candidates']]==[c['numbers'] for c in f],
                      generators_match=[c['generator'] for c in s['candidates']]==[c['generator'] for c in f],qualifiers=s['qualifiers'])
    return res
