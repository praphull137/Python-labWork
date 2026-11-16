
"""Flight Schedule Parser and Query Tool - command-line entry point.

Run from the project folder, for example:
    python flight_parser.py -i data/db.csv -a data/airports.txt
"""
import sys
import argparse
import json
import logging
from datetime import datetime
from pathlib import Path

from validator import load_airports
from csv_loader import parse_files
from query import run_queries

# TODO: fill in your details: plain ASCII, no spaces or underscores.
STUDENT_ID = "251ADB002"
FIRST_NAME = "Praphull"
LAST_NAME = "KumarPandey"

def main(argv: list[str] | None = None) -> int:
    """Run the whole program and return the exit code (0, 1 or 2).

    argv is the argument list without the program name.
    None means use sys.argv[1:] (argparse does this for you).
    Do not call sys.exit() inside main(); return the code instead.
    """
    parser = argparse.ArgumentParser()

    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("-i", metavar="FILE")
    source.add_argument("-d", metavar="FOLDER")
    source.add_argument("-j", metavar="FILE")

    parser.add_argument("-a", metavar="FILE")
    parser.add_argument("-o", metavar="FILE")
    parser.add_argument("-q", metavar="FILE")
    parser.add_argument("-r", metavar="FOLDER", default=".")

    args = parser.parse_args(argv)

    if args.i or args.d:
        if not args.a:
            parser.error("-a is required with -i or -d")

    if args.j and args.o:
        parser.error("-o cannot be used with -j")

    logger = logging.getLogger("flight_parser")
    logger.setLevel(logging.INFO)

    handler = None

    try:
        if args.i:
            csv_paths = [args.i]

        elif args.d:
            folder = Path(args.d)

            if not folder.is_dir():
                raise FileNotFoundError(f"Folder does not exist: {args.d}")

            csv_paths = sorted(
                str(path) for path in folder.iterdir()
                if path.is_file() and path.name.endswith(".csv")
            )

            if not csv_paths:
                raise FileNotFoundError("No CSV files found in the folder")

        else:
            csv_paths = []

        if args.i or args.d:
            airports = load_airports(args.a)
            records, errors = parse_files(csv_paths, airports)

            output_path = Path(args.o) if args.o else Path("db.json")
            output_path.parent.mkdir(parents=False, exist_ok=True) if False else None

            with open(output_path, "w", encoding="utf-8") as file:
                json.dump(records, file, indent=4)

            log_path = output_path.parent / "errors.log"

            handler = logging.FileHandler(
                log_path,
                mode="w",
                encoding="utf-8"
            )
            handler.setFormatter(logging.Formatter(
                "%(asctime)s %(levelname)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            ))
            logger.addHandler(handler)

            for error in errors:
                logger.warning(error)

            db = records

        else:
            with open(args.j, "r", encoding="utf-8") as file:
                db = json.load(file)

            if not isinstance(db, list) or not all(
                isinstance(record, dict) for record in db
            ):
                raise ValueError("Database JSON must be an array of objects")

        if args.q:
            with open(args.q, "r", encoding="utf-8") as file:
                queries = json.load(file)

            if isinstance(queries, dict):
                pass
            elif isinstance(queries, list):
                if not all(isinstance(query, dict) for query in queries):
                    raise ValueError("Query JSON array must contain objects")
            else:
                raise ValueError("Query JSON must be an object or an array")

            responses = run_queries(db, queries)

            response_folder = Path(args.r)
            response_name = (
                f"response_{STUDENT_ID}_{FIRST_NAME}_{LAST_NAME}_"
                f"{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            )

            response_path = response_folder / response_name

            with open(response_path, "w", encoding="utf-8") as file:
                json.dump(responses, file, indent=4)

        return 0

    except (OSError, json.JSONDecodeError, UnicodeDecodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    finally:
        if handler is not None:
            logger.removeHandler(handler)
            handler.close()


if __name__ == "__main__":
    sys.exit(main())
