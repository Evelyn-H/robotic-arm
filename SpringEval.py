from math import radians as rad
import numpy as np

class Eval(object):

    def __init__(self, sample_angles, sampled_points, fk, physics):
        self.sample_angles = sample_angles
        self.sampled_points = sampled_points
        self.fk = fk
        self.physics = physics

    def measureError(self, spring_constants):
        for s in spring_constants:
            if s <= 0:
                return 10000
        error = 0
        for i in range(len(self.sampled_points)):
            point = self.get_z(self.sample_angles[i].copy(), spring_constants)
            origpos = self.fk.move([rad(self.sample_angles[i].copy()[0]), -rad(self.sample_angles[i].copy()[1]), -rad(self.sample_angles[i].copy()[2]), -rad(self.sample_angles[i].copy()[3])])

            if i % 1 == 0:
                print("From: ", origpos[3][0], origpos[3][1], origpos[3][2])
                # temp = origpos[3][0]
                # origpos[3][0] = origpos[3][1]
                # origpos[3][1] = temp
                #print(origpos[3])
                print("To: ", point)
            h = origpos[3][2]-10.5

            hdiff = origpos[3][2]-point[2]
            if point[2]-10.5 < 0:
                return 10000
            if i%1 == 0:
                print("Hdiff: ", hdiff * 10)
                print("Rdiff: ", h * 10 - self.sampled_points[i])
            point = point[0:1]
            origpos = origpos[3][0:1]
            #error += np.linalg.norm(origpos-point)+abs(hdiff*50-(h-self.sampled_points[i])*5)
            error += abs(hdiff*10-(h*10-self.sampled_points[i]))


        return error/len(self.sampled_points)

    def get_z(self, iksol, spring_constants):
        self.physics.set_spring_constants(spring_constants)
        positions = self.fk.move(iksol)
        angles = self.apply_postprocessing_physics(iksol, positions)
        positions = self.fk.move([rad(angles[0]), -rad(angles[1]), -rad(angles[2]), -rad(angles[3])])
        h = positions[3][2]
        for i in range(0, 200):
            angles = self.apply_postprocessing_physics(angles, positions)
            positions = self.fk.move([rad(angles[0]), -rad(angles[1]), -rad(angles[2]), -rad(angles[3])])

        #print("To: ", positions[3])
        if h-positions[3][2] < 0:
            return [3333, 3333, 3333, 1]

        return positions[3]

    def apply_postprocessing_physics(self, angles, positions):
        return self.physics.apply_postprocessing_physics(angles, positions)
