# The Traits Database Project [![Build Status](https://travis-ci.org/rafelafrance/traiter.svg?branch=master)](https://travis-ci.org/rafelafrance/traiter)

## All right, what's this all about then?
**Challenge**: Extract trait information from unstructured or semi-structured natural history notations. That is, if I'm given text like:

 ```
 This rather large female specimen is 12 lbs 7 oz and 3 feet 7 inches in total length.
 ```
I should be able to extract:

 - sex = female
 - body mass = 5,641 g
 - total length = 1,092 mm

 Of course, this is a rather straight-forward example. Natural history/museum notations are highly idiosyncratic and may use various shorthand notations. Here are just a few examples of how total length measurements appear:

 - Total Length: 15.7cm
 - 15.7cm T.L.
 - 157-60-20-19=21g
 - SVL 157 mm
 - standard length: 157-215mm
 - t.l. = 2 feet 3.1 - 4.5 inches
 - As well as measurements embedded in prose like: "Snout vent lengths range anywhere from 16 to 23 cm."
 - We flag ambiguous measurements like: "length: 12.0". This may be a total length measurement or another length measurement.
 - We also flag numeric measurements without units like: "total length = 120". The units may or may not be the default millimeters.
 - etc.

Values from controlled vocabularies are also extracted.
 - These values sometimes have a signifier like "Life Stage: Adult"
 - And other times we see a value on its own like "Adult" without the signifier.

## Parsing strategy

We are using the stacked-regex module to do most of the parsing. This module returns a list of putative traits. However, there is some ambiguity remaining in some trait parses. To fix this we perform a postprocessing step. This is nothing more than applying heuristics on the traits and their surrounding context to resolve the ambiguities. Here are some issues that are resolved in postprocessing:

- Add missing units
- Not assigning inappropriate traits like assigning ovary traits to males or testes traits to females
- Determine if a `"` character is an abbreviation for inches or a quote character.
- We also have a situations where the same abbreviation is used for different traits. For instance `T` can indicate either a testes measurement or a tail length measurement. 

## List of traits extracted (so far)
- Total length (aka snout vent length, fork length, etc.)
- Tail Length
- Hind foot Length
- Ear Length
- Body body mass
- Life stage
- Sex
- Ovaries state & size
- Pregnancy state
- Embryo count & size
- Nipple state
- Lactation state
- Placental scar state, count, & location
- Testes state & size

## Install

You will need to have Python3 installed, as well as pip, a package manager for python. You can install the requirements into your python environment like so:
```
git clone https://github.com/rafelafrance/traiter.git
python3 -m pip install --user -r traiter/requirements.txt
```

## Run
```
python3 traiter.py ... TODO ...
```

## Tests
Having a test suite is absolutely critical. The strategy I use is every new pattern gets its own test. And any time there is a parser error I the relevant parts that caused the error to the test suite and correct the parser. I.e. I use the standard red/green testing methodology.

You will need to install `pytest`. After that, you can run the tests like so:
```
python3 -m pytest tests/
```

## Example parser output

TODO
