"""Shared, isolated sample data; no network services or credentials."""

import json

import pytest


@pytest.fixture
def records():
    return [{"id": 1, "name": "Ada", "amount": 10}, {"id": 2, "name": "Lin", "amount": 20}]


@pytest.fixture
def jsonl_path(tmp_path, records):
    path = tmp_path / "records.jsonl"
    path.write_text("\n".join(json.dumps(row) for row in records) + "\n", encoding="utf-8")
    return path


@pytest.fixture
def csv_path(tmp_path):
    path = tmp_path / "records.csv"
    path.write_text("id,name,amount\n1,Ada,10\n2,Lin,20\n", encoding="utf-8")
    return path
