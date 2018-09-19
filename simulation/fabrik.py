import math

# Tolerance for the final result, unit is centimeters
TOLERANCE = 0.05
# everything is kept pretty verbose on purpose to ease porting the algorithm
# into C++ later on.
def fabrik_iteration(joints, target, d):

    # calculates distance from root to target
    dist = math.sqrt(math.pow(joints[0,0]-target[0,0],2)
               + math.pow(joints[1,0]-target[1,0],2)
               + math.pow(joints[2,0]-target[2,0],2))

    # columns is number of joints
    num_joints = joints.shape(1)

    # checks if target is reachable
    if dist > sum(d):
        # target is unreachable
        for i in range(num_joints-1):
            # finds distance between each target and each joint, except the last joint
            r = math.sqrt(math.pow(joints[0,i]-target[0,0],2)
               + math.pow(joints[1,i]-target[1,0],2)
               + math.pow(joints[2,i]-target[2,0],2))
            kappa = d[i] / r

            #updates joint positions
            joints[0,i+1] = (1-kappa)*joints[0,i]+kappa*target[0]
            joints[1,i+1] = (1-kappa)*joints[1,i]+kappa*target[1]
            joints[2,i+1] = (1-kappa)*joints[2,i]+kappa*target[2]
    else:
        # target is reachable
        b = numpy.zeros((3,))
        b[0] = joints[0,0]
        b[1] = joints[1,0]
        b[2] = joints[2,0]

        # Check whether the distance between end effector and the target is greater
        # than some tolerance

        difA = math.sqrt(math.pow(joints[0,num_joints-1]-target[0,0],2)
               + math.pow(joints[1,num_joints-1]-target[1,0],2)
               + math.pow(joints[2,num_joints-1]-target[2,0],2))

        while difA > TOLERANCE:
            # STAGE 1: FORWARD REACHING
            # Set the end effector as target t
            joints[0, num_joints - 1] = target[0, 0]
            joints[1, num_joints - 1] = target[1, 0]
            joints[2, num_joints - 1] = target[2, 0]


            for i in reversed(range(num_joints-1)):
                # finds distances between the new joint positions of the next joint
                # and the current position of the lower joint
                r = math.sqrt(math.pow(joints[0, i] - joints[0, i + 1], 2)
                              + math.pow(joints[1, i] - joints[1, i + 1], 2)
                              + math.pow(joints[2, i] - joints[2, i + 1], 2))

                kappa = d[i] / r

                # updates joint positions
                joints[0, i] = (1 - kappa) * joints[0, i + 1] + kappa * joints[0, i]
                joints[1, i] = (1 - kappa) * joints[1, i + 1] + kappa * joints[1, i]
                joints[2, i] = (1 - kappa) * joints[2, i + 1] + kappa * joints[2, i]

            # STAGE 2: BACKWARD REACHING
            # Set the root as the initial position

            joints[0,0] = b[0]
            joints[1,0] = b[1]
            joints[2,0] = b[2]

            for i in range(num_joints-1):
                # finds distances between the new joint positions of the next joint
                # and the current position of the lower joint
                r = math.sqrt(math.pow(joints[0, i] - joints[0, i + 1], 2)
                              + math.pow(joints[1, i] - joints[1, i + 1], 2)
                              + math.pow(joints[2, i] - joints[2, i + 1], 2))

                kappa = d[i] / r

                joints[0, i + 1] = (1 - kappa) * joints[0, i] + kappa * joints[0, i + 1]
                joints[1, i + 1] = (1 - kappa) * joints[1, i] + kappa * joints[1, i + 1]
                joints[2, i + 1] = (1 - kappa) * joints[2, i] + kappa * joints[2, i + 1]

            difA = math.sqrt(math.pow(joints[0, num_joints - 1] - target[0, 0], 2)
                             + math.pow(joints[1, num_joints - 1] - target[1, 0], 2)
                             + math.pow(joints[2, num_joints - 1] - target[2, 0], 2))
