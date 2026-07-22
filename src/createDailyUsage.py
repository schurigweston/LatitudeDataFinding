#This makes the table for daily usages. It is append only. 

from pathlib import Path
import sqlite3
from config import DB_PATH

def createDailyUsageDatabase():
    with sqlite3.connect(DB_PATH) as conn:

        conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_usage (
            AccountId TEXT,
            SubscriptionId TEXT,
            CostCenterName TEXT,
            APN TEXT,
            ServiceType TEXT,
            AirtimeClass TEXT,
            ICCID TEXT,
            IMSI TEXT,
            MSISDN TEXT,
            IMEI TEXT,
            UsageType TEXT,
            ExactUsageTime TEXT,
            UsageAmount INTEGER,
            MNC TEXT,
            MCC TEXT,
            ParentOrgUrn TEXT,
            BilledOrgChild TEXT,
            SessionDuration INTEGER,
            UsageEndTime TEXT,
            CalledParty TEXT,
            UsageHash TEXT,
            CallingParty TEXT,
            SourceFile TEXT
        )
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_daily_usage_iccid
            ON daily_usage (ICCID)
        """)

if __name__ == "__main__":
    createDailyUsageDatabase()