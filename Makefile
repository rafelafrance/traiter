.PHONY: test install dev clean
.ONESHELL:

test:
	uv run -m unittest discover

install:
	uv sync
	uv run -- spacy download en_core_web_md

dev:
	uv sync
	uv run -- spacy download en_core_web_md

clean:
	rm -r .venv
	find -iname "*.pyc" -delete
