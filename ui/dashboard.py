"""
Hotel Management System - Dashboard (Main Shell)
Sidebar navigation + stats bar + content frame
"""
import tkinter as tk
from tkinter import ttk, messagebox

# Colour palette (shared)
BG       = "#0f172a"
SIDEBAR  = "#1e293b"
ACCENT   = "#3b82f6"
ACCENT_H = "#2563eb"
CARD     = "#1e293b"
TEXT     = "#f1f5f9"
MUTED    = "#94a3b8"
SUCCESS  = "#10b981"
WARNING  = "#f59e0b"
DANGER   = "#ef4444"
BORDER   = "#334155"
STAT_BG  = "#0f172a"


class Dashboard:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title(f"Hotel Management System — {user['full_name'] or user['username']}")
        self.root.geometry("1280x750")
        self.root.configure(bg=BG)
        self._center()
        self._active_btn = None
        self._build()

    def _center(self):
        self.root.update_idletasks()
        w, h = 1280, 750
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build(self):
        # ── Top bar ──────────────────────────────────────
        topbar = tk.Frame(self.root, bg=SIDEBAR, height=54)
        topbar.pack(fill="x", side="top")
        topbar.pack_propagate(False)

        tk.Label(topbar, text="🏨  Grand Hotel  Management System",
                 font=("Arial", 14, "bold"), bg=SIDEBAR, fg=TEXT).pack(side="left", padx=20)

        tk.Label(topbar,
                 text=f"👤  {self.user['full_name'] or self.user['username']}  [{self.user['role'].upper()}]",
                 font=("Arial", 10), bg=SIDEBAR, fg=MUTED).pack(side="right", padx=20)

        logout_btn = tk.Button(topbar, text="⏻ Logout", font=("Arial", 10, "bold"),
                               bg=DANGER, fg=TEXT, relief="flat", cursor="hand2",
                               command=self._logout, padx=12, pady=4)
        logout_btn.pack(side="right", padx=6, pady=10)

        # ── Stats bar ─────────────────────────────────────
        self.stats_frame = tk.Frame(self.root, bg=BG, height=80)
        self.stats_frame.pack(fill="x", side="top")
        self.stats_frame.pack_propagate(False)
        self._refresh_stats()

        # ── Body (sidebar + content) ──────────────────────
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True)

        # Sidebar
        sidebar = tk.Frame(body, bg=SIDEBAR, width=210)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="NAVIGATION", font=("Arial", 8, "bold"),
                 bg=SIDEBAR, fg=MUTED).pack(pady=(20, 6), padx=12, anchor="w")

        self.content = tk.Frame(body, bg=BG)
        self.content.pack(side="right", fill="both", expand=True)

        # Nav items: (emoji_label, Page class)
        nav_items = [
            ("🏠  Dashboard",  self._show_home),
            ("🛏  Rooms",       self._show_rooms),
            ("📋  Bookings",    self._show_bookings),
            ("👥  Guests",      self._show_guests),
            ("🧾  Billing",     self._show_billing),
            ("📊  Reports",     self._show_reports),
            ("⚙  Settings",    self._show_settings),
        ]
        self._nav_buttons = []
        for label, cmd in nav_items:
            b = tk.Button(sidebar, text=label, font=("Arial", 11),
                          bg=SIDEBAR, fg=TEXT, relief="flat", cursor="hand2",
                          anchor="w", padx=18, pady=10,
                          command=lambda c=cmd, b2=None: self._nav_click(c, b2))
            b.pack(fill="x")
            b.bind("<Enter>",  lambda e, btn=b: btn.config(bg="#334155") if btn != self._active_btn else None)
            b.bind("<Leave>",  lambda e, btn=b: btn.config(bg=SIDEBAR) if btn != self._active_btn else None)
            # Fix late binding issue
            b.config(command=lambda c=cmd, btn=b: self._nav_click(c, btn))
            self._nav_buttons.append(b)

        # Show home by default
        self._nav_click(self._show_home, self._nav_buttons[0])

    def _nav_click(self, cmd, btn):
        if self._active_btn:
            self._active_btn.config(bg=SIDEBAR)
        self._active_btn = btn
        if btn:
            btn.config(bg=ACCENT)
        # Clear content
        for w in self.content.winfo_children():
            w.destroy()
        cmd()

    def _refresh_stats(self):
        for w in self.stats_frame.winfo_children():
            w.destroy()
        from database import get_dashboard_stats
        s = get_dashboard_stats()
        stats = [
            ("🛏 Total Rooms",   str(s["total_rooms"]),   ACCENT),
            ("🔴 Booked",        str(s["booked"]),         DANGER),
            ("🟢 Available",     str(s["available"]),      SUCCESS),
            ("🟡 Maintenance",   str(s["maintenance"]),    WARNING),
            ("👥 Total Guests",  str(s["total_guests"]),   "#a855f7"),
            ("💰 Today Revenue", f"৳{s['today_revenue']:,.0f}", SUCCESS),
        ]
        for label, val, color in stats:
            card = tk.Frame(self.stats_frame, bg=CARD, padx=16, pady=10)
            card.pack(side="left", fill="y", padx=(12, 0), pady=10)
            tk.Label(card, text=val, font=("Arial", 18, "bold"),
                     bg=CARD, fg=color).pack()
            tk.Label(card, text=label, font=("Arial", 9),
                     bg=CARD, fg=MUTED).pack()

    # ─── Page loaders ────────────────────────────────────────────────────────
    def _show_home(self):
        self._refresh_stats()
        from ui.home import HomePage
        HomePage(self.content, self.user, self._nav_buttons, self._nav_click,
                 self._show_rooms, self._show_bookings)

    def _show_rooms(self):
        from ui.rooms import RoomsPage
        RoomsPage(self.content, self.user, refresh_cb=self._refresh_stats)

    def _show_bookings(self):
        from ui.booking import BookingsPage
        BookingsPage(self.content, self.user, refresh_cb=self._refresh_stats)

    def _show_guests(self):
        from ui.guests import GuestsPage
        GuestsPage(self.content, self.user)

    def _show_billing(self):
        from ui.billing import BillingPage
        BillingPage(self.content, self.user)

    def _show_reports(self):
        from ui.reports import ReportsPage
        ReportsPage(self.content, self.user)

    def _show_settings(self):
        from ui.settings import SettingsPage
        SettingsPage(self.content, self.user)

    def _logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            import main
            main.start_app()
