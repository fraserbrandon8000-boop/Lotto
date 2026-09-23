"""Step 10: pre-draw state through #2339 and the #2340 candidate pool with code-computed evidence profiles.

Candidate generation rule (mechanical, fixed before any Jev interaction):
  1. the pre-registered dev-selected ticket method
  2. every non-control ranker with the protocol-default constructor opt_top12 (lambda_pair=0.5, lambda_struct=0.5)
  3. the consensus constructor
  4. two uniform random control tickets (H_random|top6 and random_ticket)
  Duplicate tickets are merged (all generating methods listed). Order is shuffled with a fixed seed and
  IDs C01.. are assigned after shuffling.
"""
import csv
import json
import os

import numpy as np

import models as M
from common import MASTER_SEED, N_BALLS, OUT, TARGET_DRAW, indicator_matrix, load_draws, pool_pmf, write_json

CORE_RANKERS = ["A_freq_all", "B_ew_20", "B_roll_10", "C_hazard", "D_trend_20v40", "E_transition",
                "E_pair_centrality", "G_ensemble_equal"]
LAMBDAS = [0.0, 0.25, 0.5, 1.0]
EXP6 = 36 / 38


def main():
    ids, dates, mains, bonus = load_draws()
    X = indicator_matrix(mains)
    valid = np.concatenate([[False], np.diff(ids) == 1])
    T = len(ids)
    assert ids[-1] == 2339 and TARGET_DRAW - ids[-1] == 1
    val = json.load(open(os.path.join(OUT, "06_validation_decision.json")))
    perf = json.load(open(os.path.join(OUT, "05_ticket_method_performance.json")))
    cov = json.load(open(os.path.join(OUT, "05_number_discovery_coverage.json")))
    rnd = json.load(open(os.path.join(OUT, "03_randomness_tests.json")))

    # adaptive-ensemble weights from all 140 walk-forward targets (causal for #2340)
    w = [max(0.0, cov[c]["12"]["mean"] - 12 * 6 / 38) for c in M.COMPONENTS]
    S, z = M.compute_scores(X, valid, True, T, adaptive_w=w)
    rk = {r: M.ranking(S[r]) for r in M.RANKERS}
    rank_of = {r: {int(b): i + 1 for i, b in enumerate(rk[r])} for r in M.RANKERS}
    pct = {r: M.pct_rank(S[r]) for r in M.RANKERS}

    # ---- generate candidates by the fixed rule
    specs = [val["dev_selected_ticket_method"]]
    specs += [f"{r}|opt_top12" for r in M.RANKERS if r != "H_random"]
    specs += ["consensus", "H_random|top6", "random_ticket"]
    tickets = {}
    for sp in specs:
        if sp == "consensus":
            tk = M.build_ticket("consensus", None, z, T, consensus_rankings=[rk[c] for c in M.COMPONENTS], ens_score=S["G_ensemble_equal"])
        elif sp == "random_ticket":
            tk = M.build_ticket("random_ticket", None, z, T)
        else:
            r, c = sp.split("|")
            tk = M.build_ticket(c, S[r], z, T)
        key = tuple(int(x) for x in tk)
        tickets.setdefault(key, []).append(sp)
    keys = list(tickets)
    order = np.random.default_rng(MASTER_SEED + 2340).permutation(len(keys))
    keys = [keys[i] for i in order]

    counts_all = X.sum(0)
    exp_all = T * 6 / 38
    sd_all = np.sqrt(T * (6 / 38) * (32 / 38))
    last20 = X[-20:].sum(0)
    hp = pool_pmf(6)
    pairs_idx = [(a, b) for i, a in enumerate(range(6)) for b in range(i + 1, 6)]

    cands = {}
    for n, key in enumerate(keys, start=1):
        cid = f"C{n:02d}"
        t6 = np.array(key)
        methods = tickets[key]
        is_control = all(m.startswith("H_random") or m == "random_ticket" for m in methods)
        # out-of-sample performance of each generating method (the ticket method, walk-forward)
        oos = {}
        for m in methods:
            p = perf.get(m)
            if p:
                oos[m] = {"walk_forward_targets": p["n_targets"], "mean_matches": round(p["mean"], 3),
                          "random_expectation": round(p["exact_random_expectation"], 3),
                          "dev_mean": round(p["dev_mean"], 3), "confirmation_mean": round(p["conf_mean"], 3),
                          "exact_p_one_sided_full": round(p["p_upper_exact"], 3),
                          "holm_p_family": round(p.get("p_upper_holm_family", 1.0), 3) if not is_control else None,
                          "pct_3plus": round(p["pct_3plus"], 1), "baseline_pct_3plus": round(p["baseline_pct_3plus"], 1),
                          "ci95_mean": [round(x, 3) for x in p["ci95_bootstrap"]]}
        # per-number evidence
        per_num = []
        for b in key:
            j = b - 1
            per_num.append({
                "number": b,
                "ranks_among_38": {r: rank_of[r][b] for r in CORE_RANKERS},
                "full_history_count": int(counts_all[j]), "full_history_z": round(float((counts_all[j] - exp_all) / sd_all), 2),
                "last20_count": int(last20[j]), "last20_expected": round(20 * 6 / 38, 2),
                "components_ranking_it_top12": int(sum(rank_of[c][b] <= 12 for c in M.COMPONENTS)),
            })
        mean_pct = {r: round(float(np.mean([pct[r][b - 1] for b in key])), 3) for r in CORE_RANKERS}
        pz = [float(z[t6[a] - 1, t6[bb] - 1]) for a, bb in pairs_idx]
        s = int(t6.sum())
        # sensitivity at the #2340 state: lambda grid and sibling rankers reproducing >= 4 of the 6 numbers
        lam_hits, lam_total = 0, 0
        fam_hits, fam_total = 0, 0
        for m in methods:
            if "|" in m and m.split("|")[1] == "opt_top12":
                r = m.split("|")[0]
                T6, _, (sp_, pp_, st_) = M.eval_subsets(rk[r][:12], S[r], z, 0, 0)
                for a in LAMBDAS:
                    for bb in LAMBDAS:
                        tk = T6[np.argmax(sp_ + a * pp_ + bb * st_)]
                        lam_total += 1
                        lam_hits += len(set(tk.tolist()) & set(key)) >= 4
                letter = r.split("_")[0]
                for r2 in M.RANKERS:
                    if r2 != r and r2.split("_")[0] == letter:
                        tk = M.build_ticket("opt_top12", S[r2], z, T)
                        fam_total += 1
                        fam_hits += len(set(tk.tolist()) & set(key)) >= 4
        consensus_idx = float(np.mean([pn["components_ranking_it_top12"] for pn in per_num]) / len(M.COMPONENTS))
        best_conf = max((o["confirmation_mean"] for o in oos.values()), default=None)
        counter = ["All 20 global randomness tests are consistent with an independent uniform draw (min Holm p = 1.0).",
                   "No ticket method survives Holm correction; the pre-registered dev-selected method fell below baseline in confirmation.",
                   "Every ticket, including this one, has exactly the same random probabilities: P(3+) = 3.87%, expected matches 0.947."]
        if is_control:
            counter.insert(0, "This ticket is a uniform random control, not derived from any feature.")
        if best_conf is not None and best_conf <= EXP6:
            counter.append("Its generating method(s) did not beat the random expectation in the confirmation period.")
        if best_conf is not None and oos and all(o["dev_mean"] > EXP6 and o["confirmation_mean"] < o["dev_mean"] for o in oos.values()):
            counter.append("Development-period performance of its method(s) fell in the confirmation period (regression toward random).")
        cands[cid] = {
            "numbers": list(key),
            "generating_methods": methods,
            "is_random_control": is_control,
            "out_of_sample_performance_of_generating_methods": oos,
            "per_number_evidence": per_num,
            "mean_percentile_under_core_rankers": mean_pct,
            "long_term_evidence": {"mean_full_history_z": round(float(np.mean([p["full_history_z"] for p in per_num])), 2)},
            "recent_frequency_evidence": {"last20_total": int(sum(p["last20_count"] for p in per_num)),
                                          "last20_total_expected": round(6 * 20 * 6 / 38, 2),
                                          "mean_ew20_percentile": mean_pct["B_ew_20"]},
            "trend_evidence": {"mean_trend_percentile": mean_pct["D_trend_20v40"]},
            "gap_evidence": {"mean_hazard_percentile": mean_pct["C_hazard"],
                             "note": "C_hazard (pooled re-appearance hazard) had top-12 walk-forward coverage 1.893 vs 1.895 random"},
            "pair_evidence": {"mean_pair_z": round(float(np.mean(pz)), 3), "pairs_with_z_above_2": int(sum(x > 2 for x in pz)),
                              "note": "no pair co-occurrence survives BH correction (min q = %.2f)" % rnd["pairs_min_q"]},
            "structure_evidence": {"sum": s, "odd": int((t6 % 2).sum()), "low_1_19": int((t6 <= 19).sum()),
                                   "consecutive_pairs": int((np.diff(t6) == 1).sum()), "range": int(t6[-1] - t6[0]),
                                   "structure_class_null_probability": round(float(M.structure_tables()["prob"][M.struct_key(t6)]), 4),
                                   "structure_typicality_z": round(float(M.struct_z(t6)), 2)},
            "ensemble_evidence": {"mean_ensemble_percentile": mean_pct["G_ensemble_equal"],
                                  "consensus_index_0_to_1": round(consensus_idx, 3)},
            "sensitivity": {"lambda_grid_variants_keeping_4plus_numbers": f"{lam_hits}/{lam_total}" if lam_total else "n/a",
                            "sibling_rankers_keeping_4plus_numbers": f"{fam_hits}/{fam_total}" if fam_total else "n/a"},
            "uncertainty": {"expected_matches_under_exact_random": round(EXP6, 3), "P_3plus_random": 0.0387,
                            "note": "Walk-forward CIs of every method include the random expectation."},
            "counterevidence": counter,
        }

    rankings = {r: [int(b) for b in rk[r]] for r in M.RANKERS}
    out = {"target_draw": TARGET_DRAW, "information_cutoff": int(ids[-1]), "draws_used": int(T),
           "adaptive_weights": dict(zip(M.COMPONENTS, w)), "generation_rule": __doc__.split("Candidate generation rule")[1].strip(),
           "n_candidates": len(cands), "candidates": cands}
    write_json(os.path.join(OUT, "07_candidates_2340.json"), out)
    write_json(os.path.join(OUT, "07_rankings_2340.json"), {"target_draw": TARGET_DRAW, "information_cutoff": int(ids[-1]),
                                                             "rankings_best_first": rankings,
                                                             "scores": {r: [float(x) for x in S[r]] for r in M.RANKERS}})
    for cid, c in cands.items():
        print(cid, c["numbers"], c["generating_methods"], "ctrl" if c["is_random_control"] else "",
              "sum", c["structure_evidence"]["sum"], "cons", c["ensemble_evidence"]["consensus_index_0_to_1"],
              c["sensitivity"])
    print(len(cands), "candidates")


if __name__ == "__main__":
    main()
