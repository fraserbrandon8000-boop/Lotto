"""Super Lotto #1754 forensic (research only). Reads only results/super_lotto and Super Lotto/generic code.
Outputs: results/super_lotto/forensic_1754/."""
import sys,json,math,itertools,hashlib
from pathlib import Path
from collections import Counter
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts/research'))
import super_lotto as sl,super_history as S
from common import save,holm,pmean,blockci,hg
V=R/'results/super_lotto';D=V/'draw1754';O=V/'forensic_1754';O.mkdir(exist_ok=True)
def J(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
WIN=[3,4,21,23,31];WSB=8;SEL=[1,2,18,34,35];SSB=2;NS=[5,7,10,12,15,20]
OUT1753=dict(main=[1,5,8,14,18],sb=3);SEL1753=dict(main=[1,22,32,34,35],sb=2)

# ---------------------------------------------------------------- 1. verification
pred=J(V/'prospective/prediction_1754.json');fr=J(D/'freeze-receipt.json');cf=J(D/'candidate-freeze.json');att=J(D/'jev-attempt.json');rc=J(D/'jev_receipt.json')
ic=J(D/'integrity-check.json');fic=J(D/'final-integrity-check.json');hv=J(V/'bootstrap/hash_verification.json')
led=[json.loads(l) for l in (V/'prospective/ledger.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]
cands=J(D/'candidates.json');sel=[c for c in cands if c['id']==pred['selection']['candidate_id']][0]
verification=dict(frozen_ticket=pred['selection'],ticket_matches_pool=sel['main']==pred['selection']['main'] and sel['super_ball']==pred['selection']['super_ball'],
  ledger_entry=[e for e in led if e.get('target_draw_id')==1754],ledger_hash_matches=hv['ledger_prediction_hashes'].get('prediction_1754.json'),
  embedded_hashes=hv['summary']['prediction_1754_embedded'],embedded_mismatch=hv['differs']['prediction_1754_embedded'],candidate_freeze_hashes=hv['summary']['candidate_freeze_1754'],
  jev_receipt=hv['jev_receipt_1754'],jev_single_attempt=att['http_attempts']==1 and att['retries_disabled'],
  chronology_utc=dict(preflight_unpublished_check=ic['checked_utc'],candidate_pool_frozen=cf['frozen_utc'],final_unpublished_check=fic['checked_utc'],jev_call_started=att['started_utc'],jev_receipt=rc['created_utc'],ticket_frozen=pred['created_utc'],scheduled_draw=pred['scheduled_draw_utc']),
  order_ok=cf['frozen_utc']<att['started_utc'].replace('Z','')<pred['created_utc']<'2026-09-26T01:30',
  note='The Codex snapshot is a single commit, so there is no git chronology for #1754; ordering rests on the embedded UTC timestamps, the official-API unpublished checks at 00:58:57 and 01:04:15 UTC, and the hash chain.')

# ---------------------------------------------------------------- 2. pre-draw number evidence (frozen complete_rankings.json)
cr=J(D/'complete_rankings.json')
def mrow(m,n):
    e=cr['main'][m]
    if not e.get('applicable'):return None
    x=[r for r in e['numbers'] if r['number']==n][0];return dict(score=x['score'],rank=x['rank'],tie_interval=[x['tie_min'],x['tie_max']],informative=e['informative'])
main_ev={n:dict(role='winner' if n in WIN else 'selected_loser',models={m:mrow(m,n) for m in sl.MN}) for n in WIN+SEL}
def coverage(m):
    e=cr['main'][m];order=e['order'];sc={r['number']:r['score'] for r in e['numbers']};out={}
    for N in NS:
        pt=len(set(order[:N])&set(WIN));v=sorted(sc.values(),reverse=True)[N-1]
        inside=[i for i in sc if sc[i]>v+1e-12];tied=[i for i in sc if abs(sc[i]-v)<=1e-12];slots=N-len(inside)
        dw=len(set(inside)&set(WIN));tw=len(set(tied)&set(WIN));tn=len(tied)-tw;pm=hg(35,5,N)
        out[N]=dict(point=pt,min=dw+max(0,slots-tn),max=dw+min(slots,tw),expected=5*N/35,p_ge=float(pm[pt:].sum()))
    return out
cov={m:coverage(m) for m in sl.MN if cr['main'][m].get('applicable') and (cr['main'][m]['informative'] or m=='G_ensemble')}
sbe={}
for m,e in cr['super_ball'].items():
    if e.get('order') is None:sbe[m]=dict(informative=False,random_control=True,selected=e['selected']);continue
    row=lambda n:[r for r in e['numbers'] if r['number']==n][0]
    sbe[m]=dict(informative=e['informative'],selected=e['selected'],SB8=dict(rank=row(8)['rank'],tie=[row(8)['tie_min'],row(8)['tie_max']],score=row(8)['score']),SB2=dict(rank=row(2)['rank'],tie=[row(2)['tie_min'],row(2)['tie_max']],score=row(2)['score']))
pool_sbs=sorted({c['super_ball'] for c in cands});c1753=J(V/'candidates.json');pool_sbs_1753=sorted({c['super_ball'] for c in c1753})
save(O/'number_evidence.json',dict(cutoff=1753,target=1754,winners=WIN,winning_sb=WSB,selected=SEL,selected_sb=SSB,main=main_ev,flat_or_non_informative=[m for m in sl.MN if not cr['main'][m].get('applicable') or not cr['main'][m].get('informative')],
  coverage=cov,super_ball=sbe,SB8_in_any_candidate=WSB in pool_sbs,pool_super_balls_1754=pool_sbs,pool_super_balls_1753=pool_sbs_1753,SB3_in_any_1753_candidate=3 in pool_sbs_1753,
  sb_omission_repeated=(WSB not in pool_sbs) and (3 not in pool_sbs_1753),
  note='Exact frozen pre-draw values from draw1754/complete_rankings.json. E_pairs flat (no Holm-retained pair); G_ensemble proxy marked non-informative by V1 instrumentation but ranked; F_structure has no number-level ranking; H_random is a control.'))

# ---------------------------------------------------------------- 3. pool scoring
resp=J(D/'jev_response.json');an=resp['answers'];pr=an['overall']['probabilities']
def jr(cid):p=pr[cid];return dict(best=1+sum(v>p for v in pr.values()),worst=sum(v>=p for v in pr.values()))
pool=[]
for c in cands:
    m=sorted(set(c['main'])&set(WIN));pool.append(dict(id=c['id'],main=c['main'],super_ball=c['super_ball'],main_generator=c['main_generator'],SB_generator=c['SB_generator'],eligible=True,
      main_matches=len(m),matched=m,sb_match=c['super_ball']==WSB,outcome=f"{len(m)}/5"+(' + SB' if c['super_ball']==WSB else ''),jev_choice=pr[c['id']],jev_rank=jr(c['id']),
      sensitivity=dict(rank_range=c['sensitivity_rank_range'],top5_fraction=c['sensitivity_top5_fraction']),
      evidence=dict(model_agreement_count=c['model_agreement_count'],ensemble_score=c['ensemble_score'],qualified_models=c['qualified_models'],main_support_confirmation_mean=c['main_support']['mean'],SB_support_confirmation_mean=c['SB_support']['mean'])))
dist=Counter(r['main_matches'] for r in pool);best=max(r['main_matches'] for r in pool)
ps=dict(outcome=dict(main=WIN,sb=WSB),main_match_distribution={k:dist.get(k,0) for k in range(6)},best_main=best,best_candidates=[r['id'] for r in pool if r['main_matches']==best],
  v1_selected=[r for r in pool if r['id']==pred['selection']['candidate_id']][0],jev_preferred=dict(id=an['overall']['choice'],probability=pr[an['overall']['choice']],confidence=an['overall']['confidence'],main_matches=[r['main_matches'] for r in pool if r['id']==an['overall']['choice']][0]),
  candidates_with_correct_sb=sum(r['sb_match'] for r in pool),materially_outperformed_v1=[r['id'] for r in pool if r['main_matches']>=2],
  random_reference=dict(expected_main=5/7,p_ticket_ge2=float(hg(35,5,5)[2:].sum()),p_any_of_20_ge2=float(1-(1-hg(35,5,5)[2:].sum())**20),expected_candidates_ge2=float(20*hg(35,5,5)[2:].sum())),
  jev_choice_vs_matches_spearman=float(np.corrcoef(np.argsort(np.argsort([r['jev_choice'] for r in pool])),np.argsort(np.argsort([r['main_matches'] for r in pool])))[0,1]),
  note='No candidate is promoted retrospectively.')
save(O/'pool_scores.json',dict(summary=ps,candidates=pool))

# ---------------------------------------------------------------- 4. historical reconstruction through #1754 (forensic context)
records,d,sb,ids=S.load(D/'draws.json');assert ids[-1]==1753
full=records+[dict(draw_id=1754,date='2026-09-25',numbers=WIN,super_ball=WSB)]
d2=np.array([r['numbers'] for r in full])-1;sb2=np.array([r['super_ball'] for r in full])-1;ids2=[r['draw_id'] for r in full]
C=S.cache(d2,sb2,ids2);val=S.validate(C,ids2);assert all(v['mains'] and v['super_balls'] and v['generators'] for v in val.values()),val
hist=[]
for ci in range(49,len(ids2)):     # cutoffs 1626..1754 -> targets 1627..1755 (last has no outcome)
    rows,fit=S.run_at_cutoff(C,ci);cs=S.candidates(fit);g,mp=S.gate(rows);tgt=ids2[ci]+1
    o=None if tgt>1754 else dict(main=full[ci+1]['numbers'],sb=full[ci+1]['super_ball'])
    hist.append(dict(target=tgt,candidates=cs,gate=g,min_holm=mp,outcome=o,sb_weights=fit['sb_weights'].tolist(),sb_scores=fit['sb_scores'].tolist()))
save(O/'v1_history_states.json',dict(validation=val,states=[{k:v for k,v in h.items() if k not in ('sb_scores',)} for h in hist]))
H=[h for h in hist if h['outcome'] and h['candidates']]
# fixed-seed study (V1 has no overlap rule)
def chain(pick):
    sel=[]
    for i,h in enumerate(H):
        cs=sorted(h['candidates'],key=lambda c:c['id']);sel.append(cs[pick(i,len(cs),h['target'])])
    return sel
def met(sel):
    ids_=[c['id'] for c in sel];m=[len(set(c['main'])&set(h['outcome']['main'])) for c,h in zip(sel,H)];sbh=[int(c['super_ball']==h['outcome']['sb']) for c,h in zip(sel,H)]
    ov=[len(set(x['main'])&set(y['main'])) for x,y in zip(sel,sel[1:])];nums=Counter(x for c in sel for x in c['main'])
    return dict(distinct_ids=len(set(ids_)),top_id_share=Counter(ids_).most_common(1)[0][1]/len(ids_),same_id_consecutive=float(np.mean([a==b for a,b in zip(ids_,ids_[1:])])),
                same_sb_consecutive=float(np.mean([x['super_ball']==y['super_ball'] for x,y in zip(sel,sel[1:])])),distinct_sbs=len({c['super_ball'] for c in sel}),
                mean_consecutive_main_overlap=float(np.mean(ov)),max_number_rate=max(nums.values())/len(sel),mean_main=float(np.mean(m)),sd_main=float(np.std(m,ddof=1)),ge2=int(sum(x>=2 for x in m)),sb_hits=int(sum(sbh)),
                generator_shares=dict(Counter(c['main_generator'] for c in sel)),sb_generator_shares=dict(Counter(c['SB_generator'] for c in sel)))
SEEDS=[sl.SEED]+list(range(1,1001))
fixed={s:met(chain(lambda i,n,t,s=s:int(np.random.default_rng(s).integers(n)))) for s in SEEDS}
perdraw={s:met(chain(lambda i,n,t,s=s:int(np.random.default_rng(s+t).integers(n)))) for s in SEEDS[:301]}
def dd(x,k):v=np.array([m[k] for m in x.values()]);return dict(mean=float(v.mean()),p05=float(np.quantile(v,.05)),p95=float(np.quantile(v,.95)))
keys=['distinct_ids','top_id_share','same_id_consecutive','same_sb_consecutive','distinct_sbs','mean_consecutive_main_overlap','max_number_rate','mean_main','sd_main','ge2','sb_hits']
# SB coverage and compression across history
sbcov=[];comp=[]
for h in H:
    sbs={c['super_ball'] for c in h['candidates']};sbcov.append(dict(target=h['target'],distinct_sbs=len(sbs),actual_sb_in_pool=h['outcome']['sb'] in sbs))
    union=set(x for c in h['candidates'] for x in c['main']);comp.append(dict(target=h['target'],union=len(union),winners_in_union=len(union&set(h['outcome']['main'])),best=max(len(set(c['main'])&set(h['outcome']['main'])) for c in h['candidates'])))
un=np.array([c['union'] for c in comp]);wu=np.array([c['winners_in_union'] for c in comp])
seed_study=dict(targets=[H[0]['target'],H[-1]['target']],n=len(H),gate_flagged=[h['target'] for h in H if h['gate']['main'] or h['gate']['SB']],
  production=fixed[sl.SEED],fixed_seed_designs={k:dd(fixed,k) for k in keys},per_draw_seed_designs={k:dd(perdraw,k) for k in keys},
  fallback_index_by_n={n:int(np.random.default_rng(sl.SEED).integers(n)) for n in range(15,21)},
  sb_pool_coverage=dict(mean_distinct_sbs=float(np.mean([x['distinct_sbs'] for x in sbcov])),actual_sb_in_pool_rate=float(np.mean([x['actual_sb_in_pool'] for x in sbcov])),
       expected_if_k_distinct='k/10',targets_1753_1754=[x for x in sbcov if x['target'] in (1753,1754)]),
  compression=dict(mean_union_of_20_candidates=float(un.mean()),mean_winners_in_union=float(wu.mean()),expected_winners_in_union=float(np.mean(un*5/35)),
       mean_best_candidate=float(np.mean([c['best'] for c in comp])),targets_1753_1754=[c for c in comp if c['target'] in (1753,1754)]),
  note='Research only; production seed unchanged. V1 Super Lotto has no previous-ticket rule, so any fixed seed repeats the same candidate position every draw.')
save(O/'seed_and_construction.json',seed_study)

# ---------------------------------------------------------------- 5. V2 test (V1 components, data through #1754)
rows,fit=S.run_at_cutoff(C,len(ids2)-1);g,mp=S.gate(rows)
conf=[r for r in rows if r['period']=='confirmation']
selectors=[]
for domain,names,key,NN,KK,base in [('main',sl.MN,'main_hits',35,5,sl.BASE),('SB',sl.SN,'SB_hits',10,1,.1)]:
    ys=[np.array([r[key][j] for r in conf]) for j in range(len(names))];ph=holm([pmean(y,NN,KK,KK) for y in ys])
    for nm,y,p in zip(names,ys,ph):selectors.append(dict(domain=domain,model=nm,n=len(y),mean=float(y.mean()),random=base,holm_p=float(p),block95=[float(x) for x in blockci(y)],halves=[float(y[:len(y)//2].mean()),float(y[len(y)//2:].mean())],passes=nm in g[domain]))
_,build,_=sl.walk(d2,sb2,ids2,build=True);last=max(b['index'] for b in build);cons=[]
for mth in sorted({b['method'] for b in build}):
    y=np.array([b['hits'] for b in build if b['method']==mth and b['index']>=last-39]);cons.append(dict(method=mth,n=len(y),mean=float(y.mean()),p=pmean(y,35,5,5),block95=[float(x) for x in blockci(y)],halves=[float(y[:len(y)//2].mean()),float(y[len(y)//2:].mean())]))
for r,p in zip(cons,holm([r['p'] for r in cons])):r['holm_p']=float(p);r['passes']=bool(p<.05 and r['block95'][0]>sl.BASE and min(r['halves'])>sl.BASE)
fixm=fixed[sl.SEED]['mean_main'];pdm=dd(perdraw,'mean_main')
v2=dict(data_through=1754,origins=len(rows),selectors=selectors,construction_methods=sorted(cons,key=lambda r:r['holm_p'])[:12],construction_family_size=len(cons),
  any_selector_passes=any(s['passes'] for s in selectors),any_construction_passes=any(r['passes'] for r in cons),
  fallback_design=dict(production_mean_main=fixm,per_draw_seed_mean_main=pdm,note='Both are random selections among the same candidates; no expected difference and no gate can be passed.'),
  conclusion='NO SUPER LOTTO V2 IS JUSTIFIED' if not (any(s['passes'] for s in selectors) or any(r['passes'] for r in cons)) else 'A refinement passed; see details')
save(O/'v2_decision.json',v2)
print(json.dumps(dict(verification_order_ok=verification['order_ok'],pool=ps['main_match_distribution'],best=ps['best_candidates'],sb_correct=ps['candidates_with_correct_sb'],pool_sbs=pool_sbs,sb1753=pool_sbs_1753,
      seed=dict(prod={k:fixed[sl.SEED][k] for k in keys},fixed={k:dd(fixed,k)['mean'] for k in keys},perdraw={k:dd(perdraw,k)['mean'] for k in keys}),sbcov=seed_study['sb_pool_coverage'],comp=seed_study['compression'],
      v2=v2['conclusion'],best_selectors=sorted(selectors,key=lambda s:s['holm_p'])[:3],best_cons=v2['construction_methods'][:3],gate_flagged=seed_study['gate_flagged']),indent=1,default=str))
json.dump(verification,open(O/'verification.json','w'),indent=1)
