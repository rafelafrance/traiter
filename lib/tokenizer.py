"""Tokenize the notations."""

import re


SPACES = 1
NUMBER = 2
WORD = 3

PUNCT = 100
LPAR = PUNCT + 1
RPAR = PUNCT + 2
LSQB = PUNCT + 3
RSQB = PUNCT + 4
COLON = PUNCT + 5
COMMA = PUNCT + 6
SEMI = PUNCT + 7
PLUS = PUNCT + 8
DASH = PUNCT + 9
STAR = PUNCT + 10
SLASH = PUNCT + 11
VBAR = PUNCT + 12
AMPER = PUNCT + 13
LESS = PUNCT + 14
GREATER = PUNCT + 15
EQUAL = PUNCT + 16
DOT = PUNCT + 17
PERCENT = PUNCT + 18
LBRACE = PUNCT + 19
RBRACE = PUNCT + 20
AT = PUNCT + 21
SQUOTE = PUNCT + 22
DQUOTE = PUNCT + 23
QUEST = PUNCT + 24
BSLASH = PUNCT + 25
OTHER = 1000

PUNCT_TOKENS = {
    '(': LPAR,
    ')': RPAR,
    '[': LSQB,
    ']': RSQB,
    ':': COLON,
    ',': COMMA,
    ';': SEMI,
    '+': PLUS,
    '-': DASH,
    '*': STAR,
    '/': SLASH,
    '|': VBAR,
    '&': AMPER,
    '<': LESS,
    '>': GREATER,
    '=': EQUAL,
    '.': DOT,
    '%': PERCENT,
    '{': LBRACE,
    '}': RBRACE,
    '@': AT,
    "'": SQUOTE,
    '"': DQUOTE,
    '?': QUEST,
    r'\\': BSLASH,
}

# For our purposes NUMBER_REGEXs are always positive and decimals
NUMBER_REGEX = r""" (?: \d{1,3} (?: , \d{3} ){1,3} | \d+ ) (?: \. \d+ )? """
SPACES_REGEX = r""" \s+ """
WORD_REGEX = r""" \w+ """
PUNCT_REGEX = r""" \W """

# NUMBER_REGEX must go before WORD_REGEX
# SPACES_REGEX must go before PUNCT_REGEX
REGEX = re.compile(
    f' {NUMBER_REGEX} | {SPACES_REGEX} | {WORD_REGEX} | {PUNCT_REGEX} ',
    re.VERBOSE)


def tokenize(text):
    """Split the text into tokens."""
    raw_tokens = REGEX.findall(text)

    tokens = []

    start = 0  # Start of the match
    end = 0    # End of the match

    for raw_token in raw_tokens:
        start = end
        end = start + len(raw_token)

        if raw_token[0].isspace():
            tokens.append((SPACES, raw_token, start, end))
        elif raw_token[0].isnumeric():
            tokens.append((NUMBER, raw_token, start, end))
        elif raw_token[0].isalpha():
            tokens.append((WORD, raw_token, start, end))
        else:
            token = PUNCT_TOKENS.get(raw_token[0], OTHER)
            tokens.append((token, raw_token, start, end))

    return tokens
