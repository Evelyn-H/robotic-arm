from math import pi, atan
from ForwardKinamatics import ForwardKinematics
import numpy as np
from ikanalytical import ik


# Creates a forward kinematics solver with the following DH parameters:
# theta0 = 0, theta1 = 1/2 pi, theta2 = 0, theta3 = 0
# d0 = 10.7, d1 = 0, d2 = 0, d3 = 0
# r0 = 0, r1 = 10.4, r2 = 12.9, r3 = 0
# alpha0 = 1/2 pi, alpha1 = 0, alpha2 = 0, alpha3 = 1/2 pi
# actuator position = [0, 0, 5]

target = [12, -5, 0]

LINKS = [10.4, 12.8, 7.887331614684399]
PEN_ANGLE = -atan(5/6.1)
INIT_PHI = -20

fk = ForwardKinematics([0, 0.5*pi, 0, 0],
                       [10.7, 0, 0, 0],
                       [0, 10.4, 12.8, 6.1],
                       [0.5*pi, 0, 0, 0.5*pi],
                       np.array([0, 0, 5, 1]))

angles2 = ik(np.array(np.array(target)), LINKS, PEN_ANGLE+INIT_PHI)

if angles2 == None:
    exit(1)

for solution in angles2:
    print("Possible solution: " +str(solution[0:4]))
    if solution[0] > 0:
        fk.move([solution[4]*solution[0], -(0.5*pi-solution[1]), solution[2], solution[3]-PEN_ANGLE])
    else:
        fk.move([-solution[0], (-0.5 * pi - solution[1]), -solution[2], -solution[3]-PEN_ANGLE])
    print("\n")
