CODE = shops
TESTS = tests

ALL = $(CODE) $(TESTS)

VENV ?= .venv

venv:
	python3 -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install poetry
	$(VENV)/bin/poetry install

dev:
	$(VENV)/bin/uvicorn shops.app:app --reload
