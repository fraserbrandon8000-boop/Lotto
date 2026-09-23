# Claude + Jev — Lotto #2340 (2026-09-23)

## Final prediction

**01 · 02 · 04 · 07 · 13 · 24** (candidate C12)

| Field | Value |
|---|---|
| Jev Choice probability | 0.90 |
| Jev confidence | 0.89 |
| Selection basis | `no_edge_branch`: no method passed the pre-declared gate, so the ticket is the highest-probability candidate in the Jev Choice distribution of the first valid Jev response (ties to lower ID; none occurred) |
| Jev model/version | jev-1.13.0 (requested `jev-latest`) |
| Jev calls | 1 (sent 2026-09-23T17:18:17.373814+00:00, received 2026-09-23T17:18:18.269060+00:00) |
| Information cutoff | draw #2339 |
| Frozen | 2026-09-23T17:19:06.222651+00:00 (pre-draw) |

## Decision rule (declared in `config.json` before Jev was called)

> If no method passed the gate (all candidates have equal expected value 36/38 under the validated evidence): final ticket = the candidate with the highest probability in the Jev Choice distribution from the FIRST valid completed Jev response. Score/Noul answers are recorded as advisory diagnostics only and do not change the choice. Ties broken by lower candidate ID.

Gate: Holm-adj full-sample one-sided p<0.05 AND development p<0.05 AND confirmation p<0.05. Methods passing: none (`validated_edge = false`). Under the validated evidence every candidate has the same expected value, 0.9474 matches (36/38).

## Jev Choice distribution (first valid response)

| Candidate | Ticket | P |
|---|---|---|
| C12 | 01-02-04-07-13-24 | 0.90 |
| C08 | 01-04-06-13-18-25 | 0.05 |
| C01 | 01-06-13-18-25-33 | 0.01 |
| C03 | 01-02-04-13-18-24 | 0.01 |
| C05 | 04-13-18-25-29-33 | 0.01 |
| C11 | 04-13-18-24-25-33 | 0.01 |
| C16 | 01-04-06-13-23-28 | 0.01 |
| C02 | 01-02-04-07-13-18 | 0.00 |
| C04 | 02-04-07-12-13-24 | 0.00 |
| C06 | 04-08-18-24-35-38 | 0.00 |
| C07 | 01-05-06-18-25-33 | 0.00 |
| C09 | 01-06-13-15-18-33 | 0.00 |
| C10 | 10-11-19-21-25-29 | 0.00 |
| C13 | 11-14-16-27-34-38 | 0.00 |
| C14 | 01-09-10-13-24-38 | 0.00 |
| C15 | 05-16-21-23-28-29 | 0.00 |

## Advisory diagnostics for C12 (recorded only; did not affect the choice)

- Robustness score: 2.03 (confidence 0.03)
- Model agreement score: 1.93 (confidence 0.9)
- Likely chance/overfitting (Noul): 0.85
- Depends mainly on one model (Noul): 0.62
- Materially stronger than a random ticket (Noul): 0.28

Jev itself judges this ticket's apparent merit as most likely chance (0.85) and not materially stronger than a random ticket (0.28). This matches the walk-forward result: no method showed a validated edge. The pick is a disciplined tie-break among equal-expectation tickets, not evidence of predictive signal.

## Integrity

- The analysis, candidates, seeds and rankings are unchanged since commit `d4c62c2`.
- Before the real call, the Jev request was rebuilt into a scratch location and confirmed byte-identical to the frozen `jev_request.json` (sha256 `050ce03201107d874f8ae986b0bfb3299ec09964380474729353cefb5844cf8f`).
- `python src/jev_decide.py` was run exactly once. Its first response was valid and is final; there was no rerun and the Claude-only fallback was not used.
- `jev_request.json` is unchanged after the run (confirmed with `git diff`).
- The full first Jev response is in `jev_response.json` (sha256 `6bcbdc001b579a2b9b8fe3396e577a18a4c0f3a4f8880e822e30dd7a4c1014fc`).
- `SHA256SUMS` lists every frozen file.
