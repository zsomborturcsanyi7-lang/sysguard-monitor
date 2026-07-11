import psutil
import time
import json
from datetime import datetime
import os

def get_system_info():
    """Get basic system information"""
    info = {
        "timestamp": datetime.now().isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "memory_used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
        "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "disk_usage": {},
        "process_count": len(psutil.pids()),
        "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat()
    }
    
    # Get disk usage for C: drive
    try:
        disk = psutil.disk_usage('C:\\')
        info["disk_usage"]["C:"] = {
            "percent": disk.percent,
            "free_gb": round(disk.free / (1024**3), 2),
            "total_gb": round(disk.total / (1024**3), 2)
        }
    except:
        info["disk_usage"]["C:"] = {"error": "Could not read"}
    
    return info

def monitor_system(interval=10, max_cycles=None):
    """Monitor system with simple console output"""
    print("=" * 50)
    print("SysGuard Simple Monitor")
    print("=" * 50)
    print(f"Starting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Interval: {interval} seconds")
    print("=" * 50)
    
    cycle_count = 0
    
    try:
        while True:
            if max_cycles and cycle_count >= max_cycles:
                print(f"\nReached max cycles ({max_cycles}), stopping.")
                break
                
            info = get_system_info()
            
            # Display info
            print(f"\n[{info['timestamp']}]")
            print(f"  CPU: {info['cpu_percent']:5.1f}%")
            print(f"  RAM: {info['memory_percent']:5.1f}% ({info['memory_used_gb']} GB / {info['memory_total_gb']} GB)")
            
            if "C:" in info["disk_usage"]:
                disk = info["disk_usage"]["C:"]
                if "percent" in disk:
                    print(f"  Disk C:: {disk['percent']:5.1f}% (Free: {disk['free_gb']} GB)")
            
            print(f"  Processes: {info['process_count']}")
            
            # Check thresholds
            warnings = []
            if info['cpu_percent'] > 80:
                warnings.append(f"CPU high: {info['cpu_percent']}%")
            if info['memory_percent'] > 80:
                warnings.append(f"Memory high: {info['memory_percent']}%")
            
            if warnings:
                print(f"  ⚠️  Warnings: {', '.join(warnings)}")
            
            cycle_count += 1
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print(f"\n\nMonitoring stopped after {cycle_count} cycles.")
        print(f"Stopped at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    # Run for 5 cycles with 5 second intervals (demo mode)
    monitor_system(interval=5, max_cycles=5)