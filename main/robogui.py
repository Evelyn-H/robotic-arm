# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 13:25:08 2018

@author: heier
"""

from tkinter import *
from tkinter import ttk
root = Tk()

# Global variables
bg = 0
robo = 0
cam = 0
bgoffsetx, bgoffsety = 50, 50
bgx, bgy = 500, 300
curLine = None

# Methods
def xy(event):
    global lastx, lasty
    lastx, lasty = canvas.canvasx(event.x), canvas.canvasy(event.y)

def addLine(event):
    xy(event)
    global lastx, lasty, curLine
    if (curLine is None):
        curLine = canvas.create_line((lastx, lasty, lastx, lasty), width=3)
    else:
        x,y = canvas.canvasx(event.x), canvas.canvasy(event.y)
        extendLine(curLine, x, y)
        

# Adds another point to the given line
def extendLine(line, x, y):
    canvas.coords(line, canvas.coords(line)+[x,y])

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
insertPoint.grid(column=4, row=0)
deletePoint.grid(column=5, row=0)

# Bindings
canvas.bind("<Button-1>", addLine)

# Base stuff, like white rectangle bg and ish-robot position.
bg = canvas.create_rectangle((bgoffsetx,bgoffsety, bgoffsetx+bgx, bgoffsety+bgy), 
                             fill='white', tags=('bg'))
robo = canvas.create_rectangle((bgoffsetx + (bgx/3), 5, bgoffsetx+bgx-(bgx/3), bgoffsety-5), 
                               fill='black', tags =('robo'))
cam = canvas.create_rectangle((bgoffsetx + (bgx/2) - (bgx/20), bgoffsety+bgy+5,
                               bgoffsetx + (bgx/2) + (bgx/20), bgoffsety+bgy+5+(bgoffsety)),
                              fill='grey', tags=('cam'))

# Begin thingie.
root.mainloop()