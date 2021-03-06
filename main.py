import itertools
import math
import time
import sys
import numpy as np

from control.arm import Arm
from vision import Vision

# def drawFromFile(arm):
#     f = open("currentDrawing.txt", 'r')
#     armUp = False
#     for line in f:
#         if line == "NEWLINE\n":
#             arm.up()
#             armUp = True
#         else:
#             x, y = line.split()
#             arm.move_to([float(y), float(x)], speed=1)
#
#             if (armUp):
#                 arm.down()
#                 armUp = False
#
#     f.close()


def interactive_shell(arm):
    import vision
    v = None

    while True:
        command = input('arm shell >> ')
        name, *args = command.split(' ')

        try:
            if name == "":
                print('Please enter a command')
            elif name == "move":
                if len(args) == 2:
                    target = np.array([float(args[0]), float(args[1])])
                    arm.move_to(target, speed=3, auto_height=True)
                elif len(args) == 3:
                    target = np.array([float(args[0]), float(args[1]), float(args[2])])
                    arm.move_to(target, speed=3, auto_height=False)

            elif name == "up":
                arm.up()

            elif name == "down":
                arm.down()
            elif name == "height":
                if not v:
                    v = vision.Vision()
                avg_amount = 10
                h_list = (v.get_pen_height() for _ in range(avg_amount))
                h = sum(h_list) / avg_amount
                print('Height:', round(h, 2), 'mm')

        except Exception as e:
            print("Error while processing command")


def main():
    try:
        arm = Arm('/dev/ttyACM0')
    except Exception as e:
        arm = Arm('/dev/ttyACM1')

    if len(sys.argv) > 1 and sys.argv[1] == 'shell':
        interactive_shell(arm)

    if len(sys.argv) > 1 and sys.argv[1] == 'height':
        import collections
        import vision

        v = vision.Vision()
        q = collections.deque(maxlen=4)

        while True:
            h = v.get_pen_height()
            q.append(h if h else 0)
            print(sum(q) / 4)

    # import collections
    # import time
    #
    # v = Vision()
    # q_len = 4
    # q = collections.deque(maxlen=q_len)
    #
    # # while True:
    # #     h = v.get_pen_height()
    # #     print(h)
    #
    # import control.pid
    # controller = control.pid.PID(2, 0, 0)
    # target_h = 4
    #
    # arm.down()
    # arm.move_to([0,0,0])
    #
    # t0 = time.time()
    # while True:
    #     t = time.time()
    #     dt = t - t0
    #     t0 = t
    #
    #     for _ in range(q_len):
    #         h = v.get_pen_height()
    #         if not h:
    #             continue
    #         h = h / 10  # mm to cm
    #         q.append(h if h else 0)
    #     current = sum(q) / q_len
    #
    #     # print("dt ", dt)
    #     power = controller.update(target_h, current, max(0.1, dt))
    #
    #     # target = np.array(arm._pos) + np.array([0, 0, power])
    #     # arm._move_to_position(target, duration=dt)
    #
    #     pos = np.array(arm._pos)
    #     target_pos = pos + np.array([0, 0, max(-1, min(1, power))])
    #     print("{:03.2f}, {:03.2f}, {}, {}".format(h, power, pos, target_pos))
    #     arm.clear_move_queue()
    #     arm._move_line(pos, target_pos, speed=power, step_size=0.1, blocking=False)

        # target_h += dt * 0.5

    # move away and back
    # print('back')
    # arm.move_away()
    # time.sleep(5)
    # arm.move_back()

    # arm.down()
    # arm.move_to([0,0], speed=3)
    # arm.move_to([-11,0], speed=3)

    # circle
    # print('circle')
    # arm.up()
    # r = 5
    # x0 = 0
    # arm.move_to([x0, r], speed=2)
    # arm.down()
    # for theta in np.linspace(0, 4 * math.pi, 40):
    #     x = math.sin(theta) * r + x0
    #     y = math.cos(theta) * r
    #     arm.move_to([x, y], speed=2)

    # grid
    # size = 8
    # horizontal = (([x, -5], [x, 5]) for x in np.linspace(-5, 5, size + 1))
    # vertical = (([-5, y], [5, y]) for y in np.linspace(-5, 5, size + 1))
    #
    # for start, end in itertools.chain(*zip(horizontal, vertical)):
    #     arm.line(start, end, speed=3)
    #
    # # and move back up
    # arm.up()

if __name__ == '__main__':
    main()
