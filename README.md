# The Traits Database Project

## All right, what's this all about then?
**Challenge**: Extract trait information from unstructured or semi-structured natural history notations. That is, if I'm given text like, "This rather large female specimen is 12 lbs 7 oz and 3 feet and 7 inches in total length." I should be able to extract that the "sex = female", the "body mass = 5,641 g" and the "total length = 1,092 mm". Of course this is a rather straight-forward example. Natural history/museum notations are highly idiosyncratic and may use various shorthand notations. For example, total length can be written in as "Total Length: 20cm", or as "20cm T.L.", etc. Controlled vocabularies can sometimes have a signifier like "Life Stage: Adult" and other times we will just see the word "Adult" without a signifier. In other cases we will see uncommented shorthand notations like "157-60-20-19-21g" and we will need to extract the proper values from that.

There are many possible strategies for parsing traits from these notations. For now, I'm using a modified shift-reduce parser and I am writing one parser per trait (or trait set). See below.

## Install
You will need to have Python3 (3.6+) installed, as well as pip, a package manager for python. You can install the requirements into your python environment like so:
```
git clone https://github.com/rafelafrance/traiter.git
python3 -m pip install --user -r traiter/requirements.txt
```

## Run
```
python3 traiter.py ... more to follow ...
```
## Running tests
```
pytest tests/
```

## Parsing strategy
I am basing the trait parsers on modified but simple shift-reduce parsers.

Basic program flow:

* Extract the data to be parsed from, for now, CSV columns.

* Feed each column cell to one or more parsers.

* The parser will first use a lexer to tokenize the input string. The lexers will skip as many irrelevant characters as possible leaving only what is relevant for parsing that particular trait.

* The parser then:
  - Scans the tokens from left to right looking for the **longest** rule that matches the top of the stack. I look both back into the stack of productions and forward into the token list to find the longest match that uses the token at the top of the stack.
  - If there is no match then I shift to the next token.
  - If there is match I perform the reduction.
  - All terminal reductions are put into an array of dictionaries that contain the matched value(s) as well as where in the string the match occurred.


* There is a possible post-processing step to handle things like having too many results returned, which is almost always unhelpful. Or, to make sure that I have agreement between sets of traits. For instance, making sure that the "sex" trait agrees with the "testes" or "ovaries" trait.

* The results are output in either an HTML or CSV format.
