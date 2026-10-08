# Super Lotto #1757 forensic (research only)

Actual #1757 (2026-10-06): **04 · 23 · 29 · 31 · 32 + SB9**.

| Frozen ticket | Result |
|---|---|
| V1 Science 01 · 02 · 11 · 15 · 22 + SB2 | 0/5, SB miss |
| P0 Coverage 1 06 · 12 · 18 · 23 · 24 + SB3 | 1/5 (23), SB miss |
| P0 Coverage 2 01 · 12 · 17 · 18 · 29 + SB7 | 1/5 (29), SB miss |

**Integrity: all checks pass (True).**
- The manifest hashes and the pre-Jev pool freeze are exact.
- The ledger is append-only (an exact prefix of the current ledger).
- One Jev attempt; the response hash matches; the known 0.03 boundary was validated offline.
- The tickets are unchanged since `dd2b47e`.
- Chronology: pool 2026-10-06T21:35:24 → Jev 2026-10-06T21:36:00 → V1 2026-10-06T21:36:16 → P0 2026-10-06T21:36:22 → replicates 2026-10-06T21:36:46 → draw 2026-10-07T01:30Z.

## Pre-draw evidence for the winners (cutoff #1756)
| Winner | A_long | B_recent | C_gap | D_trend | P0 rank | in Top-12 | best support | worst | Top 15/18/20/25 |
|---|---|---|---|---|---|---|---|---|---|
| 04 | 7 | 18 | 25 | 26 | **23** | no | A_long 7 | D_trend 26 | n/n/n/Y |
| 23 | 9 | 5 | 24 | 3 | **7** | yes | D_trend 3 | C_gap 24 | Y/Y/Y/Y |
| 29 | 13 | 8 | 35 | 6 | **10** | yes | D_trend 6 | C_gap 35 | Y/Y/Y/Y |
| 31 | 30 | 12 | 26 | 16 | **26** | no | B_recent 12 | A_long 30 | n/n/n/n |
| 32 | 23 | 11 | 32 | 8 | **16** | no | D_trend 8 | C_gap 32 | n/Y/Y/Y |

- **Why 04, 31 and 32 missed the pool.** Every P0 credibility was 0, so P0 used the equal-weight average.
  - 04 was 7th on long-run frequency but 25th–26th on gap and trend (P0 rank 23).
  - 31 had no Top-11 support (best 12th, B_recent; P0 rank 26).
  - 32 was D_trend 8th but C_gap 32nd (P0 rank 16).
  - As in #1755/#1756, the anti-correlated gap model averages away the other models' picks. Neither the gap model nor any other has validated skill.
- **Construction:** 2 winners were available (23, 29), and **both reached a ticket** (one each). Nothing was lost in construction. Capturing ≤2 in a random Top-12 has probability 0.79.
- **SB9:**
  - Ranks: S_long 6, S_recent 7, S_gap 6, S_trend 9, S_transition 1 (flat), S_ensemble 6; P0 SB rank 8.
  - Played SBs: 2, 3, 7, so a 3-distinct-SB miss (probability 0.70).
  - SB9 was in the V1 pool (SL05, SL12, SL19).

## Whole V1 pool (scored after the draw; nothing promoted)
| ID | Mains | SB | Generator | Matches | Matched | SB9 | Jev Choice | Jev rank | replicate mean Choice |
|---|---|---|---|---|---|---|---|---|---|
| SL01 | 03 · 06 · 12 · 17 · 24 | 5 | A_long | 0 | — | no | 0.02 | 4–5 | 0.02 |
| SL02 | 12 · 17 · 22 · 23 · 24 | 3 | A_long | 1 | 23 | no | 0.01 | 6–8 | 0.01 |
| SL03 | 09 · 11 · 12 · 17 · 24 | 2 | A_long | 0 | — | no | 0.02 | 4–5 | 0.02 |
| SL04 | 01 · 05 · 11 · 12 · 18 | 1 | B_recent | 0 | — | no | 0.01 | 6–8 | 0.01 |
| SL05 | 05 · 18 · 23 · 24 · 29 | 9 | B_recent | 2 | 23 29 | yes | 0.03 | 3 | 0.03 |
| SL06 | 01 · 09 · 11 · 18 · 29 | 2 | B_recent | 1 | 29 | no | 0.09999999999999999 | 2 | 0.10 |
| SL07 | 13 · 17 · 19 · 30 · 34 | 1 | C_gap | 0 | — | no | 0 | 9–20 | 0.00 |
| SL08 | 10 · 19 · 27 · 30 · 34 | 5 | C_gap | 0 | — | no | 0 | 9–20 | 0.00 |
| SL09 | 06 · 10 · 13 · 16 · 30 | 3 | C_gap | 0 | — | no | 0 | 9–20 | 0.00 |
| SL10 | 01 · 02 · 11 · 15 · 22 | 2 | D_trend | 0 | — | no | 0.01 | 6–8 | 0.00 |
| SL11 | 01 · 12 · 15 · 18 · 35 | 1 | D_trend | 0 | — | no | 0 | 9–20 | 0.00 |
| SL12 | 01 · 02 · 09 · 21 · 35 | 9 | D_trend | 0 | — | yes | 0 | 9–20 | 0.00 |
| SL13 | 18 · 22 · 23 · 24 · 30 | 2 | E_pairs | 1 | 23 | no | 0 | 9–20 | 0.00 |
| SL14 | 05 · 10 · 20 · 22 · 32 | 1 | E_pairs | 1 | 32 | no | 0 | 9–20 | 0.00 |
| SL15 | 03 · 08 · 12 · 20 · 32 | 5 | E_pairs | 1 | 32 | no | 0 | 9–20 | 0.00 |
| SL16 | 06 · 07 · 18 · 22 · 29 | 3 | F_structure | 1 | 29 | no | 0 | 9–20 | 0.00 |
| SL17 | 06 · 07 · 18 · 25 · 28 | 2 | F_structure | 0 | — | no | 0 | 9–20 | 0.00 |
| SL18 | 05 · 13 · 18 · 28 · 29 | 1 | F_structure | 1 | 29 | no | 0 | 9–20 | 0.00 |
| SL19 | 01 · 12 · 18 · 23 · 25 | 9 | G_ensemble | 1 | 23 | yes | 0.8 | 1 | 0.80 |
| SL20 | 04 · 06 · 13 · 17 · 18 | 2 | H_random | 1 | 04 | no | 0 | 9–20 | 0.00 |

- Distribution {'0': 10, '1': 9, '2': 1, '3': 0, '4': 0, '5': 0}; best SL05 (2/5).
- V1 selected SL10 by the no-edge seeded rule: 0/5, SB miss.
- Jev's favourite was **SL19** in all 6 calls; it scored 1/5 **+ SB9**. That is one draw. Jev has no validated skill, and the protocol forbids switching to Jev's favourite.

## Cumulative prospective record #1753–#1757
- **V1 (one ticket per draw):** [1, 0, 0, 0, 0] = 1 mains in 5 tickets.
  - Expected 3.57; P(≤1) = 0.095.
  - SB 0/5 (P = 0.59). **V1 played SB2 in all five draws** (fixed slot SL10 with the S_gap Super Ball).
- **P0 challengers (#1755–#1757):** 4 mains in 6 tickets (expected 4.29); 1 SB hit.
- **Fixed random control (#1755–#1757):** 7 mains in 9 tickets (expected 6.43); 1 SB hit.

All of this is consistent with chance.
