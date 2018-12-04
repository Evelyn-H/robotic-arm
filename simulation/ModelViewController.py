from math import cos, sin, tan, acos, pi
class MVC(object):
    def __init__(self, timestep):
        self.paused = False
        self.model = None
        self.view = None
        self.currentDrawFile = None
        self.i = 0
        self.TIMESTEP = timestep

    def setDrawFile(self, file):
        self.currentDrawFile  = file

    def test(self):
        #x = 7*cos(self.i)+sin(self.i*1.5)-((abs(cos(self.i)+3*(sin(self.i+0.5*pi))*sin(self.i))/cos(self.i))*sin(self.i-0.5*pi))
        #y = 3*sin(self.i)+sin(cos(self.i*1.64))
        x= 7*cos(self.i)
        y = 7*sin(self.i)
        z = -0.1

        self.i = self.i + 0.025

        self.model.apply_movement([x, y, z])

    def updateData(self):
        pass

    def draw(self):
        pass

    def getJoint1Angle(self):
        return self.model.getJoint1Angle()

    def getJoint2Angle(self):
        return self.model.getJoint2Angle()

    def getJoint3Angle(self):
        return self.model.getJoint3Angle()

    def getJoint4Angle(self):
        return self.model.getJoint4Angle()

    def getEEorientation(self):
        return self.model.getEEorientation()

    def getJoint1Pos(self):
        return self.model.getJoint1Pos()

    def getJoint2Pos(self):
        return self.model.getJoint2Pos()

    def getJoint3Pos(self):
        return self.model.getJoint3Pos()

    def getJoint4Pos(self):
        return self.model.getJoint4Pos()

    def getEEPos(self):
        return self.model.getEEPos()

    def getCOMPos(self):
        return self.model.getCOMPos()

    def getKappaJoint2(self):
        return self.model.getKappaJoint2()

    def getKappaJoint3(self):
        return self.model.getKappaJoint3()

    def getKappaJoint4(self):
        return self.model.getKappaJoint4()

    def pause(self):
        self.paused = (not self.paused)

    def createModel(self, constructor, **kwargs):
        self.model = constructor(**kwargs)

    def createView(self, constructor, **kwargs):
        self.view = constructor(**kwargs)

    def viewLoop(self):
        if not self.paused:
            self.view.refresh()

        self.view.master.after(self.TIMESTEP, self.viewLoop)
