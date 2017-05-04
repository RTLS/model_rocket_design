import math

import numpy as np
import pdb


def drag(height,u,Cd,A):
  height = 3.28084*height
  T = 59 - 0.00356 * height    # Temp in Farenheighteit
  p = 473.1 * np.exp(1.73 - 0.000048 * height)    # Pressure
  rho = p / (1718 * (T + 459.7))    # State equation
  rho = 515.379 * rho    # Converting to kg/m^3
  drag = .5*rho*u*np.absolute(u)*Cd*A
  return drag

#class motor():
#
#  def __init_(impulse, burn_time, delay, wet_mass, dry_mass):
#    self.impulse = 

def trajectory(m=None, delta_t=None, angle=None, OD=2, chute_diam=20,
              Cd1=.75, Cd2=1.5, design_impulse=None, burn_time=None, delay=None):
  """ Simulates a launch trajectory"""
  # Computation is in SI units and uses modified Euler for numerical approximation

  #Simulation Parameters
  # "Dynamic" timestep- more important to be high fideltity during non linear
  # portion
  if delta_t is None:
    dt1 = .002    #time step size (seconds)
  else:
    dt1 = delta_t
  dt2 = dt1*5

  t = np.array([0])    #time vector
  position = np.zeros([1,2], dtype=np.float)    #position vector, 2 dimensional
  velocity = np.zeros([1,2], dtype=np.float)    #velocity vector, 2 dimensional
  accel = np.zeros([1,2], dtype=np.float)    #acceleration vector, 2 dimensional

  # Motor Parameters
  if design_impulse is None:
    design_impulse = 97.14
    motor_t = np.array([0, 0.024, 0.057, 0.252, 0.500, 0.765, 1.000, 1.250, 1.502, 1.751, 1.999, 2.121, 2.300, 9.70])
    motor_thrust = np.array([0, 74.325, 67.005, 65.879, 63.063, 60.248, 54.054, 47.298, 36.599, 25.338, 12.951, 3.941, 0, 0])
    thrust = [np.interp(i*dt1, motor_t, motor_thrust)  for i in xrange(int(motor_t[-1]/dt1)+4)]    #motor thrust over time
    impulse = sum(thrust)*dt1
    thrust = [element*design_impulse/impulse for element in thrust]
    motor_t = np.array([0, motor_t[-1]])
    motor_m = np.array([.1234, .0607])
    motor_m = [np.interp(i*dt1, motor_t, motor_m) for i in xrange(int(motor_t[-1]/dt1)+4)]    #motor mass over time
  else:
    motor_t = np.array([0, 0.024, 0.057, 0.252, 0.500, 0.765, 1.000, 1.250, 1.502, 1.751, 1.999, 2.121, 2.300])
    motor_t = np.array([elem*burn_time/motor_t[-1] for elem in motor_t])
    motor_t = np.append(motor_t, motor_t[-1]+delay)
    motor_thrust = np.array([0, 74.325, 67.005, 65.879, 63.063, 60.248, 54.054, 47.298, 36.599, 25.338, 12.951, 3.941, 0, 0])
    thrust = [np.interp(i*dt1, motor_t, motor_thrust)  for i in xrange(int(motor_t[-1]/dt1)+4)]    #motor thrust over time
    impulse = sum(thrust)*dt1
    thrust = [element*design_impulse/impulse for element in thrust]
    motor_t = np.array([0, motor_t[-1]])
    motor_m = np.array([.1234, .0607])
    motor_m = [np.interp(i*dt1, motor_t, motor_m) for i in xrange(int(motor_t[-1]/dt1)+4)]    #motor mass over time


  #Rocket Parameters
  if m is None:
    dry_mass = .23
  else:
    dry_mass = m    # kg
  mass = [elem + dry_mass for elem in motor_m]

  A1 = math.pow(OD/2.0*2.54/100,2)*3.14159
  A2 = math.pow(chute_diam/2.0*2.54/100,2)*3.14159

  # Launch Parameters
  if angle is None:
    flight_angle = 2/180.0*math.pi    #rads
  else:
    flight_angle = angle/180.0*math.pi
  transform = np.array([math.sin(flight_angle), math.cos(flight_angle)])
  g = 9.81;

  landed = False
  burnout = False
  (i, landed_counter) = (0,0)
  # main loop.  perform calcs until we land
  while not landed:
    # before we're burned out we use equations that account for thrust and pre-parachute drag coeffs
    if not burnout:
      drag1 = drag(position[i,1], velocity[i,:], Cd1, A1)
      m1 = (transform*thrust[i] - drag1)/mass[i] - np.array([0,g])
      drag2 = drag(position[i,1], velocity[i,:]+dt1*m1, Cd1, A1)
      m2 = (transform*thrust[i+1] - drag2)/mass[i+1] - np.array([0,g])

      # Here's the numerical integration for velocity and position. All modified euler
      accel = np.append(accel, np.array([(m1+m2)/2.0]), axis=0)
      velocity = np.append(velocity, np.array([velocity[i,:] + dt1*(m1+m2)/2.0]), axis=0) 
      position = np.append(position, np.array([position[i,:] + dt1*(velocity[i,:] + velocity[i+1,:])/2.0]), axis=0)
      i+=1
      t = np.append(t, np.array([t[-1]+dt1]))
    else: # If we're burned out there's no need to consider thrust, plus we use post-parachute drag coeffs
      drag1 = drag(position[i,1], velocity[i,:], Cd2, A2)
      m1 = -1*drag1/dry_mass - np.array([0,g])
      drag2 = drag(position[i,1], velocity[i,:]+dt2*m1, Cd2, A2)
      m2 = -1*drag2/dry_mass - np.array([0,g])

      # Here's the numerical integration for velocity and position. All modified euler
      accel = np.append(accel, np.array([(m1+m2)/2.0]), axis=0)
      velocity = np.append(velocity, np.array([velocity[i,:] + dt2*(m1+m2)/2.0]), axis=0) 
      position = np.append(position, np.array([position[i,:] + dt2*(velocity[i,:] + velocity[i+1,:])/2.0]), axis=0)
      i+=1
      t = np.append(t, np.array([t[-2]+dt2]))



    # Check for burnout condition
    if t[-1] > motor_t[-1]:
      burnout = True

    # Check if we're on the ground... don't want to accelerate into the earth
    if position[-1,1] <= 0:
      accel[-1,1] = max(0, accel[-1,1])
      velocity[-1,1] = max(0, velocity[-1,1])
      position[-1,1] = max(0, position[-1,1])
      landed_counter += 1
      if landed_counter > 1/dt2:    # Let's land for one second
        landed = True
   
  return t, position, velocity, accel, thrust
