#!/usr/bin/env python3
"""
Main entry point for the System Monitor Dashboard.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))

from ui.app import SystemMonitorApp

def main():
    """Main function to start the application."""
    app = SystemMonitorApp()
    app.run()

if __name__ == "__main__":
    main()