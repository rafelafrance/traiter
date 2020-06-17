# The Traits Database Project [![Build Status](https://travis-ci.org/rafelafrance/traiter.svg?branch=master)](https://travis-ci.org/rafelafrance/traiter)

## Traiter
This is the base Traiter information extraction / data mining library used by all of the other client Traiter projects (traiter_efloras, traiter_vertnet, etc.). It's a small library with some historical cruft still attached.

The modules to consider are:
- trait_matcher.py: The core matcher used by the child matcher projects.
- spacy_nlp.py: Where I setup spaCy for our unique information extraction needs.
- util.py: Just a bucket for shared utility functions.
- The historical cruft mentioned above: It will be removed when I update some of the older Traiter projects.

## Parsing strategy
1. I label terms using Spacy's phrase and regular expression matchers.
1. Then I build up terms using Spacy's rule-based matchers repeatedly until I have built up a recognizable trait.
1. Everything else is handled by the client Traiters.

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
