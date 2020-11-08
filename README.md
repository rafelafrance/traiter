# The Traits Database Project ![Super-Linter](https://github.com/rafelafrance/traiter/workflows/Super-Linter/badge.svg)

## Traiter
This is the base Traiter information extraction/data mining library used by all client Traiter projects ([traiter_floras](https://github.com/rafelafrance/traiter_floras), [traiter_anoplura](https://github.com/rafelafrance/traiter_anoplura), etc.). It contains no runnable code itself.

Some of the literature mined:
- PDFs containing research papers of descriptions of species.
- PDFs containing distribution data of species.
- Database downloads of field notes and species descriptions.
- Images of museum specimens. We are currently extracting data from the labels in the images.
- Data scraped from websites containing formal descriptions (treatments) of species.
- Images of PDSs of species descriptions and distribution data.
- Images of data collection notes.

**Note** All terms, traits, and extraction methods are unique to the body of literature being mined so this repository only contains truly universal terms, traits or, for that matter, functions used across many research domains.

## Parsing strategy
1. Have experts identify relevant terms and target traits.
1. We use expert identified terms to label terms using Spacy's phrase and regular expression matchers. These are sometimes traits themselves but are more often used as anchors for more complex patterns of traits.
1. We then build up more complex terms from simpler term using Spacy's rule-based matchers repeatedly until there is a recognizable trait. See the image below.

![parsing example](assets/anoplura_rules.png)

## Install
You will need to have Python3 installed, as well as pip, a package manager for python. You can install the requirements into your python environment like so:
```bash
git clone https://github.com/rafelafrance/traiter.git
cd traiter
optional: virtualenv -p python3 venv
optional: source venv/bin/activate
python -m pip install --requirement requirements.txt
python -m spacy download en
```

## Run
This repository is a library for the other Traiter projects and is not run directly.

## Tests
You can run the tests like so:
```bash
cd /my/path/to/traiter
python -m unittest discover
```

## Other sources of data
- (Optional) We use the Integrated Taxonomic Information System (ITIS) for gathering some taxonomic information like species, genus, or common names. We do not store this database in GitHub. If you want to use it you may download the SQLite version of [ITIS here](https://www.itis.gov/downloads/index.html) and extract it into the `/data` directory.
