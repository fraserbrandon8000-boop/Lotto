"""Steps 13-14: apply the frozen decision rule to the first valid Jev result and append the prospective ledger."""
import datetime as dt
import json
import os

from common import CONFIG, JEV, LEDGER, OUT, ROOT, sha256_file, write_json


def main():
    rule = json.load(open(os.path.join(CONFIG, "decision_rule.json")))
    for k, v in rule["frozen_inputs"].items():
        assert sha256_file(os.path.join(ROOT, v["path"])) == v["sha256"], f"frozen input changed: {k}"
    log = json.load(open(os.path.join(JEV, "jev_call_log.json")))
    resp = json.load(open(os.path.join(JEV, "jev_response_raw.json")))
    cand = json.load(open(os.path.join(OUT, "07_candidates_2340.json")))["candidates"]
    val = json.load(open(os.path.join(OUT, "06_validation_decision.json")))

    # validity of the result (as defined in the frozen rule)
    ans = resp["answers"]["strongest_case"]
    probs = ans["probabilities"]
    assert log.get("http_status") == 200 and ans["type"] == "choice" and set(probs) == set(cand), "not a valid completed result"

    if val["VALIDATED_EDGE"]:
        branch = "A"
        eligible = [c for c in cand if val["dev_selected_ticket_method"] in cand[c]["generating_methods"]]
    else:
        branch = "B"
        eligible = sorted(cand)
    best = max(round(probs[c], 6) for c in eligible)
    selected = sorted(c for c in eligible if round(probs[c], 6) == best)[0]
    ranked = sorted(cand, key=lambda c: -probs[c])

    final = {
        "target_draw": 2340, "target_date": "2026-09-23", "information_cutoff_draw": 2339,
        "final_ticket": cand[selected]["numbers"],
        "final_ticket_display": " · ".join(f"{n:02d}" for n in cand[selected]["numbers"]),
        "selected_candidate": selected,
        "selected_generating_methods": cand[selected]["generating_methods"],
        "selected_is_random_control": cand[selected]["is_random_control"],
        "decision_rule_branch": branch,
        "selection_basis": ("Branch B of the frozen rule: no validated predictive edge; highest Jev Choice probability over the full candidate pool"
                            if branch == "B" else "Branch A of the frozen rule: highest Jev Choice probability among validated-method candidates"),
        "validated_edge": val["VALIDATED_EDGE"],
        "jev_choice_probability": probs[selected],
        "jev_confidence": ans["confidence"],
        "jev_choice_field": ans["choice"],
        "jev_choice_field_matches_argmax": ans["choice"] == selected,
        "jev_model_version": resp["model"],
        "jev_usage": resp.get("usage"),
        "jev_choice_distribution_ranked": [{"candidate": c, "numbers": cand[c]["numbers"], "probability": probs[c],
                                            "methods": cand[c]["generating_methods"], "random_control": cand[c]["is_random_control"]} for c in ranked],
        "jev_scores": {k: v for k, v in resp["answers"].items() if v["type"] == "score"},
        "jev_nouls": {k: v for k, v in resp["answers"].items() if v["type"] == "noul"},
        "exact_random_expectation": {"expected_matches": 36 / 38, "P_3plus": 0.038698, "P_4plus": 0.002765, "jackpot": "1 in 2,760,681"},
        "disclaimer": rule["reporting"]["disclaimer"],
        "jev_calls_made": log["attempt"],
    }
    write_json(os.path.join(OUT, "08_final_ticket.json"), final)

    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    files = ["config/protocol.json", "config/decision_rule.json", "data/04_normalized_analysis_dataset.csv",
             "outputs/01_data_audit.json", "outputs/02_exact_baseline.json", "outputs/03_randomness_tests.json",
             "outputs/04_walkforward_matches.csv", "outputs/05_ticket_method_performance.json",
             "outputs/05_number_discovery_coverage.json", "outputs/06_validation_decision.json",
             "outputs/07_candidates_2340.json", "outputs/07_rankings_2340.json", "jev/jev_request.json",
             "jev/jev_response_raw.json", "jev/jev_call_log.json", "outputs/08_final_ticket.json"]
    entry = {
        "ledger": "claude_jev_cleanroom_prospective", "entry_type": "PRE_DRAW_FREEZE", "recorded_at_utc": now,
        "target_draw": 2340, "target_date": "2026-09-23", "draw_time_local": "20:25 America/Jamaica (UTC-5)",
        "information_cutoff_draw": 2339, "final_ticket": final["final_ticket"], "selected_candidate": selected,
        "decision_rule_branch": branch, "validated_edge": val["VALIDATED_EDGE"],
        "jev_model": resp["model"], "jev_choice_probability": probs[selected], "jev_confidence": ans["confidence"],
        "jev_request_sent_at_utc": log["sent_at_utc"], "jev_response_received_at_utc": log["received_at_utc"],
        "jev_calls_made": log["attempt"], "random_seed_master": 23402026,
        "workbook_sha256": sha256_file(os.path.join(ROOT, "..", "..", "data", "original", "Lotto-Draw-Dataset.xlsx")),
        "sha256": {f: sha256_file(os.path.join(ROOT, f)) for f in files},
        "outcome": None,
    }
    os.makedirs(LEDGER, exist_ok=True)
    path = os.path.join(LEDGER, "prospective_ledger.jsonl")
    existing = open(path).read().splitlines() if os.path.exists(path) else []
    assert not any(json.loads(l).get("target_draw") == 2340 and json.loads(l).get("entry_type") == "PRE_DRAW_FREEZE" for l in existing), \
        "ledger already has a #2340 freeze entry (append-only)"
    with open(path, "a") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")
    print(json.dumps({k: final[k] for k in ("final_ticket_display", "selected_candidate", "selected_generating_methods",
                                            "selected_is_random_control", "decision_rule_branch", "jev_choice_probability",
                                            "jev_confidence", "jev_choice_field", "jev_model_version", "jev_usage")}, indent=1))
    for d in final["jev_choice_distribution_ranked"]:
        print(f"{d['candidate']} {d['probability']:.4f} {d['numbers']} {d['methods']}{' [control]' if d['random_control'] else ''}")
    for k, v in final["jev_scores"].items():
        print(k, round(v["score"], 3), "conf", round(v["confidence"], 3), {kk: round(p, 3) for kk, p in v["probabilities"].items()})
    for k, v in final["jev_nouls"].items():
        print(k, round(v["noul"], 3))


if __name__ == "__main__":
    main()
