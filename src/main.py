import sqlite3

with sqlite3.connect("sim_uses.db") as source:
    rows = source.execute("""
        SELECT DISTINCT
            CalledParty
        FROM usage
        WHERE ICCID = '89010303300162373014'
          AND UsageType = 'SMS-MT';
    """).fetchall()

with sqlite3.connect("uniqueIncomginMessages89010303300162373014.db") as dest:
    dest.execute("""
        CREATE TABLE IF NOT EXISTS sms (
            CalledParty TEXT
        )
    """)

    dest.executemany(
        "INSERT INTO sms VALUES (?)",
        rows
    )