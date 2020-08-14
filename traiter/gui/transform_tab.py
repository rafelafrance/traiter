"""Transform tab for the main app."""

import pipes
import tempfile
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText

import traiter.pylib.doc as doc
from .app_util import doc_selected
from .scripts_tab import add_script


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
        sub_frame, text='\u21BB', width=2, command=lambda: undo_edits(app))
    button.pack(side=tk.RIGHT, padx=(4, 32))

    button = ttk.Button(
        sub_frame, text='\u21BA', width=2, command=lambda: redo_edits(app))
    button.pack(side=tk.RIGHT, padx=(32, 4))


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
