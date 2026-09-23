"""Step 12 (part 1): build the single Jev request from code-computed evidence and validate it against
the TypeSafe OpenAPI schema served by api.typesafe.ai. This script makes no network call to Jev."""
import json
import os

import jsonschema

from common import JEV, OUT, sha256_file

MODEL = "jev-latest"


def fmt(nums):
    return " · ".join(f"{n:02d}" for n in nums)


CORE = ["A_freq_all", "B_ew_20", "B_roll_10", "C_hazard", "D_trend_20v40", "E_transition", "E_pair_centrality", "G_ensemble_equal"]
COMMON = ("All 20 global", "No ticket method survives", "Every ticket, including")


def compact(c):
    wf = {m: [o["mean_matches"], o["dev_mean"], o["confirmation_mean"], o["exact_p_one_sided_full"], o["holm_p_family"], o["pct_3plus"]]
          for m, o in c["out_of_sample_performance_of_generating_methods"].items()}
    se = c["structure_evidence"]
    return {
        "numbers": c["numbers"],
        "generating_methods": c["generating_methods"],
        "random_control": c["is_random_control"],
        "walk_forward": wf,
        "number_evidence": {f"{p['number']:02d}": [p["ranks_among_38"][r] for r in CORE] + [p["full_history_z"], p["last20_count"], p["components_ranking_it_top12"]]
                            for p in c["per_number_evidence"]},
        "summary": {"mean_ensemble_percentile": c["ensemble_evidence"]["mean_ensemble_percentile"],
                    "consensus_index_0_to_1": c["ensemble_evidence"]["consensus_index_0_to_1"],
                    "mean_full_history_z": c["long_term_evidence"]["mean_full_history_z"],
                    "last20_total_vs_expected_18.95": c["recent_frequency_evidence"]["last20_total"],
                    "mean_trend_percentile": c["trend_evidence"]["mean_trend_percentile"],
                    "mean_hazard_percentile": c["gap_evidence"]["mean_hazard_percentile"],
                    "mean_pair_z": c["pair_evidence"]["mean_pair_z"], "pairs_z_above_2": c["pair_evidence"]["pairs_with_z_above_2"]},
        "structure": [se["sum"], se["odd"], se["low_1_19"], se["consecutive_pairs"], se["range"], se["structure_class_null_probability"], se["structure_typicality_z"]],
        "sensitivity": [c["sensitivity"]["lambda_grid_variants_keeping_4plus_numbers"], c["sensitivity"]["sibling_rankers_keeping_4plus_numbers"]],
        "specific_counterevidence": [x for x in c["counterevidence"] if not x.startswith(COMMON)],
    }


def main():
    cand = json.load(open(os.path.join(OUT, "07_candidates_2340.json")))
    val = json.load(open(os.path.join(OUT, "06_validation_decision.json")))
    base = json.load(open(os.path.join(OUT, "02_exact_baseline.json")))
    rnd = json.load(open(os.path.join(OUT, "03_randomness_tests.json")))
    perf = json.load(open(os.path.join(OUT, "05_ticket_method_performance.json")))
    cov = json.load(open(os.path.join(OUT, "05_number_discovery_coverage.json")))

    rt = rnd["global_tests"]
    smallest = min(rt, key=lambda t: t["p_value"])
    base_methods = [m for m in perf if not (m.startswith("H_random") or m == "random_ticket")]
    state = {
        "decision_context": {
            "game": "Jamaica Lotto: 6 distinct main numbers drawn from 1-38.",
            "target": "Draw #2340 on 2026-09-23 (not yet drawn).",
            "information_used": "169 observed historical draws #2161-#2339 (2025-01-01 to 2026-09-19); draws #2252-#2261 were unavailable and left as a gap. All evidence below was computed by code from these draws only.",
            "interpretation": "Under a fair uniform draw every 6-number ticket has exactly the same chance. A preference among tickets is a judgment about which ticket's supporting evidence is strongest, not a winning probability.",
        },
        "exact_random_baseline_per_ticket": {
            "P_matches": {k: round(v["probability"], 6) for k, v in base["single_ticket"].items()},
            "expected_matches": round(base["expected_matches_per_ticket"], 4),
            "P_3_or_more": round(base["tails"]["P(3+)"], 4), "P_4_or_more": round(base["tails"]["P(4+)"], 5),
            "jackpot_one_in": base["total_combinations"],
        },
        "randomness_tests": {
            "global_tests_run": len(rt),
            "validated_departures_holm_p_below_0.05": rnd["n_validated"],
            "raw_p_below_0.05": rnd["n_suggestive"],
            "smallest_raw_p": {"test": smallest["test"], "p": round(smallest["p_value"], 3)},
            "tests_covered": "number frequency, max/min counts, re-appearance gaps, repeats and lag-1..5 overlaps, pair co-occurrence, 38x38 transitions, draw-sum autocorrelation, sum/odd/low/consecutive/range structure, bonus uniformity",
            "per_number_binomial": {"raw_p_below_0.05": len(rnd["per_number_raw_p_below_0.05"]), "of": 38, "min_bh_q": round(rnd["per_number_min_q"], 2)},
            "pairs": {"raw_p_below_0.05": rnd["pairs_raw_p_below_0.05"], "expected_by_chance": round(rnd["pairs_raw_p_below_0.05_expected_by_chance"], 1), "min_bh_q": round(rnd["pairs_min_q"], 2)},
            "conclusion": rnd["overall_classification"],
        },
        "walk_forward_results": {
            "design": "Strict causal walk-forward: for each of 140 historical targets (#2190-#2339) all features, rankings and tickets used only earlier draws; development = first 70 targets, confirmation = last 70. Selection on development only, one pre-registered test on confirmation.",
            "ticket_methods_tested": val["n_base_methods"],
            "random_expectation_matches_per_ticket": 0.947,
            "pre_registered_dev_selected_method": {
                "method": val["dev_selected_ticket_method"],
                "development_mean": round(val["dev_selected_dev_mean"], 3), "development_p": round(val["dev_selected_dev_p"], 4),
                "confirmation_mean": round(val["dev_selected_conf_mean"], 3), "confirmation_p": round(val["dev_selected_conf_p_upper"], 3),
                "sensitivity_variants_above_random_in_confirmation": round(val["sensitivity_fraction_above_baseline"], 3),
            },
            "validated_edge": val["VALIDATED_EDGE"],
            "methods_with_raw_p_below_0.05_full_period": len(val["methods_raw_p_below_0.05_full_period"]),
            "expected_by_chance_at_0.05": round(0.05 * val["n_base_methods"], 1),
            "methods_surviving_holm_correction": len(val["methods_surviving_holm"]),
            "uniform_random_controls_mean_matches": {k: round(v["mean"], 3) for k, v in val["random_controls"].items()},
            "number_discovery_top12": {
                "random_expectation": round(12 * 6 / 38, 3),
                "dev_selected_ranker": val["number_discovery"]["dev_selected_ranker_top12"],
                "dev_mean": round(val["number_discovery"]["dev_mean"], 3), "confirmation_mean": round(val["number_discovery"]["conf_mean"], 3),
                "confirmation_p": round(val["number_discovery"]["conf_p_upper"], 3),
                "random_ranker_top12_mean": round(cov["H_random"]["12"]["mean"], 3),
            },
            "power": f"With 70 confirmation targets only a mean improvement of about {val['power']['min_detectable_mean_improvement_80pct_power']:.2f} matches per ticket ({val['power']['as_percent_of_baseline']:.0f}% over random) was detectable at 80% power.",
        },
        "glossary": {
            "A_freq_all": "count over all prior draws", "A_inv_cold": "least frequent numbers ranked first",
            "B_roll_W": "count in the last W draws", "B_ew_h": "exponentially weighted count, half-life h draws",
            "C_hazard": "pooled empirical re-appearance rate at each number's current gap", "C_overdue": "longest current gap first",
            "C_recent": "shortest current gap first", "C_own_gap_pct": "current gap percentile within the number's own gap history",
            "D_trend_20v40": "rate in last 20 draws minus rate in the 40 before", "D_slope_50": "linear trend over last 50 draws",
            "E_transition": "smoothed lift of appearing after the numbers of the preceding draw, estimated from all prior consecutive pairs",
            "E_pair_centrality": "strength of frequency-adjusted positive pair co-occurrence",
            "G_ensemble_equal": "equal-weight average of percentile ranks of A_freq_all, B_ew_20, C_hazard, D_trend_20v40, E_transition",
            "G_ensemble_adaptive": "same components weighted by their past walk-forward excess coverage",
            "opt_top12": "best 6-subset of the ranker's top 12 by score + pair lift + structural typicality",
            "pair_top12": "6-subset of the ranker's top 12 with the strongest pair co-occurrence", "consensus": "numbers most often in the top 12 of the five component rankers",
            "H_random / random_ticket": "uniform random control", "ranks_among_38": "1 = ranked best by that ranker for #2340",
        },
        "candidate_evidence_legend": {
            "number_evidence": "per number: [" + ", ".join(f"rank under {r}" for r in CORE) + ", full-history count z-score, count in last 20 draws (expected 3.16), how many of the 5 ensemble components rank it top 12]",
            "walk_forward": "out-of-sample record of each generating method over 140 targets: mean matches per ticket (random 0.947), development mean, confirmation mean, one-sided exact p (full period), Holm-adjusted p across 162 methods, % of targets with 3+ matches (random 3.87%)",
            "sensitivity": "at the #2340 state: construction-weight variants and sibling rankers that keep at least 4 of the 6 numbers",
            "structure": "sum, odd count, count in 1-19, consecutive pairs, range, exact null probability of the ticket's structure class, typicality z (0 = average)",
        },
        "counterevidence_common_to_all_candidates": [
            "All 20 global randomness tests are consistent with an independent uniform draw (min Holm p = 1.0).",
            "No ticket method survives Holm correction; the pre-registered dev-selected method fell below the random baseline in confirmation.",
            "Every ticket has exactly the same random odds: expected matches 0.947, P(3+) = 3.87%.",
            "No pair co-occurrence survives correction; C_hazard's walk-forward top-12 coverage (1.893) equals random (1.895).",
        ],
        "candidates": {cid: compact(c) for cid, c in cand["candidates"].items()},
    }
    criteria = {cid: f"Ticket {fmt(c['numbers'])} (evidence in `candidates.{cid}`)" for cid, c in cand["candidates"].items()}
    questions = {
        "strongest_case": {
            "type": "choice",
            "instructions": {
                "question": "Given only the supplied pre-draw empirical evidence, which complete candidate ticket has the strongest overall case among these alternatives?",
                "how_to_judge": [
                    "Judge each candidate as a complete six-number ticket using its evidence profile in `candidates`.",
                    "Give most weight to out-of-sample (walk-forward) performance of the generating methods, especially confirmation-period results, then to independent model consensus, sensitivity/stability, and the listed counterevidence.",
                    "Do not prefer a ticket for its visual pattern.",
                    "Every ticket has identical exact random odds; decide which ticket's supporting evidence is strongest, not which is certain to win.",
                ],
            },
            "criteria": criteria,
        },
        "empirical_robustness": {
            "type": "score",
            "instructions": "Using `walk_forward_results` and `randomness_tests`, rate how robust the out-of-sample empirical support is for preferring any evidence-based candidate ticket over a uniformly random ticket for draw #2340.",
            "criteria": [
                "No support: confirmation-period results are at or below the random baseline and no result survives multiple-testing correction.",
                "Weak: isolated raw-significant results occur at about the rate expected by chance and do not replicate in the confirmation period.",
                "Mixed: some confirmation-period improvement over random, but not statistically significant or not robust across variants.",
                "Moderate: a pre-registered method beats random in the confirmation period with p < 0.05, but robustness across variants is limited.",
                "Strong: a pre-registered method beats random in confirmation with p < 0.05, survives multiple-testing correction, and holds across variants.",
            ],
        },
        "evidence_quality": {
            "type": "score",
            "instructions": "Rate the quality of the evidence base for judging lottery prediction methods here: sample size, data completeness, causal testing design, controls, and statistical power, as described in the state.",
            "criteria": [
                "Very poor: tiny or unreliable data, no out-of-sample testing, no controls.",
                "Poor: small data and weak design, with leakage or selection problems likely.",
                "Adequate: causal walk-forward testing with random controls, but small sample and low power for realistic effects.",
                "Good: causal design, random controls, complete data and power adequate for modest effects.",
                "Excellent: large complete sample, high power, fully causal design, results replicated.",
            ],
        },
        "model_consensus": {
            "type": "score",
            "instructions": "Rate how strongly independent model families (frequency, recency, gap, trend, pair/transition) agree on the same numbers and tickets for draw #2340, using the candidates' per-number ranks, consensus indices and generating methods.",
            "criteria": [
                "No agreement: model families point to largely different numbers.",
                "Slight agreement: a few numbers recur, mostly among closely related frequency-type rankers.",
                "Partial agreement: several numbers recur across two or three families.",
                "Substantial agreement: most families rank a common core of numbers highly.",
                "Strong agreement: nearly all independent families converge on the same ticket.",
            ],
        },
        "stability": {
            "type": "score",
            "instructions": "Rate how stable the evidence-based candidate preferences are under reasonable changes: construction weights (lambda grid), window and half-life variants, sibling rankers, and development versus confirmation periods.",
            "criteria": [
                "Highly unstable: small changes replace most numbers and method rankings reverse between periods.",
                "Unstable: rankings of methods change between periods and variants often replace several numbers.",
                "Moderately stable: tickets persist under construction weights but method performance does not persist across periods.",
                "Stable: tickets and method performance persist across most variants and both periods.",
                "Highly stable: tickets and performance are essentially unchanged under all reasonable variants and periods.",
            ],
        },
        "likely_chance_or_overfitting": {
            "type": "noul",
            "instructions": "The apparent historical advantages of the best-performing methods in `walk_forward_results` are most likely explained by chance or overfitting.",
            "criteria": {"true": "Chance and selection effects plausibly explain the observed advantages.",
                         "false": "The advantages are too large or consistent to be explained by chance or overfitting."},
        },
        "depends_on_one_model": {
            "type": "noul",
            "instructions": "The case for the strongest-looking candidate tickets depends mainly on a single model or ranker rather than on several independent model families.",
            "criteria": {"true": "One model or ranker drives the case.", "false": "Several independent model families support it."},
        },
        "unstable_under_reasonable_assumptions": {
            "type": "noul",
            "instructions": "The preferred candidate tickets would change materially under reasonable alternative assumptions (parameters, windows, evaluation periods).",
            "criteria": {"true": "Reasonable alternative assumptions would materially change which tickets look best.",
                         "false": "The preferred tickets are robust to reasonable alternative assumptions."},
        },
        "materially_stronger_than_random": {
            "type": "noul",
            "instructions": "The supplied evidence shows predictive strength materially stronger than the exact random baseline.",
            "criteria": {"true": "Evidence demonstrates a material, validated advantage over random.",
                         "false": "Evidence does not demonstrate a material advantage over random."},
        },
    }
    request = {"model": MODEL, "state": state, "questions": questions}

    spec = json.load(open(os.path.join(JEV, "typesafe_openapi.json")))
    schema = dict(spec["components"]["schemas"]["SystemOneRequest"])
    schema["$defs"] = spec["components"]["schemas"]
    s = json.dumps(schema).replace("#/components/schemas/", "#/$defs/")
    jsonschema.validate(request, json.loads(s))
    assert set(questions["strongest_case"]["criteria"]) == set(cand["candidates"])

    path = os.path.join(JEV, "jev_request.json")
    with open(path, "w") as f:
        json.dump(request, f, indent=1)
        f.write("\n")
    text = json.dumps(state)
    for banned in ("2339 numbers", "last draw", "most recent draw", "previous ticket", "played"):
        assert banned not in text.lower(), banned
    print("request valid; bytes:", os.path.getsize(path), "approx tokens:", len(json.dumps(request)) // 4,
          "questions:", len(questions), "choices:", len(criteria), "sha256:", sha256_file(path))


if __name__ == "__main__":
    main()
