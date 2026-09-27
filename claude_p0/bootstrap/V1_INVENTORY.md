# Lotto V1 inventory (Claude bootstrap)

Branch `claude/lotto-2341-p0`, created from `codex/lotto-v1-snapshot` @ `ba7c5a3` (a single-commit snapshot of 280 files). Nothing in V1 was modified, run or sent to Jev. This folder is the only addition.

## Entry points
- **Canonical V1 pipeline:** `run.ps1`, which runs `scripts/audit.py` → `scripts/analyze.py` → `scripts/verify_analysis.py` → (with `-AskJev`) `scripts/jev.mjs` → `scripts/finalize.py`. Outputs go to `results/`.
- **How the frozen #2340 V1 ticket was actually produced:** `scripts/research/lotto_2340.py` → `scripts/research/lotto_2340_jev.mjs` → `scripts/research/freeze_lotto_2340.py`. These call the unchanged `analyze.py` functions and add one rule: the candidate must share ≤2 numbers with the previous primary. All three scripts are hard-wired to #2340. There is no generic per-draw wrapper.

## Where things are defined
| Item | Location |
|---|---|
| A_long … F_structure scores/objectives | `scripts/analyze.py` `model_features()`, `objectives()` (`NAMES` line 14) |
| G_ensemble weights | `analyze.py` `ensemble_weights()`; frozen at the first confirmation origin in `walk()` |
| H_random | `analyze.py` `walk()` (seed + draw_id×1009); fills candidates in `candidates()` (SEED+555) |
| Walk-forward | `analyze.py` `walk()`: min 50 training draws, a 512-combo pool per origin (SEED + draw_id×101), last 40 targets = confirmation |
| Candidate construction | `analyze.py` `candidates()`: 4,096-combo pool (SEED+999); A–F take the top 3 each, G the top 1, H_random fills to 20; ≤3 shared numbers between candidates |
| Empirical evidence gate | `analyze.py` `summaries()`: `qualifies` = confirmation Holm p < 0.05 AND block-bootstrap 95% lower bound > 36/38 AND both confirmation halves > 36/38 |
| Seeded no-edge fallback | `scripts/finalize.py` (and `freeze_lotto_2340.py`): `default_rng(20260919)` uniform pick over candidates sorted by ID; `finalize.py` also picks a minimum-overlap secondary |
| Edge-branch composite | `finalize.py` / `freeze_lotto_2340.py` (weights as in `PROTOCOL.md`) |
| Jev request | `scripts/jev.mjs`, reading `results/jev_state.json`: `jev-latest`, 1 Choice + 7 per candidate (3 Score + 4 Noul) = 141 questions; receipt stores the state SHA-256 |
| Seeds / policy | `PROTOCOL.md`; `SEED=20260919` in `analyze.py` |
| TypeSafe skill | `.agents/skills/typesafe-ai/SKILL.md` (`skills-lock.json`) |

## Data, ledger and frozen artifacts
- Data: `data/draws.json` (178 draws, 2161–2338, gap-free), `data/original_draws.json`, `data/external_draws.json`, `data/official-*.json`. The #2340 run used `results/lotto/draw2340/draws.json` (2161–2339).
- Ledger: `results/lotto/prospective_ledger.jsonl` (outcomes for #2339, the #2340 freeze, the #2340 outcome with 0 matches).
- Frozen #2340: `results/lotto/draw2340/` (`frozen.json`: C07 `C_gap` 05·11·16·24·27·34, no-edge rule, jev-1.13.0).
- Forensic: `results/lotto/forensic_2340/` and `FORENSIC_PROTOCOL.md`. Conclusion: "No Lotto V2 is justified"; no #2341 output.
- V1 frozen copy and manifest: `results/lotto/v1_snapshot/`, `results/lotto/v1_manifest.json` (captured 2026-09-21).

## Hash verification (details: `hash_verification.json`)
- V1 manifest (49 files, both the top-level files and the `v1_snapshot/` copy): all match. 17 match exactly and 32 match after LF→CRLF (the manifest was hashed on Windows).
- `draw2340/frozen.json` embedded hashes: 13 of 14 match. `frozen.json` itself matches its ledger hash `955c7d8c…`.
- Forensic `integrity.json` protected hashes: 22 of 23 match.
- **Mismatch:** `scripts/research/lotto_2340_jev.mjs` does not match the frozen hash `add06470…` under any LF/CRLF/BOM/final-newline normalization. The #2340 Jev request, response and state files all match, so the frozen #2340 evidence is intact; only the committed caller script's bytes differ.

## Gaps before any #2341 run
1. **No #2341 wrapper.** V1 has no generic per-draw entry point. `run.ps1` needs PowerShell (not installed) and Windows paths, and it overwrites `results/`. The #2340 wrapper is hard-coded to #2340.
2. **Line-ending asserts.** The research wrappers assert raw SHA-256 equality with `v1_manifest.json`. That fails on this LF checkout for 32 files.
3. **Runtime missing.** NumPy and openpyxl are not installed. `node_modules` (`@typesafe-ai/sdk` 0.6.0) is absent.
4. **Official #2340 record missing.** No raw official file exists for #2340; the ledger records it as user-supplied. V1 requires verified official additions.
5. **Workbook not in snapshot.** A byte-identical copy (`5d55e059…`) exists on other branches and can be passed with `audit.py --workbook`.
6. **Jev caller script mismatch.** `lotto_2340_jev.mjs` does not match its frozen hash (see above).
