from ForwardKinematics import ForwardKinematics
from InverseKinematics import IKSolver
from PhysicsEngine import Physics
from math import sqrt, pi, radians as rad
import numpy as np


class Model(object):

    def __init__(self, robot, physics, com):
        self.robot = robot
        links = robot.links
        ee_dims = robot.ee_dims
        self.fk = ForwardKinematics(
                                    [0, 0.5 * pi, 0, 0],
                                    [links[0], 0, 0, 0],
                                    [0, links[1], links[2], ee_dims[0]],
                                    [0.5 * pi, 0, 0, 0.5 * pi],
                                    np.array([
                                        [0, 0, 0, 1],
                                        [0, 0, 0, 1],
                                        [0, 0, 0, 1],
                                        [0, 0, ee_dims[1], 1]
                                    ]), com
                                    )
        ik_params = [[11.9, 10.5, sqrt(ee_dims[0] ** 2 + ee_dims[1] ** 2)], [[-60, 60], [-90, 90], [-90, 90]], ee_dims,
                     20, -45, 45, 50]
        self.ik = IKSolver(*ik_params)
        self.physics = physics

    def apply_preprocessing_physics(self, from_position, to_position):
        return to_position

    def apply_postprocessing_physics(self, angles, positions):
        return self.physics.apply_postprocessing_physics(angles, positions)

    def apply_movement(self, to_position):
        # applies preprocessing physics
        # to_position = self.apply_preprocessing_physics(self.robot.currentPosition, to_position)

        # runs inverse kinematics
        iksol = self.ik.find_angles([to_position[0], to_position[1], to_position[2]])

        # applies postprocessing physics on the joint angles
        self.robot.currentAngles = -(np.array([iksol[0], iksol[1], iksol[2], iksol[3]]))
        self.robot.ee_orientation = iksol[4]
        positions = self.fk.move([rad(iksol[0]), -rad(iksol[1]), -rad(iksol[2]), -rad(iksol[3])])

        angles = self.apply_postprocessing_physics(iksol, positions)
        positions = self.fk.move([rad(angles[0]), -rad(angles[1]), -rad(angles[2]), -rad(angles[3])])

        for i in range(0,200):
            angles = self.apply_postprocessing_physics(angles, positions)
            positions = self.fk.move([rad(angles[0]), -rad(angles[1]), -rad(angles[2]), -rad(angles[3])])

        self.robot.com = positions[4]
        self.robot.currentPosition[-1][0] = positions[3][1]
        self.robot.currentPosition[-1][1] = positions[3][0]
        self.robot.currentPosition[-1][2] = positions[3][2]

        self.robot.currentPosition[-2][0] = positions[2][1]
        self.robot.currentPosition[-2][1] = positions[2][0]
        self.robot.currentPosition[-2][2] = positions[2][2]

        self.robot.currentPosition[-3][0] = positions[1][1]
        self.robot.currentPosition[-3][1] = positions[1][0]
        self.robot.currentPosition[-3][2] = positions[1][2]

        self.robot.currentPosition[-4][0] = positions[0][1]
        self.robot.currentPosition[-4][1] = positions[0][0]
        self.robot.currentPosition[-4][2] = positions[0][2]

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
        return self.robot.com

    def getKappaJoint2(self):
        return self.robot.spring_constants[0]

    def getKappaJoint3(self):
        return self.robot.spring_constants[1]

    def getKappaJoint4(self):
        return self.robot.spring_constants[2]
