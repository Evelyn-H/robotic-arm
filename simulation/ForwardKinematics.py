from math import cos, sin
import numpy as np


class ForwardKinematics(object):
    # theta, d, r, a: lists
    # actuator: numpy array

    def __init__(self, theta, d, r, a, actuators, ee_center_of_mass):
        self.theta_add = theta
        self.d = d
        self.r = r
        self.a = a
        self.actuator = actuators
        self.COM = ee_center_of_mass

    def move(self, theta):
        # print("Angles set to: " + " ".join(str(theta[x]) for x in range(len(theta))))
        matrices = [ForwardKinematics.dh_matrix(theta[x] + self.theta_add[x], self.a[x], self.d[x], self.r[x])
                    for x in range(len(theta))]


        resultEE = matrices[3].dot(self.actuator[3])
        resultEE = matrices[2].dot(resultEE)
        resultEE = matrices[1].dot(resultEE)
        resultEE = matrices[0].dot(resultEE)

        resultCOM = matrices[3].dot(self.COM)
        resultCOM = matrices[2].dot(resultCOM)
        resultCOM = matrices[1].dot(resultCOM)
        resultCOM = matrices[0].dot(resultCOM)

        resultJ4 = matrices[2].dot(self.actuator[2])
        resultJ4 = matrices[1].dot(resultJ4)
        resultJ4 = matrices[0].dot(resultJ4)

        resultJ3 = matrices[1].dot(self.actuator[1])
        resultJ3 = matrices[0].dot(resultJ3)

        resultJ2 = matrices[0].dot(self.actuator[0])

        return resultJ2, resultJ3, resultJ4, resultEE, resultCOM

    @staticmethod
    def dh_matrix(theta, alpha, d, r):
        return np.array([
            [cos(theta), -sin(theta)*cos(alpha), sin(theta)*sin(alpha), r*cos(theta)],
            [sin(theta), cos(theta)*cos(alpha), -cos(theta)*sin(alpha), r*sin(theta)],
            [0, sin(alpha), cos(alpha), d],
            [0, 0, 0, 1]
        ])