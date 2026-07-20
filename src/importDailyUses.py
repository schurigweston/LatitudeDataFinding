from pathlib import Path
import sqlite3
import csv
import zipfile

DB_PATH = Path(__file__).parent.parent / "sim_uses_small_sample.db"

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

with sqlite3.connect(DB_PATH) as conn:

    cursor = conn.cursor()

    zip_files = sorted(REPORT_FOLDER.glob("*.zip"))

    for zip_path in zip_files:

        print(f"Importing {zip_path.name}")

        with zipfile.ZipFile(zip_path) as z:

            csv_names = [
                name
                for name in z.namelist()
                if name.lower().endswith(".csv")
            ]

            if len(csv_names) != 1:
                print("Skipping:", zip_path.name)
                continue

            with z.open(csv_names[0]) as csv_file:

                reader = csv.DictReader(
                    (line.decode("utf-8") for line in csv_file)
                )

                rows = []
                i = 0
                for row in reader:

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
                    i = i+1
                    if i >= 100:
                        break

                cursor.executemany("""
                    INSERT INTO usage VALUES (
                        ?,?,?,?,?,?,?,?,?,?,
                        ?,?,?,?,?,?,?,?,?,?,
                        ?,?,?
                    )
                """, rows)

        print(f"Imported {len(rows):,} rows")

print("Done!")