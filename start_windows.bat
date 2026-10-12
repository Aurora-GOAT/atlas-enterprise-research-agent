@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_CMD=py -3"
) else (
    set "PYTHON_CMD=python"
)
if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Creating Python environment...
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 goto fail
)
echo [2/3] Installing required Python packages...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto fail
echo [3/3] Starting Atlas on http://127.0.0.1:8000
start "" http://127.0.0.1:8000
".venv\Scripts\python.exe" run.py
exit /b 0
:fail
echo Setup failed. Confirm Python 3.11+ is installed from python.org and retry.
pause
exit /b 1
