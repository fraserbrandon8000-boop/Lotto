"""Independent invariants and targeted future-information leakage checks."""
import json, hashlib, math
import numpy as np
from audit import DEFAULT
from analyze import ROOT, OUT, SEED, PMF, BASE, sample, walk, structure, save

records=json.loads((ROOT/'data/draws.json').read_text()); draws=np.array([r['numbers'] for r in records])-1
audit=json.loads((OUT/'audit.json').read_text()); rows=json.loads((OUT/'walk_forward_predictions.json').read_text())
assert hashlib.sha256(DEFAULT.read_bytes()).hexdigest()==audit['sha256']
assert len(records)==len(set(r['draw_id'] for r in records))
assert abs(PMF.sum()-1)<1e-12 and abs(np.arange(7)@PMF-BASE)<1e-12
for r in rows:
    truth=set(records[r['index']]['numbers'])
    assert r['training_last_draw_id']<r['draw_id']
    for ticket,m in zip(r['tickets'],r['matches']):
        assert len(set(ticket))==6 and all(1<=x<=38 for x in ticket)
        assert len(set(ticket)&truth)==m
    assert abs(sum(r['ensemble_weights'])-1)<1e-12
# At the target and after it, replace every outcome. Predictions at and before
# the target must be identical. Use a short fixed timeline to keep this test fast.
short=draws[:65].copy(); rr=records[:65]; before=walk(short,rr)
mutated=short.copy(); mutated[57:]=sample(np.random.default_rng(99),len(short)-57)
after=walk(mutated,rr)
for a,b in zip(before,after):
    if a['index']<=57: assert a['tickets']==b['tickets'] and a['ensemble_weights']==b['ensemble_weights']
assert len(rows)==len(records)-50
confirm=[r for r in rows if r['period']=='confirmation']
assert len(confirm)==40 and all(r['ensemble_weights']==confirm[0]['ensemble_weights'] for r in confirm)
# Independent random-ticket empirical distribution validates combinatorial PMF.
rng=np.random.default_rng(SEED+700); random=sample(rng,200000)
hits=(random<6).sum(1); frequencies=np.bincount(hits,minlength=7)/len(hits)
assert abs(hits.mean()-BASE)<.01 and np.max(np.abs(frequencies-PMF))<.005
# Descriptive comparison of ALL listed structural features to uniform tickets.
actual=structure(draws); theoretical=structure(random); names=['sum','median','minimum','maximum','range','odd_count','low_count','adjacent_pairs','largest_spacing','close_spacings_le2']
summary=[dict(feature=n,observed_mean=float(actual[:,j].mean()),random_mean=float(theoretical[:,j].mean()),observed_sd=float(actual[:,j].std()),random_sd=float(theoretical[:,j].std()),observed_ticket_95=np.quantile(actual[:,j],[.025,.975]).tolist(),random_ticket_95=np.quantile(theoretical[:,j],[.025,.975]).tolist()) for j,n in enumerate(names)]
save('structure_summary.json',dict(simulated_tickets=200000,features=summary,band_expected_per_draw=[60/38,60/38,60/38,48/38],last_digit_expected_per_draw=[18/38]+[24/38]*8+[18/38],note='Intervals describe individual tickets, not uncertainty about the mean. Categories have different sizes; last-digit 0 and 9 each have three numbers, other digits have four. These structural properties do not change the probability of any specific ticket.'))
save('verification.json',dict(original_workbook_unchanged=True,no_future_outcome_leakage_test=True,holdout_ensemble_weights_frozen=True,prediction_match_reconciliation=True,uniform_generator_check=True,null_pmf_normalized=True,all_prediction_tickets_valid=True,tested_draws=len(rows)))
print('All audit, baseline, prediction, chronology, future-mutation, frozen-weight and uniform-generator checks passed.')
