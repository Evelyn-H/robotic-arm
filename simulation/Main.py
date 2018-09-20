from math import pi
from ForwardKinamatics import ForwardKinematics
import numpy as np
# from InverseKinematicsNN import KerasNet
import os
#os.environ['PYTHONHASHSEED'] = '0'
from fabrik import fabrik3d
from fabrik import fabrik_rotation

np.random.seed(535)
# Creates a forward kinematics solver with the following parameters:
# theta0 = 0, theta1 = 1/2 pi, theta2 = 0, theta3 = 0
# d0 = 10.7, d1 = 0, d2 = 0, d3 = 0
# r0 = 0, r1 = 10.4, r2 = 12.9, r3 = 0
# alpha0 = 1/2 pi, alpha1 = 0, alpha2 = 0, alpha3 = 1/2 pi
# actuator position = [0, 0, 1]
#
# All parameters are based on the Denavit-Hartenberg convention.
# Schematics can be found in the repository. (NOT YET)
fk = ForwardKinematics([0, 0.5*pi, 0, 0],
                       [10.7, 0, 0, 0],
                       [0, 10.4, 12.8, 0],
                       [0.5*pi, 0, 0, 0.5*pi],
                       np.array([0, 0, 0, 1]))

angles = fabrik3d(np.array([[0, 0, 10.7],
                              [0, 0, 21.1],
                              [0, 0, 33.9],
                              [0, 0, 0.001]]), np.array([5,8,23]), [10.4, 12.8, 0.001])

angles2 = fabrik_rotation(np.array([[0, 0, 10.7],
                              [0, 0, 21.1],
                              [0, 0, 33.9],
                              [0, 0, 0.001]]), np.array([5,5,23]), [10.4, 12.8, 0.001])

#print(new_joints)
#net = KerasNet()
#net.run(fk)
# result = net.predict(fk)
fk.move([-angles[0], -angles[1], angles[2], angles[3]])
