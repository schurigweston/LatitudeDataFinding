#This creates the table that is only really concerned with when things were last used. 

from pathlib import Path
import sqlite3
from config import DB_PATH

def createRollingLastUsage():
    with sqlite3.connect(DB_PATH) as conn:

        conn.execute("""
        CREATE TABLE IF NOT EXISTS last_usage (
            ICCID TEXT,
            SmsLastUsageDate TEXT,
            VoiceLastUsageDate Text,
            DataLastUsageDate Text,
            AnyLastUsageDate Text
        )
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_last_usage_iccid
            ON last_usage (ICCID)
        """)

if __name__ == "__main__":
    createRollingLastUsage()