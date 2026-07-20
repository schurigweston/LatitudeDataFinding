import sqlite3
import csv

DATABASE = "sim_uses.db"
TABLE = "usage"
OUTPUT = "usage.csv"

with sqlite3.connect(DATABASE) as conn:
    cursor = conn.cursor()

    # Read all rows
    cursor.execute(f"SELECT * FROM {TABLE}")
    rows = cursor.fetchall()

    # Get the column names
    headers = [description[0] for description in cursor.description]

with open(OUTPUT, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(headers)
    writer.writerows(rows)

print(f"Exported {len(rows):,} rows to {OUTPUT}")