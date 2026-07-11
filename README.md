# SysGuard — Windows Rendszermonitor

**Python alapú rendszermonitorozó eszköz, amely valós időben figyeli a CPU, RAM, lemez és hálózat használatot, és riasztást küld határértékek átlépésekor.**

## 📊 Leírás

A SysGuard egy könnyűsúlyú, konfigurálható rendszermonitor, amely:

- **CPU használat** figyelése (összesített és magonkénti)
- **RAM foglaltság** monitorozása
- **Lemez I/O** és szabad hely követése
- **Hálózati forgalom** mérése (küldött/fogadott bájtok)
- **Konfigurálható riasztások** — email értesítés határérték átlépéskor
- **JSON és log formátumú** metrika gyűjtés
- **Könnyű és erőforrás-takarékos** működés

## 📁 Fájlszerkezet

```
SysGuard/
├── sysguard.py                  # Teljes funkcionalitású monitor (318 sor)
├── sysguard_simple.py           # Egyszerűsített verzió
├── install.py                   # Telepítő szkript
├── config/
│   └── config.json              # Konfigurációs fájl
├── logs/
│   ├── sysguard_YYYYMMDD.log    # Rendszernaplók
│   └── metrics_YYYYMMDD.json    # Metrika adatok
├── start.bat                    # Windows indító (batch)
├── Start-SysGuard.ps1           # Windows indító (PowerShell)
└── README.md
```

## 🚀 Használat

### Telepítés

```bash
python install.py
```

### Indítás

```bash
# Teljes verzió
python sysguard.py

# PowerShell
.\Start-SysGuard.ps1

# Batch
start.bat
```

### Konfiguráció

A `config/config.json` fájlban állítható:

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

### Riasztási szintek

| Erőforrás | Figyelmeztetés | Kritikus | Alapértelmezett művelet |
|-----------|---------------|----------|------------------------|
| CPU | >80% | >90% | Email riasztás |
| RAM | >75% | >85% | Email riasztás |
| Lemez | >80% | >90% | Email riasztás |
| Hálózat | >500 MB/perc | >1000 MB/perc | Email riasztás |

## 📦 Függőségek

```bash
pip install psutil
```

- **Python 3.8+**
- **psutil** — rendszer erőforrások lekérdezése
- Standard library: `json`, `logging`, `smtplib`, `email`

## 📈 Kimenet formátumok

### Log fájl
```
2026-04-29 14:30:05 - SysGuard - INFO - Monitoring started
2026-04-29 14:30:10 - SysGuard - INFO - CPU: 45.2% | RAM: 62.1% | Disk: 34.8%
```

### JSON metrika
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

## ⚙️ Automatikus indítás

A rendszerrel együtt indítható:
1. `Windows + R` → `shell:startup`
2. Hozz létre egy parancsikont a `start.bat`-ra
