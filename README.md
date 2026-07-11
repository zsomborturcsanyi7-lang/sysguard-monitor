# SysGuard — Windows System Monitor

**A Python-based system monitoring tool that tracks CPU, RAM, disk, and network usage in real time and sends alerts when thresholds are exceeded.**

## 📊 Description

SysGuard is a lightweight, configurable system monitor that:

- Monitors **CPU usage** (aggregate and per-core)
- Tracks **RAM utilization**
- Monitors **disk I/O** and free space
- Measures **network traffic** (bytes sent/received)
- Provides **configurable alerts** — email notification on threshold breaches
- Collects metrics in **JSON and log formats**
- Operates with a **lightweight and resource-efficient** footprint

## 📁 File Structure

```
SysGuard/
├── sysguard.py                  # Full-featured monitor (318 lines)
├── sysguard_simple.py           # Simplified version
├── install.py                   # Installer script
├── config/
│   └── config.json              # Configuration file
├── logs/
│   ├── sysguard_YYYYMMDD.log    # System logs
│   └── metrics_YYYYMMDD.json    # Metric data
├── start.bat                    # Windows launcher (batch)
├── Start-SysGuard.ps1           # Windows launcher (PowerShell)
└── README.md
```

## 🚀 Usage

### Installation

```bash
python install.py
```

### Starting

```bash
# Full version
python sysguard.py

# PowerShell
.\Start-SysGuard.ps1

# Batch
start.bat
```

### Configuration

The following can be set in `config/config.json`:

```json
{
  "monitoring_interval": 5,
  "cpu_threshold": 90,
  "memory_threshold": 85,
  "disk_threshold": 90,
  "network_alert_mb": 1000,
  "email_alerts": {
    "enabled": false,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "from_email": "",
    "to_email": ""
  },
  "log_retention_days": 30
}
```

### Alert Levels

| Resource | Warning | Critical | Default Action |
|----------|---------|----------|----------------|
| CPU | >80% | >90% | Email alert |
| RAM | >75% | >85% | Email alert |
| Disk | >80% | >90% | Email alert |
| Network | >500 MB/min | >1000 MB/min | Email alert |

## 📦 Dependencies

```bash
pip install psutil
```

- **Python 3.8+**
- **psutil** — system resource queries
- Standard library: `json`, `logging`, `smtplib`, `email`

## 📈 Output Formats

### Log file
```
2026-04-29 14:30:05 - SysGuard - INFO - Monitoring started
2026-04-29 14:30:10 - SysGuard - INFO - CPU: 45.2% | RAM: 62.1% | Disk: 34.8%
```

### JSON metrics
```json
{
  "timestamp": "2026-04-29T14:30:10",
  "cpu_percent": 45.2,
  "memory_percent": 62.1,
  "disk_percent": 34.8,
  "network_sent_mb": 12.5,
  "network_recv_mb": 8.3
}
```

## ⚙️ Auto-start

Can be launched with the system:
1. `Windows + R` → `shell:startup`
2. Create a shortcut to `start.bat`

## Author
Zsombi & Hermes Agent (Nous Research)
