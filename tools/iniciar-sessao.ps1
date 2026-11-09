# Inicia uma sessão de trabalho documentada.
#   .\tools\iniciar-sessao.ps1
#
# - Grava TUDO o que aparece neste terminal em .privado/terminal/AAAA-MM-DD_HHMM.txt
#   (bruto, com caminhos e nomes reais: por isso fica fora do git).
# - Ativa o ambiente virtual do projeto.
# - Cria o diário do dia, se ainda não existir.
# Para encerrar a gravação: Stop-Transcript (ou feche o terminal).

$root = Split-Path -Parent $PSScriptRoot
$stamp = Get-Date -Format "yyyy-MM-dd_HHmm"
$today = Get-Date -Format "yyyy-MM-dd"

$logDir = Join-Path $root ".privado\terminal"
New-Item -ItemType Directory -Force $logDir | Out-Null
Start-Transcript -Path (Join-Path $logDir "$stamp.txt") -Append | Out-Null

$venv = Join-Path $root ".venv\Scripts\Activate.ps1"
if (Test-Path $venv) { . $venv }

$diarioDir = Join-Path $root "docs\diario"
$existente = Get-ChildItem $diarioDir -Filter "$today*.md" -ErrorAction SilentlyContinue
if (-not $existente) {
    $n = (Get-ChildItem $diarioDir -Filter "*.md" -ErrorAction SilentlyContinue | Measure-Object).Count
    $arquivo = Join-Path $diarioDir ("{0}_dia-{1:D2}.md" -f $today, $n)
    @"
# Dia $('{0:D2}' -f $n) · $today

**Fase:**
**Duração:**

## Objetivo da sessão


## O que foi feito


## Resultados e números


## Problemas e como resolvi


## Prints
<!-- ![descrição](../prints/$today`_fase-N_descricao.png) -->

## Próximos passos
- [ ]
"@ | Set-Content -Encoding utf8 $arquivo
    Write-Host "Diário criado: docs\diario\$(Split-Path -Leaf $arquivo)" -ForegroundColor Cyan
}

Write-Host "Sessão gravada em .privado\terminal\$stamp.txt  (Stop-Transcript para encerrar)" -ForegroundColor Green
