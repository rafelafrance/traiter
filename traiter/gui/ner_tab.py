"""NER tab for the main app."""

import tkinter.ttk as ttk


def build_ner_tab(app):
    """Build the named entity recognition tab."""
    tab = ttk.Frame(app.notebook)
    app.notebook.add(tab, text='Entity Recognition')

    tab_frame = ttk.Frame(tab)
    tab_frame.pack(expand=True, fill='both')
