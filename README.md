# SIM Usage Analyzer

Imports daily KORE Wireless usage reports into a SQLite database and provides
tools for querying and analyzing SIM usage.

## AI disclaimer

All the code was written by AI, including most of this README.md, with only minor changes by human. 
I'm the one that decided to use a database though, so there. 

## Features

- Import ZIP-compressed daily usage reports
- Store data in SQLite
- Query SMS, voice, and data usage
- Export query results to CSV

## Project Structure

```
src/
    code and scripts

data/
    input/
        DailyUsageReports/
        other things

sim_uses.db
```

## Requirements

- Python 3.11+
- Standard library only

## Usage

I'll need to update usage at the end.

## Notes

Daily reports are expected to be ZIP files containing a single CSV.

The database (`sim_uses.db`) is generated locally and is not tracked by Git.