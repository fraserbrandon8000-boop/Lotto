"""Step 4: is the draw history consistent with an independent uniform 6-of-38 process?

Every global test gets an exact or Monte Carlo null computed under that process with the same
observed-draw sequence and the same consecutive-ID mask (the 2252-2261 gap), then Holm correction.
"""
import math
import os

import numpy as np
from scipy import stats

from common import (K_DRAW, MASTER_SEED, N_BALLS, OUT, all_tickets, bh, convolve_n, holm,
                    indicator_matrix, load_draws, pool_pmf, write_json)

N_SIM = 20000
CHUNK = 500
GAP_BINS = list(range(1, 16))  # 1..15 and 16+


def sim_indicators(rng, n, T):
    idx = rng.random((n, T, N_BALLS)).argpartition(K_DRAW, axis=2)[:, :, :K_DRAW]
    X = np.zeros((n, T, N_BALLS), dtype=np.int8)
    np.put_along_axis(X, idx, 1, axis=2)
    return X


def gap_hist(X):
    """Pooled histogram of re-appearance gaps (in observed draws). X: (S,T,38)."""
    S, T, _ = X.shape
    t_idx = np.arange(T)[None, :, None]
    last = np.where(X == 1, t_idx, -1)
    last = np.maximum.accumulate(last, axis=1)
    prev = np.concatenate([np.full((S, 1, N_BALLS), -1), last[:, :-1]], axis=1)
    gaps = np.where((X == 1) & (prev >= 0), t_idx - prev, 0)
    h = np.zeros((S, len(GAP_BINS) + 1))
    for b, g in enumerate(GAP_BINS):
        h[:, b] = (gaps == g).sum(axis=(1, 2))
    h[:, -1] = (gaps > GAP_BINS[-1]).sum(axis=(1, 2))
    return h


def stats_block(X, valid, sums):
    """Global statistics for a stack of indicator matrices X (S,T,38)."""
    S, T, _ = X.shape
    Xf = X.astype(np.float32)
    counts = Xf.sum(1)
    E = T * K_DRAW / N_BALLS
    out = {
        "freq_chisq": ((counts - E) ** 2 / E).sum(1),
        "freq_max": counts.max(1),
        "freq_min": -counts.min(1),  # larger = more extreme low
    }
    pair = np.einsum("stj,stk->sjk", Xf, Xf)
    iu = np.triu_indices(N_BALLS, 1)
    pc = pair[:, iu[0], iu[1]]
    Ep = T * (K_DRAW * (K_DRAW - 1)) / (N_BALLS * (N_BALLS - 1))
    out["pair_chisq"] = ((pc - Ep) ** 2 / Ep).sum(1)
    out["pair_max"] = pc.max(1)
    v = valid[1:].astype(np.float32)[None, :, None]
    for L in (1, 2, 3, 4, 5):
        # lag-L overlap only when the L draws in between are all consecutive IDs
        okL = np.array([all(valid[t - k] for k in range(L)) for t in range(L, T)], dtype=np.float32)
        ov = (Xf[:, L:, :] * Xf[:, :-L, :]).sum(2)
        out[f"lag{L}_overlap"] = (ov * okL[None, :]).sum(1)
    M = np.einsum("stj,stk->sjk", Xf[:, :-1, :] * v, Xf[:, 1:, :])
    n_pairs = valid[1:].sum()
    Em = n_pairs * (K_DRAW / N_BALLS) ** 2
    out["transition_chisq"] = ((M - Em) ** 2 / Em).sum((1, 2))
    gh = gap_hist(X)
    p = K_DRAW / N_BALLS
    probs = np.array([p * (1 - p) ** (g - 1) for g in GAP_BINS] + [(1 - p) ** GAP_BINS[-1]])
    tot = gh.sum(1, keepdims=True)
    out["gap_chisq"] = ((gh - tot * probs) ** 2 / (tot * probs)).sum(1)
    out["gap_mean"] = (gh * np.array(GAP_BINS + [20])).sum(1) / tot[:, 0]
    s = sums.astype(np.float32)
    ok = valid[1:].astype(bool)
    a, b = s[:, :-1][:, ok], s[:, 1:][:, ok]
    a = a - a.mean(1, keepdims=True)
    b = b - b.mean(1, keepdims=True)
    out["sum_lag1_autocorr"] = (a * b).sum(1) / np.sqrt((a * a).sum(1) * (b * b).sum(1))
    return out


TWO_SIDED = {"lag1_overlap", "lag2_overlap", "lag3_overlap", "lag4_overlap", "lag5_overlap",
             "sum_lag1_autocorr", "gap_mean"}


def main():
    rng = np.random.default_rng(MASTER_SEED + 4)
    ids, dates, mains, bonus = load_draws()
    T = len(ids)
    X = indicator_matrix(mains)
    valid = np.concatenate([[False], np.diff(ids) == 1])
    obs = stats_block(X[None], valid, mains.sum(1)[None])
    obs = {k: float(v[0]) for k, v in obs.items()}

    sims = {k: [] for k in obs}
    for _ in range(N_SIM // CHUNK):
        Xs = sim_indicators(rng, CHUNK, T)
        sums = (Xs * np.arange(1, N_BALLS + 1)[None, None, :]).sum(2)
        for k, v in stats_block(Xs, valid, sums).items():
            sims[k].append(v)
    sims = {k: np.concatenate(v) for k, v in sims.items()}

    tests = []

    def mc(name, desc):
        s = sims[name]
        o = obs[name]
        if name in TWO_SIDED:
            c = np.median(s)
            p = (1 + np.sum(np.abs(s - c) >= abs(o - c) - 1e-9)) / (1 + len(s))
        else:
            p = (1 + np.sum(s >= o - 1e-9)) / (1 + len(s))
        tests.append({"test": name, "description": desc, "observed": o, "null_mean": float(s.mean()),
                      "null_sd": float(s.std()), "p_value": float(p), "method": f"Monte Carlo ({len(s)} sims)"})

    mc("freq_chisq", "Chi-square of the 38 number counts vs uniform expectation")
    mc("freq_max", "Largest single-number count")
    mc("freq_min", "Smallest single-number count (negated)")
    mc("gap_chisq", "Pooled re-appearance gap histogram vs geometric(6/38), bins 1..15,16+")
    mc("gap_mean", "Mean re-appearance gap (two-sided)")
    mc("pair_chisq", "Dispersion of the 703 pair co-occurrence counts")
    mc("pair_max", "Largest pair co-occurrence count")
    mc("transition_chisq", "38x38 previous-draw -> next-draw transition matrix vs independence")
    mc("sum_lag1_autocorr", "Lag-1 autocorrelation of the draw sum (two-sided)")

    # exact repeat / lag overlap tests (overlaps are iid Hypergeometric(38,6,6) under the null)
    hp = pool_pmf(6)
    for L in (1, 2, 3, 4, 5):
        n = int(np.sum([all(valid[t - k] for k in range(L)) for t in range(L, T)]))
        o = int(obs[f"lag{L}_overlap"])
        dist = convolve_n(hp, n)
        mean = n * 36 / 38
        lo, hi = dist[: o + 1].sum(), dist[o:].sum()
        tests.append({"test": f"lag{L}_overlap", "description": f"Numbers shared with the draw {L} earlier (lag {L}); lag 1 = repeat behaviour",
                      "observed": o, "pairs": n, "null_mean": mean, "observed_per_draw": o / n,
                      "p_value": float(min(1.0, 2 * min(lo, hi))), "method": "exact convolution, two-sided"})

    # structure tests against exact enumeration of all C(38,6) tickets
    A = all_tickets().astype(np.int16)
    s_all = A.sum(1)
    odd_all = (A % 2).sum(1)
    low_all = (A <= 19).sum(1)
    cons_all = (np.diff(A, axis=1) == 1).sum(1)
    rng_all = A[:, -1] - A[:, 0]
    M = mains.astype(np.int16)
    feats = {
        "sum": (s_all, M.sum(1)),
        "odd_count": (odd_all, (M % 2).sum(1)),
        "low_count_1_19": (low_all, (M <= 19).sum(1)),
        "consecutive_pairs": (cons_all, (np.diff(M, axis=1) == 1).sum(1)),
        "range": (rng_all, M[:, -1] - M[:, 0]),
    }
    structure_summary = {}
    for name, (null_vals, o_vals) in feats.items():
        if name in ("sum", "range"):
            edges = np.unique(np.quantile(null_vals, np.linspace(0, 1, 11)))
            edges[-1] += 1
            nb = np.histogram(null_vals, bins=edges)[0] / len(null_vals)
            ob = np.histogram(o_vals, bins=edges)[0]
        else:
            vals = np.arange(0, 7)
            nb = np.array([(null_vals == v).mean() for v in vals])
            ob = np.array([(o_vals == v).sum() for v in vals])
            # merge sparse tails so expected >= 5
            while len(nb) > 2 and nb[-1] * T < 5:
                nb[-2] += nb[-1]; ob[-2] += ob[-1]; nb = nb[:-1]; ob = ob[:-1]
            while len(nb) > 2 and nb[0] * T < 5:
                nb[1] += nb[0]; ob[1] += ob[0]; nb = nb[1:]; ob = ob[1:]
        exp = nb * T
        chi = float(((ob - exp) ** 2 / exp).sum())
        sim = rng.multinomial(T, nb / nb.sum(), size=N_SIM)
        chis = ((sim - exp) ** 2 / exp).sum(1)
        p = (1 + np.sum(chis >= chi - 1e-9)) / (1 + N_SIM)
        tests.append({"test": f"structure_{name}", "description": f"Distribution of draw {name} vs exact enumeration of all tickets",
                      "observed_chisq": chi, "bins": len(nb), "p_value": float(p), "method": f"exact null categories, multinomial MC ({N_SIM})"})
        structure_summary[name] = {"observed_mean": float(o_vals.mean()), "null_mean": float(null_vals.mean()),
                                   "observed_sd": float(o_vals.std()), "null_sd": float(null_vals.std())}

    # bonus: uniform over the 32 numbers not drawn as mains
    bc = np.bincount(bonus - 1, minlength=N_BALLS)
    eb = (1 - X).sum(0) / (N_BALLS - K_DRAW)
    chi_b = float(((bc - eb) ** 2 / eb).sum())
    sims_b = np.zeros(N_SIM)
    avail = [np.flatnonzero(X[t] == 0) for t in range(T)]
    draws_b = np.stack([rng.choice(a, size=N_SIM) for a in avail], axis=1)
    for k in range(N_SIM):
        c = np.bincount(draws_b[k], minlength=N_BALLS)
        sims_b[k] = ((c - eb) ** 2 / eb).sum()
    tests.append({"test": "bonus_uniformity", "description": "Bonus counts vs uniform over the 32 non-main numbers",
                  "observed": chi_b, "p_value": float((1 + np.sum(sims_b >= chi_b)) / (1 + N_SIM)), "method": f"Monte Carlo ({N_SIM})"})

    # Holm across the global family and classification
    p = [t["p_value"] for t in tests]
    ph = holm(p)
    for t, a in zip(tests, ph):
        t["p_holm"] = float(a)
        t["classification"] = ("validated evidence" if a < 0.05 else
                               "suggestive but insufficient" if t["p_value"] < 0.05 else "consistent with randomness")

    # per-number and per-pair exact binomial tests with BH
    counts = X.sum(0)
    pn = K_DRAW / N_BALLS
    num_p = [stats.binomtest(int(c), T, pn).pvalue for c in counts]
    num_q = bh(num_p)
    per_number = [{"number": j + 1, "count": int(counts[j]), "expected": T * pn, "p": float(num_p[j]), "q_bh": float(num_q[j])}
                  for j in range(N_BALLS)]
    pair = X.T.astype(int) @ X.astype(int)
    pp = K_DRAW * (K_DRAW - 1) / (N_BALLS * (N_BALLS - 1))
    pair_rows = []
    for i in range(N_BALLS):
        for j in range(i + 1, N_BALLS):
            pair_rows.append((i + 1, j + 1, int(pair[i, j]), stats.binomtest(int(pair[i, j]), T, pp).pvalue))
    pq = bh([r[3] for r in pair_rows])
    top_pairs = sorted(zip(pair_rows, pq), key=lambda z: z[0][3])[:10]

    summary = {
        "draws_analyzed": T,
        "consecutive_pairs_used": int(valid.sum()),
        "global_tests": tests,
        "n_validated": sum(t["classification"] == "validated evidence" for t in tests),
        "n_suggestive": sum(t["classification"] == "suggestive but insufficient" for t in tests),
        "per_number": per_number,
        "per_number_min_q": float(min(num_q)),
        "per_number_raw_p_below_0.05": [r["number"] for r in per_number if r["p"] < 0.05],
        "pairs_expected_count": T * pp,
        "pairs_min_q": float(min(pq)),
        "pairs_raw_p_below_0.05": int(sum(r[3] < 0.05 for r in pair_rows)),
        "pairs_raw_p_below_0.05_expected_by_chance": 0.05 * len(pair_rows),
        "top_pairs_by_p": [{"pair": [r[0], r[1]], "count": r[2], "p": float(r[3]), "q_bh": float(q)} for r, q in top_pairs],
        "structure_summary": structure_summary,
        "overall_classification": None,
    }
    if summary["n_validated"]:
        summary["overall_classification"] = "validated evidence of departure from an independent uniform process"
    elif summary["n_suggestive"] or summary["per_number_min_q"] < 0.05 or summary["pairs_min_q"] < 0.05:
        summary["overall_classification"] = "suggestive but insufficient; no test survives multiple-testing correction"
    else:
        summary["overall_classification"] = "consistent with an independent uniform draw process"
    write_json(os.path.join(OUT, "03_randomness_tests.json"), summary)
    for t in tests:
        print(f"{t['test']:<28} p={t['p_value']:.4f} holm={t['p_holm']:.3f}  {t['classification']}")
    print("per-number min q:", round(summary["per_number_min_q"], 3), "raw p<.05:", summary["per_number_raw_p_below_0.05"])
    print("pairs min q:", round(summary["pairs_min_q"], 3), "raw p<.05:", summary["pairs_raw_p_below_0.05"], "expected", 0.05 * len(pair_rows))
    print(summary["overall_classification"])


if __name__ == "__main__":
    main()
