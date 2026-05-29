"""
Data model for shared state between threads.
Contains queues and current system data.
"""

import queue
import threading
from collections import deque

class DataModel:
    """Shared data model for the system monitor."""

    def __init__(self):
        # Queues for thread-safe data transfer
        self.data_queue = queue.Queue(maxsize=10)  # For latest data
        self.alert_queue = queue.Queue(maxsize=10)  # For alerts

        # Current data
        self.current_data = {
            'cpu_percent': 0.0,
            'cpu_per_core': [],
            'memory': {'total': 0, 'used': 0, 'available': 0, 'percent': 0.0},
            'disk': {'total': 0, 'used': 0, 'free': 0, 'percent': 0.0},
            'processes': [],
            'top_processes': [],
            'uptime': 0,
            'system_info': {}
        }

        # History for graphs (rolling windows)
        self.cpu_history = deque(maxlen=50)
        self.memory_history = deque(maxlen=50)

        # Alerts
        self.alerts = {
            'cpu_high': False,
            'memory_high': False
        }

        # Thread control
        self.running = threading.Event()
        self.running.set()

    def get_latest_data(self):
        """Get the latest data from the queue."""
        try:
            return self.data_queue.get_nowait()
        except queue.Empty:
            return None

    def put_data(self, data):
        """Put new data into the queue."""
        try:
            self.data_queue.put_nowait(data)
        except queue.Full:
            # Remove old data if queue is full
            try:
                self.data_queue.get_nowait()
                self.data_queue.put_nowait(data)
            except queue.Empty:
                pass

    def update_current_data(self, data):
        """Update the current data dictionary."""
        self.current_data.update(data)

        # Update history
        if 'cpu_percent' in data:
            self.cpu_history.append(data['cpu_percent'])
        if 'memory' in data and 'percent' in data['memory']:
            self.memory_history.append(data['memory']['percent'])

        # Check for alerts
        self.check_alerts(data)

    def check_alerts(self, data):
        """Check for alert conditions."""
        if 'cpu_percent' in data:
            cpu_high = data['cpu_percent'] > 80
            if cpu_high != self.alerts['cpu_high']:
                self.alerts['cpu_high'] = cpu_high
                self.alert_queue.put({'type': 'cpu', 'active': cpu_high})

        if 'memory' in data and 'percent' in data['memory']:
            mem_high = data['memory']['percent'] > 80
            if mem_high != self.alerts['memory_high']:
                self.alerts['memory_high'] = mem_high
                self.alert_queue.put({'type': 'memory', 'active': mem_high})

    def get_alert(self):
        """Get the latest alert from the queue."""
        try:
            return self.alert_queue.get_nowait()
        except queue.Empty:
            return None