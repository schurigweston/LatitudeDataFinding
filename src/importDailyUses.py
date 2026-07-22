from pathlib import Path
import sqlite3
from config import DB_PATH
from zipCSVReader import get_single_csv_name, read_csv_rows
from fileHashTracker import compute_file_hash, has_been_loaded, record_loaded_file

REPORT_FOLDER = (
    Path(__file__).parent.parent
    / "data"
    / "input"
    / "DailyUsageReports"
)


def to_int(value):
    if value == "":
        return None
    return int(value)


def importDailyUses(db_path=DB_PATH, report_folder=REPORT_FOLDER):

    with sqlite3.connect(db_path) as conn:

        cursor = conn.cursor()

        zip_files = sorted(report_folder.glob("*.zip"))

        for zip_path in zip_files:

            file_hash = compute_file_hash(zip_path)

            if has_been_loaded(conn, file_hash):
                print(f"Already imported, skipping: {zip_path.name}")
                continue

            print(f"Importing {zip_path.name}")

            csv_name = get_single_csv_name(zip_path)

            if csv_name is None:
                print("Skipping:", zip_path.name)
                continue

            rows = []
            i = 0  # used for when I want only X entries
            for row in read_csv_rows(zip_path, csv_name):

                if db_path.name == "SIM_USAGE_TESTING.db":
                    i = i + 1
                    if i > 100:
                        break

                rows.append((
                    row["AccountId"],
                    row["SubscriptionId"],
                    row["CostCenterName"],
                    row["APN"],
                    row["ServiceType"],
                    row["AirtimeClass"],
                    row["ICCID"],
                    row["IMSI"],
                    row["MSISDN"],
                    row["IMEI"],
                    row["UsageType"],
                    row["ExactUsageTime"],
                    to_int(row["UsageAmount"]),
                    to_int(row["MNC"]),
                    to_int(row["MCC"]),
                    row["ParentOrgUrn"],
                    row["BilledOrgChild"],
                    to_int(row["SessionDuration"]),
                    row["UsageEndTime"],
                    row["CalledParty"],
                    row["UsageHash"],
                    row["CallingParty"],
                    zip_path.name
                ))

            cursor.executemany("""
                INSERT INTO daily_usage (
                    AccountId, SubscriptionId, CostCenterName, APN,
                    ServiceType, AirtimeClass, ICCID, IMSI, MSISDN, IMEI,
                    UsageType, ExactUsageTime, UsageAmount, MNC, MCC,
                    ParentOrgUrn, BilledOrgChild, SessionDuration,
                    UsageEndTime, CalledParty, UsageHash, CallingParty,
                    SourceFile
                ) VALUES (
                    ?,?,?,?,?,?,?,?,?,?,
                    ?,?,?,?,?,?,?,?,?,?,
                    ?,?,?
                )
            """, rows)
            
            record_loaded_file(conn, zip_path.name, file_hash, "daily_usage", len(rows))

            conn.commit()

            print(f"Imported {len(rows):,} rows")

            

    print("Done!")


if __name__ == "__main__":
    importDailyUses()