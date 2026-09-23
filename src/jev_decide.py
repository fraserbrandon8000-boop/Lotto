"""Step 12-15: one Jev request over complete candidate tickets; apply the pre-declared rule; freeze."""
import json, hashlib, datetime, sys, numpy as np
from typesafe_sdk import TypeSafeClient, Choice, Score, Noul, RetryPolicy
OUT = "results/claude_lotto_2340"
ev = json.load(open(f"{OUT}/candidate_evidence.json")); cands = ev["candidates"]; ids = [c["id"] for c in cands]
state = {"task": "Advisory review of complete six-number Jamaica Lotto candidate tickets (6 of 1-38) for draw #2340, using only pre-draw evidence through draw #2339.",
         "statistical_context": ev["common_context"], "candidates": cands}
Q = {"choice_strongest_case": Choice(
        instructions="Given only the supplied pre-draw empirical evidence in `statistical_context` and `candidates`, which complete candidate ticket has the strongest overall case among these alternatives?",
        criteria={c["id"]: f"Ticket {'-'.join(f'{n:02d}' for n in c['numbers'])}" for c in cands})}
for c in cands:
    i = c["id"]; t = '-'.join(f'{n:02d}' for n in c['numbers'])
    Q[f"robustness_{i}"] = Score(instructions=f"How robust is the walk-forward backtest support for candidate {i} ({t}) across development and confirmation periods, relative to the random expectation of 0.947 matches?",
        criteria=["Below or at random expectation, or inconsistent between periods", "Slightly above random in one period only", "Modestly above random in both periods but not statistically significant", "Clearly and significantly above random in both periods"])
    Q[f"agreement_{i}"] = Score(instructions=f"How much do independent ranking models agree on the numbers in candidate {i} ({t}), per `models_count_of_ticket_numbers_in_their_top10`?",
        criteria=["Little agreement: most models place few of its numbers in their top 10", "Mixed agreement", "Broad agreement across most models"])
    Q[f"overfit_{i}"] = Noul(instructions=f"Is any apparent merit of candidate {i} ({t}) likely attributable to chance or overfitting rather than real predictive signal?")
    Q[f"one_model_{i}"] = Noul(instructions=f"Does the case for candidate {i} ({t}) depend mainly on a single model?")
    Q[f"stronger_than_random_{i}"] = Noul(instructions=f"Is the evidence for candidate {i} ({t}) materially stronger than for a randomly chosen valid ticket?")
req = {"model": "jev-latest", "state": state, "questions": {k: v.model_dump() for k, v in Q.items()}}
json.dump(req, open(f"{OUT}/jev_request.json", "w"), indent=1)
if len(sys.argv) > 1 and sys.argv[1] == "--dry": print(len(Q), "questions"); sys.exit()
t0 = datetime.datetime.now(datetime.timezone.utc).isoformat()
with TypeSafeClient(api_key="placeholder-proxy-injects", model="jev-latest", retry=RetryPolicy(max_retries=2), timeout=180) as cl:
    r = cl.system_one(state=state, questions=Q)
resp = r.model_dump(mode="json"); resp["_received_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat(); resp["_sent_utc"] = t0
json.dump(resp, open(f"{OUT}/jev_response.json", "w"), indent=1)
print("saved; model:", resp.get("model"))
