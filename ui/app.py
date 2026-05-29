"""
Main application class using customtkinter.
"""

import customtkinter as ctk
from .dashboard import DashboardPage
from .process_page import ProcessPage
from .analytics import AnalyticsPage
from core.data_collector import DataCollector
from core.data_model import DataModel

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SystemMonitorApp:
    """Main application class."""

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("System Monitor Dashboard")
        self.root.geometry("1200x800")

        # Data model and collector
        self.data_model = DataModel()
        self.data_collector = DataCollector(self.data_model)
        self.data_collector.start()

        # UI components
        self.sidebar = ctk.CTkFrame(self.root, width=200)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        self.content = ctk.CTkFrame(self.root)
        self.content.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Sidebar buttons
        self.dashboard_btn = ctk.CTkButton(
            self.sidebar, text="Dashboard", command=self.show_dashboard
        )
        self.dashboard_btn.pack(pady=10, padx=10, fill="x")

        self.process_btn = ctk.CTkButton(
            self.sidebar, text="Processes", command=self.show_processes
        )
        self.process_btn.pack(pady=10, padx=10, fill="x")

        self.analytics_btn = ctk.CTkButton(
            self.sidebar, text="Analytics", command=self.show_analytics
        )
        self.analytics_btn.pack(pady=10, padx=10, fill="x")

        # Pages
        self.pages = {}
        self.current_page = None

        # Initialize pages
        self.pages['dashboard'] = DashboardPage(self.content, self.data_model)
        self.pages['processes'] = ProcessPage(self.content, self.data_model)
        self.pages['analytics'] = AnalyticsPage(self.content, self.data_model)

        # Start UI updates
        self.update_ui()

        # Show default page
        self.show_dashboard()

    def show_dashboard(self):
        self._switch_page('dashboard')

    def show_processes(self):
        self._switch_page('processes')

    def show_analytics(self):
        self._switch_page('analytics')

    def _switch_page(self, page_name):
        if self.current_page:
            self.current_page.hide()
        self.current_page = self.pages[page_name]
        self.current_page.show()

    def update_ui(self):
        """Update UI with latest data."""
        # Get latest data
        data = self.data_model.get_latest_data()
        if data:
            # Update current page
            if self.current_page:
                self.current_page.update(data)

            # Check for alerts
            alert = self.data_model.get_alert()
            if alert:
                self._handle_alert(alert)

        # Schedule next update
        self.root.after(1000, self.update_ui)

    def _handle_alert(self, alert):
        """Handle alert notifications."""
        if alert['type'] == 'cpu' and alert['active']:
            print("ALERT: High CPU usage!")
        elif alert['type'] == 'memory' and alert['active']:
            print("ALERT: High memory usage!")

    def run(self):
        """Start the application."""
        self.root.mainloop()

        # Cleanup
        self.data_model.running.clear()
        self.data_collector.join()