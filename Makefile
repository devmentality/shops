CODE = shops
TESTS = tests

ALL = $(CODE) $(TESTS)

VENV ?= .venv

venv:
	python3 -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install poetry
	$(VENV)/bin/poetry install

up:
	uvicorn shops.app:app --host 0.0.0.0 --reload
