from math import atan, atan2, sin, cos, acos, pi, sqrt, radians, degrees
from numpy import array, dot, min
import numpy as np
from numpy.linalg import norm


class JointConstraintsViolated(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class NotReachable(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class IKSolver(object):

    # our parameters are: __init([11.9, 10.5, 15], [[-90, 90], [-90, 90], [-90, 90]], [12.5, 9], -90, 90, 0.1)
    def __init__(self, links, joint_constraints, effector_dims, min_phi, max_phi, phi_increments):
        '''
            Keyword arguments:
            links = The lengths of the robot links (1x3 vector)
            joint_constraints = The minimal and maximal angle each joint can have (3x2 vector)
            effector_dims = The size of the end effector ([x, y] vector)
            min_phi = The minimal allowable end effector orientation angle
            max_phi = The maximal allowable end effector orientation angle
            phi_increments = The increments by which the end effector orientation will be increased during search, from
            min_phi to max_phi
        '''

        self.links = links
        self.joint_constraints = joint_constraints
        self.effector_dims = effector_dims
        self.min_phi = radians(min_phi)
        self.max_phi = radians(max_phi)
        self.ee_angle = -atan(effector_dims[1]/effector_dims[0])
        self.base = array([1, 0])
        self.phi_increments = radians(phi_increments)

        for i, _ in enumerate(self.joint_constraints):
            self.joint_constraints[i][0] = radians(self.joint_constraints[i][0])
            self.joint_constraints[i][1] = radians(self.joint_constraints[i][1])

    """Takes a x-y-z target array and returns a vector of solutions (at most two)."""
    def find_angles(self, target):
        phi = (self.min_phi + self.max_phi) / 2
        sign = 1

        # calculates the angle by which the target has to be rotated to land on the y-z-plane
        t = target[0:2]
        dn = dot(t, self.base)
        n = norm(t) * norm(self.base)
        res = acos((dn / n))
        if min(t) < 0:
            baseangle = res
        else:
            baseangle = -res

        # rotation matrix to rotate the target onto the y-z-plane
        rotmat = array([[cos(baseangle), -sin(baseangle), 0],
                        [sin(baseangle), cos(baseangle), 0],
                        [0, 0, 1]])

        rotated_target = dot(rotmat, target)

        # Tries out different EE-orientations and calculates a solution, which is then transformed to our angle space
        while True:
            try:
                # ignores the x-component since the target is rotated onto the y-z-plane
                angles = self._ik_solver((rotated_target[0], rotated_target[2]), phi)

                solution = [[degrees(baseangle),
                             degrees(joints[0]),
                             degrees(joints[1]),
                             degrees(joints[2])] for joints in angles]

                print('pre:  \n', np.round(solution, 2))
                transformed = self._transform_angles(solution, phi)
                print('post: \n', np.round(transformed, 2))
                print('phi: ', phi)
                return transformed

            except (JointConstraintsViolated, NotReachable):
                if phi >= self.max_phi:
                    return []
                sign = -1 * sign
                if sign == -1:
                    phi = sign * phi
                else:
                    phi = -1 * phi + self.phi_increments


    '''Calculates the solution of an IK problem given the parameters of the robot, the target, and an EE-orientation'''
    def _ik_solver(self, target, phi):
        px = target[0]
        py = target[1]

        wx = px - self.links[2] * cos(phi)
        wy = py - self.links[2] * sin(phi)

        delta = (wx ** 2) + (wy ** 2)

        t2 = acos((delta - self.links[0] ** 2 - self.links[1] ** 2) / (2 * self.links[0] * self.links[1]))

        t1 = ((-self.links[1] * sin(t2))*wx + (self.links[0] + self.links[1] * cos(t2))*wy) / ((self.links[1] * sin(t2))*wy + (self.links[0] + self.links[1] * cos(t2))*wx)

        t1 = t1 #+ radians(90)
        t2 = t2 #- radians(90)
        print('--', degrees(t1), degrees(t2), degrees(phi))
        # # if 1-c^2 is negative, the target is not reachable with the current robot configuration.
        # try:
        #     s2 = [-sqrt(1 - c2 ** 2), sqrt(1 - c2 ** 2)]
        # except ValueError:
        #     raise NotReachable("The target is not reachable!")
        #
        # theta2_unbounded = [atan2(x, c2) for x in s2]
        # theta2 = [x for x in theta2_unbounded
        #           if self.joint_constraints[1][0] < x < self.joint_constraints[1][1]]
        #
        # # Angles for theta2 exceed joint limits
        # if len(theta2) == 0:
        #     raise JointConstraintsViolated("Theta2 has illegal joint angle values!")
        #
        # s1 = [((self.links[0] + self.links[1] * c2) * wy - self.links[1] * var * wx) / delta for var in s2]
        #
        # c1 = [((self.links[0] + self.links[1] * c2) * wx + self.links[1] * var * wy) / delta for var in s2]
        #
        # theta1_unbounded = [atan2(x, y) for x, y in zip(s1, c1)]
        # theta1 = [x for x in theta1_unbounded
        #           if 2*self.joint_constraints[0][1] > x > 2*self.joint_constraints[0][0]]
        #
        # # Angles for theta1 exceed joint limits
        # if len(theta1) == 0:
        #     raise JointConstraintsViolated("Theta1 has illegal joint angle values!")

        all_angles = [[t1, t2, phi - t2 - t1]]

        # Angles for theta3 exceed joint limits
        if len(all_angles) == 0:
            raise JointConstraintsViolated("Theta3 has illegal joint angle values!")

        return all_angles

    '''Transforms the angle space given by the solver to the angle space used in our robot setup'''
    def _transform_angles(self, angles, ee_phi):
        for solution in angles:
            # the solver considers our two-dimensional end effector as a single link, this corrects the solution

            s = np.sign(cos(ee_phi))
            print(s)
            solution[3] = solution[3] + s*degrees(self.ee_angle)
            solution[1] = solution[1] + s*degrees(0.5 * pi)


            solution[3] = s * solution[3]
            solution[2] = s * solution[2]

            # for i in range(1, len(solution)):
                # solution[i] = -solution[i]

        return angles
