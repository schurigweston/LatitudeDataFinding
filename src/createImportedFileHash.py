from pathlib import Path
import sqlite3
from config import DB_PATH


def createImportedFileHash():
    with sqlite3.connect(DB_PATH) as conn:

        conn.execute("""
        CREATE TABLE IF NOT EXISTS loaded_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            file_hash TEXT NOT NULL,
            target_table TEXT,
            loaded_at TEXT DEFAULT CURRENT_TIMESTAMP,
            row_count INTEGER,
            UNIQUE(file_hash)
        )
        """)


if __name__ == "__main__":
    createImportedFileHash()