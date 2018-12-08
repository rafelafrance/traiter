# The Traits Database Project

# Install

You will need to have Python3 (3.6+) installed, as well as pip, a package manager for python. Beyond these, it is easiest to handle Traiter dependencies by setting up a virtual environment, which is a contained workspace with internally installed python libraries. Run the following code in what you intend to be your working directory:
```
git clone https://github.com/rafelafrance/traiter.git
cd traiter
python3 -m venv venv
source venv/bin/activate
(optional) git checkout v0.2 (or any other version)
pip install -r requirements.txt
```

If you prefer to not deal with setting up a virtual environment then you can install the requirements into your python environment. WARNING: This may cause conflicts with other project requirements.
```
git clone https://github.com/rafelafrance/traiter.git
python3 -m pip install --user -r traiter/requirements.txt
```

# Run
```
python3 traiter.py -i vertnet-file.csv
```
# Running tests
```
pytest tests/
```

# Parsing strategy

I am basing the trait parsers on modified but simple shift-reduce parsers with a K look-ahead.

Basic program flow:

* Extract the data to be parsed from (for now) CSV columns.

* Feed each column cell to a parser.

* The parser will first tokenize the input string. The lexers will skip as many irrelevant characters as possible leaving only what is relevant to the parser.

* The parser then:
  - Scans the tokens from left to right looking for rule matches.
  - We are doing a right-most reduction.
  - If there is not match then we shift to the next token.
  - If we have a match we perform the reduction.
  - For our purposes we want to look for the **longest match**. So whenever we get a set of tokens to match we look-ahead into the tokens to see if there is a longer match. If there is one we directly advance the stack to this longer match. If there are multiple look-ahead options that match the tokens we take the longest one.
  - All matches are put into an array of dictionaries that contain the match value(s) as well as where in the string the match occurred.


* The results are output in either an HTML or CSV format.
