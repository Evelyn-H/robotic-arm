import math
import numpy

# Tolerance for the final result, unit is centimeters
TOLERANCE = 0.05
# everything is kept pretty verbose on purpose to ease porting the algorithm
# into C++ later on.


def get_new_joints2d(joints, target, d):

    # calculates distance from root to target
    dist = math.sqrt(math.pow(joints[0,0]-target[0],2)
               + math.pow(joints[0,1]-target[1],2))

    # columns is number of joints
    num_joints = joints.shape[0]

    # checks if target is reachable
    if dist > sum(d):
        # target is unreachable
        for i in range(num_joints-1):
            # finds distance between each target and each joint, except the last joint
            r = math.sqrt(math.pow(joints[i,0]-target[0],2)
               + math.pow(joints[i,1]-target[1],2))
            kappa = d[i] / r

            #updates joint positions
            joints[i+1,0] = (1-kappa)*joints[i,0]+kappa*target[0]
            joints[i+1,1] = (1-kappa)*joints[i,1]+kappa*target[1]
    else:
        # target is reachable
        b = numpy.zeros((2,))
        b[0] = joints[0,0]
        b[1] = joints[0,1]

        # Check whether the distance between end effector and the target is greater
        # than some tolerance

        difA = math.sqrt(math.pow(joints[num_joints-1,0]-target[0],2)
               + math.pow(joints[num_joints-1,1]-target[1],2))

        while difA > TOLERANCE:
            # STAGE 1: FORWARD REACHING
            # Set the end effector as target t
            joints[num_joints - 1,0] = target[0]
            joints[num_joints - 1,1] = target[1]


            for i in reversed(range(num_joints-1)):
                # finds distances between the new joint positions of the next joint
                # and the current position of the lower joint
                r = math.sqrt(math.pow(joints[i, 0] - joints[i + 1, 0], 2)
                              + math.pow(joints[i, 1] - joints[i + 1, 1], 2))

                kappa = d[i] / r

                # updates joint positions
                joints[i, 0] = (1 - kappa) * joints[i + 1, 0] + kappa * joints[i,0]
                joints[i, 1] = (1 - kappa) * joints[i + 1, 1] + kappa * joints[i,1]

            # STAGE 2: BACKWARD REACHING
            # Set the root as the initial position

            joints[0,0] = b[0]
            joints[0,1] = b[1]

            for i in range(num_joints-1):
                # finds distances between the new joint positions of the next joint
                # and the current position of the lower joint
                r = math.sqrt(math.pow(joints[i,0] - joints[i + 1,0], 2)
                              + math.pow(joints[i,1] - joints[i + 1,1], 2))

                kappa = d[i] / r

                joints[i + 1,0] = (1 - kappa) * joints[i, 0] + kappa * joints[i + 1,0]
                joints[i + 1,1] = (1 - kappa) * joints[i, 1] + kappa * joints[i + 1,1]

            difA = math.sqrt(math.pow(joints[num_joints - 1, 0] - target[0], 2)
                             + math.pow(joints[num_joints - 1, 1] - target[1], 2))

    return joints


def get_new_joints3d(joints, target, d):

    # calculates distance from root to target
    dist = math.sqrt(math.pow(joints[0,0]-target[0],2)
               + math.pow(joints[0,1]-target[1],2)
               + math.pow(joints[0,2]-target[2],2))

    # columns is number of joints
    num_joints = joints.shape[0]

    # checks if target is reachable
    if dist > sum(d):
        # target is unreachable
        for i in range(num_joints-1):
            # finds distance between each target and each joint, except the last joint
            r = math.sqrt(math.pow(joints[i,0]-target[0],2)
               + math.pow(joints[i,1]-target[1],2)
               + math.pow(joints[i,2]-target[2],2))
            kappa = d[i] / r

            #updates joint positions
            joints[i+1,0] = (1-kappa)*joints[i,0]+kappa*target[0]
            joints[i+1,1] = (1-kappa)*joints[i,1]+kappa*target[1]
            joints[i+1,2] = (1-kappa)*joints[i,2]+kappa*target[2]
    else:
        # target is reachable
        b = numpy.zeros((3,))
        b[0] = joints[0,0]
        b[1] = joints[0,1]
        b[2] = joints[0,2]

        # Check whether the distance between end effector and the target is greater
        # than some tolerance

        difA = math.sqrt(math.pow(joints[num_joints-1,0]-target[0],2)
               + math.pow(joints[num_joints-1,1]-target[1],2)
               + math.pow(joints[num_joints-1,2]-target[2],2))

        while difA > TOLERANCE:
            # STAGE 1: FORWARD REACHING
            # Set the end effector as target t
            joints[num_joints - 1,0] = target[0]
            joints[num_joints - 1,1] = target[1]
            joints[num_joints - 1,2] = target[2]


            for i in reversed(range(num_joints-1)):
                # finds distances between the new joint positions of the next joint
                # and the current position of the lower joint
                r = math.sqrt(math.pow(joints[i, 0] - joints[i + 1, 0], 2)
                              + math.pow(joints[i, 1] - joints[i + 1, 1], 2)
                              + math.pow(joints[i, 2] - joints[i + 1, 2], 2))

                kappa = d[i] / r

                # updates joint positions
                joints[i, 0] = (1 - kappa) * joints[i + 1, 0] + kappa * joints[i,0]
                joints[i, 1] = (1 - kappa) * joints[i + 1, 1] + kappa * joints[i,1]
                joints[i, 2] = (1 - kappa) * joints[i + 1, 2] + kappa * joints[i,2]

            # STAGE 2: BACKWARD REACHING
            # Set the root as the initial position

            joints[0,0] = b[0]
            joints[0,1] = b[1]
            joints[0,2] = b[2]

            for i in range(num_joints-1):
                # finds distances between the new joint positions of the next joint
                # and the current position of the lower joint
                r = math.sqrt(math.pow(joints[i,0] - joints[i + 1,0], 2)
                              + math.pow(joints[i,1] - joints[i + 1,1], 2)
                              + math.pow(joints[i,2] - joints[i + 1,2], 2))

                kappa = d[i] / r

                joints[i + 1,0] = (1 - kappa) * joints[i, 0] + kappa * joints[i + 1,0]
                joints[i + 1,1] = (1 - kappa) * joints[i, 1] + kappa * joints[i + 1,1]
                joints[i + 1,2] = (1 - kappa) * joints[i, 2] + kappa * joints[i + 1,2]

            difA = math.sqrt(math.pow(joints[num_joints - 1, 0] - target[0], 2)
                             + math.pow(joints[num_joints - 1, 1] - target[1], 2)
                             + math.pow(joints[num_joints - 1, 2] - target[2], 2))

    return joints


def fabrik_rotation(joints, target, d):
    # angle the base has to have to face the target
    baseangle = get_base_angle(joints, target)

    # rotation matrix to rotate the target onto the x-z-plane
    rotmat = rotation_matrix(baseangle)
    rotated_target = numpy.dot(rotmat, target)

    # removes the y-component from the target
    target_in_plane = numpy.array([rotated_target[0], rotated_target[2]])

    # removes the y-components from the joints
    joints_in_plane = numpy.array([[joints[0,0], joints[0,2]],
                                   [joints[0, 0], joints[0, 2]],
                                   [joints[0, 0], joints[0, 2]],
                                   [joints[0, 0], joints[0, 2]]])

    # applies FABRIK on the 2D-data
    j = get_new_joints2d(joints_in_plane, target_in_plane, d)
    print("FABRIK 3D version by rotating the target point onto the x-z-plane")
    print(j)

    # add the y-components back to the joints
    j1 = numpy.array([j[0, 0], 0, j[0, 1]])
    j2 = numpy.array([j[1, 0], 0, j[1, 1]])
    j3 = numpy.array([j[2, 0], 0, j[2, 1]])
    j4 = numpy.array([j[3, 0], 0, j[3, 1]])

    # rotation matrix to rotate back to the original target point
    rotmat = rotation_matrix(-baseangle)

    # rotates the joint positions to the correct positions
    j1 = numpy.dot(rotmat, j1)
    j2 = numpy.dot(rotmat, j2)
    j3 = numpy.dot(rotmat, j3)
    j4 = numpy.dot(rotmat, j4)

    joints_in_space = numpy.array([j1, j2, j3, j4])

    # calculates the angles from the joint positions
    theta1, theta2, theta3 = get_joint_angles(joints_in_space, d)
    print(joints_in_space)
    print("Base: " + str(baseangle) + " Th1: " + str(theta1) + " Th2: " + str(theta2) + " Th3: " + str(theta3))
    return (baseangle, theta1, theta2, theta3)

def fabrik3d(joints, target, d):
    #updates the joint positions
    joints = get_new_joints3d(joints, target, d)
    baseangle = get_base_angle(joints, target)
    theta1, theta2, theta3 = get_joint_angles(joints, d)
    print("FABRIK native 3D")
    print(joints)
    print("Base: " + str(baseangle) + " Th1: " + str(theta1) + " Th2: " + str(theta2) + " Th3: " + str(theta3))
    return baseangle, theta1, theta2, theta3

# calculates the angle the base has to have to face the target (if target is left of the base, theta will be negative,
# else positive)


def get_base_angle(joints, target):
    b = numpy.array([1,0])
    t = target[0:2]
    if numpy.min(t) < 0:
        return get_angle_between_vectors(t,b)
    else:
        return -get_angle_between_vectors(t,b)


def rotation_matrix(theta):
    return numpy.array([[math.cos(theta), -math.sin(theta), 0], [math.sin(theta), math.cos(theta), 0], [0, 0, 1]])

# gets joint angle


def get_joint_angles(joints, d):
    basevec = numpy.array([0, 0, 10.7])
    link1vec = joints[1,:]-joints[0,:]
    link2vec = joints[2,:]-joints[1,:]
    link3vec = joints[3,:] - joints[2,:]

    theta1 = get_angle_between_vectors(link1vec, basevec)
    theta2 = get_angle_between_vectors(link2vec, link1vec)
    theta3 = get_angle_between_vectors(link3vec, link2vec)

    return theta1, theta2, theta3


# finds the angle between the plane in which the new joint positions lie and the x-z-plane,
# which is the angle for the base.
def find_angle_to_plane(planecoeffs):
    xvec = numpy.array([1, 0, 0])
    zvec = numpy.array([0, 0, 1])

    # gets the normal of the x-z-plane
    crossproduct = numpy.cross(xvec, zvec)

    # the angle between the two normals
    theta = get_angle_between_vectors(crossproduct, planecoeffs)

    print(str(theta))

    return theta


# calculates an angle between two vectors
def get_angle_between_vectors(v1, v2):
    dn = numpy.dot(v1, v2)
    n = numpy.linalg.norm(v1)*numpy.linalg.norm(v2)
    return math.acos( (dn / n) )
