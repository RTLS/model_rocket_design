import math

import numpy as np
from matplotlib import pyplot as plt
import pdb

from trajectory import trajectory


altitudes = []
masses = np.linspace(.2,.5,10)

for mass in masses:
  t, position, velocity, accel, thrust = trajectory(mass)
  altitudes.append(max(position[:,1]))

print(max(altitudes))
plt.figure(1)
plt.plot(masses, altitudes)
plt.show()
