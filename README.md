# The Traits Database Project

## All right, what's this all about then?
**Challenge**: Extract trait information from unstructured or semi-structured natural history notations. That is, if I'm given text like:

 ```This rather large female specimen is 12 lbs 7 oz and 3 feet 7 inches in total length.```

 I should be able to extract:

 - sex = female
 - body mass = 5,641 g
 - total length = 1,092 mm


 Of course this is a rather straight-forward example. Natural history/museum notations are highly idiosyncratic and may use various shorthand notations. Here are just a few examples of how total length measurements appear:

 - `Total Length: 15.7cm`
 - `15.7cm T.L.`
 - `157-60-20-19-21g`
 - `SVL 157 mm`
 - `standard length: 157-215mm`
 - `t.l.= 2 feet 3.1 - 4.5 inches`
 - As well as measurements embedded in prose like: `Snout vent lengths range anywhere from 16 to 23 mm.` I am experimenting with various distances between the anchor token `Snout vent lengths` and the measurements `16 to 23 mm`.
 - We but flag ambiguous measurements like: `length: 12.0`. This may be a total length measurement or another length measurement.
 - etc.

We also extract values from controlled vocabularies.
 - These values sometimes have a signifier like `Life Stage: Adult`
 - and other times we will just see the value like `Adult` without a signifier.

Ambiguous values like `length` are flagged as well as numeric values that do not have associated units like `total length: 12.0`. In both cases we can cleanup or cull the values in post-processing.


## List of traits extracted
- Body body mass
- Total length (aka snout vent length, fork length, etc.)
- Sex
- Life stage
- Testes state
- Testes size (In progress)
- Tail Length (In progress)
- Hind foot Length (In progress)
- Ear Length (In progress)

## Parsing strategy

There are many possible strategies for parsing traits from these notations. I am using simple but modified shift-reduce parsers. For now, there is one parser per trait or trait set.

Basic program flow:

* Extract the data to be parsed from a text file.

* Feed each column cell to one or more parsers.

* The parser will first use a lexer to tokenize the input string. The lexers will skip as many irrelevant characters as possible leaving only what is relevant for parsing that particular trait.

* The parser then:
  - Scans the tokens from left to right looking for the **longest** rule that matches the top of the stack. I look both back into the stack of productions and forward into the token list to find the longest match that uses the token at the top of the stack.
  - If there is no match then I shift to the next token.
  - If there is a match I perform the reduction.
  - All terminal reductions are put into an array that contain the matched value(s), where in the string the match occurred, and any flags that indicate possible problems with the extraction.


* There is a possible post-processing step to handle things like having too many results returned, which is almost always unhelpful. Or, to make sure that we have agreement between sets of traits. For instance, making sure that the "sex" trait agrees with the "testes" or "ovaries" trait.

* Results are place into an output file (CSV, or HTML).

## Install
You will need to have Python3 (3.7+) installed, as well as pip, a package manager for python. You can install the requirements into your python environment like so:
```
git clone https://github.com/rafelafrance/traiter.git
python3 -m pip install --user -r traiter/requirements.txt
```

## Run
```
python3 traiter.py ... TODO ...
```
## Running tests
```
pytest tests/
```
