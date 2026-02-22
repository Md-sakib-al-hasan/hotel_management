"""
Hotel Management System - Settings Page
Hotel info, password change, user management (admin only).
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_settings, set_setting, get_all_rooms, update_room
from auth import change_password, get_all_users, delete_user

BG      = "#0f172a"
CARD    = "#1e293b"
TEXT    = "#f1f5f9"
MUTED   = "#94a3b8"
ACCENT  = "#3b82f6"
SUCCESS = "#10b981"
DANGER  = "#ef4444"
BORDER  = "#334155"


class SettingsPage:
    def __init__(self, parent, user):
        self.user = user
        self.frame = tk.Frame(parent, bg=BG)
        self.frame.pack(fill="both", expand=True, padx=24, pady=20)
        self._build()

    def _build(self):
        tk.Label(self.frame, text="⚙  Settings", font=("Arial", 18, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", pady=(0, 16))

        nb = ttk.Notebook(self.frame)
        style = ttk.Style()
        style.configure("S.TNotebook", background=BG, borderwidth=0)
        style.configure("S.TNotebook.Tab", background=CARD, foreground=MUTED,
                        font=("Arial", 10, "bold"), padding=[14, 6])
        style.map("S.TNotebook.Tab",
                  background=[("selected", ACCENT)], foreground=[("selected", TEXT)])
        nb.configure(style="S.TNotebook")
        nb.pack(fill="both", expand=True)

        # Tab 1: Hotel Info
        t1 = tk.Frame(nb, bg=CARD)
        nb.add(t1, text="  🏨 Hotel Info  ")
        self._build_hotel_info(t1)

        # Tab 2: Change Password
        t2 = tk.Frame(nb, bg=CARD)
        nb.add(t2, text="  🔒 Change Password  ")
        self._build_change_password(t2)

        # Tab 3: User Management (admin only)
        if self.user["role"] == "admin":
            t3 = tk.Frame(nb, bg=CARD)
            nb.add(t3, text="  👤 Users  ")
            self._build_users(t3)

    # ── Hotel Info ──────────────────────────────────────────────────────────
    def _build_hotel_info(self, parent):
        tk.Label(parent, text="Hotel Configuration", font=("Arial", 14, "bold"),
                 bg=CARD, fg=TEXT).pack(pady=(20, 4), padx=30, anchor="w")
        tk.Label(parent, text="Changes take effect immediately.", font=("Arial", 10),
                 bg=CARD, fg=MUTED).pack(padx=30, anchor="w", pady=(0, 14))

        settings = get_settings()
        form = tk.Frame(parent, bg=CARD, padx=30)
        form.pack(fill="x")

        def field(label, key):
            tk.Label(form, text=label, font=("Arial", 10, "bold"),
                     bg=CARD, fg=MUTED, anchor="w").pack(fill="x", pady=(8, 2))
            v = tk.StringVar(value=settings.get(key, ""))
            tk.Entry(form, textvariable=v, font=("Arial", 11),
                     bg=BG, fg=TEXT, insertbackground=TEXT, relief="flat",
                     highlightthickness=1, highlightbackground=BORDER).pack(fill="x", ipady=5)
            return v, key

        fields = [
            field("🏨  Hotel Name",   "hotel_name"),
            field("📍  Address",       "hotel_address"),
            field("📞  Phone",         "hotel_phone"),
            field("📧  Email",         "hotel_email"),
            field("💱  Tax Rate (%)",  "tax_rate"),
        ]

        msg = tk.Label(form, text="", font=("Arial", 10), bg=CARD, fg=SUCCESS)
        msg.pack(pady=(6, 0))

        def save():
            for var, key in fields:
                set_setting(key, var.get())
            msg.config(text="✅  Settings saved successfully!")

        tk.Button(form, text="💾  Save Settings", font=("Arial", 11, "bold"),
                  bg=SUCCESS, fg=TEXT, relief="flat", cursor="hand2", pady=8,
                  command=save).pack(fill="x", pady=14)

    # ── Change Password ──────────────────────────────────────────────────────
    def _build_change_password(self, parent):
        tk.Label(parent, text="Change Password", font=("Arial", 14, "bold"),
                 bg=CARD, fg=TEXT).pack(pady=(20, 4), padx=30, anchor="w")

        form = tk.Frame(parent, bg=CARD, padx=30)
        form.pack(fill="x")

        def pw_field(label):
            tk.Label(form, text=label, font=("Arial", 10, "bold"),
                     bg=CARD, fg=MUTED, anchor="w").pack(fill="x", pady=(10, 2))
            v = tk.StringVar()
            tk.Entry(form, textvariable=v, show="●", font=("Arial", 11),
                     bg=BG, fg=TEXT, insertbackground=TEXT, relief="flat",
                     highlightthickness=1, highlightbackground=BORDER).pack(fill="x", ipady=5)
            return v

        v_old  = pw_field("🔑  Current Password")
        v_new1 = pw_field("🔒  New Password")
        v_new2 = pw_field("🔒  Confirm New Password")

        msg = tk.Label(form, text="", font=("Arial", 10), bg=CARD)
        msg.pack(pady=(8, 0))

        def do_change():
            if v_new1.get() != v_new2.get():
                msg.config(text="❌  New passwords do not match.", fg=DANGER); return
            ok, err = change_password(self.user["username"], v_old.get(), v_new1.get())
            if ok:
                msg.config(text="✅  Password changed successfully!", fg=SUCCESS)
                v_old.set(""); v_new1.set(""); v_new2.set("")
            else:
                msg.config(text=f"❌  {err}", fg=DANGER)

        tk.Button(form, text="🔄  Change Password", font=("Arial", 11, "bold"),
                  bg=ACCENT, fg=TEXT, relief="flat", cursor="hand2", pady=8,
                  command=do_change).pack(fill="x", pady=14)

    # ── Users Management ─────────────────────────────────────────────────────
    def _build_users(self, parent):
        tk.Label(parent, text="User Accounts", font=("Arial", 14, "bold"),
                 bg=CARD, fg=TEXT).pack(pady=(20, 8), padx=30, anchor="w")

        cols = ("#", "Username", "Full Name", "Role", "Created")
        style = ttk.Style()
        style.configure("U.Treeview", background=CARD, foreground=TEXT,
                        fieldbackground=BG, rowheight=28, font=("Arial", 10))
        style.configure("U.Treeview.Heading", background=ACCENT, foreground=TEXT,
                        font=("Arial", 10, "bold"))
        style.map("U.Treeview", background=[("selected", "#2563eb")])

        t_f = tk.Frame(parent, bg=CARD, padx=30)
        t_f.pack(fill="both", expand=True)

        tree = ttk.Treeview(t_f, columns=cols, show="headings",
                            style="U.Treeview", height=10)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        tree.pack(fill="both", expand=True)

        def load():
            tree.delete(*tree.get_children())
            for u in get_all_users():
                tree.insert("", "end", iid=u["id"], values=(
                    u["id"], u["username"], u["full_name"] or "-",
                    u["role"].title(),
                    u["created_at"][:10] if u.get("created_at") else "-"
                ))
        load()

        def del_user():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Select", "Please select a user."); return
            uid = int(sel[0])
            if uid == self.user["id"]:
                messagebox.showwarning("Error", "Cannot delete your own account."); return
            if messagebox.askyesno("Delete", "Delete this user?"):
                delete_user(uid); load()

        act = tk.Frame(parent, bg=CARD, padx=30)
        act.pack(fill="x", pady=10)
        tk.Button(act, text="🗑 Delete User", font=("Arial", 10, "bold"),
                  bg=DANGER, fg=TEXT, relief="flat", cursor="hand2", padx=12, pady=5,
                  command=del_user).pack(side="left")
        tk.Button(act, text="🔄 Refresh", font=("Arial", 10),
                  bg=ACCENT, fg=TEXT, relief="flat", cursor="hand2", padx=10, pady=5,
                  command=load).pack(side="left", padx=6)
