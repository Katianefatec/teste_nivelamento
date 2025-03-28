<#
.SYNOPSIS
    Script para executar consultas SQL no MySQL a partir do PowerShell
.DESCRIPTION
    Executa arquivos SQL em sequência e mostra os resultados formatados
#>

param(
    [string]$senhaMySQL
)

# Configurações
$arquivos = "10OpMaiorDesp4T.sql", "10OpMaiorDespUltimoAno.sql"
$mysqlPath = "mysql" # Ou "C:\caminho\para\mysql\bin\mysql.exe"

foreach ($arquivo in $arquivos) {
    Write-Host "`n[EXECUTANDO: $arquivo]`n" -ForegroundColor Cyan
    
    # Verifica se o arquivo existe
    if (-not (Test-Path $arquivo)) {
        Write-Host "ERRO: Arquivo $arquivo não encontrado!" -ForegroundColor Red
        continue
    }

    # Lê o conteúdo do arquivo SQL
    try {
        $query = Get-Content -Path $arquivo -Raw -Encoding UTF8
    } catch {
        Write-Host "ERRO ao ler o arquivo $arquivo : $_" -ForegroundColor Red
        continue
    }

    # Executa a consulta no MySQL
    try {
        if ($senhaMySQL) {
            $result = & $mysqlPath -u root -p$senhaMySQL ans_db -e $query -t 2>&1
        } else {
            $result = & $mysqlPath -u root -p ans_db -e $query -t 2>&1
        }

        # Processa o resultado
        if ($result -match "Empty set") {
            Write-Host "AVISO: A consulta não retornou resultados." -ForegroundColor Yellow
            Write-Host "Considere verificar os filtros ou datas utilizadas." -ForegroundColor Yellow
        }
        elseif ($result -match "ERROR") {
            Write-Host "ERRO NA EXECUÇÃO:" -ForegroundColor Red
            $result
        }
        else {
            $result
        }
    }
    catch {
        Write-Host "ERRO FATAL ao executar a consulta: $_" -ForegroundColor Red
    }

    Write-Host "`n[FIM: $arquivo]`n" -ForegroundColor Cyan
    Write-Host ("-" * 80)
}