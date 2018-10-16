import math
import itertools
import time
import numpy as np

import clib
import iksolver

class Arm:
    def __init__(self, device, baud_rate=19200, ik_params=None):
        self._serial = clib.Arm(device, baud_rate)
        if not ik_params:
            ik_params =[[11.9, 10.5, 11.5], [[-60, 60], [-90, 90], [-90, 90]], [8.6, 9], 20, -45, 45, 50]
        self._ik = iksolver.IKSolver(*ik_params)
        # move to start position
        self._pos = [0, 0, 0]
        self._pen_up = True
        self._move_to_position(self._pos, duration=1000)

    @staticmethod
    def h_for_pos(pos, pen_up=False):
        dist = math.sqrt((pos[0]+20) ** 2 + pos[1] ** 2)
        slope = -4
        offset = 1
        h = (slope / 20) * (dist - 10) + offset
        return h# + 4 * pen_up


    def _move_to_position(self, target, duration=1000):
        angles = self._ik.find_angles(target)
        if not angles:
            raise iksolver.NotReachable('Can\'t reach this point')
            # print('no solution found')
            return

        angles[1] -= 10 * self._pen_up
        angles[3] -= 5 * self._pen_up

        self._serial.move_to(angles[0], angles[1], angles[2], angles[3], duration)
        self._pos = target

    def _move_line(self, start, end, speed=1):
        '''start and end are the (x, y, z) position of the pen'''
        start = np.array(start)
        end = np.array(end)
        path_len = np.linalg.norm(start - end)
        time = path_len * 500 / speed
        steps = max(3, int(round(path_len * 2)))

        interp_points = np.array([
            np.linspace(start[0], end[0], steps),
            np.linspace(start[1], end[1], steps),
            np.linspace(start[2], end[2], steps)
        ])
        for i in range(steps):
            self._move_to_position(interp_points[:, i], time / steps)

    def move_to(self, target, speed=1):
        target_h = self.h_for_pos(target, self._pen_up)
        start = [self._pos[0], self._pos[1], self._pos[2]]
        target = [target[0], target[1], target_h]
        self._move_line(start, target, speed)

    def up(self):
        self._pen_up = True
        self._move_to_position(self._pos, duration=500)

    def down(self):
        self._pen_up = False
        self._move_to_position(self._pos, duration=1000)

    def line(self, start, end, speed=1):
        self.up()
        self.move_to(start, speed=speed); time.sleep(0.5)
        self.down();
        self.move_to(end, speed=speed); time.sleep(0.5)
        self.up()


if __name__ == '__main__':
    arm = Arm('/dev/ttyACM0')

    # circle
    # arm.up()
    # r = 5
    # x0 = 0
    # arm.move_to([x0, r])
    # arm.down()
    # for theta in np.linspace(0, 4 * math.pi, 40):
    #     x = math.sin(theta) * r + x0
    #     y = math.cos(theta) * r
    #     arm.move_to([x, y], speed=1)

    # grid

    size = 8
    horizontal = (([x, -5], [x, 5]) for x in np.linspace(-5, 5, size + 1))
    vertical = (([-5, y], [5, y]) for y in np.linspace(-5, 5, size + 1))

    for start, end in itertools.chain(*zip(horizontal, vertical)):
        arm.line(start, end, speed=3)

    # and move back up
    arm.up()
