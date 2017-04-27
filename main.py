import sys, getopt

import pdb

from trajectory import trajectory
from data_vis import plot, stats

def main(argv):
  """ Main Function """
  mass = None
  dt = None
  angle = None
  plotting = False

  #pdb.set_trace()

  try:
    opts, args = getopt.getopt(argv, "hm:t:pa:", ["help", "mass", "time", "mode", "plotting", "angle"])
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
    elif opt is '--mode':
      print('Modes coming soon, I swear!')
    elif opt in ('-p', '--print'):
      plotting = True

  t, position, velocity, accel, thrust = trajectory(mass, dt, angle)
  stats(t, position, velocity, accel, thrust) 
  if plotting:
    plot(t, position, velocity, accel, thrust)

if __name__ == '__main__':
  main(sys.argv[1:])
