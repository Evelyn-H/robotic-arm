import tkinter as tk
from tkinter import filedialog

class Window(tk.Frame):

    def __init__(self, master, callback):
        tk.Frame.__init__(self, master)

        self.y_bias = 10
        self.x_bias = 10
        self.linewidth = 2
        table_dims = [29.7, 42]

        self.tabletopleftx = -table_dims[1]/2
        self.tabletoplefty= 5.15

        self.tabletoprightx = table_dims[1]/2
        self.tabletoprighty = 5.15

        self.tablebottomleftx = -table_dims[1]/2
        self.tablebottomlefty = 5.15+table_dims[0]

        self.tablebottomrightx = table_dims[1]/2
        self.tablebottomrighty = 5.15+table_dims[0]

        # Table
        self.table = None

        # Ovals and lines
        self.j1topdownoval = None
        self.j2topdownoval = None
        self.j3topdownoval = None
        self.j4topdownoval = None
        self.eetopdownoval = None

        self.j1j2topdownline = None
        self.j2j3topdownline = None
        self.j3j4topdownline = None
        self.j4EEtopdownline = None

        self.j1sideoval = None
        self.j2sideoval = None
        self.j3sideoval = None
        self.j4sideoval = None
        self.eesideoval = None
        self.comsideoval = None

        self.j1j2sideline = None
        self.j2j3sideline = None
        self.j3j4sideline = None
        self.j4EEsideline = None

        # Labels
        self.j1l = None
        self.j1thl = None
        self.j1x = None
        self.j1y = None
        self.j1z = None

        self.j2l = None
        self.j2thl = None
        self.j2x = None
        self.j2y = None
        self.j2z = None
        self.j2Kappa = None

        self.j3l = None
        self.j3thl = None
        self.j3x = None
        self.j3y = None
        self.j3z = None
        self.j3Kappa = None

        self.j4l = None
        self.j4thl = None
        self.j4x = None
        self.j4y = None
        self.j4z = None
        self.j4Kappa = None

        self.eel = None
        self.eethl = None
        self.eex = None
        self.eey = None
        self.eez = None

        self.master = master
        self.master.title("Simulation")
        self.master.geometry("1000x530")
        self.master.resizable(width=tk.TRUE, height=tk.TRUE)
        self.callback = callback

        self.posJ1 = self.callback.getJoint1Pos()
        self.posJ2 = self.callback.getJoint2Pos()
        self.posJ3 = self.callback.getJoint3Pos()
        self.posJ4 = self.callback.getJoint4Pos()
        self.posEE = self.callback.getEEPos()

        self.canvas_dims = [500, 500]
        self.mainframe = self.createMainContainer(master)
        self.canvascontainer = self.createCanvasContainer(self.mainframe)
        #self.informationContainer = self.createInformationContainer(self.mainframe)
        self.menucontainer = self.createMenuContainer(self.mainframe)
        self.topviewcanvas = self.createTopViewCanvas(self.canvascontainer)
        self.sideviewcanvas = self.createSideViewCanvas(self.canvascontainer)

        self.createMenuBar(self.menucontainer)
        self.createControlButtons(self.menucontainer)
        #self.createInformationLabels(self.informationContainer)

        self.tablex0 = self.canvas_dims[0]/2+self.x_bias+self.tabletopleftx*10
        self.tabley0 = self.y_bias+self.tabletoplefty*10
        self.tablex1 = self.canvas_dims[0]/2 + self.x_bias + self.tablebottomrightx*10
        self.tabley1 = self.y_bias + self.tablebottomrighty*10

        self.drawTable()




    def createInformationLabels(self, parent):
        # Delete old labels
        try:
            self.j1l.destroy()
            self.j1thl.destroy()
            self.j1x.destroy()
            self.j1y.destroy()
            self.j1z.destroy()

            self.j2l.destroy()
            self.j2thl.destroy()
            self.j2x.destroy()
            self.j2y.destroy()
            self.j2z.destroy()
            self.j2Kappa.destroy()

            self.j3l.destroy()
            self.j3thl.destroy()
            self.j3x.destroy()
            self.j3y.destroy()
            self.j3z.destroy()
            self.j3Kappa.destroy()

            self.j4l.destroy()
            self.j4thl.destroy()
            self.j4x.destroy()
            self.j4y.destroy()
            self.j4z.destroy()
            self.j4Kappa.destroy()

            self.eel.destroy()
            self.eethl.destroy()
            self.eex.destroy()
            self.eey.destroy()
            self.eez.destroy()
        except Exception:
            pass

        # LABEL JOINT 1
        self.j1l = tk.Label(parent, text="Joint 1")
        self.j1l.grid(column=0, row=0, sticky="N")

        self.j1thl = tk.Label(parent, text="θ = " +str(round(self.callback.getJoint1Angle(),2)))
        self.j1thl.grid(column=0, row=1, sticky="N W")

        self.j1x = tk.Label(parent, text="x = " +str(round(self.posJ1[0],2)))
        self.j1x.grid(column=0, row=2, sticky="N W")

        self.j1y = tk.Label(parent, text="y = " +str(round(self.posJ1[1],2)))
        self.j1y.grid(column=0, row=3, sticky="N W")

        self.j1z = tk.Label(parent, text="z = " +str(round(self.posJ1[2],2)))
        self.j1z.grid(column=0, row=4, sticky="N W")

        # LABEL Joint 2
        self.j2l = tk.Label(parent, text="Joint 2")
        self.j2l.grid(column=1, row=0, sticky="N", padx=15)

        self.j2thl = tk.Label(parent, text="θ = " + str(round(self.callback.getJoint2Angle(),2)))
        self.j2thl.grid(column=1, row=1, sticky="N W", padx=15)

        self.j2x = tk.Label(parent, text="x = " + str(round(self.posJ2[0],2)))
        self.j2x.grid(column=1, row=2, sticky="N W", padx=15)

        self.j2y = tk.Label(parent, text="y = " + str(round(self.posJ2[1],2)))
        self.j2y.grid(column=1, row=3, sticky="N W", padx=15)

        self.j2z = tk.Label(parent, text="z = " + str(round(self.posJ2[2],2)))
        self.j2z.grid(column=1, row=4, sticky="N W", padx=15)

        self.j2Kappa = tk.Label(parent, text="k = " + str(round(self.callback.getKappaJoint2(), 4)))
        self.j2Kappa.grid(column=1, row=5, sticky="N W", padx=15)

        # LABEL JOINT 3
        self.j3l = tk.Label(parent, text="Joint 3")
        self.j3l.grid(column=2, row=0, sticky="N", padx=15)

        self.j3thl = tk.Label(parent, text="θ = " + str(round(self.callback.getJoint3Angle(),2)))
        self.j3thl.grid(column=2, row=1, sticky="N W", padx=15)

        self.j3x = tk.Label(parent, text="x = " + str(round(self.posJ3[0],2)))
        self.j3x.grid(column=2, row=2, sticky="N W", padx=15)

        self.j3y = tk.Label(parent, text="y = " + str(round(self.posJ3[1],2)))
        self.j3y.grid(column=2, row=3, sticky="N W", padx=15)

        self.j3z = tk.Label(parent, text="z = " + str(round(self.posJ3[2],2)))
        self.j3z.grid(column=2, row=4, sticky="N W", padx=15)

        self.j3Kappa = tk.Label(parent, text="k = " + str(round(self.callback.getKappaJoint3(), 4)))
        self.j3Kappa.grid(column=2, row=5, sticky="N W", padx=15)

        # LABEL JOINT 4
        self.j4l = tk.Label(parent, text="Joint 4")
        self.j4l.grid(column=3, row=0, sticky="N", padx=15)

        self.j4thl = tk.Label(parent, text="θ = " + str(round(self.callback.getJoint4Angle(),2)))
        self.j4thl.grid(column=3, row=1, sticky="N W", padx=15)

        self.j4x = tk.Label(parent, text="x = " + str(round(self.posJ4[0],2)))
        self.j4x.grid(column=3, row=2, sticky="N W", padx=15)

        self.j4y = tk.Label(parent, text="y = " + str(round(self.posJ4[1],2)))
        self.j4y.grid(column=3, row=3, sticky="N W", padx=15)

        self.j4z = tk.Label(parent, text="z = " + str(round(self.posJ4[2],2)))
        self.j4z.grid(column=3, row=4, sticky="N W", padx=15)

        self.j4Kappa = tk.Label(parent, text="k = " + str(round(self.callback.getKappaJoint4(), 4)))
        self.j4Kappa.grid(column=3, row=5, sticky="N W", padx=15)

        # LABEL EE
        self.eel = tk.Label(parent, text="EE")
        self.eel.grid(column=4, row=0, sticky="N", padx=15)

        self.eethl = tk.Label(parent, text="θ = " + str(round(self.callback.getEEorientation(),2)))
        self.eethl.grid(column=4, row=1, sticky="N W", padx=15)

        self.eex = tk.Label(parent, text="x = " + str(round(self.posEE[0],2)))
        self.eex.grid(column=4, row=2, sticky="N W", padx=15)

        self.eey = tk.Label(parent, text="y = " + str(round(self.posEE[1],2)))
        self.eey.grid(column=4, row=3, sticky="N W", padx=15)

        self.eez = tk.Label(parent, text="z = " + str(round(self.posEE[2],2)))
        self.eez.grid(column=4, row=4, sticky="N W", padx=15)

    def createTopViewCanvas(self, parent):
        canvas = tk.Canvas(parent, width=self.canvas_dims[0], height=self.canvas_dims[1], bg="gainsboro")
        canvas.grid(column=0, row=0, sticky="W E")
        return canvas

    def createSideViewCanvas(self, parent):
        canvas = tk.Canvas(parent, width=self.canvas_dims[0], height=self.canvas_dims[1], bg="gainsboro")
        canvas.grid(column=1, row=0, sticky="W E")
        return canvas

    def createMainContainer(self, parent):
        frame = tk.Frame(parent, background="bisque")
        frame.pack(side="bottom", fill="both", expand=True)
        return frame

    def createInformationContainer(self, parent):
        frame = tk.Frame(parent, background="white")
        frame.pack(side="top", fill="both", expand=True)
        return frame

    def createMenuContainer(self, parent):
        frame = tk.Frame(parent, background="light grey")
        frame.pack(side="bottom", fill="x", expand=False)
        return frame

    def createCanvasContainer(self, parent):
        frame = tk.Frame(parent, background="white")
        frame.pack(side="top", fill="both", expand=True)
        return frame

    def clearDrawing(self):
        self.topviewcanvas = self.createTopViewCanvas(self.canvascontainer)
        self.drawTable()
        self._refreshTopDownView()
        self._refreshSideView()

    def createMenuBar(self, parent):
        tk.Label(parent, text=".draw file:", background="light grey").pack(side="left", fill="y")
        tk.Button(parent, text="Browse...", command=self.browseFiles).pack(side="left", fill="y", padx=10)
        #self.filenamelabel = Label(parent, text="None")
        #self.filenamelabel.grid(column=0, row=0, padx=10, sticky="N S W E")

    def browseFiles(self):
        self.filewrapper = filedialog.askopenfile(parent=self.master, initialdir="C:", title="Select file",
                                                  filetypes=(("draw files", "*.draw"), ("all files", "*.*")))
        self.callback.setDrawFile(self.filewrapper)
        #self.filenamelabel.config(text=self.filepath)

    def createControlButtons(self, parent):
        tk.Button(parent, text="Pause/Continue", command=self.callback.pause).pack(side="left", fill="y", padx=15)
        tk.Button(parent, text="Clear", command=self.clearDrawing).pack(side="left", fill="y", padx=15)

    def drawTable(self):
        self.table = self.topviewcanvas.create_rectangle(self.tablex0,
                                            self.tabley0,
                                            self.tablex1,
                                            self.tabley1, fill="white")

        self.sideviewcanvas.create_line(self.x_bias+self.tabletoplefty*10,
                                        self.canvas_dims[1]-self.y_bias-(self.callback.getJoint2Pos())[2]*10,
                                        self.x_bias+self.tablebottomrighty*10,
                                        self.canvas_dims[1] - self.y_bias -(self.callback.getJoint2Pos())[2]*10)

    def refresh(self):
        self.posJ1 = self.callback.getJoint1Pos()
        self.posJ2 = self.callback.getJoint2Pos()
        self.posJ3 = self.callback.getJoint3Pos()
        self.posJ4 = self.callback.getJoint4Pos()
        self.posEE = self.callback.getEEPos()

        self.callback.test()
        #self.callback.draw()
        self._drawOnTable()
        #self._refreshInformation()
        self._refreshTopDownView()
        self._refreshSideView()

    def _drawOnTable(self):
        collision = self._checkCollisionEE_Table()

        if collision[0]:
            self.topviewcanvas.create_oval(collision[1]-1, collision[2]-1,
                                           collision[1]+1, collision[2]+1,
                                           fill="black")

    def _checkCollisionEE_Table(self):
        eepos = self.callback.getEEPos()
        collision = False
        x = 0
        y = 0

        if (self.tablex0 < eepos[0] * 10 + self.canvas_dims[0] / 2 + self.x_bias < self.tablex1
            and self.tabley0 < eepos[1] * 10 + self.y_bias < self.tabley1 and eepos[2] <= self.callback.getJoint2Pos()[2]):
            collision = True
            x = eepos[0] * 10 + self.canvas_dims[0] / 2 + self.x_bias
            y = eepos[1] * 10 + self.y_bias

        return (collision, x, y)

    def _refreshInformation(self):
        self.createInformationLabels(self.informationContainer)

    def _refreshTopDownView(self):
        self.topviewcanvas.delete(self.j1topdownoval)
        self.topviewcanvas.delete(self.j2topdownoval)
        self.topviewcanvas.delete(self.j3topdownoval)
        self.topviewcanvas.delete(self.j4topdownoval)
        self.topviewcanvas.delete(self.eetopdownoval)

        self.topviewcanvas.delete(self.j1j2topdownline)
        self.topviewcanvas.delete(self.j2j3topdownline)
        self.topviewcanvas.delete(self.j3j4topdownline)
        self.topviewcanvas.delete(self.j4EEtopdownline)

        self.j1j2topdownline = self.topviewcanvas.create_line(
            self.posJ1[0] * 10 + self.canvas_dims[0] / 2 + self.x_bias,
            self.posJ1[1] * 10 + self.y_bias,
            self.posJ2[0] * 10 + self.canvas_dims[0] / 2 + self.x_bias,
            self.posJ2[1] * 10 + self.y_bias,
            width=self.linewidth)

        self.j2j3topdownline = self.topviewcanvas.create_line(
            self.posJ2[0] * 10 + self.canvas_dims[0] / 2 + self.x_bias,
            self.posJ2[1] * 10 + self.y_bias,
            self.posJ3[0] * 10 + self.canvas_dims[0] / 2 + self.x_bias,
            self.posJ3[1] * 10 + self.y_bias,
            width=self.linewidth)

        self.j3j4topdownline = self.topviewcanvas.create_line(
            self.posJ3[0] * 10 + self.canvas_dims[0] / 2 + self.x_bias,
            self.posJ3[1] * 10 + self.y_bias,
            self.posJ4[0] * 10 + self.canvas_dims[0] / 2 + self.x_bias,
            self.posJ4[1] * 10 + self.y_bias,
            width=self.linewidth)

        self.j4EEtopdownline = self.topviewcanvas.create_line(
            self.posJ4[0] * 10 + self.canvas_dims[0] / 2 + self.x_bias,
            self.posJ4[1] * 10 + self.y_bias,
            self.posEE[0] * 10 + self.canvas_dims[0] / 2 + self.x_bias,
            self.posEE[1] * 10 + self.y_bias,
            width=self.linewidth)

        #Ovals
        self.j1topdownoval = self.topviewcanvas.create_oval(
            self.posJ1[0] * 10 + self.canvas_dims[0] / 2 - 5 + self.x_bias,
            self.posJ1[1] * 10 + self.y_bias - 5,
            self.posJ1[0] * 10 + self.canvas_dims[0] / 2 + 5 + self.x_bias,
            self.posJ1[1] * 10 + 5 + self.y_bias,
            fill="yellow")

        self.j2topdownoval = self.topviewcanvas.create_oval(
            self.posJ2[0] * 10 + self.canvas_dims[0] / 2 - 5 + self.x_bias,
            self.posJ2[1] * 10 + self.y_bias - 5,
            self.posJ2[0] * 10 + self.canvas_dims[0] / 2 + 5 + self.x_bias,
            self.posJ2[1] * 10 + 5 + self.y_bias,
            fill="green")

        self.j3topdownoval = self.topviewcanvas.create_oval(
            self.posJ3[0] * 10 + self.canvas_dims[0] / 2 - 5 + self.x_bias,
            self.posJ3[1] * 10 + self.y_bias - 5,
            self.posJ3[0] * 10 + self.canvas_dims[0] / 2 + 5 + self.x_bias,
            self.posJ3[1] * 10 + 5 + self.y_bias,
            fill="blue")

        self.j4topdownoval = self.topviewcanvas.create_oval(
            self.posJ4[0] * 10 + self.canvas_dims[0] / 2 - 5 + self.x_bias,
            self.posJ4[1] * 10 + self.y_bias - 5,
            self.posJ4[0] * 10 + self.canvas_dims[0] / 2 + 5 + self.x_bias,
            self.posJ4[1] * 10 + 5 + self.y_bias,
            fill="cyan")

        self.eetopdownoval = self.topviewcanvas.create_oval(
            self.posEE[0] * 10 + self.canvas_dims[0] / 2 - 5 + self.x_bias,
            self.posEE[1] * 10 + self.y_bias - 5,
            self.posEE[0] * 10 + self.canvas_dims[0] / 2 + 5 + self.x_bias,
            self.posEE[1] * 10 + 5 + self.y_bias,
            fill="red")

    def _refreshSideView(self):
        self.sideviewcanvas.delete(self.j1sideoval)
        self.sideviewcanvas.delete(self.j2sideoval)
        self.sideviewcanvas.delete(self.j3sideoval)
        self.sideviewcanvas.delete(self.j4sideoval)
        self.sideviewcanvas.delete(self.eesideoval)
        self.sideviewcanvas.delete(self.comsideoval)

        self.sideviewcanvas.delete(self.j1j2sideline)
        self.sideviewcanvas.delete(self.j2j3sideline)
        self.sideviewcanvas.delete(self.j3j4sideline)
        self.sideviewcanvas.delete(self.j4EEsideline)

        #Lines
        self.j1j2sideline = self.sideviewcanvas.create_line(self.posJ1[1] * 10 + self.x_bias,
                                                            self.canvas_dims[1] - self.posJ1[2] * 10 - self.y_bias,
                                                            self.posJ2[1] * 10 + self.x_bias,
                                                            self.canvas_dims[1] - self.posJ2[2] * 10 - self.y_bias,
                                                            width=self.linewidth)

        self.j2j3sideline = self.sideviewcanvas.create_line(self.posJ2[1] * 10 + self.x_bias,
                                                            self.canvas_dims[1] - self.posJ2[2] * 10 - self.y_bias,
                                                            self.posJ3[1] * 10 + self.x_bias,
                                                            self.canvas_dims[1] - self.posJ3[2] * 10 - self.y_bias,
                                                            width=self.linewidth)

        self.j3j4sideline = self.sideviewcanvas.create_line(self.posJ3[1] * 10 + self.x_bias,
                                                            self.canvas_dims[1] - self.posJ3[2] * 10 - self.y_bias,
                                                            self.posJ4[1] * 10 + self.x_bias,
                                                            self.canvas_dims[1] - self.posJ4[2] * 10 - self.y_bias,
                                                            width=self.linewidth)

        self.j4EEsideline = self.sideviewcanvas.create_line(self.posJ4[1] * 10 + self.x_bias,
                                                            self.canvas_dims[1] - self.posJ4[2] * 10 - self.y_bias,
                                                            self.posEE[1] * 10 + self.x_bias,
                                                            self.canvas_dims[1] - self.posEE[2] * 10 - self.y_bias,
                                                            width=self.linewidth)


        # Ovals
        self.j1sideoval = self.sideviewcanvas.create_oval(self.posJ1[1] * 10 + self.x_bias - 5,
                                                          self.canvas_dims[1] - self.posJ1[2] * 10 - 5 - self.y_bias,
                                                          self.posJ1[1] * 10 + self.x_bias + 5,
                                                          self.canvas_dims[1] - self.posJ1[2] * 10 + 5 - self.y_bias,
                                                          fill="yellow")

        self.j2sideoval = self.sideviewcanvas.create_oval(self.posJ2[1]*10 + self.x_bias - 5,
                                                          self.canvas_dims[1] - self.posJ2[2]*10 - 5 - self.y_bias,
                                                          self.posJ2[1]*10 + self.x_bias + 5,
                                                          self.canvas_dims[1] - self.posJ2[2]*10 + 5 - self.y_bias,
                                                          fill="green")

        self.j3sideoval = self.sideviewcanvas.create_oval(self.posJ3[1]*10 + self.x_bias - 5,
                                                          self.canvas_dims[1] - self.posJ3[2]*10 - 5 - self.y_bias,
                                                          self.posJ3[1]*10 + self.x_bias + 5,
                                                          self.canvas_dims[1] - self.posJ3[2]*10 + 5 - self.y_bias,
                                                          fill="blue")

        self.j4sideoval = self.sideviewcanvas.create_oval(self.posJ4[1]*10 + self.x_bias - 5,
                                                          self.canvas_dims[1] - self.posJ4[2]*10 - 5 - self.y_bias,
                                                          self.posJ4[1]*10 + self.x_bias + 5,
                                                          self.canvas_dims[1] - self.posJ4[2]*10 + 5 - self.y_bias,
                                                          fill="cyan")

        self.eesideoval = self.sideviewcanvas.create_oval(self.posEE[1]*10 + self.x_bias - 5,
                                                          self.canvas_dims[1] - self.posEE[2]*10 - 5 - self.y_bias,
                                                          self.posEE[1]*10 + self.x_bias + 5,
                                                          self.canvas_dims[1] - self.posEE[2]*10 + 5 - self.y_bias,
                                                          fill="red")

        self.posCOM = self.callback.getCOMPos()
        self.comsideoval = self.sideviewcanvas.create_oval(self.posCOM[1]*10 + self.x_bias - 5,
                                                          self.canvas_dims[1] - self.posCOM[2]*10 - 5 - self.y_bias,
                                                          self.posCOM[1]*10 + self.x_bias + 5,
                                                          self.canvas_dims[1] - self.posCOM[2]*10 + 5 - self.y_bias,
                                                          fill="orange")