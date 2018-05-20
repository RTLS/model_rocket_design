import operator

from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
import seaborn as sns
import pdb
import tables

def stats(t, position, velocity, accel, thrust, drag, name=None):
  if name is None:
    name = "Mockheed Lartin"
  stats = {}
  dt = t[1] - t[0]
  stats['name'] = name
  stats['max_altitude [ft]'] = max(position[:,1])
  stats['max_velocity [ft/s]'] = max(velocity[:,1])
  stats['max_g_force'] = (max(accel[:,1])/32.18)
  stats['total_impulse [lbf-s]'] = sum(thrust)*dt
  stats['peak_thrust [lbf]'] = max(thrust)
  stats['flight_time [s]'] = max([t[i] if position[i,1] > 0 else 0 for i in xrange(len(t))])
  stats['descent_rate [ft/s]'] = [velocity[i,1] for i in xrange(len(t)) if velocity[i,1] != 0][-1]
  stats['max_drag [lbf]'] = max(drag[:,1])
  launch_rod_length = 3         #ft
  stats['velocity_off_launch_rod'] = max([velocity[i,1] for i in xrange(len(t)) if position[i,1] < launch_rod_length])

  print(stats)

def stats_table(t, position, velocity, accel, thrust, drag, angle, delay):
  
  altitude = max(position[:,1])
  flight_time = max([t[i] if position[i,1] > 0 else 0 for i in xrange(len(t))])
  print("Angle: ", angle, "Delay: ", delay, "Altitude: ", altitude, "Time: ", flight_time)

def stats_mass_curve(t, position, velocity, accel, thrust, drag, masses, altitudes):
  index, altitude = max(enumerate(altitudes), key=operator.itemgetter(1))
  print("Max altitude of " + str(altitude) + " with mass of " + str(masses[index]) + ".")
  stats(t, position, velocity, accel, thrust, drag)
  plt.figure(1)
  plt.plot(masses, altitudes)
  plt.ylabel("Apogee Height [ft]")
  plt.xlabel("Dry Mass [kg]")
  plt.title("Mass Curve")
  plt.show()

def plot(t, position, velocity, accel, thrust, drag, name=None, export=False):
  if name is None:
    name = "Mockheed Lartin"

  plt.close('all')

  sns.set_style('darkgrid')

  # Altitude
  plt.figure(1)
  plt.subplot(211)
  plt.plot(t, position[:,1], label=name)
  plt.ylabel('Height [ft]')
  plt.xlabel('Time [s]')
  plt.title('Altitude')
  plt.grid()
  plt.subplot(212)
  plt.plot(t, velocity[:,1], label=name)
  plt.ylabel('Velocity [ft/s]')
  plt.xlabel('Time [s]')
  plt.title('Velocity')
  plt.grid()
  plt.tight_layout()

  # Velocity
  plt.figure(2)
  plt.plot(t, velocity[:,1], label=name)
  plt.ylabel('Velocity [ft/s]')
  plt.xlabel('Time [s]')
  plt.title('Velocity')
  plt.grid()
  plt.tight_layout()

  # Launch Rod Velocity
  plt.figure(3)
  rod_velocity = [velocity[i,1] for i in xrange(len(velocity[:,1]))
          if (position[i,1] < 5) & (t[i] < 1)]
  rod_position = [position[i,1] for i in xrange(len(position[:,1]))
          if (position[i,1] < 5) & (t[i] < 1)]
  plt.plot(rod_position, rod_velocity, label=name)
  plt.ylabel('Velocity [ft/s]')
  plt.xlabel('Position on Launch Rod [ft]')
  plt.title('Launch Velocity')
  plt.grid()
  plt.tight_layout()
  
  # Acceleration
  plt.figure(4)
  plt.subplot(211)
  plt.plot(t[0:len(thrust)-4], accel[0:len(thrust)-4,1], label=name)
  plt.ylabel('Acceleration ft/s^2')
  plt.xlabel('Time [s]')
  plt.title(' Acceleration')
  plt.grid()
  plt.subplot(212)
  plt.plot(t[0:len(thrust)], thrust, label=name)
  plt.ylabel('Thrust [lbf]')
  plt.xlabel('Time [s]')
  plt.title(' Thrust')
  plt.grid()
  plt.tight_layout()

  # Drag and Thrust
  plt.figure(5)
  plt.plot(t, drag[:,1], label="Drag")
  plt.plot([t[i] for i in xrange(len(thrust))], thrust, label="Thrust")
  plt.ylabel('Force [lbf]')
  plt.xlabel('Time [s]')
  plt.title('Drag and Thrust')
  lgd = plt.legend()
  plt.grid()
  plt.tight_layout()

  if not export:
    plt.show()

def save_plots(name):
  """ Saves figures 1, 2, and 3 using labels for legend.  These figures must be populated by a call for plot()."""
  fontP = FontProperties()
  fontP.set_size('small')

  fig = plt.figure(1)
  lgd = plt.legend(bbox_to_anchor=(0.91,-0.1), loc="lower right", ncol=3,
            bbox_transform=fig.transFigure,  prop=fontP)
  plt.savefig('../lab3/plots/' + 'Altitude' + '.png',
              bbox_extra_artists=(lgd,), bbox_inches='tight')

  fig = plt.figure(2)
  lgd = plt.legend(bbox_to_anchor=(0.91,-0.1), loc="lower right", ncol=3,
            bbox_transform=fig.transFigure,  prop=fontP)
  plt.savefig('../lab3/plots/' + 'Velocity' + '.png',
              bbox_extra_artists=(lgd,), bbox_inches='tight')

  fig = plt.figure(3)
  lgd = plt.legend(bbox_to_anchor=(0.91,-0.1), loc="lower right", ncol=3,
            bbox_transform=fig.transFigure,  prop=fontP)
  plt.savefig('../lab3/plots/' + 'Acceleration' + '.png',
              bbox_extra_artists=(lgd,), bbox_inches='tight')

