"""Import tab for the main app."""

import tkinter as tk
import tkinter.ttk as ttk
from os.path import dirname
from tkinter import filedialog

import traiter.pylib.doc as doc
from .app_util import doc_selected, repopulate


def build_import_tab(app):
    """Build import tab for the main app."""

    app.docs = None
    app.doc_tree = None

    tab = ttk.Frame(app.notebook)
    app.notebook.add(tab, text='Import')

    tab_frame = ttk.Frame(tab)
    tab_frame.pack(expand=True, fill='both')

    sub_frame = ttk.Frame(tab_frame)
    sub_frame.pack(expand=False, fill='x', pady=(24, 24))

    button = ttk.Button(
        sub_frame, text='PDF to Text...', command=lambda: pdf_to_text(app))
    button.pack(side=tk.LEFT, padx=(8, 8))

    button = ttk.Button(
        sub_frame, text='Import Text...', command=lambda: import_text(app))
    button.pack(side=tk.LEFT, padx=(8, 8))

    button = ttk.Button(
        sub_frame, text='OCR PDF...', state=tk.DISABLED,
        command=lambda: ocr_pdf(app))
    button.pack(side=tk.LEFT, padx=(8, 8))

    sub_frame = ttk.Frame(tab_frame)
    sub_frame.pack(expand=True, fill='both')

    app.docs = doc.select_docs(app.cxn)
    app.docs.set_index('doc_id', inplace=True)

    app.doc_tree = ttk.Treeview(sub_frame)
    app.doc_tree.bind('<Double-Button-1>', lambda _: select_doc(app))
    app.doc_tree['columns'] = list(app.docs.columns)
    app.doc_tree.column('#0', stretch=True)
    app.doc_tree.heading('#0', text='document')
    for col in app.docs.columns:
        app.doc_tree.column(col, stretch=True)
        app.doc_tree.heading(col, text=col)

    vsb = ttk.Scrollbar(
        sub_frame, orient='vertical', command=app.doc_tree.yview)
    vsb.pack(side='right', fill='y')

    app.doc_tree.bind('<Delete>', app.delete_docs)

    app.doc_tree.configure(yscrollcommand=vsb.set)
    app.doc_tree.pack(expand=True, fill='both')


def pdf_to_text(app):
    """Import PDFs into the database."""
    paths = filedialog.askopenfilenames(
        initialdir=app.curr_dir, title='Import PDF Files', multiple=True,
        filetypes=(('pdf files', '*.pdf'), ('all files', '*.*')))
    if paths:
        app.curr_dir = dirname(paths[0])
        doc.import_files(app.cxn, paths, type_='pdf')
        repopulate(app)


def import_text(app):
    """Import PDFs into the database."""
    print('import_text')


def ocr_pdf(app):
    """Import PDFs into the database."""
    print('ocr_pdf')


def select_doc(app):
    """Select the doc and prepare to edit it."""
    selected = app.doc_tree.selection()
    if not selected:
        return
    app.doc_id = app.doc_tree.item(selected[0])['text']
    app.doc_sel.set(app.doc_id)
    doc_selected(app)
    app.notebook.select(2)


def delete_docs(app, _):
    """Delete selected docs."""
    selected = app.doc_tree.selection()
    if not selected:
        return
    doc_ids = [app.doc_tree.item(selected[s])['text']
               for s in range(len(selected))]
    doc.delete_docs(app.cxn, doc_ids)
    repopulate(app)
