from tkinter import *
from Keyboard import Keyboard

class KeyboardGui(Tk):

    def __init__(self, parent):
        Tk.__init__(self,parent)
        self.parent = parent
        self.value = ""
        self.k = Keyboard()
        self.initialize()

    def initialize(self):        
        self.k.load_language('ru')        
        self.geometry('{0}x{1}+{2}+{3}'.format(self.k.width, self.k.height, self.k.location_x, self.k.location_y))
        self.bind("<FocusOut>", self.on_focus_out)
        self.myEntry = Entry(self)
        self.myEntry.place(x=0,y=0, width=440, height=30)

    # def create_el(self, el, x, y):
    #     if el["control"]=="button":
    #         pass
    #     elif el["control"]=="field":
    #         pass

    # def clear(self):
    #     pass

    # def width(self, size):
    #     pass

    def on_focus_out(self, event):
        if event.widget == self:
            self.value = "WORK"
            self.destroy()            


