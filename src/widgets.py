import urwid
import sequoia as sq

class MainWindow(urwid.Filler):

    def __init__(self):
        self.pile = urwid.Pile([])
        super().__init__(self.pile)

        self.sesh = sq.session("termina")
        self.outport = sq.outport("out")
        self.sesh.register_outport(self.outport)

        self.addSequence(16)
        self.playing = False

    def keypress(self, size, key):
        if key==' ':
            self.playing = not self.playing
            if self.playing:
                self.sesh.start()
            else:
                self.sesh.stop()
        elif key in ('n', 'N'):
            self.addSequence(16)
        elif key=='h':
            return super().keypress(size, 'left')
        elif key=='j':
            return super().keypress(size, 'down')
        elif key=='k':
            return super().keypress(size, 'up')
        elif key=='l':
            return super().keypress(size, 'right')
        else:
            return super().keypress(size, key)

    def addSequence(self, n):
        seq = sq.sequence(n)
        seq.set_outport(self.outport)
        self.sesh.add_sequence(seq)
        self.pile.contents.append((SequenceWidget(seq), ('pack', None)))

class SequenceWidget(urwid.Columns):

    def __init__(self, seq):
        self.seq = seq
        self.triggerWidgets = []
        for i in range(self.seq.get_nsteps()):
            self.triggerWidgets.append(TriggerWidget(i, self.seq))
        super().__init__(self.triggerWidgets)

    def keypress(self, size, key):
        return super().keypress(size, key)

class TriggerWidget(urwid.Edit):

    """
    Just using Edit for now because it's selectable (Text isn't)
    """

    def __init__(self, index, seq):
        super().__init__('_', align='center')
        self.set = False
        self.index = index
        self.seq = seq
        self.trig = sq.trigger()

    def keypress(self, size, key):
        if key in ('t', 'T'):
            self.set = not self.set
            if self.set:
                self.set_caption('X')
                self.trig.set_type(1)
            else:
                self.set_caption('_')
                self.trig.set_type(0)
            self.seq.set_trig(self.index, self.trig)
        else:
            return key  # don't call base method

