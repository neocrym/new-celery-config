PYTHON ?= python3
POETRY ?= $(PYTHON) -m poetry

help:
	@cat .makefile-help

install:
	$(POETRY) update
	$(POETRY) install

fmt: install
	$(POETRY) run isort --atomic .
	$(POETRY) run black .

fmt-check: install
	$(POETRY) run isort --check-only .
	$(POETRY) run black --check .

lint: install
	$(POETRY) run pylint new_celery_config tests
	$(POETRY) run mypy new_celery_config tests

build: install
	$(POETRY) run python -m pip --no-cache-dir wheel --no-deps .

test: install
	$(POETRY) run python -m unittest

.PHONY: help fmt fmt-check lint build test
