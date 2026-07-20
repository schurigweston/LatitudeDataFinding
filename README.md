# SIM Usage Analyzer

Imports daily KORE Wireless usage reports into a SQLite database and provides
tools for querying and analyzing SIM usage.

## AI disclaimer

All the code was written by AI, including most of this README.md, with only minor changes by human. 
I'm the one that decided to use a database though. 

## Features

- Import ZIP-compressed daily usage reports
- Store data in SQLite
- Query SMS, voice, and data usage
- Export query results to CSV

## Project Structure

```
src/
    create_database.py
    import_usage_reports.py
    queries.py

data/
    input/
        DailyUsageReports/

sim_uses.db
```

## Requirements

- Python 3.11+
- Standard library only

## Usage

Create the database:

```bash
python src/create_database.py
```

Import reports:

```bash
python src/import_usage_reports.py
```

Run queries:

```bash
python src/queries.py
```

## Notes

Daily reports are expected to be ZIP files containing a single CSV.

The database (`sim_uses.db`) is generated locally and is not tracked by Git.