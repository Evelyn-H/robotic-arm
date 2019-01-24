from math import cos, sin, tan, acos, pi
import numpy as np
from scipy.interpolate import RegularGridInterpolator

class MVC(object):
    def __init__(self, timestep):
        self.paused = False
        self.model = None
        self.view = None
        self.currentDrawFile = None
        self.i = 0
        self.TIMESTEP = timestep
        self.angles = np.array([])

    def setDrawFile(self, file):
        self.currentDrawFile = file
        self.draw()

    def test(self):
        #self.model.apply_movement([5, 0, 0])
        #x = 7*cos(self.i)+sin(self.i*1.5)-((abs(cos(self.i)+3*(sin(self.i+0.5*pi))*sin(self.i))/cos(self.i))*sin(self.i-0.5*pi))
        #y = 3*sin(self.i)+sin(cos(self.i*1.64))
        # x= 7*cos(self.i)
        # y = 7*sin(self.i)
        # z = 0
        #
        # self.i = self.i + 0.025
        #
        # self.model.apply_movement([x, y, z])
        #self.model.apply_movement([8,-15,0])

        # x = np.linspace(-10, 8, 200)
        # y = np.linspace(-15,15,200)
        # z = np.zeros((1,200))
        # grid=[]
        # for c in x:
        #     for b in y:
        #         grid.append([c,b,0])
        #
        #
        #
        # data = []
        # for d in range(len(grid)):
        #     print(d)
        #     data.append(self.model.apply_movement(grid[d]))
        #
        # for i in range(len(grid)):
        #     data[i][0] = data[i][0]-20
        #     print(grid[i],"->", data[i])
        #
        # np.save("/home/hermann/grid.dat", np.array(grid))
        # np.save("/home/hermann/data.dat", np.array(data))
        # #interpf = RegularGridInterpolator(x,y,z,data)





    def updateData(self):
        pass

    def draw(self):
        if self.angles.size == 0 and self.currentDrawFile is not None:
            oldpos = np.array([-5,0,11])

            with open(self.currentDrawFile.name, 'r') as f:
                #print(f)

                for line in f:

                    #print("line:", line)
                    if line[0] == 'E':
                        print("break")
                        f.close()
                        break

                    if line[0] == 'N':
                        self.angles = np.append(self.angles, self.model.goto(oldpos, oldpos+[0,0, 1]))
                        oldpos = oldpos+np.array([0, 0, 1])

                    else:
                        c = list(map(float, line.split()))
                        c.append(-0.01)
                        coordinates = np.array([c[1], c[0], c[2]])
                        self.angles = np.append(self.angles, self.model.goto(oldpos, coordinates))
                        oldpos = coordinates
            self.angles = np.append(self.angles, (np.array([0,0,0,0]), np.array([0])))
            self.angles = self.angles.flatten()
            self.currentDrawFile = None

        elif self.angles.size > 0:
            if self.angles[0].size > 1:
                self.model.moveToAngle(self.angles[0])

            self.angles = np.delete(self.angles, 0)

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
        #self.view.master.after_idle(self.viewLoop)