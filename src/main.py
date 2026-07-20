import sqlite3

with sqlite3.connect("sim_uses.db") as source:
    rows = source.execute("""
        SELECT DISTINCT
            ICCID
        FROM usage
        WHERE CalledParty = '00000000000000000911';
    """).fetchall()

with sqlite3.connect("called911AtLeastOnce.db") as dest:
    dest.execute("""
        CREATE TABLE IF NOT EXISTS sms (
            ICCID TEXT
        )
    """)

    dest.executemany(
        "INSERT INTO sms VALUES (?)",
        rows
    )