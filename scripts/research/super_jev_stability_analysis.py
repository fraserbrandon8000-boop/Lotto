"""Analyze production + research replicates of a Super Lotto V1 Jev request (diagnostic only)."""
import json,math,itertools,sys,argparse
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts/research'))
from common import save
ap=argparse.ArgumentParser();ap.add_argument('--target',required=True);a=ap.parse_args();T=int(a.target)
S=R/f'results/super_lotto/draw{T}';O=R/f'results/super_lotto/jev_stability_{T}'
runs=[('production',json.loads((S/'jev_response.json').read_text()))]+[(f'replicate_{i}',json.loads((O/f'replicate_{i}_response.json').read_text())) for i in range(1,6)]
ids=sorted(runs[0][1]['answers']['overall']['probabilities']);P=np.array([[r['answers']['overall']['probabilities'][i] for i in ids] for _,r in runs])
conf=[r['answers']['overall']['confidence'] for _,r in runs];top=[r['answers']['overall']['choice'] for _,r in runs]
def rk(v):
    o=np.argsort(-v,kind='stable');x=np.empty(len(v));i=0;vs=v[o]
    while i<len(v):
        j=i
        while j+1<len(v) and abs(vs[j+1]-vs[i])<1e-12:j+=1
        x[o[i:j+1]]=(i+j)/2+1;i=j+1
    return x
t3=lambda v:set(np.array(ids)[np.lexsort((np.arange(len(v)),-v))[:3]])
pairs=list(itertools.combinations(range(6),2));rho=[float(np.corrcoef(rk(P[i]),rk(P[j]))[0,1]) for i,j in pairs];ov=[len(t3(P[i])&t3(P[j])) for i,j in pairs]
ent=[float(-sum(p*math.log2(p) for p in row if p>0)) for row in P]
keys=[k.split('_',1)[1] for k in runs[0][1]['answers'] if k.startswith(ids[0]+'_')];var={}
for k in keys:
    vals=np.array([[r['answers'][f'{c}_{k}'].get('score',r['answers'][f'{c}_{k}'].get('noul')) for c in ids] for _,r in runs]);var[k]=float((vals.max(0)-vals.min(0)).max())
pred=json.loads((R/f'results/super_lotto/prospective/prediction_{T}.json').read_text())
out=dict(runs=[dict(run=n,model=r['model'],top_choice=t,top_probability=float(r['answers']['overall']['probabilities'][t]),confidence=c,entropy_bits=e) for (n,r),t,c,e in zip(runs,top,conf,ent)],
  production_top=top[0],top_choice_agreement_replicates=f"{sum(t==top[0] for t in top[1:])}/5",mean_pairwise_spearman=float(np.mean(rho)),min_pairwise_spearman=float(np.min(rho)),
  mean_top3_overlap=float(np.mean(ov)),min_top3_overlap=int(min(ov)),choice_variance_by_candidate={i:float(v) for i,v in zip(ids,P.var(0,ddof=1))},max_abs_prob_range=float((P.max(0)-P.min(0)).max()),
  confidence=dict(mean=float(np.mean(conf)),sd=float(np.std(conf,ddof=1)),min=min(conf),max=max(conf)),per_candidate_answer_max_range=var,aggregated_top=ids[int(np.argmax(P.mean(0)))],
  v1_policy=dict(selection_policy=pred['selection_policy'],selected=pred['selection']['candidate_id'],statistical_edge_detected=pred['statistical_edge_detected'],jev_influence='none under the no-edge rule: the seeded index depends only on the number of candidates'),
  would_aggregation_change_v1_ticket='NO' if not pred['statistical_edge_detected'] else 'see edge branch')
save(O/'stability_analysis.json',out);print(json.dumps({k:v for k,v in out.items() if k not in ('runs','choice_variance_by_candidate')},indent=1))
