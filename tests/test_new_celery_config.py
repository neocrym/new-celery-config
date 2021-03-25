"""Tests for the new_celery_config.Config object."""

import unittest

from celery import Celery

from new_celery_config import Config, InvalidCeleryConfig

BROKER_TRANSPORT_OPTIONS = '{"visibility_timeout": 36000}'

BROKER_URL = "transport://userid:password@hostname:port/virtual_host"

S3_BUCKET = "bucket"


def d(config):  # pylint: disable=invalid-name
    """Turn a config object into a dictionary."""
    return config.__dict__


class TestNewCeleryConfig(unittest.TestCase):
    """Run unit tests for :py:class:`new_celery_config.Config`."""

    def test_emptiness(self):
        """Test the empty state."""
        config = Config(environ={})
        self.assertEqual(d(config), {})

    def test_single_config_item(self):
        """Test that we can set a single config item."""
        config = Config(
            environ=dict(
                EXCLUDE_THIS_TERM="nope",
                NEW_CELERY_="exclude this too",
                NEW_CELERY_broker_url=BROKER_URL,
            )
        )
        self.assertEqual(d(config), dict(broker_url=BROKER_URL))

    def test_multiple_config_items(self):
        """Test that we can set multiple config items."""
        config = Config(
            environ=dict(
                EXCLUDE_THIS_TERM="nope",
                NEW_CELERY_="exclude this too",
                NEW_CELERY_broker_url=BROKER_URL,
                NEW_CELERY_s3_bucket=S3_BUCKET,
                NEW_CELERY_broker_transport_options=BROKER_TRANSPORT_OPTIONS,
                NEW_CELERY_worker_hijack_root_logger="false",
            )
        )
        self.assertEqual(
            d(config),
            dict(
                broker_transport_options=dict(visibility_timeout=36000),
                broker_url=BROKER_URL,
                s3_bucket=S3_BUCKET,
                worker_hijack_root_logger=False,
            ),
        )

    def test_raises_on_capitalized_config_name(self):
        """Enforce that Celery config names should be lowercased."""
        with self.assertRaises(ValueError):
            Config(
                environ=dict(
                    NEW_CELERY_BROKER_URL="ignore this",
                )
            )
        with self.assertRaises(InvalidCeleryConfig):
            Config(
                environ=dict(
                    NEW_CELERY_BROKER_URL="ignore this",
                )
            )

    def test_works_with_celery(self):
        """Test that Celery understands these objects."""
        config = Config(
            environ=dict(
                NEW_CELERY_broker_transport_options=BROKER_TRANSPORT_OPTIONS,
                NEW_CELERY_broker_url=BROKER_URL,
                NEW_CELERY_s3_bucket=S3_BUCKET,
                NEW_CELERY_something_else="true",
            )
        )
        app = Celery()
        app.config_from_object(config)
        self.assertEqual(
            app.conf.broker_transport_options, dict(visibility_timeout=36000)
        )
        self.assertEqual(app.conf.broker_url, BROKER_URL)
        self.assertEqual(app.conf.s3_bucket, S3_BUCKET)
        self.assertEqual(app.conf.something_else, True)
