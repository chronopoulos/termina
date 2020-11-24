#!/usr/bin/env python3

import urwid
import sys

from widgets import *
from dialogs import *

def defaultHandler(key):
    if key == 'q':
        raise urwid.ExitMainLoop()
    else:
        # unhandled
        return key

if __name__ == "__main__":
    if len(sys.argv) > 1:
        #top = MainWindow(sys.argv[1])
        print('TODO file loading')
        sys.exit(0)
    else:
        top = MainWindow()
    loop = urwid.MainLoop(top, handle_mouse=False, unhandled_input=defaultHandler, pop_ups=True)
    top.setLoop(loop)
    loop.run()

