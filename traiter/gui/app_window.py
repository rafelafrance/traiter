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
from .add_script_dialog import AddScriptDialog

OK = 0
ERROR = 1
MEMORY = ':memory:'

signal(SIGPIPE, SIG_DFL)


# TODO Break this into smaller modules
class App:
    """Build the app."""

    def __init__(self):
        self.win = ThemedTk(theme='radiance')

        self.dirty = False
        self.path = MEMORY
        self.doc_id = ''

        self.cxn = db.connect(self.path)
        self.curr_dir = '.'

        self.docs = None
        self.doc_tree = None

        self.doc_sel = None
        self.edits = None
        self.edits_popup = None
        self.script_sel = None

        self.scripts = None
        self.script_tree = None

        db.create(self.cxn, self.path)

        self.win.title(self.get_title())
        self.win.geometry('1200x800')

        self.build_top_menu()

        self.notebook = ttk.Notebook(self.win)
        self.notebook.pack(expand=True, fill="both")
        self.build_import_tab()
        self.build_scripts_tab()
        self.build_transform_tab()
        self.build_ner_tab()
        self.build_nel_tab()

        self.repopulate()

    def build_ner_tab(self):
        """Build the named entity recognition tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Entity Recognition')

        tab_frame = ttk.Frame(tab)
        tab_frame.pack(expand=True, fill='both')

    def build_nel_tab(self):
        """Build the named entity recognition tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Entity Linking')

        tab_frame = ttk.Frame(tab)
        tab_frame.pack(expand=True, fill='both')

    def build_top_menu(self):
        """Build the menu."""
        menu = tk.Menu(self.win)
        sub_menu = tk.Menu(menu, tearoff=False)
        sub_menu.add_command(label='Open', underline=0, command=self.open_db)
        sub_menu.add_command(label='New', underline=0, command=self.new_db)
        sub_menu.add_command(
            label='Save...', underline=0,
            command=self.save_as_db,
            state=tk.DISABLED)
        sub_menu.add_command(
            label='Save as...', underline=5, command=self.save_as_db)
        sub_menu.add_separator()
        sub_menu.add_command(label='Quit', underline=0, command=self.safe_quit)
        menu.add_cascade(label='File', underline=0, menu=sub_menu)
        self.win.config(menu=menu)

    def build_import_tab(self):
        """Build the import tab controls."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Import')

        tab_frame = ttk.Frame(tab)
        tab_frame.pack(expand=True, fill='both')

        sub_frame = ttk.Frame(tab_frame)
        sub_frame.pack(expand=False, fill='x', pady=(24, 24))

        button = ttk.Button(
            sub_frame, text='PDF to Text...', command=self.pdf_to_text)
        button.pack(side=tk.LEFT, padx=(8, 8))

        button = ttk.Button(
            sub_frame, text='Import Text...', command=self.import_text)
        button.pack(side=tk.LEFT, padx=(8, 8))

        button = ttk.Button(
            sub_frame, text='OCR PDF...', state=tk.DISABLED,
            command=self.ocr_pdf)
        button.pack(side=tk.LEFT, padx=(8, 8))

        sub_frame = ttk.Frame(tab_frame)
        sub_frame.pack(expand=True, fill='both')

        self.docs = doc.select_docs(self.cxn)
        self.docs.set_index('doc_id', inplace=True)

        self.doc_tree = ttk.Treeview(sub_frame)
        self.doc_tree.bind('<Double-Button-1>', self.select_doc)
        self.doc_tree['columns'] = list(self.docs.columns)
        self.doc_tree.column('#0', stretch=True)
        self.doc_tree.heading('#0', text='document')
        for col in self.docs.columns:
            self.doc_tree.column(col, stretch=True)
            self.doc_tree.heading(col, text=col)

        vsb = ttk.Scrollbar(
            sub_frame, orient='vertical', command=self.doc_tree.yview)
        vsb.pack(side='right', fill='y')

        self.doc_tree.bind('<Delete>', self.delete_docs)

        self.doc_tree.configure(yscrollcommand=vsb.set)
        self.doc_tree.pack(expand=True, fill='both')

    def build_transform_tab(self):
        """Build the transform tab controls."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Transform')

        tab_frame = ttk.Frame(tab)
        tab_frame.pack(expand=True, fill='both')

        sub_frame = ttk.Frame(tab_frame)
        sub_frame.pack(expand=False, fill='x', pady=(24, 24))

        self.doc_sel = ttk.Combobox(sub_frame)
        self.doc_sel.pack(side=tk.LEFT, padx=(8, 8))
        self.doc_sel.bind('<<ComboboxSelected>>', self.doc_selected)

        sub_frame = ttk.Frame(tab_frame)
        sub_frame.pack(expand=True, fill='both')

        self.edits = ScrolledText(sub_frame)
        self.edits.pack(fill="both", expand=True)
        self.edits.insert(tk.INSERT, '')

        self.edits_popup = tk.Menu(self.edits, tearoff=False)
        self.edits_popup.add_command(label='Test', command=self.test_edits)
        self.edits.bind('<Button-3>', self.open_edits_menu)

        sub_frame = ttk.Frame(tab_frame)
        sub_frame.pack(expand=False, fill='x', pady=(24, 24))

        self.script_sel = ttk.Combobox(sub_frame)
        self.script_sel.pack(side=tk.LEFT, padx=(8, 0))

        button = ttk.Button(
            sub_frame, text='+', command=self.add_script, width=1)
        button.pack(side=tk.LEFT, padx=(0, 8))

        button = ttk.Button(
            sub_frame, text='Run Script', command=self.run_script)
        button.pack(side=tk.LEFT, padx=(8, 8))

        button = ttk.Button(
            sub_frame, text='Reset', command=self.reset_edits)
        button.pack(side=tk.RIGHT, padx=(8, 8))

        button = ttk.Button(
            sub_frame, text='Cancel', command=self.cancel_edits)
        button.pack(side=tk.RIGHT, padx=(8, 8))

        button = ttk.Button(
            sub_frame, text='Save', command=self.save_edits)
        button.pack(side=tk.RIGHT, padx=(8, 8))

        button = ttk.Button(
            sub_frame, text='\u21BB', command=self.undo_edits, width=2)
        button.pack(side=tk.RIGHT, padx=(4, 32))

        button = ttk.Button(
            sub_frame, text='\u21BA', command=self.redo_edits, width=2)
        button.pack(side=tk.RIGHT, padx=(32, 4))

    def build_scripts_tab(self):
        """Build the pipes tab controls."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Scripts')

        tab_frame = ttk.Frame(tab)
        tab_frame.pack(expand=True, fill='both')

        sub_frame = ttk.Frame(tab_frame)
        sub_frame.pack(expand=True, fill='both')

        self.scripts = script_lib.select_scripts(self.cxn)
        self.scripts.set_index('script_id', inplace=True)

        self.script_tree = ttk.Treeview(sub_frame)
        # self.script_tree.bind('<Double-Button-1>', self.select_script)
        self.script_tree['columns'] = list(self.scripts.columns)
        self.script_tree.column('#0', stretch=True)
        self.script_tree.heading('#0', text='')
        for col in self.scripts.columns:
            self.script_tree.column(col, stretch=True)
            self.script_tree.heading(col, text=col)

        vsb = ttk.Scrollbar(
            sub_frame, orient='vertical', command=self.script_tree.yview)
        vsb.pack(side='right', fill='y')

        self.script_tree.configure(yscrollcommand=vsb.set)
        self.script_tree.pack(expand=True, fill='both')

        sub_frame = ttk.Frame(tab_frame)
        sub_frame.pack(expand=False, fill='x', pady=(24, 24))

        button = ttk.Button(sub_frame, text='Add', command=self.add_script)
        button.pack(side=tk.RIGHT, padx=(8, 8))

    def open_db(self):
        """Open a database and fill the fields with its data."""
        path = filedialog.askopenfile(
            initialdir=self.curr_dir, title='Open a Traiter Database',
            filetypes=(('db files', '*.db'), ('all files', '*.*')))
        if not path:
            return
        self.curr_dir = dirname(path.name)
        self.path = path.name
        self.cxn = db.connect(self.path)
        self.repopulate()

    def new_db(self):
        """Open a database and fill the fields with its data."""
        path = filedialog.asksaveasfilename(
            initialdir=self.curr_dir, title='Create a New Traiter Database',
            filetypes=(('db files', '*.db'), ('all files', '*.*')))
        if not path:
            return
        self.curr_dir = dirname(path)
        self.path = path
        self.cxn = db.create(self.cxn, path)
        self.repopulate()

    def save_as_db(self):
        """Open a database and fill the fields with its data."""
        path = filedialog.asksaveasfilename(
            initialdir=self.curr_dir, title='Save the Database',
            filetypes=(('db files', '*.db'), ('all files', '*.*')))
        if not path:
            return
        copy(self.path, path)
        self.curr_dir = dirname(path)
        self.path = path
        self.cxn = db.connect(path)
        self.repopulate()

    def safe_quit(self):
        """Prompt to save changes before quitting."""
        if self.path == MEMORY and self.dirty:
            yes = messagebox.askyesno(
                self.get_title(),
                'Are you sure you want to exit before saving?')
            if not yes:
                return
        self.win.quit()

    def pdf_to_text(self):
        """Import PDFs into the database."""
        paths = filedialog.askopenfilenames(
            initialdir=self.curr_dir, title='Import PDF Files', multiple=True,
            filetypes=(('pdf files', '*.pdf'), ('all files', '*.*')))
        if paths:
            self.dirty = True
            self.curr_dir = dirname(paths[0])
            doc.import_files(self.cxn, paths, type_='pdf')
            self.repopulate()

    def import_text(self):
        """Import PDFs into the database."""
        self.dirty = True
        print('import_text')

    def ocr_pdf(self):
        """Import PDFs into the database."""
        self.dirty = True
        print('ocr_pdf')

    def repopulate(self):
        """Repopulate the controls from new data."""
        self.win.title(self.get_title())
        self.docs = doc.select_docs(self.cxn)
        self.docs.set_index('doc_id', inplace=True)

        self.doc_tree.delete(*self.doc_tree.get_children())
        for doc_id, row in self.docs.iterrows():
            self.doc_tree.insert('', tk.END, text=doc_id, values=list(row))

        self.doc_tree.column('#0', stretch=True)
        self.doc_tree.heading('#0', text='document')
        for col in self.docs.columns:
            self.doc_tree.column(col, stretch=True)
            self.doc_tree.heading(col, text=col)

        doc_ids = self.docs.index.tolist()
        if doc_ids:
            self.doc_sel['values'] = [''] + doc_ids
            self.doc_sel['width'] = max(len(i) for i in doc_ids)
            self.doc_sel.current(0)
        else:
            self.doc_sel['values'] = ['']

        self.scripts = script_lib.select_scripts(self.cxn)
        self.scripts.set_index('script_id', inplace=True)
        self.script_tree.delete(*self.script_tree.get_children())
        for script_id, row in self.scripts.iterrows():
            self.script_tree.insert(
                '', tk.END, text=script_id, values=list(row))

        self.script_tree.column('#0', stretch=True)
        self.script_tree.heading('#0', text='name')
        for col in self.scripts.columns:
            self.script_tree.column(col, stretch=True)
            self.script_tree.heading(col, text=col)

        script_ids = self.scripts.index.tolist()
        if script_ids:
            self.script_sel['values'] = [''] + script_ids
            self.script_sel['width'] = max(len(i) for i in script_ids)
            self.script_sel.current(0)
        else:
            self.script_sel['values'] = ['']

    def select_doc(self, _):
        """Select the doc and prepare to edit it."""
        selected = self.doc_tree.selection()
        if not selected:
            return
        self.doc_id = self.doc_tree.item(selected[0])['text']
        self.doc_sel.set(self.doc_id)
        self.doc_selected()
        self.notebook.select(2)

    def doc_selected(self, _=None):
        """Update the doc edit text box when selected."""
        self.doc_id = self.doc_sel.get()
        text = doc.select_doc_edits(self.cxn, self.doc_id)
        self.edits.delete('1.0', tk.END)
        self.edits.insert(tk.INSERT, text)

    def delete_docs(self, _):
        """Delete selected docs."""
        selected = self.doc_tree.selection()
        if not selected:
            return
        doc_ids = [self.doc_tree.item(selected[s])['text']
                   for s in range(len(selected))]
        doc.delete_docs(self.cxn, doc_ids)
        self.repopulate()

    def open_edits_menu(self, event):
        """Open the edit popup menu."""
        try:
            self.edits_popup.tk_popup(event.x_root, event.y_root)
        finally:
            self.edits_popup.grab_release()

    def test_edits(self):
        """Test popup menu selection."""
        print('test_edits')

    def add_script(self):
        """Add a pipe to the select list."""
        dialog = AddScriptDialog(self.win)
        self.win.wait_window(dialog.win)
        script_id = dialog.script_id.get()
        action = dialog.action.get()
        if not action:
            return
        self.dirty = True
        script_id = script_id if script_id else action
        script_lib.add_script(self.cxn, script_id, action)
        self.repopulate()

    def run_script(self):
        """Run the pipe on the text."""
        self.dirty = True
        script = self.script_sel.get()
        script = self.scripts.at[script, 'action']
        pipe = pipes.Template()
        pipe.append(script, '--')
        with tempfile.NamedTemporaryFile('r') as temp_file:
            with pipe.open(temp_file.name, 'w') as stream:
                try:
                    text = self.edits.get('1.0', tk.END)
                    stream.write(text)
                except Exception as err:
                    print(err)
                temp_file.seek(0)
            text = temp_file.read()
        self.edits.delete('1.0', tk.END)
        self.edits.insert(tk.INSERT, text)

    def undo_edits(self):
        """Undo the last edit for the current doc."""

    def redo_edits(self):
        """Redo the last edit for the current doc."""

    def save_edits(self):
        """Save edits to the database."""
        text = self.edits.get('1.0', tk.END)
        doc.update_doc(self.cxn, self.doc_id, text)

    def cancel_edits(self):
        """Cancel edits back to the last saved point."""
        text = doc.select_doc_edits(self.cxn, self.doc_id)
        self.edits.delete('1.0', tk.END)
        self.edits.insert(tk.INSERT, text)

    def reset_edits(self):
        """Reset edits back to the original data."""
        text = doc.select_doc_raw(self.cxn, self.doc_id)
        self.edits.delete('1.0', tk.END)
        self.edits.insert(tk.INSERT, text)

    def get_title(self):
        """Build the window title."""
        title = splitext(basename(self.path))[0]
        return f'Traiter ({title})'
