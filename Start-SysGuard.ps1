Write-Host "========================================" -ForegroundColor Cyan
Write-Host "       SysGuard System Monitor" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$choice = Read-Host "Choose an option:
1. Run full SysGuard (with logging)
2. Run simple monitor (console only)
3. Run demo (5 cycles)
4. Install dependencies
5. Exit

Enter choice (1-5)"

switch ($choice) {
    "1" {
        Write-Host "Starting SysGuard..." -ForegroundColor Green
        python sysguard.py
        Read-Host "`nPress Enter to continue"
    }
    "2" {
        Write-Host "Starting simple monitor..." -ForegroundColor Green
        python sysguard_simple.py
        Read-Host "`nPress Enter to continue"
    }
    "3" {
        Write-Host "Starting demo mode..." -ForegroundColor Green
        python sysguard_simple.py
        Read-Host "`nPress Enter to continue"
    }
    "4" {
        Write-Host "Installing dependencies..." -ForegroundColor Yellow
        python install.py
        Read-Host "`nPress Enter to continue"
    }
    "5" {
        Write-Host "Exiting..." -ForegroundColor Gray
        Start-Sleep -Seconds 2
    }
    default {
        Write-Host "Invalid choice!" -ForegroundColor Red
        Read-Host "`nPress Enter to continue"
    }
}