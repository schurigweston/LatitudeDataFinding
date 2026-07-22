import re
from datetime import datetime
from pathlib import Path
import sqlite3
from config import DB_PATH
from zipCSVReader import get_single_csv_name, read_csv_rows

REPORT_FOLDER = (
    Path(__file__).parent.parent
    / "data"
    / "input"
    / "SimsInventory"
)

FILENAME_PATTERN = re.compile(r"simsInventory(\d{17})\.zip$", re.IGNORECASE)

EXPECTED_HEADER = [
    "ServiceTypeName", "Iccid_esn", "Eid", "Msisdn", "Imsi", "CreatedDate",
    "IpAddress", "ApnFeature", "State", "ServiceTypeId", "Imei",
    "ProductOffer", "DataPlan", "CostCenterId", "CostCenterName", "Model",
    "Serial", "SubscriptionId", "LastStockedDate", "LastActivatedDate",
    "LastSuspendedDate", "LastDeactivatedDate", "StockOrderRequestId",
    "SessionStatus", "ProfileRole", "[State]", "[Profile Role]",
    "[Data Feature]", "[SMS Feature]", "[Voice Feature]",
    "[Roaming Feature]", "[Other Feature]", "[Profile ID]", "[APN]",
    "[Customer Address]", "[Customer Name]", "[Customer Number]",
    "[Firmware Version ]", "[IMEI]", "[Order Number]"
]


def parse_timestamp(filename):
    match = FILENAME_PATTERN.match(filename)
    if match is None:
        return None

    digits = match.group(1)
    year   = int(digits[0:4])
    month  = int(digits[4:6])
    day    = int(digits[6:8])
    hour   = int(digits[8:10])
    minute = int(digits[10:12])
    second = int(digits[12:14])
    millis = int(digits[14:17])

    try:
        return datetime(year, month, day, hour, minute, second, millis * 1000)
    except ValueError:
        return None


def pick_inventory_file(folder):
    files = sorted(folder.glob("*.zip"))

    if not files:
        raise FileNotFoundError(f"No zip files found in {folder}")

    if len(files) == 1:
        return files[0]

    parsed = []
    for f in files:
        ts = parse_timestamp(f.name)
        if ts is None:
            raise ValueError(f"Unrecognized filename format: {f.name}")
        parsed.append((ts, f))

    parsed.sort(key=lambda pair: pair[0])
    return parsed[-1][1]


def validate_header(fieldnames):
    if fieldnames != EXPECTED_HEADER:
        raise ValueError(
            "SIM inventory file header does not match the expected columns.\n"
            "Please re-download the export from KORE with 'select all' "
            "columns chosen, and try again.\n"
            f"Expected: {EXPECTED_HEADER}\n"
            f"Got:      {fieldnames}"
        )


def importSimInventory(db_path=DB_PATH, report_folder=REPORT_FOLDER):

    zip_path = pick_inventory_file(report_folder)

    print(f"Importing {zip_path.name}")

    csv_name = get_single_csv_name(zip_path)

    if csv_name is None:
        raise ValueError(f"Expected exactly one CSV inside {zip_path.name}")

    rows_iter = read_csv_rows(zip_path, csv_name)

    # peek at the header via the underlying DictReader's fieldnames
    import zipfile
    import csv
    with zipfile.ZipFile(zip_path) as z:
        with z.open(csv_name) as csv_file:
            reader = csv.DictReader(
                (line.decode("utf-8") for line in csv_file)
            )
            validate_header(reader.fieldnames)

    rows = []
    for row in read_csv_rows(zip_path, csv_name):
        rows.append((
            row["ServiceTypeName"],
            row["Iccid_esn"],
            row["Eid"],
            row["Msisdn"],
            row["Imsi"],
            row["CreatedDate"],
            row["IpAddress"],
            row["ApnFeature"],
            row["State"],
            row["ServiceTypeId"],
            row["Imei"],
            row["ProductOffer"],
            row["DataPlan"],
            row["CostCenterId"],
            row["CostCenterName"],
            row["Model"],
            row["Serial"],
            row["SubscriptionId"],
            row["LastStockedDate"],
            row["LastActivatedDate"],
            row["LastSuspendedDate"],
            row["LastDeactivatedDate"],
            row["StockOrderRequestId"],
            row["SessionStatus"],
            row["ProfileRole"],
            row["[State]"],
            row["[Profile Role]"],
            row["[Data Feature]"],
            row["[SMS Feature]"],
            row["[Voice Feature]"],
            row["[Roaming Feature]"],
            row["[Other Feature]"],
            row["[Profile ID]"],
            row["[APN]"],
            row["[Customer Address]"],
            row["[Customer Name]"],
            row["[Customer Number]"],
            row["[Firmware Version ]"],
            row["[IMEI]"],
            row["[Order Number]"],
            zip_path.name
        ))

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute("DELETE FROM sim_inventory")

        cursor.executemany("""
                    INSERT INTO sim_inventory (
                        ServiceTypeName, ICCID, Eid, Msisdn, Imsi, CreatedDate,
                        IpAddress, ApnFeature, State, ServiceTypeId, Imei,
                        ProductOffer, DataPlan, CostCenterId, CostCenterName,
                        Model, Serial, SubscriptionId, LastStockedDate,
                        LastActivatedDate, LastSuspendedDate, LastDeactivatedDate,
                        StockOrderRequestId, SessionStatus, ProfileRole,
                        State_Alt, ProfileRole_Alt, DataFeature, SmsFeature,
                        VoiceFeature, RoamingFeature, OtherFeature, ProfileId,
                        Apn, CustomerAddress, CustomerName, CustomerNumber,
                        FirmwareVersion, Imei_Alt, OrderNumber, SourceFile
                    ) VALUES (
                        ?,?,?,?,?,?,?,?,?,?,
                        ?,?,?,?,?,?,?,?,?,?,
                        ?,?,?,?,?,?,?,?,?,?,
                        ?,?,?,?,?,?,?,?,?,?,
                        ?
                    )
                """, rows)

        conn.commit()

    print(f"Imported {len(rows):,} rows")
    print("Done!")


if __name__ == "__main__":
    importSimInventory()