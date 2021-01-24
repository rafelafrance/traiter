#!/usr/bin/env bash

deactivate

rm -rf venv
virtualenv -p python3.8 venv

./venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f requirements_dev.txt ]; then pip install -r requirements_dev.txt; fi

pip install -U spacy-nightly --pre
python -m spacy download en_core_web_sm
