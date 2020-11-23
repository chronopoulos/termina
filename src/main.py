#!/usr/bin/env python3

import urwid

from widgets import *

def defaultHandler(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    else:
        # undhandled
        return key

if __name__ == "__main__":
    top = MainWindow()
    loop = urwid.MainLoop(top, handle_mouse=False, unhandled_input=defaultHandler)
    top.setLoop(loop)
    loop.run()

