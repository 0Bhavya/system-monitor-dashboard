"""
Process utility functions.
"""

import psutil

def kill_process(pid):
    """Safely kill a process by PID."""
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        # Wait a bit for graceful termination
        proc.wait(timeout=3)
        return True, "Process terminated successfully"
    except psutil.NoSuchProcess:
        return False, "Process not found"
    except psutil.AccessDenied:
        return False, "Permission denied"
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_process_info(pid):
    """Get detailed info about a process."""
    try:
        proc = psutil.Process(pid)
        return {
            'pid': proc.pid,
            'name': proc.name(),
            'status': proc.status(),
            'cpu_percent': proc.cpu_percent(),
            'memory_percent': proc.memory_percent(),
            'create_time': proc.create_time()
        }
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None