"""
Hotel Management System - Reports Page
Daily/Monthly revenue and occupancy statistics.
"""
import tkinter as tk
from tkinter import ttk, filedialog
from datetime import date, timedelta
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_revenue_report, get_dashboard_stats

BG      = "#0f172a"
CARD    = "#1e293b"
TEXT    = "#f1f5f9"
MUTED   = "#94a3b8"
ACCENT  = "#3b82f6"
SUCCESS = "#10b981"
DANGER  = "#ef4444"
WARNING = "#f59e0b"
BORDER  = "#334155"


class ReportsPage:
    def __init__(self, parent, user):
        self.frame = tk.Frame(parent, bg=BG)
        self.frame.pack(fill="both", expand=True, padx=24, pady=20)
        self._build()

    def _build(self):
        tk.Label(self.frame, text="📊  Reports & Analytics", font=("Arial", 18, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w")
        tk.Label(self.frame, text="Revenue and occupancy overview for any date range.",
                 font=("Arial", 11), bg=BG, fg=MUTED).pack(anchor="w", pady=(4, 16))

        # Quick stats
        s = get_dashboard_stats()
        stat_row = tk.Frame(self.frame, bg=BG)
        stat_row.pack(fill="x", pady=(0, 16))
        quick_stats = [
            ("🛏 Total Rooms",   s["total_rooms"],        ACCENT),
            ("🔴 Booked Now",    s["booked"],             DANGER),
            ("🟢 Available",     s["available"],          SUCCESS),
            ("👥 Total Guests",  s["total_guests"],       "#a855f7"),
            ("💰 Today",        f"৳{s['today_revenue']:,.0f}", SUCCESS),
        ]
        for label, val, color in quick_stats:
            c = tk.Frame(stat_row, bg=CARD, padx=18, pady=10)
            c.pack(side="left", padx=(0, 12))
            tk.Label(c, text=str(val), font=("Arial", 20, "bold"), bg=CARD, fg=color).pack()
            tk.Label(c, text=label, font=("Arial", 9), bg=CARD, fg=MUTED).pack()

        # Date range selector
        dr = tk.Frame(self.frame, bg=BG)
        dr.pack(fill="x", pady=(0, 10))
        tk.Label(dr, text="📅 From:", font=("Arial", 10, "bold"), bg=BG, fg=MUTED).pack(side="left")
        today = date.today()
        self.from_var = tk.StringVar(value=str(today.replace(day=1)))
        self.to_var   = tk.StringVar(value=str(today))
        tk.Entry(dr, textvariable=self.from_var, font=("Arial", 11),
                 bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat",
                 highlightthickness=1, highlightbackground=BORDER, width=14).pack(side="left", padx=6, ipady=3)
        tk.Label(dr, text="To:", font=("Arial", 10, "bold"), bg=BG, fg=MUTED).pack(side="left")
        tk.Entry(dr, textvariable=self.to_var, font=("Arial", 11),
                 bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat",
                 highlightthickness=1, highlightbackground=BORDER, width=14).pack(side="left", padx=6, ipady=3)
        tk.Button(dr, text="🔍 Generate", font=("Arial", 10, "bold"),
                  bg=ACCENT, fg=TEXT, relief="flat", cursor="hand2", padx=12, pady=4,
                  command=self._generate).pack(side="left", padx=6)
        tk.Button(dr, text="💾 Export TXT", font=("Arial", 10),
                  bg=SUCCESS, fg=TEXT, relief="flat", cursor="hand2", padx=10, pady=4,
                  command=self._export).pack(side="left", padx=4)

        # Shortcut buttons
        shortcuts = tk.Frame(self.frame, bg=BG)
        shortcuts.pack(anchor="w", pady=(0, 8))
        for label, delta in [("Today", 0), ("Last 7 Days", 7), ("This Month", -1)]:
            tk.Button(shortcuts, text=label, font=("Arial", 9),
                      bg=CARD, fg=MUTED, relief="flat", cursor="hand2", padx=10, pady=3,
                      command=lambda d=delta, l=label: self._shortcut(d, l)).pack(side="left", padx=3)

        # Report table
        cols = ("Date", "Bookings", "Revenue (৳)", "Collected (৳)")
        style = ttk.Style()
        style.configure("R.Treeview", background=CARD, foreground=TEXT,
                        fieldbackground=CARD, rowheight=30, font=("Arial", 10))
        style.configure("R.Treeview.Heading", background=ACCENT, foreground=TEXT,
                        font=("Arial", 10, "bold"))
        style.map("R.Treeview", background=[("selected", "#2563eb")])

        t_frame = tk.Frame(self.frame, bg=BG)
        t_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(t_frame, columns=cols, show="headings",
                                 style="R.Treeview", height=10)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180, anchor="center")
        sb = ttk.Scrollbar(t_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="left", fill="y")

        # Total label
        self.total_lbl = tk.Label(self.frame, text="",
                                  font=("Arial", 12, "bold"), bg=BG, fg=SUCCESS)
        self.total_lbl.pack(anchor="w", pady=6)

        self._generate()

    def _shortcut(self, delta, label):
        today = date.today()
        if delta == 0:
            self.from_var.set(str(today)); self.to_var.set(str(today))
        elif delta == -1:
            self.from_var.set(str(today.replace(day=1))); self.to_var.set(str(today))
        else:
            self.from_var.set(str(today - timedelta(days=delta))); self.to_var.set(str(today))
        self._generate()

    def _generate(self):
        self.tree.delete(*self.tree.get_children())
        try:
            rows = get_revenue_report(self.from_var.get(), self.to_var.get())
        except Exception:
            return
        total_rev = 0; total_col = 0
        for r in rows:
            rev = r["revenue"] or 0; col = r["collected"] or 0
            total_rev += rev; total_col += col
            self.tree.insert("", "end", values=(
                r["date"], r["bookings"],
                f"৳{rev:,.2f}", f"৳{col:,.2f}"
            ))
        self.total_lbl.config(
            text=f"Total Revenue: ৳{total_rev:,.2f}  |  Total Collected: ৳{total_col:,.2f}")

    def _export(self):
        rows = get_revenue_report(self.from_var.get(), self.to_var.get())
        if not rows:
            from tkinter import messagebox
            messagebox.showinfo("No Data", "No data for selected range."); return
        lines = [f"Revenue Report: {self.from_var.get()} to {self.to_var.get()}",
                 "─" * 60,
                 f"{'Date':<15}{'Bookings':>10}{'Revenue':>18}{'Collected':>18}",
                 "─" * 60]
        total = 0
        for r in rows:
            rev = r["revenue"] or 0; total += rev
            lines.append(f"{r['date']:<15}{r['bookings']:>10}{rev:>18,.2f}{(r['collected'] or 0):>18,.2f}")
        lines += ["─"*60, f"{'TOTAL':15}{'':>10}{total:>18,.2f}"]
        path = filedialog.asksaveasfilename(defaultextension=".txt",
               initialfile="revenue_report.txt",
               filetypes=[("Text", "*.txt"),("All","*.*")])
        if path:
            with open(path, "w", encoding="utf-8") as f: f.write("\n".join(lines))
            from tkinter import messagebox
            messagebox.showinfo("Saved", f"Report saved:\n{path}")
