# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""Secrets management for PyDataRheo.

PyDataRheo provides a secrets management system that allows you to securely store and retrieve
sensitive information. This module provides the secrets functionality.

## Secrets Management

PyDataRheo can auto-import secrets from the following sources:

1. Environment variables.
2. Variables defined in a local `.env` ("Dotenv") file.
3. [Google Colab secrets](https://medium.com/@parthdasawant/how-to-use-secrets-in-google-colab-450c38e3ec75).
4. Manual entry via [`getpass`](https://docs.python.org/3.10/library/getpass.html).

**Note:** You can also build your own secret manager by subclassing the `CustomSecretManager`
implementation. For more information, see the `datarheo.secrets.CustomSecretManager` reference docs.

### Retrieving Secrets

To retrieve a secret, use the `get_secret()` function. For example:

```python
import datarheo as dr

source = dr.get_source("source-github")
source.set_config(
   "credentials": {
      "personal_access_token": dr.get_secret("GITHUB_PERSONAL_ACCESS_TOKEN"),
   }
)
```

By default, PyDataRheo will search all available secrets sources. The `get_secret()` function also
accepts an optional `sources` argument of specific source names (`SecretSourceEnum`) and/or secret
manager objects to check.

By default, PyDataRheo will prompt the user for any requested secrets that are not provided via
other secret managers. You can disable this prompt by passing `allow_prompt=False` to
`get_secret()`.

### Secrets Auto-Discovery

If you have a secret matching an expected name, PyDataRheo will automatically use it. For example,
if you have a secret named `GITHUB_PERSONAL_ACCESS_TOKEN`, PyDataRheo will automatically use it
when configuring the GitHub source.

The naming convention for secrets is as `{CONNECTOR_NAME}_{PROPERTY_NAME}`, for instance
`SNOWFLAKE_PASSWORD` and `BIGQUERY_CREDENTIALS_PATH`.

PyDataRheo will also auto-discover secrets for interop with the hosted cloud:
`DATARHEO_CLOUD_API_URL`, `DATARHEO_CLOUD_API_KEY`, etc.

## Custom Secret Managers

If you need to build your own secret manager, you can subclass the
`datarheo.secrets.CustomSecretManager` class. This allows you to build a custom secret manager that
can be used with the `get_secret()` function, securely storing and retrieving secrets as needed.

## Using "Secrets References" to Decouple Secrets from Configuration

PyDataRheo now allows you to decouple secrets from configuration parameters. This means you can
use the `secret_reference::` prefix (`datarheo.constants.SECRETS_HYDRATION_PREFIX`) to specify a
reference to a named secret instead of hard-coding the secret value directly in your configuration.

For example, in your JSON or `dict` configuration, you can specify a secret reference like this:

```json
{
  "credentials": {
    "personal_access_token": "secret_reference::GITHUB_PERSONAL_ACCESS_TOKEN"
  }
}
```

This allows you to keep your connector configuration clean and free of sensitive information,
while still allowing PyDataRheo to dynamically resolve the secrets at runtime.

By default, PyDataRheo will automatically resolve these references with a call to `get_secret()`,
utilizing whichever secret managers have been registered using `register_secret_manager()`.

If you've not already registered a secret manager, PyDataRheo will use the default
`EnvVarSecretManager`, which retrieves secrets from named environment variables.

## API Reference

_Below are the classes and functions available in the `datarheo.secrets` module._

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from datarheo.secrets.base import SecretHandle, SecretManager, SecretSourceEnum, SecretString
from datarheo.secrets.config import disable_secret_source, register_secret_manager
from datarheo.secrets.custom import CustomSecretManager
from datarheo.secrets.env_vars import DotenvSecretManager, EnvVarSecretManager
from datarheo.secrets.google_colab import ColabSecretManager
from datarheo.secrets.google_gsm import GoogleGSMSecretManager
from datarheo.secrets.prompt import SecretsPrompt
from datarheo.secrets.util import get_secret

# Submodules imported here for documentation reasons: https://github.com/mitmproxy/pdoc/issues/757
if TYPE_CHECKING:
    # ruff: noqa: TC004  # imports used for more than type checking
    from datarheo.secrets import (
        base,
        config,
        custom,
        env_vars,
        google_colab,
        google_gsm,
        prompt,
        util,
    )


__all__ = [
    # Submodules
    "base",
    "config",
    "custom",
    "env_vars",
    "google_colab",
    "google_gsm",
    "prompt",
    "util",
    # Secret Access
    "get_secret",
    # Secret Classes
    "SecretSourceEnum",
    "SecretString",
    "SecretHandle",
    # Secret Managers
    "SecretManager",
    "EnvVarSecretManager",
    "DotenvSecretManager",
    "ColabSecretManager",
    "SecretsPrompt",
    "CustomSecretManager",
    "GoogleGSMSecretManager",
    # Registration Functions`
    "register_secret_manager",
    "disable_secret_source",
]
