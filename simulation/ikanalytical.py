import numpy
import math
from math import cos, sin, atan2


def ik(target, d, phi):
    # the orientation of the end effector
    phi = math.radians(phi)

    # angle the base has to have to face the target
    baseangle = get_base_angle(target)

    # whether the target is behind or in front of the arm
    sign = numpy.sign(target[1])

    ###
    # HOTFIX FOR BUG
    ###
    print(target[2])
    print(target[2]+sign*10.9)
    target[2] = target[2]+sign*10.9
    print(sign*10.9)
    print(target[2])


    # rotation matrix to rotate the target onto the y-z-plane
    rotmat = numpy.array([[math.cos(baseangle), -math.sin(baseangle), 0], [math.sin(baseangle), math.cos(baseangle), 0],
                          [0, 0, 1]])

    rotated_target = numpy.dot(rotmat, target)
    # Tries out different EE-orientations and calculates a solution
    found_solution = False
    while not found_solution:
        try:
            # ignores the x-component since the target is rotated onto the y-z-plane
            angles = get_angles((rotated_target[0], rotated_target[2]), d, phi)
            print("Found two solutions for phi = " + str(math.degrees(phi)) + ".\n")
            found_solution = True
        except ValueError as e:
            if phi >= math.radians(20):
                print("No solution possible.")
                return None
            phi = phi + math.radians(1)
            print("Could not find a solution for phi = " + str(math.degrees(phi)-1)
                  + ". Trying phi = " + str(math.degrees(phi)) + " now.")

    solution = [[baseangle, a[0], a[1], a[2], sign] for a in angles]
    return solution

def get_angles(target, d, phi):
    px, py = target

    wx = px - d[2] * cos(phi)
    wy = py - d[2] * sin(phi)

    delta = (wx**2) + (wy**2)

    c2 = (delta - d[0]**2 - d[1]**2) / (2*d[0]*d[1])

    s2 = [-math.sqrt(1-c2**2), math.sqrt(1-c2**2)]

    theta2 = [atan2(x, c2) for x in s2]

    s1 = [((d[0] + d[1]*c2) * wy - d[1] * var * wx) / delta for var in s2]

    c1 = [((d[0] + d[1]*c2) * wx + d[1] * var * wy) / delta for var in s2]

    theta1 = [atan2(x, y) for x, y in zip(s1, c1)]

    all_angles = [[th1, th2, phi-th2-th1] for th1, th2 in zip(theta1, theta2)]

    return all_angles

def get_base_angle(target):
    b = numpy.array([1,0])
    t = target[0:2]

    dn = numpy.dot(t, b)
    n = numpy.linalg.norm(t) * numpy.linalg.norm(b)
    res = math.acos((dn / n))

    if numpy.min(t) < 0:
        return res
    else:
        return -res
