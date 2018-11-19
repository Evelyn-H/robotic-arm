from View import Window
from tkinter import Tk
import numpy as np
from Robot import Robot
from math import sqrt
from ModelViewController import MVC
from Model import Model
from PhysicsEngine import Physics

# EE characteristics
ee_dims = [8.6, 9]
ee_angle = np.arctan((9/8.6))
ee_orientation = 0
links = [10.7, 11.9, 10.5, sqrt(ee_dims[0]**2 + ee_dims[1]**2)]
angleRanges = [[-90, 90], [-90, 90], [-90, 90], [-90, 90]]
currentPosition = [[0,0,0],
                   [0,0,links[0]],
                   [0,0,links[0]+links[1]],
                   [0,0,links[0]+links[1]+links[2]],
                   [0,ee_dims[1],links[0]+links[1]+links[2]+ee_dims[0]]]

initialAngles = [0, 0, 0, 0]
link_masses = [1, 1, 1, 1]
spring_constants = [0.1, 0.1, 0.001]
TIMESTEP = 25

robot = Robot(links, angleRanges, currentPosition, initialAngles, ee_orientation, ee_dims, link_masses, spring_constants)
physics = Physics(robot.link_masses, robot.spring_constants)


master = Tk()

mvc = MVC(TIMESTEP)
mvc.createModel(Model, robot=robot, physics=physics)
mvc.createView(Window, master=master, callback=mvc)
mvc.viewLoop()
master.mainloop()