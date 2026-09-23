"""Claude-only final ticket selection for Jamaica Lotto #2340.

Reads ONLY frozen clean-room outputs from commit 91eae5d and scores every
candidate in the frozen pool with the pre-registered rubric in
config/selection_rubric.json. Nothing is re-estimated: no dataset rebuild,
no walk-forward, no ranker, no candidate generation, no random baseline.

No TypeSafe / Jev file is opened and no network call is made.

Usage:
    python3 select_claude_only.py                      # the one real run
    python3 select_claude_only.py --root FIX --out TMP  # synthetic-fixture dry run
"""

import argparse
import csv
import hashlib
import json
import math
import os
import re
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
EXP_DIR = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(EXP_DIR))
CLEANROOM = os.path.join("results", "claude_lotto_2340_cleanroom")
RUBRIC_PATH = os.path.join(EXP_DIR, "config", "selection_rubric.json")

INPUTS = {
    "protocol": "config/protocol.json",
    "candidates": "outputs/07_candidates_2340.json",
    "method_perf": "outputs/05_ticket_method_performance.json",
    "lambda_grid": "outputs/05_sensitivity_lambda_grid.json",
    "coverage": "outputs/05_number_discovery_coverage.json",
    "validation": "outputs/06_validation_decision.json",
    "rankings": "outputs/07_rankings_2340.json",
    "baseline": "outputs/02_exact_baseline.json",
    "randomness": "outputs/03_randomness_tests.json",
    "leakage": "outputs/04b_leakage_test.json",
}

FAMILY_REPS = ["A_freq_all", "B_ew_20", "C_hazard", "D_trend_20v40", "E_transition"]
CORE8 = ["A_freq_all", "B_ew_20", "B_roll_10", "C_hazard", "D_trend_20v40",
         "E_transition", "E_pair_centrality", "G_ensemble_equal"]
CONSENSUS_COMPONENTS = FAMILY_REPS
N_DEV = 70
N_CONF = 70
E0 = 36 / 38
SD0 = math.sqrt(6 * (6 / 38) * (32 / 38) * (32 / 37))
CRITERIA = ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8"]
WEIGHTS = {"R1": 8, "R2": 7, "R3": 6, "R4": 5, "R5": 4, "R6": 3, "R7": 2, "R8": 1}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def pct(rank):
    return (38 - rank) / 37


def avg_rank_u(values):
    """Ascending average rank -> u in [0,1]; best (largest) value gets 1."""
    n = len(values)
    keyed = sorted(range(n), key=lambda i: round(values[i], 12))
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and round(values[keyed[j + 1]], 12) == round(values[keyed[i]], 12):
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[keyed[k]] = r
        i = j + 1
    return [(r - 1) / (n - 1) for r in ranks]


def parse_fraction(s):
    if s is None:
        return None
    if isinstance(s, (int, float)):
        return float(s) if 0 <= s <= 1 else None
    t = str(s).strip()
    if t.lower().startswith("n/a") or t.lower().startswith("not applicable"):
        return None
    nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", t)]
    if len(nums) >= 2:
        a, b = nums[0], nums[1]
        return a / b if b > 0 and 0 <= a <= b else None
    if len(nums) == 1:
        if "%" in t:
            return nums[0] / 100
        return nums[0] if 0 <= nums[0] <= 1 else None
    return None


def method_ranker(method):
    return method.split("|")[0] if "|" in method else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.join(REPO, CLEANROOM))
    ap.add_argument("--out", default=os.path.join(EXP_DIR, "outputs"))
    args = ap.parse_args()
    real_run = os.path.abspath(args.root) == os.path.abspath(os.path.join(REPO, CLEANROOM))

    final_path = os.path.join(args.out, "final_prediction.json")
    if os.path.exists(final_path):
        sys.exit("REFUSING TO RUN: a final selection already exists (one-decision rule).")

    run_started = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rubric = json.load(open(RUBRIC_PATH))
    for c in rubric["criteria_in_priority_order"]:
        assert WEIGHTS[c["id"]] == c["weight"], "weights in code differ from frozen rubric"

    paths = {k: os.path.join(args.root, v) for k, v in INPUTS.items()}
    data = {k: json.load(open(p)) for k, p in paths.items()}
    input_hashes = {os.path.join(CLEANROOM, INPUTS[k]): sha256_file(p) for k, p in paths.items()}

    cands = data["candidates"]["candidates"]
    perf = data["method_perf"]
    grid = data["lambda_grid"]
    val = data["validation"]
    rankings = data["rankings"]["rankings_best_first"]
    ids = sorted(cands)
    checks = []

    # ---------------- validity checks (never change the pool) ----------------
    def check(name, ok, detail=""):
        checks.append({"check": name, "passed": bool(ok), "detail": detail})

    for cid in ids:
        nums = cands[cid]["numbers"]
        check(f"{cid} six distinct numbers in 1..38",
              len(nums) == 6 and len(set(nums)) == 6 and all(1 <= x <= 38 for x in nums))
    sd_frozen = (val.get("power") or {}).get("sd_per_ticket_under_null")
    if sd_frozen is not None:
        check("sd0 matches frozen power.sd_per_ticket_under_null",
              abs(sd_frozen - SD0) < 1e-6, f"code={SD0:.9f} frozen={sd_frozen}")

    rank_mismatch = 0
    for cid in ids:
        for pe in cands[cid]["per_number_evidence"]:
            for r, rk in pe["ranks_among_38"].items():
                if r in rankings and rankings[r].index(pe["number"]) + 1 != rk:
                    rank_mismatch += 1
    check("per-number ranks match 07_rankings_2340.json positions", rank_mismatch == 0,
          f"{rank_mismatch} mismatches")

    # --------------------------- raw criteria --------------------------------
    raw = {c: {} for c in CRITERIA}
    detail = {}

    def grid_fraction(ranker):
        keys = [k for k in grid if k.startswith(ranker + "|")]
        if not keys:
            return None, 0
        return sum(1 for k in keys if grid[k]["conf_mean"] > E0) / len(keys), len(keys)

    for cid in ids:
        c = cands[cid]
        pne = c["per_number_evidence"]
        d = {"numbers": c["numbers"], "generating_methods": c["generating_methods"],
             "is_random_control": c["is_random_control"]}

        # R1 multi-family support
        fam_counts = []
        for pe in pne:
            k = sum(1 for r in FAMILY_REPS if pe["ranks_among_38"][r] <= 12)
            fam_counts.append(k)
            if "components_ranking_it_top12" in pe:
                check(f"{cid} n{pe['number']} family top-12 count == components_ranking_it_top12",
                      k == pe["components_ranking_it_top12"],
                      f"recomputed={k} frozen={pe['components_ranking_it_top12']}")
        raw["R1"][cid] = sum(fam_counts) / (6 * 5)
        d["family_top12_counts"] = dict(zip([pe["number"] for pe in pne], fam_counts))

        # method-level dev / confirmation means
        oos = c.get("out_of_sample_performance_of_generating_methods", {})
        mstats = {}
        for m in c["generating_methods"]:
            if m in oos:
                dev, conf = oos[m]["dev_mean"], oos[m]["confirmation_mean"]
                src = "candidate"
            else:
                dev, conf = perf[m]["dev_mean"], perf[m]["conf_mean"]
                src = "05_ticket_method_performance (fallback)"
            if m in perf:
                check(f"{cid} {m} dev/conf means match 05_ticket_method_performance",
                      abs(perf[m]["dev_mean"] - dev) < 1e-9 and abs(perf[m]["conf_mean"] - conf) < 1e-9)
            mstats[m] = {"dev_mean": dev, "confirmation_mean": conf, "source": src,
                         "z_conf": (conf - E0) / (SD0 / math.sqrt(N_CONF)),
                         "z_decay": max(0.0, dev - conf) / (SD0 * math.sqrt(1 / N_DEV + 1 / N_CONF))}
            if m in perf:
                for k in ("mean", "p_upper_exact", "p_upper_holm_family", "dev_p_upper", "conf_p_upper"):
                    if k in perf[m]:
                        mstats[m][k] = perf[m][k]
        d["method_stats"] = mstats

        # R2 confirmation-period evidence
        raw["R2"][cid] = sum(v["z_conf"] for v in mstats.values()) / len(mstats)

        # R3 ranking consistency (worst-case core ranker)
        P = {r: sum(pct(pe["ranks_among_38"][r]) for pe in pne) / 6 for r in CORE8}
        raw["R3"][cid] = min(P.values())
        d["core_ranker_ticket_percentile"] = P

        # R4 ticket sensitivity / stability
        sens = c.get("sensitivity", {})
        fr = {k: parse_fraction(v) for k, v in sens.items()}
        good = [v for v in fr.values() if v is not None]
        raw["R4"][cid] = sum(good) / len(good) if good else 0.0
        d["sensitivity_raw"] = sens
        d["sensitivity_parsed"] = fr

        # R5 dependence on a single model
        V = {r: sum(1 for pe in pne if pe["ranks_among_38"][r] <= 12) for r in CORE8}
        tot = sum(V.values())
        max_share = max(V.values()) / tot if tot else 1.0
        raw["R5"][cid] = 1 - max_share
        d["core_ranker_top12_votes"] = V

        # R6 overfitting (dev -> confirmation decay)
        raw["R6"][cid] = -sum(v["z_decay"] for v in mstats.values()) / len(mstats)

        # R7 inputs
        d["ensemble_equal_ticket_percentile"] = P["G_ensemble_equal"]
        d["n_counterevidence"] = len(c.get("counterevidence", []))
        d["counterevidence"] = c.get("counterevidence", [])

        # R8 method robustness over the lambda grid
        fs = {}
        for m in c["generating_methods"]:
            if m == "consensus":
                vals = [grid_fraction(r)[0] for r in CONSENSUS_COMPONENTS]
                vals = [v for v in vals if v is not None]
                fs[m] = sum(vals) / len(vals) if vals else None
            elif m == "random_ticket":
                fs[m] = grid_fraction("H_random")[0]
            else:
                fs[m] = grid_fraction(method_ranker(m))[0] if method_ranker(m) else None
        good = [v for v in fs.values() if v is not None]
        raw["R8"][cid] = sum(good) / len(good) if good else 0.0
        d["lambda_grid_fraction_conf_above_E0"] = fs

        detail[cid] = d

    # R7 = average of two within-pool normalized ranks
    ua = avg_rank_u([detail[c]["ensemble_equal_ticket_percentile"] for c in ids])
    ub = avg_rank_u([-detail[c]["n_counterevidence"] for c in ids])
    for i, cid in enumerate(ids):
        raw["R7"][cid] = (ua[i] + ub[i]) / 2

    # ------------------------ normalize and combine ---------------------------
    u = {}
    for crit in CRITERIA:
        vals = avg_rank_u([raw[crit][c] for c in ids])
        u[crit] = dict(zip(ids, vals))
    wsum = sum(WEIGHTS.values())
    S = {c: sum(WEIGHTS[k] * u[k][c] for k in CRITERIA) / wsum for c in ids}

    def sort_key(c):
        return tuple([-round(S[c], 12)] + [-round(raw[k][c], 12) for k in CRITERIA] + [c])

    order_all = sorted(ids, key=sort_key)
    eligible = [c for c in order_all if not cands[c]["is_random_control"]]
    selected = eligible[0]
    run_finished = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # -------------------------------- outputs ---------------------------------
    os.makedirs(args.out, exist_ok=True)
    evaluation = {
        "rubric_id": rubric["rubric_id"],
        "rubric_sha256": sha256_file(RUBRIC_PATH),
        "scorer_sha256": sha256_file(os.path.abspath(__file__)),
        "real_run": real_run,
        "run_started_utc": run_started,
        "run_finished_utc": run_finished,
        "input_sha256": input_hashes,
        "constants": {"E0": E0, "sd0": SD0, "n_dev": N_DEV, "n_conf": N_CONF, "weights": WEIGHTS},
        "validity_checks": {"n": len(checks), "n_failed": sum(not c["passed"] for c in checks),
                            "failed": [c for c in checks if not c["passed"]],
                            "all": checks},
        "composite_order_all_candidates": order_all,
        "candidates": {
            c: {"composite_S": S[c],
                "overall_position": order_all.index(c) + 1,
                "eligible": not cands[c]["is_random_control"],
                "raw": {k: raw[k][c] for k in CRITERIA},
                "u": {k: u[k][c] for k in CRITERIA},
                **detail[c]} for c in ids},
        "selected_candidate": selected,
    }
    with open(os.path.join(args.out, "candidate_evaluation.json"), "w") as f:
        json.dump(evaluation, f, indent=1)
    with open(os.path.join(args.out, "candidate_evaluation.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["position", "candidate", "eligible", "numbers", "generating_methods", "S"]
                   + [f"{k}_raw" for k in CRITERIA] + [f"{k}_u" for k in CRITERIA])
        for c in order_all:
            w.writerow([order_all.index(c) + 1, c, not cands[c]["is_random_control"],
                        " ".join(f"{x:02d}" for x in sorted(cands[c]["numbers"])),
                        ";".join(cands[c]["generating_methods"]), f"{S[c]:.6f}"]
                       + [f"{raw[k][c]:.6f}" for k in CRITERIA] + [f"{u[k][c]:.6f}" for k in CRITERIA])

    nums_sorted = sorted(cands[selected]["numbers"])
    ticket_str = " · ".join(f"{x:02d}" for x in nums_sorted)
    final = {
        "experiment": "CLAUDE ONLY — LOTTO #2340",
        "target_draw_id": 2340,
        "target_draw_date": "2026-09-23",
        "information_cutoff_draw_id": 2339,
        "selected_candidate": selected,
        "numbers_as_stored_in_pool": cands[selected]["numbers"],
        "numbers_sorted": nums_sorted,
        "ticket": ticket_str,
        "composite_S": S[selected],
        "generating_methods": cands[selected]["generating_methods"],
        "validated_predictive_edge": bool(val.get("VALIDATED_EDGE")),
        "source_commit": rubric["source_commit"],
        "rubric_sha256": evaluation["rubric_sha256"],
        "scorer_sha256": evaluation["scorer_sha256"],
        "frozen_at_utc": run_finished,
        "real_run": real_run,
        "typesafe_jev_used": False,
    }
    canon = f"LOTTO#2340|{'-'.join(map(str, nums_sorted))}|{selected}|{final['rubric_sha256']}|{final['source_commit']}"
    final["prediction_canonical_string"] = canon
    final["prediction_sha256"] = hashlib.sha256(canon.encode()).hexdigest()
    with open(final_path, "w") as f:
        json.dump(final, f, indent=1)

    print(f"checks: {len(checks)} run, {evaluation['validity_checks']['n_failed']} failed")
    print(f"selected: {selected}  S={S[selected]:.4f}  real_run={real_run}")
    print("CLAUDE ONLY — LOTTO #2340")
    print(ticket_str)


if __name__ == "__main__":
    main()
