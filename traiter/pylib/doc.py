"""Utilities for converting PDFs into text."""

import re
import subprocess
import tempfile
from pathlib import Path

import pandas as pd
from traiter.pylib.util import FLAGS

from .util import now


# Todo move this into scripts
def clean_text_more(text):
    """Clean peculiarities particular to these guides."""
    text = re.sub(r'(?<= [a-z] -) \s (?= [a-z])', '', text, flags=FLAGS)
    text = re.sub(r'(?<= [a-z]) \s (?= - [a-z])', '', text, flags=FLAGS)
    text = re.sub(r'(?<=[a-z]) / (?=[a-z])', 'l', text, flags=FLAGS)
    return text


def import_files(cxn, paths, type_):
    """Load files into the database."""
    for path in paths:
        path = Path(path)
        doc_id = path.name
        if type_ == 'pdf':
            pdf_to_text(cxn, path, doc_id)
        else:
            import_text(cxn, path, doc_id)


def pdf_to_text(cxn, path, doc_id, timeout=30):
    """Load one PDF into the database."""
    with tempfile.NamedTemporaryFile(mode='w') as temp_file:
        cmd = f'pdftotext {path} {temp_file.name}'

        try:
            subprocess.check_call(cmd, shell=True, timeout=timeout)
        except Exception as err:  # pylint: disable=broad-except
            # TODO: report the error
            print(err)
            return

        with open(temp_file.name) as text_file:
            text = text_file.read()

    # TODO: Warn if the file is small

    text_to_db(cxn, doc_id, path, text, 'pdf to text')


def import_text(cxn, path, doc_id):
    """Load a text file and import it."""
    with open(path) as handle:
        text = handle.read()
        text_to_db(cxn, doc_id, path, text, 'text import')


def text_to_db(cxn, doc_id, path, text, method):
    """Import a text file into the database."""
    sql = """
        INSERT OR REPLACE INTO docs
            (doc_id, path, loaded, edited, extracted, method, raw, edits)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
    cxn.execute(sql, (doc_id, str(path), now(), '', '', method, text, text))
    cxn.commit()


def select_docs(cxn):
    """Get documents as a dataframe."""
    sql = """
        select doc_id, loaded, edited, extracted, method, path,
               length(raw) as size
          from docs
      order by doc_id;"""
    df = pd.read_sql(sql, cxn)
    return df


def select_doc_edits(cxn, doc_id):
    """Get a document for editing."""
    sql = """select edits from docs where doc_id = ?;"""
    result = cxn.execute(sql, (doc_id,)).fetchone()
    return result[0] if result else ''


def select_doc_raw(cxn, doc_id):
    """Get a document for editing."""
    sql = """select edits from docs where doc_id = ?;"""
    result = cxn.execute(sql, (doc_id,)).fetchone()
    return result[0] if result else ''


def update_doc(cxn, doc_id, edits):
    """Update the document with edits."""
    sql = """update docs set edits = ? where doc_id = ?;"""
    cxn.execute(sql, (edits, doc_id))
    cxn.commit()


def reset_doc(cxn, doc_id):
    """Reset the doc edits to back to the original text."""
    sql = """update docs set edits = raw where doc_id = ?;"""
    cxn.execute(sql, (doc_id,))
    cxn.commit()


def delete_docs(cxn, doc_ids):
    """Delete docs in the list of IDs."""
    sql = """delete from docs where doc_id = ?;"""
    for doc_id in doc_ids:
        cxn.execute(sql, (doc_id,))
    cxn.commit()
