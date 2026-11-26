param([int]$Port = 18772)
$ErrorActionPreference = 'Stop'
$taskState = Join-Path (Split-Path -Parent $PSScriptRoot) "service/runs/launcher-$Port.local.json"
if (-not (Test-Path -LiteralPath $taskState)) { Write-Output '没有由双击启动器记录的服务。'; exit 0 }
$taskRecord = Get-Content -LiteralPath $taskState -Raw | ConvertFrom-Json
$taskAllProcesses = Get-CimInstance Win32_Process
$taskRootProcess = $taskAllProcesses | Where-Object ProcessId -eq $taskRecord.pid
if (-not $taskRootProcess) { Write-Output '服务已停止。'; exit 0 }
if ($taskRootProcess.ExecutablePath -ne $taskRecord.executable -or ($taskRootProcess.CommandLine -notmatch 'qingqi.product|run_models.py')) { throw '记录的进程身份已变化，拒绝停止。' }
function Stop-TaskChildren([int]$TaskParentId) {
    foreach ($taskChild in ($taskAllProcesses | Where-Object ParentProcessId -eq $TaskParentId)) {
        Stop-TaskChildren -TaskParentId $taskChild.ProcessId
        Stop-Process -Id $taskChild.ProcessId -Force -ErrorAction SilentlyContinue
    }
}
Stop-TaskChildren -TaskParentId $taskRootProcess.ProcessId
Stop-Process -Id $taskRootProcess.ProcessId -Force -ErrorAction SilentlyContinue
Write-Output '已停止本机教育服务和它创建的隧道。'
