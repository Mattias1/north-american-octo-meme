from tkinter import *
from tkinter.ttk import *

# The constants
H_LEFT        = 0
H_COPY_LEFT   = 1
H_CENTER      = 2
H_COPY_RIGHT  = 3
H_RIGHT       = 4
V_TOP         = 0
V_COPY_TOP    = 1
V_MIDDLE      = 2
V_COPY_BOTTOM = 3
V_BOTTOM      = 4

# The class
class Btn(Button):
    """Matty's button class"""

    # Init method
    def __init__(self, parent, **kwargs):
        """Create a button given it's text and it's parent frame."""
        Button.__init__(self, parent, **kwargs)

    # Some getters and setters
    x = property(lambda self: self.winfo_x(), lambda self, val: self.place(x = val))
    y = property(lambda self: self.winfo_y(), lambda self, val: self.place(y = val))
    width = property(lambda self: self.winfo_width(), lambda self, val: self.configure(width = val))
    height = property(lambda self: self.winfo_height(), lambda self, val: self.configure(height = val))
    text = property(lambda self: self["text"], lambda self, val: self.configure(text = val))
    command = property(lambda self: self["command"], lambda self, val: self.configure(command = val))

    # The positioning methods
    def locateInside(self, c, h=H_LEFT, v=V_TOP, d=10):
        """Locate the current control inside c at the horizontal placement h, the vertical placement v and with a margin of d"""
        x = 0
        y = 0

        if h == H_LEFT:        x = d
        #if h == H_COPY_LEFT:   x = c.winfo_x()
        #if h == H_CENTER:      x = (c.winfo_width() - self.winfo_width()) / 2
        #if h == H_COPY_RIGHT:  x = c.winfo_x() + c.winfo_width() - self.winfo_width()
        #if h == H_RIGHT:       x = c.winfo_width() - self.winfo_width() - d

        if v == V_TOP:         y = d
        #if v == V_COPY_TOP:    y = c.winfo_y()
        #if v == V_MIDDLE:      y = (c.winfo_height() - self.winfo_height()) / 2
        #if v == V_COPY_BOTTOM: y = c.winfo_y() + c.winfo_height() - self.winfo_height()
        #if v == V_BOTTOM:      y = c.winfo_height() - self.winfo_height() - d

        self.place(x=x, y=y)

    def locateFrom(self, c, h=H_LEFT, v=V_TOP, d=10):
        """Locate the current control relative to c at the horizontal placement h, the vertical placement v and with a margin of d"""
        x = 0
        y = 0

        if h == H_LEFT:        x = c.x - self.width - d
        #if h == H_COPY_LEFT:   x = c.x
        #if h == H_CENTER:      x = c.x + (c.width - self.width) / 2
        #if h == H_COPY_RIGHT:  x = c.x + c.width - self.width
        #if h == H_RIGHT:       x = c.x + c.width + d

        if v == V_TOP:         y = c.y - self.height - d
        #if v == V_COPY_TOP:    y = c.y
        #if v == V_MIDDLE:      y = c.y + (c.height - self.height) / 2
        #if v == V_COPY_BOTTOM: y = c.y + c.height - self.height
        #if v == V_BOTTOM:      y = c.y + c.height + d

        self.place(x=x, y=y)

