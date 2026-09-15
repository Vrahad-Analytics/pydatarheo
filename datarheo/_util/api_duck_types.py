# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""A set of duck-typed classes for working with the cloud API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    import requests


class DataRheoApiResponseDuckType(Protocol):
    """Used for duck-typing various API responses."""

    content_type: str
    r"""HTTP response content type for this operation"""
    status_code: int
    r"""HTTP response status code for this operation"""
    raw_response: requests.Response
    r"""Raw HTTP response; suitable for custom response parsing"""
