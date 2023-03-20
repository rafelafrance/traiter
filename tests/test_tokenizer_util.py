import unittest

from tests.setup import PIPELINE
from traiter.pylib import tokenizer_util


class TestTokenizerUtil(unittest.TestCase):
    def test_remove_special_case_01(self):
        special = [r for r in PIPELINE.nlp.tokenizer.rules if r == "Jan."]
        self.assertEqual(special, ["Jan."])

        tokenizer_util.remove_special_case(PIPELINE.nlp, ["Jan."])
        special = [r for r in PIPELINE.nlp.tokenizer.rules if r == "Jan."]
        self.assertEqual(special, [])
