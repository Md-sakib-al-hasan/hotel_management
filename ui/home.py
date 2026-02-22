"""
Hotel Management System - Home Page (Overview)
"""
import tkinter as tk
from tkinter import ttk
from database import get_dashboard_stats, get_active_bookings

BG    = "#0f172a"
CARD  = "#1e293b"
TEXT  = "#f1f5f9"
MUTED = "#94a3b8"
ACCENT = "#3b82f6"
SUCCESS = "#10b981"
DANGER  = "#ef4444"
WARNING = "#f59e0b"
BORDER  = "#334155"


class HomePage:
    def __init__(self, parent, user, nav_buttons, nav_click, show_rooms, show_bookings):
        self.parent = parent
        self.user = user
        frame = tk.Frame(parent, bg=BG)
        frame.pack(fill="both", expand=True, padx=24, pady=20)

        tk.Label(frame, text=f"🏠  Dashboard Overview", font=("Arial", 18, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w")
        tk.Label(frame, text="Real-time hotel status at a glance",
                 font=("Arial", 11), bg=BG, fg=MUTED).pack(anchor="w", pady=(2, 16))

        # Active bookings table
        tk.Label(frame, text="📋  Today's Active Bookings", font=("Arial", 13, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", pady=(10, 6))

        cols = ("Room", "Guest", "Phone", "Check-In", "Check-Out", "Nights", "Amount")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.Treeview", background=CARD, foreground=TEXT,
                        fieldbackground=CARD, rowheight=32, font=("Arial", 10))
        style.configure("Dark.Treeview.Heading", background=ACCENT, foreground=TEXT,
                        font=("Arial", 10, "bold"))
        style.map("Dark.Treeview", background=[("selected", ACCENT)])

        tree = ttk.Treeview(frame, columns=cols, show="headings",
                            style="Dark.Treeview", height=10)
        widths = [80, 160, 120, 110, 110, 60, 100]
        for col, w in zip(cols, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center")

        bookings = get_active_bookings()
        for b in bookings:
            tree.insert("", "end", values=(
                b["room_number"], b["guest_name"], b["phone"] or "-",
                b["check_in"], b["check_out"], b["nights"],
                f"৳{b['total_amount']:,.0f}"
            ))

        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="left", fill="y")

        if not bookings:
            tk.Label(frame, text="No active bookings today.",
                     font=("Arial", 11), bg=BG, fg=MUTED).pack(pady=10)
