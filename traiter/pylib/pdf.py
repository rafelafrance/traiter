"""Common utilities for dealing with PDF files."""
from collections import Counter

import regex

import sys
from traiter.pylib.util import FLAGS


TRANS_TABLE = {'¼': '='}
TRANS = str.maketrans(TRANS_TABLE)

NOISE = regex.compile(
    (r'^ \s* ( abstract | fig[.u] | C \s The \s Authors .* '
     r'     | All \s rights \s reserved .* )'),
    flags=FLAGS)


def translate():
    """Translate characters."""
    for line in sys.stdin.readlines():
        line = line.translate(TRANS)
        sys.stdout.write(line)


def clean_text(text, remove_inserts=False, space_normalize=True):
    """Remove headers & footers and join hyphenated words etc."""
    pages = text.count('\f')

    # Remove figure notes, abstract, etc.
    lines = []
    keys = []
    removing = False
    for ln in text.splitlines():
        if NOISE.match(ln):
            removing = True & remove_inserts
        elif len(ln) == 0:
            removing = False
        elif removing:
            pass
        elif regex.match(r'^ \s* \d{0,4} \s* $', ln, flags=FLAGS):
            pass
        else:
            lines.append(ln)
            key = regex.sub(r'^\s*\d+|\d+\s*$', ' ', ln)
            key = ' '.join(key.split())
            keys.append(key)

    # Find and remove page headers and footers
    counts = Counter(keys)
    patterns = []
    for pattern, n in counts.most_common(4):
        if n >= pages / 2:
            pattern = regex.sub(r'\s+', r'\s*', pattern)
            pattern = fr'^ [\s\d]* {pattern} [\s\d]* $'
            patterns.append(pattern)

    pattern = ' | '.join(patterns)
    pattern = regex.compile(pattern, flags=FLAGS)

    lines = [ln for ln in lines if not pattern.match(ln)]

    # Join the lines text
    text = '\n'.join(lines)

    # Joining hyphens has to happen after the removal of headers & footers
    text = regex.sub(r' [–-] \n ([a-z]) ', r'\1', text, flags=FLAGS)

    # Space normalize text
    if space_normalize:
        text = ' '.join(text.split())

    return text
