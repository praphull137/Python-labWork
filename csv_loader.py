"""Reading CSV files into flight records and error messages."""
import csv
from pathlib import Path
from validator import validate_row, to_record
def parse_files(paths: list[str], airports: set[str]) -> tuple[list[dict], list[str]]:
    """Process the CSV files in the order given.

    Return (records, errors):
      records - valid flight records, in input order
      errors  - one message per invalid row, in input order, formatted as
                "<file name>:<line number>: <ERROR_CODE> | <free text>"
                (base file name only, no timestamp or level, no newline)

    Also performs the DUPLICATE_FLIGHT check across all the files.
    Does not write any files and does not log anything itself.
    """
    records = []
    errors = []
    seen_flights = set()

    for path in paths:
        with open(path, "r", encoding="utf-8", newline="") as file:
            for line_number, line in enumerate(file, start=1):

                if line_number == 1:
                    continue

                if not line.strip() or line.lstrip().startswith("#"):
                    continue

                fields = next(csv.reader([line]))
                fields = [field.strip() for field in fields]

                error = validate_row(fields, airports)
                file_name = Path(path).name
                original_line = line.rstrip("\r\n")

                if error is not None:
                    errors.append(
                        f"{file_name}:{line_number}: {error} | {original_line}"
                    )
                    continue

                flight = to_record(fields)
                flight_key = (
                    flight["flight_id"],
                    flight["departure_datetime"]
                )

                if flight_key in seen_flights:
                    errors.append(
                        f"{file_name}:{line_number}: DUPLICATE_FLIGHT | {original_line}"
                    )
                    continue

                seen_flights.add(flight_key)
                records.append(flight)

    return records, errors