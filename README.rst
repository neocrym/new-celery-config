``new-celery-config`` specifies Celery config via environment variables
=======================================================================

`Celery <https://docs.celeryproject.org/en/stable/>`_ is a distributed task queue library for Python. It accepts some of its configuration via environment variables--but some configuration needs to be specified as Python code.

``new-celery-config`` is a Python package that lets you set any top-level Celery key using an environment variable containing YAML.

Installation
------------

The latest stable can be installed via pip:

.. code:: text

    python3 -m pip install new-celery-config

Usage
-----

(Usage) as a module
^^^^^^^^^^^^^^^^^^^

To set configuration values, you must set an environment variables for each top-level key (`as documented in the Celery documentation <https://docs.celeryproject.org/en/latest/userguide/configuration.html#configuration>`_).

Each environment variable is prefixed with ``NEW_CELERY_``, followed by the config key name in lowercase. The value for each environment variable must be valid YAML (or JSON--remember that JSON is a subset of YAML).

You must also set the environment variable ``CELERY_CONFIG_MODULE`` to ``new_celery_config.as_module`` to enable Celery to read all of the other environment variables that you have set.

For example, setting these environment variables in the shell looks like:

.. code:: bash

    export CELERY_CONFIG_MODULE=new_celery_config.as_module
    export NEW_CELERY_broker_url='transport://userid:password@hostname:port/virtual_host'
    export NEW_CELERY_broker_transport_options='{"visibility_timeout": 36000}'

And in your Python code, initialize the Celery object as follows:

.. code:: python

    app = Celery()

If you want to change the name of the ``CELERY_CONFIG_MODULE``, you can use the ``config_from_envvar`` function. For example:

.. code:: bash

    export ARBITRARY_CELERY_CONFIG_MODULE=new_celery_config.as_module

.. code:: python

    app.config_from_envvar("ARBITRARY_CELERY_CONFIG_MODULE")

You can test that the configuration works by examining the ``app.conf`` object:

.. code:: python

    print(app.conf.broker_transport_options)
    # prints out {'visibility_timeout': 36000}

Usage (as an object)
^^^^^^^^^^^^^^^^^^^^

Celery also accepts configuration in the form of a Python object. If you prefer this way, you can give Celery a ``new_celery_config.Config`` object. For example:

.. code:: python

    from celery import Celery
    import new_celery_config

    app = Celery()
    app.config_from_object(new_celery_config.Config())


Contributing changes to ``new-celery-config``
---------------------------------------------

If you want to make changes to ``new-celery-config``, you can clone this repository. You can run ``make`` in the root directory to show commands relevant to development.

For example:
 - ``make fmt`` automatically formats Python code.
 - ``make lint`` runs pylint and mypy to catch errors.
 - ``make test`` runs unit tests.
