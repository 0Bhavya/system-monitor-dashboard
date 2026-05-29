"""
Data collector thread for gathering system metrics.
Runs in background and pushes data to the shared model.
"""

import time
import threading
import psutil
from .data_model import DataModel

class DataCollector(threading.Thread):
    """Background thread for collecting system data."""

    def __init__(self, data_model: DataModel):
        super().__init__(daemon=True)
        self.data_model = data_model
        self.interval = 1.0  # Collect data every 1 second

    def run(self):
        """Main loop for data collection."""
        while self.data_model.running.is_set():
            try:
                data = self.collect_data()
                self.data_model.put_data(data)
                self.data_model.update_current_data(data)
            except Exception as e:
                print(f"Error in data collection: {e}")
            time.sleep(self.interval)

    def collect_data(self):
        """Collect all system metrics."""
        data = {}

        # CPU data
        data['cpu_percent'] = psutil.cpu_percent(interval=None)
        data['cpu_per_core'] = psutil.cpu_percent(percpu=True, interval=None)

        # Memory data
        memory = psutil.virtual_memory()
        data['memory'] = {
            'total': memory.total,
            'used': memory.used,
            'available': memory.available,
            'percent': memory.percent
        }

        # Disk data (root partition)
        disk = psutil.disk_usage('/')
        data['disk'] = {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent
        }

        # Processes data
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'][:50],  # Truncate long names
                        'cpu_percent': proc.info['cpu_percent'] or 0.0,
                        'memory_percent': proc.info['memory_percent'] or 0.0
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # Sort by CPU usage and take top 100 for performance
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            data['processes'] = processes[:100]

            # Top 5 processes
            data['top_processes'] = processes[:5]

        except Exception as e:
            print(f"Error collecting process data: {e}")
            data['processes'] = []
            data['top_processes'] = []

        # System info
        data['uptime'] = time.time() - psutil.boot_time()
        data['system_info'] = {
            'os': f"{psutil.os.uname().sysname} {psutil.os.uname().release}",
            'hostname': psutil.os.uname().nodename
        }

        return data