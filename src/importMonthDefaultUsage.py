#This will run whever we grab new data. It will update 2 tables, the RawMonthDefaultUsage and RollingLastUsage tables. 

from pathlib import Path
import sqlite3
from config import DB_PATH
from zipCSVReader import get_single_csv_name, read_csv_rows
from fileHashTracker import compute_file_hash, has_been_loaded, record_loaded_file

REPORT_FOLDER = (
    Path(__file__).parent.parent
    / "data"
    / "input"
    / "MonthDefaultUsages"
)


def to_int(value):
    if value == "":
        return None
    return int(value)


def importMonthDefaultUsage(db_path=DB_PATH, report_folder=REPORT_FOLDER):

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
                    to_int(row["SmsUsageTotal"]),
                    to_int(row["DataUsageTotal"]),
                    to_int(row["VoiceUsageTotal"]),
                    row["SubscriptionId"],
                    row["OrgId"],
                    row["OrgUrn"],
                    row["SubscriptionUrn"],
                    row["Iccid"],
                    row["Msisdn"],
                    row["ServiceTypeId"],
                    row["ServiceTypeName"],
                    row["DataPlanId"],
                    row["DataPlanTypeId"],
                    row["DataPlanTypeName"],
                    row["DataPlanName"],
                    row["SmsPlanId"],
                    row["SmsPlanTypeId"],
                    row["SmsPlanTypeName"],
                    row["SmsPlanName"],
                    row["State"],
                    row["Eid"],
                    row["CostcenterId"],
                    row["CostcenterUrn"],
                    row["ProfileId"],
                    row["CustomFields"],
                    row["Imei"],
                    row["SmsLastUsageDate"],
                    row["VoiceLastUsageDate"],
                    row["DataLastUsageDate"],
                    row["CostCenterName"],
                    zip_path.name
                ))

            cursor.executemany("""
                INSERT INTO raw_month_default_usage (
                    SmsUsageTotal, DataUsageTotal, VoiceUsageTotal, SubscriptionId,
                    OrgId, OrgUrn, SubscriptionUrn, ICCID, Msisdn, ServiceTypeId,
                    ServiceTypeName, DataPlanId, DataPlanTypeId, DataPlanTypeName,
                    DataPlanName, SmsPlanId, SmsPlanTypeId, SmsPlanTypeName, SmsPlanName,
                    State, Eid, CostCenterId, CostCenterUrn, ProfileId, CustomFields,
                    Imei, SmsLastUsageDate, VoiceLastUsageDate, DataLastUsageDate,
                    CostCenterName, SourceFile
                ) VALUES (
                    ?,?,?,?,?,?,?,?,?,?,
                    ?,?,?,?,?,?,?,?,?,?,
                    ?,?,?,?,?,?,?,?,?,?,?
                )
            """, rows)

            record_loaded_file(conn, zip_path.name, file_hash, "raw_month_default_usage", len(rows))

            conn.commit()

            print(f"Imported {len(rows):,} rows")

    print("Done!")


if __name__ == "__main__":
    importMonthDefaultUsage()