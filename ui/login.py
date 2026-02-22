"""
Hotel Management System - Login & Register Screen
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Make sure parent directory is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import auth


# ── Color palette ────────────────────────────────────────────────────────────
BG        = "#0f172a"       # dark navy
CARD      = "#1e293b"       # card background
ACCENT    = "#3b82f6"       # blue
ACCENT_H  = "#2563eb"       # blue hover
SUCCESS   = "#10b981"       # green
TEXT      = "#f1f5f9"       # light text
MUTED     = "#94a3b8"       # grey text
ENTRY_BG  = "#0f172a"
BORDER    = "#334155"
ERR       = "#ef4444"


class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("Hotel Management System — Login")
        self.root.geometry("960x640")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self._center_window()
        self._build_ui()

    def _center_window(self):
        self.root.update_idletasks()
        w, h = 960, 640
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        # ── Left panel (branding) ──
        left = tk.Frame(self.root, bg=ACCENT, width=380)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        # Center content vertically
        spacer_top = tk.Frame(left, bg=ACCENT)
        spacer_top.pack(fill="both", expand=True)

        tk.Label(left, text="🏨", font=("Arial", 60), bg=ACCENT, fg=TEXT).pack()
        tk.Label(left, text="Grand Hotel", font=("Arial", 24, "bold"),
                 bg=ACCENT, fg=TEXT).pack(pady=(8, 2))
        tk.Label(left, text="Management System", font=("Arial", 13),
                 bg=ACCENT, fg="#bfdbfe").pack()

        tk.Label(left, text="─" * 22, bg=ACCENT, fg="#93c5fd",
                 font=("Arial", 10)).pack(pady=16)

        tk.Label(left,
                 text="Welcome to Grand Hotel\nManagement System.\n\nManage rooms, guests,\nbookings and invoices\nall in one place.",
                 font=("Arial", 11), bg=ACCENT, fg="#dbeafe",
                 justify="center").pack()

        spacer_bot = tk.Frame(left, bg=ACCENT)
        spacer_bot.pack(fill="both", expand=True)

        tk.Label(left, text="v1.0  |  © 2026 Grand Hotel",
                 font=("Arial", 9), bg=ACCENT, fg="#93c5fd").pack(pady=12)

        # ── Right panel (form) ──
        right = tk.Frame(self.root, bg=BG)
        right.pack(side="right", fill="both", expand=True)

        # Notebook (Login / Register tabs)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.TNotebook", background=BG, borderwidth=0)
        style.configure("Dark.TNotebook.Tab",
                        background=CARD, foreground=MUTED,
                        font=("Arial", 11, "bold"), padding=[20, 8])
        style.map("Dark.TNotebook.Tab",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", TEXT)])

        self.nb = ttk.Notebook(right, style="Dark.TNotebook")
        self.nb.pack(fill="both", expand=True, padx=40, pady=30)

        self._build_login_tab()
        self._build_register_tab()

    # ─── Login Tab ────────────────────────────────
    def _build_login_tab(self):
        frame = tk.Frame(self.nb, bg=CARD)
        self.nb.add(frame, text="  Login  ")

        tk.Label(frame, text="Welcome Back!", font=("Arial", 20, "bold"),
                 bg=CARD, fg=TEXT).pack(pady=(30, 4))
        tk.Label(frame, text="Sign in to your account", font=("Arial", 11),
                 bg=CARD, fg=MUTED).pack()

        form = tk.Frame(frame, bg=CARD)
        form.pack(pady=20, padx=50, fill="x")

        self.login_user = self._field(form, "Username")
        self.login_pass = self._field(form, "Password", show="●")

        # Login button
        btn = tk.Button(form, text="Sign In", font=("Arial", 12, "bold"),
                        bg=ACCENT, fg=TEXT, relief="flat", cursor="hand2",
                        pady=10, command=self._do_login)
        btn.pack(fill="x", pady=(14, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT_H))
        btn.bind("<Leave>", lambda e: btn.config(bg=ACCENT))

        self.login_err = tk.Label(form, text="", fg=ERR, bg=CARD, font=("Arial", 10))
        self.login_err.pack(pady=(8, 0))

        tk.Label(frame, text="Default credentials: admin / admin123",
                 font=("Arial", 9), bg=CARD, fg=MUTED).pack(pady=(4, 10))

    # ─── Register Tab ──────────────────────────────
    def _build_register_tab(self):
        frame = tk.Frame(self.nb, bg=CARD)
        self.nb.add(frame, text="  Register  ")

        tk.Label(frame, text="Create Account", font=("Arial", 20, "bold"),
                 bg=CARD, fg=TEXT).pack(pady=(20, 4))
        tk.Label(frame, text="Register a new staff account", font=("Arial", 11),
                 bg=CARD, fg=MUTED).pack()

        form = tk.Frame(frame, bg=CARD)
        form.pack(pady=14, padx=50, fill="x")

        self.reg_name  = self._field(form, "Full Name")
        self.reg_user  = self._field(form, "Username")
        self.reg_pass  = self._field(form, "Password", show="●")
        self.reg_pass2 = self._field(form, "Confirm Password", show="●")

        # Role
        tk.Label(form, text="Role", font=("Arial", 10, "bold"),
                 bg=CARD, fg=MUTED, anchor="w").pack(fill="x", pady=(8, 2))
        self.reg_role = ttk.Combobox(form, values=["receptionist", "admin"],
                                     font=("Arial", 11), state="readonly")
        self.reg_role.set("receptionist")
        self.reg_role.pack(fill="x", ipady=4)

        self.reg_err = tk.Label(form, text="", fg=ERR, bg=CARD, font=("Arial", 10))
        self.reg_err.pack(pady=(6, 0))

        btn = tk.Button(form, text="Create Account", font=("Arial", 12, "bold"),
                        bg=SUCCESS, fg=TEXT, relief="flat", cursor="hand2",
                        pady=10, command=self._do_register)
        btn.pack(fill="x", pady=(10, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg="#059669"))
        btn.bind("<Leave>", lambda e: btn.config(bg=SUCCESS))

    # ─── Helpers ───────────────────────────────────
    def _field(self, parent, label, show=None):
        tk.Label(parent, text=label, font=("Arial", 10, "bold"),
                 bg=CARD, fg=MUTED, anchor="w").pack(fill="x", pady=(8, 2))
        var = tk.StringVar()
        e = tk.Entry(parent, textvariable=var, font=("Arial", 12),
                     bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT,
                     relief="flat", bd=0, highlightthickness=1,
                     highlightbackground=BORDER, highlightcolor=ACCENT)
        e.pack(fill="x", ipady=7)
        if show:
            e.config(show=show)
        return var

    def _do_login(self):
        username = self.login_user.get().strip()
        password = self.login_pass.get()
        if not username or not password:
            self.login_err.config(text="Please fill in all fields.")
            return
        user = auth.login(username, password)
        if user:
            self.login_err.config(text="")
            self.on_login_success(user)
        else:
            self.login_err.config(text="Invalid username or password.")

    def _do_register(self):
        name  = self.reg_name.get().strip()
        uname = self.reg_user.get().strip()
        pw1   = self.reg_pass.get()
        pw2   = self.reg_pass2.get()
        role  = self.reg_role.get()

        if not all([name, uname, pw1, pw2]):
            self.reg_err.config(text="Please fill in all fields.")
            return
        if pw1 != pw2:
            self.reg_err.config(text="Passwords do not match.")
            return

        ok, result = auth.register(uname, pw1, role, name)
        if ok:
            self.reg_err.config(text="", fg=ERR)
            messagebox.showinfo("Success", f"Account created for '{uname}'!\nYou can now log in.")
            self.nb.select(0)
            self.reg_name.set(""); self.reg_user.set("")
            self.reg_pass.set(""); self.reg_pass2.set("")
        else:
            self.reg_err.config(text=f"{result}")
