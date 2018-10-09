# -*- coding: utf-8 -*-
# Adapted from https://github.com/un33k/python-slugify/blob/master/test.py
__version__ = "slugify_test.py 2016-05-30T20:34-03:00"

import unittest
from slugify import slugify

class TestSlugification(unittest.TestCase):

    def test_extraneous_seperators(self):
        print 'testing extraneous_seperators'
        txt = "This is a test ---"
        r = slugify(txt)
        self.assertEqual(r, "this-is-a-test")

        txt = "___This is a test ---"
        r = slugify(txt)
        self.assertEqual(r, "this-is-a-test")

        txt = "___This is a test___"
        r = slugify(txt)
        self.assertEqual(r, "this-is-a-test")

    def test_non_word_characters(self):
        print 'testing non_word_characters'
        txt = "This -- is a ## test ---"
        r = slugify(txt)
        self.assertEqual(r, "this-is-a-test")

    def test_phonetic_conversion_of_eastern_scripts(self):
        print 'testing phonetic_conversion_of_eastern_scripts'
        txt = '影師嗎'
        r = slugify(txt)
        self.assertEqual(r, "ying-shi-ma")

    def test_accented_text(self):
        print 'testing accented_text'
        txt = 'C\'est déjà l\'été.'
        r = slugify(txt)
        self.assertEqual(r, "c-est-deja-l-ete")

        txt = 'Nín hǎo. Wǒ shì zhōng guó rén'
        r = slugify(txt)
        self.assertEqual(r, "nin-hao-wo-shi-zhong-guo-ren")

        txt = 'aàáâäãåāǎæ'
        r = slugify(txt)
        self.assertEqual(r, "aaaaaaaaaae")

    def test_accented_text_with_non_word_characters(self):
        print 'testing accented_text_with_non_word_characters'
        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt)
        self.assertEqual(r, "jaja-lol-mememeoo-a")

    def test_cyrillic_text(self):
        print 'testing cyrillic_text'
        txt = 'Компьютер'
        r = slugify(txt)
        self.assertEqual(r, "kompiuter")

    def test_max_length(self):
        print 'testing max_length'
        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=9)
        self.assertEqual(r, "jaja-lol")

        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=15)
        self.assertEqual(r, "jaja-lol-mememe")

    def test_max_length_cutoff_not_required(self):
        print 'testing max_length_cutoff_not_required'
        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=50)
        self.assertEqual(r, "jaja-lol-mememeoo-a")

    def test_word_boundary(self):
        print 'testing word_boundary'
        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=15, word_boundary=True)
        self.assertEqual(r, "jaja-lol-a")

        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=17, word_boundary=True)
        self.assertEqual(r, "jaja-lol-mememeoo")

        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=18, word_boundary=True)
        self.assertEqual(r, "jaja-lol-mememeoo")

        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=19, word_boundary=True)
        self.assertEqual(r, "jaja-lol-mememeoo-a")

    def test_custom_separator(self):
        print 'testing custom_separator'
        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=20, word_boundary=True, separator=".")
        self.assertEqual(r, "jaja.lol.mememeoo.a")

    def test_multi_character_separator(self):
        print 'testing multi_character_separator'
        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=20, word_boundary=True, separator="ZZZZZZ")
        self.assertEqual(r, "jajaZZZZZZlolZZZZZZmememeooZZZZZZa")

    def test_save_order(self):
        print 'testing save_order'
        txt = 'one two three four five'
        r = slugify(txt, max_length=13, word_boundary=True, save_order=True)
        self.assertEqual(r, "one-two-three")

        txt = 'one two three four five'
        r = slugify(txt, max_length=13, word_boundary=True, save_order=False)
        self.assertEqual(r, "one-two-three")

        txt = 'one two three four five'
        r = slugify(txt, max_length=12, word_boundary=True, save_order=False)
        self.assertEqual(r, "one-two-four")

        txt = 'one two three four five'
        r = slugify(txt, max_length=12, word_boundary=True, save_order=True)
        self.assertEqual(r, "one-two")

    def test_stopword_removal(self):
        print 'testing stopword_removal'
        txt = 'this has a stopword'
        r = slugify(txt, stopwords=['stopword'])
        self.assertEqual(r, 'this-has-a')

    def test_multiple_stopword_occurances(self):
        print 'testing multiple_stopword_occurances'
        txt = 'the quick brown fox jumps over the lazy dog'
        r = slugify(txt, stopwords=['the'])
        self.assertEqual(r, 'quick-brown-fox-jumps-over-lazy-dog')

    def test_differently_cased_stopword_match(self):
        print 'testing differently_cased_stopword_match'
        txt = 'Foo A FOO B foo C'
        r = slugify(txt, stopwords=['foo'])
        self.assertEqual(r, 'a-b-c')

        txt = 'Foo A FOO B foo C'
        r = slugify(txt, stopwords=['FOO'])
        self.assertEqual(r, 'a-b-c')

    def test_multiple_stopwords(self):
        print 'testing multiple_stopwords'
        txt = 'the quick brown fox jumps over the lazy dog in a hurry'
        r = slugify(txt, stopwords=['the', 'in', 'a', 'hurry'])
        self.assertEqual(r, 'quick-brown-fox-jumps-over-lazy-dog')

    def test_stopwords_with_different_separator(self):
        print 'testing stopwords_with_different_separator'
        txt = 'the quick brown fox jumps over the lazy dog'
        r = slugify(txt, stopwords=['the'], separator=' ')
        self.assertEqual(r, 'quick brown fox jumps over lazy dog')

    def test_html_entities(self):
        print 'testing html_entities'
        txt = 'foo &amp; bar'
        r = slugify(txt)
        self.assertEqual(r, 'foo-bar')

    def test_starts_with_number(self):
        print 'testing starts_with_number'
        txt = '10 amazing secrets'
        r = slugify(txt)
        self.assertEqual(r, '10-amazing-secrets')

    def test_contains_numbers(self):
        print 'testing contains_numbers'
        txt = 'buildings with 1000 windows'
        r = slugify(txt)
        self.assertEqual(r, 'buildings-with-1000-windows')

    def test_ends_with_number(self):
        print 'testing ends_with_number'
        txt = 'recipe number 3'
        r = slugify(txt)
        self.assertEqual(r, 'recipe-number-3')

    def test_numbers_only(self):
        print 'testing numbers_only'
        txt = '404'
        r = slugify(txt)
        self.assertEqual(r, '404')

    def test_numbers_and_symbols(self):
        print 'testing numbers_and_symbols'
        txt = '1,000 reasons you are #1'
        r = slugify(txt)
        self.assertEqual(r, '1000-reasons-you-are-1')

if __name__ == '__main__':
    unittest.main()