"""
Hotel Management System - Guests Management Page
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_all_guests, add_guest, update_guest, delete_guest, search_guests

BG      = "#0f172a"
CARD    = "#1e293b"
TEXT    = "#f1f5f9"
MUTED   = "#94a3b8"
ACCENT  = "#3b82f6"
SUCCESS = "#10b981"
DANGER  = "#ef4444"
BORDER  = "#334155"


class GuestsPage:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.frame = tk.Frame(parent, bg=BG)
        self.frame.pack(fill="both", expand=True, padx=24, pady=20)
        self._build()

    def _build(self):
        hdr = tk.Frame(self.frame, bg=BG)
        hdr.pack(fill="x", pady=(0, 10))
        tk.Label(hdr, text="👥  Guest Management", font=("Arial", 18, "bold"),
                 bg=BG, fg=TEXT).pack(side="left")
        tk.Button(hdr, text="➕ Add Guest", font=("Arial", 10, "bold"),
                  bg=SUCCESS, fg=TEXT, relief="flat", cursor="hand2", padx=12, pady=4,
                  command=lambda: self._open_form()).pack(side="right", padx=6)

        # Search
        sr = tk.Frame(self.frame, bg=BG)
        sr.pack(fill="x", pady=(0, 8))
        tk.Label(sr, text="🔍 Search:", font=("Arial", 10), bg=BG, fg=MUTED).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *a: self._load())
        tk.Entry(sr, textvariable=self.search_var, font=("Arial", 11),
                 bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat",
                 highlightthickness=1, highlightbackground=BORDER, width=30).pack(
                     side="left", padx=8, ipady=4)

        # Table
        cols = ("#", "Full Name", "Phone", "Email", "NID", "Address", "Joined")
        style = ttk.Style()
        style.configure("G.Treeview", background=CARD, foreground=TEXT,
                        fieldbackground=CARD, rowheight=30, font=("Arial", 10))
        style.configure("G.Treeview.Heading", background=ACCENT, foreground=TEXT,
                        font=("Arial", 10, "bold"))
        style.map("G.Treeview", background=[("selected", "#2563eb")])

        t_frame = tk.Frame(self.frame, bg=BG)
        t_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(t_frame, columns=cols, show="headings",
                                 style="G.Treeview", height=14)
        widths = [40, 180, 120, 180, 130, 200, 120]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")
        sb = ttk.Scrollbar(t_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="left", fill="y")
        self._load()

        # Actions
        act = tk.Frame(self.frame, bg=BG)
        act.pack(fill="x", pady=10)
        tk.Button(act, text="✏ Edit Guest", font=("Arial", 10, "bold"),
                  bg=ACCENT, fg=TEXT, relief="flat", cursor="hand2", padx=12, pady=5,
                  command=self._edit_selected).pack(side="left", padx=4)
        tk.Button(act, text="🗑 Delete Guest", font=("Arial", 10, "bold"),
                  bg=DANGER, fg=TEXT, relief="flat", cursor="hand2", padx=12, pady=5,
                  command=self._delete_selected).pack(side="left", padx=4)

    def _load(self):
        q = self.search_var.get().strip()
        self.tree.delete(*self.tree.get_children())
        rows = search_guests(q) if q else get_all_guests()
        for g in rows:
            self.tree.insert("", "end", iid=g["id"], values=(
                g["id"], g["full_name"], g["phone"] or "-",
                g["email"] or "-", g["nid"] or "-",
                g["address"] or "-",
                g["created_at"][:10] if g.get("created_at") else "-"
            ))

    def _get_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Please select a guest first.")
            return None
        return int(sel[0])

    def _edit_selected(self):
        gid = self._get_selected()
        if gid:
            guests = get_all_guests()
            g = next((x for x in guests if x["id"] == gid), None)
            if g: self._open_form(g)

    def _delete_selected(self):
        gid = self._get_selected()
        if gid and messagebox.askyesno("Delete", "Delete this guest? This cannot be undone."):
            delete_guest(gid)
            self._load()

    def _open_form(self, guest=None):
        dlg = tk.Toplevel(self.frame)
        dlg.title("Add Guest" if not guest else "Edit Guest")
        dlg.configure(bg=CARD)
        dlg.geometry("440x460")
        dlg.resizable(False, False)
        dlg.grab_set()
        dlg.update_idletasks()
        x = (dlg.winfo_screenwidth()-440)//2; y = (dlg.winfo_screenheight()-460)//2
        dlg.geometry(f"440x460+{x}+{y}")

        title = "✏  Edit Guest" if guest else "➕  Add Guest"
        tk.Label(dlg, text=title, font=("Arial", 16, "bold"), bg=CARD, fg=TEXT).pack(pady=(20, 10))

        form = tk.Frame(dlg, bg=CARD, padx=30)
        form.pack(fill="both", expand=True)

        def field(label, val=""):
            tk.Label(form, text=label, font=("Arial", 10, "bold"),
                     bg=CARD, fg=MUTED, anchor="w").pack(fill="x", pady=(8, 2))
            v = tk.StringVar(value=val)
            tk.Entry(form, textvariable=v, font=("Arial", 11), bg=BG,
                     fg=TEXT, insertbackground=TEXT, relief="flat",
                     highlightthickness=1, highlightbackground=BORDER).pack(fill="x", ipady=4)
            return v

        v_name  = field("👤  Full Name",  guest["full_name"]  if guest else "")
        v_phone = field("📞  Phone",      guest["phone"]      if guest else "")
        v_email = field("📧  Email",      guest["email"]      if guest else "")
        v_nid   = field("🪪  NID / Passport", guest["nid"]   if guest else "")
        v_addr  = field("🏠  Address",    guest["address"]    if guest else "")

        err = tk.Label(form, text="", fg=DANGER, bg=CARD, font=("Arial", 10))
        err.pack(pady=(6, 0))

        def save():
            name = v_name.get().strip()
            if not name:
                err.config(text="Full name is required."); return
            if guest:
                update_guest(guest["id"], name, v_phone.get(), v_email.get(),
                             v_nid.get(), v_addr.get())
            else:
                add_guest(name, v_phone.get(), v_email.get(), v_nid.get(), v_addr.get())
            dlg.destroy()
            self._load()

        tk.Button(form, text="💾  Save Guest", font=("Arial", 12, "bold"),
                  bg=SUCCESS, fg=TEXT, relief="flat", cursor="hand2", pady=10,
                  command=save).pack(fill="x", pady=12)
