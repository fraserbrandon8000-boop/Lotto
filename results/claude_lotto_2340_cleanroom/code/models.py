"""Number rankers and ticket constructors. Every function sees only the history passed to it."""
import math
from itertools import combinations

import numpy as np

from common import K_DRAW, MASTER_SEED, N_BALLS, all_tickets

P1 = K_DRAW / N_BALLS
COMPONENTS = ["A_freq_all", "B_ew_20", "C_hazard", "D_trend_20v40", "E_transition"]
RANKERS = (["H_random", "A_freq_all", "A_inv_cold"]
           + [f"B_roll_{w}" for w in (10, 20, 30, 50, 100)]
           + [f"B_ew_{h}" for h in (10, 20, 40)]
           + ["C_overdue", "C_recent", "C_hazard", "C_own_gap_pct", "D_trend_20v40", "D_slope_50",
              "E_transition", "E_pair_centrality", "G_ensemble_equal", "G_ensemble_adaptive"])


# ---------------------------------------------------------------- history statistics
def gaps_now(H):
    """Draws since last appearance (1 = appeared in the latest history draw); never seen -> len+1."""
    t = len(H)
    g = np.full(N_BALLS, t + 1)
    for j in range(N_BALLS):
        nz = np.flatnonzero(H[:, j])
        if len(nz):
            g[j] = t - nz[-1]
    return g


def own_gaps(H):
    out = []
    for j in range(N_BALLS):
        nz = np.flatnonzero(H[:, j])
        out.append(np.diff(nz))
    return out


def hazard_table(H, cap=25):
    """Pooled P(appear next | current gap g), Beta(6,32)-smoothed, from history only."""
    t = len(H)
    at_risk = np.zeros(cap + 1)
    hits = np.zeros(cap + 1)
    last = np.full(N_BALLS, -1)
    for s in range(t):
        seen = last >= 0
        g = np.minimum(s - last[seen], cap)
        np.add.at(at_risk, g, 1)
        np.add.at(hits, g, H[s, seen])
        last[H[s] == 1] = s
    return (hits + 6.0) / (at_risk + 38.0)


def pair_z(H):
    """Frequency-adjusted pair co-occurrence z-scores (38x38, diagonal 0)."""
    t = max(len(H), 1)
    Hf = H.astype(float)
    P = Hf.T @ Hf
    n = Hf.sum(0)
    e = np.outer(n, n) / t * (5 * 38) / (37 * 6)
    z = (P - e) / np.sqrt(e + 1.0)
    np.fill_diagonal(z, 0.0)
    return z


def transition_lift(H, valid_h, alpha=10.0):
    """Smoothed lift P(k at s | j at s-1) / P1 from consecutive pairs inside the history."""
    ok = valid_h[1:].astype(float)[:, None]
    A = H[:-1].astype(float) * ok
    C = A.T @ H[1:].astype(float)
    nj = A.sum(0)[:, None]
    return (C + alpha * P1) / (nj + alpha) / P1


def pct_rank(v):
    order = np.argsort(np.argsort(v, kind="stable"), kind="stable")
    return order / (len(v) - 1)


# ---------------------------------------------------------------- rankers
def compute_scores(H, valid_h, target_consecutive, t_index, adaptive_w=None):
    """All ranker scores for the draw following history H (rows = draws, cols = balls)."""
    t = len(H)
    S = {}
    rng = np.random.default_rng(MASTER_SEED + t_index)
    S["H_random"] = rng.random(N_BALLS)
    S["A_freq_all"] = H.sum(0).astype(float)
    S["A_inv_cold"] = -S["A_freq_all"]
    for w in (10, 20, 30, 50, 100):
        S[f"B_roll_{w}"] = H[max(0, t - w):].sum(0).astype(float)
    ages = np.arange(t - 1, -1, -1)
    for h in (10, 20, 40):
        S[f"B_ew_{h}"] = (0.5 ** (ages / h))[:, None].T @ H.astype(float)
        S[f"B_ew_{h}"] = S[f"B_ew_{h}"].ravel()
    g = gaps_now(H)
    S["C_overdue"] = g.astype(float)
    S["C_recent"] = -g.astype(float)
    hz = hazard_table(H)
    S["C_hazard"] = hz[np.minimum(g, len(hz) - 1)]
    og = own_gaps(H)
    S["C_own_gap_pct"] = np.array([((x < g[j]).sum() + 0.5 * (x == g[j]).sum()) / len(x) if len(x) >= 3 else 0.5
                                   for j, x in enumerate(og)])
    recent = H[max(0, t - 20):].mean(0)
    before = H[max(0, t - 60):max(0, t - 20)]
    S["D_trend_20v40"] = recent - (before.mean(0) if len(before) else P1)
    W = H[max(0, t - 50):].astype(float)
    x = np.arange(len(W)) - (len(W) - 1) / 2
    S["D_slope_50"] = (x[:, None] * (W - W.mean(0))).sum(0) / max((x * x).sum(), 1e-9)
    if target_consecutive and t >= 2:
        L = transition_lift(H, valid_h)
        prev = np.flatnonzero(H[-1])
        S["E_transition"] = L[prev].mean(0)
    else:
        S["E_transition"] = np.ones(N_BALLS)
    z = pair_z(H)
    S["E_pair_centrality"] = np.clip(z, 0, None).sum(1)
    comp = np.array([pct_rank(S[c]) for c in COMPONENTS])
    S["G_ensemble_equal"] = comp.mean(0)
    w = np.ones(len(COMPONENTS)) if adaptive_w is None else np.asarray(adaptive_w, float)
    if w.sum() <= 0:
        w = np.ones(len(COMPONENTS))
    S["G_ensemble_adaptive"] = (w[:, None] * comp).sum(0) / w.sum()
    # neutral, seeded tie-breaking jitter (never favours low or high numbers)
    jit = np.random.default_rng(MASTER_SEED * 7 + t_index).random(N_BALLS) * 1e-9
    for k in S:
        sd = S[k].std()
        S[k] = S[k] + jit * (sd if sd > 0 else 1.0)
    return S, z


def ranking(score):
    return np.argsort(-score, kind="stable") + 1  # ball numbers, best first


# ---------------------------------------------------------------- structure null
_STRUCT = None


def structure_tables():
    """Exact null probability of each structure class, plus sum-decile edges."""
    global _STRUCT
    if _STRUCT is None:
        A = all_tickets().astype(np.int16)
        s = A.sum(1)
        edges = np.quantile(s, np.linspace(0, 1, 11))[1:-1]
        dec = np.searchsorted(edges, s, side="right")
        odd = (A % 2).sum(1)
        low = (A <= 19).sum(1)
        cons = np.minimum((np.diff(A, axis=1) == 1).sum(1), 2)
        key = ((dec * 7 + odd) * 7 + low) * 3 + cons
        cnt = np.bincount(key, minlength=10 * 7 * 7 * 3).astype(float)
        prob = cnt / len(A)
        logp_all = np.log(prob[key])
        _STRUCT = {"edges": edges, "prob": prob, "logp_mean": logp_all.mean(), "logp_sd": logp_all.std()}
    return _STRUCT


def struct_key(T6):
    st = structure_tables()
    T6 = np.sort(np.asarray(T6), axis=-1)
    s = T6.sum(-1)
    dec = np.searchsorted(st["edges"], s, side="right")
    odd = (T6 % 2).sum(-1)
    low = (T6 <= 19).sum(-1)
    cons = np.minimum((np.diff(T6, axis=-1) == 1).sum(-1), 2)
    return ((dec * 7 + odd) * 7 + low) * 3 + cons


def struct_z(T6):
    st = structure_tables()
    lp = np.log(np.maximum(st["prob"][struct_key(T6)], 1e-12))
    return (lp - st["logp_mean"]) / st["logp_sd"]


_COMB = {}


def combos(m):
    if m not in _COMB:
        _COMB[m] = np.array(list(combinations(range(m), K_DRAW)))
    return _COMB[m]


_PAIRS6 = np.array(list(combinations(range(6), 2)))


def eval_subsets(pool, score, z, lam_pair, lam_struct):
    """Return (tickets, J, parts) for all 6-subsets of pool (ball numbers)."""
    pool = np.asarray(pool)
    C = combos(len(pool))
    T6 = pool[C]
    sc = (score - score.mean()) / (score.std() + 1e-12)
    s_part = sc[T6 - 1].mean(1)
    p_part = z[T6[:, _PAIRS6[:, 0]] - 1, T6[:, _PAIRS6[:, 1]] - 1].mean(1)
    st_part = struct_z(T6)
    J = s_part + lam_pair * p_part + lam_struct * st_part
    return T6, J, (s_part, p_part, st_part)


def build_ticket(kind, score, z, t_index, consensus_rankings=None, lam_pair=0.5, lam_struct=0.5, ens_score=None):
    r = ranking(score) if score is not None else None
    if kind == "top6":
        return np.sort(r[:6])
    if kind.startswith("opt_top"):
        m = int(kind[7:])
        T6, J, _ = eval_subsets(r[:m], score, z, lam_pair, lam_struct)
        return np.sort(T6[np.argmax(J)])
    if kind == "pair_top12":
        T6, J, (s, p, st) = eval_subsets(r[:12], score, z, 0, 0)
        return np.sort(T6[np.lexsort((-s, -p))[0]])
    if kind == "struct_top12":
        T6, J, (s, p, st) = eval_subsets(r[:12], score, z, 0, 0)
        return np.sort(T6[np.lexsort((-s, -st))[0]])
    if kind == "diversity_top15":
        out, band = [], {}
        for b in r[:15]:
            k = min((b - 1) // 10, 3)
            if band.get(k, 0) < 2:
                out.append(b)
                band[k] = band.get(k, 0) + 1
            if len(out) == 6:
                break
        for b in r:  # fallback (never needed with 4 bands x 2 >= 6 but kept for safety)
            if len(out) == 6:
                break
            if b not in out:
                out.append(b)
        return np.sort(np.array(out))
    if kind == "consensus":
        votes = np.zeros(N_BALLS)
        for rk in consensus_rankings:
            votes[np.asarray(rk[:12]) - 1] += 1
        key = votes + 1e-3 * pct_rank(ens_score)
        return np.sort(np.argsort(-key, kind="stable")[:6] + 1)
    if kind == "random_ticket":
        return np.sort(np.random.default_rng(MASTER_SEED * 13 + t_index).choice(np.arange(1, 39), 6, replace=False))
    raise ValueError(kind)
