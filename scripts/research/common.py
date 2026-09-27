"""Game-agnostic mathematics. No files, fitted parameters or game data loaded."""
import json,math,csv
from pathlib import Path
from functools import lru_cache
import numpy as np
def clean(x):
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [clean(v) for v in x]
    if isinstance(x,np.ndarray):return clean(x.tolist())
    if isinstance(x,np.integer):return int(x)
    if isinstance(x,np.bool_):return bool(x)
    if isinstance(x,(float,np.floating)):return float(x) if math.isfinite(x) else None
    return x
def save(path,x):Path(path).write_text(json.dumps(clean(x),indent=2,allow_nan=False),encoding='utf-8')
def csvsave(path,rows):
    with Path(path).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows([{k:json.dumps(clean(v)) if isinstance(v,(dict,list,np.ndarray)) else clean(v) for k,v in r.items()} for r in rows])
def holm(p):
    p=np.asarray(p);i=np.argsort(p);o=np.empty(len(p));o[i]=np.minimum(1,np.maximum.accumulate(p[i]*(len(p)-np.arange(len(p)))));return o
def hg(N,K,m):return np.array([math.comb(K,j)*math.comb(N-K,m-j)/math.comb(N,m) if 0<=m-j<=N-K else 0 for j in range(K+1)])
@lru_cache(None)
def sumpmf(N,K,m,n):
    p=np.array([1.]);q=hg(N,K,m)
    for _ in range(n):p=np.convolve(p,q)
    return p
def pmean(y,N,K,m):return float(sumpmf(N,K,m,len(y))[int(sum(y)):].sum())
def blockci(y,seed=421,iterations=5000):
    y=np.asarray(y);n=len(y);r=np.random.default_rng(seed);ix=(r.integers(n,size=(iterations,math.ceil(n/5),1))+np.arange(5))%n
    return np.quantile(y[ix.reshape(iterations,-1)[:,:n]].mean(1),[.025,.975])
def ind(d,N):
    a=np.zeros((len(d),N),dtype=np.int64);a[np.arange(len(d))[:,None],d]=1;return a
def sample(r,n,N,K):return np.sort(np.argpartition(r.random((n,N)),K-1,axis=1)[:,:K],axis=1)
def z(x):return (x-np.mean(x))/(np.std(x)+1e-12)
def table(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','|'+'|'.join(['---']*len(headers))+'|']+['| '+' | '.join(map(str,r))+' |' for r in rows])
