#This does append-only, needs to skip files or rows that already exist because they are duplicates and shouldn't be in there. 
#This is where all MonthDefaultUsages will be stored. 

from pathlib import Path
import sqlite3
from config import DB_PATH


def createAllRawMonthDefaultUsage():
    with sqlite3.connect(DB_PATH) as conn:

        conn.execute("""
        CREATE TABLE IF NOT EXISTS raw_month_default_usage (
            SmsUsageTotal INTEGER,
            DataUsageTotal INTEGER,
            VoiceUsageTotal INTEGER,
            SubscriptionId TEXT,
            OrgId TEXT,
            OrgUrn TEXT,
            SubscriptionUrn TEXT,
            ICCID TEXT,
            Msisdn TEXT,
            ServiceTypeId TEXT,
            ServiceTypeName TEXT,
            DataPlanId TEXT,
            DataPlanTypeId TEXT,
            DataPlanTypeName TEXT,
            DataPlanName TEXT,
            SmsPlanId TEXT,
            SmsPlanTypeId TEXT,
            SmsPlanTypeName TEXT,
            SmsPlanName TEXT,
            State TEXT,
            Eid	TEXT,
            CostCenterId TEXT,
            CostCenterUrn TEXT,
            ProfileId TEXT,
            CustomFields TEXT,
            Imei TEXT,
            SmsLastUsageDate TEXT,
            VoiceLastUsageDate TEXT,
            DataLastUsageDate TEXT,
            CostCenterName TEXT,
            SourceFile TEXT

        )
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_raw_month_default_usage_iccid
            ON raw_month_default_usage (ICCID)
        """)

if __name__ == "__main__":
    createAllRawMonthDefaultUsage()