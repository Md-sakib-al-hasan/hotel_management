"""
Hotel Management System - Rooms Page
Visual grid of room cards: Green=Available, Red=Booked, Yellow=Maintenance
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import get_all_rooms, update_room_status, update_room

BG      = "#0f172a"
CARD    = "#1e293b"
TEXT    = "#f1f5f9"
MUTED   = "#94a3b8"
ACCENT  = "#3b82f6"
SUCCESS = "#10b981"
DANGER  = "#ef4444"
WARNING = "#f59e0b"
BORDER  = "#334155"

STATUS_COLOR = {
    "available":   ("#10b981", "#d1fae5"),   # green bg, light fg
    "booked":      ("#ef4444", "#fee2e2"),   # red
    "maintenance": ("#f59e0b", "#fef3c7"),   # yellow
}
STATUS_LABEL = {
    "available":   "✅ Available",
    "booked":      "🔴 Booked",
    "maintenance": "🟡 Maintenance",
}


class RoomsPage:
    def __init__(self, parent, user, refresh_cb=None):
        self.parent = parent
        self.user = user
        self.refresh_cb = refresh_cb

        self.frame = tk.Frame(parent, bg=BG)
        self.frame.pack(fill="both", expand=True, padx=24, pady=20)

        self._build_header()
        self._build_legend()
        self._build_grid()

    def _build_header(self):
        hdr = tk.Frame(self.frame, bg=BG)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🛏  Room Management", font=("Arial", 18, "bold"),
                 bg=BG, fg=TEXT).pack(side="left")
        tk.Button(hdr, text="🔄 Refresh", font=("Arial", 10),
                  bg=ACCENT, fg=TEXT, relief="flat", cursor="hand2",
                  command=self._refresh, padx=10, pady=4).pack(side="right")
        tk.Label(self.frame, text="Click any room card to view details or change status.",
                 font=("Arial", 11), bg=BG, fg=MUTED).pack(anchor="w", pady=(4, 10))

    def _build_legend(self):
        leg = tk.Frame(self.frame, bg=BG)
        leg.pack(anchor="w", pady=(0, 10))
        for status, (bg, _) in STATUS_COLOR.items():
            dot = tk.Label(leg, text="  ●  " + STATUS_LABEL[status],
                           font=("Arial", 10, "bold"), bg=BG, fg=bg)
            dot.pack(side="left", padx=10)

    def _build_grid(self):
        # Scrollable canvas
        canvas = tk.Canvas(self.frame, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)

        self.grid_frame = tk.Frame(canvas, bg=BG)
        window = canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")

        def _on_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.grid_frame.bind("<Configure>", _on_configure)

        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        rooms = get_all_rooms()
        # Group by floor
        floors = {}
        for r in rooms:
            floors.setdefault(r["floor"], []).append(r)

        for floor in sorted(floors.keys()):
            floor_rooms = floors[floor]
            floor_label = {1: "Floor 1 — Standard", 2: "Floor 2 — Deluxe", 3: "Floor 3 — Suite"}
            tk.Label(self.grid_frame, text=f"  🏢  {floor_label.get(floor, f'Floor {floor}')}",
                     font=("Arial", 12, "bold"), bg=BG, fg=MUTED).grid(
                         row=(floor-1)*3, column=0, columnspan=10,
                         sticky="w", pady=(14, 4), padx=8)
            for i, room in enumerate(floor_rooms):
                self._room_card(room, row=(floor-1)*3+1, col=i)

    def _room_card(self, room, row, col):
        status = room["status"]
        bg_color, _ = STATUS_COLOR.get(status, ("#334155", TEXT))

        card = tk.Frame(self.grid_frame, bg=bg_color, width=110, height=110,
                        cursor="hand2", relief="flat")
        card.grid(row=row, column=col, padx=8, pady=6, sticky="nsew")
        card.pack_propagate(False)

        tk.Label(card, text=f"🏠", font=("Arial", 20), bg=bg_color, fg=TEXT).pack(pady=(12, 0))
        tk.Label(card, text=f"Room {room['room_number']}", font=("Arial", 10, "bold"),
                 bg=bg_color, fg=TEXT).pack()
        tk.Label(card, text=room["room_type"], font=("Arial", 8),
                 bg=bg_color, fg=TEXT).pack()
        tk.Label(card, text=f"৳{room['price_per_night']:,.0f}", font=("Arial", 9),
                 bg=bg_color, fg=TEXT).pack()

        for widget in [card] + card.winfo_children():
            widget.bind("<Button-1>", lambda e, r=room: self._room_detail(r))

        # Hover effect
        def on_enter(e, f=card, c=bg_color):
            f.config(highlightbackground=TEXT, highlightthickness=2, relief="solid")
        def on_leave(e, f=card, c=bg_color):
            f.config(highlightthickness=0, relief="flat")
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

    def _room_detail(self, room):
        dlg = tk.Toplevel(self.frame)
        dlg.title(f"Room {room['room_number']} — Details")
        dlg.configure(bg=CARD)
        dlg.geometry("400x360")
        dlg.resizable(False, False)
        dlg.grab_set()

        # Center
        dlg.update_idletasks()
        x = (dlg.winfo_screenwidth() - 400) // 2
        y = (dlg.winfo_screenheight() - 360) // 2
        dlg.geometry(f"400x360+{x}+{y}")

        bg_c, _ = STATUS_COLOR.get(room["status"], (CARD, TEXT))
        tk.Label(dlg, text=f"Room {room['room_number']}", font=("Arial", 22, "bold"),
                 bg=bg_c, fg=TEXT).pack(fill="x", pady=20)

        details = tk.Frame(dlg, bg=CARD, padx=20)
        details.pack(fill="both", expand=True)

        rows = [
            ("Floor",  str(room["floor"])),
            ("Type",   room["room_type"]),
            ("Price",  f"৳{room['price_per_night']:,.0f} / night"),
            ("Status", STATUS_LABEL.get(room["status"], room["status"])),
            ("Notes",  room.get("description") or "—"),
        ]
        for label, val in rows:
            row_f = tk.Frame(details, bg=CARD)
            row_f.pack(fill="x", pady=4)
            tk.Label(row_f, text=f"{label}:", font=("Arial", 10, "bold"),
                     bg=CARD, fg=MUTED, width=10, anchor="w").pack(side="left")
            tk.Label(row_f, text=val, font=("Arial", 11),
                     bg=CARD, fg=TEXT, anchor="w").pack(side="left")

        # Status change buttons (admin only)
        btn_frame = tk.Frame(details, bg=CARD)
        btn_frame.pack(fill="x", pady=16)

        status_options = [
            ("✅ Available", "available", SUCCESS),
            ("🔴 Booked",   "booked",   DANGER),
            ("🟡 Maintenance", "maintenance", WARNING),
        ]
        for label, st, color in status_options:
            tk.Button(btn_frame, text=label, font=("Arial", 9, "bold"),
                      bg=color, fg=TEXT, relief="flat", cursor="hand2", padx=8, pady=4,
                      command=lambda s=st, d=dlg, r=room: self._change_status(r["id"], s, d)).pack(
                          side="left", padx=4)

    def _change_status(self, room_id, status, dlg):
        update_room_status(room_id, status)
        dlg.destroy()
        if self.refresh_cb:
            self.refresh_cb()
        self._refresh()

    def _refresh(self):
        for w in self.frame.winfo_children():
            w.destroy()
        self._build_header()
        self._build_legend()
        self._build_grid()
