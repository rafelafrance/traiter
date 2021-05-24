#!/usr/bin/env bash

if [[ ! -z "$VIRTUAL_ENV" ]]; then
  echo "'deactivate' before running this script."
  exit 1
fi

rm -rf .venv
virtualenv -p python3.9 .venv

source ./.venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

pip install -U spacy[cuda,transformers,lookups]
python -m spacy download en_core_web_sm

# Commonly used for dev
pip install -U pynvim
pip install -U 'python-lsp-server[all]'
pip install -U autopep8 flake8 isort pylint yapf pydocstyle
pip install -U jupyter jupyter_nbextensions_configurator
pip install -U jupyterlab
pip install -U jupyterlab_code_formatter
pip install -U jupyterlab-drawio
pip install -U jupyterlab-lsp
pip install -U jupyterlab-spellchecker
pip install -U jupyterlab-git
pip install -U aquirdturtle-collapsible-headings
pip install -U nbdime
pip install -U ipyparallel

jupyter labextension install jupyterlab_onedarkpro
jupyter server extension enable --py jupyterlab_git
jupyter serverextension enable --py jupyterlab_code_formatter
