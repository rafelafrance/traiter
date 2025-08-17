.PHONY: test install dev clean
.ONESHELL:

test:
	. .venv/bin/activate
	python3.13 -m unittest discover

install:
	test -d .venv || python3.13 -m venv .venv
	. .venv/bin/activate
	python3.13 -m pip install -U pip setuptools wheel
	python3.13 -m pip install .
	python3.13 -m spacy download en_core_web_md

dev:
	test -d .venv || python3.13 -m venv .venv
	. .venv/bin/activate
	python3.13 -m pip install -U pip setuptools wheel
	python3.13 -m pip install -e .[dev]
	python3.13 -m spacy download en_core_web_md

clean:
	rm -r .venv
	find -iname "*.pyc" -delete
