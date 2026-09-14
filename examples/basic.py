"""Configure a built-in source and iterate over records. No files or services needed."""

from pydatarheo import get_source


def main() -> None:
    # Configuration is explicit; the connector takes a snapshot of these records.
    source = get_source("memory", config={"records": [{"id": 1, "name": "Ada"}]})
    source.check()
    # read() is pull-based; no cache or database is created.
    for record in source.read():
        print(record)


if __name__ == "__main__":
    main()
