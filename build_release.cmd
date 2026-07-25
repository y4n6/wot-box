@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PY27=D:\02.registered programs\Python27\python.exe"
set "SCRIPT=%ROOT%tools\build_release.py"
set "OUTPUT=%ROOT%release\battle_efficiency_standalone.wotmod"

if not exist "%SCRIPT%" (
    echo [ERROR] Missing build script: "%SCRIPT%"
    pause
    exit /b 1
)

if exist "%PY27%" (
    echo [INFO] Using Python 2.7: "%PY27%"
    "%PY27%" "%SCRIPT%"
    goto after_run
)

echo [WARN] Python 2.7 not found at fixed path, trying py launcher...
py -2.7 "%SCRIPT%"

:after_run
if errorlevel 1 (
    echo.
    echo [ERROR] Build failed.
    pause
    exit /b 1
)

if exist "%OUTPUT%" (
    echo.
    echo [OK] Build finished.
    echo [OK] Output: "%OUTPUT%"
) else (
    echo.
    echo [ERROR] Build script finished but output file was not found: "%OUTPUT%"
    pause
    exit /b 1
)

echo.
pause
exit /b 0
