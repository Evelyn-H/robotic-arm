import itertools
import math
import numpy as np
from math import cos, sin, pi


ee_dims = [8.6, 9]
robot_params = ([11.9, 10.5, math.sqrt(ee_dims[0]**2 + ee_dims[1]**2)], [[-60, 60], [-90, 90], [-90, 90]], ee_dims, 20, -45, 45, 50)

class JointConstraintsViolated(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class NotReachable(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class Solver(object):

    def __init__(self, links, joint_constraints, effector_dims, distance_from_page, min_phi, max_phi, phi_steps):
        '''
            Keyword arguments:
            links = The lengths of the robot links (1x3 vector)
            joint_constraints = The minimal and maximal angle each joint can have (3x2 vector)
            effector_dims = The size of the end effector ([x, y] vector)
            distance_from_page = distance between the center of the page and the position of the robot
            min_phi = The minimal allowable end effector orientation angle
            max_phi = The maximal allowable end effector orientation angle
            phi_increments = The increments by which the end effector orientation will be increased during search, from
            min_phi to max_phi
        '''

        self.links = links
        self.joint_constraints = joint_constraints
        self.effector_dims = effector_dims
        self.distance_from_page = distance_from_page
        self.min_phi = math.radians(min_phi)
        self.max_phi = math.radians(max_phi)
        self.ee_angle = math.atan(effector_dims[1] / effector_dims[0])
        self.base = np.array([1, 0])
        self.phi_steps = phi_steps

        self.joint_constraints[2][0] -= self.ee_angle
        self.joint_constraints[2][1] -= self.ee_angle

        for i, _ in enumerate(self.joint_constraints):
            self.joint_constraints[i][0] = math.radians(self.joint_constraints[i][0])
            self.joint_constraints[i][1] = math.radians(self.joint_constraints[i][1])


        # FK

        self.theta_add = [0, 0.5 * pi, 0, 0]
        self.d = [links[0], 0, 0, 0]
        self.r = [0, links[1], links[2], effector_dims[0]]
        self.a = [0.5 * pi, 0, 0, 0.5 * pi]
        self.actuator = np.array([
                           [0, 0, 0, 1],
                           [0, 0, 0, 1],
                           [0, 0, 0, 1],
                           [0, 0, effector_dims[1], 1]
                       ])


    def find_angles(self, target):
        """Takes a x-y-z target array and returns a vector of solutions (at most two)."""
        # convert to coordinates with (0,0) being the base of the robot instead of the centre of the page
        target = target.copy()
        target[0] += self.distance_from_page
        # angle the base has to have to face the target
        base_angle = angle_between_vectors(target[0:2], np.array([1, 0]))

        # rotation the target onto the xz plane
        target_x = math.sqrt(target[0]**2 + target[1]**2)
        rotated_target = np.array([target_x, target[2]])

        def phi_middle_out(min, max, steps):
            mid = (min + max) / 2
            positive = np.linspace(mid, max, steps // 2)
            negative = np.linspace(mid, min, steps // 2)
            return itertools.chain(*itertools.zip_longest(positive, negative))

        def phi_positive_half(min, max, steps):
            mid = (min + max) / 2
            return np.linspace(mid, max, steps)

        def phi_negative_half(min, max, steps):
            mid = (min + max) / 2
            return np.linspace(mid, min, steps)

        def phi_negative(min, max, steps):
            return np.linspace(max, min, steps)

        def phi_from_zero(min, max, steps):
            mid = (min + max) / 2
            return itertools.chain(
                np.linspace(mid, min, int(steps / 2)),
                np.linspace(mid, max, int(steps / 2)),
            )

        # Tries out different EE-orientations and calculates a solution
        for phi in phi_from_zero(self.min_phi, self.max_phi, self.phi_steps):
            phi += math.radians(90) - self.ee_angle
            try:
                # ignores the x-component since the target is rotated onto the y-z-plane
                angles = self._ik_solver(rotated_target, phi)

                return ([
                    math.degrees(base_angle),
                    -math.degrees(angles[0]),
                    -math.degrees(angles[1]),
                    -math.degrees(angles[2]),
                ], phi)

            except (JointConstraintsViolated, NotReachable):
                pass
        return None

    def _ik_solver(self, target, phi):
        '''Calculates the solution of an IK problem given the parameters of the robot, the target, and an EE-orientation'''
        px = target[0]
        py = target[1]

        wx = px - self.links[2] * math.cos(phi)
        wy = py + self.links[2] * math.sin(phi)

        # print(f' phi {round(math.degrees(phi),3)} xyz {round(px,3)}, {round(py,3)}, {round(wx,3)}, {round(wy,3)}')

        d = wx ** 2 + wy ** 2

        if math.sqrt(d) > self.links[0] + self.links[1]:
            raise NotReachable("Arm isn't long enough")

        try:
            t2 = -math.acos((d - self.links[0] ** 2 - self.links[1] ** 2) / (2 * self.links[0] * self.links[1]))
            t1 = math.atan(wy / wx) - math.atan((self.links[1] * math.sin(t2)) / (self.links[0] + self.links[1] * math.cos(t2)))
        except ValueError as e:
            raise NotReachable('math error')

        t1 = math.pi / 2 - t1
        t2 = -t2
        t3 = phi + (math.pi / 2 - t1 - t2)
        t3 = t3 - self.ee_angle

        # print(' -- ', np.array([math.degrees(t1), math.degrees(t2), math.degrees(t3)]))

        # check angles for constraint violations
        # theta 1
        if not self.joint_constraints[0][0] < t1 < self.joint_constraints[0][1]:
            raise JointConstraintsViolated("Theta 1 has illegal joint angle values!")
        # theta 2
        if not self.joint_constraints[1][0] < t2 < self.joint_constraints[1][1]:
            raise JointConstraintsViolated("Theta 2 has illegal joint angle values!")
        # theta 3
        if not self.joint_constraints[2][0] < t3 < self.joint_constraints[2][1]:
            raise JointConstraintsViolated("Theta 3 has illegal joint angle values!")

        return [t1, t2, t3]


    def move(self, thetas):
        thetas = [-math.radians(t) for t in thetas]

        # final result
        d = np.array([0.0, 0.0, 0.0])

        # cumulative angles (skipping the base angle)
        thetas[2] += thetas[1]
        thetas[3] += thetas[2]
        # take ee angle into account
        thetas[3] += self.ee_angle

        for i, theta in enumerate(thetas):
            if i == 0:
                # skip the base angle
                continue
            offset = np.array([0.0, 0.0, 0.0])
            offset[0] = math.sin(theta) * self.links[i-1]
            offset[2] = math.cos(theta) * self.links[i-1]
            d += offset

        # and rotate away from the xz plane according to the base angle
        dist = d[0]
        d[0] = math.cos(-thetas[0]) * dist
        d[1] = math.sin(-thetas[0]) * dist

        # coordinate space transformation
        d[0] = d[0] - self.distance_from_page
        return d

    # def move(self, theta, COM=None):
    #     # print("Angles set to: " + " ".join(str(theta[x]) for x in range(len(theta))))
    #     theta = [math.radians(t) for t in theta]
    #
    #     matrices = [self.dh_matrix(theta[x] + self.theta_add[x], self.a[x], self.d[x], self.r[x])
    #                 for x in range(len(theta))]
    #
    #     def change_coordinate_space(target):
    #         return [
    #             target[0] - self.distance_from_page,
    #             target[1],
    #             target[2] - self.links[0],
    #         ]
    #
    #
    #     resultEE = matrices[3].dot(self.actuator[3])
    #     resultEE = matrices[2].dot(resultEE)
    #     resultEE = matrices[1].dot(resultEE)
    #     resultEE = matrices[0].dot(resultEE)
    #
    #     if COM:
    #         resultCOM = matrices[3].dot(COM)
    #         resultCOM = matrices[2].dot(resultCOM)
    #         resultCOM = matrices[1].dot(resultCOM)
    #         resultCOM = matrices[0].dot(resultCOM)
    #
    #
    #         resultJ4 = matrices[2].dot(self.actuator[2])
    #         resultJ4 = matrices[1].dot(resultJ4)
    #         resultJ4 = matrices[0].dot(resultJ4)
    #
    #         resultJ3 = matrices[1].dot(self.actuator[1])
    #         resultJ3 = matrices[0].dot(resultJ3)
    #
    #         resultJ2 = matrices[0].dot(self.actuator[0])
    #
    #         return [change_coordinate_space(t) for t in [resultJ2, resultJ3, resultJ4, resultEE, resultCOM]]
    #     else:
    #         return change_coordinate_space(resultEE)

    def dh_matrix(self, theta, alpha, d, r):
        return np.array([
            [cos(theta), -sin(theta) * cos(alpha), sin(theta) * sin(alpha), r * cos(theta)],
            [sin(theta), cos(theta) * cos(alpha), -cos(theta) * sin(alpha), r * sin(theta)],
            [0, sin(alpha), cos(alpha), d],
            [0, 0, 0, 1]
        ])


def angle_between_vectors(v0, v1):
    a0 = math.atan2(v0[1], v0[0])
    a1 = math.atan2(v1[1], v1[0])
    return a0 - a1
