"""
Hotel Management System - Database Module
SQLite-based storage for all hotel data
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hotel.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():
    """Create all tables and seed default data if needed."""
    conn = get_connection()
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'receptionist',
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Hotel settings
    c.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    # Rooms table
    c.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT UNIQUE NOT NULL,
            room_type TEXT NOT NULL DEFAULT 'Standard',
            floor INTEGER DEFAULT 1,
            price_per_night REAL NOT NULL DEFAULT 1000.0,
            status TEXT NOT NULL DEFAULT 'available',
            description TEXT
        )
    """)

    # Guests table
    c.execute("""
        CREATE TABLE IF NOT EXISTS guests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            nid TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Bookings table
    c.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL,
            guest_id INTEGER NOT NULL,
            check_in DATE NOT NULL,
            check_out DATE NOT NULL,
            nights INTEGER NOT NULL DEFAULT 1,
            total_amount REAL NOT NULL DEFAULT 0,
            advance_paid REAL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'active',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (room_id) REFERENCES rooms(id),
            FOREIGN KEY (guest_id) REFERENCES guests(id)
        )
    """)

    # Invoices table
    c.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER NOT NULL,
            invoice_number TEXT UNIQUE NOT NULL,
            amount REAL NOT NULL,
            discount REAL DEFAULT 0,
            tax REAL DEFAULT 0,
            paid_amount REAL DEFAULT 0,
            status TEXT DEFAULT 'unpaid',
            issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (booking_id) REFERENCES bookings(id)
        )
    """)

    conn.commit()

    # Seed default settings
    defaults = {
        "hotel_name": "Grand Hotel",
        "hotel_address": "123 Main Street, Dhaka",
        "hotel_phone": "01700000000",
        "hotel_email": "info@grandhotel.com",
        "currency": "BDT",
        "tax_rate": "0",
    }
    for k, v in defaults.items():
        c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (k, v))

    # Seed default admin user (password: admin123)
    import hashlib
    def _hash(p):
        return hashlib.sha256(p.encode()).hexdigest()

    c.execute("INSERT OR IGNORE INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)",
              ("admin", _hash("admin123"), "admin", "Administrator"))

    # Seed rooms (30 rooms: floors 1-3, 10 per floor)
    room_types = {1: "Standard", 2: "Deluxe", 3: "Suite"}
    prices = {1: 1500, 2: 2500, 3: 4000}
    for floor in range(1, 4):
        for num in range(1, 11):
            rnum = f"{floor}{num:02d}"
            rtype = room_types[floor]
            price = prices[floor]
            c.execute("""
                INSERT OR IGNORE INTO rooms (room_number, room_type, floor, price_per_night, status)
                VALUES (?, ?, ?, ?, 'available')
            """, (rnum, rtype, floor, price))

    conn.commit()
    conn.close()


# ─────────────────────────────────────────────────
# Settings helpers
# ─────────────────────────────────────────────────
def get_settings():
    conn = get_connection()
    rows = conn.execute("SELECT key, value FROM settings").fetchall()
    conn.close()
    return {r["key"]: r["value"] for r in rows}


def set_setting(key, value):
    conn = get_connection()
    conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()


# ─────────────────────────────────────────────────
# Room helpers
# ─────────────────────────────────────────────────
def get_all_rooms():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM rooms ORDER BY room_number").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_room_status(room_id, status):
    conn = get_connection()
    conn.execute("UPDATE rooms SET status=? WHERE id=?", (status, room_id))
    conn.commit()
    conn.close()


def update_room(room_id, room_type, price, description):
    conn = get_connection()
    conn.execute("UPDATE rooms SET room_type=?, price_per_night=?, description=? WHERE id=?",
                 (room_type, price, description, room_id))
    conn.commit()
    conn.close()


# ─────────────────────────────────────────────────
# Guest helpers
# ─────────────────────────────────────────────────
def get_all_guests():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM guests ORDER BY full_name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_guest(full_name, phone, email, nid, address):
    conn = get_connection()
    c = conn.execute(
        "INSERT INTO guests (full_name, phone, email, nid, address) VALUES (?, ?, ?, ?, ?)",
        (full_name, phone, email, nid, address)
    )
    gid = c.lastrowid
    conn.commit()
    conn.close()
    return gid


def update_guest(gid, full_name, phone, email, nid, address):
    conn = get_connection()
    conn.execute(
        "UPDATE guests SET full_name=?, phone=?, email=?, nid=?, address=? WHERE id=?",
        (full_name, phone, email, nid, address, gid)
    )
    conn.commit()
    conn.close()


def delete_guest(gid):
    conn = get_connection()
    conn.execute("DELETE FROM guests WHERE id=?", (gid,))
    conn.commit()
    conn.close()


def search_guests(query):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM guests WHERE full_name LIKE ? OR phone LIKE ? OR nid LIKE ?",
        (f"%{query}%", f"%{query}%", f"%{query}%")
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────────
# Booking helpers
# ─────────────────────────────────────────────────
def get_all_bookings():
    conn = get_connection()
    rows = conn.execute("""
        SELECT b.*, r.room_number, r.room_type, g.full_name as guest_name, g.phone
        FROM bookings b
        JOIN rooms r ON b.room_id = r.id
        JOIN guests g ON b.guest_id = g.id
        ORDER BY b.created_at DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_active_bookings():
    conn = get_connection()
    rows = conn.execute("""
        SELECT b.*, r.room_number, r.room_type, g.full_name as guest_name, g.phone
        FROM bookings b
        JOIN rooms r ON b.room_id = r.id
        JOIN guests g ON b.guest_id = g.id
        WHERE b.status = 'active'
        ORDER BY b.check_in
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def create_booking(room_id, guest_id, check_in, check_out, nights, total, advance, notes):
    conn = get_connection()
    c = conn.execute("""
        INSERT INTO bookings (room_id, guest_id, check_in, check_out, nights,
                              total_amount, advance_paid, notes, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'active')
    """, (room_id, guest_id, check_in, check_out, nights, total, advance, notes))
    bid = c.lastrowid
    conn.execute("UPDATE rooms SET status='booked' WHERE id=?", (room_id,))
    conn.commit()
    conn.close()
    return bid


def cancel_booking(booking_id):
    conn = get_connection()
    row = conn.execute("SELECT room_id FROM bookings WHERE id=?", (booking_id,)).fetchone()
    if row:
        conn.execute("UPDATE rooms SET status='available' WHERE id=?", (row["room_id"],))
    conn.execute("UPDATE bookings SET status='cancelled' WHERE id=?", (booking_id,))
    conn.commit()
    conn.close()


def checkout_booking(booking_id):
    conn = get_connection()
    row = conn.execute("SELECT room_id FROM bookings WHERE id=?", (booking_id,)).fetchone()
    if row:
        conn.execute("UPDATE rooms SET status='available' WHERE id=?", (row["room_id"],))
    conn.execute("UPDATE bookings SET status='checked_out' WHERE id=?", (booking_id,))
    conn.commit()
    conn.close()


def search_bookings(query):
    conn = get_connection()
    rows = conn.execute("""
        SELECT b.*, r.room_number, r.room_type, g.full_name as guest_name, g.phone
        FROM bookings b
        JOIN rooms r ON b.room_id = r.id
        JOIN guests g ON b.guest_id = g.id
        WHERE g.full_name LIKE ? OR r.room_number LIKE ?
        ORDER BY b.created_at DESC
    """, (f"%{query}%", f"%{query}%")).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────────
# Invoice helpers
# ─────────────────────────────────────────────────
def create_invoice(booking_id, amount, discount, tax, paid_amount):
    conn = get_connection()
    import random, string
    inv_num = "INV-" + "".join(random.choices(string.digits, k=6))
    conn.execute("""
        INSERT INTO invoices (booking_id, invoice_number, amount, discount, tax, paid_amount, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (booking_id, inv_num, amount, discount, tax, paid_amount,
          "paid" if paid_amount >= amount else "partial"))
    conn.commit()
    conn.close()
    return inv_num


def get_invoice_by_booking(booking_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM invoices WHERE booking_id=? ORDER BY id DESC LIMIT 1",
                       (booking_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# ─────────────────────────────────────────────────
# Reports helpers
# ─────────────────────────────────────────────────
def get_dashboard_stats():
    conn = get_connection()
    total_rooms = conn.execute("SELECT COUNT(*) FROM rooms").fetchone()[0]
    booked = conn.execute("SELECT COUNT(*) FROM rooms WHERE status='booked'").fetchone()[0]
    available = conn.execute("SELECT COUNT(*) FROM rooms WHERE status='available'").fetchone()[0]
    maintenance = conn.execute("SELECT COUNT(*) FROM rooms WHERE status='maintenance'").fetchone()[0]
    today = conn.execute("""
        SELECT COALESCE(SUM(total_amount),0) FROM bookings
        WHERE DATE(created_at)=DATE('now') AND status='active'
    """).fetchone()[0]
    total_guests = conn.execute("SELECT COUNT(*) FROM guests").fetchone()[0]
    conn.close()
    return {
        "total_rooms": total_rooms,
        "booked": booked,
        "available": available,
        "maintenance": maintenance,
        "today_revenue": today,
        "total_guests": total_guests,
    }


def get_revenue_report(from_date, to_date):
    conn = get_connection()
    rows = conn.execute("""
        SELECT DATE(created_at) as date, COUNT(*) as bookings,
               SUM(total_amount) as revenue, SUM(advance_paid) as collected
        FROM bookings
        WHERE DATE(created_at) BETWEEN ? AND ? AND status != 'cancelled'
        GROUP BY DATE(created_at)
        ORDER BY date
    """, (from_date, to_date)).fetchall()
    conn.close()
    return [dict(r) for r in rows]
