"""Steps 5-9: strict causal walk-forward of every ranker and ticket constructor, with the
pre-registered dev-select / confirmation-test procedure."""
import csv
import json
import math
import os

import numpy as np

import models as M
from common import (MASTER_SEED, N_BALLS, OUT, bh, convolve_n, holm, indicator_matrix, load_draws,
                    pool_pmf, write_json)

BURN_IN = 29
POOLS = (6, 8, 10, 12, 15, 20)
CONSTRUCTORS = ["top6", "opt_top8", "opt_top10", "opt_top12", "opt_top15", "pair_top12", "struct_top12", "diversity_top15"]
LAMBDAS = [0.0, 0.25, 0.5, 1.0]
EXP6 = 36 / 38


def main():
    ids, dates, mains, bonus = load_draws()
    X = indicator_matrix(mains)
    valid = np.concatenate([[False], np.diff(ids) == 1])
    T = len(ids)
    targets = list(range(BURN_IN, T))
    n_dev = len(targets) // 2
    base_methods = [f"{r}|{c}" for r in M.RANKERS if r != "H_random" for c in CONSTRUCTORS] + ["consensus", "M_follow_leader"]
    control_methods = [f"H_random|{c}" for c in CONSTRUCTORS] + ["random_ticket"]
    lam_methods = [f"{r}|opt_top{m}|lp={a}|ls={b}" for r in M.RANKERS for m in (8, 10, 12, 15) for a in LAMBDAS for b in LAMBDAS]
    matches = {m: [] for m in base_methods + control_methods + lam_methods}
    coverage = {r: {k: [] for k in POOLS} for r in M.RANKERS}
    ticket_log = []
    comp_hist = {c: [] for c in M.COMPONENTS}

    for t in targets:
        H, vh = X[:t], valid[:t]
        # causal adaptive-ensemble weights from earlier targets only
        if len(comp_hist[M.COMPONENTS[0]]) >= 10:
            w = [max(0.0, np.mean(comp_hist[c]) - 12 * 6 / 38) for c in M.COMPONENTS]
        else:
            w = None
        S, z = M.compute_scores(H, vh, bool(valid[t]), t, adaptive_w=w)
        actual = set(mains[t])
        rk = {r: M.ranking(S[r]) for r in M.RANKERS}
        for r in M.RANKERS:
            for k in POOLS:
                coverage[r][k].append(len(actual & set(rk[r][:k])))
        for c in M.COMPONENTS:
            comp_hist[c].append(len(actual & set(rk[c][:12])))
        row = {"target_index": t, "draw_id": int(ids[t]), "actual": sorted(int(a) for a in actual), "tickets": {}}
        for r in M.RANKERS:
            for c in CONSTRUCTORS:
                tk = M.build_ticket(c, S[r], z, t)
                key = f"{r}|{c}"
                matches[key].append(len(actual & set(tk.tolist())))
                row["tickets"][key] = tk.tolist()
            for m in (8, 10, 12, 15):
                T6, _, (sp, pp, stp) = M.eval_subsets(rk[r][:m], S[r], z, 0, 0)
                for a in LAMBDAS:
                    for b in LAMBDAS:
                        tk = T6[np.argmax(sp + a * pp + b * stp)]
                        matches[f"{r}|opt_top{m}|lp={a}|ls={b}"].append(len(actual & set(tk.tolist())))
        tk = M.build_ticket("consensus", None, z, t, consensus_rankings=[rk[c] for c in M.COMPONENTS], ens_score=S["G_ensemble_equal"])
        matches["consensus"].append(len(actual & set(tk.tolist())))
        row["tickets"]["consensus"] = tk.tolist()
        tk = M.build_ticket("random_ticket", None, z, t)
        matches["random_ticket"].append(len(actual & set(tk.tolist())))
        row["tickets"]["random_ticket"] = tk.tolist()
        # follow-the-leader: the base method with the best trailing mean over earlier targets
        pool = [m for m in base_methods if m not in ("M_follow_leader",)]
        if len(matches[pool[0]]) - 1 >= 10:
            prev = {m: np.mean(matches[m][:-1]) for m in pool}
            lead = max(pool, key=lambda m: (prev[m], -pool.index(m)))
        else:
            lead = "G_ensemble_equal|opt_top12"
        tk = row["tickets"][lead]
        matches["M_follow_leader"].append(len(actual & set(tk)))
        row["tickets"]["M_follow_leader"] = tk
        row["follow_leader_choice"] = lead
        ticket_log.append(row)

    with open(os.path.join(OUT, "04_walkforward_tickets.jsonl"), "w") as f:
        for r in ticket_log:
            f.write(json.dumps(r) + "\n")
    with open(os.path.join(OUT, "04_walkforward_matches.csv"), "w", newline="") as f:
        w = csv.writer(f)
        keys = list(matches)
        w.writerow(["draw_id"] + keys)
        for i, t in enumerate(targets):
            w.writerow([int(ids[t])] + [matches[k][i] for k in keys])

    # ------------------------------------------------------------------ statistics
    dist_cache = {}

    def exact_p(vals, pool):
        n = len(vals)
        if (pool, n) not in dist_cache:
            dist_cache[(pool, n)] = convolve_n(pool_pmf(pool), n)
        d = dist_cache[(pool, n)]
        tot = int(np.sum(vals))
        up, lo = float(d[tot:].sum()), float(d[: tot + 1].sum())
        return up, min(1.0, 2 * min(up, lo))

    boot_rng = np.random.default_rng(MASTER_SEED + 9)
    BOOT = boot_rng.integers(0, len(targets), size=(5000, len(targets)))

    def summarize(vals, pool=6):
        v = np.asarray(vals)
        pmf = pool_pmf(pool)
        exp = float(sum(k * p for k, p in enumerate(pmf)))
        sd0 = math.sqrt(sum((k - exp) ** 2 * p for k, p in enumerate(pmf)))
        up, two = exact_p(v, pool)
        dv, cv = v[:n_dev], v[n_dev:]
        bm = v[BOOT[:, : len(v)] % len(v)].mean(1)
        out = {
            "n_targets": int(len(v)), "total": int(v.sum()), "mean": float(v.mean()), "median": float(np.median(v)),
            "sd": float(v.std(ddof=1)), "exact_random_expectation": exp,
            "ci95_bootstrap": [float(np.quantile(bm, 0.025)), float(np.quantile(bm, 0.975))],
            "ci95_normal": [float(v.mean() - 1.96 * v.std(ddof=1) / math.sqrt(len(v))), float(v.mean() + 1.96 * v.std(ddof=1) / math.sqrt(len(v)))],
            "p_upper_exact": up, "p_two_sided_exact": two,
            "dev_mean": float(dv.mean()), "dev_p_upper": exact_p(dv, pool)[0],
            "conf_mean": float(cv.mean()), "conf_p_upper": exact_p(cv, pool)[0],
            "z_vs_random": float((v.mean() - exp) / (sd0 / math.sqrt(len(v)))),
        }
        for j in range(0, 7):
            out[f"pct_{j}"] = float(np.mean(v == j) * 100)
        for j in (3, 4, 5):
            out[f"pct_{j}plus"] = float(np.mean(v >= j) * 100)
            out[f"baseline_pct_{j}plus"] = float(pmf[j:].sum() * 100) if j < len(pmf) else 0.0
        out["count_6"] = int(np.sum(v == 6))
        return out

    ticket_stats = {m: summarize(matches[m]) for m in base_methods + control_methods}
    fam = base_methods + control_methods
    ph = holm([ticket_stats[m]["p_upper_exact"] for m in base_methods])
    pb = bh([ticket_stats[m]["p_upper_exact"] for m in base_methods])
    for m, a, b in zip(base_methods, ph, pb):
        ticket_stats[m]["p_upper_holm_family"] = float(a)
        ticket_stats[m]["q_bh_family"] = float(b)
    lam_stats = {m: {"dev_mean": float(np.mean(matches[m][:n_dev])), "conf_mean": float(np.mean(matches[m][n_dev:])),
                     "mean": float(np.mean(matches[m]))} for m in lam_methods}

    cov_stats = {r: {str(k): summarize(coverage[r][k], k) for k in POOLS} for r in M.RANKERS}

    # ------------------------------------------------------------------ pre-registered validation
    dev_best = max(base_methods, key=lambda m: (ticket_stats[m]["dev_mean"], -base_methods.index(m)))
    s = ticket_stats[dev_best]
    if "|" in dev_best:
        r, c = dev_best.split("|")
        fam_letter = r.split("_")[0]
        variants = [f"{r2}|{c}" for r2 in M.RANKERS if r2.split("_")[0] == fam_letter and r2 != "H_random"]
        if c.startswith("opt_top"):
            variants += [f"{r}|{c}|lp={a}|ls={b}" for a in LAMBDAS for b in LAMBDAS]
    else:
        variants = [dev_best]
    var_conf = {v: (ticket_stats[v]["conf_mean"] if v in ticket_stats else lam_stats[v]["conf_mean"]) for v in variants}
    frac_above = float(np.mean([x > EXP6 for x in var_conf.values()]))
    step2 = s["conf_p_upper"] < 0.05
    step3 = frac_above >= 2 / 3
    validated = bool(step2 and step3)
    suggestive = (not validated) and (s["conf_p_upper"] < 0.10 or any(ticket_stats[m]["p_upper_exact"] < 0.05 for m in base_methods))

    dev_best_r = max([r for r in M.RANKERS if r != "H_random"], key=lambda r: (cov_stats[r]["12"]["dev_mean"], -M.RANKERS.index(r)))
    cr = cov_stats[dev_best_r]["12"]

    # power: minimum detectable mean shift (one-sided 5%, 80% power) with 70 confirmation targets
    sd0 = math.sqrt(sum((k - EXP6) ** 2 * p for k, p in enumerate(pool_pmf(6))))
    mde = (1.645 + 0.842) * sd0 / math.sqrt(len(targets) - n_dev)

    validation = {
        "targets": len(targets), "first_target": int(ids[targets[0]]), "last_target": int(ids[targets[-1]]),
        "dev_targets": [int(ids[targets[0]]), int(ids[targets[n_dev - 1]])],
        "conf_targets": [int(ids[targets[n_dev]]), int(ids[targets[-1]])],
        "n_base_methods": len(base_methods),
        "dev_selected_ticket_method": dev_best,
        "dev_selected_dev_mean": s["dev_mean"], "dev_selected_dev_p": s["dev_p_upper"],
        "dev_selected_conf_mean": s["conf_mean"], "dev_selected_conf_p_upper": s["conf_p_upper"],
        "step2_conf_p_below_0.05": bool(step2),
        "sensitivity_variants_conf_mean": var_conf,
        "sensitivity_fraction_above_baseline": frac_above,
        "step3_two_thirds_variants_above_baseline": bool(step3),
        "VALIDATED_EDGE": validated,
        "suggestive": bool(suggestive),
        "methods_raw_p_below_0.05_full_period": [m for m in base_methods if ticket_stats[m]["p_upper_exact"] < 0.05],
        "methods_surviving_holm": [m for m in base_methods if ticket_stats[m]["p_upper_holm_family"] < 0.05],
        "min_holm_p": float(min(ph)),
        "number_discovery": {"dev_selected_ranker_top12": dev_best_r, "dev_mean": cr["dev_mean"], "conf_mean": cr["conf_mean"],
                             "conf_p_upper": cr["conf_p_upper"], "baseline": 12 * 6 / 38,
                             "validated": bool(cr["conf_p_upper"] < 0.05)},
        "power": {"confirmation_targets": len(targets) - n_dev, "sd_per_ticket_under_null": sd0,
                  "min_detectable_mean_improvement_80pct_power": mde,
                  "as_percent_of_baseline": mde / EXP6 * 100},
        "random_controls": {m: {"mean": ticket_stats[m]["mean"], "p_two_sided": ticket_stats[m]["p_two_sided_exact"]} for m in control_methods},
    }
    write_json(os.path.join(OUT, "05_ticket_method_performance.json"), ticket_stats)
    write_json(os.path.join(OUT, "05_number_discovery_coverage.json"), cov_stats)
    write_json(os.path.join(OUT, "05_sensitivity_lambda_grid.json"), lam_stats)
    write_json(os.path.join(OUT, "06_validation_decision.json"), validation)

    print(json.dumps(validation, indent=1)[:4000])
    top = sorted(base_methods, key=lambda m: -ticket_stats[m]["mean"])[:12]
    print("\nTop full-period ticket methods:")
    for m in top:
        t = ticket_stats[m]
        print(f"{m:<34} mean={t['mean']:.3f} dev={t['dev_mean']:.3f} conf={t['conf_mean']:.3f} p={t['p_upper_exact']:.3f} holm={t['p_upper_holm_family']:.2f} 3+={t['pct_3plus']:.1f}%")
    print("\nRanker coverage (mean captured) k=6..20; baseline", [round(6 * k / 38, 3) for k in POOLS])
    for r in M.RANKERS:
        print(f"{r:<22}", " ".join(f"{cov_stats[r][str(k)]['mean']:.3f}" for k in POOLS),
              " top12 dev/conf", round(cov_stats[r]['12']['dev_mean'], 3), round(cov_stats[r]['12']['conf_mean'], 3),
              "p12", round(cov_stats[r]['12']['p_upper_exact'], 3))


if __name__ == "__main__":
    main()
