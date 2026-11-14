
"""Row validation: airport list loading, single-row checks, record building."""
from datetime import datetime
import math
def load_airports(path: str) -> set[str]:
    """Read an airport list file and return the set of codes.

    One code per line. Strip whitespace; skip blank lines and lines
    starting with '#'.
    """
    airports = set()

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            code = line.strip()
            if code and not code.startswith("#"):
                airports.add(code)

    return airports


def validate_row(fields: list[str], airports: set[str]) -> str | None:
    """Check one CSV row (fields as returned by csv.reader, not yet stripped).

    Return None if the row is valid, otherwise the error code of the
    FIRST failing check (checks 1-11 in the specification, in order).
    Does not check for duplicates.
    """
    if len(fields) != 6:
        return "WRONG_FIELD_COUNT"

    fields = [field.strip() for field in fields]

    if any(field == "" for field in fields):
        return "MISSING_FIELD"

    flight_id, origin, destination, departure, arrival, price = fields

    if not (2 <= len(flight_id) <= 8 and flight_id.isascii() and flight_id.isalnum()):
        return "INVALID_FLIGHT_ID"

    if len(origin) != 3 or not origin.isascii() or not origin.isalpha() or not origin.isupper() or origin not in airports:
        return "INVALID_ORIGIN"

    if len(destination) != 3 or not destination.isascii() or not destination.isalpha() or not destination.isupper() or destination not in airports:
        return "INVALID_DESTINATION"

    if origin == destination:
        return "SAME_ORIGIN_DESTINATION"

    try:
        departure_time = datetime.strptime(departure, "%Y-%m-%d %H:%M")
        if departure_time.strftime("%Y-%m-%d %H:%M") != departure:
            return "INVALID_DEPARTURE"
    except ValueError:
        return "INVALID_DEPARTURE"

    try:
        arrival_time = datetime.strptime(arrival, "%Y-%m-%d %H:%M")
        if arrival_time.strftime("%Y-%m-%d %H:%M") != arrival:
            return "INVALID_ARRIVAL"
    except ValueError:
        return "INVALID_ARRIVAL"

    if arrival_time <= departure_time:
        return "ARRIVAL_NOT_AFTER_DEPARTURE"

    try:
        flight_price = float(price)
    except ValueError:
        return "INVALID_PRICE"

    
    if not math.isfinite(flight_price):
        return "INVALID_PRICE"

    if flight_price <= 0:
        return "NON_POSITIVE_PRICE"

    return None


def to_record(fields: list[str]) -> dict:
    """Turn a valid row into a flight record dictionary.

    Keys: flight_id, origin, destination, departure_datetime,
    arrival_datetime (stripped strings) and price (float).
    """
    fields = [field.strip() for field in fields]

    return {
        "flight_id": fields[0],
        "origin": fields[1],
        "destination": fields[2],
        "departure_datetime": fields[3],
        "arrival_datetime": fields[4],
        "price": float(fields[5])
    }
