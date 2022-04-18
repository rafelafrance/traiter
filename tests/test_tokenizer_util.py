"""Test tokenizer utils."""
import unittest

import spacy

from traiter import tokenizer_util


class TestTokenizerUtil(unittest.TestCase):
    def setUp(self) -> None:
        self.nlp = spacy.load("en_core_web_sm")

    def test_remove_special_case_01(self):
        special = [r for r in self.nlp.tokenizer.rules if r == "Ark."]
        self.assertEqual(special, ["Ark."])

        tokenizer_util.remove_special_case(self.nlp, [{"pattern": "Ark."}])
        special = [r for r in self.nlp.tokenizer.rules if r == "Ark."]
        self.assertEqual(special, [])
