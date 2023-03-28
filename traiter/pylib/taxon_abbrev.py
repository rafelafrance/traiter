"""Taxa are terms (see term_list.py) with 2 types of terms: binomials and monomials.

Taxon traits are build up from these two as well as other terms like ranks and names.
"""
from collections import defaultdict


def abbreviate_binomials(binomials: list[dict], singles_only=True):
    """Create a mapping from binomial terms to abbreviated binomials.

    Example: "C. lupus"  -> {"Canis lupus", "Cartoonus lupus"}
         or: "D. Duckus" -> {"Daffyus Duckus"}

    singles_only prunes this mapping to only known mappings. So in the example above
    only "D. Duckus" would be returned.
    """
    abbrevs = defaultdict(set)

    for term in binomials:
        pattern = term["pattern"]
        abbrev = abbreviate(pattern)
        abbrevs[abbrev].add(pattern.split()[0])

    if singles_only:
        abbrevs = {k: v.pop().title() for k, v in abbrevs.items() if len(v) == 1}

    return abbrevs


def abbreviate(pattern):
    genus, *parts = pattern.split()
    abbrev = genus[0].upper() + "."
    abbrev = " ".join([abbrev] + parts)
    return abbrev
