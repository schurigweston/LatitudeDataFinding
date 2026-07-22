from pathlib import Path
import sqlite3
from config import DB_PATH


def createSimsInventory():
    with sqlite3.connect(DB_PATH) as conn:

        conn.execute("""
        CREATE TABLE IF NOT EXISTS sim_inventory (
            ServiceTypeName TEXT,
            ICCID TEXT,
            Eid TEXT,
            Msisdn TEXT,
            Imsi TEXT,
            CreatedDate TEXT,
            IpAddress TEXT,
            ApnFeature TEXT,
            State TEXT,
            ServiceTypeId TEXT,
            Imei TEXT,
            ProductOffer TEXT,
            DataPlan TEXT,
            CostCenterId TEXT,
            CostCenterName TEXT,
            Model TEXT,
            Serial TEXT,
            SubscriptionId TEXT,
            LastStockedDate TEXT,
            LastActivatedDate TEXT,
            LastSuspendedDate TEXT,
            LastDeactivatedDate TEXT,
            StockOrderRequestId TEXT,
            SessionStatus TEXT,
            ProfileRole TEXT,
            State_Alt TEXT,
            ProfileRole_Alt TEXT,
            DataFeature TEXT,
            SmsFeature TEXT,
            VoiceFeature TEXT,
            RoamingFeature TEXT,
            OtherFeature TEXT,
            ProfileId TEXT,
            Apn TEXT,
            CustomerAddress TEXT,
            CustomerName TEXT,
            CustomerNumber TEXT,
            FirmwareVersion TEXT,
            Imei_Alt TEXT,
            OrderNumber TEXT,
            SourceFile TEXT
        )
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_sim_inventory_iccid
            ON sim_inventory (ICCID)
        """)


if __name__ == "__main__":
    createSimsInventory()