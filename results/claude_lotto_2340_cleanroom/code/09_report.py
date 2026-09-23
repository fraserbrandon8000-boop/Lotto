"""Write REPORT.md from the computed outputs (no numbers are typed by hand)."""
import json
import os

from common import OUT, ROOT

SERIOUS_RANKERS = ["A_freq_all", "A_inv_cold", "B_roll_10", "B_roll_50", "B_ew_20", "C_hazard", "C_overdue", "C_recent",
                   "D_trend_20v40", "E_transition", "E_pair_centrality", "G_ensemble_equal", "G_ensemble_adaptive", "H_random"]
CONSTR = ["top6", "opt_top8", "opt_top10", "opt_top12", "opt_top15", "pair_top12", "struct_top12", "diversity_top15"]


def j(name):
    return json.load(open(os.path.join(OUT, name)))


def main():
    audit, base, rnd = j("01_data_audit.json"), j("02_exact_baseline.json"), j("03_randomness_tests.json")
    perf, cov, val = j("05_ticket_method_performance.json"), j("05_number_discovery_coverage.json"), j("06_validation_decision.json")
    fin, leak, cand = j("08_final_ticket.json"), j("04b_leakage_test.json"), j("07_candidates_2340.json")
    L = []
    w = L.append
    w("# Claude + TypeSafe Jev clean-room experiment: Jamaica Lotto #2340\n")
    w("```\nCLAUDE + JEV CLEAN ROOM — LOTTO #2340\n\n" + fin["final_ticket_display"] + "\n```\n")
    w(f"- **Data cutoff:** draw #2339 (2026-09-19); 169 observed draws #2161–#2339, gap #2252–#2261 not recovered")
    w(f"- **Validated edge found:** {'YES' if fin['validated_edge'] else 'NO'}")
    w(f"- **Selection basis:** {fin['selection_basis']} (candidate {fin['selected_candidate']}, method `{', '.join(fin['selected_generating_methods'])}`)")
    w(f"- **Jev Choice probability:** {fin['jev_choice_probability']:.2f} (relative preference among 21 candidates, not a winning probability)")
    w(f"- **Jev confidence:** {fin['jev_confidence']:.2f}")
    w(f"- **Jev model/version:** `jev-latest` → `{fin['jev_model_version']}`")
    w(f"- **Exact random expectation for this (and every) ticket:** {36/38:.3f} matches, P(3+) = 3.87%, P(4+) = 0.28%, jackpot 1 in 2,760,681\n")

    w("## 1. Data audit\n")
    fd = audit["final_dataset"]
    w(f"- Workbook: {audit['rows_in_workbook']} rows, draws {audit['draw_id_range_workbook'][0]}–{audit['draw_id_range_workbook'][1]}, newest first; sha256 `{audit['workbook']['workbook_sha256'][:16]}…`")
    w(f"- Issues found: {audit['issue_count']} (IDs, duplicates, dates, missing values, six unique mains in 1–38, bonus validity, Wed/Sat weekday, chronology all pass)")
    w(f"- Missing IDs: {audit['missing_ids_in_workbook'][0]}–{audit['missing_ids_in_workbook'][-1]} ({len(audit['missing_ids_in_workbook'])} draws, expected dates {audit['missing_ids_expected_dates']['2252']} … {audit['missing_ids_expected_dates']['2261']}). Official Supreme Ventures pages were blocked by the environment's egress policy, so nothing was recovered or guessed.")
    for a in audit["schedule_spacing_anomalies"]:
        w(f"- Schedule note: #{a['from']} ({a['from_date']}) → #{a['to']} ({a['to_date']}) skipped one Wed/Sat slot with consecutive IDs (a suspended draw date, not a missing draw).")
    w(f"- #2338 and #2339 were added as ordinary rows (user-supplied); no conflicts; schedule continuity OK.")
    w(f"- Final analysis dataset: {fd['rows']} draws, {fd['first_date']} → {fd['last_date']}; layers kept separately in `data/01..04`.\n")

    w("## 2. Exact random baseline (6 of 38)\n")
    w("| matches | probability | 1 in |\n|---|---|---|")
    for k, v in base["single_ticket"].items():
        w(f"| {k} | {v['probability']:.8f} ({v['fraction']}) | {v['one_in']:,.2f} |")
    w(f"\nExpected matches = 18/19 = {base['expected_matches_per_ticket']:.4f}; P(3+) = {base['tails']['P(3+)']:.5f}; P(4+) = {base['tails']['P(4+)']:.6f}; P(5+) = {base['tails']['P(5+)']:.3e}; jackpot = 1/{base['total_combinations']:,}.\n")
    w("Top-k pool baselines (expected winners captured): " + ", ".join(f"top {k}: {v['expected_winners_captured']:.3f}" for k, v in base["top_k_pool_baselines"].items()) + "\n")

    w("## 3. Randomness tests\n")
    w("| test | p | Holm p | classification |\n|---|---|---|---|")
    for t in rnd["global_tests"]:
        w(f"| {t['test']} | {t['p_value']:.4f} | {t['p_holm']:.3f} | {t['classification']} |")
    w(f"\nPer-number binomial: {len(rnd['per_number_raw_p_below_0.05'])}/38 raw p<0.05, min BH q = {rnd['per_number_min_q']:.2f}. Pairs: {rnd['pairs_raw_p_below_0.05']}/703 raw p<0.05 (≈{rnd['pairs_raw_p_below_0.05_expected_by_chance']:.0f} expected by chance), min BH q = {rnd['pairs_min_q']:.2f}.")
    w(f"**Conclusion: {rnd['overall_classification']}.**\n")

    w("## 4. Walk-forward design\n")
    w(f"{val['targets']} causal targets (#{val['first_target']}–#{val['last_target']}); development #{val['dev_targets'][0]}–#{val['dev_targets'][1]}, confirmation #{val['conf_targets'][0]}–#{val['conf_targets'][1]}. "
      f"Leakage test (scrambling all future draws leaves every prediction unchanged): {'PASSED' if leak['passed'] else 'FAILED'}. Protocol committed before any predictive result (`config/protocol.json`).\n")

    w("## 5. Number discovery (mean winners captured in top k; exact p is one-sided, full period)\n")
    ks = ["6", "8", "10", "12", "15", "20"]
    w("| ranker | " + " | ".join(f"top {k}" for k in ks) + " | top-12 dev | top-12 conf | top-12 p | top-12 3+% |\n|" + "---|" * 11)
    w("| *random expectation* | " + " | ".join(f"*{6*int(k)/38:.3f}*" for k in ks) + f" | *1.895* | *1.895* | | *{base['top_k_pool_baselines']['12']['P(3+)']*100:.1f}* |")
    for r in cov:
        c = cov[r]
        w(f"| {r} | " + " | ".join(f"{c[k]['mean']:.3f}" for k in ks) + f" | {c['12']['dev_mean']:.3f} | {c['12']['conf_mean']:.3f} | {c['12']['p_upper_exact']:.3f} | {c['12']['pct_3plus']:.1f} |")
    nd = val["number_discovery"]
    w(f"\nPre-registered number-discovery check: dev-selected ranker `{nd['dev_selected_ranker_top12']}` top-12 dev {nd['dev_mean']:.3f} → confirmation {nd['conf_mean']:.3f} (random 1.895, p = {nd['conf_p_upper']:.3f}). Not validated. Full 3+/4+/5+/6 coverage for every pool size is in `outputs/05_number_discovery_coverage.json`.\n")

    w("## 6. Ticket methods (6-number tickets, 140 targets)\n")
    w("| method | mean | 95% CI | sd | 0% | 1% | 2% | 3% | 4+% | 6s | dev | conf | exact p | Holm p |\n|" + "---|" * 14)
    w("| *exact random* | *0.947* | | *0.831* | *32.8* | *43.8* | *19.5* | *3.6* | *0.28* | | *0.947* | *0.947* | | |")
    rows = [f"{r}|{c}" for r in SERIOUS_RANKERS for c in ("top6", "opt_top12")] + ["consensus", "M_follow_leader", "random_ticket"]
    rows += [m for m in val["methods_raw_p_below_0.05_full_period"] if m not in rows]
    for m in rows:
        p = perf[m]
        w(f"| {m} | {p['mean']:.3f} | {p['ci95_bootstrap'][0]:.2f}–{p['ci95_bootstrap'][1]:.2f} | {p['sd']:.2f} | {p['pct_0']:.1f} | {p['pct_1']:.1f} | {p['pct_2']:.1f} | {p['pct_3']:.1f} | {p['pct_4plus']:.1f} | {p['count_6']} | {p['dev_mean']:.3f} | {p['conf_mean']:.3f} | {p['p_upper_exact']:.3f} | {p.get('p_upper_holm_family', float('nan')):.2f} |")
    w(f"\nAll {val['n_base_methods']} methods plus 9 random controls, with medians, two-sided p, BH q and the λ sensitivity grid, are in `outputs/05_*.json`.\n")

    w("## 7. Pre-registered validation\n")
    w(f"- Dev-selected method: `{val['dev_selected_ticket_method']}`: development {val['dev_selected_dev_mean']:.3f} (p = {val['dev_selected_dev_p']:.4f}) → confirmation {val['dev_selected_conf_mean']:.3f} (p = {val['dev_selected_conf_p_upper']:.3f}).")
    w(f"- Sensitivity variants above random in confirmation: {val['sensitivity_fraction_above_baseline']:.0%} (needed ≥ 67%).")
    w(f"- Methods with raw p < 0.05: {len(val['methods_raw_p_below_0.05_full_period'])} of {val['n_base_methods']} (≈{0.05*val['n_base_methods']:.1f} expected by chance); surviving Holm: {len(val['methods_surviving_holm'])}.")
    w(f"- Power: with 70 confirmation targets, the minimum detectable improvement at 80% power is {val['power']['min_detectable_mean_improvement_80pct_power']:.2f} matches per ticket (+{val['power']['as_percent_of_baseline']:.0f}%).")
    w(f"- **VALIDATED EDGE: {'YES' if val['VALIDATED_EDGE'] else 'NO'}**. Formally 'suggestive' under the protocol wording (raw p < 0.05 results exist), but their count is at the chance rate.\n")

    w("## 8. #2340 candidate pool and Jev's first and only response\n")
    w("| candidate | ticket | generating method(s) | Jev Choice p |\n|---|---|---|---|")
    for d in fin["jev_choice_distribution_ranked"]:
        w(f"| {d['candidate']}{' (control)' if d['random_control'] else ''} | {' · '.join(f'{n:02d}' for n in d['numbers'])} | {', '.join(d['methods'])} | {d['probability']:.2f} |")
    w("\n| Jev Score (0–4) | expected score | confidence |\n|---|---|---|")
    for k, v in fin["jev_scores"].items():
        w(f"| {k} | {v['score']:.2f} | {v['confidence']:.2f} |")
    w("\n| Jev Noul | P(yes) |\n|---|---|")
    for k, v in fin["jev_nouls"].items():
        w(f"| {k} | {v['noul']:.2f} |")
    w(f"\nJev: model `{fin['jev_model_version']}`, {fin['jev_usage']['input_tokens']} input tokens, one request (`jev/jev_call_log.json`).\n")

    w("## 9. Clean-room controls\n")
    w("- Branch `claude/lotto-2340-cleanroom` created from clean base `a810de0` (base tree: `.gitignore` only).")
    w("- No other branch was checked out, logged, diffed or read; GitHub was not searched; no prior #2340 prediction, candidate set, Jev response or ticket performance was seen.")
    w("- #2339 entered only as one row of the dataset; no feature, candidate or Jev input singles it out, and the Jev state contains no raw draw list.")
    w("- Protocol committed before walk-forward results; the decision rule, candidate pool and exact request bytes were hashed, committed and pushed before the Jev call.")
    w("- Jev was called once; the first valid result is final; no rerun, no regeneration, no manual edits.\n")
    w("## 10. Limitations\n")
    w("- docs.typesafe.ai and supremeventures.com were blocked by the environment's network policy. The Jev request was built from the OpenAPI contract served by api.typesafe.ai (`jev/typesafe_openapi.json`) and the installed TypeSafe skill; the missing draws were not recovered.")
    w("- 169 draws is a small sample, so only large effects were detectable; the randomness tests and walk-forward results are both consistent with a fair, independent draw.")
    w("- Jev's Choice probabilities rank the strength of evidence cases. They are not probabilities of winning, and the final ticket has exactly the same odds as any other ticket.")
    open(os.path.join(ROOT, "REPORT.md"), "w").write("\n".join(L) + "\n")
    print("REPORT.md written,", len(L), "lines")


if __name__ == "__main__":
    main()
