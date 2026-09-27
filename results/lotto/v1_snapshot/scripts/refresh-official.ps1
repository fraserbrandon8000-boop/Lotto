param([datetime]$From)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$page='https://supremeventures.com/past-results/'
$html=(Invoke-WebRequest -UseBasicParsing $page).Content
# Public client token published by the official results page; never log it.
$publicToken=[regex]::Match($html,'"ivr_api_key":"([^"]+)"').Groups[1].Value
$base=[regex]::Match($html,'"ivr_api_url":"([^"]+)"').Groups[1].Value
if (-not $publicToken -or $base -ne 'https://test-results.supremeventures.com/public') { throw 'Official feed configuration changed; inspect the official page before fetching.' }
if (-not $PSBoundParameters.ContainsKey('From')) {
    $draws=Get-Content (Join-Path $root 'data/draws.json') -Raw | ConvertFrom-Json
    $From=[datetime]($draws | Sort-Object date | Select-Object -Last 1).date
}
$today=[TimeZoneInfo]::ConvertTimeBySystemTimeZoneId([datetime]::UtcNow,'SA Pacific Standard Time').Date
$sources=@()
for ($start=$From.Date; $start -le $today; $start=$end.AddDays(1)) {
    $end=$start.AddDays(9); if ($end -gt $today) { $end=$today }
    $startText=$start.ToString('yyyy-MM-dd'); $endText=$end.ToString('yyyy-MM-dd')
    $url="$base/game/5/from/$startText/to/$endText"
    $content=(Invoke-WebRequest -UseBasicParsing $url -Headers @{Authorization="Bearer $publicToken"}).Content
    $parsed=$content | ConvertFrom-Json
    if ($parsed.error) { throw "Official results error: $($parsed.error)" }
    if (-not $content.TrimStart().StartsWith('[')) { throw 'Unexpected official archive schema.' }
    $file="data/official-$startText.json"
    $content | Set-Content -Encoding utf8 (Join-Path $root $file)
    $sources+=@{source_page=$page;url=$url;file=$file;retrieved_utc=[datetime]::UtcNow.ToString('o')}
    Write-Output "Retrieved official Lotto archive: $startText through $endText"
}
$sources | ConvertTo-Json -Depth 5 | Set-Content -Encoding utf8 (Join-Path $root 'data/latest-retrieval.json')
Remove-Variable publicToken
