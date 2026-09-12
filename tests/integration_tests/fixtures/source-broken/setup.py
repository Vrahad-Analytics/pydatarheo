#
# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
#
from __future__ import annotations

from setuptools import setup

setup(
    name="datarheo-source-broken",
    version="0.0.1",
    description="Test Soutce",
    author="Vrahad Analytics",
    author_email="ardb40@gmail.com",
    packages=["source_broken"],
    entry_points={
        "console_scripts": [
            "source-broken=source_broken.run:run",
        ],
    },
)
