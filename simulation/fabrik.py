import math
import numpy

# Tolerance for the final result, unit is centimeters
TOLERANCE = 0.05
# everything is kept pretty verbose on purpose to ease porting the algorithm
# into C++ later on.


def fabrik(joints, target, d):

    # calculates distance from root to target
    dist = math.sqrt(math.pow(joints[0,0]-target[0],2)
               + math.pow(joints[0,1]-target[1],2)
               + math.pow(joints[0,2]-target[2],2))

    # columns is number of joints
    num_joints = joints.shape[1]

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
            print("difA: " +str(difA))
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
                print("Old x: " +str(joints[i + 1,0]))
                joints[i + 1,0] = (1 - kappa) * joints[i, 0] + kappa * joints[i + 1,0]
                print("New x: " +str(joints[i + 1,0]))
                joints[i + 1,1] = (1 - kappa) * joints[i, 1] + kappa * joints[i + 1,1]
                joints[i + 1,2] = (1 - kappa) * joints[i, 2] + kappa * joints[i + 1,2]

            difA = math.sqrt(math.pow(joints[num_joints - 1, 0] - target[0], 2)
                             + math.pow(joints[num_joints - 1, 1] - target[1], 2)
                             + math.pow(joints[num_joints - 1, 2] - target[2], 2))

    return joints