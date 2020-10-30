# The Traits Database Project [![Build Status](https://travis-ci.org/rafelafrance/traiter.svg?branch=master)](https://travis-ci.org/rafelafrance/traiter)

## Traiter
This is the base Traiter information extraction / data mining library used by all client Traiter projects (traiter_floras, traiter_anoplura, etc.).

## Parsing strategy
1. Label terms using Spacy's phrase and regular expression matchers.
1. Then build up terms using Spacy's rule-based matchers repeatedly until there is a recognizable trait.

This is a visual representation of the strategy outlined above.
![parsing example](assets/anoplura_rules.png)

## Install
You will need to have Python3 installed, as well as pip, a package manager for python. You can install the requirements into your python environment like so:
```
git clone https://github.com/rafelafrance/traiter.git
cd traiter
optional: virtualenv -p python3 venv
optional: source venv/bin/activate
python -m pip install --requirement requirements.txt
python -m spacy download en
```

## Run
```
python3 traiter.py ... TODO ...
```

## Tests
You can run the tests like so:
```
cd /my/path/to/traiter
python -m unittest discover
```
