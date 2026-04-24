import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

DB_DIR = Path.home() / ".oracle"
DB_PATH = DB_DIR / "db.sqlite3"


def _connect() -> sqlite3.Connection:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the links table if it does not exist."""
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS links (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                code        TEXT    NOT NULL UNIQUE,
                original_url TEXT   NOT NULL UNIQUE,
                created_at  TEXT    NOT NULL
            )
        """)


def get_by_url(url: str) -> Optional[sqlite3.Row]:
    """Return the row for an existing URL, or None."""
    with _connect() as conn:
        return conn.execute(
            "SELECT * FROM links WHERE original_url = ?", (url,)
        ).fetchone()


def get_by_code(code: str) -> Optional[sqlite3.Row]:
    """Return the row for a given short code, or None."""
    with _connect() as conn:
        return conn.execute(
            "SELECT * FROM links WHERE code = ?", (code,)
        ).fetchone()


def code_exists(code: str) -> bool:
    """Return True if a short code is already taken."""
    return get_by_code(code) is not None


def insert(code: str, url: str) -> sqlite3.Row:
    """Insert a new link and return the created row."""
    created_at = datetime.now(timezone.utc).isoformat()
    with _connect() as conn:
        conn.execute(
            "INSERT INTO links (code, original_url, created_at) VALUES (?, ?, ?)",
            (code, url, created_at),
        )
    return get_by_code(code)


def list_all() -> list[sqlite3.Row]:
    """Return all rows ordered by creation time."""
    with _connect() as conn:
        return conn.execute(
            "SELECT * FROM links ORDER BY created_at ASC"
        ).fetchall()


def delete(code: str) -> bool:
    """Delete a link by short code. Returns True if a row was removed."""
    with _connect() as conn:
        cursor = conn.execute("DELETE FROM links WHERE code = ?", (code,))
        return cursor.rowcount > 0
