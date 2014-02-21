from tkinter import *
from tkinter.ttk import *

class Btn(Button):
    """Matty's button class"""
    def __init__(self, parent, rest):
        """Create a button given it's text and it's parent frame."""
        Button.__init__(self, parent, rest) # HOW TO DO THIS???
        self["text"] = text

    def getText(self):
        return self["text"]
    def setText(self, value):
        self.configure(text = value)
    text = property(getText, setText)

    def getCommand(self):
        return self["command"]
    def setCommand(self, value):
        self.configure(command = value)
    command = property(getCommand, setCommand)

