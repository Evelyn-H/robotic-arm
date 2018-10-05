from math import radians, degrees
import numpy as np

import clib
import iksolver
import fabrik

# arm = clib.Arm('/dev/ttyACM0', 9600)
ik = iksolver.IKSolver([11.9, 10.5, 11.5], [[-45, 45], [-80, 80], [-90, 90]], [8.6, 9], 0, 180, 50)


# ik_fabrik = fabrik.IKSolver([11.9, 10.5, 11.5], [[-90, 90], [-80, 80], [-90, 90]], [8.6, 9])
# target = [15, 0, 2]
# angles = ik_fabrik.find_angles(target)

def move_to(target, duration=1000):
    solutions = ik.find_angles(target)
    if len(solutions) < 1:
        raise iksolver.NotReachable('nope')
    elif len(solutions) > 1:
        angles = solutions[1]
    else:
        angles = solutions[0]
    arm.move_to(angles[0], angles[1], angles[2], angles[3], duration)


def move_interpolated(start, end, duration=1000, steps=10):
    start = np.transpose(np.array(start))
    end = np.transpose(np.array(end))
    interp_points = np.array([np.linspace(start[0], end[0], steps), np.linspace(start[1], end[1], steps), np.linspace(start[2], end[2], steps)])

    for i in range(steps):
        print(interp_points[:, i])
        move_to(interp_points[:, i], duration / steps)

h = 0

move_to([15, 0, h])
# move_to(10, -10)

# while True:
#     move_interpolated([15, 5, h], [15, -5, h], 5000, 50)
#     move_interpolated([15, -5, h], [30, -5, h+2], 5000, 50)
#     move_interpolated([30, -5, h+2], [30, 5, h+2], 5000, 50)
#     move_interpolated([30, 5, h+2], [15, 5, h], 5000, 50)
