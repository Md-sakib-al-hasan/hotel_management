"""
Hotel Management System - Login & Register Screen
Custom tab switcher to eliminate all borders.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import auth

# ── Palette ──────────────────────────────────────────────────────────────────
BG       = "#0f172a"
CARD     = "#1e293b"
ACCENT   = "#3b82f6"
ACCENT_H = "#2563eb"
SUCCESS  = "#10b981"
TEXT     = "#f1f5f9"
MUTED    = "#64748b"
ENTRY_BG = "#0f172a"
BORDER   = "#475569"
BORDER_F = "#3b82f6"
ERR      = "#ef4444"


# ─── Draw a clean rounded rectangle on a Canvas ──────────────────────────────
def _draw_rounded_rect(canvas, x1, y1, x2, y2, r, fill, border, bw=2):
    canvas.create_oval(x1, y1, x1+2*r, y1+2*r, fill=fill, outline=fill)
    canvas.create_oval(x2-2*r, y1, x2, y1+2*r, fill=fill, outline=fill)
    canvas.create_oval(x1, y2-2*r, x1+2*r, y2, fill=fill, outline=fill)
    canvas.create_oval(x2-2*r, y2-2*r, x2, y2, fill=fill, outline=fill)
    canvas.create_rectangle(x1+r, y1, x2-r, y2, fill=fill, outline=fill)
    canvas.create_rectangle(x1, y1+r, x2, y2-r, fill=fill, outline=fill)
    if bw > 0:
        canvas.create_arc(x1, y1, x1+2*r, y1+2*r, start=90,  extent=90, style="arc", outline=border, width=bw)
        canvas.create_arc(x2-2*r, y1, x2, y1+2*r, start=0,   extent=90, style="arc", outline=border, width=bw)
        canvas.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, style="arc", outline=border, width=bw)
        canvas.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, style="arc", outline=border, width=bw)
        canvas.create_line(x1+r, y1, x2-r, y1, fill=border, width=bw)
        canvas.create_line(x1+r, y2, x2-r, y2, fill=border, width=bw)
        canvas.create_line(x1, y1+r, x1, y2-r, fill=border, width=bw)
        canvas.create_line(x2, y1+r, x2, y2-r, fill=border, width=bw)


# ─── Rounded Entry ────────────────────────────────────────────────────────────
def rounded_entry(parent, show=None, height=44, r=10):
    var = tk.StringVar()
    frame = tk.Frame(parent, bg=CARD)
    frame.pack(fill="x", pady=(0, 2))
    cv = tk.Canvas(frame, bg=CARD, highlightthickness=0, height=height, bd=0)
    cv.pack(fill="x")
    entry = tk.Entry(cv, textvariable=var, font=("Arial", 12),
                     bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT,
                     relief="flat", bd=0, highlightthickness=0)
    if show: entry.config(show=show)
    def _redraw(color):
        cv.delete("all")
        w, h = cv.winfo_width(), cv.winfo_height()
        if w < 4: return
        _draw_rounded_rect(cv, 1, 1, w-1, h-1, r, ENTRY_BG, color, bw=2)
        cv.create_window(w//2, h//2, window=entry, width=w - r*2, height=h - 10)
    cv.bind("<Configure>", lambda e: _redraw(BORDER))
    entry.bind("<FocusIn>",  lambda e: _redraw(BORDER_F))
    entry.bind("<FocusOut>", lambda e: _redraw(BORDER))
    return frame, var


# ─── Rounded Button ────────────────────────────────────────────────────────────
def rounded_button(parent, text, command, bg=ACCENT, hover=ACCENT_H,
                   fg=TEXT, height=46, r=10, font=("Arial", 12, "bold")):
    cv = tk.Canvas(parent, bg=CARD, highlightthickness=0, height=height, bd=0)
    cv.pack(fill="x", pady=(6, 0))
    def _redraw(color):
        cv.delete("all")
        w, h = cv.winfo_width(), cv.winfo_height()
        if w < 4: return
        _draw_rounded_rect(cv, 0, 0, w, h, r, color, color, bw=0)
        cv.create_text(w//2, h//2, text=text, fill=fg, font=font)
    cv.bind("<Configure>", lambda e: _redraw(bg))
    cv.bind("<Enter>",     lambda e: _redraw(hover))
    cv.bind("<Leave>",     lambda e: _redraw(bg))
    cv.bind("<Button-1>",  lambda e: command())


# ─── Login Window ─────────────────────────────────────────────────────────────
class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("Hotel Management System — Login")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self._center(960, 640)
        self._build()

    def _center(self, w, h):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build(self):
        # ── Left branding ────────────────────────────────────────────────────
        left = tk.Frame(self.root, bg=ACCENT, width=370)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        top_sp = tk.Frame(left, bg=ACCENT); top_sp.pack(fill="both", expand=True)

        # Handle Logo Image
        try:
            logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hotel_logo.png")
            self.logo_img = tk.PhotoImage(file=logo_path)
            # Scale down if too big (example: if it's 1024x1024, subsample by 8 makes it 128x128)
            # Adjust subsample factors based on chosen icon size
            if self.logo_img.width() > 150:
                fact = self.logo_img.width() // 120
                if fact > 0: self.logo_img = self.logo_img.subsample(fact, fact)
            
            self.logo_lbl = tk.Label(left, image=self.logo_img, bg=ACCENT)
            self.logo_lbl.pack(pady=(20, 0))
        except Exception as e:
            # Fallback to emoji if image fails
            tk.Label(left, text="🏨", font=("Arial", 56), bg=ACCENT, fg=TEXT).pack()

        tk.Label(left, text="Grand Hotel", font=("Arial", 23, "bold"), bg=ACCENT, fg=TEXT).pack(pady=(6, 2))
        tk.Label(left, text="Management System", font=("Arial", 13), bg=ACCENT, fg="#bfdbfe").pack()
        tk.Frame(left, bg="#93c5fd", height=1, width=200).pack(pady=18)
        tk.Label(left, text="Welcome.\n\nManage rooms, guests,\nbookings and invoices\nall in one place.",
                 font=("Arial", 11), bg=ACCENT, fg="#dbeafe", justify="center").pack()
        tk.Frame(left, bg=ACCENT).pack(fill="both", expand=True)
        tk.Label(left, text="v1.0  ·  © 2026 Grand Hotel", font=("Arial", 9), bg=ACCENT, fg="#93c5fd").pack(pady=14)

        # ── Right form ───────────────────────────────────────────────────────
        right = tk.Frame(self.root, bg=BG)
        right.pack(side="right", fill="both", expand=True)

        # Container for form and tabs
        main_container = tk.Frame(right, bg=BG)
        main_container.pack(fill="both", expand=True, padx=36, pady=28)

        # Custom Tab Switcher
        tab_bar = tk.Frame(main_container, bg=BG)
        tab_bar.pack(fill="x")

        self.login_tab_btn = tk.Button(tab_bar, text="Login", font=("Arial", 11, "bold"),
                                       bg=ACCENT, fg=TEXT, relief="flat", padx=25, pady=8,
                                       command=lambda: self._show_tab("login"), cursor="hand2",
                                       highlightthickness=0, bd=0)
        self.login_tab_btn.pack(side="left")

        self.reg_tab_btn = tk.Button(tab_bar, text="Register", font=("Arial", 11, "bold"),
                                     bg=CARD, fg=MUTED, relief="flat", padx=25, pady=8,
                                     command=lambda: self._show_tab("register"), cursor="hand2",
                                     highlightthickness=0, bd=0)
        self.reg_tab_btn.pack(side="left")

        # Page Container
        self.page_container = tk.Frame(main_container, bg=CARD, bd=0, highlightthickness=0)
        self.page_container.pack(fill="both", expand=True)

        # Init styled combobox for general use
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground=ENTRY_BG, background=CARD,
                        foreground=TEXT, arrowcolor=ACCENT, borderwidth=0)
        style.map("TCombobox", fieldbackground=[("readonly", ENTRY_BG)])

        self._build_login_tab()
        self._build_register_tab()
        
        # Default state
        self._show_tab("login")

    def _show_tab(self, name):
        if name == "login":
            self.reg_frame.pack_forget()
            self.login_frame.pack(fill="both", expand=True)
            self.login_tab_btn.config(bg=ACCENT, fg=TEXT)
            self.reg_tab_btn.config(bg=CARD, fg=MUTED)
        else:
            self.login_frame.pack_forget()
            self.reg_frame.pack(fill="both", expand=True)
            self.reg_tab_btn.config(bg=ACCENT, fg=TEXT)
            self.login_tab_btn.config(bg=CARD, fg=MUTED)

    # ── Login Tab ─────────────────────────────────────────────────────────────
    def _build_login_tab(self):
        self.login_frame = tk.Frame(self.page_container, bg=CARD, bd=0, highlightthickness=0)
        
        tk.Label(self.login_frame, text="Welcome Back!", font=("Arial", 20, "bold"), bg=CARD, fg=TEXT).pack(pady=(32, 4))
        tk.Label(self.login_frame, text="Sign in to continue", font=("Arial", 11), bg=CARD, fg=MUTED).pack()

        form = tk.Frame(self.login_frame, bg=CARD)
        form.pack(fill="x", padx=48, pady=(22, 0))
        self._lbl(form, "Username")
        _, self.login_user = rounded_entry(form)
        self._lbl(form, "Password")
        _, self.login_pass = rounded_entry(form, show="●")
        self.login_err = tk.Label(form, text="", fg=ERR, bg=CARD, font=("Arial", 10))
        self.login_err.pack(anchor="w", pady=(8, 0))
        rounded_button(form, "Sign In", self._do_login, bg=ACCENT, hover=ACCENT_H)
        tk.Label(self.login_frame, text="Default: admin / admin123", font=("Arial", 9), bg=CARD, fg=MUTED).pack(pady=(12, 0))

    # ── Register Tab ──────────────────────────────────────────────────────────
    def _build_register_tab(self):
        self.reg_frame = tk.Frame(self.page_container, bg=CARD, bd=0, highlightthickness=0)
        
        tk.Label(self.reg_frame, text="Create Account", font=("Arial", 20, "bold"), bg=CARD, fg=TEXT).pack(pady=(24, 4))
        tk.Label(self.reg_frame, text="Register a new staff account", font=("Arial", 11), bg=CARD, fg=MUTED).pack()

        form = tk.Frame(self.reg_frame, bg=CARD)
        form.pack(fill="x", padx=48, pady=(14, 0))
        self._lbl(form, "Full Name")
        _, self.reg_name = rounded_entry(form)
        self._lbl(form, "Username")
        _, self.reg_user = rounded_entry(form)
        self._lbl(form, "Password")
        _, self.reg_pass = rounded_entry(form, show="●")
        self._lbl(form, "Confirm Password")
        _, self.reg_pass2 = rounded_entry(form, show="●")
        self._lbl(form, "Role")
        self.reg_role = ttk.Combobox(form, values=["receptionist", "admin"], font=("Arial", 11), state="readonly")
        self.reg_role.set("receptionist")
        self.reg_role.pack(fill="x", ipady=4)
        self.reg_err = tk.Label(form, text="", fg=ERR, bg=CARD, font=("Arial", 10))
        self.reg_err.pack(anchor="w", pady=(6, 0))
        rounded_button(form, "Create Account", self._do_register, bg=SUCCESS, hover="#059669")

    def _lbl(self, parent, text):
        tk.Label(parent, text=text, font=("Arial", 10, "bold"), bg=CARD, fg=MUTED, anchor="w").pack(fill="x", pady=(10, 3))

    def _do_login(self):
        u, p = self.login_user.get().strip(), self.login_pass.get()
        if not u or not p: self.login_err.config(text="Please fill in all fields."); return
        user = auth.login(u, p)
        if user: self.login_err.config(text=""); self.on_login_success(user)
        else: self.login_err.config(text="Invalid username or password.")

    def _do_register(self):
        n, u, p1, p2, r = self.reg_name.get().strip(), self.reg_user.get().strip(), self.reg_pass.get(), self.reg_pass2.get(), self.reg_role.get()
        if not all([n, u, p1, p2]): self.reg_err.config(text="Please fill in all fields."); return
        if p1 != p2: self.reg_err.config(text="Passwords do not match."); return
        ok, res = auth.register(u, p1, r, n)
        if ok:
            messagebox.showinfo("Success", f"Account '{u}' created!"); self._show_tab("login")
            for v in [self.reg_name, self.reg_user, self.reg_pass, self.reg_pass2]: v.set("")
            self.reg_err.config(text="")
        else: self.reg_err.config(text=res)
