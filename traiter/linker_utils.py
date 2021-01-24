"""Common linker functions."""

from collections import defaultdict


def linker(_, doc, idx, matches, linked):
    """Link traits to the root trait trait."""
    match_ents = defaultdict(list)
    for ent in doc.ents:
        for k, i in enumerate(matches[idx][1]):
            if ent.start <= i < ent.end:
                match_ents[ent].append(k)
                break
    match_ents = dict(sorted(match_ents.items(), key=lambda x: min(x[1])))
    root, *others = match_ents.keys()
    root = root._.data[linked]
    for ent in others:
        ent._.data[linked] = root
