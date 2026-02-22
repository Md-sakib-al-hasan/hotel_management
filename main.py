"""
Hotel Management System
Entry Point — main.py
Run: python main.py
"""
import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from database import initialize_database


def start_app():
    """Initialize DB and show the login window."""
    initialize_database()

    root = tk.Tk()
    root.title("Hotel Management System")

    # Login window
    from ui.login import LoginWindow

    def on_login_success(user):
        """Open dashboard after successful login."""
        root.destroy()
        dash_root = tk.Tk()
        from ui.dashboard import Dashboard
        Dashboard(dash_root, user)
        dash_root.mainloop()

    LoginWindow(root, on_login_success)
    root.mainloop()


if __name__ == "__main__":
    start_app()
