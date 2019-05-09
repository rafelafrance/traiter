import unittest
from lib.parse import Parse
from lib.traits.ovaries_size_trait import OvariesSizeTrait


PAR = OvariesSizeTrait()


class TestOvariesSizeTrait(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('testes = 8x5 mm'),
            [Parse(value=[8, 5], units='mm', start=0, end=15)])
