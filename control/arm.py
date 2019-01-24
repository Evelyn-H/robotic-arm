import math
import time
import numpy as np

import clib
import kinematics.solver as solver


class Arm:
    def __init__(self, device, baud_rate=19200):
        self._serial = clib.Arm(device, baud_rate)
        self._ik = solver.Solver(*solver.robot_params)
        # move to start position
        self._pos = [0, 0, 0]
        self._pen_up = True
        self._move_to_position(self._pos, duration=1000)

    @staticmethod
    def h_for_pos(pos):
        dist = math.sqrt((pos[0] + 20) ** 2 + pos[1] ** 2)
        slope = -4
        offset = 1
        h = (slope / 20) * (dist - 10) + offset
        return h  # + 4 * pen_up

    def _move_to_position(self, target, duration=1000):
        angles, _ = self._ik.find_angles(target)
        # print(target, duration)
        if not angles:
            raise solver.NotReachable('Can\'t reach this point')
            # print('no solution found')
            return

        angles = [
            angles[0],
            -angles[1],
            -angles[2],
            -angles[3],
        ]

        angles[1] -= 10 * self._pen_up
        angles[3] -= 5 * self._pen_up

        self._serial.move_to(angles[0], angles[1], angles[2], angles[3], duration)
        while self._serial.is_done() < 0.8:
            time.sleep(10 / 1000)
        self._pos = target

    def _move_line(self, start, end, speed=1, step_size=0.5):
        '''start and end are the (x, y, z) position of the pen'''
        start = np.array(start)
        end = np.array(end)
        path_len = np.linalg.norm(start - end)
        time = path_len / speed * 1000
        steps = max(2, int(round(path_len / step_size)))

        interp_points = np.array([
            np.linspace(start[0], end[0], steps),
            np.linspace(start[1], end[1], steps),
            np.linspace(start[2], end[2], steps)
        ])
        for i in range(steps):
            self._move_to_position(interp_points[:, i], time / steps)

    def move_away(self):
        self._serial.move_to(0, 0, 0, 0, 2000)
        while self._serial.is_done() < 0.9:
            time.sleep(10 / 1000)

    def move_back(self):
        self._serial.move_to(0, 0, 90, -20, 2000)
        while self._serial.is_done() < 0.9:
            time.sleep(10 / 1000)
        self._pos = [0, 0, 0]
        self._pen_up = True
        self._move_to_position(self._pos, duration=1000)
        time.sleep(0.5)

    def move_to(self, target, speed=1, auto_height=True):
        if auto_height:
            target_h = self.h_for_pos(target)
        else:
            target_h = target[2]

        start = [self._pos[0], self._pos[1], self._pos[2]]
        target = [target[0], target[1], target_h]
        self._move_line(start, target, speed)

    def up(self):
        if self._pen_up:
            return
        self._pen_up = True
        self._move_to_position(self._pos, duration=1000)
        time.sleep(0.5)

    def down(self):
        if not self._pen_up:
            return
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

# import math
# import time
# import threading
# import queue
#
# import numpy as np
#
# import clib
# import kinematics.solver as solver
#
#
# # small debugging utility (Print And Return)
# def par(arg):
#     print(arg)
#     return arg
#
#
# class Arm:
#     def __init__(self, device, baud_rate=19200):
#         self._serial = clib.Arm(device, baud_rate)
#         self._thread_lock = threading.RLock()
#         self._thread_queue = queue.Queue()
#         self._thread = threading.Thread(target=self._thread_loop, args=(self._thread_queue,))
#         self._thread.daemon = True
#         self._thread.start()
#
#         self._ik = solver.Solver(*solver.robot_params)
#         # move to start position
#         # self._pos = [0, 0, 0]
#         self._pen_up = True
#         # self._move_to_position(np.array([0, 0, 0]), duration=1000)
#         self._thread_queue.put((np.array([0, 0, 4]), 1000))
#         self._thread_queue.join()
#         time.sleep(1)
#
#     @property
#     def _pos(self):
#         """Getter for the current position"""
#         with self._thread_lock:
#             angles = self._serial.get_all_angles()
#         angles = [
#             angles[0],
#             -angles[1],
#             -angles[2],
#             -angles[3],
#         ]
#
#         # angles[1] -= 10 * self._pen_up
#         # angles[3] -= 5 * self._pen_up
#
#         t = self._ik.move(angles)
#         t[2] = Arm.h_for_pos(par(t[0:2])) + 6 * self._pen_up
#         # print(angles, t)
#         return t
#
#     @staticmethod
#     def h_for_pos(pos):
#         dist = math.sqrt((pos[0] + 20) ** 2 + pos[1] ** 2)
#         slope = -4
#         offset = 1
#         h = (slope / 20) * (dist - 10) + offset
#         return h  # + 4 * pen_up
#
#     def _thread_loop(self, q):
#         while True:
#             with self._thread_lock:
#                 try:
#                     (target, t) = par(q.get(block=False))
#
#                     self._move_to_position(target, t, blocking_constant=0.5)
#                     q.task_done()
#                 except queue.Empty as e:
#                     pass
#             time.sleep(0)
#
#     def _move_to_position(self, target, duration=1000, blocking_constant=0.5):
#         with self._thread_lock:
#
#             angles, _ = self._ik.find_angles(target)
#             angles = [
#                 angles[0],
#                 -angles[1],
#                 -angles[2],
#                 -angles[3],
#             ]
#             if not angles:
#                 raise solver.NotReachable('Can\'t reach this point')
#                 # print('no solution found')
#                 return
#
#             # angles[1] -= 10 * self._pen_up
#             # angles[3] -= 5 * self._pen_up
#
#             self._serial.move_to(angles[0], angles[1], angles[2], angles[3], duration)
#             while self._serial.is_done() < blocking_constant:
#                 time.sleep(10 / 1000)
#
#     def clear_move_queue(self):
#         with self._thread_lock:
#             while True:
#                 try:
#                     self._thread_queue.get(block=False)
#                 except Exception as e:
#                     break
#
#     def move_away(self):
#         with self._thread_lock:
#             self.clear_move_queue()
#             self._serial.move_to(0, 0, 0, 0, 2000)
#             while self._serial.is_done() < 0.9:
#                 time.sleep(10 / 1000)
#
#     def move_back(self):
#         with self._thread_lock:
#             self.clear_move_queue()
#             self._serial.move_to(0, 0, 90, -20, 2000)
#             while self._serial.is_done() < 0.9:
#                 time.sleep(10 / 1000)
#
#
#     def _move_line(self, start, end, speed=1, step_size=0.5, blocking=True):
#         '''start and end are the (x, y, z) position of the pen'''
#         start = np.array(start)
#         end = np.array(end)
#         path_len = np.linalg.norm(start - end)
#         t = path_len / speed * 1000
#         steps = max(2, int(round(path_len / step_size)))
#
#         interp_points = np.array([
#             np.linspace(start[0], end[0], steps),
#             np.linspace(start[1], end[1], steps),
#             np.linspace(start[2], end[2], steps)
#         ])
#
#         with self._thread_lock:
#             for i in range(steps):
#                 self._thread_queue.put(
#                     (interp_points[:, i], t / steps)
#                 )
#                 # self._move_to_position(interp_points[:, i], t / steps)
#         while blocking and self._thread_queue.qsize() > 0:
#             time.sleep(1 / 1000)
#         # print('returned')
#
#     def move_to(self, target, speed=1, blocking=True, auto_height=True):
#         if blocking:
#             self._thread_queue.join()
#         if auto_height:
#             target_h = self.h_for_pos(target) + 6 * self._pen_up
#         else:
#             target_h = target[2]
#
#         current_pos = self._pos
#         start = [current_pos[0], current_pos[1], current_pos[2]]
#         target = [target[0], target[1], target_h]
#         self._move_line(start, target, speed, blocking)
#
#     def up(self):
#         if not self._pen_up:
#             self._thread_queue.join()
#             self._pen_up = True
#             print('up')
#             # self._move_to_position(self._pos, duration=1000, blocking_constant=1.0)
#             self._thread_queue.put((self._pos, 1000))
#             self._thread_queue.join()
#             # pos = self._pos
#             # self._move_line(pos, pos, speed=0.2, blocking=True)
#             print('/up')
#             time.sleep(2)
#
#     def down(self):
#         if self._pen_up:
#             self._thread_queue.join()
#             self._pen_up = False
#             print('down')
#             # self._move_to_position(self._pos, duration=1000, blocking_constant=1.0)
#             self._thread_queue.put((self._pos, 1000))
#             self._thread_queue.join()
#
#             # pos = self._pos
#             # self._move_line(pos, pos, speed=0.2, blocking=True)
#             print('/down')
#             time.sleep(2)
#
#     def line(self, start, end, speed=1):
#         self.up()
#         self.move_to(start, speed=speed)
#         # time.sleep(0.5)
#         self.down()
#         self.move_to(end, speed=speed)
#         # time.sleep(0.5)
#         self.up()
