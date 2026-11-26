@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0education\tools\stop-workspace.ps1"
if errorlevel 1 pause
