# The Traits Database Project![CI](https://github.com/rafelafrance/traiter/workflows/CI/badge.svg)

These days this code is mainly used to:
1. Gather training data for fine-tuning a large language model.
2. Post-processing annotations gathered by a large language model.

-- ~~If you can get away with it, you may want to try an end-to-end machine learning approach.~~

I just spent a substantial effort on using a machine learning model, and I was wrong about the relative usefulness of rule-based and machine learning approaches for information extraction. Both have their strengths and weaknesses. I now tend to use rule-based models for data pre- and post-processing, as well as generating training data.

## Traiter
This is the rule-based Traiter information extraction/data mining library used by all client Traiter projects.

This contains only the rule-based parsers used for information extraction. The model-based parsers are in [other repositories](https://github.com/rafelafrance/hybrid_traiter).

Some literature mined:
- PDFs containing research papers of descriptions of species.
- PDFs containing distribution data of species.
- Database downloads of field notes and species descriptions.
- Images of museum specimens. We are currently extracting data from the labels in the images.
- Data scraped from websites containing formal descriptions (treatments) of species.
- Images of PDFs of species descriptions and distribution data.
- Images of data collection notes.

**Note** All terms, traits, and extraction methods are unique to the body of literature being mined so this repository only contains truly universal terms, traits, or functions used across many research domains.

## SpaCy Entities vs Traits:
- *A trait is just an annotated spaCy entity.* That is, I'm treating traits (aka attributes) as if they were their own entity. This has the advantage in that I can use named entity recognition (NER) techniques on them. We can also use standard entity link methods for linking traits to entities.
- There may (or not) be several layers of entities and traits. For instance, a plant SPECIES (a top-level entity) may have FLOWERs (a secondary or sub-entity) and those FLOWERs will have a set of characteristic COLORs (a trait).
- We leverage normal spaCy entities to build traits. Sometimes I will use spaCy's NER entities as building block traits.

## Rule-based parsing strategy
1. Have experts identify relevant terms and target traits.
2. We use expert identified terms to label terms using spaCy's phrase matchers. These are sometimes traits themselves but are more often used as anchors for more complex patterns of traits.
3. We then build up more complex terms from simpler terms using spaCy's rule-based matchers repeatedly until there is a recognizable trait. See the image below.
4. We may then link traits to each other (entity relationships) also using spaCy rules.
   1. Typically, a trait gets linked to a higher level entity like SPECIES <--- FLOWER <--- {COLOR, SIZE, etc.} and not peer to peer like PERSON <---> ORG.
   2. Also note that sometimes the highest level entity is assumed by its context. For instance, if a web page is a description of a newly found species then I don't need to parse the species name in the document.

![parsing example](assets/anoplura_rules.png)

## Install
TODO: Change to use `uv`.

## Run
This repository is a library for other Traiter projects and is not designed to be run directly.

## Tests

There are tests which you can run like so:
```bash
uv run -m unittest discover
```
