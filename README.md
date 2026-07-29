# sysguard-monitor

Windows system resource monitoring application with automated email alerts.

## Overview & Purpose
sysguard-monitor tracks real-time Windows system metrics including CPU utilization, RAM consumption, disk space, and network interface activity, sending automated notifications upon threshold exceedance.

## Key Features
- Low-overhead system resource polling via `psutil`.
- Configurable threshold limits for CPU, RAM, and Disk space.
- Automated email alert dispatcher.
- JSON-formatted performance logging.

## Tech Stack & Dependencies
- **Languages**: Python, Go
- **Libraries**: `psutil`, `requests`

## Project Structure
```text
sysguard-monitor/
├── monitor.py
├── sysguard.go
├── config.json
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.9+ or Go 1.20+

### Steps
```bash
git clone https://github.com/zsomborturcsanyi7-lang/sysguard-monitor.git
cd sysguard-monitor
python monitor.py
```

## Usage Examples
```bash
python monitor.py --config config.json
```

## Status & License
Status: Functional Application.
License: MIT
