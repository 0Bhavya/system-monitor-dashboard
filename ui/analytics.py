"""
Analytics page with trends and insights.
"""

import customtkinter as ctk
from utils.system_utils import get_system_insights

class AnalyticsPage:
    """Analytics page showing trends and insights."""

    def __init__(self, parent, data_model):
        self.parent = parent
        self.data_model = data_model
        self.frame = ctk.CTkFrame(parent)

        # Create widgets
        self._create_widgets()

    def _create_widgets(self):
        """Create analytics widgets."""
        # Title
        title = ctk.CTkLabel(self.frame, text="System Analytics", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=10)

        # Trends section
        self.trends_frame = ctk.CTkFrame(self.frame)
        self.trends_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.trends_frame, text="Performance Trends", font=ctk.CTkFont(weight="bold")).pack()

        self.cpu_trend_label = ctk.CTkLabel(self.trends_frame, text="CPU Trend: Stable")
        self.cpu_trend_label.pack(anchor="w", pady=2)

        self.mem_trend_label = ctk.CTkLabel(self.trends_frame, text="Memory Trend: Stable")
        self.mem_trend_label.pack(anchor="w", pady=2)

        # Insights section
        self.insights_frame = ctk.CTkFrame(self.frame)
        self.insights_frame.pack(fill="both", expand=True, padx=10, pady=5)

        ctk.CTkLabel(self.insights_frame, text="System Insights", font=ctk.CTkFont(weight="bold")).pack()

        self.insights_text = ctk.CTkTextbox(self.insights_frame, wrap="word")
        self.insights_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.insights_text.insert("0.0", "Loading insights...")

        # Statistics
        self.stats_frame = ctk.CTkFrame(self.frame)
        self.stats_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.stats_frame, text="Statistics", font=ctk.CTkFont(weight="bold")).pack()

        self.avg_cpu_label = ctk.CTkLabel(self.stats_frame, text="Average CPU: 0%")
        self.avg_cpu_label.pack(anchor="w", pady=2)

        self.avg_mem_label = ctk.CTkLabel(self.stats_frame, text="Average Memory: 0%")
        self.avg_mem_label.pack(anchor="w", pady=2)

        self.peak_cpu_label = ctk.CTkLabel(self.stats_frame, text="Peak CPU: 0%")
        self.peak_cpu_label.pack(anchor="w", pady=2)

        self.peak_mem_label = ctk.CTkLabel(self.stats_frame, text="Peak Memory: 0%")
        self.peak_mem_label.pack(anchor="w", pady=2)

    def show(self):
        """Show the analytics page."""
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        """Hide the analytics page."""
        self.frame.pack_forget()

    def update(self, data):
        """Update analytics with new data."""
        # Update trends
        self._update_trends()

        # Update insights
        insights = get_system_insights(data)
        self.insights_text.delete("0.0", "end")
        for insight in insights:
            self.insights_text.insert("end", insight + "\n")

        # Update statistics
        self._update_statistics()

    def _update_trends(self):
        """Update trend analysis."""
        cpu_history = list(self.data_model.cpu_history)
        mem_history = list(self.data_model.memory_history)

        if len(cpu_history) > 1:
            cpu_trend = "Increasing" if cpu_history[-1] > cpu_history[0] else "Decreasing" if cpu_history[-1] < cpu_history[0] else "Stable"
            self.cpu_trend_label.configure(text=f"CPU Trend: {cpu_trend}")

        if len(mem_history) > 1:
            mem_trend = "Increasing" if mem_history[-1] > mem_history[0] else "Decreasing" if mem_history[-1] < mem_history[0] else "Stable"
            self.mem_trend_label.configure(text=f"Memory Trend: {mem_trend}")

    def _update_statistics(self):
        """Update statistical data."""
        cpu_history = list(self.data_model.cpu_history)
        mem_history = list(self.data_model.memory_history)

        if cpu_history:
            avg_cpu = sum(cpu_history) / len(cpu_history)
            peak_cpu = max(cpu_history)
            self.avg_cpu_label.configure(text=f"Average CPU: {avg_cpu:.1f}%")
            self.peak_cpu_label.configure(text=f"Peak CPU: {peak_cpu:.1f}%")

        if mem_history:
            avg_mem = sum(mem_history) / len(mem_history)
            peak_mem = max(mem_history)
            self.avg_mem_label.configure(text=f"Average Memory: {avg_mem:.1f}%")
            self.peak_mem_label.configure(text=f"Peak Memory: {peak_mem:.1f}%")