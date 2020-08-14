"""NEL tab for the main app."""

import tkinter.ttk as ttk


def build_nel_tab(app):
    """Build the named entity recognition tab."""
    tab = ttk.Frame(app.notebook)
    app.notebook.add(tab, text='Entity Linking')

    tab_frame = ttk.Frame(tab)
    tab_frame.pack(expand=True, fill='both')
