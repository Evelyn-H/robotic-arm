import numpy as np
import clib
from iksolver import IKSolver, NotReachable

arm = clib.Arm('/dev/ttyACM0', 9600)
ik = IKSolver([11.9, 10.5, 15], [[-90, 90], [-90, 90], [-90, 90]], [12.5, 9], -90, 90, 0.1)


def move_to(target, duration=1000):
    solutions = ik.find_angles(target)
    if len(solutions) < 1:
        raise NotReachable('nope')
    angles = solutions[0]
    arm.move_to(angles[0], angles[1], angles[2], angles[3], duration)


def move_interpolated(start, end, duration=1000, steps=10):
    start = np.transpose(np.array(start))
    end = np.transpose(np.array(end))
    interp_points = np.array([np.linspace(start[0], end[0], steps), np.linspace(start[1], end[1], steps), np.linspace(start[2], end[2], steps)])

    for i in range(steps):
        print(interp_points[:, i])
        move_to(interp_points[:, i], duration / steps)


# move_to(10, 10)
# move_to(10, -10)

while True:
    move_interpolated([15, 5, 0], [15, -5, 0], 5000, 50)
    move_interpolated([15, -5, 0], [20, -5, 0], 5000, 50)
    move_interpolated([20, -5, 0], [20, 5, 0], 5000, 50)
    move_interpolated([20, 5, 0], [15, 5, 0], 5000, 50)
