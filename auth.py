"""
Hotel Management System - Authentication Module
"""
import hashlib
from database import get_connection


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def login(username: str, password: str):
    """
    Verify credentials.
    Returns user dict on success, None on failure.
    """
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, _hash_password(password))
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def register(username: str, password: str, role: str, full_name: str):
    """
    Register a new user.
    Returns (True, user_id) on success, (False, error_message) on failure.
    """
    if len(username.strip()) < 3:
        return False, "Username must be at least 3 characters."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    conn = get_connection()
    existing = conn.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
    if existing:
        conn.close()
        return False, f"Username '{username}' already exists."

    cursor = conn.execute(
        "INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)",
        (username, _hash_password(password), role, full_name)
    )
    uid = cursor.lastrowid
    conn.commit()
    conn.close()
    return True, uid


def change_password(username: str, old_password: str, new_password: str):
    """Change a user's password. Returns (True, '') or (False, error)."""
    if not login(username, old_password):
        return False, "Current password is incorrect."
    if len(new_password) < 6:
        return False, "New password must be at least 6 characters."
    conn = get_connection()
    conn.execute("UPDATE users SET password=? WHERE username=?",
                 (_hash_password(new_password), username))
    conn.commit()
    conn.close()
    return True, ""


def get_all_users():
    conn = get_connection()
    rows = conn.execute("SELECT id, username, role, full_name, created_at FROM users").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_user(user_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
