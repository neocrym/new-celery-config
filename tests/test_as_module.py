"""
Test that :py:mod:`new_celery_config.as_module` is a celeryconfig.py module
generated from the environment.
"""
import os

BROKER_TRANSPORT_OPTIONS = '{"visibility_timeout": 36000}'

BROKER_URL = "transport://userid:password@hostname:port/virtual_host"

S3_BUCKET = "bucket"

os.environ["CELERY_CONFIG_MODULE"] = "new_celery_config.as_module"
os.environ["NEW_CELERY_broker_transport_options"] = BROKER_TRANSPORT_OPTIONS
os.environ["NEW_CELERY_broker_url"] = BROKER_URL
os.environ["NEW_CELERY_s3_bucket"] = S3_BUCKET
os.environ["IGNORE_THIS"] = "first"
os.environ["NEW_CELERY"] = "ignoring this too"
os.environ["NEW_CELERY_something_else"] = "true"

import unittest  # pylint: disable=wrong-import-position

from celery import Celery  # pylint: disable=wrong-import-position


class TestAsModule(unittest.TestCase):
    """Test that the module-level attributes work."""

    def test_works_with_celery(self):  # pylint: disable-duplicate-code
        """Test that Celery understands these objects."""
        app = Celery()
        self.assertEqual(
            app.conf.broker_transport_options, dict(visibility_timeout=36000)
        )
        self.assertEqual(app.conf.broker_url, BROKER_URL)
        self.assertEqual(app.conf.s3_bucket, S3_BUCKET)
        self.assertEqual(app.conf.something_else, True)
