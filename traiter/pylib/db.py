"""Common functions for dealing with the database."""

import sqlite3
import subprocess
from os import fspath, remove
from pathlib import Path

from .util import today

# DB = DATA_DIR / f'{NAME}.sqlite3.db'
SCRIPT_PATH = Path('.') / 'traiter' / 'sql'


def connect(path):
    """Connect to an SQLite database."""
    return sqlite3.connect(path)


def get_metadata(cxn, key, default=''):
    """Get metadata from the database."""
    sql = """SELECT datum FROM metadata WHERE label = ?"""
    try:
        result = cxn.execute(sql, (key,))
        result = result.fetchone()
        return default if not result else result[0]
    except sqlite3.OperationalError:
        return default


def create(cxn, path):
    """Create the database."""
    script = fspath(SCRIPT_PATH / 'create_db.sql')
    with open(script) as script_file:
        script = script_file.read()

    if path != ':memory:':
        remove(path)
        cxn = connect(path)

    cxn.executescript(script)
    return cxn


def backup_database(path):
    """Backup the SQLite3 database."""
    backup = f'{path[:-3]}.{today()}.db'
    cmd = f'cp {path} {backup}'
    return subprocess.check_call(cmd, shell=True)
