"""Prompt for script fields."""

import tkinter as tk
import tkinter.ttk as ttk

from ttkthemes import ThemedStyle


class AddScriptDialog:
    """Prompt for script fields."""

    def __init__(self, parent):
        win = self.win = tk.Toplevel(parent)

        style = ThemedStyle(win)
        style.set_theme('radiance')

        self.script = ''
        self.script_id = ''

        ttk.Label(win, text="Enter script action").grid(row=0, pady=16, padx=8)
        ttk.Label(win, text="Enter script name").grid(row=1, pady=16, padx=8)

        self.script_ent = ttk.Entry(win)
        self.script_ent.grid(row=0, column=1, pady=16, padx=8)

        self.script_id_ent = ttk.Entry(win)
        self.script_id_ent.grid(row=1, column=1, pady=16, padx=8)

        ttk.Button(win, text="OK", command=self.ok).grid(row=2, pady=16)

    def ok(self):
        """Save the value and return."""
        self.script = self.script_ent.get()
        self.script_id = self.script_id_ent.get()
        print(self.script, self.script_id)
        self.win.destroy()
