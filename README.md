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

Note that I am trying to extract data from text and not parse a formal language. I am just looking for for patterns of text. Most importantly, I don't need to worry about recursive structures. Pattern recognition is a common technique in **Natural Language Processing, Information Extraction**.

One complication is that the characters in the text can take on different meaning depending on the context. For is instance, is a double quote after a number `"` an inch symbol (like `3' 4"`or a closing quote (like `"length=4"`)? It's just as tricky to handle single characters have multiple meanings like the letter "T" on its own. In some contexts it indicates a tail length measurement and in other contexts it indicates a testes notation and most contexts it is an initial in some one's name. In this project, we differentiate and capture the first two cases and try to ignore the last one.

Another important point is that we want to parse gigabytes (or terabytes) of data in a relatively short amount of time. Speed isn't the primary concern but having fast turnaround is still important.

This implementation uses a technique that I call **"Stacked Regular Expressions"**. The concept is very simple we build tokens in one step and in the next two steps we use those tokens to reduce combinations to other tokens or productions. Finally, there is a post-processing step where we handle things like ovaries cannot be a male trait or testes cannot be a female trait.

1. Tokenize the text.
2. (Optional) Replace sequences of tokens to simplify the token stream. Repeat this step as many times as needed.
3. Convert sequences of tokens into the final productions.
4. Post processing of traits.


#### 1. Tokenize the text
This step is directly analogous to this method in the documentation for python's `re` module, [Writing a Tokenizer](https://docs.python.org/3/library/re.html#writing-a-tokenizer). It's a text simplification step that makes looking for patterns much easier.

The following regular expressions will replace the regular expressions with the "sex", "word", "keyword", and "quest" tokens respectively.

```python
    self.kwd('keyword', 'sex')
    self.kwd('sex', r' females? | males? | f | m')
    self.lit('word', r' \b [a-z] \S+ ')
    self.lit('quest', r' \? ')
```

`kwd` and `lit` are methods for adding token regular expressions to the parser. The `kwd` surrounds a pattern with `\b` word-separator character class and the `lit` method does not. So `self.lit('pattern_name', r'my pattern')` just adds the pattern as is but `self.kwd('pattern_name', r'my pattern')` will add the pattern like so: `\b (?: my pattern) \b`.

Given these rules and the following text: `Specimen 2399: sex is female? ,`

We will produce the following tokens: `word keyword word sex quest`.

Notice that there are no tokens for any of the spaces, the `2399:` character sequence or the final `;` semicolon. We have removed the "noise". This turns out to be very helpful with simplifying the parsers. However, nothing codes for free. If you elide over too much text you can bring unrelated text next to each other and cause false positives.

I should also note that the regular expressions for tokens can get fairly complex. See `lib/shared_tokens.py` for some examples.

#### 2. (Optional) Replace sequences of tokens to simplify the token stream. Repeat this step as many times as needed.

Use regular expressions on the tokens to combine groups of tokens into a single token. Repeat this step until there is nothing left to combine. These are regular expressions just like any other they're just matching on the token names instead of on raw text.

```python
self.replace('key', ' keyword | char_key | char_measured_from ')
```

In this example any of the three tokens (`keyword`, `char_key`, or `char_measured_from`) will be replaced with the `key` token. The `key` token may be used in the final rules for producing traits. This is a trivial example that only simplifies the notation but other examples do get more complex and use the full power of regular expressions.

#### 3. Convert sequences of tokens into the final productions
Use regular expressions to find patterns of tokens that are then converted into traits. This is a single pass.

Here is a rule for recognizing when a sex trait is present. The first argument is a pointer to the function that will do the conversion. Traits may be converted in several ways. Just like in step 2, each word represents a single token.

```python
    self.product(
        self.convert,
        r"""  keyword (?P<value> (?: sex | word ) (?: quest )? )
            | keyword (?P<value> sex | word )""")
```

This rule will convert token sequences like `keyword sex quest` (handling strings similar to `sex = female?`) or `keyword word` (handling string similar to `sex: unknown`) into the a sex trait.

#### 4. Post processing of traits
This is where I apply a set of heuristics to modify traits to handle things like missing units, or to make sure we don't assign an ovary trait to a male or a testis trait to female.

There is also where we handle issues that are not easily resolved with this parsing technique. For example, the double quote '"' is used as both an abbreviation for inches and as a quote character. A human can human can easily tell the difference but these parsers struggle.

#### Notes on the algorithm

Some of the other techniques that I tried but don't currently use:

- The original version used lists of regular expressions for parsing. As a proof-of-concept it was OK but ultimately proved too cumbersome to use. I was playing Whack-a-Mole with subtle regular expression bugs. Also, regular expressions lack the full transformational capabilities of parsers.

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
pytest tests/
```

## Example output

TODO
