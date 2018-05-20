######################################
###  Trajectory analysis for 157A  ###
######################################

import sys, getopt
import operator

import pdb
import numpy as np

from trajectory import trajectory, rocket_engine
from mass_estimate import mass_curve
from data_vis import plot, stats, stats_mass_curve, save_plots, stats_table

def main(argv):
  """ Main Function """
  mass = None
  dt = None
  angle = None
  plotting = False
  mode = "trajectory"
  modes = ["trajectory", "mass-curve", "validation", "angle-compare", "stat-table"]

  # This block allows control of the sim from the command line.  Default
  # arguments for mass, dt, angle are found in the trajectory file, but other
  # values can be specifed and passed in from this file.
  try:
    opts, args = getopt.getopt(argv, "hm:t:pa:",
    ["help", "mass=", "time=", "mode=", "plotting", "angle="])
  except getopt.GetoptError:
    sys.exit(2)
  for opt, arg in opts:
    if opt in ('-h', '--help'):
      printHelp(modes)
      sys.exit()
    elif opt in ('-m', '--mass'):
      mass = float(arg)
    elif opt in ('-a', '--angle'):
      angle = float(arg)
    elif opt in ('-t', '--time'):
      dt = float(arg)
    elif opt == '--mode':
      if arg in modes:
        mode = arg
      else:
        print(arg + " is not a valid mode.")
        print("valid modes include:")
        print(modes)
        sys.exit()
    elif opt in ('-p', '--print'):
      plotting = True

  if mode == "trajectory":
    # Calling the trajectory, stat, and plotting functions
    f506_motor = rocket_engine(80., 1.3, 6, 0.096, 0.06)
    t, position, velocity, accel, thrust, drag = trajectory(f506_motor, mass, dt, angle)
    stats(t, position, velocity, accel, thrust, drag) 
    data = np.asarray(position[:,1])
    np.savetxt("launch_data_position.txt", data)
    data = np.asarray(t)
    np.savetxt("launch_data_time.txt", data)
    if plotting:
      plot(t, position, velocity, accel, thrust, drag)

  elif mode == "mass-curve":
    f506_motor = rocket_engine(80., 1.3, 5.3, 0.096, 0.06)
    altitudes = []
    min_mass = 0.05
    max_mass = 0.25
    masses = np.linspace(min_mass,max_mass,20)
    for mass in masses:
      t, position, velocity, accel, thrust, drag = trajectory(f506_motor, mass, dt, angle, Cd1=.25)
      altitudes.append(max(position[:,1]))

    index, altitude = max(enumerate(altitudes), key=operator.itemgetter(1))
    results = trajectory(f506_motor, masses[index])
    results = results + (masses, altitudes)
    stats_mass_curve(*results)
    if plotting:
        plot(*results)

  elif mode == "stat-table":
    angles = range(0,31,5)
    delays = [i/float(4) + 4.0 for i in range(0,13)]
    table_info = []
    for angle, delay in [(angle, delay) for angle in angles for delay in delays]:
      f506_motor = rocket_engine(80., 1.3, delay, 0.096, 0.06)
      results = trajectory(f506_motor, mass, dt, angle)
      results = results + (angle, delay)
      stats_table(*results)
      table_info.append(results)

  elif mode == "validation":
    b64_motor = rocket_engine(5.0, 0.8, 4, 0.0201, 0.01386)
    c63_motor = rocket_engine(10.0, 1.6, 3.0, 0.0249, 0.01242)

    params = [([b64_motor, 0.0672, .01, 5.0, 1.33, 12, 0, 0], "Bullpug No Drag"),               #Bullpug
              ([b64_motor, 0.0672, .01, 5.0, 1.33, 12, 0.5, 1.5], "Bullpug Low Drag"),
              ([b64_motor, 0.0672, .01, 5.0, 1.33, 12, 0.8, 2.0], "Bullpug High Drag"),
              ([c63_motor, 0.1148, .01, 5.0, 1.33, 18, 0, 0], "Amazon No Drag"),                #Amazon
              ([c63_motor, 0.1148, .01, 5.0, 1.33, 18, 0.5, 1.5], "Amazon Low Drag"),
              ([c63_motor, 0.1148, .01, 5.0, 1.33, 18, 1.6, 2.0], "Amazon High Drag"),
              ([b64_motor, 0.0805, .01, 5.0, 1.64, 12, 0, 0], "Big Bertha No Drag"),            #Big Bertha
              ([b64_motor, 0.0805, .01, 5.0, 1.64, 12, 0.5, 1.5], "Big Bertha Low Drag"),
              ([b64_motor, 0.0805, .01, 5.0, 1.64, 12, 0.8, 2.0], "Big Bertha High Drag")]
    for param, name in params:
      t, position, velocity, accel, thrust, drag = trajectory(*param)
      stats(t, position, velocity, accel, thrust, drag, name) 
      if plotting:
        plot(t, position, velocity, accel, thrust, drag, name, True)
        save_plots('Validation')

  elif mode == "angle-compare":
    b64_motor = rocket_engine(5.0, 0.8, 4, 0.0201, 0.01386)

    params = [([b64_motor, 0.0672, .01, 0., 1.33, 12, 0.8, 2.0], "Bullpug Zero Degree"),
              ([b64_motor, 0.0672, .01, 10.0, 1.33, 12, 0.8, 2.0], "Bullpug Ten Degree")]
    for param, name in params:
      t, position, velocity, accel, thrust, drag = trajectory(*param)
      stats(t, position, velocity, accel, thrust, drag, name) 
      if plotting:
        plot(t, position, velocity, accel, thrust, drag, name, True)
        save_plots('Angle Compare')

def printHelp(modes):
    print("MAE 157A Python Codebase\n")
    print("Arguments")
    print("\t--mode <mode>")
    print("\t\tModes include: " + '[%s]' % ', '.join(map(str, modes)))
    print("\t-m, --mass <mass>")
    print("\t\tMass in kilograms to be used in simulation")
    print("\t-t, --time <dt>")
    print("\t\tSpecifify a time step for euler approximation (seconds)")
    print("\t-a, --angle <angle>")
    print("\t\tLaunch angle to be used in simulation (degrees). Default value is 0.")
    print("\t-p, --print")
    print("\t\tPrint graphs of results.")


if __name__ == '__main__':
  main(sys.argv[1:])
