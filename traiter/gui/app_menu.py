"""Main app menu."""

import tkinter as tk
from os.path import dirname
from shutil import copy
from tkinter import filedialog, messagebox

import traiter.pylib.db as db
from .app_util import MEMORY, repopulate


def build_app_menu(app):
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
