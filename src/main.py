#!/usr/bin/python2

import urwid

txt = urwid.Text("hello world", align='center')
top = urwid.Filler(txt)
loop = urwid.MainLoop(top)
loop.run()
