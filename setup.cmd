@echo off
setlocal
cd /d "%~dp0"

powershell.exe -NoProfile -NoExit -ExecutionPolicy Bypass -Command "Unblock-File -LiteralPath '%~dp0setup.ps1' -ErrorAction SilentlyContinue; . '%~dp0setup.ps1'"

endlocal
