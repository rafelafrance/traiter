# The Traits Database Project [![Build Status](https://travis-ci.org/rafelafrance/traiter.svg?branch=master)](https://travis-ci.org/rafelafrance/traiter)

## All right, what's this all about then?
**Challenge**: Extract trait information from unstructured or semi-structured natural history field notations. That is, if I'm given text like:

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

This implementation uses a technique that I call **"Stacked Regular Expressions"**. The concept is very simple, we build tokens in one step and in the next two steps we use those tokens to reduce combinations to other tokens or productions.

1. Tokenize the text.
2. (Optional) Replace sequences of tokens to simplify the token stream. Repeat this step as many times as needed.
3. Convert sequences of tokens into the final productions.
* Postprocessing of the extracted information is performed by the caller.

All steps use regular expressions. Step 1 uses them on raw text like any other regular expression but the other two steps use them on the token stream. The regular expressions on the token stream look and behave just like normal regular expressions but they are adjusted to work on tokens & not text. I.e. steps 2 & 3 use a domain specific language (DSL) for the token-level regular expressions.

Note that I am trying to extract data from patterns of text and not parse a formal language. Most importantly, I don't need to worry about recursive structures. Pattern recognition is a common technique in **Natural Language Processing, Information Extraction**.

Another point to note, is that we want to parse gigabytes (or terabytes) of data in a "reasonable" amount of time. So speed may not be the primary concern but having fast turnaround is still important. The development of parsers that use this module tends to be iterative.

#### 1. Tokenize the text
Replace text with tokens. We use regular expressions to create a token stream from the raw text. During this process, any text that is not captured by a token regex is removed from the token stream, i.e. noise is removed from the text.
   
The following regular expressions will return a sequence of tokens with the name as one of (animal, color, etc.) and what the regular expression matches as the value of the token. 

```python
keyword('animal', r' dogs? | cats? ')
keyword('color', r' brown | black | white | tan | gr [ae] y')
keyword('age', r' adult | puppy | younger | older ')
keyword('fur', r' fur | hair ' )
fragment('and', r' [&] | \b and \b ')
```

`keyword` and `fragment` are methods for adding token regular expressions to the parser. The `keyword` surrounds a pattern with `\b` word-separator character class and the `fragment` method does not.

Tokens are scanned in order so if two tokens would read the same sequence of characters the first one wins. This can be very useful when you have pattern conflicts.

Given these rules and the following text: `The specimen is an older dog with tan and gray fur,` Will produce the following tokens:
- {age: older}
- {animal: dog}
- {color: tan}
- {and: and}
- {color: gray}

Notice that there are no tokens for any of the spaces, any of the words "The specimen is a", or the final `,` comma. We have removed the "noise". This turns out to be very helpful with simplifying the parsers. 

#### 2. (Optional) Replace sequences of tokens to simplify the token stream. Repeat this step as many times as needed.

Replace tokens with other tokens. Use a DSL to capture sets of tokens that may be combined into a single token. This simplification step is often repeated so simplifications may be built up step-wise.

```python
replacer('graying', ' color and color ')
```

Continuing the example above the three tokens:
- {color: tan}
- {and: and}
- {color: gray}

Are replaced with the single token:
- {graying: 'tan and gray'}

Note that this rule will match any pair of colors linked by the word "and". Also note that the original information is preserved. So the new "graying" token also has the color list of `["tan", "gray"]`.
 
#### 3. Convert sequences of tokens into the final productions
Replace tokens with the final tokens. Everything except the final tokens are removed. This final stream of tokens is what the client code processes.

Here is a rule for recognizing fur color.

```python
def fur_color(token):
    # Process the token for fur color.

producer(fur_color, r' ( color | mixed_color ) fur ')
```

Keeping with the example above we get the following information:
- {fur_color: 'tan and gray fur'}

 Combined token data is preserved just like it is in step 2. We will have the fur_color data but also the color list of `["tan", "gray"]`.

#### The domain specific language.

Token names are just regular expression group names and follow the same rules. All rules are case insensitive and use the verbose regular expression syntax.

The replacers and producers (steps 2 & 3 not in step 1). Use a simple domain specific language based on regular expressions. In fact, they are just slightly modified regular expressions. The only conceptual difference is that a token in a replacer or producer regular expression can be treated as if it is a single character. So you can do things like:
```python
keyword('modifier', 'dark | light')
replacer('color_phrase', ' modifier? color ')
```
The "modifier" token is treated as a single unit. But also note that you still have to group multiple tokens if you want to do something like:
```python
keyword('modifier', 'dark | light')
replacer('color_phrase', ' modifier? ( color and )? color ')
```
Here "color and" is two tokens and must be grouped as you would have to group letters in a normal regular expression.

## Install

You will need to have Python3 installed, as well as pip, a package manager for python. You can install the requirements into your python environment like so:
```
git clone https://github.com/rafelafrance/traiter.git
python3 -m pip install --user --requirement traiter/requirements.txt
```
  
## Run
```
python3 traiter.py ... TODO ...
```

## Tests
Having a test suite is absolutely critical. The strategy I use is every new pattern gets its own test. Any time there is a parser error I add the parts that caused the error to the test suite and correct the parser. I.e. I use the standard red/green testing methodology.

You can run the tests like so:
```
cd /my/path/to/traiter
python -m unittest discover
```
