# The Traits Database Project![CI](https://github.com/rafelafrance/traiter/workflows/CI/badge.svg)

![STOP!](assets/StopSign.SVG) Rule-based parsing can be tricky and error-prone (When using rules, homonyms become evil.). If you can get away with it, you may want to try a machine learning approach. Having said that, there are some uses for rule-based parsing:

- You can use rules to build up a corpus data for training your models.
- You can use some hand-crafted rules as input for the automatic generation of other rules.
- Sometimes existing models can't handle jargon, shorthand notation, and unique (condensed) sentence structures, and you're not really parsing that much data. The "one-off" excuse never really holds though.
- You can use a hybrid rule/model-based approach. I have found this to be quite productive. For instance, you can let a model find names in a document, then you can use those names to identify people with certain roles (collector, determiner, etc.).

## Traiter
This is the base Traiter information extraction/data mining library used by all client Traiter projects, it contains **no runnable** code itself.

Some literature mined:
- PDFs containing research papers of descriptions of species.
- PDFs containing distribution data of species.
- Database downloads of field notes and species descriptions.
- Images of museum specimens. We are currently extracting data from the labels in the images.
- Data scraped from websites containing formal descriptions (treatments) of species.
- Images of PDFs of species descriptions and distribution data.
- Images of data collection notes.

**Note** All terms, traits, and extraction methods are unique to the body of literature being mined so this repository only contains truly universal terms, traits or, for that matter, functions used across many research domains.

## SpaCy Entities vs Traits:
- **A trait is just an annotated spaCy entity.**
- We leverage normal spaCy entities to build traits. Sometimes we will use spaCy's NER entities to as building block traits.

## Parsing strategy
1. Have experts identify relevant terms and target traits.
2. We use expert identified terms to label terms using spaCy's phrase matchers. These are sometimes traits themselves but are more often used as anchors for more complex patterns of traits.
3. We then build up more complex terms from simpler term using spaCy's rule-based matchers repeatedly until there is a recognizable trait. See the image below.
4. We may then link traits to each other (entity relationships) using spaCy's dependency matchers.

![parsing example](assets/anoplura_rules.png)

## Install
You will need to have Python3.9+ installed, as well as pip, a package manager for Python. You can install the requirements into your python environment like so:
```bash
git clone https://github.com/rafelafrance/traiter.git
cd traiter
optional: virtualenv -p python3 venv
optional: source venv/bin/activate
python -m pip install --requirement requirements.txt
python -m spacy download en
```

## Run
This repository is a library for other Traiter projects and is not run directly.

## Tests
You can run the tests like so:
```bash
cd /my/path/to/traiter
python -m unittest discover
```

## Other sources of data
- (Optional) We use the Integrated Taxonomic Information System (ITIS) for gathering some taxonomic information like species, genus, or common names. We do not store this database in GitHub. If you want to use it you may download the SQLite version of [ITIS here](https://www.itis.gov/downloads/index.html) and extract it into the `./data` directory.
