"""Functions for handling terms in a term database."""
import sqlite3
from pathlib import Path
from typing import Union

from . import terms
from .. import const

DbPathType = Union[Path, str]

SHARED_DB = const.VOCAB_DIR / "terms.sqlite"


class Db(terms.Terms):
    """A dictionary of terms."""

    def create_db(self, database: DbPathType) -> None:
        """Build the term database."""
        self.create_term_tables(database)
        self.create_char_tables(database)
        self.create_spell_check_tables(database)

    @staticmethod
    def create_term_tables(database: DbPathType) -> None:
        """Build the term database."""
        sql = """
            create table if not exists terms (
                term_set text,
                label    text,
                pattern  text,
                attr     text,
                replace  blob,
                extra1   blob,
                extra2   blob
            );
            create index if not exists term_sets on terms (term_set);
            create index if not exists term_labels on terms (label);
            create index if not exists term_patterns on terms (pattern);

            create table if not exists term_columns (
                term_set text,
                extra    text,
                rename   text
            );
            create index if not exists term_column_sets on term_columns (term_set);
        """
        with sqlite3.connect(database) as cxn:
            cxn.executescript(sql)

    @staticmethod
    def create_char_tables(database: DbPathType) -> None:
        """A table to hold character distances used in multiple-sequence alignments."""
        sql = """
            create table if not exists chars (
                char1 text,
                char2 text,
                score real
            );
        """
        with sqlite3.connect(database) as cxn:
            cxn.executescript(sql)

    @staticmethod
    def create_spell_check_tables(database: DbPathType) -> None:
        """Create tables used for spell checking."""
        sql = """
            create table if not exists vocab (
                word text,
                freq integer
            );

            create table if not exists misspellings (
                miss text,
                word text,
                dist text,
                freq integer
            );
        """
        with sqlite3.connect(database) as cxn:
            cxn.executescript(sql)

    @classmethod
    def select_term_set(cls, database: DbPathType, term_set: str) -> "Db":
        """Select all terms for the given group."""
        sql = "select extra, rename from term_columns where term_set = ?"
        with sqlite3.connect(database) as cxn:
            extras = cxn.execute(sql, (term_set,))

        sql = "select label, pattern, attr, replace"
        for extra in extras:
            sql += f", {extra[0]} as {extra[1]}"
        sql += " from terms where term_set = ?"

        with sqlite3.connect(database) as cxn:
            cxn.row_factory = sqlite3.Row
            terms_ = [dict(r) for r in cxn.execute(sql, (term_set,))]

            if not terms_:
                err = f'\nShared terms "{term_set}" not found in the shared database.'
                raise Exception(err)

        return cls(terms=terms_)

    @classmethod
    def shared(cls, term_sets: terms.StrList) -> "Db":
        """Get terms from a shared vocabulary database."""
        term_sets = term_sets.split() if isinstance(term_sets, str) else term_sets

        terms_ = cls()

        for term_set in term_sets:
            terms_ += cls.select_term_set(SHARED_DB, term_set)

        return terms_
