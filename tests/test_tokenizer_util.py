"""Test tokenizer utils."""
import unittest

import spacy

from traiter.pylib.old import tokenizer_util

NLP = spacy.load("en_core_web_sm")  # Singleton for testing


class TestTokenizerUtil(unittest.TestCase):
    def test_remove_special_case_01(self):
        special = [r for r in NLP.tokenizer.rules if r == "Ark."]
        self.assertEqual(special, ["Ark."])

        tokenizer_util.remove_special_case(NLP, [{"pattern": "Ark."}])
        special = [r for r in NLP.tokenizer.rules if r == "Ark."]
        self.assertEqual(special, [])
