"""
Dashboard page with system metrics and graphs.
"""

import customtkinter as ctk
from graphs.graph_manager import GraphManager
from utils.system_utils import format_bytes, format_uptime, get_system_insights

class DashboardPage:
    """Dashboard page showing system overview."""

    def __init__(self, parent, data_model):
        self.parent = parent
        self.data_model = data_model
        self.frame = ctk.CTkFrame(parent)

        # Create widgets
        self._create_widgets()

    def _create_widgets(self):
        """Create all dashboard widgets."""
        # Title
        title = ctk.CTkLabel(self.frame, text="System Dashboard", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=10)

        # Metrics cards
        self.metrics_frame = ctk.CTkFrame(self.frame)
        self.metrics_frame.pack(fill="x", padx=10, pady=5)

        # CPU card
        self.cpu_frame = ctk.CTkFrame(self.metrics_frame)
        self.cpu_frame.pack(side="left", fill="both", expand=True, padx=5)
        ctk.CTkLabel(self.cpu_frame, text="CPU Usage").pack()
        self.cpu_label = ctk.CTkLabel(self.cpu_frame, text="0%", font=ctk.CTkFont(size=24))
        self.cpu_label.pack()

        # Memory card
        self.mem_frame = ctk.CTkFrame(self.metrics_frame)
        self.mem_frame.pack(side="left", fill="both", expand=True, padx=5)
        ctk.CTkLabel(self.mem_frame, text="Memory Usage").pack()
        self.mem_label = ctk.CTkLabel(self.mem_frame, text="0%", font=ctk.CTkFont(size=24))
        self.mem_label.pack()

        # Disk card
        self.disk_frame = ctk.CTkFrame(self.metrics_frame)
        self.disk_frame.pack(side="left", fill="both", expand=True, padx=5)
        ctk.CTkLabel(self.disk_frame, text="Disk Usage").pack()
        self.disk_label = ctk.CTkLabel(self.disk_frame, text="0%", font=ctk.CTkFont(size=24))
        self.disk_label.pack()

        # Alerts
        self.alert_frame = ctk.CTkFrame(self.frame)
        self.alert_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(self.alert_frame, text="Alerts").pack()
        self.alert_label = ctk.CTkLabel(self.alert_frame, text="No alerts", text_color="green")
        self.alert_label.pack()

        # Graphs
        self.graph_frame = ctk.CTkFrame(self.frame)
        self.graph_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.graph_manager = GraphManager(self.graph_frame)

        # System info
        self.info_frame = ctk.CTkFrame(self.frame)
        self.info_frame.pack(fill="x", padx=10, pady=5)
        self.uptime_label = ctk.CTkLabel(self.info_frame, text="Uptime: 0")
        self.uptime_label.pack(side="left", padx=10)
        self.os_label = ctk.CTkLabel(self.info_frame, text="OS: Unknown")
        self.os_label.pack(side="left", padx=10)

        # Insights
        self.insights_label = ctk.CTkLabel(self.frame, text="Insights: System running normally")
        self.insights_label.pack(pady=5)

    def show(self):
        """Show the dashboard page."""
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        """Hide the dashboard page."""
        self.frame.pack_forget()

    def update(self, data):
        """Update dashboard with new data."""
        # Update metrics
        if 'cpu_percent' in data:
            self.cpu_label.configure(text=f"{data['cpu_percent']:.1f}%")

        if 'memory' in data:
            mem = data['memory']
            self.mem_label.configure(text=f"{mem['percent']:.1f}%")

        if 'disk' in data:
            disk = data['disk']
            self.disk_label.configure(text=f"{disk['percent']:.1f}%")

        # Update alerts
        cpu_percent = data.get('cpu_percent', 0)
        memory_percent = data.get('memory', {}).get('percent', 0)

        if cpu_percent > 80:
            alert_text = "⚠ High CPU Usage"
            alert_color = "red"
        elif memory_percent > 80:
            alert_text = "⚠ High Memory Usage"
            alert_color = "red"
        else:
            alert_text = "System running normally"
            alert_color = "green"

        self.alert_label.configure(text=alert_text, text_color=alert_color)

        # Update graphs
        self.graph_manager.update_data(self.data_model.cpu_history, self.data_model.memory_history)

        # Update system info
        if 'uptime' in data:
            self.uptime_label.configure(text=f"Uptime: {format_uptime(data['uptime'])}")

        if 'system_info' in data:
            self.os_label.configure(text=f"OS: {data['system_info']['os']}")

        # Update insights
        insights = get_system_insights(data)
        self.insights_label.configure(text=f"Insights: {insights[0]}")