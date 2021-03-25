``new_celery_config`` specifies Celery config via environment variables
=======================================================================

`Celery <https://docs.celeryproject.org/en/stable/>`_ is a distributed task queue library for Python. It accepts some of its configuration via environment variables--but some configuration needs to be specified as Python code.

``new_celery_config`` is a Python package that lets you set any top-level Celery key using an environment variable containing YAML.

Installation
------------

The latest stable can be installed via pip:

.. code:: text

    python3 -m pip install new-celery-config

Usage
-----

To set configuration values, you must set an environment variables for each top-level key (`as documented in the Celery documentation <https://docs.celeryproject.org/en/latest/userguide/configuration.html#configuration>`_).

Each environment variable is prefixed with ``NEW_CELERY_``, followed by the config key name in lowercase. The value for each environment variable must be valid YAML (or JSON--remember that JSON is a subset of YAML).

For example, setting these variables in the shell looks like:

.. code:: bash

    export BROKER_URL='transport://userid:password@hostname:port/virtual_host'
    export NEW_CELERY_broker_transport_options='{"visibility_timeout": 36000}'

Usage (as an object)
^^^^^^^^^^^^^^^^^^^^

Then, when you create your Celery object in code, you can pass it a ``new_celery_config.Config`` object. For example:

.. code:: python

    from celery import Celery
    import new_celery_config

    app = Celery()
    app.config_from_object(new_celery_config.Config())


and you can test that the configuration works by examining the ``app.conf`` object:

.. code:: python

    print(app.conf.broker_transport_options)
    # prints out {'visibility_timeout': 36000}

(Usage) as a module
^^^^^^^^^^^^^^^^^^^

Celery also accepts configuration from a module with top-level variables mapping to config keys. The location of this module can be set via an environment variable.

If your existing configuration is already in an module, then your code probably already looks like:

.. code:: python

    app = Celery()
    app.config_from_envvar("ARBITRARY_CELERY_CONFIG_MODULE")

where the value of ``ARBITRARY_CELERY_CONFIG_MODULE`` is something like ``your_project.celeryconfig``.

If you don't want to change your Python code to read, then just set your ``ARBITRARY_CELERY_CONFIG_MODULE`` environment variable to ``new_celery_config.as_module`` and everything will work as expected.

Contributing changes to ``new_celery_config``
---------------------------------------------

If you want to make changes to ``new_celery_config``, you can clone this repository. You can run ``make`` in the root directory to show commands relevant to development.

For example:
 - ``make fmt`` automatically formats Python code.
 - ``make lint`` runs pylint and mypy to catch errors.
 - ``make test`` runs unit tests.
