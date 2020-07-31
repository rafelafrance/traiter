#!/usr/bin/env python3

"""Run the GUI."""

from traiter.gui.app_window import App


def main():
    """"Do it."""
    app = App()
    app.win.mainloop()


if __name__ == '__main__':
    main()
