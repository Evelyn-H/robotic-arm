from math import pi
from ForwardKinamatics import ForwardKinematics
import numpy as np

fk = ForwardKinematics([0, 0.5*pi, 0, 0], [10.7, 0, 0, 0], [0, 10.4, 12.8, 0], [0.5*pi, 0, 0, 0.5*pi], np.array([0, 0, 1, 1]))
fk.move([2, 0, 0, 0])
