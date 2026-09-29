"""P0 portfolio research library. Implements results/lotto/p0_protocol/DESIGN_PRECOMMIT.json exactly.
Uses unchanged V1 functions from scripts/analyze.py. P0 is a research challenger, never V1/V2."""
import sys,math,itertools
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'))
import analyze as a

FAM=['A_long','B_recent','C_gap','D_trend','E_pairs']
SIGMA=math.sqrt(((38**2-1)/12)/37**2/6*(32/37))          # exact null SD of per-origin winner-percentile excess
SD0=math.sqrt(6*(6/38)*(32/38)*(32/37))                  # exact null SD of ticket matches
TAU=0.09;MINPRIOR=20;K_OPTIONS=[10,12,15,20];K_DEFAULT=15;ETA=1.0;BASE=36/38
SEEDS=dict(V1=20260919,pool_bootstrap=20260930,comparators_base=20260931,null_mc_base=20260932,gate_bootstrap=20260933,random_control_2342=20260930)

def midrank_pct(s):
    """pct = (38 - midrank)/37 with midranks for exact ties (descending score). Flat -> all 0.5."""
    s=np.asarray(s,float);order=np.argsort(-s,kind='stable');ranks=np.empty(38);i=0;ss=s[order]
    while i<38:
        j=i
        while j+1<38 and abs(ss[j+1]-ss[i])<=1e-12:j+=1
        ranks[order[i:j+1]]=(i+j)/2+1;i=j+1
    return (38-ranks)/37,ranks

def origin_features(d,t):
    """V1 features from draws strictly before index t."""
    return a.model_features(a.indicator(d[:t]))

def build_history(d,records,minimum=50):
    """Per V1 origin u (index>=minimum): family scores, informative flags, winner-percentile excess x,
    V1 E_pairs/F_structure walk ticket matches (from the unchanged V1 walk), retained pairs."""
    A=a.indicator(d);H=[]
    for u in range(minimum,len(d)):
        ft=origin_features(d,u);win=np.nonzero(A[u])[0]
        pool=a.sample(np.random.default_rng(a.SEED+records[u]['draw_id']*101),512);val=a.objectives(pool,ft)
        mE=int(A[u][pool[np.argmax(val[4])]].sum());mF=int(A[u][pool[np.argmax(val[5])]].sum())
        x={};inf={};wr={}
        for j,f in enumerate(FAM):
            sc=ft[0][j];inf[f]=bool(np.std(sc)>1e-12);p,rk=midrank_pct(sc);x[f]=float(p[win].mean()-.5);wr[f]=float(rk[win].mean())
        H.append(dict(index=u,draw_id=records[u]['draw_id'],x=x,informative=inf,winner_midrank=wr,mE=mE,mF=mF,retained=int(ft[-1]),scores=ft[0]))
    return H

def shrunk_weight(z_list,raw_list=None):
    """d = mean(z) * n tau^2/(n tau^2 + 1); h from chronological halves of raw values; w = max(0,d)*h."""
    n=len(z_list)
    if n<MINPRIOR:return dict(n=n,dbar=None,d=0.,h=0.,w=0.)
    z=np.array(z_list);raw=np.array(raw_list if raw_list is not None else z_list)
    dbar=float(z.mean());d=dbar*n*TAU**2/(n*TAU**2+1)
    h1=raw[:n//2].mean()>0;h2=raw[n//2:].mean()>0;h=1. if (h1 and h2) else (.5 if (h1 or h2) else 0.)
    return dict(n=n,dbar=dbar,d=float(d),h=h,w=float(max(0.,d)*h))

def weights_at(H,t_index):
    """Weights for a P0 target at V1 index t_index, using only V1 origins with index < t_index."""
    prior=[h for h in H if h['index']<t_index];out={}
    for f in FAM:
        xs=[h['x'][f] for h in prior if h['informative'][f]];out[f]=shrunk_weight([v/SIGMA for v in xs],xs)
    pe=[(h['mE']-BASE)/SD0 for h in prior if h['retained']>0];out['pair']=shrunk_weight(pe)
    pf=[(h['mF']-BASE)/SD0 for h in prior];out['struct']=shrunk_weight(pf)
    return out

def discovery(scores,W):
    """M_i = sum_f w_f z_f,i; EQ_i = mean z over informative A-E families; ordering by (-M, -EQ, number)."""
    inf=[j for j in range(5) if np.std(scores[j])>1e-12]
    M=sum(W[f]['w']*scores[j] for j,f in enumerate(FAM));M=np.asarray(M,float)
    EQ=scores[inf].mean(0) if inf else np.zeros(38)
    order=sorted(range(38),key=lambda i:(-round(M[i],12),-round(EQ[i],12),i))
    return M,EQ,[i+1 for i in order]

def Z(v):
    s=np.std(v);return np.zeros_like(v) if s<1e-12 else (v-v.mean())/s

def universe(pool_numbers,ft,W,M,EQ):
    """Enumerate every 6-combination of the pool and compute T, EQ(t) and components."""
    nums=sorted(pool_numbers);C=np.array(list(itertools.combinations(nums,6)))-1   # 0-based, lexicographic
    scores,mat,means,sd,_=ft;comp={}
    for j,f in enumerate(FAM):comp[f]=Z(scores[j][C].mean(1))
    I,Jj=np.triu_indices(6,1);comp['pair']=Z(2*mat[C[:,I],C[:,Jj]].sum(1)/30)
    comp['struct']=Z(-np.mean(((a.structure(C)-means)/sd)**2,axis=1))
    T=sum(W[f]['w']*comp[f] for f in FAM)+W['pair']['w']*comp['pair']+W['struct']['w']*comp['struct']
    return dict(C=C,T=np.asarray(T,float),EQ=EQ[C].mean(1),comp=comp)

def _best(idx,J,EQt):
    """argmax J, ties by higher EQ then lexicographic (enumeration order)."""
    idx=np.asarray(idx);key=np.lexsort((idx,-np.round(EQt[idx],12),-np.round(J[idx],12)));return int(idx[key[0]])

def portfolio(U,M,pool_numbers,v1_ticket,K):
    C=U['C'];T=U['T'];EQt=U['EQ'];selected=[np.array(v1_ticket)-1];picks=[];log=[]
    mass=np.zeros(38);pn=np.array(sorted(pool_numbers))-1;mm=np.maximum(.01,1+M[pn]);mass[pn]=mm/mm.sum()
    inC=np.zeros((len(C),38),bool);inC[np.arange(len(C))[:,None],C]=True
    wsum=None
    for k in range(2):
        covered=np.zeros(38,bool)
        for s in selected:covered[s]=True
        cov=(inC&~covered).astype(float)@mass/(6/K);J=T+ETA*cov
        ov=np.stack([inC[:,s].sum(1) for s in selected],1).max(1)
        L=2
        while L<=4 and not (ov<=L).any():L+=1
        feas=np.nonzero(ov<=L)[0];allidx=np.arange(len(C));exception=False
        if U['wsum']>0 and T.max()-T[feas].max()>2*T.std():exception=True
        b=_best(allidx if exception else feas,J,EQt)
        picks.append(b);selected.append(C[b])
        log.append(dict(ticket=(C[b]+1).tolist(),T=float(T[b]),J=float(J[b]),coverage=float(cov[b]),overlap_limit=L,evidence_exception=exception,
                        max_overlap_with_selected=int(ov[b]),feasible_count=int(len(feas))))
    return log

def top3_standalone(U):
    idx=np.lexsort((np.arange(len(U['C'])),-np.round(U['EQ'],12),-np.round(U['T'],12)))[:3]
    return [(U['C'][i]+1).tolist() for i in idx]

def port_stats(tickets,win):
    w=set(win);m=[len(set(t)&w) for t in tickets];ov=[len(set(x)&set(y)) for x,y in itertools.combinations(tickets,2)]
    return dict(matches=m,best=max(m),total=sum(m),challengers_total=sum(m[1:]),ge3=int(max(m)>=3),ge4=int(max(m)>=4),ge5=int(max(m)>=5),six=int(max(m)==6),
                unique=len(set().union(*map(set,tickets))),mean_overlap=float(np.mean(ov)))

def random_ticket(rng):return sorted((rng.choice(38,6,replace=False)+1).tolist())
def random_diverse(rng,fixed,n):
    out=[];tries=0
    while len(out)<n:
        t=random_ticket(rng);tries+=1
        if all(len(set(t)&set(s))<=2 for s in fixed+out):out.append(t)
    return out

def null_pmfs(tickets,rng,sims=20000):
    """Per-origin null pmfs (uniform draws) of challengers_total, best and ge3 for a fixed portfolio."""
    D=np.zeros((sims,38),bool);D[np.arange(sims)[:,None],np.argsort(rng.random((sims,38)),1)[:,:6]]=True
    Tm=np.zeros((len(tickets),38),bool)
    for k,t in enumerate(tickets):Tm[k,np.array(t)-1]=True
    m=D.astype(int)@Tm.T.astype(int);ch=m[:,1:].sum(1);best=m.max(1)
    return dict(challengers_total=np.bincount(ch,minlength=13)/sims,best=np.bincount(best,minlength=7)/sims,ge3=np.array([np.mean(best<3),np.mean(best>=3)]))

def conv_p(pmfs,observed):
    p=np.array([1.])
    for q in pmfs:p=np.convolve(p,q)
    return float(p[int(observed):].sum())

def block_lb(y,seed,reps=10000):
    y=np.asarray(y,float);n=len(y);rng=np.random.default_rng(seed);ix=(rng.integers(0,n,(reps,math.ceil(n/5)))[:,:,None]+np.arange(5))%n
    means=y[ix.reshape(reps,-1)[:,:n]].mean(1);return np.quantile(means,[.025,.975]).tolist()

def hg_pmf(K):return np.array([math.comb(6,k)*math.comb(32,K-k)/math.comb(38,K) for k in range(7)])
