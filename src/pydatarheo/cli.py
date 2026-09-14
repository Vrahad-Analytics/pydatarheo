"""Minimal local-file pipeline CLI; never installs or executes external connectors."""

from __future__ import annotations

import argparse

from pydatarheo import DatarheoError, JsonlSink, __version__, get_source


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pydatarheo", description="Vrahad native data pipelines")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    read = commands.add_parser("read", help="Read local CSV/JSONL into a new JSONL file")
    read.add_argument("--source", choices=("csv", "jsonl"), required=True)
    read.add_argument("--input", required=True)
    read.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        source = get_source(args.source, config={"path": args.input})
        source.check()
        count = JsonlSink(args.output).write(source.read())
    except DatarheoError as error:
        parser.exit(1, f"Error: {error}\n")
    print(f"Wrote {count} records")
    return 0
