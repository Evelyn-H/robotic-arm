from kinematics.solver import Solver
from simulation.InverseKinematics import IKSolver
from simulation.ForwardKinematics import ForwardKinematics
from simulation.PhysicsEngine import Physics
from kinematics.solverNEW import Solver
from math import sqrt, pi, radians as rad
import numpy as np


class Model(object):

    def __init__(self, robot, physics, com):
        self.robot = robot
        links = robot.links
        ee_dims = robot.ee_dims
        print(robot.ee_dims)
        ik_params = [[links[1], links[2], sqrt(ee_dims[0] ** 2 + ee_dims[1] ** 2)], [[-60, 60], [-90, 90], [-90, 90]], ee_dims,
                     20, -45, 45, 50]
        self.ik = IKSolver(*ik_params)
        self.fk = ForwardKinematics([0, 0.5 * pi, 0, 0],
                               [links[0], 0, 0, 0],
                               [0, links[1], links[2], ee_dims[0]],
                               [0.5 * pi, 0, 0, 0.5 * pi],
                               np.array([
                                   [0, 0, 0, 1],
                                   [0, 0, 0, 1],
                                   [0, 0, 0, 1],
                                   [0, 0, ee_dims[1], 1]
                               ]),
                               com)

        self.physics = physics
        self.iksol = []
        self.com = com

    def apply_postprocessing_physics(self, angles, positions):
        return self.physics.apply_postprocessing_physics(angles, positions)

    def physics_set_angles(self, angles):
        self.physics.set_angles(angles)

    def interpGoto(self, oldpos, position):
        SEGMENTS = 10

        currentAngles = self.ik.find_angles(oldpos)
        targetAngles = self.ik.find_angles(position)
        angleVec = np.array(targetAngles)[0:4]-np.array(currentAngles)[0:4]

        return np.array([(currentAngles[0:4] + (angleVec/SEGMENTS)*(i+1), np.array([0])) for i in range(SEGMENTS)])

    def moveToAngle(self, angle):
        positions = self.fk.move([rad(angle[0]), -rad(angle[1]), -rad(angle[2]), -rad(angle[3])])
        for i in range(4):
            self.robot.currentPosition[-i-1][0] = positions[3-i][1]
            self.robot.currentPosition[-i-1][1] = positions[3-i][0]
            self.robot.currentPosition[-i-1][2] = positions[3-i][2]

    def goto(self, oldpos, position):
        vector = position-oldpos
        num_segments = max(3, int(round(np.linalg.norm(vector)*2)))
        angles = np.array([self.interpGoto(oldpos+(vector/num_segments)*(i), oldpos+(vector/num_segments)*(i+1)) for i in range(num_segments)])

        return angles

    def apply_movement(self, to_position):
        oldiksol = self.iksol.copy()

        self.iksol = self.ik.find_angles([to_position[0], to_position[1], to_position[2]].copy())

        if self.iksol is None:
            self.iksol = oldiksol

        self.robot.currentAngles = -(np.array([self.iksol[0], self.iksol[1], self.iksol[2], self.iksol[3]]))

        self.robot.ee_orientation = self.iksol[4]

        positions = self.fk.move([rad(self.iksol[0]), -rad(self.iksol[1]), -rad(self.iksol[2]), -rad(self.iksol[3])])
        self.physics_set_angles([rad(self.iksol[0]), rad(self.iksol[1]), rad(self.iksol[2]), rad(self.iksol[3])])

        angles = self.apply_postprocessing_physics(self.iksol, positions)
        positions = self.fk.move([rad(angles[0]), -rad(angles[1]), -rad(angles[2]), -rad(angles[3])])

        for i in range(0,200):
            angles = self.apply_postprocessing_physics(angles, positions)
            positions = self.fk.move([rad(angles[0]), -rad(angles[1]), -rad(angles[2]), -rad(angles[3])])

        self.robot.com = positions[4]
        for i in range(4):
            self.robot.currentPosition[-i-1][0] = positions[3-i][1]
            self.robot.currentPosition[-i-1][1] = positions[3-i][0]
            self.robot.currentPosition[-i-1][2] = positions[3-i][2]

        return [positions[3][0], positions[3][1], positions[3][2]-10.5]

    def getJoint1Angle(self):
        return self.robot.currentAngles[0]

    def getJoint2Angle(self):
        return self.robot.currentAngles[1]

    def getJoint3Angle(self):
        return self.robot.currentAngles[2]

    def getJoint4Angle(self):
        return self.robot.currentAngles[3]

    def getEEorientation(self):
        return self.robot.ee_orientation

    def getJoint1Pos(self):
        return self.robot.currentPosition[0]

    def getJoint2Pos(self):
        return self.robot.currentPosition[1]

    def getJoint3Pos(self):
        return self.robot.currentPosition[2]

    def getJoint4Pos(self):
        return self.robot.currentPosition[3]

    def getEEPos(self):
        return self.robot.currentPosition[4]

    def getCOMPos(self):
        com = self.robot.com
        return [com[1], com[0], com[2]]

    def getKappaJoint2(self):
        return self.robot.spring_constants[0]

    def getKappaJoint3(self):
        return self.robot.spring_constants[1]

    def getKappaJoint4(self):
        return self.robot.spring_constants[2]
