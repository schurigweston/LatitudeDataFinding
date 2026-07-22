import hashlib
import sqlite3


def compute_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def has_been_loaded(conn, file_hash):
    cursor = conn.execute(
        "SELECT 1 FROM loaded_files WHERE file_hash = ?",
        (file_hash,)
    )
    return cursor.fetchone() is not None


def record_loaded_file(conn, filename, file_hash, target_table, row_count):
    conn.execute("""
        INSERT INTO loaded_files (filename, file_hash, target_table, row_count)
        VALUES (?, ?, ?, ?)
    """, (filename, file_hash, target_table, row_count))