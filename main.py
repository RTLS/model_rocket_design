######################################
###  Trajectory analysis for 157A  ###
######################################

import sys, getopt

import pdb

from trajectory import trajectory
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
    t, position, velocity, accel, thrust = trajectory(mass, dt, angle)
    stats(t, position, velocity, accel, thrust) 
    if plotting:
      plot(t, position, velocity, accel, thrust)
  elif mode == "mass-curve":
    t, position, velocity, accel, thrust, masses, altitudes = mass_curve()
    stats_mass_curve(t, position, velocity, accel, thrust, masses, altitudes) 
  elif mode == "validation":
    params = [([0.2300, .001, 5.0, 2.0, 20.0,0.75, 1.5, 97.14, 2.3, 9.0], None),    #Validtion
              ([0.0672, .001, 5.0, 1.33, 12, 0, 0, 5.0, 0.8, 4.0], "Bullpug No Drag"),           #Bullpug
              ([0.0672, .001, 5.0, 1.33, 12, 0.5, 1.5, 5.0, 0.8, 4.0], "Bullpug Low Drag"),
              ([0.0672, .001, 5.0, 1.33, 12, 0.8, 2.0, 5.0, 0.8, 4.0], "Bullpug High Drag"),
              ([0.1148, .001, 5.0, 1.33, 18, 0, 0, 10.0, 1.6, 6.0], "Amazon No Drag"),           #Amazon
              ([0.1148, .001, 5.0, 1.33, 18, 0.5, 1.5, 10.0, 1.6, 6.0], "Amazon Low Drag"),
              ([0.1148, .001, 5.0, 1.33, 18, 1.6, 2.0, 10.0, 1.6, 6.0], "Amazon High Drag"),
              ([0.0805, .001, 5.0, 1.64, 12, 0, 0, 5.0, 0.8, 4.0], "Big Bertha No Drag"),
              ([0.0805, .001, 5.0, 1.64, 12, 0.5, 1.5, 5.0, 0.8, 4.0], "Big Bertha Low Drag"),
              ([0.0805, .001, 5.0, 1.64, 12, 0.8, 2.0, 5.0, 0.8, 4.0], "Big Bertha High Drag")]
    pdb.set_trace()
    for param, name in params:
      t, position, velocity, accel, thrust = trajectory(*param)
      stats(t, position, velocity, accel, thrust, name) 
      if plotting:
        plot(t, position, velocity, accel, thrust, name)

if __name__ == '__main__':
  main(sys.argv[1:])
