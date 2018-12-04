import itertools
import math
import numpy as np

from arm import Arm


def drawFromFile(arm):
    f = open("currentDrawing.txt", 'r')
    armUp = False
    for line in f:
        if line == "NEWLINE\n":
            arm.up()
            armUp = True
        else:
            x, y = line.split()
            arm.move_to([float(y), float(x)], speed=1)

            if (armUp):
                arm.down()
                armUp = False

    f.close()


if __name__ == '__main__':
    arm = Arm('/dev/ttyACM1')

    # import collections
    # import time
    #
    # import vision
    #
    # v = vision.Vision()
    # q_len = 4
    # q = collections.deque(maxlen=q_len)
    #
    # import pid
    # controller = pid.PID(0.5, 0, 0)
    # target_h = 2
    #
    # arm.down()
    #
    # t0 = time.time()
    # while True:
    #     t = time.time()
    #     dt = t - t0
    #     t0 = t
    #
    #     for _ in range(q_len):
    #         h = v.get_pen_height() / 10  # mm to cm
    #         q.append(h if h else 0)
    #     current = sum(q) / q_len
    #
    #     print("dt ", dt)
    #     power = controller.update(target_h, current, max(0.1, dt))
    #
    #     # target = np.array(arm._pos) + np.array([0, 0, power])
    #     # arm._move_to_position(target, duration=dt)
    #
    #     pos = np.array(arm._pos)
    #     target_pos = pos + np.array([0, 0, max(-1, min(1, power))])
    #     # print(pos, target_pos)
    #     arm._move_line(pos, target_pos, speed=power*10, step_size=0.5)

        # target_h += dt * 0.5

    # circle
    print('circle')
    arm.up()
    r = 5
    x0 = 0
    arm.move_to([x0, r], speed=2)
    arm.down()
    for theta in np.linspace(0, 4 * math.pi, 40):
        x = math.sin(theta) * r + x0
        y = math.cos(theta) * r
        arm.move_to([x, y], speed=2)

    # grid
    # size = 8
    # horizontal = (([x, -5], [x, 5]) for x in np.linspace(-5, 5, size + 1))
    # vertical = (([-5, y], [5, y]) for y in np.linspace(-5, 5, size + 1))
    #
    # for start, end in itertools.chain(*zip(horizontal, vertical)):
    #     arm.line(start, end, speed=3)

    # drawFromFile(arm)

    # and move back up
    # arm.up()


    # vision test
    # import collections
    # import vision
    #
    # v = vision.Vision()
    # q = collections.deque(maxlen=4)
    #
    # while True:
    #     h = v.get_pen_height()
    #     q.append(h if h else 0)
    #     print(sum(q) / 4)
