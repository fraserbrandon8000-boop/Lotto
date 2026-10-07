"""A15/A16: cumulative Lotto research registry (recovered from saved artifacts) and holdout-reuse counts.
Super Lotto is a separate program and is excluded. Output results/lotto/system_audit_2344/RESEARCH_REGISTRY.json"""
import json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[2];O=R/'results/lotto/system_audit_2344'
D=json.loads((O/'data/a6_discovery.json').read_text());A3=json.loads((O/'data/a3_strategies.json').read_text());A9=json.loads((O/'data/a9_combination_probability.json').read_text())
E=[
 dict(id='R01',date='2026-09-19',study='V1 original analysis',hypothesis='Any of A_long..H_random beats the hypergeometric match null',family_tests=8,exploratory_tests=112,
      window=[2211,2338],confirmation=[2299,2338],raw_best_p='A_long confirmation Holm 0.846',result='no model qualifies',reused_later=True,source='results/model_performance.json, results/sensitivity.csv'),
 dict(id='R02',date='2026-09-21..2026-10-03',study='V1 refresh runs #2340-#2343 (gate re-evaluated each cutoff)',hypothesis='same 8-model gate at each new cutoff',family_tests=32,exploratory_tests=0,
      window=[2211,2342],confirmation=[2300,2342],result='no model qualifies at any cutoff',reused_later=True,source='results/lotto/draw23xx/model_performance.json'),
 dict(id='R03',date='2026-09-2x',study='forensic #2340 construction family',hypothesis='63 discovery-pool x construction rules (direct top6, uniform-in-topN, structure-penalised search, G variants)',family_tests=63,exploratory_tests=141,
      window=[2211,2339],confirmation=[2300,2339],raw_best_p=0.024,corrected='Holm 1.0',result='none passes; no V2',reused_later=True,source='results/lotto/forensic_2340/construction_performance.json'),
 dict(id='R04',date='2026-09-2x',study='forensic #2340 historical discovery / minimum pool',hypothesis='family rankings capture winners above random',family_tests=126,exploratory_tests=0,window=[2211,2339],confirmation=None,result='descriptive; random level',reused_later=True,source='results/lotto/forensic_2340/historical_discovery.json'),
 dict(id='R05',date='2026-09-27',study='forensic #2341 fixed-seed sensitivity',hypothesis='seed designs change V1 fallback matches',family_tests=0,exploratory_tests=1027,window=[2211,2341],confirmation=None,result='production seed inside the seed distribution; descriptive',reused_later=True,source='results/lotto/forensic_2341/seed_sensitivity.json'),
 dict(id='R06',date='2026-09-28',study='P0 design: reliability weights + pool size K',hypothesis='K in {10,12,15,20} captures above 6K/38; family reliability',family_tests=4,exploratory_tests=5,window=[2211,2340],confirmation=[2231,2300],result='no K passes; default K=15; weights B 0.031, D 0.024, struct 0.007',reused_later=True,source='results/lotto/p0_protocol/pool_size_selection.json, reliability.json'),
 dict(id='R07',date='2026-09-28',study='P0 historical gate E1-E3',hypothesis='P0 portfolio beats null on challenger totals / best / >=3',family_tests=3,exploratory_tests=8,window=[2231,2340],confirmation=[2301,2340],raw_best_p=0.086,corrected='Holm 0.26',result='FAIL',reused_later=True,source='results/lotto/p0_protocol/historical_evaluation.json'),
 dict(id='R08',date='2026-10-03',study='forensic #2342 research challengers',hypothesis='19 P0/V1 variants (K18/20/25, dynamic K, shrinkage, equal weights, overlap, struct0, exhaustive, seeds)',family_tests=19,exploratory_tests=0,window=[2231,2342],confirmation=[2303,2342],raw_best_p=0.09,corrected='Holm 1.0',result='none passes',reused_later=True,source='results/lotto/forensic_2342/research_challengers.json'),
 dict(id='R09',date='2026-10-03',study='forensic #2342 Top-N audit + cluster tests + seed follow-up',hypothesis='pool sizes 10-25; run-length deviations; seed designs',family_tests=6+10,exploratory_tests=2504,window=[2211,2342],confirmation=[2303,2342],raw_best_p=0.012,corrected='Holm 0.06 (cluster), 0.11 (Top-N conf.)',result='none passes',reused_later=True,source='results/lotto/forensic_2342/historical_2342.json'),
 dict(id='R10',date='2026-10-07',study='#2344 system audit (this audit)',hypothesis='8 portfolio strategies (best-ticket), 10 discovery orderings x 10 metrics, 6 combination-probability models, 5 seed designs',
      family_tests=len(A3['strategies'])+D['family_size']+len(A9['models']),exploratory_tests=5,window=[2231,2343],confirmation=[2304,2343],raw_best_p=D['min_raw'],corrected=f"Holm min {D['min_holm']}",result='none passes',reused_later=False,source='results/lotto/system_audit_2344/data/'),
]
total=sum(e['family_tests'] for e in E);expl=sum(e['exploratory_tests'] for e in E)
use=Counter();conf=Counter()
for e in E:
    for t in range(e['window'][0],e['window'][1]+1):use[t]+=1
    if e['confirmation']:
        for t in range(e['confirmation'][0],e['confirmation'][1]+1):conf[t]+=1
out=dict(program='Jamaica Lotto (Super Lotto excluded)',entries=E,cumulative_formal_tests=total,cumulative_exploratory_comparisons=expl,
  draw_reuse=dict(max_studies_using_a_draw=max(use.values()),max_times_used_as_confirmation=max(conf.values()),
     confirmation_uses_by_draw={str(t):conf[t] for t in range(2299,2344)},draws_used_as_confirmation_3plus=sum(v>=3 for v in conf.values())),
  bonferroni_alpha_per_test_at_cumulative_family=0.05/total,
  any_result_survives_cumulative_bonferroni=False,
  assessment='Every promotion-style test has failed, so inflated false discoveries have not entered production. But the last ~40 historical draws (2299-2343) have been used as "confirmation" by up to %d separate studies and inspected in every forensic; they are no longer a pristine holdout. Only prospective draws after a protocol is frozen are clean.'%max(conf.values()))
(O/'RESEARCH_REGISTRY.json').write_text(json.dumps(out,indent=1))
print(total,expl,out['draw_reuse']['max_studies_using_a_draw'],out['draw_reuse']['max_times_used_as_confirmation'],out['draw_reuse']['draws_used_as_confirmation_3plus'])
