import math
import operator

import numpy as np
from matplotlib import pyplot as plt
import pdb

from trajectory import trajectory

def mass_curve(min_mass = None, max_mass = None):
  if min_mass == None:
    min_mass = 0 
  if max_mass == None:
    max_mass = 1.55

  altitudes = []
  masses = np.linspace(min_mass,max_mass,60)

  for mass in masses:
    t, position, velocity, accel, thrust = trajectory(mass)
    altitudes.append(max(position[:,1]))
  index, altitude = max(enumerate(altitudes), key=operator.itemgetter(1))
  t, position, velocity, accel, thrust = trajectory(masses[index])

  return t, position, velocity, accel, thrust, masses, altitudes

