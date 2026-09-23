import itertools, numpy as np; from math import comb; from scipy import stats; N=38; K=6
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
