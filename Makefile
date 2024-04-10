.PHONY: test install dev venv clean
.ONESHELL:

VENV=.venv
PY_VER=python3.11
PYTHON=./$(VENV)/bin/$(PY_VER)
PIP_INSTALL=$(PYTHON) -m pip install
SPACY_MODEL=$(PYTHON) -m spacy download en_core_web_sm
BASE=pip setuptools wheel

test:
	export MOCK_DATA=1
	$(PYTHON) -m unittest discover
	export MOCK_DATA=0

install: venv
	source $(VENV)/bin/activate
	$(PIP_INSTALL) -U $(BASE)
	$(PIP_INSTALL) .
	$(PIP_INSTALL) git+https://github.com/rafelafrance/common_utils.git@main#egg=common_utils
	$(SPACY_MODEL)

dev: venv
	source $(VENV)/bin/activate
	$(PIP_INSTALL) -U $(BASE)
	$(PIP_INSTALL) -e ../../misc/common_utils
	$(PIP_INSTALL) -e .[dev]
	$(SPACY_MODEL)
	pre-commit install

venv:
	test -d $(VENV) || $(PY_VER) -m venv $(VENV)

clean:
	rm -r $(VENV)
	find -iname "*.pyc" -delete
