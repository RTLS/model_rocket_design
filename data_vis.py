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

  print(stats)

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
  
  # Velocity
  plt.figure(2)
  plt.plot(t, velocity[:,1])
  plt.ylabel('Velocity [m/s]')
  plt.xlabel('Time [s]')
  plt.title('Velocity')
  
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
  plt.show()

