.PHONY: test install dev venv clean
.ONESHELL:

VENV=.venv
PYTHON=./$(VENV)/bin/python3.11
PIP_INSTALL=$(PYTHON) -m pip install
SPACY_MODEL=$(PYTHON) -m spacy download en_core_web_sm
CREATE_DB=$(PYTHON) ./traiter/create_term_db.py

test:
	$(PYTHON) -m unittest discover

install: venv
	source $(VENV)/bin/activate
	$(PIP_INSTALL) -U pip setuptools wheel
	$(PIP_INSTALL) .
	$(SPACY_MODEL)
	$(CREATE_DB)

dev: venv
	source $(VENV)/bin/activate
	$(PIP_INSTALL) -U pip setuptools wheel
	$(PIP_INSTALL) -e .[dev]
	$(SPACY_MODEL)
	pre-commit install
	$(CREATE_DB)

venv:
	test -d $(VENV) || python3.11 -m venv $(VENV)

clean:
	rm -r $(VENV)
	find -iname "*.pyc" -delete
