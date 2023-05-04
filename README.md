# The Traits Database Project![CI](https://github.com/rafelafrance/traiter/workflows/CI/badge.svg)

![STOP!](assets/StopSign.SVG) Rule-based parsing can be tricky, labor-intensive, error-prone, and tedious. -- When using rules, homonyms become evil. -- If you can get away with it, you may want to try an end-to-end machine learning approach. Having said that, there are some uses for rule-based parsing:

- You can use rules to build training data for your models.
- You can use some hand-crafted rule output as input for the automatic generation of other rules.
- Sometimes existing models can't handle jargon, shorthand notation, and unique (condensed) sentence structures, and you're not really parsing that much data. The "one-off" excuse never really holds because it's never just one, is it.
- You can use a hybrid model/rule-based approach. I have found this to be quite productive.
  - For instance, you can let a model find names (PERSON entities) in a document, then you can use those names as input for rules that identify people with certain roles (collector, determiner, etc.).
  - I almost always use models for finding parts of speech and sentence structure which I then use as rule input.
  - The goal is still to use the output of the hybrid model as training data for a model that brings you ever closer to the sought after end-to-end model.

## Traiter
This is the base Traiter information extraction/data mining library used by all client Traiter projects, it contains **no runnable code** itself.

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
- **A trait is just an annotated spaCy entity.** That is we're treating traits (aka attributes) as if they were their own entity. This has the advantage in that we can use named entity recognition (NER) techniques on them. We can also use standard entity link methods for linking traits to entities.
- There may (or not) be several layers of entities and traits. For instance, a plant SPECIES (a top-level entity) may have FLOWERs (a secondary or sub-entity) and those FLOWERs will have a set of characteristic COLORs (a trait).
- We leverage normal spaCy entities to build traits. Sometimes we will also use spaCy's NER entities as building block traits. (See below.)

## Parsing strategy
1. Have experts identify relevant terms and target traits.
2. We use expert identified terms to label terms using spaCy's phrase matchers. These are sometimes traits themselves but are more often used as anchors for more complex patterns of traits.
3. We then build up more complex terms from simpler terms using spaCy's rule-based matchers repeatedly until there is a recognizable trait. See the image below.
4. We may then link traits to each other (entity relationships) using spaCy's dependency matchers.
   1. Typically, a trait gets linked to a higher level entity like SPECIES <--- FLOWER <--- {COLOR, SIZE, etc.} and not peer to peer like PERSON <---> ORG.
   2. Also note that sometimes the highest level entity is assumed by its context. For instance, if a web page is a description of a newly found species then we don't need to parse the species name in the document.

![parsing example](assets/anoplura_rules.png)

## Install
You will need GIT to clone this repository. You will also need to have Python3.10+ installed, as well as pip, a package manager for Python.
You can install the requirements into your python environment like so:
```bash
git clone https://github.com/rafelafrance/traiter.git
cd /path/to/traiter
python3 -m pip install .
python3 -m spacy download en_core_web_sm
```

**I recommend using a virtual environment but that is not required.**

## Run
This repository is a library for other Traiter projects and is not run directly. Well it could be, but it's not really designed for it.

## Tests
You can run the tests like so:
```bash
cd /my/path/to/traiter
python -m unittest discover
```
