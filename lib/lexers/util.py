"""Lexer utilities."""


def boundary(regex):
    r"""Wrap a regular expression in \b character class.

    This is used to "boundary" a word on a word boundary so the regex does
    not match the interior of a word.

    - This is helpful for keyword searches like 't'. Without this 't' would
      match both 't's in 'that' but the regex in \b neither 't' is matched.
      Only 't's like ' t ', or '$t.', etc. will match.
    - It is not helpful for searching for things like '19mm' where there is
      no word break between the two tokens.
    - It is also not helpful if your pattern ends or starts with a non-word
      character.
    """
    return r'\b (?: {} ) \b'.format(regex)
