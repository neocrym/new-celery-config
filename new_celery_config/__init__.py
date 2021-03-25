"""
Generates a Celery config object from environment variables.
"""
import importlib
import os

import yaml

_PREFIX = "NEW_CELERY_"
_PLEN = len(_PREFIX)


class InvalidCeleryConfig(ValueError):
    """Raised when the given input environment variables are ambiguous or wrong."""


def _load_key(environment_key: str):
    """Strips keys of our environment variable prefix"""
    if environment_key.startswith(_PREFIX):
        key = environment_key[_PLEN:]
        if key != key.lower():
            raise InvalidCeleryConfig(
                "new_celery_config key names should have an uppercase prefix "
                "and a lowercase suffix. For example, the environment variable "
                f"`{_PREFIX}broker_url` sets the `broker_url` Celery "
                f"config setting. You passed the key `{environment_key}` "
                "which is invalid."
            )
        return key
    return ""


class Config:  # pylint: disable=too-few-public-methods
    """A Celery config object. For each key, it reads values as YAML in environment variables."""

    def __init__(self, *, environ=None):
        """Initialize the object from the environment."""
        if environ is None:
            environ = os.environ
        for environment_key, serialized_value in environ.items():
            key = _load_key(environment_key)
            if key:
                try:
                    value = yaml.safe_load(serialized_value)
                except yaml.YAMLError:
                    continue
                else:
                    setattr(self, key, value)
