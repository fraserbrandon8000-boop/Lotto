# Lotto Protocol 2344 (frozen before any #2344 ticket)

## Objective
Primary: maximise P(at least one played ticket = 6/6) = Σᵢ P(ticketᵢ) over three distinct tickets. With no calibrated combination model (audit A9), P(ticket) = 1/C(38,6) for every ticket, so P(6/6) = 3/2,760,681 for any three distinct tickets. Secondary (only where the primary is unaffected): P(best ≥5), P(best ≥4), P(best ≥3), E[best single-ticket matches]. Union coverage and total matches are diagnostic only.

## Data
History #2161–#2343. #2343 = 04 07 13 23 33 35, bonus 38 (official result supplied by the user) is appended exactly once as an ordinary observation by the unchanged V1 wrapper. The bonus is never a feature or a main.

## Ticket 1 — V1 SCIENCE (unchanged V1)
```
python3 scripts/research/v1_prospective.py --target 2344 --date 2026-10-07 --base results/lotto/draw2343/draws.json \
  --append-json '{"draw_id":2343,"date":"2026-10-03","numbers":[4,7,13,23,33,35],"bonus":38,...}' --previous 1,4,13,14,24,38 \
  --out results/lotto/draw2344 --protocol-append-text "..."
git commit   # candidate pool frozen before Jev
node scripts/research/v1_prospective_jev.mjs results/lotto/draw2344        # exactly one production call, jev-latest
python3 scripts/research/v1_freeze.py --dir results/lotto/draw2344 --target 2344 --previous 1,4,13,14,24,38 --deadline-utc 2026-10-08T01:25:00+00:00
```
- The first valid response is preserved.
- At a known Score-rounding boundary, the response is kept, there is no retry, and it is validated offline under V1's documented tolerance without editing.
- V1 evidence gate and final rule are unchanged: the qualified composite if a model qualifies, otherwise the seeded uniform fallback (seed 20260919) among the ≤2-overlap eligible candidates sorted by ID.

## Tickets 2–3 — ALIGNED COVERAGE (corrected construction)
```
python3 scripts/research/protocol_2344.py --draws results/lotto/draw2344/draws.json --cutoff 2343 --v1 <ticket 1> --out results/lotto/draw2344/aligned
```
1. **Features:** the V1 features at cutoff #2343 (`analyze.model_features`, unchanged).
2. **Weights:** the frozen P0 constants from `results/lotto/p0_protocol/PROTOCOL.json` (commit 72e1c07, 2026-09-29): B_recent 0.031431, D_trend 0.023771, struct 0.006750; all others 0. No re-estimation.
3. **Scoring:** score all 2,760,681 combinations, T = Σ w·Z_universe(component), using the P0 component definitions. EQ(t) = mean of the equal-weight number z-scores.
4. **Ranking:** by T descending, then EQ descending, then lexicographic order.
5. **Ticket 2:** the highest-ranked combination sharing no number with ticket 1.
6. **Ticket 3:** the highest-ranked combination sharing no number with tickets 1 and 2.
7. **Status:** T is an **unvalidated tie-break**; it carries no claim of predictive skill. Disjointness is the objective-aligned rule.

## Freeze order (hard)
1. Pre-draw check.
2. V1 run; pool commit.
3. One Jev call.
4. V1 freeze.
5. Aligned tickets.
6. **Freeze commit of all three tickets.**
7. Only then the post-freeze research:
   - Jev stability ×5;
   - Jev order-permutation ×1 and blinded IDs ×1;
   - the fixed and per-draw random controls;
   - the P1 shadows (concentration, V1 per-draw seed);
   - the legacy P0 continuity shadow.

None of these can change a ticket.

## Promotion / switching rule (prospective only)
- A track may move from SHADOW to production only on **prospective** draws after this protocol.
- It needs a pre-registered one-sided test with α = 0.05 divided by the number of live challengers, at least 50 prospective draws, and every hypothesis entered in `RESEARCH_REGISTRY.json` first.
- Concentration (top-3 combinations by P̂) becomes the jackpot-rational construction only if a model's conditional-Bernoulli log-score vs uniform passes that test.
- Historical re-tests cannot promote anything.
