param([switch]$Refresh,[switch]$AskJev)
$ErrorActionPreference='Stop'
Push-Location $PSScriptRoot
try {
    $python=Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
    $node=Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
    if (-not (Test-Path $python)) { $python=(Get-Command python -ErrorAction Stop).Source }
    if (-not (Test-Path $node)) { $node=(Get-Command node -ErrorAction Stop).Source }
    if ($Refresh) { & (Join-Path $PSScriptRoot 'scripts/refresh-official.ps1') }
    & $python scripts/audit.py
    if ($LASTEXITCODE -ne 0) { throw 'Data audit failed.' }
    & $python scripts/analyze.py
    if ($LASTEXITCODE -ne 0) { throw 'Analysis failed.' }
    & $python scripts/verify_analysis.py
    if ($LASTEXITCODE -ne 0) { throw 'Verification failed.' }
    if ($AskJev) {
        $env:TYPESAFE_API_KEY=[Environment]::GetEnvironmentVariable('TYPESAFE_API_KEY','User')
        if (-not $env:TYPESAFE_API_KEY) { throw 'Set TYPESAFE_API_KEY in your user environment using a masked local prompt.' }
        $env:NODE_USE_SYSTEM_CA='1'
        try { & $node scripts/jev.mjs; if ($LASTEXITCODE -ne 0) { throw 'Jev request failed; prior response is not current.' } }
        finally { Remove-Item Env:TYPESAFE_API_KEY -ErrorAction SilentlyContinue }
    }
    $receipt=Get-Content results/jev_receipt.json -Raw | ConvertFrom-Json
    $currentHash=(Get-FileHash results/jev_state.json -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($receipt.state_file_sha256 -ne $currentHash) { throw 'Jev evidence changed. Run ./run.ps1 -AskJev to obtain a matching response before finalizing.' }
    & $python scripts/finalize.py
    if ($LASTEXITCODE -ne 0) { throw 'Final report generation failed.' }
    Write-Output 'Completed. Read results/REPORT.md and results/final_decision.json.'
} finally { Pop-Location }
