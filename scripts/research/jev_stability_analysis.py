"""Analyze production + research replicates of the #2342 V1 Jev request (diagnostic only)."""
import json,math,itertools,sys
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'))
import analyze as a
S=R/'results/lotto/draw2342';O=R/'results/lotto/jev_stability_2342'
runs=[('production',json.loads((S/'jev_response.json').read_text()))]+[(f'replicate_{i}',json.loads((O/f'replicate_{i}_response.json').read_text())) for i in range(1,6)]
ids=sorted(runs[0][1]['answers']['overall']['probabilities']);P=np.array([[r['answers']['overall']['probabilities'][i] for i in ids] for _,r in runs])
conf=[r['answers']['overall']['confidence'] for _,r in runs];top=[r['answers']['overall']['choice'] for _,r in runs]
def ranks(v):
    o=np.argsort(-v,kind='stable');rk=np.empty(len(v));i=0;vs=v[o]
    while i<len(v):
        j=i
        while j+1<len(v) and abs(vs[j+1]-vs[i])<1e-12:j+=1
        rk[o[i:j+1]]=(i+j)/2+1;i=j+1
    return rk
def top3(v):return set(np.array(ids)[np.lexsort((np.arange(len(v)),-v))[:3]])
rho=[float(np.corrcoef(ranks(P[i]),ranks(P[j]))[0,1]) for i,j in itertools.combinations(range(6),2)]
t3=[len(top3(P[i])&top3(P[j])) for i,j in itertools.combinations(range(6),2)]
ent=[float(-sum(p*math.log2(p) for p in row if p>0)) for row in P]
keys=['robustness','consensus','quality','overfit','stable','stronger','dependent'];var={}
for k in keys:
    vals=np.array([[r['answers'][f'{c}_{k}'].get('score',r['answers'][f'{c}_{k}'].get('noul')) for c in ids] for _,r in runs])
    var[k]=dict(max_range_across_runs=float((vals.max(0)-vals.min(0)).max()),mean_range=float((vals.max(0)-vals.min(0)).mean()))
agg=P.mean(0);agg_top=ids[int(np.argmax(agg))]
fz=json.loads((S/'frozen.json').read_text());meta=json.loads((S/'metadata.json').read_text())
# Hypothetical V1 edge-branch composite per run (not applicable: no qualifying model, so no candidate is eligible).
st=json.loads((S/'jev_state.json').read_text());conf_rows={r['model']:r for r in st['methodology_confirmation']}
def composite(r,c):
    an=r['answers'];aa={k:an[f"{c['id']}_{k}"] for k in keys}
    return .20*c['sensitivity_top_quartile_fraction']+.10*(20-c['ensemble_rank'])/19+.10*aa['robustness']['score']/4+.05*aa['consensus']['score']/4+.10*aa['quality']['score']/4+.10*an['overall']['probabilities'][c['id']]-.10*aa['overfit']['noul']-.05*aa['dependent']['noul']
comp_top=[max(st['candidates'],key=lambda c:(composite(r,c),c['id']))['id'] for _,r in runs]
out=dict(runs=[dict(run=n,model=r['model'],top_choice=t,top_probability=float(r['answers']['overall']['probabilities'][t]),confidence=c,entropy_bits=e,distribution=r['answers']['overall']['probabilities']) for (n,r),t,c,e in zip(runs,top,conf,ent)],
  production_top=top[0],top_choice_agreement_replicates=f"{sum(t==top[0] for t in top[1:])}/5",top1_agreement_all_pairs=float(np.mean([top[i]==top[j] for i,j in itertools.combinations(range(6),2)])),
  mean_pairwise_spearman=float(np.mean(rho)),min_pairwise_spearman=float(np.min(rho)),mean_top3_overlap=float(np.mean(t3)),min_top3_overlap=int(min(t3)),
  choice_probability_sd_by_candidate={i:float(s) for i,s in zip(ids,P.std(0,ddof=1))},max_abs_prob_range=float((P.max(0)-P.min(0)).max()),
  confidence=dict(mean=float(np.mean(conf)),sd=float(np.std(conf,ddof=1)),min=min(conf),max=max(conf)),entropy_bits=dict(mean=float(np.mean(ent)),sd=float(np.std(ent,ddof=1))),
  per_candidate_score_noul_variation=var,aggregated_mean_distribution={i:float(v) for i,v in zip(ids,agg)},aggregated_top=agg_top,
  v1_policy=dict(qualifying_models=meta['qualifying_models'],branch='no-edge seeded fallback',selected=fz['candidate_id'],jev_influence='none: the fallback index depends only on the number of eligible candidates',
                 hypothetical_edge_branch_composite_top_by_run=comp_top,note='The edge branch is not applicable (no qualifying model, so no candidate has validated models).'),
  would_aggregation_change_v1_ticket='NO',
  answer='Using the first valid response or an aggregate of all six responses would not have changed the V1 ticket: under the no-edge rule Jev has no role in selection, and even Jev\'s own favourite (C03) is identical in every run.')
a.OUT=O;a.save('stability_analysis.json',out);print(json.dumps({k:v for k,v in out.items() if k not in ('runs','choice_probability_sd_by_candidate','aggregated_mean_distribution')},indent=1));print([(r['run'],r['top_probability'],r['confidence'],round(r['entropy_bits'],3)) for r in out['runs']])
