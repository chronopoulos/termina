#!/usr/bin/env python3

import urwid

from widgets import *

def defaultHandler(key):
    global PLAYING
    if key==' ':
        PLAYING = not PLAYING
        if PLAYING:
            SESH.start()
        else:
            SESH.stop()
    elif key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    else:
        # undhandled
        return key

if __name__ == "__main__":
    top = MainWindow()
    loop = urwid.MainLoop(top, unhandled_input=defaultHandler)
    loop.run()

