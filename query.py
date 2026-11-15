"""Running queries against the flight database."""
from datetime import datetime
import math

def run_query(db: list[dict], query: dict) -> dict:
    """Return one response entry for one query object.

    Valid query:   {"query": query, "matches": [...]}
    Invalid query: {"query": query, "error": "INVALID_QUERY", "matches": []}
    """
    if not isinstance(query, dict):
        return {
            "query": query,
            "error": "INVALID_QUERY",
            "matches": []
        }

    record_keys = {
        "flight_id",
        "origin",
        "destination",
        "departure_datetime",
        "arrival_datetime",
        "price"
    }

    allowed_keys = record_keys | {
        "min_price",
        "sort_by",
        "order",
        "limit"
    }

    for key, value in query.items():

        if key not in allowed_keys:
            return {
                "query": query,
                "error": "INVALID_QUERY",
                "matches": []
            }

        if key in {"flight_id", "origin", "destination"}:
            if not isinstance(value, str):
                return {
                    "query": query,
                    "error": "INVALID_QUERY",
                    "matches": []
                }

        if key in {"departure_datetime", "arrival_datetime"}:
            if not isinstance(value, str):
                return {
                    "query": query,
                    "error": "INVALID_QUERY",
                    "matches": []
                }

            try:
                date_value = datetime.strptime(value, "%Y-%m-%d %H:%M")
                if date_value.strftime("%Y-%m-%d %H:%M") != value:
                    raise ValueError
            except ValueError:
                return {
                    "query": query,
                    "error": "INVALID_QUERY",
                    "matches": []
                }

        if key in {"price", "min_price"}:
            if (isinstance(value, bool)
                    or not isinstance(value, (int, float))
                    or not math.isfinite(value)):
                return {
                    "query": query,
                    "error": "INVALID_QUERY",
                    "matches": []
                }

        if key == "sort_by":
            if not isinstance(value, str) or value not in record_keys:
                return {
                    "query": query,
                    "error": "INVALID_QUERY",
                    "matches": []
                }

        if key == "order":
            
            if not isinstance(value, str) or value not in {"asc", "desc"}:
                return {
                    "query": query,
                    "error": "INVALID_QUERY",
                    "matches": []
                }

        if key == "limit":
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                return {
                    "query": query,
                    "error": "INVALID_QUERY",
                    "matches": []
                }

    if "order" in query and "sort_by" not in query:
        return {
            "query": query,
            "error": "INVALID_QUERY",
            "matches": []
        }

    matches = []

    for flight in db:
        if "flight_id" in query and flight["flight_id"] != query["flight_id"]:
            continue

        if "origin" in query and flight["origin"] != query["origin"]:
            continue

        if "destination" in query and flight["destination"] != query["destination"]:
            continue

        if ("departure_datetime" in query
                and flight["departure_datetime"] < query["departure_datetime"]):
            continue

        if ("arrival_datetime" in query
                and flight["arrival_datetime"] > query["arrival_datetime"]):
            continue

        if "price" in query and flight["price"] > query["price"]:
            continue

        if "min_price" in query and flight["price"] < query["min_price"]:
            continue

        matches.append(flight)

    if "sort_by" in query:
        sort_key = query["sort_by"]
        reverse = query.get("order", "asc") == "desc"

        matches = sorted(
            matches,
            key=lambda flight: flight[sort_key],
            reverse=reverse
        )

    if "limit" in query:
        matches = matches[:query["limit"]]
    return {
        "query": query,
        "matches": matches
    }

def run_queries(db: list[dict], queries: dict | list) -> list[dict]:
    """Accept one query object or a list of them; always return a list."""
    raise NotImplementedError
