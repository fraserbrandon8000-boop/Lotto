# Lotto #2344 system audit — plan (committed BEFORE any audit computation or #2344 work)

Branch `claude/lotto-2344-audit`, base `670a300` (head of `claude/lotto-2342-p0`).
Note: the original "audit-first prompt" text is not present in this session. This plan implements the user's stated
objective (P(at least one ticket = 6/6)) and their explicit instructions of 2026-10-07. Phases may be realigned to the
original prompt if it is supplied; nothing below generates #2344 tickets.

Game: Jamaica Lotto, 6 mains from 1–38 (bonus excluded), |universe| = C(38,6) = 2,760,681.

## Phase A — #2343 forensic (input, not a design signal)
Actual #2343 mains 04 07 13 23 33 35, bonus 38. Frozen: V1 01 04 13 14 24 38 (2/6), P0-1 02 06 07 08 12 22 (1/6), P0-2 04 09 10 13 18 33 (3/6).
Verify integrity/chronology of the frozen #2343 run, score the V1 pool, recover pre-draw evidence for the 6 winners,
the exact frozen P0 pool, discovery vs construction loss, and append the #2343 outcome to the ledger as ordinary history.

## Phase B — objective audit (analytic, exact)
For distinct tickets the events {ticket i = 6/6} are disjoint, so P(>=1 jackpot) = sum_i P(draw = ticket_i).
B1. Derive what this implies for overlap penalties, coverage terms, pool restriction and ticket count.
B2. Exact enumeration over all 2,760,681 draws: P(best >= k), k = 3..6, for the frozen #2343 portfolio vs
    three-identical, maximally overlapping, random-distinct and zero-overlap portfolios.
B3. Map every V1/P0 component (4,096-ticket fixed source pool, <=2 overlap rule, fixed seed, Top-K pool,
    coverage term, structure penalty, Jev) to its effect on P(6/6) and on lower tiers.

## Phase C — objective-aligned historical skill test (strict causal walk-forward)
Primary metric (predeclared): at each causal origin, the midrank percentile u of the REALIZED winning combination
among all 2,760,681 combinations under a model's combination score. Under any outcome-independent score u ~ U(0,1)
(mean 0.5, SD 1/sqrt(12)); a model that raises P(6/6) must push u above 0.5.
Models: A_long, B_recent, C_gap, D_trend, equal-weight A–D, P0 marginal M (causal weights), P0-style T with
structure term, F_structure alone, explicit random control. Additive marginal models score a combination by the sum
of its number z-scores.
Secondary (descriptive): P(all 6 winners inside causal Top-K) for K = 10..25 vs exact hypergeometric; historical
best-ticket tiers for V1, P0 and random portfolios.
Gate (one Holm family over all models): Holm p < .05 for mean u > .5 over all causal targets, confirmation
(last 40) mean u > .5, both chronological halves > .5, 5-block bootstrap 95% lower bound > .5.

## Phase D — corrections and corrected protocol (decision rules fixed now)
- If >= 1 model passes the Phase C gate: the jackpot-optimal portfolio under that model is its top-3 distinct
  combinations over the full universe (no coverage/overlap term). This is the corrected protocol.
- If no model passes: every set of 3 distinct tickets has identical P(6/6) = 3/2,760,681 under the evidence.
  The corrected protocol then (i) states that objective-aligned optimisation is impossible with current evidence,
  (ii) removes components that restrict the reachable universe or repeat tickets for no objective reason, and
  (iii) keeps any remaining "science" track explicitly labelled as research with no jackpot advantage.
- Each correction must be validated: analytic proof where exact, historical check otherwise.
The corrected protocol is committed (with hash) before any #2344 ticket is generated.

## Phase E — #2344 implementation (only after D is committed)
Target #2344, Wednesday 2026-10-07, 8:25 PM Jamaica (2026-10-08T01:25Z). Verify unpublished; append #2343 as one
ordinary observation; apply the committed corrected protocol exactly; freeze and commit tickets before any
post-freeze research calls.
