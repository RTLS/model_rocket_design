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
    ["help", "mass=", "time=", "mode=", "plotting", "angle=",
    "Cd1=", "Cd2=", "OD=", "chute-diam=", "impulse=", "burn_time=", "delay="])
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
    elif opt == '--Cd1': 
      Cd1 = float(arg)
    elif opt == '--Cd2': 
      Cd2 = float(arg)
    elif opt == '--OD': 
      OD = float(arg)
    elif opt == '--chute-diam': 
      chute_diam = float(arg)
    elif opt == '--impulse': 
      impulse = float(arg)

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
    params = [OD, chute_diam, Cd1, Cd2, impulse, 2.3, 9.0]
    pdb.set_trace()
    t, position, velocity, accel, thrust = trajectory(mass, dt, angle, *params)
    stats(t, position, velocity, accel, thrust) 
    if plotting:
      plot(t, position, velocity, accel, thrust)

if __name__ == '__main__':
  main(sys.argv[1:])
