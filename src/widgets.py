import urwid
import sequoia as sq
from random import randint

from dialogs import *

class MainWindow(urwid.Filler):

    def __init__(self, loadfile=''):
        self.pile = urwid.Pile([])
        super().__init__(self.pile)

        self.seqWidgets = []

        if loadfile:
            self.sesh = sq.load(loadfile)
        else:
            self.sesh = sq.session("termina")
            self.outport = sq.outport("out")
            self.sesh.register_outport(self.outport)
            self.addSequence(16)

        self.playing = False
        self.stopNoti = False

    def setLoop(self, loop):
        self.loop = loop

    def keypress(self, size, key):
        if key==' ':
            if self.playing:
                self.stop()
            else:
                self.start()
        elif key == 'n':
            self.addSequence(16)
        elif key == 's':
            self.sesh.save('termina.sqa')
        else:
            return super().keypress(size, key)

    def checkNotifications(self, loop, data):
        if self.stopNoti:
            self.stopNoti = False
            return
        for seqWidget in self.seqWidgets:
            seqWidget.checkNotifications()
        self.loop.set_alarm_in(0.1, self.checkNotifications)

    def start(self):
        self.sesh.start()
        self.loop.set_alarm_in(0, self.checkNotifications)
        self.playing = True

    def stop(self):
        self.sesh.stop()
        self.stopNoti = True
        self.playing = False
        for sw in self.seqWidgets:
            sw.stop()

    def addSequence(self, n):
        seq = sq.sequence(n)
        seq.set_outport(self.outport)
        self.sesh.add_sequence(seq)
        seqWidget = SequenceWidget(seq)
        self.pile.contents.append((seqWidget, ('pack', None)))
        self.seqWidgets.append(seqWidget)


class SequenceWidget(urwid.PopUpLauncher):

    def __init__(self, seq):
        self.seq = seq
        self.seq.set_notifications(True)

        self.triggerWidgets = []
        for i in range(self.seq.nsteps):
            self.triggerWidgets.append(TriggerWidget(i, self.seq))

        self.current = self.triggerWidgets[0]
        self.columns = urwid.Columns(self.triggerWidgets)
        self.linebox = urwid.LineBox(self.columns)
        super().__init__(self.linebox)

    def create_pop_up(self):
        self.fillPop = FillPop()
        urwid.connect_signal(self.fillPop, 'close', lambda w: self.handleFill())
        return self.fillPop

    def handleFill(self, *args):
        self.close_pop_up()
        note, freq = self.fillPop.result()
        for i, tw in enumerate(self.triggerWidgets):
            tw.setNote(i%freq == 0, note)

    def get_pop_up_parameters(self):
        return {'left':80, 'top':1, 'overlay_width':32, 'overlay_height':7}

    def keypress(self, size, key):
        if key == 'f':   # fill
            self.open_pop_up()
        else:
            return super().keypress(size, key)

    def checkNotifications(self):
        new, ph = self.seq.read_new_playhead()
        if new:
            self.current.setPlayhead(False)
            self.current = self.triggerWidgets[ph]
            self.current.setPlayhead(True)

    def stop(self):
        self.current.show()


class TriggerWidget(urwid.Edit):

    """
    Just using Edit for now because it's selectable (Text isn't)
    """

    def __init__(self, index, seq):
        super().__init__('__', align='center')
        self.playhead = False
        self.index = index
        self.seq = seq
        self.trig = sq.trigger()

    def keypress(self, size, key):
        if key == 't':
            self.trig.type = 0 if self.trig.type else 1 # toggle
            self.seq.set_trig(self.index, self.trig)
            self.show()
        elif key == 'r':
            self.trig.type = 1
            self.trig.note_value = randint(60,72)
            self.seq.set_trig(self.index, self.trig)
            self.show()
        elif key == 'J':
            self.trig.note_value -= 1
            self.seq.set_trig(self.index, self.trig)
            self.show()
        elif key == 'K':
            self.trig.note_value += 1
            self.seq.set_trig(self.index, self.trig)
            self.show()
        elif key == 'h':
            return super().keypress(size, 'left')
        elif key == 'j':
            return super().keypress(size, 'down')
        elif key == 'k':
            return super().keypress(size, 'up')
        elif key == 'l':
            return super().keypress(size, 'right')
        else:
            return key  # don't call base method

    def show(self):
        if self.playhead:
            self.set_caption('**')
        elif self.trig.type == 1:
            self.set_caption(str(self.trig.note_value))
        else:
            self.set_caption('__')
            
    def setPlayhead(self, ph):
        self.playhead = ph
        self.show()

    def setNote(self, state, note):
        self.trig.type = 1 if state else 0
        self.trig.note_value = note
        self.seq.set_trig(self.index, self.trig)
        self.show()

