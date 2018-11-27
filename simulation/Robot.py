class Robot(object):

    def __init__(self, links, angleRanges, currentPosition, initialAngles, initEEorientation, ee_dims, link_masses, spring_constants, com):
        self. links = links
        self.angleRanges = angleRanges
        self.currentPosition = currentPosition
        self.currentAngles = initialAngles
        self.ee_orientation = initEEorientation
        self.ee_dims = ee_dims
        self.link_masses = link_masses
        self.spring_constants = spring_constants
        self.com = com