import zipfile
import csv


def get_single_csv_name(zip_path):
    """Return the one CSV name inside a zip, or None if zero/multiple exist."""
    with zipfile.ZipFile(zip_path) as z:
        csv_names = [
            name
            for name in z.namelist()
            if name.lower().endswith(".csv")
        ]
        if len(csv_names) != 1:
            return None
        return csv_names[0]


def read_csv_rows(zip_path, csv_name):
    """Yield DictReader rows from a single CSV inside a zip."""
    with zipfile.ZipFile(zip_path) as z:
        with z.open(csv_name) as csv_file:
            reader = csv.DictReader(
                (line.decode("utf-8") for line in csv_file)
            )
            yield from reader