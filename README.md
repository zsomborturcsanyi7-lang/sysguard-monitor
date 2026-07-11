# SysGuard - System Monitoring and Alerting Tool

![SysGuard Logo](https://img.shields.io/badge/SysGuard-System%20Monitor-blue)
![Python](https://img.shields.io/badge/Python-3.7%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

SysGuard is an automated system monitoring tool that tracks CPU, memory, disk, network usage, and running processes. It provides real-time alerts when system resources exceed configured thresholds.

## Features

- **Real-time Monitoring**: CPU, Memory, Disk, Network, Processes
- **Configurable Thresholds**: Set warning and critical levels
- **Email Alerts**: Get notified when issues occur
- **JSON Logging**: All metrics saved in structured format
- **Simple CLI**: Easy-to-use command line interface
- **Extensible**: Modular design for adding new monitors

## Quick Start

### 1. Installation

```bash
# Clone or extract to your desktop
cd C:\Users\iga\Desktop\SysGuard

# Install dependencies
python install.py
```

### 2. Configuration

Edit `config/config.json` to set your thresholds and alert settings:

```json
{
  "system": {
    "monitor_interval_seconds": 30,
    "log_level": "INFO"
  },
  "thresholds": {
    "cpu_warning": 70,
    "cpu_critical": 90,
    "memory_warning": 75,
    "memory_critical": 90
  }
}
```

For email alerts, configure the `alerting` section with your SMTP settings.

### 3. Running

**Full version (with logging and alerts):**
```bash
python sysguard.py
```

**Simple version (console output only):**
```bash
python sysguard_simple.py
```

**Demo mode (run 5 cycles):**
```bash
python sysguard_simple.py
```

## Project Structure

```
SysGuard/
├── config/
│   └── config.json          # Configuration file
├── logs/                    # Log files directory
├── modules/                 # Future module extensions
├── tests/                   # Test files
├── sysguard.py             # Main monitoring application
├── sysguard_simple.py      # Simplified version
├── install.py              # Installation script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Configuration Options

### System Settings
- `monitor_interval_seconds`: How often to check metrics (default: 30)
- `log_level`: Logging level (DEBUG, INFO, WARNING, ERROR)

### Thresholds
- `cpu_warning/cpu_critical`: CPU usage percentages
- `memory_warning/memory_critical`: Memory usage percentages
- `disk_warning/disk_critical`: Disk usage percentages

### Alerting
- `enabled`: Enable/disable alerts
- `email`: SMTP configuration for email alerts
- `telegram`: Telegram bot configuration (future)

## Example Output

```
2025-03-06 17:30:00 - SysGuard - INFO - Starting monitoring cycle
2025-03-06 17:30:01 - SysGuard - INFO - CPU: 45.2%, Memory: 67.8%, Processes: 142
2025-03-06 17:30:01 - SysGuard - WARNING - Memory usage high: 67.8%
2025-03-06 17:30:01 - SysGuard - INFO - Cycle complete. Alerts: 1
```

## Requirements

- Python 3.7 or higher
- psutil library
- Internet connection (for email alerts)

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues or questions:
1. Check the logs in `logs/` directory
2. Review configuration in `config/config.json`
3. Open an issue on GitHub

---

**Note**: This tool is for monitoring purposes only. Always test in a safe environment before deploying to production systems.