@echo off
REM Dubbelklik om de security-commons-nl org te syncen (pull-only, veilig).
cd /d "%~dp0"
where pwsh >nul 2>nul
if %errorlevel%==0 (
    pwsh -ExecutionPolicy Bypass -File "%~dp0sync-org.ps1"
) else (
    powershell -ExecutionPolicy Bypass -File "%~dp0sync-org.ps1"
)
echo.
pause
