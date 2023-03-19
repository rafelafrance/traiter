import unittest

from .setup import PIPELINE
from traiter.pylib import tokenizer_util


class TestTokenizerUtil(unittest.TestCase):
    def test_remove_special_case_01(self):
        special = [r for r in PIPELINE.nlp.tokenizer.rules if r == "Ark."]
        self.assertEqual(special, ["Ark."])

        tokenizer_util.remove_special_case(PIPELINE.nlp, [{"pattern": "Ark."}])
        special = [r for r in PIPELINE.nlp.tokenizer.rules if r == "Ark."]
        self.assertEqual(special, [])
