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
    EPSILON = 0.08

    # link_dims contains the link from the base to the first R joint.
    # link_masses does NOT contain the mass for the link from the base to the first R joint.
    def __init__(self, link_masses, spring_constants):
        self.link_masses = link_masses
        self.spring_constants = spring_constants
        self.base_axis = np.array([1, 0, 0])
        self.axis = np.array([1, 0, 0])
        self.lever_forces = [0, 0]
        self.torques = [0, 0, 0]
        self.mass_l3_ee = self.link_masses[1]+self.MASS_EE
        self.mass_l2_l3_ee = self.link_masses[0] + self.mass_l3_ee

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

        self.torques[2] = force

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

        self.torques[1] = force
        # TORQUE FOR JOINT 2

        # calculates the center of mass
        com_link = (np.array(pos[1]) - np.array(pos[2]))[0:3]/2

        # center of mass for link 2
        com = (self.link_masses[0]*com_link + self.mass_l3_ee*com)[0:3]
        com = com / self.mass_l2_l3_ee

        # calculates the angle wrt to the link gravity is acting upon
        angle_of_attack = com.dot(self.GRAVITY_VEC)/norm(com)
        angle_of_attack = acos(angle_of_attack)

        # calculates the force perpendicular to the link
        force = self.mass_l2_l3_ee*self.F_G/1000

        s = sin(angle_of_attack)

        if s < self.EPSILON:
            s = 0

        force = s*force
        # torque
        self.torques[0] = force

    def change_angles(self, angles):
        angles[1] = angles[1]+self.torques[0]/self.spring_constants[0]
        # print(self.torques[0]/self.spring_constants[0])
        angles[2] = angles[2]+self.torques[1]/self.spring_constants[1]
        # print(self.torques[1]/self.spring_constants[1])
        angles[3] = angles[3]+self.torques[2]/self.spring_constants[2]
        # print(self.torques[2]/self.spring_constants[2])

        return angles
