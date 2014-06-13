#!/usr/bin/python

from Tkinter import *

root = Tk()
root.title("setup wavelength")

def callback1064():
    print "called the callback 1064"

def callback532():
    print "called the callback 532"

# create a toolbar
toolbar = Frame(root)

b = Button(toolbar, text="1064 nm", width=6, command=callback1064)
b.pack(side=LEFT, padx=2, pady=2)

b = Button(toolbar, text="532 nm", width=6, command=callback532)
b.pack(side=LEFT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)

root.mainloop()

#Example : *PWC01064 selects the wavelength 1064 nm

