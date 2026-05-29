"""
System utility functions for the monitor.
"""

import psutil
from datetime import timedelta

def format_bytes(bytes_value):
    """Format bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return ".1f"
        bytes_value /= 1024.0
    return ".1f"

def format_uptime(seconds):
    """Format uptime seconds to human readable string."""
    return str(timedelta(seconds=int(seconds)))

def get_system_insights(data):
    """Generate system insights based on current data."""
    insights = []

    if data.get('cpu_percent', 0) > 80:
        top_proc = data.get('top_processes', [])
        if top_proc:
            insights.append(f"High CPU usage ({data['cpu_percent']:.1f}%) caused by {top_proc[0]['name']}")

    if data.get('memory', {}).get('percent', 0) > 80:
        insights.append(f"High memory usage ({data['memory']['percent']:.1f}%)")

    if not insights:
        insights.append("System running normally")

    return insights