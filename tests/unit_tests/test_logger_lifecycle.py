"""Repeated connector construction must close old file handles, not hide resource warnings."""

import logging

from datarheo import logs


def test_connector_logger_replacement_closes_all_previous_handlers(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(logs, "DATARHEO_LOGGING_ROOT", tmp_path)
    monkeypatch.setattr(logs, "get_global_file_logger", lambda: None)
    logger = logs.new_passthrough_file_logger("lifecycle-test")
    first = logger.handlers[0]
    second = logging.FileHandler(tmp_path / "second.log", encoding="utf-8")
    logger.addHandler(second)
    updated = logs.new_passthrough_file_logger("lifecycle-test")
    assert first.stream is None
    assert second.stream is None
    assert len(updated.handlers) == 1
    for handler in list(updated.handlers):
        updated.removeHandler(handler)
        handler.close()
