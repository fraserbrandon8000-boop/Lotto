# Jamaica Lotto experiment

Read **[results/REPORT.md](results/REPORT.md)** for the analysis and **[results/final_decision.json](results/final_decision.json)** for the saved picks. This is an experimental evidence-ranking pipeline, not an established predictor. The current dataset showed **no detectable out-of-sample edge**.

## Run or update

In PowerShell, from this project:

```powershell
# Reproduce deterministic results and reuse the matching saved Jev response:
./run.ps1

# After a new Lotto draw: refresh official records, analyze, and ask Jev again:
./run.ps1 -Refresh -AskJev
```

Runtime: Node.js >=20 and `@typesafe-ai/sdk` 0.6.0; Python with NumPy and openpyxl. The runner uses the existing Codex bundled runtime, with PATH fallback. No new Python dependency was installed. Seeds and modelling policy are in `PROTOCOL.md`; code is in `scripts/analyze.py`. Historical predictions and all evidence are saved, so new draws can be incorporated without rebuilding the project. New analysis replaces the current `results/` snapshot; copy it to a dated folder first if retaining multiple experiments. The Jev receipt prevents reusing a response against changed evidence. The final Jev stage is not a historically validated forecasting model.

## Credential handling

`TYPESAFE_API_KEY` stays in the Windows user environment. The runner loads it into the child process only for Jev and disables SDK logging. It is never written to source or result files. `.env` and other environment secret files are Git-ignored; `.env.example` contains only an empty placeholder. User environment variables are a local configuration store, not an encrypted vault. Do not paste the key into chat or source.

To update the local key using a masked prompt:

```powershell
$secret = Read-Host 'TypeSafe API key' -AsSecureString
[Environment]::SetEnvironmentVariable('TYPESAFE_API_KEY', [System.Net.NetworkCredential]::new('', $secret).Password, 'User')
Remove-Variable secret
```

## Data and provenance

Original: `C:/Data_Unbackupped/FRASEB01/Downloads/Lotto-Draw-Dataset.xlsx`, sheet `Lotto Draws`. The original is opened read-only and its SHA-256 checked. `scripts/audit.py --workbook PATH` supports a replacement path; the provided runner uses the original location. `data/original_draws.json` is a read-only extraction. `data/external_draws.json` contains official additions; `data/draws.json` is the merged chronological input. `data/official-*.json` retains raw official responses. Source conflicts stop the audit instead of silently replacing rows. The official feed is discovered from [Supreme Ventures' past-results page](https://supremeventures.com/past-results/) and fetched in ten-day batches.

For an explicitly requested historical backfill, `./scripts/refresh-official.ps1 -From '2025-11-19'` fetches official data from that date to today, then run the pipeline. No result is guessed. Bonuses are audited separately from main numbers and excluded from match prediction.

## Experiment files

- `PROTOCOL.md`: fixed model definitions, period separation, tests, seed, edge gate and selection policy.
- `results/audit.json`, `baseline.json`, `randomness.json`: quality checks and null expectations.
- `results/number_statistics.csv`, `draw_structure.csv`, `pair_statistics.csv`, `triple_statistics.csv`, `conditional_statistics.csv`: full descriptive evidence and corrections.
- `results/walk_forward_predictions.json`, `model_performance.csv`, `sensitivity.csv`: causal predictions, outcomes, uncertainty and robustness.
- `results/candidates.json`, `candidate_sensitivity.json`: 20 candidate profiles and perturbed ranks.
- `results/jev_request.json`, `jev_response.json`, `jev_receipt.json`: exact evidence/questions, all returned probabilities and usage, and provenance hashes.
- `results/jev_candidate_summary.csv`, `ranked_candidates.json`, `final_decision.json`: interpreted judgments and deterministic decision.
- `results/verification.json`: meaningful implementation checks, including future-outcome mutation.

Jev is called with `jev-latest`; its resolved model version is recorded. **Choice** selects an option and returns the competing-option probability distribution and confidence. **Score** returns the probability-weighted position on ordered descriptive levels, its level distribution and confidence. **Noul** returns the probability of yes, without separate confidence. These are evidence judgments, not lottery-winning probabilities. See the installed `.agents/skills/typesafe-ai/SKILL.md` and current [TypeSafe docs](https://docs.typesafe.ai/llms.txt) before changing API usage.

No frontend, database or app framework is required.
