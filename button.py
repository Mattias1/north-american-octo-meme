#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode Tkinter tutorial

In this script, we use pack manager
to position two buttons in the
bottom right corner of the window. 

author: Jan Bodnar
last modified: December 2010
website: www.zetcode.com
"""

from tkinter import Tk, RIGHT, BOTH, RAISED
from tkinter.ttk import Frame, Button, Style


class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("Buttons")
        #self.style = Style()
        #self.style.theme_use("default")
        
        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=1)
        
        self.pack(fill=BOTH, expand=1)
        
        closeButton = Button(self, text="Close")
        closeButton.pack(side=RIGHT, padx=10, pady=5)
        okButton = Button(self, text="OK")
        okButton.pack(side=RIGHT)
              

def main():
  
    root = Tk()
    root.geometry("300x200+300+300")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()
