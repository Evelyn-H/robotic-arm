import numpy as np
from scipy.optimize import fmin_powell
from scipy.optimize import minimize, basinhopping
from SpringEval import Eval
import numpy as np
from Robot import Robot
from math import sqrt, pi, radians as rad
from PhysicsEngine import Physics
from InverseKinematics import IKSolver
from ForwardKinematics import ForwardKinematics
from multiprocessing import Pool
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import math
from random import random
import random
import scipy.io
import time


def apply_postprocessing_physics(angles, positions):
    return physics.apply_postprocessing_physics(angles, positions)

# EE characteristics
ee_dims = [8.6, 9]
ee_angle = np.arctan((9/8.6))
ee_orientation = 0

# CALCULATE THIS PROPERLY, THIS IS JUST FOR TESTING PURPOSES
ee_center_of_mass = [-2, 0, 1, 1]
links = [10.5, 11.7654, 10.5, sqrt(ee_dims[0]**2 + ee_dims[1]**2)]
angleRanges = [[-90, 90], [-90, 90], [-90, 90], [-90, 90]]
currentPosition = [[0,0,0],
                   [0,0,links[0]],
                   [0,0,links[0]+links[1]],
                   [0,0,links[0]+links[1]+links[2]],
                   [0,ee_dims[1],links[0]+links[1]+links[2]+ee_dims[0]]]

initialAngles = [0, 0, 0, 0]

# masses for every link
link_masses = [0.120, 0.111, 0.075, 0.085]

# spring constant for the torsion spring joints
spring_constants = [25, 25, 25, 25]

# refresh rate of view (and later maybe physics) - in ms
TIMESTEP = 12

k = 90

robot = Robot(links, angleRanges, currentPosition, initialAngles, ee_orientation, ee_dims, link_masses, spring_constants, ee_center_of_mass[0:3], [k, k, k, k])
physics = Physics(robot.link_masses, robot.spring_constants, robot.maximum_sag)
fk = ForwardKinematics([0, 0.5 * pi, 0, 0],
                       [links[0], 0, 0, 0],
                       [0, links[1], links[2], ee_dims[0]],
                       [.5 * pi, 0, 0, 0.5 * pi],
                       np.array([
                           [0, 0, 0, 1],
                           [0, 0, 0, 1],
                           [0, 0, 0, 1],
                           [0, 0, ee_dims[1], 1]
                       ]),
                       ee_center_of_mass)

ik_params = [[11.9, 10.5, sqrt(ee_dims[0] ** 2 + ee_dims[1] ** 2)], [[-60, 60], [-90, 90], [-90, 90]], ee_dims, 20, -45, 45, 50]
ik = IKSolver(*ik_params)
n = 5
# j1 = 0
# j2 = np.linspace(0, 90, n)
# j3 = np.linspace(0, 90, n)
# j4 = np.linspace(0, 90, n)
#
# sample_angles = []
# sample_points = []
# for i in range(n):
#     for j in range(n):
#         for k in range(n):
#             sample_angles.append(np.array([j1, j2[i], j3[j], j4[k]]))
#
coords = []
heightdiff = []
with open("/home/hermann/Desktop/points.txt", "r") as f:
    for line in f:
        x, y, z, h = line.split()
        if float(x) >= 0:
            coords.append([float(y), float(x), float(z)])
            heightdiff.append(float(h))



# test_set_coords = []
# test_set_heightdiff = []
# for i in range(0,int((len(coords)/5))):
#     rnd = random.randint(0,len(coords)-1)
#     print("RND: ", rnd)
#     test_set_coords.append(coords[rnd])
#     test_set_heightdiff.append(heightdiff[rnd])
#     print(coords[rnd], " ", heightdiff[rnd])
#     del coords[rnd]
#     del heightdiff[rnd]

sample_angles = []

for c in coords:
    print("LEN: ", len(ik.find_angles(c)))
    sample_angles.append(ik.find_angles(c)[0:4])
#print(list(zip(coords, heightdiff)))
# test_angles = []
# for c in test_set_coords:
#     test_angles.append(ik.find_angles(c)[0:4])

#print(sample_angles)

# print("Evaluating " +str(len(sample_angles)) +" angles.")
# for j in range(len(sample_angles)):
#     #print(sample_angles[j])
#     angles = sample_angles[j].copy()
#     positions = fk.move(angles)
#     angles = apply_postprocessing_physics(angles, positions)
#     positions = fk.move([rad(angles[0]), -rad(angles[1]), -rad(angles[2]), -rad(angles[3])])
#
#     for i in range(0, 200):
#         angles = apply_postprocessing_physics(angles, positions)
#         positions = fk.move([rad(angles[0]), -rad(angles[1]), -rad(angles[2]), -rad(angles[3])])
#
#         positions = fk.move([rad(angles[0]), -rad(angles[1]), -rad(angles[2]), -rad(angles[3])])
#
#     #print(sample_angles[j])
#     #print("\n")
#     sample_points.append(positions[3])
#
# print("Done evaluating. Optimizing.")
sample_points = heightdiff.copy()
gravEval = Eval(sample_angles, sample_points, fk, physics)
#test_set_eval = Eval(test_angles, test_set_heightdiff, fk, physics)



def test_fun_a(x):
    pid = os.getpid()
    print(pid)
    s1 = 25
    s4 = 25

    n = 11
    s2 = np.linspace(24.9, 25.1, n)
    s3 = np.linspace(24.9, 25.1, n)

    result = np.zeros((n, n))

    for i in x:
        for j in range(n):
            print("PID: " +str(pid) +" I: " +str(i) + " J: " +str(j))
            result[i, j] = gravEval.measureError(np.array([s1, s2[i], s3[j], s4]))

    return result


def test_fun(x):
    print(x, "\n")
    e = gravEval.measureError(x)
    print("Error: " +str(e))
    #e_test = test_set_eval.measureError(x)
    #print("Test set error: ", e_test, "\n")
    return e

MIN_CONST = 5


def callback(par):
    r = np.sum(par,0)
    np.save(("/home/hermann/Experiments/"+str(time.clock())), r)



res = basinhopping(test_fun, x0=[30.22484294,  74.16697761, 200.69742822, 625.50922062])

# def split(a, n):
#     k, m = divmod(len(a), n)
#     return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))
#
# n=11
# u =list(split(range(n), 8))
# jobs = [u[0], u[1], u[2], u[3], u[4], u[5], u[6], u[7]]
#
# pool = Pool(processes=8)
#
# pool.map_async(test_fun_a, jobs, callback=callback)
# pool.close()
# pool.join()
print(res)
#scipy.io.savemat("/home/hermann/Experiments/file2.mat", {"myfile":g})

#result = result/np.max(result.flatten())

#np.save("/home/hermann/data10201.npy", result)

