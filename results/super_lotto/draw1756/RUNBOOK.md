# Super Lotto #1756 prospective runbook (prepared; NOT yet run)

**Target:** #1756, Friday 2026-10-02, 20:30 Jamaica = **2026-10-03T01:30:00Z**. Super Lotto draws are Tuesday and Friday (89 Tuesday and 88 Friday draws in the data).

**Why not #1755:** #1755 is Tuesday 2026-09-29 at 20:30 Jamaica. The forensic, the V2 test and designing, testing and freezing P0 could not responsibly be finished before that draw, so under the task's rule the target moves to the next future draw.

**Blocking input:** the official #1755 result (5 mains + Super Ball). It must be appended as ordinary history before V1 can run for #1756. The official results API (`test-results.supremeventures.com`) is blocked by this environment's network policy, so the result has to be supplied or the host allowed.

## Prepared and validated
- `base_draws_through_1754.json`: history 1577–1754 (#1754 appended as one ordinary observation).
- `scripts/research/super_v1_prospective.py`: V1 wrapper derived from `super_1754.py`. Re-running it for #1754 reproduced every integer output exactly (tickets, SBs, generators, ranking orders) and every float within 5.6e-16 (Windows vs Linux floating point). The only other differences are timestamps and Windows CRLF file hashes.
- `super_v1_transport.mjs` / `super_v1_jev.mjs` / `validate_super_v1_response.mjs`: a dry run on the frozen #1754 state reproduced the frozen request hash `c77ab27a…` exactly (161 questions).
- `super_v1_freeze.py`: derived from `freeze_super_1754.py` (paths and constants only; line-ending-tolerant hash checks).
- P0: `super_p0_apply.py` / `super_p0_freeze.py` (frozen protocol `5cce8a37`), `super_p0_audit_state.py` / `super_p0_jev_audit.mjs`, `super_random_control.py`, `super_jev_stability.mjs` / `super_jev_stability_analysis.py`.

## Sequence (run only when the #1755 result is known and before 2026-10-03T01:30Z)
```bash
export DEADLINE=2026-10-03T01:30:00+00:00
# 0. confirm #1756 is not yet published and now < DEADLINE
# 1. V1 (unchanged) — appends #1755 as ordinary history, freezes the candidate pool before Jev
python3 scripts/research/super_v1_prospective.py --target 1756 --base results/super_lotto/draw1756/base_draws_through_1754.json \
  --append-json '{"draw_id":1755,"date":"2026-09-29","numbers":[..],"super_ball":..,"source":"..."}' \
  --out results/super_lotto/draw1756 --deadline-utc $DEADLINE --source-sha256 e7c654a8e7c4ce56738b4bb9ea7032209f52a609e3341e448a3f260f9036a07f
git commit  # pool frozen before Jev
# 2. production Jev: exactly one call
TYPESAFE_API_KEY=proxy-injected NODE_USE_ENV_PROXY=1 NODE_EXTRA_CA_CERTS=/root/.ccr/ca-bundle.crt SL_DIR=results/super_lotto/draw1756 SL_DEADLINE=$DEADLINE node scripts/research/super_v1_jev.mjs
SL_DIR=results/super_lotto/draw1756 node scripts/research/validate_super_v1_response.mjs   # only if the caller did not write a receipt
python3 scripts/research/super_v1_freeze.py --dir results/super_lotto/draw1756 --target 1756 --target-date 2026-10-02 --deadline-utc $DEADLINE --previous-prediction results/super_lotto/prospective/prediction_1754.json
# 3. P0 tickets 2-3
python3 scripts/research/super_p0_freeze.py --dir results/super_lotto/draw1756 --target 1756 --deadline-utc $DEADLINE
# 4. random control (research only)
python3 scripts/research/super_random_control.py --target 1756 --deadline-utc $DEADLINE
# 5. Jev audit of the frozen P0 portfolio (one call)
python3 scripts/research/super_p0_audit_state.py --dir results/super_lotto/draw1756 --target 1756
SL_DIR=results/super_lotto/draw1756 node scripts/research/super_p0_jev_audit.mjs
# 6. Jev stability: 5 research replicates of the exact V1 request, after all tickets are frozen
mkdir -p results/super_lotto/jev_stability_1756 && node scripts/research/super_jev_stability.mjs results/super_lotto/draw1756 results/super_lotto/jev_stability_1756 5
python3 scripts/research/super_jev_stability_analysis.py --target 1756
```
