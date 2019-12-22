"""Common functions for dealing with the database."""

import sqlite3


def connect(path=None):
    """Connect to an SQLite database."""
    cxn = sqlite3.connect(path)

    cxn.execute('PRAGMA page_size = {}'.format(2 ** 16))
    cxn.execute('PRAGMA busy_timeout = 10000')
    cxn.execute('PRAGMA journal_mode = WAL')
    return cxn
