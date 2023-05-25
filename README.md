# The Traits Database Project![CI](https://github.com/rafelafrance/traiter/workflows/CI/badge.svg)

![STOP!](assets/StopSign.SVG) Rule-based parsing can be tricky, labor-intensive, error prone, and tedious. -- When using rules, homonyms become evil. -- If you can get away with it, you may want to try an end-to-end machine learning approach. Having said that, there are some uses for rule-based parsing:

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

## Mistakes Were Made

I made many mistakes while developing this set of repositories (all prefixed with “traiter_”). Many of them were made from sheer ignorance but others may trip up newbies to complex text parsing. Note that this advice is for people who are parsing complex jargon laden text full of technobabble and "interesting" abbreviations. So far these parsers are geared towards information extraction of natural history documents and notes. For instance: `762-292-121-76 2435.0g` has a very specific meaning to people who work with smaller vertebrates and `(12-)23-34 × 45-56 cm` is obviously length and width size range measurements containing a minimum length to people who work with plant treatments.

### Technical Hints and Mistakes

**Hint:** Some terms. As I mentioned above, what we’re doing is information extraction (**IE**). We’re finding traits using phrases and rules, linking them using other rules, and then extracting information from them in callback functions. I am going to abuse the terms Named Entity Recognition (**NER**), finding the traits, and Named Entity Linking (**NEL**), linking the traits.

**Hint:** **Use a package like spaCy** from the start. There are other options, of course. In the Python world there are also Stanza and NLTK. I am using spaCy only because it was the first one I found that worked on our data. What you want by using these packages is to off-load as much of the parsing work to the experts as possible. Writing parsers for this kind of data is hard enough.

spaCy is pipeline based and allows you to swap in or out pipeline segments as needed. You will need this ability because our parsing needs are unique, well currently. As a side note: I have found that when asked questions the spaCy team is responsive, patient, and very helpful.

**Hint:** Adding to the above hint you want to **leverage as much of spaCy as possible**. spaCy has a default pipeline. I may customize some of the steps and remove others but I try to use what I can from spaCy. I use a modified tokenizer, the default Parts Of Speech (POS) model, and the default lemmatizer. A lemmatizer normalizes words to a canonical form, for instance “better” is lemmatized to “good”. Sometimes I will also use spaCy’s default NER model as input to my rules.

**Mistake:** A note of caution about the hint above. **Use models not of your making cautiously**. Most of what the spaCy team produces is rock solid but some models will change when there is a minor revision. A while back I was using a model on sentences to do a dependency parse on each one. Everything worked just fine until there was a minor spaCy upgrade and all of the dependency parses changed ever so slightly and all of my rules broke. So far, the POS model has changed but not in any way that affects my rules.

**Hint:** The basic pipeline is:
Use a modified tokenizer to split the input text.
Allow spaCy to do its thing on parts of speech, lemmas, and named entities.
For every trait I do some variation on the following:
Find words and phrases (terms) to use as an anchor for the trait. Also find words and phrases that will never be in the trait and use them to block out noise. Sometimes these terms are the final trait.
Find patterns of words and symbols around those terms that build a trait. This step is often repeated to continue to build up larger and more complicated traits.
For each trait found I parse its details in a callback function.
Next I cleanup any partial traits from above so that I can use the leftover words in other traits.
Traits are linked with other traits. For instance a size may refer to a leaf size, flower size, or a plant size.

**Hint:** The spaCy tokenizer was built to handle web text like Wikipedia, twitter tweets, etc. It was not built to handle the idiosyncratic text we are parsing. I found that **customizing the tokenizer** by removing some smilies and splitting on more characters helps a lot.

**Hint:** **Terms are words or phrases**. You will want to get as many of these as possible from the domain experts. I use one or more spaCy phrase matchers to find these, it is fast and can build and find millions of terms (like a taxonomy or gazetteer) in seconds.

**Hint:** **Rules are patterns of tokens** and are analogous to regular expressions for tokens. Rules can get complicated but what I do to reduce this complexity is to build up traits in stages. This can greatly reduce the number of trait permutations to search. For instance, to build up a taxon trait (simplified):
I first look for all binomial, monomial, and rank terms in a document:
Binomial: “Genus species”
Monomial: “FamilyName” etc.
Rank: “subspecies”
Then I’ll search for species patterns like “binomial” or a binomial followed by a lower rank and monomial like “Genus species subsp. subspecies” and give it a taxon label.
Next I’ll see if there is an authority attached to the taxon from step 2 by looking for a taxon followed by a name like “taxon (name) name”. This will still have the taxon label.
After that I look for an extension lowering the taxon’s rank. Like: “taxon rank lowerMonomial (name)”. This extends the taxon and lowers its rank.
After all of that I remove any unused binomials, monomials, & ranks so they can be used in other traits.
There are already well over 100 patterns for parsing taxons, trying to do all of steps 2 through 4 in a single set of patterns would grow the numbers of patterns exponentially.

**Hint:** **A trait is nothing more than an annotated spaCy entity** which is itself nothing more than an annotated spaCy span.

**Hint:** You can **strategically order the traits** to simplify trait parsing. I will play little games like parsing latitude and longitude before I look for size traits. This makes sure that sizes do not interfere with lat/longs and lat/longs are guaranteed to not interfere with sizes because lat/longs are either labeled or in a specific format.

**Hint:** You can **allow some traits to overwrite other ones**. This allows you to disambiguate traits by context. For instance we can identify a color like “Brown” and later on if it is next to a taxon change it to an authority or if it is next to a “county” label change it to a county.

**Hint:** If you look at the rules that I write you will notice that they do not look like the rules in the spaCy documentation. That is because I **“compile” the rules before I use them**. I find that looking at strings with descriptive labels vs. JSON blobs it is much easier to reason about what my pattern is doing and why it may or may not contain a bug.

**Hint:** When there is a trait match (final or partial) I parse its contents to **build up the trait data in a callback function**. I do this when the trait is matched because it is easier to parse a trait when it is separated into tokens. Sometimes I’ll merge a trait into a single token.

**Mistake:** The trait data is currently stored in a Python dictionary. I really should have stored trait **data in data classes**.

**Hint:** **Linking traits uses patterns** too. The patterns superficially look pretty simple but there is some annoyingly complicated code in the library module that does the actual linking. What is happening when linking is that I’m looking at all nearby traits and using a weighted count of the distance between them to find the “closest” trait. The weights are mostly on punctuation so that it costs more to cross a period than a semicolon and a semicolon costs more than a comma. Some traits get linked multiple times; a flower could come in multiple colors and some traits and only get linked once. It does not make sense to have more than one flower size unless sexual dimorphism is involved. There is a fixed list of parent and child traits for linking.

**Hint:** I am paranoid about regression errors and test accordingly. There are so many moving parts to the parsers that I can’t keep them all in my head at one time. So, I use **red/green testing**. When I encounter an error I put the offending text into a test case, run the test to make sure it fails, fix the code, and rerun the test to make sure it passes. The tests do pile up and some of them are no longer testing something that fails but I keep them until I can prove that they’re no longer needed.

**Hint:** The traiter module is used by all of the children traiter modules. However, not all of the child traiter modules are up to date and some of the older ones may fail if you try to run their test. There is one old traiter module (VertNet) that doesn’t even use spaCy. It’s that old. I’m waiting for it to be reused before I make any changes to it.

### Collaboration Hints and Mistakes

**Hint:** Get as much **starting data, terms & rules, as soon as possible**. This is the foundation that you will use to build the parsers and you cannot do it well if you don’t get this information. The normal process is that you’ll get enthusiastic words of support that turn into at most a modest set of rules and terms and then nothing. The lack of initial support is probably caused by the initial data collection being so tedious, time-consuming, and harder than you’d think. Often, we can work around this, see the next hint.

**Hint:** **Get feedback** on the results as soon and as often as possible. Start parsing some results as soon as possible. Don’t wait until all the parsers are done, get one parser done and send the results back to the Phds for them to examine. Put these results into an easy to digest format. I make colorized HTML reports with one color per trait with the color used as a background of the trait in the text. Below the text I’ll put the formatted output of the traits in a table. spaCy can get you started with their “displacy” module; it’ll do a lot of what you need.

**Mistake:** Yours. You’ll make them but ultimately it is the responsibility of the Phds to correct them. The howlers are embarrassing but easy to fix, it’s the subtle errors that will come back to bite you. I have been working on parsing various forms of plant treatments for years and to this day I am sure that some of the leaf shapes and leaf margins are mixed up and suffix counts (counts like `6-7-flowered`) are incorrectly classified. Do your best but don’t beat yourself up about them if no one checks your work. **You are part of a team**, not the entire team.

**Hint:** You’re not the only one who is doing this. There are other people parsing similar types of data and then share their experiences online. I like to watch YouTube videos. Two of the channels that I watch are the spaCy channel itself and _Python for the Digital Humanities_. Most of the latter is real basic stuff, but sometimes he’ll do a deep dive into relevant topics; a hidden gem.

**Mistake:** There are genuine one-off scripts but parsing complex text never seems to be one of them. I have been promised that a project is a one-off and one of a kind thing and it seems to be true but then a couple of years later I get the, “Do you remember when you parsed that text? We need to do it again but with different data.” Do yourself a favor and **treat each parsing project like you’ll use it again**.

### Strategic Hints and Mistakes

**Mistake:** Probably the biggest mistake I made, strategically, is that I didn't **prioritize model-based parsing** soon enough. Why is this a mistake? Aside from rule-based parsing being tricky, labor-intensive, error prone, and tedious it is also quite brittle. Most rules will fail or worse, yield an incorrect parse when presented with a new pattern, models can sometimes adapt. Both models and rules suffer from "model or data drift" but for rules it can be catastrophic; turning dates and ID numbers into counts and administrative units into names, etc. In the long run models are less work.

However, given the nature of what's being parsed, **some rule-based parsing** is both inevitable and practical. Using rules to bootstrap model training data is helpful. Additionally, I found that a hybrid parser that uses both a model and rules is a powerful parsing technique. When I used a custom vocabulary coupled with a simple NER model (ca. 2019), the results were extremely good. So good in fact, that I was able to use the model results to correct some rules. Unfortunately, that model was abandoned for non-technical reasons and I haven’t had time to revisit it since.

The **models can be simple**. I have even seen Hidden Markov Models used effectively for NER. What we’re doing may be unique in detail but older techniques often work just fine.

**Mistake:** Another strategic mistake was not being aware that there are **free NLP packages** and techniques readily available which meant that I tried to develop everything in-house. I developed a slick package to use regular expressions in a hierarchical fashion. The results were pretty good and yet it was still a huge mistake because I was on the hook for everything. I was on the hook to build a phrase parser, find the parts of speech, find word lemmas, etc. I had to gain Phd level knowledge on the fly. You & I may be stellar programmers but we’re not better than a team of natural language processing Phds who have been doing this for decades.

This is enough for now. Now go and make your own mistakes.
