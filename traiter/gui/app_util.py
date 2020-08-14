"""Utilities common to all app tabs and menus."""

import tkinter as tk
from os.path import basename, splitext

import traiter.pylib.doc as doc
import traiter.pylib.script as script_lib


MEMORY = ':memory:'


def get_title(app):
    """Build the window title."""
    title = splitext(basename(app.path))[0]
    return f'Traiter ({title})'


def repopulate(app):
    """Repopulate the controls from new data."""
    app.win.title(get_title(app))
    app.docs = doc.select_docs(app.cxn)
    app.docs.set_index('doc_id', inplace=True)

    app.doc_tree.delete(*app.doc_tree.get_children())
    for doc_id, row in app.docs.iterrows():
        app.doc_tree.insert('', tk.END, text=doc_id, values=list(row))

    app.doc_tree.column('#0', stretch=True)
    app.doc_tree.heading('#0', text='document')
    for col in app.docs.columns:
        app.doc_tree.column(col, stretch=True)
        app.doc_tree.heading(col, text=col)

    doc_ids = app.docs.index.tolist()
    if doc_ids:
        app.doc_sel['values'] = [''] + doc_ids
        app.doc_sel['width'] = max(len(i) for i in doc_ids)
        app.doc_sel.current(0)
    else:
        app.doc_sel['values'] = ['']

    app.scripts = script_lib.select_scripts(app.cxn)
    app.scripts.set_index('script_id', inplace=True)
    app.script_tree.delete(*app.script_tree.get_children())
    for script_id, row in app.scripts.iterrows():
        app.script_tree.insert(
            '', tk.END, text=script_id, values=list(row))

    app.script_tree.column('#0', stretch=True)
    app.script_tree.heading('#0', text='name')
    for col in app.scripts.columns:
        app.script_tree.column(col, stretch=True)
        app.script_tree.heading(col, text=col)

    script_ids = app.scripts.index.tolist()
    if script_ids:
        app.script_sel['values'] = [''] + script_ids
        app.script_sel['width'] = max(len(i) for i in script_ids)
        app.script_sel.current(0)
    else:
        app.script_sel['values'] = ['']


def doc_selected(app, _=None):
    """Update the doc edit text box when selected."""
    app.doc_id = app.doc_sel.get()
    text = doc.select_doc_edits(app.cxn, app.doc_id)
    app.edits.delete('1.0', tk.END)
    app.edits.insert(tk.INSERT, text)
