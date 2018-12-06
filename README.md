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

If you prefer to not deal with setting up a virtual environment then you can install the requirements into your python environment. WARNING: This sometimes causes conflicts with other projects.

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

We are clearly not parsing a formal grammar so using a normal LR(k) parser isn't going to work well. But I am basing these parsers on simple LR(k).  Basic program flow:

* Extract the data to be parsed from (for now) CSV columns.

* Feed each column cell to a parser.

* The parser will first tokenize the input string. The lexers will skip as many irrelevant characters as possible. Leaving only what is relevant to the parser.

* The parser will:
  - Scan the tokens from left to right. Looking for rule matches.
  - For our purposes we want to look for the LONGEST LEFTMOST match. To accomplish this when we get a match we look ahead into the tokens to see if there is a possible longer match. If there is one we directly advance the stack to this longer match. If there are multiple look-ahead options we take the longest one.
  - All matches are put into an array of dictionaries that contain the match value(s) as well as where in the string the match occurred.
  - The results are output in either HTML or CSV format.


* Note: Previous version of this program were using regular expressions only. This made things difficult to update and maintain.
