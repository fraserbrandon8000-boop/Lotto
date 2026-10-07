"""Frozen M0 protocol (results/lotto_m0/protocol/PROTOCOL.md): one prospective shadow prediction. Usage: m0_predict.py TARGET DEADLINE_UTC"""
import sys,json,hashlib
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent));import m0
TG=int(sys.argv[1]);DL=datetime.fromisoformat(sys.argv[2]);now=datetime.now(timezone.utc);assert now<DL,'draw time passed: STOP'
D,X,ids,dh=m0.load_data();T=len(D);assert ids[-1]==TG-1
man=json.loads((m0.R/'results/lotto_m0/protocol/FREEZE_MANIFEST.json').read_text());assert man['selected']=='M0-C' and man['dataset_sha256']==dh
for f,h in man['files'].items():assert hashlib.sha256((m0.R/f).read_bytes()).hexdigest()==h,f'frozen file changed: {f}'
us=list(range(2,T));F=np.vstack([m0.c_features(X,u) for u in us]);y=np.concatenate([X[u] for u in us]);w,mu,sd,lam=m0.fit_tuned(F,y,m0.C_GRID)
feat=(m0.c_features(X,T)-mu)/sd;p=m0.pred_logit(w,feat);L=m0.logodds(p)
c=m0.model_C(X,T);assert np.allclose(c['p'],p)
s=m0.additive(L);fr,_=m0.evaluate_scores(s,None,True);U=m0.universe();top=m0.top_list(s,10)
state=dict(ridge=lam,coef=w.tolist(),feature_mean=mu.tolist(),feature_sd=sd.tolist(),feature_names=['in t-1','in t-2','+-1 of t-1','+-2 of t-1','+-3 of t-1','39-x in t-1','in t-1 and t-2'])
sh=hashlib.sha256(json.dumps(state,sort_keys=True).encode()).hexdigest()
top10=[dict(rank=i+1,numbers=(U['C'][j]+1).tolist(),score=float(s[j]),prob_times_C=float(np.exp(s[j]-fr['logZ'])*m0.CN)) for i,j in enumerate(top)]
out=dict(status='M0 PRIMARY SHADOW — FROZEN PRE-DRAW (research only; not a production ticket)',created_utc=now.isoformat(),target_draw=TG,scheduled_draw_utc=sys.argv[2],data_cutoff=ids[-1],
  model='M0-C draw-to-draw transition (ridge logistic, conditional-Bernoulli set score)',primary_shadow=fr['primary'],top10=top10,
  number_probabilities={i+1:float(p[i]) for i in range(38)},number_order=(np.argsort(-L,kind='stable')+1).tolist(),entropy_nats=fr['entropy_nats'],max_entropy_nats=float(np.log(m0.CN)),
  model_state=state,dataset_sha256=dh,model_state_sha256=sh,config_sha256=man['config_sha256'],protocol_commit='8814686',historical_verdict='NO EDGE',
  jackpot_probability_estimate='The model gives its top ticket %.3fx the uniform probability; this is not validated (historical exact log-score below uniform).'%top10[0]['prob_times_C'])
O=m0.R/f'results/lotto_m0/shadow_{TG}';O.mkdir(parents=True,exist_ok=True);pp=O/'prediction.json'
with pp.open('x') as h:json.dump(out,h,indent=1)
ph=hashlib.sha256(pp.read_bytes()).hexdigest()
with (m0.R/'results/lotto_m0/ledger.jsonl').open('a') as h:h.write(json.dumps(dict(event='m0_shadow_frozen',created_utc=out['created_utc'],target_draw=TG,numbers=out['primary_shadow'],path=str(pp.relative_to(m0.R)),sha256=ph,model_state_sha256=sh,dataset_sha256=dh))+'\n')
print(json.dumps(dict(primary=out['primary_shadow'],top10=[t['numbers'] for t in top10],top_prob_multiplier=top10[0]['prob_times_C'],ridge=lam,coef=[round(x,4) for x in w],state_hash=sh,prediction_hash=ph,created=out['created_utc']),indent=1))
