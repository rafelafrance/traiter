"""Utilities for working with vocabularies.

Based off of symmetric deletes method from SeekStorm. MIT license.
https://seekstorm.com/blog/1000x-spelling-correction/
"""
import logging
import sqlite3

import regex as re

from .const import DATA_DIR


class SpellWell:
    def __init__(self, vocab_db=None, min_freq=5, min_len=3, vocab_freq=10):
        self.min_len = min_len
        self.min_freq = min_freq
        self.vocab_freq = vocab_freq
        self.vocab_db = vocab_db if vocab_db else DATA_DIR / "spell_well.sqlite"
        self.cxn = sqlite3.connect(":memory:")
        self.db_to_memory()

    def db_to_memory(self):
        create1 = """
            create table spells as
            select * from aux.misspellings where freq >= ? and length(miss) >= ?;
            """
        create2 = """
            create table vocab as
            select * from aux.vocab where freq >= ?;
            """
        indexes = """
            create index spells_miss on spells (miss);
            create index vocab_word on vocab (word);
            """
        try:
            self.cxn.execute(f"attach database '{self.vocab_db}' as aux")
            self.cxn.execute(create1, (self.min_freq, self.min_len))
            self.cxn.execute(create2, (self.vocab_freq,))
            self.cxn.executescript(indexes)
            self.cxn.execute("detach database aux")
        except sqlite3.OperationalError as err:
            logging.error(err)

    def correct(self, word: str) -> str:
        if not word:
            return ""

        if hit := (self.best([word], 0) or self.best([word], 1)):
            return hit

        all_deletes = deletes1(word) | deletes2(word)

        if hit := self.best(list(all_deletes), 1):
            return hit

        return word

    def best(self, words, dist: int) -> str:
        q_marks = ", ".join(["?"] * len(words))
        args = words + [dist]
        sql = f"""select word, dist, freq
                    from spells
                   where miss in ({q_marks})
                     and dist <= ?
                order by freq desc"""
        hit = self.cxn.execute(sql, args).fetchone()
        return hit[0] if hit else ""

    @staticmethod
    def is_letters(text: str) -> bool:
        return bool(re.match(r"^\p{L}+$", text))

    @staticmethod
    def tokenize(text: str) -> list[str]:
        """Split the text into words and non-words."""
        return re.split(r"([^\p{L}]+)", text)

    def is_word(self, word: str) -> bool:
        sql = "select word from vocab where word = ?"
        hit = self.cxn.execute(sql, (word,)).fetchone()
        return bool(hit)

    def freq(self, word: str) -> int:
        sql = "select freq from vocab where word = ?"
        hit = self.cxn.execute(sql, (word,)).fetchone()
        return hit[0] if hit else 0

    def hits(self, text: str) -> int:
        """Count the number of words in the text that are in our corpus.

        A hit is:
        - A direct match in the vocabularies
        - A number like: 99.99
        """
        count = sum(1 for w in self.tokenize(text) if self.is_word(w))
        count += sum(1 for _ in re.findall(r"\d+", text))
        return count


def deletes1(word: str) -> set[str]:
    return {word[:i] + word[i + 1 :] for i in range(len(word))}


def deletes2(word: str) -> set[str]:
    return {d2 for d1 in deletes1(word) for d2 in deletes1(d1)}
