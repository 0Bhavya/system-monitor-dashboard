"""
Graph manager for live matplotlib graphs.
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from collections import deque

class GraphManager:
    """Manages live updating graphs."""

    def __init__(self, parent_widget):
        self.parent = parent_widget
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Data
        self.cpu_data = deque(maxlen=50)
        self.memory_data = deque(maxlen=50)

        # Initialize plots
        self.cpu_line, = self.ax1.plot([], [], 'r-', label='CPU %')
        self.memory_line, = self.ax2.plot([], [], 'b-', label='Memory %')

        self.ax1.set_title('CPU Usage Over Time')
        self.ax1.set_ylabel('CPU %')
        self.ax1.set_ylim(0, 100)
        self.ax1.legend()

        self.ax2.set_title('Memory Usage Over Time')
        self.ax2.set_ylabel('Memory %')
        self.ax2.set_xlabel('Time (seconds)')
        self.ax2.set_ylim(0, 100)
        self.ax2.legend()

    def update_data(self, cpu_history, memory_history):
        """Update the graph data."""
        self.cpu_data = cpu_history
        self.memory_data = memory_history
        self._redraw()

    def _redraw(self):
        """Redraw the graphs."""
        # Clear axes
        self.ax1.clear()
        self.ax2.clear()

        # Re-setup axes
        self.ax1.set_title('CPU Usage Over Time')
        self.ax1.set_ylabel('CPU %')
        self.ax1.set_ylim(0, 100)

        self.ax2.set_title('Memory Usage Over Time')
        self.ax2.set_ylabel('Memory %')
        self.ax2.set_xlabel('Time (seconds)')
        self.ax2.set_ylim(0, 100)

        # Plot data
        x_cpu = list(range(len(self.cpu_data)))
        x_mem = list(range(len(self.memory_data)))

        self.ax1.plot(x_cpu, list(self.cpu_data), 'r-', label='CPU %')
        self.ax2.plot(x_mem, list(self.memory_data), 'b-', label='Memory %')

        # Add legends
        self.ax1.legend()
        self.ax2.legend()

        # Adjust x-axis limits
        if self.cpu_data:
            self.ax1.set_xlim(0, len(self.cpu_data) - 1)
        if self.memory_data:
            self.ax2.set_xlim(0, len(self.memory_data) - 1)

        self.canvas.draw()