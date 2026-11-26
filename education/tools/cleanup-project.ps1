param([switch]$Apply)
$ErrorActionPreference='Stop'
$taskRepo=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..')).TrimEnd('\','/')
$taskArchive=[IO.Path]::GetFullPath((Join-Path (Split-Path $taskRepo -Parent) 'QingQi-ZCode-archive/2026-11-24-solid-review'))
$taskReports=Join-Path $taskRepo 'education/.local/reports'
function Assert-TaskPath([string]$Path,[string]$Root) {
    $taskResolved=[IO.Path]::GetFullPath($Path)
    if (-not $taskResolved.StartsWith($Root.TrimEnd('\','/')+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) { throw "路径越界，拒绝操作：$taskResolved" }
    return $taskResolved
}
function Move-TaskFile([string]$Source,[string]$Destination,[string]$DestinationRoot) {
    $taskSourcePath=Assert-TaskPath $Source $taskRepo
    $taskDestPath=Assert-TaskPath $Destination $DestinationRoot
    $taskSourceItem=Get-Item -LiteralPath $taskSourcePath -Force
    if ($taskSourceItem.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "保留重解析点：$taskSourcePath" }
    if ($taskSourceItem.PSIsContainer -and (Get-ChildItem -LiteralPath $taskSourcePath -Recurse -Force | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint } | Select-Object -First 1)) { throw "保留含重解析点的目录：$taskSourcePath" }
    New-Item -ItemType Directory -Path (Split-Path $taskDestPath -Parent) -Force | Out-Null
    if (Test-Path -LiteralPath $taskDestPath) { throw "归档目标已存在，保留原文件：$taskDestPath" }
    Move-Item -LiteralPath $taskSourcePath -Destination $taskDestPath
}
$taskKeepReports=@('scoped-stream-review-v1.md','curve-first-review-v1.md','runtime-reuse-review.md')
$taskKeepTmp=@('node24','pnpm10','restart-visual-product.local.py','run-visual-live.local.py')
$taskDeleteDirs=@()
foreach ($taskDirectory in Get-ChildItem -LiteralPath (Join-Path $taskRepo 'education/service/runs') -Directory -Force) {
    if ($taskDirectory.Name -match 'acceptance|tests|profiling|probe|browser|adaptive-seed|four-features|source-reuse|routing_tests|system-review|tutoring-evolution-numeric|project-audit') { $taskDeleteDirs += $taskDirectory.FullName }
}
foreach ($taskSourceDir in @('education/service/src','education/service/tests','education/tests','education/tools','education/server')) {
    if (-not (Test-Path -LiteralPath (Join-Path $taskRepo $taskSourceDir))) { continue }
    $taskDeleteDirs += @(Get-ChildItem -LiteralPath (Join-Path $taskRepo $taskSourceDir) -Directory -Recurse -Force | Where-Object { $_.Name -eq '__pycache__' } | Select-Object -ExpandProperty FullName)
}
foreach ($taskCache in @('.pytest_cache','education/service/.pytest_cache','education/plugin')) {
    $taskPath=Join-Path $taskRepo $taskCache
    if (Test-Path -LiteralPath $taskPath) { $taskDeleteDirs += $taskPath }
}
$taskDeleteDirs=@($taskDeleteDirs | Sort-Object -Unique | Where-Object { $taskCandidate=$_; -not ($taskDeleteDirs | Where-Object { $_ -ne $taskCandidate -and $taskCandidate.StartsWith($_.TrimEnd('\')+'\',[StringComparison]::OrdinalIgnoreCase) }) })
$taskPlan=@()
foreach ($taskPath in $taskDeleteDirs) {
    [void](Assert-TaskPath $taskPath $taskRepo)
    if ($taskPath -eq (Join-Path $taskRepo 'education/plugin') -and (Get-ChildItem -LiteralPath $taskPath -Force | Measure-Object).Count -ne 0) { continue }
    if ((Get-Item -LiteralPath $taskPath -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) { continue }
    if (Get-ChildItem -LiteralPath $taskPath -Recurse -Force | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint } | Select-Object -First 1) { continue }
    $taskFiles=@(Get-ChildItem -LiteralPath $taskPath -Recurse -File -Force)
    $taskPlan += [pscustomobject]@{action='remove-reproducible';source=$taskPath;files=$taskFiles.Count;bytes=($taskFiles | Measure-Object Length -Sum).Sum}
}
foreach ($taskFile in Get-ChildItem -LiteralPath (Join-Path $taskRepo 'education/reports') -File -Force) {
    if ($taskKeepReports -contains $taskFile.Name -or $taskFile.Name -eq 'README.md') { continue }
    $taskTarget=Join-Path $taskArchive ('reports/'+$taskFile.Name)
    $taskPlan += [pscustomobject]@{action='archive-report';source=$taskFile.FullName;destination=$taskTarget;bytes=$taskFile.Length}
}
foreach ($taskDirectory in Get-ChildItem -LiteralPath (Join-Path $taskRepo 'education/reports') -Directory -Force) {
    $taskPlan += [pscustomobject]@{action='archive-report';source=$taskDirectory.FullName;destination=(Join-Path $taskArchive ('reports/'+$taskDirectory.Name))}
}
if (Test-Path -LiteralPath (Join-Path $taskRepo 'education/plugin-workspace.local')) {
    $taskPlan += [pscustomobject]@{action='archive-retired';source=(Join-Path $taskRepo 'education/plugin-workspace.local');destination=(Join-Path $taskArchive 'education/plugin-workspace.local')}
}
if (Test-Path -LiteralPath (Join-Path $taskRepo 'education/docs/legacy-readme.md')) {
    $taskPlan += [pscustomobject]@{action='archive-document';source=(Join-Path $taskRepo 'education/docs/legacy-readme.md');destination=(Join-Path $taskArchive 'education/legacy-readme.md')}
}
foreach ($taskEntry in Get-ChildItem -LiteralPath (Join-Path $taskRepo 'tmp') -Force) {
    if ($taskKeepTmp -contains $taskEntry.Name) { continue }
    $taskPlan += [pscustomobject]@{action='archive-temporary';source=$taskEntry.FullName;destination=(Join-Path $taskArchive ('tmp/'+$taskEntry.Name))}
}
New-Item -ItemType Directory -Path $taskReports -Force | Out-Null
$taskManifest=Join-Path $taskReports 'project-cleanup-plan.local.json'
[IO.File]::WriteAllText($taskManifest,($taskPlan | ConvertTo-Json -Depth 5),[Text.UTF8Encoding]::new($false))
if (-not $Apply) { Write-Output (@{planned=$taskPlan.Count;reproducible_mb=[Math]::Round((($taskPlan | Where-Object action -eq 'remove-reproducible' | Measure-Object bytes -Sum).Sum)/1MB,1);manifest=$taskManifest} | ConvertTo-Json -Compress); exit 0 }
$taskResults=@()
foreach ($taskOperation in $taskPlan) {
    try {
        if ($taskOperation.action -eq 'remove-reproducible') {
            $taskResolved=Assert-TaskPath $taskOperation.source $taskRepo
            # 已确认绝对目标位于当前仓库，且没有重解析点；只删除明确可重建的测试/缓存目录。
            Remove-Item -LiteralPath $taskResolved -Recurse -Force
        } else {
            $taskDestinationRoot=if ($taskOperation.destination.StartsWith($taskArchive,[StringComparison]::OrdinalIgnoreCase)) {$taskArchive} else {$taskRepo}
            Move-TaskFile $taskOperation.source $taskOperation.destination $taskDestinationRoot
        }
        $taskResults += [pscustomobject]@{action=$taskOperation.action;source=$taskOperation.source;status='completed'}
    } catch { $taskResults += [pscustomobject]@{action=$taskOperation.action;source=$taskOperation.source;status='preserved';reason=$_.Exception.Message} }
}
[IO.File]::WriteAllText((Join-Path $taskReports 'project-cleanup-result.local.json'),($taskResults | ConvertTo-Json -Depth 5),[Text.UTF8Encoding]::new($false))
Write-Output (@{completed=@($taskResults | Where-Object status -eq 'completed').Count;preserved=@($taskResults | Where-Object status -eq 'preserved').Count;archive=$taskArchive} | ConvertTo-Json -Compress)
