"""M0 — Sequential Draw Reconstruction (independent research experiment; not V1, not P0).
Implements results/lotto_m0/MODEL_REGISTRY.json exactly. Lotto data only (#2161-#2343). Pure numpy.
Every model function receives only x[:t] (draws strictly before the target)."""
import json,math,itertools,hashlib
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2]
N=38;K=6;CN=math.comb(38,6);P0=6/38;LOGIT0=math.log(P0/(1-P0))
# ------------------------------------------------------------------ data
def load_data():
    recs=json.loads((R/'results/lotto/draw2343/draws.json').read_text())
    recs=recs+[dict(draw_id=2343,date='2026-10-03',numbers=[4,7,13,23,33,35],bonus=38)]
    for i,r in enumerate(recs):
        assert len(set(r['numbers']))==6 and all(1<=v<=38 for v in r['numbers'])
        if i:assert r['draw_id']==recs[i-1]['draw_id']+1
    D=np.array([sorted(r['numbers']) for r in recs],dtype=np.int64)
    X=np.zeros((len(D),N));X[np.arange(len(D))[:,None],D-1]=1
    ids=[r['draw_id'] for r in recs];h=hashlib.sha256(json.dumps([[r['draw_id'],sorted(r['numbers'])] for r in recs]).encode()).hexdigest()
    return D,X,ids,h
# ------------------------------------------------------------------ universe
_U=None
def universe():
    global _U
    if _U is None:
        C=np.array(list(itertools.combinations(range(N),6)),dtype=np.int64)
        cols=[C[:,j].copy() for j in range(6)];mask=(np.int64(1)<<C).sum(1);order=np.argsort(mask)
        _U=dict(C=C,cols=cols,mask_sorted=mask[order],mask_order=order)
    return _U
def comb_index(nums):
    U=universe();m=sum(1<<(v-1) for v in nums);i=np.searchsorted(U['mask_sorted'],m);assert U['mask_sorted'][i]==m;return int(U['mask_order'][i])
def additive(L):
    U=universe();s=np.zeros(CN)
    for c in U['cols']:s+=L[c]
    return s
def pair_term(W):
    U=universe();s=np.zeros(CN);c=U['cols']
    for a,b in itertools.combinations(range(6),2):s+=W[c[a],c[b]]
    return s
def lse(s):m=s.max();return float(m+np.log(np.exp(s-m).sum()))
def top_list(s,k=1000):
    idx=np.argpartition(-s,k)[:k];o=np.lexsort((idx,-s[idx]));return idx[o]
def evaluate_scores(s,actual,normalisable,L=None,p=None):
    """Freeze-then-reveal: everything up to `frozen` is computed without `actual`."""
    U=universe();top=top_list(s);primary=(U['C'][top[0]]+1).tolist()
    frozen=dict(primary=primary,top10=[(U['C'][i]+1).tolist() for i in top[:10]])
    if normalisable:
        Z=lse(s);P=np.exp(s-Z);frozen['entropy_nats']=float(Z-(P*s).sum());frozen['logZ']=Z
    if actual is None:return frozen,None
    ai=comb_index(actual);sa=s[ai];gt=int((s>sa).sum());eq=int((s==sa).sum());rank=1+gt+(eq-1)/2
    aset=set(actual);tm=[len(set((U['C'][i]+1).tolist())&aset) for i in top]
    res=dict(rank=rank,u=(rank-.5)/CN,top={k:bool(rank<=k) for k in [1,10,100,1000,10000,100000]},primary_matches=len(set(primary)&aset),
             best_top10=max(tm[:10]),best_top100=max(tm[:100]),best_top1000=max(tm))
    if normalisable:res['logscore']=float(sa-frozen['logZ']+math.log(CN))
    if L is not None:
        o=np.argsort(-L,kind='stable');pos=np.empty(N);pos[o]=np.arange(1,N+1)
        # mid-ranks for ties
        for v in np.unique(L):
            m=L==v
            if m.sum()>1:pos[m]=pos[m].mean()
        wr=[float(pos[a-1]) for a in actual];res['winner_ranks']=sorted(wr);res['capture']={n:sum(r<=n for r in wr) for n in [6,10,15,20]}
    if p is not None:
        y=np.zeros(N);y[np.array(actual)-1]=1;pc=np.clip(p,1e-6,1-1e-6)
        res['logloss']=float(-(y*np.log(pc)+(1-y)*np.log(1-pc)).mean());res['brier']=float(((pc-y)**2).mean())
    return frozen,res
# ------------------------------------------------------------------ helpers
def bern_ll(p,y):p=np.clip(p,1e-6,1-1e-6);return float(-(y*np.log(p)+(1-y)*np.log(1-p)).mean())
def logodds(p):p=np.clip(p,1e-6,1-1e-6);return np.log(p/(1-p))
def gaps_before(X,u):
    """draws since last appearance for each number, using X[:u] only (never seen -> u)."""
    last=np.full(N,-1)
    idx=np.nonzero(X[:u].any(0))[0]
    for i in idx:last[i]=np.nonzero(X[:u,i])[0][-1]
    return np.where(last>=0,u-1-last,u)
# ------------------------------------------------------------------ M0-A dynamic Bayesian frequency (prequential cache)
A_GRID=[(lam,a0) for lam in [0.97,0.985,0.995,1.0] for a0 in [10,50]]
def a_cache(X):
    T=len(X);P=np.zeros((len(A_GRID),T+1,N))
    for g,(lam,a0) in enumerate(A_GRID):
        al=np.full(N,a0*P0);be=np.full(N,a0*(1-P0))
        for u in range(T+1):
            P[g,u]=al/(al+be)
            if u<T:al=lam*al+X[u];be=lam*be+(1-X[u])
    L=np.array([[bern_ll(P[g,u],X[u]) for u in range(T)] for g in range(len(A_GRID))])
    return dict(P=P,L=L)
def model_A(X,t,c):
    g=int(np.argmin(c['L'][:,20:t].mean(1)));p=c['P'][g,t];return dict(p=p,params=dict(lam=A_GRID[g][0],a0=A_GRID[g][1]),g=g)
# ------------------------------------------------------------------ M0-B gap hazard
B_BINS=[(0,0),(1,1),(2,2),(3,4),(5,7),(8,12),(13,10**6)];B_K=[20,100,500]
def b_bin(g):return np.array([next(j for j,(lo,hi) in enumerate(B_BINS) if lo<=x<=hi) for x in g])
def b_cache(X):
    T=len(X);bins=np.array([b_bin(gaps_before(X,u)) for u in range(T+1)])
    hits=np.zeros((T+1,len(B_BINS)));tri=np.zeros((T+1,len(B_BINS)))
    for u in range(T):
        hits[u+1]=hits[u];tri[u+1]=tri[u]
        np.add.at(hits[u+1],bins[u],X[u]);np.add.at(tri[u+1],bins[u],1)
    P=np.zeros((len(B_K),T+1,N))
    for j,k in enumerate(B_K):
        for u in range(T+1):
            hz=(hits[u]+k*P0)/(tri[u]+k);P[j,u]=hz[bins[u]]
    L=np.array([[bern_ll(P[j,u],X[u]) for u in range(T)] for j in range(len(B_K))])
    return dict(P=P,L=L,hits=hits,tri=tri)
def model_B(X,t,c):
    j=int(np.argmin(c['L'][:,20:t].mean(1)));return dict(p=c['P'][j,t],params=dict(k=B_K[j]),hazard=((c['hits'][t]+B_K[j]*P0)/(c['tri'][t]+B_K[j])).tolist())
# ------------------------------------------------------------------ ridge logistic
def ridge_logit(F,y,lam,iters=30):
    F1=np.hstack([np.ones((len(F),1)),F]);w=np.zeros(F1.shape[1]);w[0]=LOGIT0;Rg=np.full(F1.shape[1],lam);Rg[0]=0
    for _ in range(iters):
        z=F1@w;p=1/(1+np.exp(-z));g=F1.T@(p-y)+Rg*w;H=(F1*(p*(1-p))[:,None]).T@F1+np.diag(Rg)+1e-9*np.eye(len(w))
        step=np.linalg.solve(H,g);w-=step
        if np.abs(step).max()<1e-8:break
    return w
def pred_logit(w,F):return 1/(1+np.exp(-(np.hstack([np.ones((len(F),1)),F])@w)))
def fit_tuned(rows_F,rows_y,grid):
    n=len(rows_F);cut=int(n*.7);best=None
    for lam in grid:
        mu=rows_F[:cut].mean(0);sd=rows_F[:cut].std(0)+1e-9
        w=ridge_logit((rows_F[:cut]-mu)/sd,rows_y[:cut],lam);ll=bern_ll(pred_logit(w,(rows_F[cut:]-mu)/sd),rows_y[cut:])
        if best is None or ll<best[0]-1e-12:best=(ll,lam)
    lam=best[1];mu=rows_F.mean(0);sd=rows_F.std(0)+1e-9;w=ridge_logit((rows_F-mu)/sd,rows_y,lam)
    return w,mu,sd,lam
# ------------------------------------------------------------------ M0-C transition
def c_features(X,u):
    """features for target index u from X[u-1], X[u-2] (u>=2)."""
    a=X[u-1];b=X[u-2] if u>=2 else np.zeros(N);sh=lambda v,k:np.roll(v,k)
    nb=lambda k:np.clip(sh(a,k)+sh(a,-k),0,1)
    mir=a[::-1]  # 39-x
    return np.column_stack([a,b,nb(1),nb(2),nb(3),mir,a*b])
C_GRID=[1,10,100]
def model_C(X,t,c=None):
    us=list(range(2,t));F=np.vstack([c_features(X,u) for u in us]);y=np.concatenate([X[u] for u in us])
    w,mu,sd,lam=fit_tuned(F,y,C_GRID);p=pred_logit(w,(c_features(X,t)-mu)/sd);return dict(p=p,params=dict(ridge=lam),coef=w.tolist())
# ------------------------------------------------------------------ M0-D co-occurrence graph
D_GRID=[(h,k) for h in [30,1000] for k in [1,5]];D_S=[0,0.05,0.1,0.2]
def d_cache(X):
    T=len(X);out={}
    for (h,k) in D_GRID:
        q=0.5**(1/h);Cm=np.zeros((N,N));W=0.;Z=np.zeros((T+1,N))
        for u in range(T+1):
            if u>=2:
                E=W*(6/38)*(5/37)+1e-12;lift=np.log((Cm+k*E)/(E+k*E));np.fill_diagonal(lift,0)
                att=lift[:,X[u-1]>0].mean(1);deg=lift.sum(1)
                zz=lambda v:(v-v.mean())/(v.std()+1e-12);Z[u]=zz(att)+zz(deg)
            if u<T:Cm=q*Cm+np.outer(X[u],X[u]);W=q*W+1
        out[(h,k)]=Z
    P={};L={}
    for key,Z in out.items():
        for s in D_S:
            pp=np.exp(s*Z);pp=P0*pp/pp.mean(1,keepdims=True);pp=np.clip(pp,1e-4,0.9);P[key+(s,)]=pp
            L[key+(s,)]=np.array([bern_ll(pp[u],X[u]) for u in range(T)])
    return dict(P=P,L=L)
def model_D(X,t,c):
    keys=list(c['L']);sel=[u for u in range(30,t,2)]
    best=min(keys,key=lambda k:(c['L'][k][sel].mean(),keys.index(k)));return dict(p=c['P'][best][t],params=dict(h=best[0],k=best[1],s=best[2]))
# ------------------------------------------------------------------ M0-E latent regime HMM
def hmm_fit(X,Kst,seed,iters=60):
    T=len(X);r=np.random.default_rng(seed);th=np.clip(P0+r.normal(0,.03,(Kst,N)),.02,.6);A=np.full((Kst,Kst),.1/max(Kst-1,1))+np.eye(Kst)*(.9 if Kst>1 else 1-0);A/=A.sum(1,keepdims=True);pi=np.ones(Kst)/Kst
    for _ in range(iters):
        lE=X@np.log(th).T+(1-X)@np.log(1-th).T;m=lE.max(1,keepdims=True);E=np.exp(lE-m)
        al=np.zeros((T,Kst));c=np.zeros(T);al[0]=pi*E[0];c[0]=al[0].sum();al[0]/=c[0]
        for u in range(1,T):al[u]=(al[u-1]@A)*E[u];c[u]=al[u].sum();al[u]/=c[u]
        be=np.ones((T,Kst))
        for u in range(T-2,-1,-1):be[u]=(A@(E[u+1]*be[u+1]))/c[u+1]
        g=al*be;g/=g.sum(1,keepdims=True)
        xi=np.zeros((Kst,Kst))
        for u in range(T-1):xi+=(al[u][:,None]*A*(E[u+1]*be[u+1])[None,:])/c[u+1]
        pi=g[0];A=(xi+1e-3)/(xi+1e-3).sum(1,keepdims=True);th=(g.T@X+1)/(g.sum(0)[:,None]+2)
    ll=float(np.log(c).sum()+m.sum())
    return dict(th=th,A=A,al=al,ll=ll,g=g)
def model_E(X,t,c=None):
    T=t;best=None
    for Kst in [1,2,3]:
        fits=[hmm_fit(X[:t],Kst,s) for s in (11,22,33)] if Kst>1 else [hmm_fit(X[:t],1,11,iters=2)]
        f=max(fits,key=lambda z:z['ll']);npar=Kst*N+Kst*(Kst-1)+Kst-1;bic=-2*f['ll']+npar*math.log(T*N)
        if best is None or bic<best[0]-1e-9:best=(bic,Kst,f)
    _,Kst,f=best;ps=f['al'][-1]@f['A'];p=ps@f['th'];return dict(p=p,params=dict(K=Kst),state_probs=ps.tolist(),fit=f)
# ------------------------------------------------------------------ M0-F supervised
def f_features(X,u):
    n=u;freq=(X[:u].sum(0)+20*P0)/(n+20);l10=X[max(0,u-10):u].sum(0);l30=X[max(0,u-30):u].sum(0);l5=X[max(0,u-5):u].sum(0)
    w=2.**(-np.arange(u-1,-1,-1)/20);ew=w@X[:u]/w.sum();g=gaps_before(X,u).astype(float)
    tr=X[max(0,u-20):u].mean(0)-X[max(0,u-60):max(0,u-20)].mean(0) if u>=40 else np.zeros(N)
    cnt=X[:u].T@X[:u];E=n*(6/38)*(5/37)+1e-9;lift=cnt/E;np.fill_diagonal(lift,0);ps=lift[:,X[u-1]>0].mean(1)
    par=np.arange(1,N+1)%2
    return np.column_stack([freq,l10,l30,ew,g,np.log1p(g),tr,X[u-1],X[u-2],ps,l5,par])
F_GRID=[1,10,100,1000];F_START=30
def f_cache(X):return {u:f_features(X,u) for u in range(F_START,len(X)+1)}
def model_F(X,t,c):
    us=list(range(F_START,t));F=np.vstack([c[u] for u in us]);y=np.concatenate([X[u] for u in us])
    w,mu,sd,lam=fit_tuned(F,y,F_GRID);p=pred_logit(w,(c[t]-mu)/sd);return dict(p=p,params=dict(ridge=lam),coef=w.tolist())
# ------------------------------------------------------------------ M0-G energy
G_GRID=[0,0.5,1.0];_SAMPLE=None
def g_sample():
    global _SAMPLE
    if _SAMPLE is None:r=np.random.default_rng(20261012);_SAMPLE=np.sort(np.argsort(r.random((20000,N)),1)[:,:6],1)
    return _SAMPLE
def pmi(X,u):
    n=u;cnt=X[:u].T@X[:u];E=n*(6/38)*(5/37);W=np.log((cnt+5)/(E+5));np.fill_diagonal(W,0);return W
def model_G(X,t,ca):
    gA=model_A(X,t,ca)['g'];S=g_sample();I,Jx=np.triu_indices(6,1);best=None
    for gam in G_GRID:
        ls=[]
        for s in range(max(50,t-30),t):
            L=logodds(ca['P'][gA,s]);W=pmi(X,s);es=L[S].sum(1)+gam*W[S[:,I],S[:,Jx]].sum(1);logZ=lse(es)-math.log(len(S))+math.log(CN)
            a=np.nonzero(X[s])[0];ea=L[a].sum()+gam*sum(W[i,j] for i,j in itertools.combinations(a,2));ls.append(ea-logZ+math.log(CN))
        sc=np.mean(ls) if ls else 0.
        if best is None or sc>best[0]+1e-12:best=(sc,gam)
    gam=best[1];L=logodds(ca['P'][gA,t]);return dict(L=L,W=pmi(X,t),gamma=gam,params=dict(gamma=gam,A=A_GRID[gA]))
# ------------------------------------------------------------------ M0-X transformation search
def fix(vals,base=None):
    out=[];used=set()
    for v in vals:
        v=int(v)
        while v<1:v+=38
        while v>38:v-=38
        w=v;k=0
        while w in used:
            k+=1;w=((v-1+k)%38)+1
        used.add(w);out.append(w)
    return sorted(out)
def x_rules(D,u,meddelta):
    a=D[u-1];b=D[u-2]
    rules=[fix(a)]+[fix(a+k) for k in [-5,-4,-3,-2,-1,1,2,3,4,5]]+[fix(39-a),fix(39-b),fix(b),fix(np.clip(2*a-b,1,38)),fix(np.floor((a+b)/2+.5)),fix(a+meddelta),fix(b.min()+np.concatenate([[0],np.cumsum(np.diff(a))]))]
    return rules
def x_cache(D):
    T=len(D);out={};ov={}
    for u in range(2,T+1):
        md=np.median(np.diff(D[:u],axis=0),axis=0) if u>=3 else np.zeros(6);rs=x_rules(D,u,np.round(md).astype(int));out[u]=rs
        if u<T:ov[u]=[len(set(r)&set(D[u].tolist())) for r in rs]
    return dict(rules=out,ov=ov)
def model_X(D,t,c):
    prior=[u for u in range(2,t)]
    if len(prior)<20:r=0
    else:
        m=np.array([c['ov'][u] for u in prior]).mean(0);r=int(np.argmax(m))
    return dict(rule=r,ticket=c['rules'][t][r],params=dict(rule=r))
def x_scores(ticket):
    U=universe();ins=np.zeros(N);ins[np.array(ticket)-1]=1;ov=additive(ins)
    tv=np.array(ticket)-1;l1=np.zeros(CN)
    for j,col in enumerate(U['cols']):l1+=np.abs(col-tv[j])
    return ov*1000-l1
