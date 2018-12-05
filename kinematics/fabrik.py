import math
import numpy as np

# Tolerance for the final result, unit is centimeters
TOLERANCE = 0.05
# everything is kept pretty verbose on purpose to ease porting the algorithm
# into C++ later on.


class IKSolver(object):
    # our parameters are: __init([11.9, 10.5, 11.5], [[-90, 90], [-90, 90], [-90, 90]], [8.6, 9], -90, 90)
    def __init__(self, links, joint_constraints, effector_dims):
        '''
            Keyword arguments:
            links = The lengths of the robot links (1x3 vector)
            joint_constraints = The minimal and maximal angle each joint can have (3x2 vector)
            effector_dims = The size of the end effector ([x, y] vector)
        '''
        self.links = links
        self.joint_constraints = joint_constraints
        self.effector_dims = effector_dims
        self.ee_angle = math.atan(effector_dims[1] / effector_dims[0])

        for constraint in self.joint_constraints:
            constraint[0] = math.radians(constraint[0])
            constraint[1] = math.radians(constraint[1])

    def find_angles(self, target):
        '''Takes a x-y-z target array and returns a solution'''
        # wrangle the data into the right input for FABRIK

        # angle the base has to have to face the target
        base_angle = angle_between_vectors(target[0:2], np.array([1, 0]))

        # rotation matrix to rotate the target onto the x-z-plane
        target_x = math.sqrt(target[0]**2 + target[1]**2)
        target_xz = np.array([target_x, target[2]])

        joints = np.array([
            [0, 0],
            [0, self.links[0]],
            [0, self.links[0] + self.links[1]],
            [0, self.links[0] + self.links[1] + self.links[2]],
        ])
        print(joints)

        # applies FABRIK on the 2D-data
        joints = self._get_new_joints2d(joints, target_xz, self.links)
        print(joints)

        angles = [base_angle]
        angles.extend(self._joints_to_angles(joints))
        print(angles)
        print([math.degrees(x) for x in angles])
        return angles

    def _joints_to_angles(self, joints):
        link_vecs = [joints[0]]
        for i in range(1, len(joints)):
            link_vecs.append(joints[i] - joints[i - 1])
        link_vecs[0] = [0, 1]  # replace the first link_vecs ([0, 0]) with the up vector for calculating the angles
        angles = []
        for i in range(len(link_vecs) - 1):
            angles.append(angle_between_vectors(link_vecs[i], link_vecs[i + 1]))
        angles[-1] -= self.ee_angle
        return angles

    def _get_new_joints2d(self, joints, target, d):

        # calculates distance from root to target
        dist = math.sqrt(math.pow(joints[0, 0] - target[0], 2) + math.pow(joints[0, 1] - target[1], 2))

        # columns is number of joints
        num_joints = joints.shape[0]

        # checks if target is reachable
        if dist > sum(d):
            # target is unreachable
            for i in range(num_joints - 1):
                # finds distance between each target and each joint, except the last joint
                r = math.sqrt(math.pow(joints[i, 0] - target[0], 2) + math.pow(joints[i, 1] - target[1], 2))
                kappa = d[i] / r

                # updates joint positions
                joints[i + 1, 0] = (1 - kappa) * joints[i, 0] + kappa * target[0]
                joints[i + 1, 1] = (1 - kappa) * joints[i, 1] + kappa * target[1]
        else:
            # target is reachable
            b = np.zeros((2,))
            b[0] = joints[0, 0]
            b[1] = joints[0, 1]

            # Check whether the distance between end effector and the target is greater
            # than some tolerance

            difA = math.sqrt(math.pow(joints[num_joints - 1, 0] - target[0], 2) + math.pow(joints[num_joints - 1, 1] - target[1], 2))

            num_iterations = 0
            while difA > TOLERANCE and num_iterations < 10:
                num_iterations += 1
                # STAGE 1: FORWARD REACHING
                # Set the end effector as target t
                joints[num_joints - 1, 0] = target[0]
                joints[num_joints - 1, 1] = target[1]

                for i in reversed(range(num_joints - 1)):
                    # finds distances between the new joint positions of the next joint
                    # and the current position of the lower joint
                    r = math.sqrt(math.pow(joints[i, 0] - joints[i + 1, 0], 2) + math.pow(joints[i, 1] - joints[i + 1, 1], 2))

                    kappa = d[i] / r

                    # updates joint positions
                    joints[i, 0] = (1 - kappa) * joints[i + 1, 0] + kappa * joints[i, 0]
                    joints[i, 1] = (1 - kappa) * joints[i + 1, 1] + kappa * joints[i, 1]

                # STAGE 2: BACKWARD REACHING
                # Set the root as the initial position

                joints[0, 0] = b[0]
                joints[0, 1] = b[1]

                for i in range(num_joints - 1):
                    # finds distances between the new joint positions of the next joint
                    # and the current position of the lower joint
                    r = math.sqrt(math.pow(joints[i, 0] - joints[i + 1, 0], 2) + math.pow(joints[i, 1] - joints[i + 1, 1], 2))

                    kappa = d[i] / r

                    joints[i + 1, 0] = (1 - kappa) * joints[i, 0] + kappa * joints[i + 1, 0]
                    joints[i + 1, 1] = (1 - kappa) * joints[i, 1] + kappa * joints[i + 1, 1]

                    # check angle constraints
                    # angles = self._joints_to_angles(joints)
                    # print('pre:  ', [math.degrees(x) for x in angles])
                    # if angles[i] < math.radians(-45):
                    #     # set position to min allowed angle
                    #     angle_diff = -math.radians(-45) + angles[i]
                    #     print('< -45', i, math.degrees(angle_diff))
                    #     # rotate
                    #     joints[i + 1, 0] = math.cos(angle_diff) * (joints[i + 1, 0] - joints[i, 0]) - math.sin(angle_diff) * (joints[i + 1, 1] - joints[i, 1]) + joints[i, 0]
                    #     joints[i + 1, 1] = math.sin(angle_diff) * (joints[i + 1, 0] - joints[i, 0]) + math.cos(angle_diff) * (joints[i + 1, 1] - joints[i, 1]) + joints[i, 1]
                    #
                    #     print('post: ', [math.degrees(x) for x in self._joints_to_angles(joints)])
                    # elif angles[i] > math.radians(45):
                    #     # set position to min allowed angle
                    #     angle_diff = -math.radians(45) + angles[i]
                    #     print('> 45', i, math.degrees(angle_diff))
                    #     # rotate
                    #     joints[i + 1, 0] = math.cos(angle_diff) * (joints[i + 1, 0] - joints[i, 0]) - math.sin(angle_diff) * (joints[i + 1, 1] - joints[i, 1]) + joints[i, 0]
                    #     joints[i + 1, 1] = math.sin(angle_diff) * (joints[i + 1, 0] - joints[i, 0]) + math.cos(angle_diff) * (joints[i + 1, 1] - joints[i, 1]) + joints[i, 1]
                    #
                    #     print('post: ', [math.degrees(x) for x in self._joints_to_angles(joints)])

                difA = math.sqrt(math.pow(joints[num_joints - 1, 0] - target[0], 2) + math.pow(joints[num_joints - 1, 1] - target[1], 2))

                # # check if any constraints are violated
                # angles = self._joints_to_angles(joints)
                # for i in range(len(angles)):
                #     # lower limit
                #     if angles[i] < self.joint_constraints[i][0]:
                #         angles[i] = self.joint_constraints[i][0]
                #     # upper limit
                #     if angles[i] > self.joint_constraints[i][1]:
                #         angles[i] = self.joint_constraints[i][1]
                #
                # # and rebuild joints from (new) angles
                # ...


        return joints


def rotation_matrix(theta):
    return np.array([
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta), math.cos(theta), 0],
        [0, 0, 1]
    ])


# calculates an angle between two vectors
def angle_between_vectors(v0, v1):
    # dn = np.dot(v1, v2)
    # n = np.linalg.norm(v1) * np.linalg.norm(v2)
    # return math.acos(dn / n)
    a0 = math.atan2(v0[1], v0[0])
    a1 = math.atan2(v1[1], v1[0])
    return a0 - a1
