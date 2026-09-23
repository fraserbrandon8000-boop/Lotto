"""Step 12 (part 2): send the frozen request to TypeSafe Jev exactly once and save the raw response.

Refuses to run if a response or call log already exists. Never reads, prints or stores the credential:
authentication is injected by the environment's egress proxy for api.typesafe.ai."""
import datetime as dt
import hashlib
import json
import os
import sys

import requests

from common import JEV, ROOT, sha256_file

URL = "https://api.typesafe.ai/v1/systemone"


def main():
    req_path = os.path.join(JEV, "jev_request.json")
    resp_path = os.path.join(JEV, "jev_response_raw.json")
    log_path = os.path.join(JEV, "jev_call_log.json")
    if os.path.exists(resp_path) or os.path.exists(log_path):
        sys.exit("REFUSING: a Jev call has already been made for this experiment (first result is final).")
    rule = json.load(open(os.path.join(ROOT, "config", "decision_rule.json")))
    body = open(req_path, "rb").read()
    if hashlib.sha256(body).hexdigest() != rule["frozen_inputs"]["jev_request"]["sha256"]:
        sys.exit("REFUSING: request bytes do not match the frozen hash in config/decision_rule.json.")
    sent = dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds")
    log = {"attempt": 1, "url": URL, "request_sha256": hashlib.sha256(body).hexdigest(), "sent_at_utc": sent}
    try:
        r = requests.post(URL, data=body, headers={"Content-Type": "application/json"}, timeout=300)
        log["received_at_utc"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds")
        log["http_status"] = r.status_code
        log["response_headers"] = {k: v for k, v in r.headers.items()
                                   if k.lower() in ("content-type", "date", "x-request-id", "request-id", "server")}
        with open(resp_path, "wb") as f:
            f.write(r.content)
        log["response_sha256"] = sha256_file(resp_path)
    except Exception as e:  # transport failure: logged, never silently retried
        log["received_at_utc"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds")
        log["transport_error"] = f"{type(e).__name__}: {e}"
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)
        f.write("\n")
    print(json.dumps({k: v for k, v in log.items() if k != "response_headers"}, indent=1))


if __name__ == "__main__":
    main()
