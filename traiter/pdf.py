"""Common utilities for dealing with PDF files."""
import subprocess
from collections import Counter
from os.path import exists, splitext

import regex

from .util import FLAGS


TRANS_TABLE = {'¼': '='}
TRANS = str.maketrans(TRANS_TABLE)

NOISE = regex.compile(
    (r'^ \s* ( abstract | fig[.u] | C \s The \s Authors .* '
     r'     | All \s rights \s reserved .* )'),
    flags=FLAGS)


def pdf2txt(pdf_dir, txt_dir):
    """Convert PDF files into text."""
    for pdf in pdf_dir.glob('*.pdf'):
        txt = txt_dir / (splitext(pdf.name)[0] + '.txt')
        if not exists(txt):
            cmd = f'pdftotext {pdf} {txt}'
            subprocess.check_call(cmd, shell=True)


def clean_text(text):
    """Remove headers & footers and join hyphenated words etc."""
    pages = text.count('\f')

    # Remove figure notes, abstract, etc.
    lines = []
    keys = []
    removing = False
    for ln in text.splitlines():
        if NOISE.match(ln):
            removing = True
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
    text = ' '.join(text.split())

    return text
