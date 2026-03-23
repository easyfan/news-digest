# install.ps1 — news-digest Claude Code plugin installer (Windows)
#
# Usage:
#   .\install.ps1              # install to $HOME\.claude\
#   .\install.ps1 -DryRun      # preview without writing
#   .\install.ps1 -Uninstall   # remove installed files

param(
  [switch]$DryRun,
  [switch]$Uninstall,
  [string]$ClaudeDir = "$HOME\.claude"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

function Write-Ok   { param($msg) Write-Host "  v $msg" -ForegroundColor Green }
function Write-Skip { param($msg) Write-Host "  - $msg (up to date)" -ForegroundColor DarkGray }
function Write-Info { param($msg) Write-Host "  $msg" }
function Write-Warn { param($msg) Write-Host "  ! $msg" -ForegroundColor Yellow }

$version = (Get-Content "$ScriptDir\package.json" | Select-String '"version"')[0] -replace '.*"version":\s*"([^"]+)".*','$1'

Write-Host ""
Write-Host "  news-digest — Claude Code plugin v$version"
Write-Host "  Target: $ClaudeDir"
if ($DryRun) { Write-Host "  Mode: DRY RUN (no files modified)" }
Write-Host ""

# Check Claude CLI
if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
  Write-Warn "'claude' not found. Install Claude Code: https://claude.ai/code"
  Write-Host ""
}

$files = @{
  "commands\news-digest.md" = "commands\news-digest.md"
  "agents\news-learner.md"  = "agents\news-learner.md"
}

if ($Uninstall) {
  Write-Host "  Uninstalling..."
  foreach ($entry in $files.GetEnumerator()) {
    $dst = Join-Path $ClaudeDir $entry.Value
    if (Test-Path $dst) {
      if (-not $DryRun) { Remove-Item $dst }
      Write-Ok "Removed $dst"
    } else {
      Write-Skip (Split-Path -Leaf $dst)
    }
  }
  Write-Host ""
  Write-Host "  Uninstall complete."
  Write-Host ""
  exit 0
}

$changed = 0
foreach ($entry in $files.GetEnumerator()) {
  $src = Join-Path $ScriptDir $entry.Key
  $dst = Join-Path $ClaudeDir $entry.Value
  $dstDir = Split-Path -Parent $dst

  if (-not (Test-Path $dstDir) -and -not $DryRun) { New-Item -ItemType Directory -Path $dstDir | Out-Null }

  $name = Split-Path -Leaf $dst
  if ((Test-Path $dst) -and ((Get-FileHash $src).Hash -eq (Get-FileHash $dst).Hash)) {
    Write-Skip $name
  } else {
    Write-Info "Installing $name..."
    if (-not $DryRun) { Copy-Item $src $dst -Force }
    Write-Ok "$name -> $dst"
    $changed++
  }
}

Write-Host ""
if ($DryRun) {
  Write-Host "  [dry-run] $changed file(s) would be modified."
} else {
  Write-Host "  Done! $changed file(s) installed."
  Write-Host ""
  Write-Host "  Quick start:"
  Write-Host "    /news-digest                  # full digest + learning layer"
  Write-Host "    /news-digest --no-learn       # news only (fast)"
  Write-Host "    /news-digest llm agent        # filter by keyword"
}
Write-Host ""
