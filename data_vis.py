import operator
from matplotlib import pyplot as plt
import pdb

def stats(t, position, velocity, accel, thrust):
  stats = {}
  dt = t[1] - t[0]
  stats['max_altitude'] = max(position[:,1])
  stats['max_velocity'] = max(velocity[:,1])
  stats['max_g_force'] = (max(accel[:,1])/9.81)
  stats['total_impulse'] = sum(thrust)*dt
  stats['peak_thrust'] = max(thrust)
  stats['flight_time'] = max([t[i] if position[i,1] > 0 else 0 for i in xrange(len(t))])
  stats['descent_rate'] = [velocity[i,1] for i in xrange(len(t)) if velocity[i,1] != 0][-1]

  print(stats)

def stats_mass_curve(t, position, velocity, accel, thrust, masses, altitudes):
  index, altitude = max(enumerate(altitudes), key=operator.itemgetter(1))
  print("Max altitude of " + str(altitude) + " with mass of " + str(masses[index]) + ".")
  stats(t, position, velocity, accel, thrust)
  plt.figure(1)
  plt.plot(masses, altitudes)
  plt.ylabel("Apogee Height [m]")
  plt.xlabel("Dry Mass [kg]")
  plt.title("Mass Curve")
  plt.show()

def plot(t, position, velocity, accel, thrust):
  # Altitude
  plt.figure(1)
  plt.subplot(211)
  plt.plot(t, position[:,1])
  plt.ylabel('Height [m]')
  plt.xlabel('Time [s]')
  plt.title('Altitude')
  plt.subplot(212)
  plt.plot(t, position[:,0])
  plt.ylabel('Distance [m]')
  plt.xlabel('Time [s]')
  plt.title('Down Range Distance')
  plt.tight_layout()

  # Velocity
  plt.figure(2)
  plt.plot(t, velocity[:,1])
  plt.ylabel('Velocity [m/s]')
  plt.xlabel('Time [s]')
  plt.title('Velocity')
  plt.tight_layout()
  
  # Acceleration
  plt.figure(3)
  plt.subplot(211)
  plt.plot(t[0:len(thrust)], accel[0:len(thrust),1])
  plt.ylabel('Acceleration m/s^2')
  plt.xlabel('Time [s]')
  plt.title('Acceleration')
  plt.subplot(212)
  plt.plot(t[0:len(thrust)], thrust)
  plt.ylabel('Thrust [N]')
  plt.xlabel('Time [s]')
  plt.title('Thrust')
  plt.tight_layout()

  plt.show()

