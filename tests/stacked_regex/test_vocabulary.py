"""Test the rule catalog object."""

import unittest
from pylib.stacked_regex.vocabulary import Vocabulary
from pylib.stacked_regex.rule import term, part, grouper


class TestVocabulary(unittest.TestCase):
    """Test the rule catalog object."""
    p1 = part('p1', 'my_part1')
    t1 = term('t1', 'my_term1')
    t2 = term('t2', 'my_term2')
    g1 = grouper('g1', 't1')
    g2 = grouper('g2', 't1 t2')
    g3 = grouper('g3', 'g1 g2')
    g4 = grouper('g4', 'p1 g1 g2')

    def test_part_01(self):
        """It adds a part rule."""
        cat = Vocabulary()
        cat.part(self.p1.name, self.p1.pattern)
        expect = {self.p1.name: self.p1}
        self.assertEqual(cat.rules, expect)

    def test_term_01(self):
        """It adds a term rule."""
        cat = Vocabulary()
        cat.term(self.t1.name, self.t1.pattern)
        expect = {self.t1.name: self.t1}
        self.assertEqual(cat.rules, expect)

    def test_grouper_01(self):
        """It adds a grouper rule and a sub-rule."""
        cat = Vocabulary()
        cat.term(self.t1.name, self.t1.pattern)
        cat.grouper(self.g1.name, self.g1.pattern)
        expect = {
            self.t1.name: self.t1,
            self.g1.name: [self.t1, self.g1],
        }
        self.assertEqual(cat.rules, expect)

    def test_grouper_02(self):
        """It adds a grouper rule and two sub-rules."""
        cat = Vocabulary()
        cat.term(self.t1.name, self.t1.pattern)
        cat.term(self.t2.name, self.t2.pattern)
        cat.grouper(self.g2.name, self.g2.pattern)
        expect = {
            self.t1.name: self.t1,
            self.t2.name: self.t2,
            self.g2.name: [self.t1, self.t2, self.g2],
        }
        self.assertEqual(cat.rules, expect)

    def test_grouper_03(self):
        """It adds sub-rules recursively."""
        cat = Vocabulary()
        cat.term(self.t1.name, self.t1.pattern)
        cat.term(self.t2.name, self.t2.pattern)
        cat.grouper(self.g1.name, self.g1.pattern)
        cat.grouper(self.g2.name, self.g2.pattern)
        cat.grouper(self.g3.name, self.g3.pattern)
        expect = {
            self.t1.name: self.t1,
            self.t2.name: self.t2,
            self.g1.name: [self.t1, self.g1],
            self.g2.name: [self.t1, self.t2, self.g2],
            self.g3.name: [self.t1, self.t2, self.g1, self.g2, self.g3],
        }
        self.assertEqual(cat.rules, expect)

    def test_grouper_04(self):
        """It adds sub-rules recursively and handles basal patterns."""
        cat = Vocabulary()
        cat.part(self.p1.name, self.p1.pattern)
        cat.term(self.t1.name, self.t1.pattern)
        cat.term(self.t2.name, self.t2.pattern)
        cat.grouper(self.g1.name, self.g1.pattern)
        cat.grouper(self.g2.name, self.g2.pattern)
        cat.grouper(self.g3.name, self.g3.pattern)
        cat.grouper(self.g4.name, self.g4.pattern)
        expect = {
            self.p1.name: self.p1,
            self.t1.name: self.t1,
            self.t2.name: self.t2,
            self.g1.name: [self.t1, self.g1],
            self.g2.name: [self.t1, self.t2, self.g2],
            self.g3.name: [self.t1, self.t2, self.g1, self.g2, self.g3],
            self.g4.name: [
                self.p1, self.t1, self.t2, self.g1, self.g2, self.g4],
        }
        self.assertEqual(cat.rules, expect)
