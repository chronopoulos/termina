import urwid
import sequoia as sq

class MainWindow(urwid.Filler):

    def __init__(self):
        self.pile = urwid.Pile([])
        super().__init__(self.pile)

        self.sesh = sq.session("termina")
        self.outport = sq.outport("out")
        self.sesh.register_outport(self.outport)

        self.seqWidgets = []

        self.addSequence(16)
        self.playing = False
        self.stopNoti = False

        self.sesh.set_bpm(90)

    def setLoop(self, loop):
        self.loop = loop

    def keypress(self, size, key):
        if key==' ':
            if self.playing:
                self.stop()
            else:
                self.start()
        elif key in ('n', 'N'):
            self.addSequence(16)
        else:
            return super().keypress(size, key)

    def checkNotifications(self, loop, data):
        for seqWidget in self.seqWidgets:
            seqWidget.checkNotifications()
        if self.stopNoti:
            self.stopNoti = False
            return
        self.loop.set_alarm_in(0.1, self.checkNotifications)

    def start(self):
        self.sesh.start()
        self.loop.set_alarm_in(0, self.checkNotifications)
        self.playing = True

    def stop(self):
        self.sesh.stop()
        self.stopNoti = True
        self.playing = False

    def addSequence(self, n):
        seq = sq.sequence(n)
        seq.set_outport(self.outport)
        self.sesh.add_sequence(seq)
        seqWidget = SequenceWidget(seq)
        self.pile.contents.append((seqWidget, ('pack', None)))
        self.seqWidgets.append(seqWidget)

class SequenceWidget(urwid.Columns):

    def __init__(self, seq):
        self.seq = seq
        self.seq.set_notifications(True)
        self.triggerWidgets = []
        for i in range(self.seq.get_nsteps()):
            self.triggerWidgets.append(TriggerWidget(i, self.seq))
        super().__init__(self.triggerWidgets)

        self.current = self.triggerWidgets[0]

    def keypress(self, size, key):
        return super().keypress(size, key)

    def checkNotifications(self):
        new, ph = self.seq.read_new_playhead()
        if new:
            self.current.setPlayhead(False)
            self.current = self.triggerWidgets[ph]
            self.current.setPlayhead(True)

class TriggerWidget(urwid.Edit):

    """
    Just using Edit for now because it's selectable (Text isn't)
    """

    def __init__(self, index, seq):
        super().__init__('__', align='center')
        self.set = False
        self.index = index
        self.seq = seq
        self.trig = sq.trigger()

    def keypress(self, size, key):
        if key in ('t', 'T'):
            self.trig.type = 0 if self.trig.type else 1 # toggle
            self.seq.set_trig(self.index, self.trig)
            self.show()
        elif key=='J':
            self.trig.note_value -= 1
            self.seq.set_trig(self.index, self.trig)
            self.show()
        elif key=='K':
            self.trig.note_value += 1
            self.seq.set_trig(self.index, self.trig)
            self.show()
        elif key=='h':
            return super().keypress(size, 'left')
        elif key=='j':
            return super().keypress(size, 'down')
        elif key=='k':
            return super().keypress(size, 'up')
        elif key=='l':
            return super().keypress(size, 'right')
        else:
            return key  # don't call base method

    def show(self):
        if self.trig.type==1:
            self.set_caption(str(self.trig.note_value))
        else:
            self.set_caption('__')
            
    def setPlayhead(self, enable):
        if enable:
            self.set_caption('**')
        else:
            self.show()

