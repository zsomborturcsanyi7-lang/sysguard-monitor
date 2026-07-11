@echo off
echo ========================================
echo        SysGuard System Monitor
echo ========================================
echo.
echo Choose an option:
echo 1. Run full SysGuard (with logging)
echo 2. Run simple monitor (console only)
echo 3. Run demo (5 cycles)
echo 4. Install dependencies
echo 5. Exit
echo.

set /p choice="Enter choice (1-5): "

if "%choice%"=="1" (
    echo Starting SysGuard...
    python sysguard.py
    pause
) else if "%choice%"=="2" (
    echo Starting simple monitor...
    python sysguard_simple.py
    pause
) else if "%choice%"=="3" (
    echo Starting demo mode...
    python sysguard_simple.py
    pause
) else if "%choice%"=="4" (
    echo Installing dependencies...
    python install.py
    pause
) else if "%choice%"=="5" (
    echo Exiting...
    timeout /t 2 >nul
) else (
    echo Invalid choice!
    pause
)