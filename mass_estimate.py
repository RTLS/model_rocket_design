import math

import numpy as np
import matplotlib.pyplot as plt
import pdb


def drag(u,Cd,A):
  rho = 1.225    #kg    #FIXME
  return .5*rho*u*np.absolute(u)*Cd*A

#Simulation Parameters
n = 1001    #simulation steps
t = np.linspace(0,150,num=n)    #time vector
dt = t[1] - t[0]


# Motor Parameters
g407_t = np.array([0, 0.024, 0.057, 0.252, 0.500, 0.765, 1.000, 1.250, 1.502, 1.751, 1.999, 2.121, 2.300])
g407_thrust = np.array([0, 74.325, 67.005, 65.879, 63.063, 60.248, 54.054, 47.298, 36.599, 25.338, 12.951, 3.941, 0])
thrust = [np.interp(t[i], g407_t, g407_thrust) if t[i] < g407_t[-1] else 0 for i in xrange(len(t))]    #motor thrust over time
g407_t = np.array([0, g407_t[-1]+7])
g407_m = np.array([.1234, .0607])
g407_m = [np.interp(t[i], g407_t, g407_m) for i in xrange(len(t))]    #motor mass over time

#Rocket Parameters
dry_mass = np.linspace(.75,2,num=9)    # kg
mass = np.array([[elem + dry_mass[i] for elem in g407_m] for i in xrange(len(dry_mass))])
Cd = [.75 if t[i] < g407_t[-1] else 1.5 for i in xrange(len(t))]
A = [0.0042 if t[i] < g407_t[-1] else 1.65 for i in xrange(len(t))]   # m^2

# Launch Parameters
flight_angle = 2/180.0*math.pi    #rads
transform = np.array([math.sin(flight_angle), math.cos(flight_angle)])
g = 9.81;

altitudes = []
#pdb.set_trace()
for j in xrange(len(mass[:,0])):
  position = np.zeros([n,2], dtype=np.float)    #position vector, 2 dimensional
  velocity = np.zeros([n,2], dtype=np.float)    #velocity vector, 2 dimensional
  accel = np.zeros([n,2], dtype=np.float)    #acceleration vector, 2 dimensional
  for i in xrange(len(t)-1):
    #pdb.set_trace()
    # If we're on the ground (either before launch or after landing)
    if position[i,1] < 0:
      pass
    # Modified Euler method.
    else:
      m1 = (transform*thrust[i] - transform*drag(velocity[i,:], Cd[i], A[i]))/mass[j,i] - np.array([0,g])
      m2 = (transform*thrust[i+1] - transform*drag(velocity[i,:]+dt*m1, Cd[i+1], A[i+1]))/mass[j,i+1] - np.array([0,g])
      accel[i, :] = (m1+m2)/2.0
      velocity[i+1, :] = velocity[i,:] + dt*accel[i, :] 
      position[i+1, :] = position[i,:] + dt*(velocity[i,:] + velocity[i+1,:])/2.0

  pdb.set_trace()
  altitudes.append(max(position[:, 1]))

pdb.set_trace()
""" Plotting """

