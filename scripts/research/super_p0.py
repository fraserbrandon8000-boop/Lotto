"""Super Lotto P0 portfolio research library. Implements results/super_lotto/p0_protocol/DESIGN_PRECOMMIT.json.
Super Lotto only: imports the unchanged Super Lotto V1 (super_lotto.py), its validated reconstruction (super_history.py)
and the game-agnostic common.py. No Lotto code, data or parameters."""
import sys,math,itertools
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts/research'))
import super_lotto as sl
from common import holm,pmean,z

MAIN=['A_long','B_recent','C_gap','D_trend','E_pairs'];SBM=['S_long','S_recent','S_gap','S_trend','S_transition']
MINPRIOR=25;K_OPTIONS=[8,10,12,15];K_DEFAULT=12;ETA=1.0;EXCEPTION_T=1.0;SB_SD=math.sqrt(99/12)/9
SEEDS=dict(V1=2026092109,pool_bootstrap=2026093011,comparators_base=2026093021,null_mc_base=2026093031,gate_bootstrap=2026093041,sb_random_base=2026093051,random_control=2026093061,ap_null_mc=2026093071)
AP0=sum((1+4*(i-1)/34)/i for i in range(1,36))/35            # exact E[AP], 5 relevant among 35, random order
def ap_null_sd(sims=200000):
    r=np.random.default_rng(SEEDS['ap_null_mc']);pos=np.sort(np.argsort(r.random((sims,35)),1)[:,:5],1)+1
    return float(((np.arange(1,6)/pos).mean(1)).std())
AP_SD=ap_null_sd()

def fam_scores(o):
    """5 x 35 main family scores (A-D V1 features, E = z(pair sums)) and informative flags."""
    e=z(o['mat'].sum(0));S=np.vstack([o['s'],e]);return S,[bool(np.std(x)>1e-10) for x in S]
def v1_ap(score,truth,jit):
    order=np.argsort(-(score+jit));rel=truth[order];return float(np.sum(rel*np.cumsum(rel)/np.arange(1,36))/5)
def midrank_pct10(x,actual):
    v=x[actual];better=np.sum(x>v+1e-12);eq=np.sum(np.abs(x-v)<=1e-12);mid=better+(eq+1)/2;return (10-mid)/9-.5

def build_history(C,seed=sl.SEED):
    """Per V1 origin with a known outcome: AP excess per main family, SB percentile excess per SB model, V1 E/F ticket hits."""
    H=[]
    for o in C:
        if 'truth' not in o:continue
        S,inf=fam_scores(o);jit=np.random.default_rng(seed+o['target']*31).random(35)*1e-10
        e={m:(v1_ap(S[j],o['truth'],jit)-AP0 if inf[j] else None) for j,m in enumerate(MAIN)}
        q={m:(midrank_pct10(o['ss'][j],o['truth_sb']) if np.std(o['ss'][j])>1e-12 else None) for j,m in enumerate(SBM)}
        H.append(dict(t=o['t'],target=o['target'],e=e,q=q,mE=o['m6'][4],mF=o['m6'][5],pair_inf=o['pair_informative']))
    return H

def _cred(zs,raws,pfun):
    """Holm-corrected credibility c = max(0, 1 - 2 p_Holm) * halves rule."""
    keys=[k for k in zs if len(zs[k])>=MINPRIOR];out={k:dict(n=len(zs[k]),p=None,p_holm=None,halves=None,c=0.) for k in zs}
    if not keys:return out
    ps=[pfun(k) for k in keys];ph=holm(ps)
    for k,p,h in zip(keys,ps,ph):
        r=np.array(raws[k]);hv=bool(r[:len(r)//2].mean()>0 and r[len(r)//2:].mean()>0)
        out[k]=dict(n=len(zs[k]),mean=float(np.mean(raws[k])),p=float(p),p_holm=float(h),halves=hv,c=float(max(0.,1-2*h)*hv))
    return out
def credibility(H,t):
    prior=[h for h in H if h['t']<t]
    e={m:[h['e'][m] for h in prior if h['e'][m] is not None] for m in MAIN}
    main=_cred(e,e,lambda m:0.5*math.erfc((np.mean(e[m])/(AP_SD/math.sqrt(len(e[m]))))/math.sqrt(2)))
    q={m:[h['q'][m] for h in prior if h['q'][m] is not None] for m in SBM}
    sb=_cred(q,q,lambda m:0.5*math.erfc((np.mean(q[m])/(SB_SD/math.sqrt(len(q[m]))))/math.sqrt(2)))
    th={'E_ticket':[h['mE'] for h in prior if h['pair_inf']],'F_ticket':[h['mF'] for h in prior]}
    tr={k:[x-5/7 for x in v] for k,v in th.items()}
    tick=_cred(th,tr,lambda k:pmean(np.array(th[k]),35,5,5))
    return dict(main=main,sb=sb,ticket=tick)

def discovery(o,cred):
    S,inf=fam_scores(o);c=np.array([cred['main'][m]['c'] for m in MAIN])
    M=c@S;EQ=S[[j for j in range(5) if inf[j]]].mean(0) if any(inf) else np.zeros(35)
    order=sorted(range(35),key=lambda i:(-round(float(M[i]),12),-round(float(EQ[i]),12),i))
    ss=o['ss'];sinf=[j for j in range(5) if np.std(ss[j])>1e-12];cs=np.array([cred['sb'][m]['c'] for m in SBM])
    Q=cs@ss;EQS=ss[sinf].mean(0) if sinf else np.zeros(10)
    sborder=sorted(range(10),key=lambda b:(-round(float(Q[b]),12),-round(float(EQS[b]),12),b))
    eqorder=sorted(range(10),key=lambda b:(-round(float(EQS[b]),12),b))
    return dict(S=S,M=M,EQ=EQ,order=[i+1 for i in order],Q=Q,EQS=EQS,sborder=[b+1 for b in sborder],sb_eq_order=[b+1 for b in eqorder])

def Zs(v):
    s=np.std(v);return np.zeros_like(v) if s<1e-12 else (v-v.mean())/s
def universe(o,disc,cred,K):
    pool=sorted(disc['order'][:K]);Cc=np.array(list(itertools.combinations(pool,5)))-1;S=disc['S'];comp={}
    for j,m in enumerate(MAIN):comp[m]=Zs(S[j][Cc].sum(1))
    I,Jx=np.triu_indices(5,1);comp['pair']=Zs(2*o['mat'][Cc[:,I],Cc[:,Jx]].sum(1)/20)
    comp['struct']=Zs(-np.mean(((sl.structures(Cc)-o['mean'])/o['sd'])**2,axis=1))
    w={m:cred['main'][m]['c'] for m in MAIN};w['pair']=cred['ticket']['E_ticket']['c'];w['struct']=cred['ticket']['F_ticket']['c']
    T=sum(w[k]*comp[k] for k in comp);EQt=disc['EQ'][Cc].sum(1)
    return dict(C=Cc,T=np.asarray(T,float),EQ=EQt,comp=comp,w=w,wsum=float(sum(w.values())),pool=pool)

def _best(idx,J,EQ):
    idx=np.asarray(idx);k=np.lexsort((idx,-np.round(EQ[idx],12),-np.round(J[idx],12)));return int(idx[k[0]])
def portfolio(U,disc,v1_main,K):
    C=U['C'];T=U['T'];EQ=U['EQ'];sel=[np.array(v1_main)-1];log=[]
    pn=np.array(U['pool'])-1;mass=np.zeros(35);ex=np.exp(disc['M'][pn]-disc['M'][pn].max());mass[pn]=ex/ex.sum()
    inC=np.zeros((len(C),35),bool);inC[np.arange(len(C))[:,None],C]=True
    for k in range(2):
        cov_=np.zeros(35,bool)
        for s in sel:cov_[s]=True
        cov=(inC&~cov_).astype(float)@mass/(5/K);J=T+ETA*cov;ov=np.stack([inC[:,s].sum(1) for s in sel],1).max(1)
        L=1
        while L<=3 and not (ov<=L).any():L+=1
        feas=np.nonzero(ov<=L)[0];exc=bool(U['wsum']>0 and T.max()-T[feas].max()>EXCEPTION_T)
        b=_best(np.arange(len(C)) if exc else feas,J,EQ);sel.append(C[b])
        log.append(dict(ticket=(C[b]+1).tolist(),T=float(T[b]),J=float(J[b]),coverage=float(cov[b]),overlap_limit=L,evidence_exception=exc,max_overlap=int(ov[b]),feasible=int(len(feas)),
                        T_rank=int(np.sum(T>T[b]))+1,contributions={k_:float(U['w'][k_]*U['comp'][k_][b]) for k_ in U['comp']}))
    return log
def top3_standalone(U):
    idx=np.lexsort((np.arange(len(U['C'])),-np.round(U['EQ'],12),-np.round(U['T'],12)))[:3];return [(U['C'][i]+1).tolist() for i in idx]

def assign_sb(rule,disc,v1_sb,target):
    if rule=='A':b=disc['sborder'][0];return [b,b]
    if rule=='B':o=[b for b in disc['sb_eq_order'] if b!=v1_sb];return o[:2]
    if rule=='C':o=[b for b in disc['sborder'] if b!=v1_sb];return o[:2]
    if rule=='D':r=np.random.default_rng(SEEDS['sb_random_base']+target);return [int(r.integers(10))+1,int(r.integers(10))+1]
    raise ValueError(rule)

def stats(tickets,sbs,win,wsb):
    w=set(win);m=[len(set(t)&w) for t in tickets];s=[int(b==wsb) for b in sbs];ov=[len(set(x)&set(y)) for x,y in itertools.combinations(tickets,2)]
    bi=int(np.argmax(m))
    return dict(main=m,best=max(m),total=sum(m),ch_total=sum(m[1:]),ge2=int(max(m)>=2),ge3=int(max(m)>=3),ge4=int(max(m)>=4),five=int(max(m)==5),
                sb=s,any_sb=int(max(s)),sb_total=sum(s),ch_sb=sum(s[1:]),best_ticket_sb=s[bi],any_ge2_sb=int(any(mm>=2 and ss for mm,ss in zip(m,s))),any_ge3_sb=int(any(mm>=3 and ss for mm,ss in zip(m,s))),
                unique=len(set().union(*map(set,tickets))),distinct_sbs=len(set(sbs)),mean_overlap=float(np.mean(ov)))
def rt(r):return sorted((r.choice(35,5,replace=False)+1).tolist())
def rdiv(r,fixed,n,limit=1):
    out=[]
    while len(out)<n:
        t=rt(r)
        if all(len(set(t)&set(s))<=limit for s in fixed+out):out.append(t)
    return out
def null_pmfs(tickets,sbs,rng,sims=20000):
    D=np.zeros((sims,35),bool);D[np.arange(sims)[:,None],np.argsort(rng.random((sims,35)),1)[:,:5]]=True;SB=rng.integers(0,10,sims)+1
    Tm=np.zeros((len(tickets),35),int)
    for k,t in enumerate(tickets):Tm[k,np.array(t)-1]=1
    m=D.astype(int)@Tm.T;ch=m[:,1:].sum(1);best=m.max(1);chs=sum((SB==b).astype(int) for b in sbs[1:])
    return dict(ch_total=np.bincount(ch,minlength=11)/sims,best=np.bincount(best,minlength=6)/sims,ch_sb=np.bincount(chs,minlength=3)/sims)
def conv_p(pmfs,obs):
    p=np.array([1.])
    for q in pmfs:p=np.convolve(p,q)
    return float(p[int(obs):].sum())
def block_ci(y,seed,reps=10000):
    y=np.asarray(y,float);n=len(y);r=np.random.default_rng(seed);ix=(r.integers(0,n,(reps,math.ceil(n/5)))[:,:,None]+np.arange(5))%n
    return np.quantile(y[ix.reshape(reps,-1)[:,:n]].mean(1),[.025,.975]).tolist()
def hg35(K):return np.array([math.comb(5,k)*math.comb(30,K-k)/math.comb(35,K) if 0<=K-k<=30 else 0. for k in range(6)])
