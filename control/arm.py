import math
import time
import threading
import queue

import numpy as np

import clib
from kinematics.solver import Solver


class Arm:
    def __init__(self, device, baud_rate=19200, ik_params=None):
        self._serial = clib.Arm(device, baud_rate)
        self._thread_lock = threading.RLock()
        self._thread_queue = queue.Queue()
        self._thread = threading.Thread(target=self._thread_loop, args=(self._thread_queue,))
        self._thread.start()

        if not ik_params:
            ik_params = [[11.9, 10.5, 11.5], [[-60, 60], [-90, 90], [-90, 90]], [8.6, 9], 20, -45, 45, 50]
        self._ik = Solver(*ik_params)
        # move to start position
        # self._pos = [0, 0, 0]
        self._pen_up = True
        self._move_to_position(self._pos, duration=1000)


    @property
    def _pos(self):
        """Getter for the current position"""
        with self._thread_lock:
            angles = self._serial.get_all_angles()
            print(angles)
        return np.array([0,0,0])#self._ik.forward(angles)

    @staticmethod
    def h_for_pos(pos):
        dist = math.sqrt((pos[0] + 20) ** 2 + pos[1] ** 2)
        slope = -4
        offset = 1
        h = (slope / 20) * (dist - 10) + offset
        return h  # + 4 * pen_up

    def _thread_loop(self, q):
        while True:
            with self._thread_lock:
                try:
                    (target, t) = q.get(block=False)

                    print(target, q.qsize())
                    self._move_to_position(target, t)
                except queue.Empty as e:
                    pass
            time.sleep(0)

    def _move_to_position(self, target, duration=1000):
        with self._thread_lock:

            angles = self._ik.find_angles(target)
            if not angles:
                raise Solver.NotReachable('Can\'t reach this point')
                # print('no solution found')
                return

            angles[1] -= 10 * self._pen_up
            angles[3] -= 5 * self._pen_up

            self._serial.move_to(angles[0], angles[1], angles[2], angles[3], duration)
            while self._serial.is_done() < 0.5:
                time.sleep(10 / 1000)

    def clear_move_queue(self):
        with self._thread_lock:
            while True:
                try:
                    self._thread_queue.get(block=False)
                except Exception as e:
                    break

    def _move_line(self, start, end, speed=1, step_size=0.5, blocking=True):
        '''start and end are the (x, y, z) position of the pen'''
        start = np.array(start)
        end = np.array(end)
        path_len = np.linalg.norm(start - end)
        t = path_len / speed * 1000
        steps = max(2, int(round(path_len / step_size)))

        interp_points = np.array([
            np.linspace(start[0], end[0], steps),
            np.linspace(start[1], end[1], steps),
            np.linspace(start[2], end[2], steps)
        ])

        with self._thread_lock:
            for i in range(steps):
                self._thread_queue.put(
                    (interp_points[:, i], t / steps)
                )
                # self._move_to_position(interp_points[:, i], t / steps)
        # if blocking:
            # self._thread_queue.join()
        while blocking and self._thread_queue.qsize() > 0:
            time.sleep(1 / 1000)
        print('returned')


    def move_to(self, target, speed=1):
        target_h = self.h_for_pos(target)
        current_pos = self._pos
        start = [current_pos[0], current_pos[1], current_pos[2]]
        target = [target[0], target[1], target_h]
        self._move_line(start, target, speed)

    def up(self):
        self._pen_up = True
        self._move_to_position(self._pos, duration=1000)
        time.sleep(0.5)


    def down(self):
        self._pen_up = False
        self._move_to_position(self._pos, duration=1000)
        time.sleep(0.5)


    def line(self, start, end, speed=1):
        self.up()
        self.move_to(start, speed=speed)
        # time.sleep(0.5)
        self.down()
        self.move_to(end, speed=speed)
        # time.sleep(0.5)
        self.up()
