# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.parsers.base_parser import BaseParser
from lib.lexers.base_lexer import BaseLexer


class TestBaseParser(unittest.TestCase):

    pass


TK = BaseParser(BaseLexer)
SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(TestBaseParser)
unittest.TextTestRunner().run(SUITE)
