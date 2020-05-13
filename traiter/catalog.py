"""Build catalogs of terms and their parts for sharing."""

import csv
from collections import defaultdict

CODE_LEN = 5
CODES = defaultdict(lambda: f'{len(CODES)+1:04x}_')


class Catalog:
    """Build catalogs of terms and their parts for sharing."""

    def __init__(self, other: 'Catalog' = None) -> None:
        self.terms = dict(other.terms) if other else {}

    def __getitem__(self, name):
        """Emulate dict access of the rules."""
        return self.terms[name]

    def __iter__(self):
        """Loop over the term values."""
        yield from self.terms.values()

    def read_terms(self, path):
        """Read terms from a file."""
        with open(path) as term_file:
            reader = csv.DictReader(term_file)
            terms = {t['term']: t for t in reader}
        self.terms = {**self.terms, **terms}

    def get_term_replacements(self, term_list):
        """Get replacement values for the terms."""
        return {v['term']: r for v in self.terms.values()
                if (r := v.get('replace')) and v['type'] in term_list}
