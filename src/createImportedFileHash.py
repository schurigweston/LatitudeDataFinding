#This will hold all the already imported files for default usage and daily usage, so we don't have repeats. 

from pathlib import Path
import sqlite3
from config import DB_PATH

def createImportedFilehash():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS already_imported_file_hashes (
            SourceFile TEXT,
            HashCode TEXT
        )
        """)

if __name__ == "__main__":
    createImportedFilehash()