.PHONY: test install dev venv clean activate base
.ONESHELL:

VENV=.venv
PY_VER=python3.11
PYTHON=./$(VENV)/bin/$(PY_VER)
PIP_INSTALL=$(PYTHON) -m pip install
SPACY_MODEL=$(PYTHON) -m spacy download en_core_web_sm

test: activate
	$(PYTHON) -m unittest discover

install: venv activate base
	$(PIP_INSTALL) git+https://github.com/rafelafrance/common_utils.git@main#egg=common_utils
	$(PIP_INSTALL) .
	$(SPACY_MODEL)

dev: venv activate base
	$(PIP_INSTALL) -e ../../misc/common_utils
	$(PIP_INSTALL) -e .[dev]
	$(SPACY_MODEL)
	pre-commit install

activate:
	. $(VENV)/bin/activate

base:
	$(PIP_INSTALL) -U pip setuptools wheel

venv:
	test -d $(VENV) || $(PY_VER) -m venv $(VENV)

clean:
	rm -r $(VENV)
	find -iname "*.pyc" -delete
