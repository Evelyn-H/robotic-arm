import math
import numpy as np

import clib
import iksolver
import fabrik

arm = clib.Arm('/dev/ttyACM0', 9600)
ik = iksolver.IKSolver([11.9, 10.5, 11.5], [[-60, 60], [-90, 90], [-90, 90]], [8.6, 9], -45, 45, 50)


# ik_fabrik = fabrik.IKSolver([11.9, 10.5, 11.5], [[-90, 90], [-80, 80], [-90, 90]], [8.6, 9])
# target = [15, 0, 2]
# angles = ik_fabrik.find_angles(target)

def move_to(target, duration=1000):
    solutions = ik.find_angles(target)
    if len(solutions) < 1:
        # raise iksolver.NotReachable('nope')
        print('no solution found')
        return
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

def h_for_pos(pos, pen_up=False):
    dist = math.sqrt(pos[0] ** 2 + pos[1] ** 2)
    slope = -3
    offset = 0
    h = (slope / 20) * (dist - 10) + offset
    return h + 3 * pen_up


def draw_line(start, end, pen_up=False, speed=1):
    '''start and end are the (x, y) position of the pen'''
    start_h = h_for_pos(start, pen_up)
    end_h = h_for_pos(end, pen_up)
    path_len = math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)
    time = path_len * 500 / speed
    steps = round(path_len * 2)
    move_interpolated([start[0], start[1], start_h], [end[0], end[1], end_h], time, steps)

# move_to([15, 0, h])
# move_to(10, -10)


draw_line([15, -1.5], [24, -1.5], pen_up=False)
draw_line([24, -1.5], [15,  1.5], pen_up=True, speed=2)
draw_line([15,  1.5], [24,  1.5], pen_up=False)
draw_line([24,  1.5], [18, -4.5], pen_up=True, speed=2)
draw_line([18, -4.5], [18,  4.5], pen_up=False)
draw_line([18,  4.5], [21, -4.5], pen_up=True, speed=2)
draw_line([21, -4.5], [21,  4.5], pen_up=False)
draw_line([21,  4.5], [15, -1.5], pen_up=True, speed=2)



# h = 0

# x1 = 20
# x2 = 25
# y1 = 5
# y2 = -5

# while True:
#     draw_line([x1, y1], [x1, y2], pen_up=False)
#     # draw_line([x1, y2], [x1, y1], pen_up=False)
#     draw_line([x1, y2], [x2, y2], pen_up=False)
#     draw_line([x2, y2], [x2, y1], pen_up=False)
#     draw_line([x2, y1], [x1, y1], pen_up=False)
