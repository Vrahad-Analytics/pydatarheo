"""Read sample sales, transform values, and write an atomic JSONL result."""

from __future__ import annotations

import argparse
from pathlib import Path

from pydatarheo import JsonlSink, get_source, transform_records


def run(output: Path) -> int:
    # Use a checked-in local source so this example works offline without secrets.
    source = get_source("csv", config={"path": str(Path(__file__).parent / "data" / "sales.csv")})
    source.check()
    # CSV preserves strings. Convert amounts explicitly and keep integer cents exact.
    records = transform_records(
        source.read(),
        lambda row: {
            "id": int(row["id"]),
            "customer": row["customer"],
            "total_cents": int(row["quantity"]) * int(row["unit_cents"]),
        },
    )
    # The sink refuses an existing output and never publishes a partial result.
    return JsonlSink(output).write(records)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    count = run(args.output)
    print(f"Wrote {count} sales records")


if __name__ == "__main__":
    main()
