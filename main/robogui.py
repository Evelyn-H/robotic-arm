# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 13:25:08 2018

@author: heier
"""

from tkinter import *
from tkinter import ttk
root = Tk()

# Creating window essentials
h = ttk.Scrollbar(root, orient=HORIZONTAL)
v = ttk.Scrollbar(root, orient=VERTICAL)
canvas = Canvas(root, scrollregion=(0,0,1000,1000), 
                yscrollcommand=v.set, xscrollcommand=h.set)
h['command'] = canvas.xview
v['command'] = canvas.yview
ttk.Sizegrip(root).grid(column=1, row=2, sticky=(S,E))
toolbar = ttk.Frame(root, padding=(5,5,10,10))

# Placing window essentials on screen
toolbar.grid(column=0, row=0, sticky=(W,E))
canvas.grid(column=0, row=1, sticky=(N,W,E,S))
h.grid(column=0, row=2, sticky=(W,E))
v.grid(column=1, row=1, sticky=(N,S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

# Creating buttons
newLine = ttk.Button(toolbar, text="New Line")
editLine = ttk.Button(toolbar, text="Edit Line")
deleteLine = ttk.Button(toolbar, text="Delete Line")
addPoint = ttk.Button(toolbar, text="Add Point")
insertPoint = ttk.Button(toolbar, text="Insert Point")
deletePoint = ttk.Button(toolbar, text="Delete Point")

# Adding buttons in grid
newLine.grid(column=0,row=0)
editLine.grid(column=1, row=0)
deleteLine.grid(column=2,row=0)
addPoint.grid(column=3, row=0)
deletePoint.grid(column=4, row=0)


# Begin thingie.
root.mainloop()