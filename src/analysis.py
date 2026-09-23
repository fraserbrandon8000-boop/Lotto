"""Steps 2-10: baseline, randomness tests, strict walk-forward model/ticket evaluation, #2339 forensics."""
import json, itertools, numpy as np, pandas as pd
from math import comb
from scipy import stats
OUT = "results/claude_lotto_2340"; N = 38; K = 6
SEED = 23402026; rng_master = np.random.default_rng(SEED)
d = pd.read_csv(f"{OUT}/normalized_draws.csv")
D = d[["n1","n2","n3","n4","n5","n6"]].values.astype(int); seg = d.segment.values; ids = d.draw.values
T = len(D); X = np.zeros((T, N+1), bool)
for t in range(T): X[t, D[t]] = True
X = X[:, 1:]  # T x 38 incidence
res = {}
def hyp(k): return stats.hypergeom(N, K, k)   # hits of a k-number pool among 6 winners
# ---------------- Step 2 baseline
p = {m: comb(6,m)*comb(32,6-m)/comb(38,6) for m in range(7)}
res["baseline"] = dict(P=p, expected=36/38, P3plus=sum(p[m] for m in (3,4,5,6)), P4plus=sum(p[m] for m in (4,5,6)),
                       P5plus=p[5]+p[6], jackpot=p[6], jackpot_one_in=comb(38,6))
# ---------------- Step 3/4 randomness tests (Monte Carlo under iid uniform 6-of-38)
def sim_draws(n, rng): return np.argsort(rng.random((n, N)), axis=1)[:, :K]
def stat_all(Xm, segv):
    f = Xm.sum(0); e = Xm.shape[0]*K/N
    chi = ((f-e)**2/e).sum()
    ok = segv[1:] == segv[:-1]
    rep = (Xm[1:] & Xm[:-1]).sum(1)[ok].mean()
    # pair co-occurrence dispersion + max
    C = Xm.T.astype(int) @ Xm.astype(int); iu = np.triu_indices(N, 1); pc = C[iu]
    pe = Xm.shape[0]*comb(36,4)/comb(38,6)
    pchi = ((pc-pe)**2/pe).sum(); pmax = pc.max()
    idx = np.where(Xm)[1].reshape(-1, K)+1
    sums = idx.sum(1); odd = (idx % 2).sum(1); low = (idx <= 19).sum(1); rng_ = idx[:, -1]-idx[:, 0]
    adj = (np.diff(idx, axis=1) == 1).any(1).mean()
    # lag-1 autocorrelation of per-number indicator (serial dependence), averaged
    a = []
    for j in range(N):
        x = Xm[:, j].astype(float); a.append(np.corrcoef(x[1:][ok], x[:-1][ok])[0, 1])
    # gap distribution: gaps between consecutive appearances within segment (dispersion vs geometric)
    gaps = []
    for j in range(N):
        for s_ in (0, 1):
            w = np.where(Xm[segv == s_, j])[0]; gaps += list(np.diff(w))
    gaps = np.array(gaps)
    # transition: does the number of repeats from t-2 differ (lag-2)
    ok2 = (segv[2:] == segv[:-2]); rep2 = (Xm[2:] & Xm[:-2]).sum(1)[ok2].mean()
    return dict(freq_chi2=chi, repeat_lag1=rep, repeat_lag2=rep2, pair_chi2=pchi, pair_max=pmax,
                sum_mean=sums.mean(), sum_sd=sums.std(), odd_mean=odd.mean(), low_mean=low.mean(),
                range_mean=rng_.mean(), adjacency_rate=adj, mean_lag1_autocorr=np.nanmean(a),
                gap_mean=gaps.mean(), gap_var=gaps.var())
obs = stat_all(X, seg)
NSIM = 4000; rngs = np.random.default_rng(SEED+1); sims = []
for _ in range(NSIM):
    idx = sim_draws(T, rngs); Xs = np.zeros((T, N), bool); np.put_along_axis(Xs, idx, True, 1); sims.append(stat_all(Xs, seg))
sims = pd.DataFrame(sims); tests = {}
for k, v in obs.items():
    s = sims[k].values; pl = (np.sum(s <= v)+1)/(NSIM+1); pu = (np.sum(s >= v)+1)/(NSIM+1)
    tests[k] = dict(observed=float(v), null_mean=float(s.mean()), null_sd=float(s.std()), p_two_sided=float(min(1, 2*min(pl, pu))))
ps = [tests[k]["p_two_sided"] for k in tests]; holm = stats.false_discovery_control(ps, method="bh")
order = np.argsort(ps); m = len(ps); hp = np.empty(m); run = 0
for r, i in enumerate(order): run = max(run, min(1, (m-r)*ps[i])); hp[i] = run
for (k, _), h, b in zip(tests.items(), hp, holm): tests[k]["p_holm"] = float(h); tests[k]["q_bh"] = float(b)
res["randomness_tests"] = dict(n_sim=NSIM, tests=tests)
freq = X.sum(0); res["frequencies_full"] = {int(i+1): int(freq[i]) for i in range(N)}
# ---------------- Step 5-7 causal ranking models
def gap_now(H):  # draws since last appearance (T+1 if never)
    g = np.full(N, H.shape[0]+1.0)
    for j in range(N):
        w = np.where(H[:, j])[0]
        if len(w): g[j] = H.shape[0]-w[-1]
    return g
def pairlift(H):
    C = H.T.astype(float) @ H.astype(float); f = H.sum(0).astype(float); n = H.shape[0]
    E = np.outer(f, f)*(5/(n*6))*(1)  # E[pair]≈ f_i f_j *5/(6 n) under exchangeability
    L = (C+1)/(E+1); np.fill_diagonal(L, 1); return L
def model_scores(H, name, rng):
    n = H.shape[0]
    if name == "freq_all": return H.sum(0).astype(float)
    if name == "freq_w10": return H[-10:].sum(0).astype(float)
    if name == "freq_w20": return H[-20:].sum(0).astype(float)
    if name == "freq_w40": return H[-40:].sum(0).astype(float)
    if name == "ewma_0.9": w = 0.9**np.arange(n)[::-1]; return (H*w[:, None]).sum(0)
    if name == "cold_all": return -H.sum(0).astype(float)
    if name == "overdue_gap": return gap_now(H)
    if name == "recent_hot": return -gap_now(H)
    if name == "trend_20v20": return H[-20:].sum(0)-H[-40:-20].sum(0).astype(float)
    if name == "pair_last": L = pairlift(H); return np.log(L[H[-1]]).sum(0)
    if name == "repeat_last": return H[-1].astype(float)
    if name == "ensemble_eq":
        parts = [model_scores(H, m, rng) for m in ("freq_all", "ewma_0.9", "trend_20v20", "pair_last")]
        return np.mean([stats.rankdata(p_) for p_ in parts], 0)
    if name == "random_control": return rng.random(N)
    raise ValueError(name)
MODELS = ["freq_all", "freq_w10", "freq_w20", "freq_w40", "ewma_0.9", "cold_all", "overdue_gap", "recent_hot",
          "trend_20v20", "pair_last", "repeat_last", "ensemble_eq", "random_control"]
def rank_numbers(sc, rng):  # descending score, random tie-break (seeded) -> array of 0-based numbers
    return np.lexsort((rng.random(N), -sc))
WARM = 40; targets = list(range(WARM, T)); nt = len(targets); half = nt//2
POOLS = [6, 8, 10, 12, 15, 20]
# structural typicality from causal history (for combination construction)
def struct_score(combo, H):
    idx = np.where(H)[1].reshape(-1, K)+1; sm, ss = idx.sum(1).mean(), idx.sum(1).std()
    c = np.array(combo)+1; odd = (c % 2).sum(); low = (c <= 19).sum()
    return -abs(c.sum()-sm)/ss-0.5*abs(odd-3)-0.5*abs(low-3)
def build_tickets(H, ranks_by_model, rng):
    out = {}
    base = ranks_by_model["ensemble_eq"]
    for m, r in ranks_by_model.items(): out[f"top6:{m}"] = sorted(r[:6])
    L = pairlift(H)
    for k in (8, 10, 12, 15):
        pool = base[:k]; best = None
        for c in itertools.combinations(pool, 6):
            rk = -sum(np.where(base == x)[0][0] for x in c)/k
            s_ = struct_score(c, H)+rk*0.2
            if best is None or s_ > best[0]: best = (s_, c)
        out[f"struct_opt_top{k}:ensemble"] = sorted(best[1])
    for k in (10, 12):
        pool = base[:k]; best = None
        for c in itertools.combinations(pool, 6):
            s_ = sum(np.log(L[a, b]) for a, b in itertools.combinations(c, 2))
            if best is None or s_ > best[0]: best = (s_, c)
        out[f"pair_opt_top{k}:ensemble"] = sorted(best[1])
    votes = np.zeros(N)
    for m, r in ranks_by_model.items():
        if m != "random_control": votes[r[:6]] += 1
    out["consensus_votes"] = sorted(np.lexsort((rng.random(N), -votes))[:6])
    # diversity: take best-ranked number per band of ~6
    bands = [range(0, 7), range(7, 13), range(13, 19), range(19, 25), range(25, 31), range(31, 38)]
    out["diversity_bands:ensemble"] = sorted([next(x for x in base if x in b) for b in bands])
    out["random_ticket"] = sorted(rng.choice(N, 6, replace=False))
    return out
pool_hits = {m: {k: [] for k in POOLS} for m in MODELS}; ticket_hits = {}; rank_log = []
for t in targets:
    H = X[:t]; rng = np.random.default_rng([SEED, t])
    rk = {m: rank_numbers(model_scores(H, m, rng), rng) for m in MODELS}
    win = set(np.where(X[t])[0])
    for m in MODELS:
        for k in POOLS: pool_hits[m][k].append(len(win & set(rk[m][:k])))
    for name, tk in build_tickets(H, rk, rng).items():
        ticket_hits.setdefault(name, []).append(len(win & set(tk)))
# significance helper: sum of iid hypergeom hits vs observed (exact via convolution)
def sum_pvalue(hits, k):
    pm = hyp(k).pmf(np.arange(7)); dist = np.array([1.0])
    for _ in range(len(hits)): dist = np.convolve(dist, pm)
    s = int(np.sum(hits)); return float(dist[s:].sum())
pool_tab = []
for m in MODELS:
    for k in POOLS:
        h = np.array(pool_hits[m][k]); e = 6*k/N
        pool_tab.append(dict(model=m, pool=k, targets=len(h), mean_hits=h.mean(), expected=e, lift=h.mean()/e,
            cov3=(h >= 3).mean(), cov3_exp=hyp(k).sf(2), cov4=(h >= 4).mean(), cov4_exp=hyp(k).sf(3),
            cov5=(h >= 5).mean(), cov5_exp=hyp(k).sf(4), cov6=(h == 6).mean(), cov6_exp=hyp(k).sf(5),
            dev_mean=h[:half].mean(), conf_mean=h[half:].mean(),
            p_full=sum_pvalue(h, k), p_dev=sum_pvalue(h[:half], k), p_conf=sum_pvalue(h[half:], k)))
pool_tab = pd.DataFrame(pool_tab)
pool_tab["p_full_holm"] = np.minimum(1, stats.false_discovery_control(pool_tab.p_full, method="by"))  # BY-FDR (dependent tests)
nm = len(pool_tab); o = np.argsort(pool_tab.p_full.values); hp = np.empty(nm); run = 0
for r, i in enumerate(o): run = max(run, min(1, (nm-r)*pool_tab.p_full.values[i])); hp[i] = run
pool_tab["p_full_holm"] = hp
pool_tab.to_csv(f"{OUT}/model_performance_pools.csv", index=False)
tk_tab = []
for name, h in ticket_hits.items():
    h = np.array(h); se = h.std(ddof=1)/np.sqrt(len(h))
    tk_tab.append(dict(method=name, targets=len(h), total=int(h.sum()), mean=h.mean(), median=float(np.median(h)), sd=h.std(ddof=1),
        ci95_lo=h.mean()-1.96*se, ci95_hi=h.mean()+1.96*se, r0=(h == 0).mean(), r1=(h == 1).mean(), r2=(h == 2).mean(),
        r3=(h == 3).mean(), r4p=(h >= 4).mean(), r5p=(h >= 5).mean(), r6=(h == 6).mean(), expected=36/38,
        dev_mean=h[:half].mean(), conf_mean=h[half:].mean(), p_full=sum_pvalue(h, 6), p_dev=sum_pvalue(h[:half], 6), p_conf=sum_pvalue(h[half:], 6)))
tk_tab = pd.DataFrame(tk_tab); nm = len(tk_tab); o = np.argsort(tk_tab.p_full.values); hp = np.empty(nm); run = 0
for r, i in enumerate(o): run = max(run, min(1, (nm-r)*tk_tab.p_full.values[i])); hp[i] = run
tk_tab["p_full_holm"] = hp; tk_tab = tk_tab.sort_values("mean", ascending=False)
tk_tab.to_csv(f"{OUT}/model_performance_tickets.csv", index=False)
# random-control simulation: distribution of best-of-M mean among M random ticket strategies (selection-bias yardstick)
R = 20000; rr = np.random.default_rng(SEED+2)
rand_means = rr.hypergeometric(6, 32, 6, size=(R, nt)).mean(1)
M_ = len(tk_tab); best_of = rr.hypergeometric(6, 32, 6, size=(2000, M_, nt)).mean(2).max(1)
res["random_control_sim"] = dict(n_targets=nt, single_mean_q95=float(np.quantile(rand_means, .95)), single_mean_q99=float(np.quantile(rand_means, .99)),
                                 best_of_M=M_, best_of_M_mean_q50=float(np.median(best_of)), best_of_M_q95=float(np.quantile(best_of, .95)))
# ---------------- Gate (declared in config before this run): method passes iff Holm-adjusted full p<0.05 AND dev p<0.05 AND conf p<0.05
gate_pool = pool_tab[(pool_tab.p_full_holm < .05) & (pool_tab.p_dev < .05) & (pool_tab.p_conf < .05)]
gate_tk = tk_tab[(tk_tab.p_full_holm < .05) & (tk_tab.p_dev < .05) & (tk_tab.p_conf < .05)]
res["gate"] = dict(rule="Holm-adj full-sample one-sided p<0.05 AND development p<0.05 AND confirmation p<0.05",
                   pool_methods_passing=gate_pool[["model", "pool"]].values.tolist(), ticket_methods_passing=gate_tk.method.tolist(),
                   validated_edge=bool(len(gate_pool) or len(gate_tk)))
res["walkforward"] = dict(warmup=WARM, n_targets=nt, first_target=int(ids[targets[0]]), last_target=int(ids[targets[-1]]),
                          dev=[int(ids[targets[0]]), int(ids[targets[half-1]])], conf=[int(ids[targets[half]]), int(ids[targets[-1]])])
# ---------------- Step 10 forensic #2339 (history strictly before 2339)
t9 = int(np.where(ids == 2339)[0][0]); H = X[:t9]; g = gap_now(H)
feat = pd.DataFrame(dict(number=np.arange(1, N+1), freq_all=H.sum(0), freq_w10=H[-10:].sum(0), freq_w20=H[-20:].sum(0),
        ewma=(H*(0.9**np.arange(H.shape[0])[::-1])[:, None]).sum(0).round(3), gap=g, trend=H[-20:].sum(0)-H[-40:-20].sum(0),
        in_2338=H[-1].astype(int), pair_last=np.log(pairlift(H)[H[-1]]).sum(0).round(3)))
for c in ["freq_all", "freq_w10", "freq_w20", "ewma", "gap", "trend", "pair_last"]:
    feat[c+"_rank"] = stats.rankdata(-feat[c], method="average")
grp = {"selected_hits(1,4,13)": [1, 4, 13], "selected_losers(14,24,38)": [14, 24, 38], "missed_winners(6,23,28)": [6, 23, 28]}
fz = {k: feat[feat.number.isin(v)].to_dict("records") for k, v in grp.items()}
p_ge3 = res["baseline"]["P3plus"]
res["forensic_2339"] = dict(groups=fz, note="Hits 1 and 13 were both in #2338 (prior-draw repeat) -> tested by repeat_last model",
                            p_3plus_random_ticket=p_ge3, p_value_single_observation=p_ge3)
res["pool_table_top"] = pool_tab.sort_values("p_full").head(12).round(4).to_dict("records")
res["ticket_table"] = tk_tab.round(4).to_dict("records")
json.dump(res, open(f"{OUT}/analysis_results.json", "w"), indent=2, default=float)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print(json.dumps(res["baseline"], indent=1)); print(pd.DataFrame(tests).T.round(4))
print(pool_tab.round(3)[["model","pool","mean_hits","expected","lift","cov3","cov3_exp","dev_mean","conf_mean","p_full","p_full_holm"]].to_string())
print(tk_tab.round(3)[["method","mean","sd","ci95_lo","ci95_hi","r0","r3","r4p","dev_mean","conf_mean","p_full","p_full_holm"]].to_string())
print(res["random_control_sim"], res["gate"], res["walkforward"])
print(feat[feat.number.isin([1,4,13,14,24,38,6,23,28])].to_string())
