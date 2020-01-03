"""Common functions for dealing with the database."""

import sqlite3

RAW_TABLE = 'raw'
RAW_ID = 'raw_id'


def connect(path: str) -> sqlite3.Connection:
    """Connect to an SQLite database."""
    cxn = sqlite3.connect(path)

    cxn.execute('PRAGMA page_size = {}'.format(2 ** 16))
    cxn.execute('PRAGMA busy_timeout = 10000')
    cxn.execute('PRAGMA journal_mode = WAL')
    cxn.row_factory = sqlite3.Row
    return cxn


def select_raw(cxn: sqlite3.Connection,
               limit: int = 0,
               offset: int = 0) -> sqlite3.Cursor:
    """Get raw records."""
    clause = f'LIMIT {limit}' if limit else ''
    clause += f' OFFSET {offset}' if offset else ''
    return cxn.execute(f'SELECT * FROM {RAW_TABLE} {clause};')
