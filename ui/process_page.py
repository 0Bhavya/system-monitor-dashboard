"""
Process page with process table and controls.
"""

import customtkinter as ctk
from tkinter import ttk
from utils.process_utils import kill_process

class ProcessPage:
    """Process management page."""

    def __init__(self, parent, data_model):
        self.parent = parent
        self.data_model = data_model
        self.frame = ctk.CTkFrame(parent)
        self.selected_pid = None
        self.update_counter = 0

        # Create widgets
        self._create_widgets()

    def _create_widgets(self):
        """Create process page widgets."""
        # Title
        title = ctk.CTkLabel(self.frame, text="Process Monitor", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=10)

        # Process table
        self.table_frame = ctk.CTkFrame(self.frame)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create treeview
        columns = ('PID', 'Name', 'CPU %', 'Memory %')
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show='headings', height=20)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

        # Bind selection
        self.tree.bind('<<TreeviewSelect>>', self._on_select)

        # Control buttons
        self.control_frame = ctk.CTkFrame(self.frame)
        self.control_frame.pack(fill="x", padx=10, pady=5)

        self.kill_btn = ctk.CTkButton(
            self.control_frame, text="Kill Selected Process", command=self._kill_process,
            fg_color="red", hover_color="darkred"
        )
        self.kill_btn.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.refresh_btn = ctk.CTkButton(
            self.control_frame, text="Refresh Processes", command=self._refresh_processes,
            fg_color="blue", hover_color="darkblue"
        )
        self.refresh_btn.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Status label
        self.status_label = ctk.CTkLabel(self.control_frame, text="")
        self.status_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")

        # Configure grid weights
        self.control_frame.grid_columnconfigure(0, weight=1)
        self.control_frame.grid_columnconfigure(1, weight=1)
        self.control_frame.grid_columnconfigure(2, weight=1)

        # Top processes
        self.top_frame = ctk.CTkFrame(self.frame)
        self.top_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(self.top_frame, text="Top 5 CPU Processes").pack()

        self.top_labels = []
        for i in range(5):
            label = ctk.CTkLabel(self.top_frame, text="")
            label.pack(anchor="w")
            self.top_labels.append(label)

    def show(self):
        """Show the process page."""
        self.frame.pack(fill="both", expand=True)
        self._refresh_processes()

    def hide(self):
        """Hide the process page."""
        self.frame.pack_forget()

    def update(self, data):
        """Update process data."""
        self.update_counter += 1

        # Update table every 2 seconds (2 UI updates)
        if self.update_counter >= 2:
            if 'processes' in data:
                self._update_table(data['processes'])
            self.update_counter = 0

        if 'top_processes' in data:
            self._update_top_processes(data['top_processes'])

    def _update_table(self, processes):
        """Update the process table."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Limit to top 20 processes for performance
        top_processes = processes[:20]

        # Add new items
        for proc in top_processes:
            self.tree.insert('', 'end', values=(
                proc['pid'],
                proc['name'],
                f"{proc['cpu_percent']:.1f}",
                f"{proc['memory_percent']:.1f}"
            ))

    def _update_top_processes(self, top_procs):
        """Update top processes display."""
        for i, label in enumerate(self.top_labels):
            if i < len(top_procs):
                proc = top_procs[i]
                label.configure(text=f"{proc['name']} (PID: {proc['pid']}) - CPU: {proc['cpu_percent']:.1f}%")
            else:
                label.configure(text="")

    def _on_select(self, event):
        """Handle process selection."""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.selected_pid = int(item['values'][0])
        else:
            self.selected_pid = None

    def _kill_process(self):
        """Kill the selected process."""
        if self.selected_pid:
            # Safety check for critical processes
            if self.selected_pid == 1:
                self.status_label.configure(text="Cannot kill system process (PID 1)", text_color="red")
                return

            success, message = kill_process(self.selected_pid)
            if success:
                self.status_label.configure(text="Process terminated", text_color="green")
                self.selected_pid = None
                self.tree.selection_remove(self.tree.selection())  # Clear selection
                self._refresh_processes()
            else:
                self.status_label.configure(text=message, text_color="red")
        else:
            self.status_label.configure(text="No process selected", text_color="orange")

    def _refresh_processes(self):
        """Refresh the process list."""
        # Force update the table with current data
        data = self.data_model.current_data
        if 'processes' in data:
            self._update_table(data['processes'])
        self.status_label.configure(text="Processes refreshed", text_color="green")