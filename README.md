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

If you prefer to not deal with setting up a virtual environment then you can install the requirements into your. WARNING: This can cause conflicts with other project requirements.

```
git clone https://github.com/rafelafrance/traiter.git
python3 -m pip install --user -r traiter/requirements.txt
```

# Run

traiter/traiter.py vertnet-file.csv

# Running tests

pytest tests/
