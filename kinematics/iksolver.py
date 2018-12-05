import itertools
import math
import numpy as np


class JointConstraintsViolated(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class NotReachable(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class IKSolver(object):

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

                return [
                    math.degrees(base_angle),
                    math.degrees(angles[0]),
                    math.degrees(angles[1]),
                    math.degrees(angles[2])
                ]

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


def angle_between_vectors(v0, v1):
    a0 = math.atan2(v0[1], v0[0])
    a1 = math.atan2(v1[1], v1[0])
    return a0 - a1
