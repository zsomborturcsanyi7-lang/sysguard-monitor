import psutil
import time
import json
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from typing import Dict, Any, List

class SysGuard:
    def __init__(self, config_path: str = "config/config.json"):
        """Initialize SysGuard with configuration"""
        self.config_path = config_path
        self.config = self.load_config()
        self.setup_logging()
        self.logger = logging.getLogger("SysGuard")
        self.alert_history = []
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.create_default_config()
            return self.load_config()
        except json.JSONDecodeError as e:
            print(f"Config JSON error: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "system": {"monitor_interval_seconds": 30, "log_level": "INFO"},
            "thresholds": {
                "cpu_warning": 70, "cpu_critical": 90,
                "memory_warning": 75, "memory_critical": 90
            },
            "alerting": {"enabled": False}
        }
    
    def create_default_config(self):
        """Create default config file if missing"""
        default_config = self.get_default_config()
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        print(f"Created default config at {self.config_path}")
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        log_level = getattr(logging, self.config.get("system", {}).get("log_level", "INFO"))
        
        # Create logger
        logger = logging.getLogger("SysGuard")
        logger.setLevel(log_level)
        
        # Remove existing handlers
        logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
        
        # File handler
        log_file = os.path.join(log_dir, f"sysguard_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Collect all system metrics"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "cpu": {
                "percent": psutil.cpu_percent(interval=1),
                "cores": psutil.cpu_count(logical=False),
                "logical_cores": psutil.cpu_count(logical=True)
            },
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "percent": psutil.virtual_memory().percent,
                "used": psutil.virtual_memory().used
            },
            "disk": {},
            "network": {},
            "processes": len(psutil.pids())
        }
        
        # Disk usage for all partitions
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                metrics["disk"][partition.mountpoint] = {
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent
                }
            except Exception as e:
                self.logger.warning(f"Could not read disk {partition.mountpoint}: {e}")
        
        # Network I/O
        net_io = psutil.net_io_counters()
        metrics["network"] = {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv
        }
        
        return metrics
    
    def check_thresholds(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check metrics against thresholds and return alerts"""
        alerts = []
        thresholds = self.config.get("thresholds", {})
        
        # CPU check
        cpu_percent = metrics["cpu"]["percent"]
        if cpu_percent >= thresholds.get("cpu_critical", 90):
            alerts.append({
                "level": "CRITICAL",
                "component": "CPU",
                "message": f"CPU usage critical: {cpu_percent}%",
                "value": cpu_percent,
                "threshold": thresholds.get("cpu_critical", 90)
            })
        elif cpu_percent >= thresholds.get("cpu_warning", 70):
            alerts.append({
                "level": "WARNING",
                "component": "CPU",
                "message": f"CPU usage high: {cpu_percent}%",
                "value": cpu_percent,
                "threshold": thresholds.get("cpu_warning", 70)
            })
        
        # Memory check
        mem_percent = metrics["memory"]["percent"]
        if mem_percent >= thresholds.get("memory_critical", 90):
            alerts.append({
                "level": "CRITICAL",
                "component": "Memory",
                "message": f"Memory usage critical: {mem_percent}%",
                "value": mem_percent,
                "threshold": thresholds.get("memory_critical", 90)
            })
        elif mem_percent >= thresholds.get("memory_warning", 75):
            alerts.append({
                "level": "WARNING",
                "component": "Memory",
                "message": f"Memory usage high: {mem_percent}%",
                "value": mem_percent,
                "threshold": thresholds.get("memory_warning", 75)
            })
        
        # Disk check
        for mountpoint, disk_info in metrics["disk"].items():
            disk_percent = disk_info["percent"]
            if disk_percent >= thresholds.get("disk_critical", 95):
                alerts.append({
                    "level": "CRITICAL",
                    "component": f"Disk ({mountpoint})",
                    "message": f"Disk usage critical: {disk_percent}%",
                    "value": disk_percent,
                    "threshold": thresholds.get("disk_critical", 95)
                })
            elif disk_percent >= thresholds.get("disk_warning", 80):
                alerts.append({
                    "level": "WARNING",
                    "component": f"Disk ({mountpoint})",
                    "message": f"Disk usage high: {disk_percent}%",
                    "value": disk_percent,
                    "threshold": thresholds.get("disk_warning", 80)
                })
        
        return alerts
    
    def send_email_alert(self, alert: Dict[str, Any], metrics: Dict[str, Any]):
        """Send email alert"""
        try:
            email_config = self.config.get("alerting", {}).get("email", {})
            
            if not email_config.get("sender_email") or not email_config.get("sender_password"):
                self.logger.warning("Email configuration incomplete")
                return
            
            msg = MIMEMultipart()
            msg['From'] = email_config['sender_email']
            msg['To'] = ", ".join(email_config.get('recipient_emails', []))
            msg['Subject'] = f"[SysGuard {alert['level']}] {alert['component']} Alert"
            
            # Create email body
            body = f"""
            SysGuard Alert Notification
            ===========================
            
            Alert Level: {alert['level']}
            Component: {alert['component']}
            Message: {alert['message']}
            Time: {metrics['timestamp']}
            
            Current Metrics:
            - CPU Usage: {metrics['cpu']['percent']}%
            - Memory Usage: {metrics['memory']['percent']}%
            - Processes: {metrics['processes']}
            
            Threshold exceeded: {alert['value']}% > {alert['threshold']}%
            
            This is an automated message from SysGuard.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                server.starttls()
                server.login(email_config['sender_email'], email_config['sender_password'])
                server.send_message(msg)
            
            self.logger.info(f"Email alert sent for {alert['component']}")
            
        except Exception as e:
            self.logger.error(f"Failed to send email alert: {e}")
    
    def log_metrics(self, metrics: Dict[str, Any]):
        """Log metrics to file"""
        log_file = os.path.join("logs", f"metrics_{datetime.now().strftime('%Y%m%d')}.json")
        
        # Read existing logs
        logs = []
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
        
        # Add new metrics
        logs.append(metrics)
        
        # Keep only last 1000 entries
        if len(logs) > 1000:
            logs = logs[-1000:]
        
        # Write back
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def run_monitoring_cycle(self):
        """Run one monitoring cycle"""
        self.logger.info("Starting monitoring cycle")
        
        # Get metrics
        metrics = self.get_system_metrics()
        
        # Log metrics
        self.log_metrics(metrics)
        
        # Check thresholds
        alerts = self.check_thresholds(metrics)
        
        # Process alerts
        for alert in alerts:
            self.logger.warning(f"Alert: {alert['level']} - {alert['message']}")
            
            # Send email if alerting enabled
            if self.config.get("alerting", {}).get("enabled", False):
                self.send_email_alert(alert, metrics)
            
            # Add to history
            self.alert_history.append({
                "timestamp": metrics["timestamp"],
                "alert": alert
            })
        
        # Log summary
        self.logger.info(f"Cycle complete. Metrics collected: CPU={metrics['cpu']['percent']}%, "
                        f"Memory={metrics['memory']['percent']}%, Alerts={len(alerts)}")
        
        return metrics, alerts
    
    def start(self):
        """Start continuous monitoring"""
        self.logger.info("SysGuard starting...")
        self.logger.info(f"Configuration loaded from {self.config_path}")
        
        interval = self.config.get("system", {}).get("monitor_interval_seconds", 30)
        
        try:
            while True:
                self.run_monitoring_cycle()
                self.logger.info(f"Sleeping for {interval} seconds")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.logger.info("SysGuard stopped by user")
        except Exception as e:
            self.logger.error(f"Fatal error: {e}")
            raise

def main():
    """Main entry point"""
    guard = SysGuard()
    guard.start()

if __name__ == "__main__":
    main()