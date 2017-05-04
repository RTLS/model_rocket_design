######################################
###  Trajectory analysis for 157A  ###
######################################

import sys, getopt

import pdb

from trajectory import trajectory, rocket_engine
from mass_estimate import mass_curve
from data_vis import plot, stats, stats_mass_curve

def main(argv):
  """ Main Function """
  mass = None
  dt = None
  angle = None
  plotting = False
  mode = "trajectory"
  modes = ["trajectory", "mass-curve", "validation"]

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
      print("Help coming soon")
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
    g407_motor = rocket_engine(97.14, 2.3, 9.0, 0.1234, 0.0607)
    t, position, velocity, accel, thrust, drag = trajectory(g407_motor, mass, dt, angle)
    stats(t, position, velocity, accel, thrust, drag) 
    if plotting:
      plot(t, position, velocity, accel, thrust)
  elif mode == "mass-curve":
    t, position, velocity, accel, thrust, masses, altitudes = mass_curve()
    stats_mass_curve(t, position, velocity, accel, thrust, masses, altitudes) 
  elif mode == "validation":
    g407_motor = rocket_engine(97.14, 2.3, 9.0, 0.1234, 0.0607)
    b64_motor = rocket_engine(5.0, 0.8, 4, 0.0201, 0.01386)
    c63_motor = rocket_engine(10.0, 1.6, 3.0, 0.0249, 0.01242)

    params = [([g407_motor, .2300, .001, 5.0, 2.0, 20.0,0.75, 1.5], None),    #Validtion
              ([b64_motor, 0.0672, .001, 5.0, 1.33, 12, 0, 0], "Bullpug No Drag"),           #Bullpug
              ([b64_motor, 0.0672, .001, 5.0, 1.33, 12, 0.5, 1.5], "Bullpug Low Drag"),
              ([b64_motor, 0.0672, .001, 5.0, 1.33, 12, 0.8, 2.0], "Bullpug High Drag"),
              ([c63_motor, 0.1148, .001, 5.0, 1.33, 18, 0, 0], "Amazon No Drag"),           #Amazon
              ([c63_motor, 0.1148, .001, 5.0, 1.33, 18, 0.5, 1.5], "Amazon Low Drag"),
              ([c63_motor, 0.1148, .001, 5.0, 1.33, 18, 1.6, 2.0], "Amazon High Drag"),
              ([b64_motor, 0.0805, .001, 5.0, 1.64, 12, 0, 0], "Big Bertha No Drag"),
              ([b64_motor, 0.0805, .001, 5.0, 1.64, 12, 0.5, 1.5], "Big Bertha Low Drag"),
              ([b64_motor, 0.0805, .001, 5.0, 1.64, 12, 0.8, 2.0], "Big Bertha High Drag")]
    for param, name in params:
      t, position, velocity, accel, thrust, drag = trajectory(*param)
      stats(t, position, velocity, accel, thrust, drag, name) 
      if plotting:
        plot(t, position, velocity, accel, thrust, name)

if __name__ == '__main__':
  main(sys.argv[1:])
