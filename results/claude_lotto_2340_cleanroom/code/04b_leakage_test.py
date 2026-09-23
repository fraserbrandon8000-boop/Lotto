"""Leakage check: scrambling every draw at or after target t must not change any ranking or ticket for t."""
import os

import numpy as np

import models as M
from common import MASTER_SEED, OUT, indicator_matrix, load_draws, write_json

CONSTRUCTORS = ["top6", "opt_top12", "pair_top12", "struct_top12", "diversity_top15"]


def run(X, valid, t):
    S, z = M.compute_scores(X[:t], valid[:t], bool(valid[t]), t)
    return {r: [M.build_ticket(c, S[r], z, t).tolist() for c in CONSTRUCTORS] + [M.ranking(S[r]).tolist()] for r in M.RANKERS}


def main():
    ids, _, mains, _ = load_draws()
    X = indicator_matrix(mains)
    valid = np.concatenate([[False], np.diff(ids) == 1])
    rng = np.random.default_rng(MASTER_SEED + 77)
    checked = []
    for t in (29, 60, 95, 130, 168):
        a = run(X, valid, t)
        Xs = X.copy()
        for s in range(t, len(X)):
            Xs[s] = 0
            Xs[s, rng.choice(38, 6, replace=False)] = 1
        b = run(Xs, valid, t)
        checked.append({"target_index": t, "draw_id": int(ids[t]), "identical": a == b})
    ok = all(c["identical"] for c in checked)
    write_json(os.path.join(OUT, "04b_leakage_test.json"), {"passed": ok, "checks": checked})
    print("leakage test passed:", ok, checked)


if __name__ == "__main__":
    main()
