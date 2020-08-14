"""Prompt for script fields."""

import tkinter as tk
import tkinter.ttk as ttk


class AddScriptDialog:
    """Prompt for script fields."""

    def __init__(self, parent):
        win = self.win = tk.Toplevel(parent)

        win.configure(bg='#f6f4f2')

        # style = ThemedStyle(win)
        # style.set_theme('radiance')

        win.columnconfigure(1, weight=1)
        win.rowconfigure(0, weight=1)

        self.action = tk.StringVar(parent, '')
        self.script_id = tk.StringVar(parent, '')

        ttk.Label(win, text='Enter script action').grid(row=0, pady=16, padx=8)
        ttk.Label(win, text='Enter script name').grid(row=1, pady=16, padx=8)

        self.action_ent = ttk.Entry(win)
        self.action_ent.grid(row=0, column=1, pady=16, padx=8, sticky='EW')

        self.script_id_ent = ttk.Entry(win)
        self.script_id_ent.grid(row=1, column=1, pady=16, padx=8, sticky='EW')

        ttk.Button(win, text='OK', command=self.ok).grid(row=2, pady=16)
        ttk.Button(win, text='Cancel', command=self.cancel).grid(
            row=2, column=1, pady=16, padx=8, sticky='W')

    def ok(self):
        """Save the value and return."""
        self.action.set(self.action_ent.get())
        self.script_id.set(self.script_id_ent.get())
        self.win.destroy()

    def cancel(self):
        """Don't add the script."""
        self.action.set('')
        self.script_id.set('')
        self.win.destroy()
