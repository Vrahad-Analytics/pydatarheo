# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""Experimental features which may change.

> **NOTE:**
> The following "experimental" features are now "stable" and can be accessed directly from the
`datarheo.get_source()` method:
> - Docker sources, using the `docker_image` argument.
> - Yaml sources, using the `source_manifest` argument.

## About Experimental Features

Experimental features may change without notice between minor versions of PyDataRheo. Although rare,
they may also be entirely removed or refactored in future versions of PyDataRheo. Experimental
features may also be less stable than other features, and may not be as well-tested.

You can help improve this product by reporting issues and providing feedback for improvements in our
[GitHub issue tracker](https://github.com/Vrahad-Analytics/pydatarheo/issues).
"""

from __future__ import annotations

from datarheo.sources.util import get_source

__all__ = [
    "get_source",
]
