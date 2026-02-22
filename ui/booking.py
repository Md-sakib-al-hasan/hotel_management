"""
Hotel Management System - Booking Management Page
Create, view, cancel, checkout bookings.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime, timedelta
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import (get_all_bookings, get_all_rooms, get_all_guests,
                      create_booking, cancel_booking, checkout_booking, search_bookings)

BG      = "#0f172a"
CARD    = "#1e293b"
TEXT    = "#f1f5f9"
MUTED   = "#94a3b8"
ACCENT  = "#3b82f6"
SUCCESS = "#10b981"
DANGER  = "#ef4444"
WARNING = "#f59e0b"
BORDER  = "#334155"


class BookingsPage:
    def __init__(self, parent, user, refresh_cb=None):
        self.parent = parent
        self.user = user
        self.refresh_cb = refresh_cb

        self.frame = tk.Frame(parent, bg=BG)
        self.frame.pack(fill="both", expand=True, padx=24, pady=20)

        self._build()

    def _build(self):
        # Header
        hdr = tk.Frame(self.frame, bg=BG)
        hdr.pack(fill="x", pady=(0, 12))
        tk.Label(hdr, text="📋  Booking Management", font=("Arial", 18, "bold"),
                 bg=BG, fg=TEXT).pack(side="left")
        tk.Button(hdr, text="➕ New Booking", font=("Arial", 10, "bold"),
                  bg=SUCCESS, fg=TEXT, relief="flat", cursor="hand2", padx=12, pady=4,
                  command=self._new_booking_dialog).pack(side="right", padx=6)
        tk.Button(hdr, text="🔄 Refresh", font=("Arial", 10),
                  bg=ACCENT, fg=TEXT, relief="flat", cursor="hand2", padx=10, pady=4,
                  command=self._refresh).pack(side="right")

        # Search bar
        search_row = tk.Frame(self.frame, bg=BG)
        search_row.pack(fill="x", pady=(0, 8))
        tk.Label(search_row, text="🔍 Search:", font=("Arial", 10), bg=BG, fg=MUTED).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *a: self._load_table())
        tk.Entry(search_row, textvariable=self.search_var, font=("Arial", 11),
                 bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat",
                 highlightthickness=1, highlightbackground=BORDER, width=30).pack(side="left", padx=8, ipady=4)

        # Table
        self._build_table()

    def _build_table(self):
        cols = ("#", "Room", "Type", "Guest", "Phone", "Check-In", "Check-Out",
                "Nights", "Amount", "Status")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("B.Treeview", background=CARD, foreground=TEXT,
                        fieldbackground=CARD, rowheight=30, font=("Arial", 10))
        style.configure("B.Treeview.Heading", background=ACCENT, foreground=TEXT,
                        font=("Arial", 10, "bold"))
        style.map("B.Treeview", background=[("selected", "#2563eb")])

        tbl_frame = tk.Frame(self.frame, bg=BG)
        tbl_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tbl_frame, columns=cols, show="headings",
                                 style="B.Treeview", height=14)
        widths = [40, 70, 80, 150, 110, 100, 100, 55, 90, 90]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        sb = ttk.Scrollbar(tbl_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="left", fill="y")

        self._load_table()

        # Action buttons
        action_row = tk.Frame(self.frame, bg=BG)
        action_row.pack(fill="x", pady=10)
        tk.Button(action_row, text="✅ Check Out", font=("Arial", 10, "bold"),
                  bg=SUCCESS, fg=TEXT, relief="flat", cursor="hand2", padx=12, pady=5,
                  command=self._checkout_selected).pack(side="left", padx=4)
        tk.Button(action_row, text="❌ Cancel Booking", font=("Arial", 10, "bold"),
                  bg=DANGER, fg=TEXT, relief="flat", cursor="hand2", padx=12, pady=5,
                  command=self._cancel_selected).pack(side="left", padx=4)

    def _load_table(self):
        q = self.search_var.get().strip() if hasattr(self, "search_var") else ""
        self.tree.delete(*self.tree.get_children())
        bookings = search_bookings(q) if q else get_all_bookings()
        tag_map = {"active": "active", "checked_out": "out", "cancelled": "cancel"}
        self.tree.tag_configure("active",  background="#1d4034", foreground=TEXT)
        self.tree.tag_configure("out",     background="#172554", foreground=TEXT)
        self.tree.tag_configure("cancel",  background="#450a0a", foreground=TEXT)
        for b in bookings:
            tag = tag_map.get(b["status"], "")
            self.tree.insert("", "end", iid=b["id"], values=(
                b["id"], b["room_number"], b["room_type"], b["guest_name"],
                b["phone"] or "-", b["check_in"], b["check_out"],
                b["nights"], f"৳{b['total_amount']:,.0f}",
                b["status"].replace("_", " ").title()
            ), tags=(tag,))

    def _get_selected_booking_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Please select a booking first.")
            return None
        return int(sel[0])

    def _checkout_selected(self):
        bid = self._get_selected_booking_id()
        if bid and messagebox.askyesno("Check Out", "Mark this booking as checked out?"):
            checkout_booking(bid)
            self._refresh()
            if self.refresh_cb: self.refresh_cb()

    def _cancel_selected(self):
        bid = self._get_selected_booking_id()
        if bid and messagebox.askyesno("Cancel Booking", "Cancel this booking? The room will be freed."):
            cancel_booking(bid)
            self._refresh()
            if self.refresh_cb: self.refresh_cb()

    def _refresh(self):
        self._load_table()

    # ─── New Booking Dialog ─────────────────────────────────────────────────
    def _new_booking_dialog(self):
        dlg = tk.Toplevel(self.frame)
        dlg.title("New Booking")
        dlg.configure(bg=CARD)
        dlg.geometry("520x580")
        dlg.resizable(False, False)
        dlg.grab_set()
        dlg.update_idletasks()
        x = (dlg.winfo_screenwidth()-520)//2; y = (dlg.winfo_screenheight()-580)//2
        dlg.geometry(f"520x580+{x}+{y}")

        tk.Label(dlg, text="➕  New Booking", font=("Arial", 16, "bold"),
                 bg=CARD, fg=TEXT).pack(pady=(20, 4))

        form = tk.Frame(dlg, bg=CARD, padx=30)
        form.pack(fill="both", expand=True)

        def lbl(text):
            tk.Label(form, text=text, font=("Arial", 10, "bold"),
                     bg=CARD, fg=MUTED, anchor="w").pack(fill="x", pady=(10, 2))

        # Room selector (only available rooms)
        lbl("🛏  Room (Available Only)")
        rooms = [r for r in get_all_rooms() if r["status"] == "available"]
        room_labels = [f"Room {r['room_number']} — {r['room_type']} (৳{r['price_per_night']:,.0f}/night)"
                       for r in rooms]
        room_var = tk.StringVar()
        room_cb = ttk.Combobox(form, values=room_labels, textvariable=room_var,
                               font=("Arial", 11), state="readonly")
        room_cb.pack(fill="x", ipady=4)

        # Guest selector
        lbl("👤  Guest")
        guests = get_all_guests()
        guest_labels = [f"{g['full_name']} — {g['phone'] or 'No phone'}" for g in guests]
        guest_var = tk.StringVar()
        guest_cb = ttk.Combobox(form, values=guest_labels, textvariable=guest_var,
                                font=("Arial", 11), state="readonly")
        guest_cb.pack(fill="x", ipady=4)

        # Dates
        date_row = tk.Frame(form, bg=CARD)
        date_row.pack(fill="x")
        today = date.today()

        def date_field(parent, label, default):
            tk.Label(parent, text=label, font=("Arial", 10, "bold"),
                     bg=CARD, fg=MUTED).pack(anchor="w", pady=(10, 2))
            v = tk.StringVar(value=str(default))
            tk.Entry(parent, textvariable=v, font=("Arial", 11),
                     bg=BG, fg=TEXT, insertbackground=TEXT, relief="flat",
                     highlightthickness=1, highlightbackground=BORDER).pack(fill="x", ipady=4)
            return v

        left_f = tk.Frame(date_row, bg=CARD)
        left_f.pack(side="left", fill="x", expand=True, padx=(0, 8))
        right_f = tk.Frame(date_row, bg=CARD)
        right_f.pack(side="right", fill="x", expand=True)

        checkin_var  = date_field(left_f,  "📅  Check-In (YYYY-MM-DD)",  today)
        checkout_var = date_field(right_f, "📅  Check-Out (YYYY-MM-DD)", today + timedelta(days=1))

        # Advance paid
        lbl("💰  Advance Paid (৳)")
        advance_var = tk.StringVar(value="0")
        tk.Entry(form, textvariable=advance_var, font=("Arial", 11),
                 bg=BG, fg=TEXT, insertbackground=TEXT, relief="flat",
                 highlightthickness=1, highlightbackground=BORDER).pack(fill="x", ipady=4)

        # Notes
        lbl("📝  Notes (optional)")
        notes_var = tk.StringVar()
        tk.Entry(form, textvariable=notes_var, font=("Arial", 11),
                 bg=BG, fg=TEXT, insertbackground=TEXT, relief="flat",
                 highlightthickness=1, highlightbackground=BORDER).pack(fill="x", ipady=4)

        # Total display
        total_lbl = tk.Label(form, text="Total: ৳0.00", font=("Arial", 13, "bold"),
                             bg=CARD, fg=SUCCESS)
        total_lbl.pack(pady=(12, 0))

        def calc_total(*a):
            try:
                ci = datetime.strptime(checkin_var.get(), "%Y-%m-%d").date()
                co = datetime.strptime(checkout_var.get(), "%Y-%m-%d").date()
                nights = (co - ci).days
                if nights <= 0:
                    total_lbl.config(text="⚠ Check-out must be after check-in", fg=DANGER)
                    return
                if room_var.get():
                    idx = room_labels.index(room_var.get())
                    price = rooms[idx]["price_per_night"]
                    total = nights * price
                    total_lbl.config(text=f"Nights: {nights}  ×  ৳{price:,.0f}  =  Total: ৳{total:,.0f}", fg=SUCCESS)
            except:
                pass

        room_var.trace("w", calc_total)
        checkin_var.trace("w", calc_total)
        checkout_var.trace("w", calc_total)

        err_lbl = tk.Label(form, text="", fg=DANGER, bg=CARD, font=("Arial", 10))
        err_lbl.pack()

        def submit():
            try:
                if not room_var.get() or not guest_var.get():
                    err_lbl.config(text="Please select a room and guest."); return
                ridx = room_labels.index(room_var.get())
                gidx = guest_labels.index(guest_var.get())
                room = rooms[ridx]; guest = guests[gidx]
                ci = datetime.strptime(checkin_var.get(), "%Y-%m-%d").date()
                co = datetime.strptime(checkout_var.get(), "%Y-%m-%d").date()
                nights = (co - ci).days
                if nights <= 0:
                    err_lbl.config(text="Check-out must be after check-in."); return
                total = nights * room["price_per_night"]
                advance = float(advance_var.get() or 0)
                create_booking(room["id"], guest["id"], str(ci), str(co),
                               nights, total, advance, notes_var.get())
                dlg.destroy()
                self._refresh()
                if self.refresh_cb: self.refresh_cb()
                messagebox.showinfo("Success", f"Booking created!\nRoom {room['room_number']} → {guest['full_name']}")
            except Exception as ex:
                err_lbl.config(text=f"Error: {ex}")

        tk.Button(form, text="✅  Confirm Booking", font=("Arial", 12, "bold"),
                  bg=SUCCESS, fg=TEXT, relief="flat", cursor="hand2", pady=10,
                  command=submit).pack(fill="x", pady=12)
