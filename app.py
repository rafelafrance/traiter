#!/usr/bin/env python3

"""Run the GUI."""

import tkinter.ttk as ttk
from signal import SIGPIPE, SIG_DFL, signal

from ttkthemes import ThemedTk

import traiter.pylib.db as db
from traiter.gui.app_menu import build_app_menu
from traiter.gui.app_util import MEMORY, get_title, repopulate
from traiter.gui.import_tab import build_import_tab
from traiter.gui.nel_tab import build_nel_tab
from traiter.gui.ner_tab import build_ner_tab
from traiter.gui.scripts_tab import build_scripts_tab
from traiter.gui.transform_tab import build_transform_tab
from traiter.pylib.util import DotDict

signal(SIGPIPE, SIG_DFL)


def build_app():
    """Build the app window."""
    app = DotDict()

    app.win = ThemedTk(theme='radiance')

    app.path = MEMORY
    app.doc_id = ''

    app.cxn = db.connect(app.path)
    app.curr_dir = '.'

    app.doc_sel = None
    app.edits = None
    app.edits_popup = None
    app.script_sel = None

    db.create(app.cxn, app.path)

    app.win.title(get_title(app))
    app.win.geometry('1200x800')

    build_app_menu(app)

    app.notebook = ttk.Notebook(app.win)
    app.notebook.pack(expand=True, fill='both')
    build_import_tab(app)
    build_scripts_tab(app)
    build_transform_tab(app)
    build_ner_tab(app)
    build_nel_tab(app)

    repopulate(app)

    return app


if __name__ == '__main__':
    APP = build_app()
    APP.win.mainloop()
