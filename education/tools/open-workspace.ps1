param([ValidateSet('full','flash')][string]$Mode='full', [switch]$Offline, [switch]$NoOpen)
$ErrorActionPreference = 'Stop'
$taskEducationRoot = Split-Path -Parent $PSScriptRoot
$taskRepositoryRoot = Split-Path -Parent $taskEducationRoot
if ($Offline) { $Mode='flash' } # 旧参数兼容；Flash仍使用云API。
$taskFlash = $Mode -eq 'flash'
$taskPort = if ($env:QINGQI_PORT) { [int]$env:QINGQI_PORT } elseif ($taskFlash) { 18774 } else { 18772 }
$taskUrl = "http://127.0.0.1:$taskPort"
try {
    $taskHealth = Invoke-RestMethod "$taskUrl/api/health" -TimeoutSec 2
    if ($taskHealth.product -eq 'qingqi-education') { if (-not $NoOpen) { Start-Process $taskUrl }; exit 0 }
} catch { }
if (-not (Test-Path -LiteralPath (Join-Path $taskEducationRoot 'web/dist/index.html'))) {
    throw '前端尚未构建，请在仓库根目录运行 pnpm education:build。'
}
$taskPython = $env:QINGQI_PYTHON
if (-not $taskPython) {
    $taskBundledPython = Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
    if (Test-Path -LiteralPath $taskBundledPython) { $taskPython = $taskBundledPython }
    else { $taskPython = (Get-Command python -ErrorAction Stop).Source }
}
$taskModelsFile = Join-Path $taskEducationRoot 'service/config/models.local.json'
$taskPreviousKey = $env:EDU_GLM_API_KEY
$taskPreviousPath = $env:PYTHONPATH
$taskArguments = @()
try {
    if (-not $taskFlash -and (Test-Path -LiteralPath $taskModelsFile)) {
        $taskModels = Get-Content -LiteralPath $taskModelsFile -Raw | ConvertFrom-Json
        if ($taskModels.models.glm.enabled -and -not $env:EDU_GLM_API_KEY) {
            $taskSecureKey = Read-Host '请输入 GLM API Key（仅传给运行进程，不保存）' -AsSecureString
            $taskKeyPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($taskSecureKey)
            try { $env:EDU_GLM_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($taskKeyPointer) }
            finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($taskKeyPointer) }
        }
        $taskArguments = @('"' + (Join-Path $PSScriptRoot 'run_models.py') + '"')
    } else {
        $env:PYTHONPATH = Join-Path $taskEducationRoot 'service/src'
        $taskArguments = @('-m', 'qingqi.product', '--port', "$taskPort")
        $taskVisionFile = Join-Path $taskEducationRoot 'service/config/vision.local.json'
        if ($taskFlash -and (Test-Path -LiteralPath $taskVisionFile)) {
            $taskVision = Get-Content -LiteralPath $taskVisionFile -Raw | ConvertFrom-Json
            if ($taskVision.models.vision.enabled -and -not $env:EDU_GLM_API_KEY) {
                $taskSecureKey = Read-Host '请输入图片辅导的 GLM API Key（仅传给进程）' -AsSecureString
                $taskKeyPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($taskSecureKey)
                try { $env:EDU_GLM_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($taskKeyPointer) }
                finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($taskKeyPointer) }
            }
            # 数组中拼接路径要先求值；否则 PowerShell 会把空格一起传入文件名。
            $taskArguments += @('--config', ('"' + $taskVisionFile + '"'))
        }
        $taskAccounts = Join-Path $taskEducationRoot 'service/config/accounts.local.json'
        if (Test-Path -LiteralPath $taskAccounts) { $taskArguments += @('--accounts', ('"' + $taskAccounts + '"')) }
    }
    $taskRuns = Join-Path $taskEducationRoot 'service/runs'
    New-Item -ItemType Directory -Path $taskRuns -Force | Out-Null
    $taskProcess = Start-Process -FilePath $taskPython -ArgumentList $taskArguments -WorkingDirectory (Join-Path $taskEducationRoot 'service') -WindowStyle Hidden -RedirectStandardOutput (Join-Path $taskRuns 'launcher.stdout.local.log') -RedirectStandardError (Join-Path $taskRuns 'launcher.stderr.local.log') -PassThru
    @{pid=$taskProcess.Id; executable=$taskPython; root=$taskRepositoryRoot} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $taskRuns "launcher-$taskPort.local.json") -Encoding utf8
} finally {
    if ($null -eq $taskPreviousKey) { Remove-Item Env:EDU_GLM_API_KEY -ErrorAction SilentlyContinue } else { $env:EDU_GLM_API_KEY = $taskPreviousKey }
    if ($null -eq $taskPreviousPath) { Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue } else { $env:PYTHONPATH = $taskPreviousPath }
}
for ($taskAttempt = 0; $taskAttempt -lt 30; $taskAttempt++) {
    Start-Sleep -Milliseconds 1000
    try {
        $taskHealth = Invoke-RestMethod "$taskUrl/api/health" -TimeoutSec 2
        if ($taskHealth.product -eq 'qingqi-education') { if (-not $NoOpen) { Start-Process $taskUrl }; exit 0 }
    } catch { }
    if ($taskProcess.HasExited) { break }
}
throw '服务启动失败。请查看 education/service/runs/launcher.stderr.local.log。'
