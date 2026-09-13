# PowerShell script to install Git hooks for MAKJI automatic logging
$ErrorActionPreference = "Stop"

$repoRoot = (Get-Item $PSScriptRoot).Parent.FullName
$hooksDir = Join-Path $repoRoot ".git/hooks"

if (-not (Test-Path $hooksDir)) {
    Write-Error ".git directory not found. Please run this inside the repository."
}

$postCommitSrc = @"
#!/bin/sh
python scripts/sync_decision_index.py 2>/dev/null || python3 scripts/sync_decision_index.py 2>/dev/null
COMMIT_HASH=\$(git rev-parse --short HEAD)
COMMIT_MSG=\$(git log -1 --pretty=%B)
COMMIT_DATE=\$(date "+%Y-%m-%d %H:%M:%S")
mkdir -p logs/ai-log
echo "[\$COMMIT_DATE] Commit \$COMMIT_HASH: \$COMMIT_MSG" >> logs/ai-log/git-activity.log
"@

$postCommitPath = Join-Path $hooksDir "post-commit"
Set-Content -Path $postCommitPath -Value $postCommitSrc -Encoding UTF8
Write-Host "✅ Git hooks installed successfully at: $postCommitPath" -ForegroundColor Green
