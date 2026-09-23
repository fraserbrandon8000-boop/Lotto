"""Shared constants, paths and exact distributions for the #2340 clean-room experiment."""
import csv
import hashlib
import json
import math
import os
from itertools import combinations

import numpy as np

N_BALLS = 38
K_DRAW = 6
TARGET_DRAW = 2340
TARGET_DATE = "2026-09-23"
CUTOFF_DRAW = 2339
MASTER_SEED = 23402026

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "outputs")
CONFIG = os.path.join(ROOT, "config")
JEV = os.path.join(ROOT, "jev")
LEDGER = os.path.join(ROOT, "ledger")
WORKBOOK = os.path.join(REPO, "data", "original", "Lotto-Draw-Dataset.xlsx")
NORMALIZED = os.path.join(DATA, "04_normalized_analysis_dataset.csv")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2, sort_keys=False, default=_json_default)
        f.write("\n")


def _json_default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(type(o))


def load_draws():
    """Return (ids, dates, mains[T,6], bonus[T]) in chronological order."""
    ids, dates, mains, bonus = [], [], [], []
    with open(NORMALIZED) as f:
        for r in csv.DictReader(f):
            ids.append(int(r["draw_id"]))
            dates.append(r["draw_date"])
            mains.append([int(r[f"n{i}"]) for i in range(1, 7)])
            bonus.append(int(r["bonus"]))
    return np.array(ids), dates, np.array(mains), np.array(bonus)


def indicator_matrix(mains):
    """T x 38 0/1 matrix; column j is ball j+1."""
    X = np.zeros((len(mains), N_BALLS), dtype=np.int8)
    for t, row in enumerate(mains):
        X[t, np.asarray(row) - 1] = 1
    return X


def hypergeom_pmf(N, K, n):
    """P(X=k) for k=0..min(K,n): X = winners among n chosen balls, K winners of N."""
    tot = math.comb(N, n)
    return np.array([math.comb(K, k) * math.comb(N - K, n - k) / tot for k in range(0, min(K, n) + 1)])


def pool_pmf(pool_size):
    return hypergeom_pmf(N_BALLS, K_DRAW, pool_size)


def convolve_n(pmf, n):
    """Exact distribution of the sum of n iid variables with the given pmf."""
    out = np.array([1.0])
    for _ in range(n):
        out = np.convolve(out, pmf)
    return out


def exact_upper_p(pmf, n, observed_total):
    """P(sum of n iid >= observed_total) under the exact null."""
    dist = convolve_n(pmf, n)
    obs = int(round(observed_total))
    return float(dist[obs:].sum()) if obs < len(dist) else 0.0


def exact_lower_p(pmf, n, observed_total):
    dist = convolve_n(pmf, n)
    obs = int(round(observed_total))
    return float(dist[: obs + 1].sum())


_ALL = None


def all_tickets():
    """All C(38,6) tickets as an int8 array (cached)."""
    global _ALL
    if _ALL is None:
        _ALL = np.array(list(combinations(range(1, N_BALLS + 1), K_DRAW)), dtype=np.int8)
    return _ALL


def holm(pvals):
    p = np.asarray(pvals, dtype=float)
    order = np.argsort(p)
    m = len(p)
    adj = np.empty(m)
    running = 0.0
    for rank, idx in enumerate(order):
        running = max(running, (m - rank) * p[idx])
        adj[idx] = min(1.0, running)
    return adj


def bh(pvals):
    p = np.asarray(pvals, dtype=float)
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m)
    prev = 1.0
    for rank in range(m - 1, -1, -1):
        idx = order[rank]
        prev = min(prev, p[idx] * m / (rank + 1))
        adj[idx] = prev
    return adj
