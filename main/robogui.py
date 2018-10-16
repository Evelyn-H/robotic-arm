# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 13:25:08 2018

@author: heier
"""

from tkinter import *
from tkinter import ttk

#-------------------------------------------------
#-------------------------------------------------
#-------------------------------------------------
#                   Methods
#-------------------------------------------------
#-------------------------------------------------
#-------------------------------------------------

def xy(event):
    global lastx, lasty
    lastx, lasty = canvas.canvasx(event.x), canvas.canvasy(event.y)

def addLine(event):
    xy(event)
    global lastx, lasty, curLine, lineList
    if (curLine is None):
        curLine = canvas.create_line((lastx, lasty, lastx, lasty), width=3,
                                     tags=('line'))
        lineList.append(curLine)
    else:
        x,y = canvas.canvasx(event.x), canvas.canvasy(event.y)
        extendLine(curLine, x, y)

def clearLines():
    global canvas, curLine, lineList
    lineList = []
    canvas.delete('line')
    curLine = None


def resetCurLine():
    global curLine
    curLine = None

# Adds another point to the given line
def extendLine(line, x, y):
    canvas.coords(line, canvas.coords(line)+[x,y])

# Save list of lines to text
def saveFile():
    global lineList
    f = open("currentDrawing.txt", "w+")
    for i in range(0, len(lineList)):
        l = lineList[i]
        cList = canvas.coords(l)
        f.write("NEWLINE\n")
        for j in range(2, len(cList), 2):
            (x,y) = convertPoint(cList[j], cList[j+1])
            f.write("%f %f\n"%(x, y))
    f.close()
    
def convertPoint(x, y):
    global bgoffsetx, bgoffsety, bgx, bgy
    newX = x-(bgoffsetx + bgx/2)
    newY = y-(bgoffsety + bgy/2)
    
    newX = a3xcm*(float(newX)/float(bgx))
    newY = a3ycm*(float(newY)/float(bgy))
    
    return (newX, newY)
    

#-------------------------------------------------
#-------------------------------------------------
#-------------------------------------------------
#                   Variables
#-------------------------------------------------
#-------------------------------------------------
#-------------------------------------------------
    
bg = 0
robo = 0
cam = 0
bgoffsetx, bgoffsety = 50, 50
bgx, bgy = 840, 600
a3xcm, a3ycm = 42.0, 29.7
curLine = None

lineList = []

#-------------------------------------------------
#-------------------------------------------------
#-------------------------------------------------
#                   GUI Creation
#-------------------------------------------------
#-------------------------------------------------
#-------------------------------------------------

root = Tk()

root.option_add('*tearOff', FALSE)

# Creating menu
menubar = Menu(root)
root.config(menu=menubar)
menu_file = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='File')

# Menu functions
menu_file.add_command(label="Save", command=saveFile)

# Creating window essentials
canvas_size = 500
canvas = Canvas(root, width=int(canvas_size*1.414), height=canvas_size)

toolbar = ttk.Frame(root, padding=(5,5,10,10))

# Placing window essentials on screen
toolbar.grid(column=0, row=0, sticky=(W,E))
canvas.grid(column=0, row=1, sticky=(N,W,E,S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

# Creating buttons
newLine = ttk.Button(toolbar, command=resetCurLine, text="New Line")
basicSep = ttk.Separator(toolbar, orient=VERTICAL)
# editLine = ttk.Button(toolbar, text="Edit Line")
# deleteLine = ttk.Button(toolbar, text="Delete Line")
# addPoint = ttk.Button(toolbar, text="Add Point")
# insertPoint = ttk.Button(toolbar, text="Insert Point")
# deletePoint = ttk.Button(toolbar, text="Delete Point")
clearLines = ttk.Button(toolbar, command=clearLines, text="Clear")

# Adding buttons in grid
newLine.grid(column=0,row=0)
# editLine.grid(column=1, row=0)
# deleteLine.grid(column=2,row=0)
# addPoint.grid(column=3, row=0)
# insertPoint.grid(column=4, row=0)
# deletePoint.grid(column=5, row=0)
basicSep.grid(column=6, row=0)
clearLines.grid(column=7, row=0)


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
