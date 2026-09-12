# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""Smoke test source for destination regression testing.

This module provides a synthetic data source that generates test data
covering common edge cases that break destinations: type variations,
null handling, naming edge cases, schema variations, and batch sizes.

.. warning::
    This module is experimental and subject to change without notice.
    The APIs and behavior may be modified or removed in future versions.
"""

from datarheo.cli.smoke_test_source.source import SourceSmokeTest


__all__ = [
    "SourceSmokeTest",
]
