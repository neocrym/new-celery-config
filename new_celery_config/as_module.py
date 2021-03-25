"""
Programmatically generates a celeryconfig.py module from the environment.

This requires Python 3.7 or newer.
"""
from new_celery_config import Config as _Config

_config = _Config()

__all__ = list(_config.__dict__)


def __getattr__(name):
    """Expose the attributes of our config object as module-level attributes."""
    return getattr(_config, name)


def __dir__():
    """List the attributes of our config object as module-level attributes."""
    return __all__
