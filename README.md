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

 - `Total Length: 15.7cm`
 - `15.7cm T.L.`
 - `157-60-20-19=21g`
 - `SVL 157 mm`
 - `standard length: 157-215mm`
 - `t.l.= 2 feet 3.1 - 4.5 inches`
 - As well as measurements embedded in prose like: `Snout vent lengths range anywhere from 16 to 23 cm.` I am experimenting with various distances between the anchor token `Snout vent lengths` and the measurements `16 to 23 cm`.
 - We flag ambiguous measurements like: `length: 12.0`. This may be a total length measurement or another length measurement.
 - We also flag numeric measurements without units like: `total length = 120`. The units may or may not be the default millimeters.
 - etc.

Values from controlled vocabularies are also extracted.
 - These values sometimes have a signifier like `Life Stage: Adult`
 - And other times we see a value on its own like `Adult` without the signifier.

## Parsing strategy

Note that I am trying to extract data from text and not parse a formal language. I am just looking for for patterns of text. Most importantly, I don't need to worry about recursive structures. One complication is that the characters in the text can take on different meaning depending on the context. For is instance, in `15.7cm T.L.` the dot is used as both a decimal point and as an abbreviation indicator. Elsewhere, it is usually elided noise. This problem gets even more pronounced when words or characters have multiple meanings like the letter "T" on its own. One some contexts it indicates a tail length measurement and in other contexts it indicates a testes notation and it may also be an initial in some one's name.

Also note that we want to parse gigabytes (or terabytes) of data in a relatively short amount of time. Speed isn't the primary concern but having fast turnaround is still important.

This implementation uses a technique that I call **"Stacked Regular Expressions"**. The concept is very simple:

1. Tokenize the text analogous to this method in the python `re` module documentation, [Writing a Tokenizer](https://docs.python.org/3/library/re.html#writing-a-tokenizer). It's a text simplification step that makes looking for patterns much easier.

The following regular expressions will replace the regular expressions with the "sex", "word", "keyword", and "quest" tokens respectively.

```python
    self.kwd('keyword', 'sex')
    self.kwd('sex', r' females? | males? | f | m')
    self.lit('word', r' \b [a-z] \S+ ')
    self.lit('quest', r' \? ')
```

The tokenizer will elide over anything that is not recognized in one of the tokenizer patterns. We cannot remove all irrelevant text because that can bring unrelated valid text next to each other, causing a false positive.

The `kwd` method surrounds a pattern with `\b` word-separator tokens and the `lit` method does not.

2. Use regular expressions to combine groups of tokens into a single token. Repeat this step until there is nothing left to combine.

The following regular expression will replace the "non fully descended" or "abdominal non descended" sequence of tokens with the "state" token.

```python
    self.replace('state', 'non fully descended | abdominal non descended')
```

3. Use regular expressions to find patterns of tokens to extract into traits. This is a single pass.

Here is a rule for recognizing when a sex trait is present. The first argument is a pointer to the function that will do the conversion. Traits may be converted in several ways.

```python
    self.product(
        self.convert,
        r"""  keyword (?P<value> (?: sex | word ) (?: quest )? )
            | keyword (?P<value> sex | word )""")
```

There are still issues with context that are not easily resolved with this parsing technique. For example, the double quote '"' is used as both an abbreviation for inches and as a quote character. A human can human can easily tell the difference but these parsers struggle. To help with this and other issues I use post processing heuristics.

Ultimately, a machine learning or hybrid of machine learning and parsers approach may work better.

Some of the other techniques that I tried but didn't use:

- The original version used lists of regular expressions for parsing. As a proof-of-concept it was OK but ultimately proved too cumbersome to use. One of the problems with the regular expression only technique is the multiple meanings for certain characters or words as mentioned above. I was playing Whack-a-Mole with subtle regular expression bugs.

- I tried using Flex and Bison. This didn't work for various reasons.

- I also attempted writing my own shift-reduce parsers. The resulting Python code was slow and the parsers began to become very *ad hoc*.

- Finally, I tried to use a parser combinator library (`pyparsing`) which was a vast improvement in developer time and code clarity but ballooned the run-time by two orders of magnitude. My test case of ~75,000 records went from over 30 minutes to roughly 15 seconds.

## List of traits extracted (so far)
- Body body mass
- Total length (aka snout vent length, fork length, etc.)
- Sex
- Life stage
- Testes state
- Testes size
- Tail Length
- Hind foot Length
- Ear Length

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

## Running tests
You will need to install `pytest`. After that, you can run the tests like so:
```
python -m pytest tests/
```

## Example output

TODO
