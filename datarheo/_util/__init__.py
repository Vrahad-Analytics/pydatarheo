# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""Internal utility functions for dealing with pip.

Note: This module is for internal use only and it should not be depended upon for production use.
It is subject to change without notice.
"""

from __future__ import annotations

from datarheo._util.pip_util import connector_pip_url, github_pip_url


__all__ = [
    "connector_pip_url",
    "github_pip_url",
]
