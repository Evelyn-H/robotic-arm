import numpy as np
from numpy.linalg import norm as norm
from math import cos, sin, acos

class Physics(object):
    # DO SOME PASSES OF THIS, BECAUSE GRAVITATIONAL FORCES ARE DEPENDANT ON BOTH SUCCINCT AND PRIOR JOINTS!!

    # WEIGHT UNITS ARE IN GRAMS
    MASS_EE = 50
    CENTER_OF_MASS_EE = [0, 7, 0]
    F_G = 9.81
    GRAVITY_VEC = np.array([0, 0, -1])
    NORM_GRAVITY_VEC = norm(GRAVITY_VEC)
    EPSILON = 0.008

    # link_dims contains the link from the base to the first R joint.
    # link_masses does NOT contain the mass for the link from the base to the first R joint.
    def __init__(self, link_masses, spring_constants, maxima):
        self.link_masses = link_masses
        self.spring_constants = spring_constants
        self.base_axis = np.array([1, 0, 0])
        self.axis = np.array([1, 0, 0])
        self.torques = [0, 0, 0, 0]
        self.mass_l3_ee = self.link_masses[2]+self.MASS_EE
        self.mass_l2_l3_ee = self.link_masses[1] + self.mass_l3_ee
        self.mass_l1_l2_l3_ee = self.link_masses[0] + self.mass_l2_l3_ee
        self.maxima = maxima
        self.curr_angles= []

    def set_angles(self, angles):
        self.curr_angles = angles

    def set_spring_constants(self, spring_constants):
        self.spring_constants = spring_constants

    def apply_postprocessing_physics(self, angles, positions):
        self.calculate_torques(positions)
        angles = self.change_angles(angles)
        return angles

    # calculates the gravitational torques on all joints
    def calculate_torques(self, pos):
        # TORQUE FOR JOINT 4

        # center of mass for the EE (it's tracked by the FK)
        com = (np.array(pos[4])-np.array(pos[2]))[0:3]
        # calculates the angle wrt to the link gravity is acting upon
        angle_of_attack = com.dot(self.GRAVITY_VEC)/norm(com)
        angle_of_attack = acos(angle_of_attack)

        # calculates the force perpendicular to the link
        force = self.MASS_EE*self.F_G/1000

        s = sin(angle_of_attack)

        if s < self.EPSILON:
            s = 0

        force = s * force

        self.torques[3] = force






        # TORQUE FOR JOINT 3

        # calculates the center of mass
        com_link = (np.array(pos[2]) - np.array(pos[3]))[0:3] / 2
        # center of mass for link 3
        com = self.link_masses[1]*com_link + self.MASS_EE*com
        com = com / self.mass_l3_ee

        # calculates the angle wrt to the link gravity is acting upon
        angle_of_attack = com.dot(self.GRAVITY_VEC)/norm(com)
        angle_of_attack = acos(angle_of_attack)

        # calculates the force perpendicular to the link
        force = self.mass_l3_ee*self.F_G/1000

        s = sin(angle_of_attack)

        if s < self.EPSILON:
            s = 0

        force = s * force

        self.torques[2] = force




        # TORQUE FOR JOINT 2

        # calculates the center of mass
        com_link = (np.array(pos[1]) - np.array(pos[2]))[0:3] / 2

        # center of mass for link 2
        com = (self.link_masses[0] * com_link + self.mass_l3_ee * com)[0:3]
        com = com / self.mass_l2_l3_ee

        # calculates the angle wrt to the link gravity is acting upon
        angle_of_attack = com.dot(self.GRAVITY_VEC) / norm(com)
        angle_of_attack = acos(angle_of_attack)

        # calculates the force perpendicular to the link
        force = self.mass_l2_l3_ee * self.F_G / 1000

        s = sin(angle_of_attack)

        if s < self.EPSILON:
            s = 0

        force = s * force
        # torque
        self.torques[1] = force




        # TORQUE FOR JOINT 1

        # calculates the center of mass
        com_link = (np.array(pos[0]) - np.array(pos[1]))[0:3] / 2

        # center of mass for link 1
        com = (self.link_masses[0] * com_link + self.mass_l2_l3_ee * com)[0:3]
        com = com / self.mass_l1_l2_l3_ee

        # calculates the angle wrt to the link gravity is acting upon
        angle_of_attack = com.dot(self.GRAVITY_VEC) / norm(com)
        angle_of_attack = acos(angle_of_attack)

        # calculates the force perpendicular to the link
        force = self.mass_l1_l2_l3_ee * self.F_G / 1000

        s = sin(angle_of_attack)

        if s < self.EPSILON:
            s = 0

        force = s * force
        # torque
        self.torques[0] = force

    def change_angles(self, angles):
        rot1 = -self.torques[0]/self.spring_constants[0]
        rot2 = -self.torques[1]/self.spring_constants[1]
        rot3 = -self.torques[2]/self.spring_constants[2]
        rot4 = -self.torques[3]/self.spring_constants[3]
        # print("A")
        # print(rot1)
        # print(rot2)
        # print(rot3)
        # print(rot4)
        # print("E\n")
        #if angles[0]+rot1 > self.curr_angles[0] + self.maxima[0]:
        #    rot1 = 0
        #print(angles)
        # if angles[1]+rot2+rot1 > self.curr_angles[1] + self.maxima[1]:
        #     angles[1] = self.curr_angles[1] + self.maxima[1]
        # else:
        #     angles[1] = angles[1]+ rot2+rot1
        #
        # if angles[2]+rot3 > self.curr_angles[2] + self.maxima[2]:
        #     angles[2] = self.curr_angles[2] + self.maxima[2]
        # else:
        #     angles[2] = angles[2] + rot3
        #
        # if angles[3]+rot4 > self.curr_angles[3] + self.maxima[3]:
        #     angles[2] = self.curr_angles[2] + self.maxima[2]
        # else:
        #     angles[3] = angles[3] + rot4

        # print(self.torques[0]/self.spring_constants[0])
        angles[1] = angles[1]+ rot2+rot1
        # print(self.torques[1]/self.spring_constants[1])
        angles[2] = angles[2]+ rot3
        # print(self.torques[2]/self.spring_constants[2])
        #print(angles[0])
        angles[3] = angles[3] + rot4
        return angles
