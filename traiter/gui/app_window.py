"""Run the GUI."""

import pipes
import tempfile
import tkinter as tk
import tkinter.ttk as ttk
from os.path import basename, dirname, splitext
from shutil import copy
from signal import SIGPIPE, SIG_DFL, signal
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

from ttkthemes import ThemedTk

import traiter.pylib.db as db
import traiter.pylib.doc as doc
import traiter.pylib.script as script_lib
from traiter.pylib.util import DotDict
from .add_script_dialog import AddScriptDialog

MEMORY = ':memory:'

signal(SIGPIPE, SIG_DFL)


def build_app():
    """Build the app window."""
    app = DotDict()

    app.win = ThemedTk(theme='radiance')

    app.path = MEMORY
    app.doc_id = ''

    app.cxn = db.connect(app.path)
    app.curr_dir = '.'

    app.docs = None
    app.doc_tree = None

    app.doc_sel = None
    app.edits = None
    app.edits_popup = None
    app.script_sel = None

    app.scripts = None
    app.script_tree = None

    db.create(app.cxn, app.path)

    app.win.title(get_title(app))
    app.win.geometry('1200x800')

    build_top_menu(app)

    app.notebook = ttk.Notebook(app.win)
    app.notebook.pack(expand=True, fill='both')
    build_import_tab(app)
    build_scripts_tab(app)
    build_transform_tab(app)
    build_ner_tab(app)
    build_nel_tab(app)

    repopulate(app)

    return app


def build_ner_tab(app):
    """Build the named entity recognition tab."""
    tab = ttk.Frame(app.notebook)
    app.notebook.add(tab, text='Entity Recognition')

    tab_frame = ttk.Frame(tab)
    tab_frame.pack(expand=True, fill='both')


def build_nel_tab(app):
    """Build the named entity recognition tab."""
    tab = ttk.Frame(app.notebook)
    app.notebook.add(tab, text='Entity Linking')

    tab_frame = ttk.Frame(tab)
    tab_frame.pack(expand=True, fill='both')


def build_top_menu(app):
    """Build the menu."""
    menu = tk.Menu(app.win)
    sub_menu = tk.Menu(menu, tearoff=False)
    sub_menu.add_command(
        label='Open', underline=0, command=lambda: open_db(app))
    sub_menu.add_command(
        label='New', underline=0, command=lambda: new_db(app))
    sub_menu.add_command(
        label='Save...', underline=0, state=tk.DISABLED,
        command=lambda: save_as_db(app))
    sub_menu.add_command(
        label='Save as...', underline=5,
        command=lambda: save_as_db(app))
    sub_menu.add_separator()
    sub_menu.add_command(
        label='Quit', underline=0, command=lambda: safe_quit(app))
    menu.add_cascade(label='File', underline=0, menu=sub_menu)
    app.win.config(menu=menu)


def build_import_tab(app):
    """Build the import tab controls."""
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


def build_transform_tab(app):
    """Build the transform tab controls."""
    tab = ttk.Frame(app.notebook)
    app.notebook.add(tab, text='Transform')

    tab_frame = ttk.Frame(tab)
    tab_frame.pack(expand=True, fill='both')

    sub_frame = ttk.Frame(tab_frame)
    sub_frame.pack(expand=False, fill='x', pady=(24, 24))

    app.doc_sel = ttk.Combobox(sub_frame)
    app.doc_sel.pack(side=tk.LEFT, padx=(8, 8))
    app.doc_sel.bind('<<ComboboxSelected>>', doc_selected)

    sub_frame = ttk.Frame(tab_frame)
    sub_frame.pack(expand=True, fill='both')

    app.edits = ScrolledText(sub_frame)
    app.edits.pack(fill='both', expand=True)
    app.edits.insert(tk.INSERT, '')

    app.edits_popup = tk.Menu(app.edits, tearoff=False)
    app.edits_popup.add_command(label='Test', command=lambda: test_edits(app))
    app.edits.bind('<Button-3>', open_edits_menu)

    sub_frame = ttk.Frame(tab_frame)
    sub_frame.pack(expand=False, fill='x', pady=(24, 24))

    app.script_sel = ttk.Combobox(sub_frame)
    app.script_sel.pack(side=tk.LEFT, padx=(8, 0))

    button = ttk.Button(
        sub_frame, text='+', width=1, command=lambda: add_script(app))
    button.pack(side=tk.LEFT, padx=(0, 8))

    button = ttk.Button(
        sub_frame, text='Run Script', command=lambda: run_script(app))
    button.pack(side=tk.LEFT, padx=(8, 8))

    button = ttk.Button(
        sub_frame, text='Reset', command=lambda: reset_edits(app))
    button.pack(side=tk.RIGHT, padx=(8, 8))

    button = ttk.Button(
        sub_frame, text='Cancel', command=lambda: cancel_edits(app))
    button.pack(side=tk.RIGHT, padx=(8, 8))

    button = ttk.Button(
        sub_frame, text='Save', command=lambda: save_edits(app))
    button.pack(side=tk.RIGHT, padx=(8, 8))

    button = ttk.Button(
        sub_frame, text='\u21BB', command=undo_edits, width=2)
    button.pack(side=tk.RIGHT, padx=(4, 32))

    button = ttk.Button(
        sub_frame, text='\u21BA', command=redo_edits, width=2)
    button.pack(side=tk.RIGHT, padx=(32, 4))


def build_scripts_tab(app):
    """Build the pipes tab controls."""
    tab = ttk.Frame(app.notebook)
    app.notebook.add(tab, text='Scripts')

    tab_frame = ttk.Frame(tab)
    tab_frame.pack(expand=True, fill='both')

    sub_frame = ttk.Frame(tab_frame)
    sub_frame.pack(expand=True, fill='both')

    app.scripts = script_lib.select_scripts(app.cxn)
    app.scripts.set_index('script_id', inplace=True)

    app.script_tree = ttk.Treeview(sub_frame)
    # app.script_tree.bind('<Double-Button-1>', app.select_script)
    app.script_tree['columns'] = list(app.scripts.columns)
    app.script_tree.column('#0', stretch=True)
    app.script_tree.heading('#0', text='')
    for col in app.scripts.columns:
        app.script_tree.column(col, stretch=True)
        app.script_tree.heading(col, text=col)

    vsb = ttk.Scrollbar(
        sub_frame, orient='vertical', command=app.script_tree.yview)
    vsb.pack(side='right', fill='y')

    app.script_tree.configure(yscrollcommand=vsb.set)
    app.script_tree.pack(expand=True, fill='both')

    sub_frame = ttk.Frame(tab_frame)
    sub_frame.pack(expand=False, fill='x', pady=(24, 24))

    button = ttk.Button(sub_frame, text='Add', command=lambda: add_script(app))
    button.pack(side=tk.RIGHT, padx=(8, 8))


def open_db(app):
    """Open a database and fill the fields with its data."""
    path = filedialog.askopenfile(
        initialdir=app.curr_dir, title='Open a Traiter Database',
        filetypes=(('db files', '*.db'), ('all files', '*.*')))
    if not path:
        return
    app.curr_dir = dirname(path.name)
    app.path = path.name
    app.cxn = db.connect(app.path)
    repopulate(app)


def new_db(app):
    """Open a database and fill the fields with its data."""
    path = filedialog.asksaveasfilename(
        initialdir=app.curr_dir, title='Create a New Traiter Database',
        filetypes=(('db files', '*.db'), ('all files', '*.*')))
    if not path:
        return
    app.curr_dir = dirname(path)
    app.path = path
    app.cxn = db.create(app.cxn, path)
    repopulate(app)


def save_as_db(app):
    """Open a database and fill the fields with its data."""
    path = filedialog.asksaveasfilename(
        initialdir=app.curr_dir, title='Save the Database',
        filetypes=(('db files', '*.db'), ('all files', '*.*')))
    if not path:
        return
    copy(app.path, path)
    app.curr_dir = dirname(path)
    app.path = path
    app.cxn = db.connect(path)
    repopulate(app)


def safe_quit(app):
    """Prompt to save changes before quitting."""
    if app.path == MEMORY:
        yes = messagebox.askyesno(
            app.get_title(),
            'Are you sure you want to exit before saving?')
        if not yes:
            return
    app.win.quit()


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


def select_doc(app):
    """Select the doc and prepare to edit it."""
    selected = app.doc_tree.selection()
    if not selected:
        return
    app.doc_id = app.doc_tree.item(selected[0])['text']
    app.doc_sel.set(app.doc_id)
    doc_selected(app)
    app.notebook.select(2)


def doc_selected(app, _=None):
    """Update the doc edit text box when selected."""
    app.doc_id = app.doc_sel.get()
    text = doc.select_doc_edits(app.cxn, app.doc_id)
    app.edits.delete('1.0', tk.END)
    app.edits.insert(tk.INSERT, text)


def delete_docs(app, _):
    """Delete selected docs."""
    selected = app.doc_tree.selection()
    if not selected:
        return
    doc_ids = [app.doc_tree.item(selected[s])['text']
               for s in range(len(selected))]
    doc.delete_docs(app.cxn, doc_ids)
    repopulate(app)


def open_edits_menu(app, event):
    """Open the edit popup menu."""
    try:
        app.edits_popup.tk_popup(event.x_root, event.y_root)
    finally:
        app.edits_popup.grab_release()


def test_edits(app):
    """Test popup menu selection."""
    print(app.cxn)
    print('test_edits')


def add_script(app):
    """Add a pipe to the select list."""
    dialog = AddScriptDialog(app.win)
    app.win.wait_window(dialog.win)
    script_id = dialog.script_id.get()
    action = dialog.action.get()
    if not action:
        return
    script_id = script_id if script_id else action
    script_lib.add_script(app.cxn, script_id, action)
    repopulate(app)


def run_script(app):
    """Run the pipe on the text."""
    script = app.script_sel.get()
    script = app.scripts.at[script, 'action']
    pipe = pipes.Template()
    pipe.append(script, '--')
    with tempfile.NamedTemporaryFile('r') as temp_file:
        with pipe.open(temp_file.name, 'w') as stream:
            try:
                text = app.edits.get('1.0', tk.END)
                stream.write(text)
            except Exception as err:
                print(err)
            temp_file.seek(0)
        text = temp_file.read()
    app.edits.delete('1.0', tk.END)
    app.edits.insert(tk.INSERT, text)


def undo_edits(app):
    """Undo the last edit for the current doc."""


def redo_edits(app):
    """Redo the last edit for the current doc."""


def save_edits(app):
    """Save edits to the database."""
    text = app.edits.get('1.0', tk.END)
    doc.update_doc(app.cxn, app.doc_id, text)


def cancel_edits(app):
    """Cancel edits back to the last saved point."""
    text = doc.select_doc_edits(app.cxn, app.doc_id)
    app.edits.delete('1.0', tk.END)
    app.edits.insert(tk.INSERT, text)


def reset_edits(app):
    """Reset edits back to the original data."""
    text = doc.select_doc_raw(app.cxn, app.doc_id)
    app.edits.delete('1.0', tk.END)
    app.edits.insert(tk.INSERT, text)


def get_title(app):
    """Build the window title."""
    title = splitext(basename(app.path))[0]
    return f'Traiter ({title})'
