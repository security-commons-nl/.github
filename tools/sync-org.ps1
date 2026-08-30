<#
.SYNOPSIS
    On-demand mirror van de security-commons-nl GitHub-org naar een lokale werkmap.

.DESCRIPTION
    Pull-only, fast-forward-only. Veilig ontworpen:
      - Haalt alle NIET-gearchiveerde org-repos op (gh repo list).
      - Ontbrekende repos worden gecloned.
      - Bestaande repos: git fetch + git pull --ff-only.
      - Repos met lokale wijzigingen (dirty) of eigen commits (ahead) worden
        OVERGESLAGEN met een waarschuwing - lokaal werk wordt nooit overschreven.
      - Pusht NOOIT. Merget nooit. Voert geen repo-code uit.
      - Mappen die geen org-clone zijn, worden met rust gelaten.
    Schrijft een logregel per run naar sync-org.log.

.NOTES
    Vereist: git + GitHub CLI (gh), ingelogd (gh auth status).
    Aanbevolen: een read-only fine-grained token (contents: read) voor least privilege.
    Draai on-demand: dubbelklik sync-org.cmd, of  pwsh -File tools/sync-org.ps1
    De werkmap is standaard de map boven .github; met -Root kies je een andere.
#>

[CmdletBinding()]
param(
    [string]$Org  = 'security-commons-nl',
    # Het script woont in .github/tools/, de werkmap met alle repo's is twee niveaus daarboven.
    # Draai je hem ergens anders vandaan, geef dan -Root mee.
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot '..' '..')).Path
)

$ErrorActionPreference = 'Stop'
$started = Get-Date
$log = Join-Path $Root 'sync-org.log'

function Write-Line {
    param([string]$Symbol, [string]$Text, [string]$Color = 'Gray')
    Write-Host ("{0}  {1}" -f $Symbol, $Text) -ForegroundColor $Color
}

# --- Pre-flight checks -------------------------------------------------------
foreach ($tool in 'git', 'gh') {
    if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) {
        Write-Line '[X]' "'$tool' niet gevonden in PATH. Installeer het en probeer opnieuw." 'Red'
        exit 1
    }
}
try { gh auth status 2>&1 | Out-Null } catch {
    Write-Line '[X]' "Niet ingelogd bij GitHub. Voer 'gh auth login' uit." 'Red'
    exit 1
}

Write-Host ""
Write-Line '==' "Sync $Org  ->  $Root" 'Cyan'
Write-Host ""

# --- Repolijst ophalen (alleen niet-gearchiveerd) ---------------------------
$repos = gh repo list $Org --limit 200 --json name,isArchived |
    ConvertFrom-Json |
    Where-Object { -not $_.isArchived } |
    Select-Object -ExpandProperty name |
    Sort-Object

if (-not $repos) {
    Write-Line '[X]' "Geen repos gevonden voor org '$Org'." 'Red'
    exit 1
}

$cloned = 0; $pulled = 0; $ok = 0; $skipped = 0; $failed = 0

foreach ($name in $repos) {
    $path = Join-Path $Root $name

    # --- Ontbrekend: clonen --------------------------------------------------
    if (-not (Test-Path (Join-Path $path '.git'))) {
        try {
            gh repo clone "$Org/$name" $path -- -q 2>&1 | Out-Null
            Write-Line '[+]' "CLONE  $name" 'Green'; $cloned++
        } catch {
            Write-Line '[!]' "FOUT   $name (clone): $_" 'Red'; $failed++
        }
        continue
    }

    Push-Location $path
    try {
        $branch = (git rev-parse --abbrev-ref HEAD).Trim()
        $dirty  = @(git status --porcelain).Count
        git fetch origin -q 2>$null
        $counts = (git rev-list --left-right --count "origin/$branch...HEAD" 2>$null)
        $behind = 0; $ahead = 0
        if ($counts) { $parts = $counts -split '\s+'; $behind = [int]$parts[0]; $ahead = [int]$parts[1] }

        if ($dirty -ne 0 -or $ahead -ne 0) {
            Write-Line '[~]' "SKIP   $name (dirty=$dirty ahead=$ahead) - lokaal werk, niet aangeraakt" 'Yellow'
            $skipped++
        }
        elseif ($behind -ne 0) {
            git pull --ff-only -q 2>$null
            Write-Line '[v]' "PULL   $name (+$behind commits)" 'Green'; $pulled++
        }
        else {
            Write-Line '[=]' "OK     $name (up-to-date)" 'DarkGray'; $ok++
        }
    } catch {
        Write-Line '[!]' "FOUT   ${name}: $_" 'Red'; $failed++
    } finally {
        Pop-Location
    }
}

# --- Samenvatting ------------------------------------------------------------
$dur = [math]::Round(((Get-Date) - $started).TotalSeconds, 1)
$summary = "cloned=$cloned pulled=$pulled ok=$ok skipped=$skipped failed=$failed ({0}s)" -f $dur
Write-Host ""
Write-Line '==' "Klaar: $summary" 'Cyan'

"{0:yyyy-MM-dd HH:mm:ss}  {1}" -f $started, $summary | Add-Content -Path $log -Encoding utf8

if ($failed -gt 0) { exit 1 }
