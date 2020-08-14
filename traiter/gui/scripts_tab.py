"""Scripts tab for the main app."""

import tkinter as tk
import tkinter.ttk as ttk

import traiter.pylib.script as script_lib
from .add_script_dialog import AddScriptDialog
from .app_util import repopulate


def build_scripts_tab(app):
    """Build the pipes tab controls."""
    app.scripts = None
    app.script_tree = None

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
