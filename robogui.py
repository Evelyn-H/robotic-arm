# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 13:25:08 2018

@author: heier
"""

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import math

# from arm import Arm
# arm = Arm('/dev/ttyACM0')


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

def cxy(event):
    global cx, cy
    cx, cy = canvas.canvasx(event.x), canvas.canvasy(event.y)

def addLine(event):
    xy(event)
    global lastx, lasty, curLine, lineList
    if (curLine is None):
        curLine = canvas.create_line((lastx, lasty, lastx, lasty), width=3,
                                     tags=('line'))
        lineList.append(curLine)

        # arm.move_to(convertPoint(lastx, lasty))
        # arm.down()
    else:
        x,y = canvas.canvasx(event.x), canvas.canvasy(event.y)
        extendLine(curLine, x, y)

        # arm.move_to(convertPoint(x, y))
        # arm.up()

def addNewLine():
    print("New line")
    resetCurLine()
    unbindAll()
    canvas.bind("<Button-1>", addLine)    

def addNewCircle():
    print("Circle tool selected")
    unbindAll()
    canvas.bind("<Button-1>", circleStart)
    canvas.bind("<B1-Motion>", circleShift)
    canvas.bind("<ButtonRelease-1>", circlePlace)
    

def circleRegPoint(x, y, r, c, cTot):
    c = c%cTot # In case it is ever larger.
    angle = (c/cTot)*2*math.pi
    xr = r*math.cos(angle)
    yr = r*math.sin(angle)
    
    return (x+xr), (y+yr)

def circleStart(event):
    resetCurLine()
    cxy(event)
    
    global cx, xy, cr, inp0, inp1, curLine
    
    # Get radius
    if str.isdigit(inp0.get()):
        cr = int(inp0.get())
    else:
        cr = 10
    
    # Get number of sides
    if str.isdigit(inp1.get()):
        cTot = int(inp1.get())
    else:
        cTot = 5
    
    # Get first starting x,y.
    startx, starty = circleRegPoint(cx,cy,cr, 0, cTot)
    curLine = canvas.create_line((startx, starty, startx, starty), width=3,
                                     tags=('line'), fill='grey')
    lineList.append(curLine)
    
    for i in range(1, cTot+1):
        nextx, nexty = circleRegPoint(cx, cy, cr, i, cTot)
        extendLine(curLine, nextx, nexty)
    
# Shift circle based on new coordinates
def circleShift(event):
    global cx, cy, cr, curLine
    
    if curLine != None:
        newx, newy = canvas.canvasx(event.x), canvas.canvasy(event.y)
        
        dx = newx-cx
        dy = newy-cy
        
        cxy(event)
        
        cTuple = canvas.coords(curLine)
        
        cList = list(cTuple)
        for i in range(0, len(cList), 2):
            cList[i] += dx
            cList[i+1] += dy
        
        newTuple = tuple(cList)
        canvas.coords(curLine, newTuple)
    else:
        print("Error: No circle-in-the-making found. ")
    
def circlePlace(event):
    global curLine
    canvas.itemconfigure(curLine, fill='black')
    curLine = None


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

def saveFileAs():
    fName = filedialog.asksaveasfilename()
    print(fName)
    if fName == "":
        return
    else:
        global lineList
        f = open(fName, "w+")
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

def unbindAll():
    global canvas
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")

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
cx, cy = 0, 0 # Circle center coordinates
cr = 10

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
menu_file.add_command(label="Save As...", command=saveFileAs)

# Creating window essentials
canvas_size = 500
canvas = Canvas(root, width=int(canvas_size*1.414), height=canvas_size)

toolbar = ttk.Frame(root, padding=(5,5,10,10))

# Placing window essentials on screen
toolbar.grid(column=0, row=0, sticky=(W,E))
canvas.grid(column=0, row=1, sticky=(N,W,E,S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

# Creating TKinter special variables
inp0 = StringVar()
inp1 = StringVar()

# Creating buttons
newLine = ttk.Button(toolbar, command=addNewLine, text="New Line")
newCircle = ttk.Button(toolbar, command=addNewCircle, text="Circle Tool")
EntryInp0 = ttk.Entry(toolbar, textvariable=inp0)
EntryInp1 = ttk.Entry(toolbar, textvariable=inp1)
basicSep = ttk.Separator(toolbar, orient=VERTICAL)
# editLine = ttk.Button(toolbar, text="Edit Line")
# deleteLine = ttk.Button(toolbar, text="Delete Line")
# addPoint = ttk.Button(toolbar, text="Add Point")
# insertPoint = ttk.Button(toolbar, text="Insert Point")
# deletePoint = ttk.Button(toolbar, text="Delete Point")
clearLines = ttk.Button(toolbar, command=clearLines, text="Clear")

# Adding buttons in grid
newLine.grid(column=0,row=0)
newCircle.grid(column=1,row=0)
# editLine.grid(column=1, row=0)
# deleteLine.grid(column=2,row=0)
# addPoint.grid(column=3, row=0)
# insertPoint.grid(column=4, row=0)
# deletePoint.grid(column=5, row=0)
EntryInp0.grid(column=6, row = 0)
EntryInp1.grid(column=7, row = 0)
basicSep.grid(column=10, row=0)
clearLines.grid(column=15, row=0)


# Bindings
# addLineBind = canvas.bind("<Button-1>", addLine)
# addCircleBind = canvas.bind("<Button-1>", circleStart)
# circleShiftBind = canvas.bind("<B1-Motion>", circleShift)
# circlePlaceBind = canvas.bind("<ButtonRelease-1>", circlePlace)

# Base stuff, like white rectangle bg and ish-robot position.
bg = canvas.create_rectangle((bgoffsetx,bgoffsety, bgoffsetx+bgx, bgoffsety+bgy),
                             fill='white', tags=('bg'))
robo = canvas.create_rectangle((bgoffsetx + (bgx/3), 5, bgoffsetx+bgx-(bgx/3), bgoffsety-5),
                               fill='black', tags =('robo'))
cam = canvas.create_rectangle((bgoffsetx + (bgx/2) - (bgx/20), bgoffsety+bgy+5,
                               bgoffsetx + (bgx/2) + (bgx/20), bgoffsety+bgy+5+(bgoffsety)),
                              fill='grey', tags=('cam'))

center = canvas.create_rectangle((bgoffsetx + (bgx/2)-3, 
                                      bgoffsety+(bgy/2)-3),
                                      bgoffsetx + (bgx/2)+3, 
                                      bgoffsety+(bgy/2)+3,
                                    fill='deep sky blue',
                                    tags=('center'))
# Begin thingie.
root.mainloop()
