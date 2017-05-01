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
  modes = ["trajectory", "mass-curve"]

  # This block allows control of the sim from the command line.  Default
  # arguments for mass, dt, angle are found in the trajectory file, but other
  # values can be specifed and passed in from this file.
  try:
    opts, args = getopt.getopt(argv, "hm:t:pa:", ["help", "mass=", "time=", "mode=", "plotting", "angle="])
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

if __name__ == '__main__':
  main(sys.argv[1:])
