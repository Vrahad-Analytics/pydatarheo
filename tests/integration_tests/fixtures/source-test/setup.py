#
# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
#
from __future__ import annotations

from setuptools import setup

setup(
    name="datarheo-source-test",
    version="0.0.1",
    description="Test Source",
    author="Vrahad Analytics",
    author_email="ardb40@gmail.com",
    packages=["source_test"],
    entry_points={
        "console_scripts": [
            "source-test=source_test.run:run",
        ],
    },
)
