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
 - As well as measurements embedded in prose like: `Snout vent lengths range anywhere from 16 to 23 cm.` I am experimenting with various distances between the anchor token `Snout vent lengths` and the measurements `16 to 23 cm`.
 - We flag ambiguous measurements like: `length: 12.0`. This may be a total length measurement or another length measurement.
 - We also flag numeric measurements without units like: `total length = 120`. The units may be the default millimeters.
 - etc.

We also extract values from controlled vocabularies.
 - These values sometimes have a signifier like `Life Stage: Adult`
 - And other times we see a value on its own like `Adult` without the signifier.

## List of traits extracted
- Body body mass
- Total length (aka snout vent length, fork length, etc.)
- Sex
- Life stage
- Testes state
- Testes size
- Tail Length (In progress)
- Hind foot Length (In progress)
- Ear Length (In progress)


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
Then you can run the tests like so:
```
python -m pytest tests/
```
