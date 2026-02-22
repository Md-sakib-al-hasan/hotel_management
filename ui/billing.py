"""
Hotel Management System - Billing / Invoice Page
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import (get_all_bookings, get_invoice_by_booking,
                      create_invoice, get_settings)

BG      = "#0f172a"
CARD    = "#1e293b"
TEXT    = "#f1f5f9"
MUTED   = "#94a3b8"
ACCENT  = "#3b82f6"
SUCCESS = "#10b981"
DANGER  = "#ef4444"
WARNING = "#f59e0b"
BORDER  = "#334155"


class BillingPage:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.frame = tk.Frame(parent, bg=BG)
        self.frame.pack(fill="both", expand=True, padx=24, pady=20)
        self._build()

    def _build(self):
        tk.Label(self.frame, text="🧾  Billing & Invoices", font=("Arial", 18, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w")
        tk.Label(self.frame, text="Select a booking to generate or view its invoice.",
                 font=("Arial", 11), bg=BG, fg=MUTED).pack(anchor="w", pady=(4, 14))

        # Booking table (active + checked out)
        cols = ("#", "Room", "Guest", "Check-In", "Check-Out", "Total", "Status")
        style = ttk.Style()
        style.configure("Bi.Treeview", background=CARD, foreground=TEXT,
                        fieldbackground=CARD, rowheight=30, font=("Arial", 10))
        style.configure("Bi.Treeview.Heading", background=ACCENT, foreground=TEXT,
                        font=("Arial", 10, "bold"))
        style.map("Bi.Treeview", background=[("selected", "#2563eb")])

        t_frame = tk.Frame(self.frame, bg=BG)
        t_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(t_frame, columns=cols, show="headings",
                                 style="Bi.Treeview", height=12)
        widths = [50, 80, 180, 100, 100, 100, 110]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")
        sb = ttk.Scrollbar(t_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="left", fill="y")

        self.bookings = get_all_bookings()
        for b in self.bookings:
            self.tree.insert("", "end", iid=b["id"], values=(
                b["id"], b["room_number"], b["guest_name"],
                b["check_in"], b["check_out"],
                f"৳{b['total_amount']:,.0f}",
                b["status"].replace("_", " ").title()
            ))

        # Buttons
        act = tk.Frame(self.frame, bg=BG)
        act.pack(fill="x", pady=10)
        tk.Button(act, text="🧾 Generate Invoice", font=("Arial", 11, "bold"),
                  bg=ACCENT, fg=TEXT, relief="flat", cursor="hand2", padx=14, pady=6,
                  command=self._generate_invoice).pack(side="left", padx=4)
        tk.Button(act, text="💾 Save as TXT", font=("Arial", 11, "bold"),
                  bg=SUCCESS, fg=TEXT, relief="flat", cursor="hand2", padx=14, pady=6,
                  command=self._save_invoice).pack(side="left", padx=4)

        # Invoice preview area
        tk.Label(self.frame, text="Invoice Preview:", font=("Arial", 11, "bold"),
                 bg=BG, fg=MUTED).pack(anchor="w", pady=(10, 4))
        self.preview = tk.Text(self.frame, height=14, bg=CARD, fg=TEXT,
                               font=("Courier", 10), relief="flat",
                               insertbackground=TEXT, state="disabled",
                               highlightthickness=1, highlightbackground=BORDER)
        self.preview.pack(fill="x")

    def _get_selected_booking(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Please select a booking from the table.")
            return None
        bid = int(sel[0])
        return next((b for b in self.bookings if b["id"] == bid), None)

    def _build_invoice_text(self, booking):
        settings = get_settings()
        hotel = settings.get("hotel_name", "Grand Hotel")
        addr  = settings.get("hotel_address", "")
        phone = settings.get("hotel_phone", "")
        tax_rate = float(settings.get("tax_rate", 0))

        subtotal = booking["total_amount"]
        tax_amt  = subtotal * tax_rate / 100
        total    = subtotal + tax_amt
        adv      = booking.get("advance_paid", 0) or 0
        due      = total - adv

        inv = get_invoice_by_booking(booking["id"])
        inv_num = inv["invoice_number"] if inv else f"INV-{booking['id']:04d}"

        lines = [
            "═" * 50,
            f"          {hotel}",
            f"          {addr}",
            f"          📞 {phone}",
            "═" * 50,
            f"  INVOICE No: {inv_num}",
            f"  Date: {datetime.now().strftime('%d %b %Y  %H:%M')}",
            "─" * 50,
            f"  Guest  : {booking['guest_name']}",
            f"  Phone  : {booking.get('phone') or '-'}",
            f"  Room   : {booking['room_number']} ({booking['room_type']})",
            f"  Check-In : {booking['check_in']}",
            f"  Check-Out: {booking['check_out']}",
            f"  Nights : {booking['nights']}",
            "─" * 50,
            f"  Sub-total : ৳{subtotal:>10,.2f}",
            f"  Tax ({tax_rate:.0f}%)  : ৳{tax_amt:>10,.2f}",
            f"  TOTAL     : ৳{total:>10,.2f}",
            f"  Advance   : ৳{adv:>10,.2f}",
            f"  DUE       : ৳{due:>10,.2f}",
            "═" * 50,
            "  Thank you for staying with us!",
            "═" * 50,
        ]
        return "\n".join(lines)

    def _generate_invoice(self):
        booking = self._get_selected_booking()
        if not booking: return

        # Create invoice record if not exists
        inv = get_invoice_by_booking(booking["id"])
        if not inv:
            create_invoice(booking["id"], booking["total_amount"], 0, 0,
                           booking.get("advance_paid", 0) or 0)

        text = self._build_invoice_text(booking)
        self.preview.configure(state="normal")
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", text)
        self.preview.configure(state="disabled")

    def _save_invoice(self):
        booking = self._get_selected_booking()
        if not booking: return
        text = self._build_invoice_text(booking)
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=f"Invoice_{booking['room_number']}_{booking['guest_name']}.txt",
            filetypes=[("Text files", "*.txt"), ("All", "*.*")]
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo("Saved", f"Invoice saved to:\n{path}")
