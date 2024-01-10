.PHONY: test install dev venv clean setup_subtrees fetch_subtrees
.ONESHELL:

VENV=.venv
PY_VER=python3.11
PYTHON=./$(VENV)/bin/$(PY_VER)
PIP_INSTALL=$(PYTHON) -m pip install
SPACY_MODEL=$(PYTHON) -m spacy download en_core_web_sm

test:
	$(PYTHON) -m unittest discover

install: venv
	source $(VENV)/bin/activate
	$(PIP_INSTALL) -U pip setuptools wheel
	$(PIP_INSTALL) .
	$(SPACY_MODEL)

dev: venv
	source $(VENV)/bin/activate
	$(PIP_INSTALL) -U pip setuptools wheel
	$(PIP_INSTALL) -e .[dev]
	$(SPACY_MODEL)
	pre-commit install

venv:
	test -d $(VENV) || $(PY_VER) -m venv $(VENV)

clean:
	rm -r $(VENV)
	find -iname "*.pyc" -delete

setup_subtrees:
	git remote add -f common_utils https://github.com/rafelafrance/common_utils.git
	git checkout -b upstream/util common_utils/main
	git subtree split -q --squash --prefix=util --annotate='[util] ' --rejoin -b merging/util
	git checkout master
	git subtree add -q --squash --prefix=util merging/util

fetch_subtrees:
	git checkout upstream/util
	git pull common_utils
	git subtree split -q --squash --prefix=util --annotate='[util] ' --rejoin -b merging/util
	git checkout master
	git subtree merge -q --squash --prefix=util merging/util
