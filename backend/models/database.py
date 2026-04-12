import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "toolkit.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS samples (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                spec_file TEXT NOT NULL,
                path TEXT NOT NULL,
                method TEXT NOT NULL,
                request_body TEXT,
                response_body TEXT
                status_code INTEGER,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()
    conn.close()
    
def save_sample(spec_file, path, method, request_body, response_body, status_code):
    conn = get_db_connection()
    with conn:
        conn.execute("""
            INSERT INTO samples (spec_file, path, method, request_body, response_body, status_code, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            spec_file if spec_file else None,
            path,
            method,
            json.dumps(request_body) if request_body else None,
            json.dumps(response_body) if response_body else None,
            status_code,
            datetime.now().isoformat()
        ))
        conn.commit()
    conn.close()
    
def get_sampels(spec_file=None):
    conn = get_db_connection()
    if spec_file:
        rows = conn.execute("SELECT * FROM samples WHERE spec_file = ? ORDER BY created_at DESC", (spec_file,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM samples ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_samples(sample_id):
    conn = get_db_connection()
    with conn:
        conn.execute("DELETE FROM samples WHERE id = ?", (sample_id,))
        conn.commit()
    conn.close()