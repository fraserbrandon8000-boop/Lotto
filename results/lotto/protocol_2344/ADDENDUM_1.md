# Protocol 2344 — Addendum 1 (committed before the production Jev call and before any #2344 ticket)

**Finding (pre-call check, class 1/2: CORRECTNESS / REPRODUCIBILITY).** `scripts/research/v1_prospective_jev.mjs` writes `jev_response.json` only after its strict in-line checks pass. A Score at the 0.03 rounding boundary would discard the first response and leave no way to preserve it without a forbidden second call. Lotto has no documented tolerance other than V1's own strict check (|score − Σk·p| < 0.03).

**Fix:** use `scripts/research/v1_prospective_jev_preserve.mjs`. It is a copy of the V1 caller with an identical state and request (diff: transport lines only) that:
- records the attempt;
- persists the first response and receipt **before** validation (write-once);
- runs the **unchanged V1 checks**;
- records any failure in the receipt and **never retries**.

If a check fails, the response is not edited. It is reported as a V1-tolerance failure. Under the no-edge rule the V1 ticket does not depend on Jev, so the failure is recorded, not repaired. No predictive logic changes.
