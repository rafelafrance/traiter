#!/usr/bin/env python3

"""Run the GUI."""

from traiter.gui.app_window import build_app


def main():
    """"Do it."""
    app = build_app()
    app.win.mainloop()


if __name__ == '__main__':
    main()
