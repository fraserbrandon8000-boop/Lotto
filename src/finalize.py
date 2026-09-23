"""Step 16: apply the pre-declared decision rule (config.json) to the FIRST Jev response; freeze prediction, ledger, report, hashes.
Reads only frozen files; makes no network calls and does not touch candidates, rankings or the Jev request/response."""
import json, hashlib, datetime, csv, os
OUT = "results/claude_lotto_2340"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
cfg = json.load(open(f"{OUT}/config.json")); rule = cfg["final_decision_rule_declared_before_jev"]
ana = json.load(open(f"{OUT}/analysis_results.json")); gate = ana["gate"]
ev = json.load(open(f"{OUT}/candidate_evidence.json")); cands = {c["id"]: c for c in ev["candidates"]}
resp = json.load(open(f"{OUT}/jev_response.json")); ch = resp["answers"]["choice_strongest_case"]
assert set(ch["probabilities"]) == set(cands), "Jev Choice keys must equal the frozen candidate IDs"

if gate["validated_edge"]:
    raise SystemExit("validated_edge_branch applies; not expected for #2340 (gate passed for no method)")
branch = "no_edge_branch"
probs = ch["probabilities"]; top = max(probs.values())
chosen = sorted(i for i, p in probs.items() if p == top)[0]  # ties -> lower candidate ID
nums = sorted(cands[chosen]["numbers"])
ticket = " · ".join(f"{n:02d}" for n in nums)
frozen_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

diag = {k.rsplit("_", 1)[0]: v for k, v in resp["answers"].items() if k.endswith("_" + chosen)}
final = {"system": "Claude + Jev", "target_draw": cfg["target_draw"], "target_date": cfg["target_date"],
         "information_cutoff_draw": cfg["information_cutoff_draw"], "numbers": nums, "ticket": ticket,
         "candidate_id": chosen, "decision_branch": branch, "decision_rule": rule[branch],
         "gate_validated_edge": gate["validated_edge"],
         "jev": {"model": resp["model"], "requested_model": "jev-latest", "choice": ch["choice"],
                 "choice_probability": probs[chosen], "confidence": ch["confidence"],
                 "sent_utc": resp["_sent_utc"], "received_utc": resp["_received_utc"],
                 "first_valid_response": True, "calls": 1},
         "advisory_diagnostics_for_chosen_not_used_in_decision": diag,
         "generating_methods": cands[chosen]["generating_methods"],
         "expected_matches_under_uniform": cands[chosen]["expected_matches_under_uniform"],
         "hashes": {f: sha(f"{OUT}/{f}") for f in ["config.json", "candidate_evidence.json", "analysis_results.json", "rankings_2340.csv", "jev_request.json", "jev_response.json"]},
         "frozen_utc": frozen_utc}
json.dump(final, open(f"{OUT}/final_prediction.json", "w"), indent=1)

led = f"{OUT}/ledger.csv"; new = not os.path.exists(led)
with open(led, "a", newline="") as f:
    w = csv.writer(f)
    if new: w.writerow(["target_draw", "target_date", "system", "numbers", "candidate_id", "decision_branch", "jev_model", "jev_choice_probability", "jev_confidence", "jev_calls", "jev_response_sha256", "frozen_utc", "actual_draw", "matches"])
    w.writerow([cfg["target_draw"], cfg["target_date"], "Claude + Jev", "-".join(f"{n:02d}" for n in nums), chosen, branch, resp["model"], probs[chosen], ch["confidence"], 1, final["hashes"]["jev_response.json"], frozen_utc, "", ""])

rows = sorted(probs.items(), key=lambda kv: (-kv[1], kv[0]))
report = f"""# Claude + Jev — Lotto #{cfg['target_draw']} ({cfg['target_date']})

## Final prediction

**{ticket}** (candidate {chosen})

| Field | Value |
|---|---|
| Jev Choice probability | {probs[chosen]:.2f} |
| Jev confidence | {ch['confidence']:.2f} |
| Selection basis | `{branch}`: no method passed the pre-declared gate, so the ticket is the highest-probability candidate in the Jev Choice distribution of the first valid Jev response (ties to lower ID; none occurred) |
| Jev model/version | {resp['model']} (requested `jev-latest`) |
| Jev calls | 1 (sent {resp['_sent_utc']}, received {resp['_received_utc']}) |
| Information cutoff | draw #{cfg['information_cutoff_draw']} |
| Frozen | {frozen_utc} (pre-draw) |

## Decision rule (declared in `config.json` before Jev was called)

> {rule[branch]}

Gate: {gate['rule']}. Methods passing: none (`validated_edge = false`). Under the validated evidence every candidate has the same expected value, {cands[chosen]['expected_matches_under_uniform']} matches (36/38).

## Jev Choice distribution (first valid response)

| Candidate | Ticket | P |
|---|---|---|
""" + "\n".join(f"| {i} | {'-'.join(f'{n:02d}' for n in sorted(cands[i]['numbers']))} | {p:.2f} |" for i, p in rows) + f"""

## Advisory diagnostics for {chosen} (recorded only; did not affect the choice)

- Robustness score: {diag['robustness']['score']} (confidence {diag['robustness']['confidence']})
- Model agreement score: {diag['agreement']['score']} (confidence {diag['agreement']['confidence']})
- Likely chance/overfitting (Noul): {diag['overfit']['noul']}
- Depends mainly on one model (Noul): {diag['one_model']['noul']}
- Materially stronger than a random ticket (Noul): {diag['stronger_than_random']['noul']}

Jev itself judges this ticket's apparent merit as most likely chance ({diag['overfit']['noul']}) and not materially stronger than a random ticket ({diag['stronger_than_random']['noul']}). This matches the walk-forward result: no method showed a validated edge. The pick is a disciplined tie-break among equal-expectation tickets, not evidence of predictive signal.

## Integrity

- The analysis, candidates, seeds and rankings are unchanged since commit `d4c62c2`.
- Before the real call, the Jev request was rebuilt into a scratch location and confirmed byte-identical to the frozen `jev_request.json` (sha256 `{final['hashes']['jev_request.json']}`).
- `python src/jev_decide.py` was run exactly once. Its first response was valid and is final; there was no rerun and the Claude-only fallback was not used.
- `jev_request.json` is unchanged after the run (confirmed with `git diff`).
- The full first Jev response is in `jev_response.json` (sha256 `{final['hashes']['jev_response.json']}`).
- `SHA256SUMS` lists every frozen file.
"""
open(f"{OUT}/REPORT.md", "w").write(report)

files = sorted(f for f in os.listdir(OUT) if f != "SHA256SUMS")
open(f"{OUT}/SHA256SUMS", "w").write("".join(f"{sha(f'{OUT}/{f}')}  {f}\n" for f in files))
print(ticket, chosen, probs[chosen], ch["confidence"], resp["model"])
