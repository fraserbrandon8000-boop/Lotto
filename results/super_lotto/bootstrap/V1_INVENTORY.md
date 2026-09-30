# Super Lotto V1 inventory (Claude bootstrap)

Branch `claude/super-lotto-p0`, created from `codex/lotto-v1-snapshot` @ `ba7c5a3`. No Lotto P0 branch was used as a base, and nothing in V1 was modified.

## Game
5 distinct main numbers from 1–35, plus an independent Super Ball from 1–10. Main matches follow Hypergeometric(35, 5, 5), so a random ticket averages 5/7 ≈ 0.714 main matches. A Super Ball guess is right with probability 0.1. Draws are on Tuesday and Friday at 20:30 Jamaica (01:30 UTC the next day); the data has 89 Tuesday and 88 Friday draws.

## Entry points
| Role | File |
|---|---|
| Core V1 (models, walk-forward, gate, candidates) | `scripts/research/super_lotto.py` (`main()`; reads the Windows workbook `super_lotto_draw_history.xlsx` via `audit()`) |
| #1753 prospective freeze | `scripts/research/freeze_super.py` + Jev `scripts/research/super_jev.mjs` |
| #1754 prospective run (the latest V1 procedure) | `scripts/research/super_1754.py` → `prepare_super_1754_jev.py` / `super_1754_transport.mjs` / `super_1754_jev.mjs` → `validate_super_1754_response.mjs` → `freeze_super_1754.py` |
| #1753 forensic | `scripts/research/super_1753_forensic.py`, `report_super_1753.py` |
| Shared, game-agnostic helpers | `scripts/research/common.py` (docstring: "Game-agnostic mathematics. No files, fitted parameters or game data loaded.") |

## Where things are defined (`super_lotto.py`)
| Item | Location |
|---|---|
| Main models A_long, B_recent, C_gap, D_trend | `features()`: long frequency, last-30/EW-20 mix, current gap, 20-vs-prior-40 trend (z-scored) |
| E_pairs | `pairmat()`: training-only Holm 0.05 positive pair lift, otherwise flat |
| F_structure | `structures()` / `objective()` row 6: whole-ticket structure distance (no number-level ranking) |
| G_ensemble | `weights()`: prior-performance weights with 20 pseudo-observations, frozen at the confirmation start |
| H_random | seeded uniform ticket (seed + target×503) |
| Super Ball models | S_long, S_recent, S_gap, S_trend (`features()` on the SB indicator), S_transition (Holm-gated transition from the previous SB), S_ensemble, S_random |
| Walk-forward | `walk()`: warm-up 50, expanding window, a 512-combination search pool per origin (seed + target×101), last 40 origins = confirmation |
| Evidence gate | `performance()`: main and SB gated separately; `qualifies` = confirmation Holm p < 0.05 AND block 95% lower bound > own random mean AND both halves > random |
| Candidates | `candidate_set()`: fixed 4,096-combination pool (SEED+333); A–F top 3 each, G top 1, H fill (SEED+555+k); ≤3 shared mains; **SB assigned cyclically: candidate i gets the SB prediction of model SN[i mod 7]** |
| No-edge fallback | `freeze_super.py` / `freeze_super_1754.py`: `candidates[default_rng(2026092109).integers(20)]`, a fresh generator each run, so the index is always **9 → SL10** (D_trend top ticket + S_gap SB). There is no previous-ticket overlap rule. |
| Edge branch | qualified candidates ranked by validated standardized excess, then Jev quality, robustness, Choice, ID |
| Jev request | `super_1754_jev.mjs`: `jev-latest`, 1 Choice over 20 tickets + 4 Scores + 4 Nouls per candidate = 161 questions; single HTTP attempt, retries disabled; the receipt hashes state, request (compact JSON) and response |
| Seed | 2026092109 (`PROTOCOL.md`, `super_lotto.py`) |
| TypeSafe | `@typesafe-ai/sdk` 0.6.0 (`package-lock.json`); `.agents/skills/typesafe-ai/SKILL.md`; `results/super_lotto/typesafe-sdk-reference.md` |

## Data, ledger, frozen artifacts
- Data: `results/super_lotto/draws.json` (1577–1752, 176 draws) and `results/super_lotto/draw1754/draws.json` (1577–1753, 177 draws; #1753 appended from the official API). The source workbook is **not in the repository**; its SHA-256 (`e7c654a8…`) is recorded in the metadata.
- Prospective ledger: `results/super_lotto/prospective/ledger.jsonl` (#1753 frozen, #1753 outcome, #1754 frozen). Frozen predictions: `prospective/prediction_1753.json`, `prediction_1754.json`.
- #1753 forensic: `results/super_lotto/forensic_1753/` (conclusion: "No Super Lotto V2 is justified").
- #1754 run: `results/super_lotto/draw1754/`, containing the pre-Jev `candidate-freeze.json` (01:02:08 UTC), the Jev call (started 01:04:15), and the freeze (01:05:45 UTC, 24 minutes before the 01:30 draw).
- Frozen tickets: #1753 SL10 01·22·32·34·35 + SB2; #1754 SL10 01·02·18·34·35 + SB2. Both used the no-edge fallback and both were Jev model jev-1.13.0.

## Hash verification (`hash_verification.json`)
- `prediction_1754.json`: 43 of 44 embedded hashes match (12 exact, 31 after LF→CRLF). `prediction_1753.json`: 11 of 12.
- Ledger hashes of both prediction files: match. The #1754 pre-Jev candidate freeze: 6 of 6. The #1754 Jev receipt: state, response and compact request all match.
- The #1754 V1 preservation manifest: 34 of 35.
- **Genuine mismatches (unresolved, historical):** `scripts/research/super_jev.mjs` (the #1753 Jev caller; the #1754 call used `super_1754_jev.mjs`, which matches), and `results/super_lotto/typesafe-sdk-reference.md` (a copied documentation page). No LF/CRLF/BOM/newline variant reproduces them. Neither affects the #1754 artifacts.

## Isolation audit
- `super_lotto.py`, `super_1754.py`, `super_1753_forensic.py`, the freeze scripts and the Jev scripts import only `common.py` and read only `results/super_lotto/`.
- Three Codex files touch Lotto paths but do not feed Super Lotto evidence:
  - `freeze_super.py` hashes the script folder and explicitly excludes `lotto_forensic.py`.
  - `verify_research.py` verifies the Lotto V1 manifest before a Super Lotto check.
  - `reports.py` has a separate Lotto report function.
- **None of these three are used by any new Super Lotto work.**

## Gaps for new prospective runs
1. The #1754 procedure is hard-wired to #1754 (cutoff 1753, deadline, target). A parameterized wrapper must be proven equivalent to it before use.
2. The workbook path is Windows-only and the workbook is absent. The normalized `draws.json` and the recorded workbook hash are available.
3. The official results API (`test-results.supremeventures.com`) is blocked by this environment's network policy, so results after #1754 must be supplied.
