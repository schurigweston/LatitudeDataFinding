from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).parent.parent / "sim_uses_small_sample.db"

with sqlite3.connect(DB_PATH) as conn:

    conn.execute("""
    CREATE TABLE IF NOT EXISTS usage (
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
        MNC INTEGER,
        MCC INTEGER,
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