from math import cos, sin
import numpy as np


class ForwardKinematics(object):
    # theta, d, r, a: lists
    # actuator: numpy array

    def __init__(self, theta, d, r, a, actuator):
        self.theta_add = theta
        self.d = d
        self.r = r
        self.a = a
        self.actuator = actuator

    def move(self, theta):
        print("Angles set to: " +" ".join(str(theta[x]) for x in range(len(theta))))
        matrices =[ForwardKinematics.dh_matrix(theta[x] + self.theta_add[x], self.a[x], self.d[x], self.r[x]) for x in range(len(theta))]

        result = matrices[-1].dot(self.actuator)
        result = matrices[-2].dot(result)
        result = matrices[-3].dot(result)
        result = matrices[-4].dot(result)

        print("Result: " + str(result))
        return result

    def get_actuator(self):
        return self.actuator

    @staticmethod
    def dh_matrix(theta, alpha, d, r):
        return np.array([[cos(theta), -sin(theta)*cos(alpha), sin(theta)*sin(alpha), r*cos(theta)],
                            [sin(theta), cos(theta)*cos(alpha), -cos(theta)*sin(alpha), r*sin(theta)],
                            [0, sin(alpha), cos(alpha), d],
                            [0, 0, 0, 1]])