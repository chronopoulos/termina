import urwid

class TestMenu(urwid.ListBox):

    def __init__(self):
        body = [urwid.Text("MyTitle"), urwid.Divider()]
        body.append(urwid.Button("Button1"))
        body.append(urwid.Button("Button2"))
        body.append(urwid.Button("Button3"))
        super().__init__(body)

class FillPop(urwid.LineBox):

    signals = ['close']

    def __init__(self):
        text = urwid.Text('Auto Fill', align='center')
        div = urwid.Divider()
        self.note_edit = urwid.IntEdit("Note Value: ", 60)
        self.freq_edit = urwid.IntEdit("Every: ", 4)
        pile = urwid.Pile([text, div, self.note_edit, self.freq_edit])
        fill = urwid.Filler(pile)
        self.__super.__init__(urwid.AttrWrap(fill, 'popbg'))

    def keypress(self, size, key):
        if key == 'enter':
            self._emit("close")
        else:
            return super().keypress(size, key)

    def result(self):
        note = self.note_edit.value()
        freq = self.freq_edit.value()
        return note, freq

