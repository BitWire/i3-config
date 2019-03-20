#!/usr/bin/env python

import sys, re, time, math
#import dbus
import os

# hdaps input file
POS_FILE = '/sys/devices/platform/hdaps/position'
# regex to gather hdaps values
POS_RX = re.compile('^\((-?\d+),(-?\d+)\)$')

# invert x and y axis (True or False)
INVERT_AXIS = False

# interval to pause between hdaps reads
INTERVAL = 0.01

# length of the short term buffer (same value will be used for x and y buffers)
ST_LENGTH = 20
# short term standard deviation threshold for x
ST_X_STDDEV_THRESHOLD = 1
# short term standard deviation threshold for y
ST_Y_STDDEV_THRESHOLD = 1
# short term threshold for x (0 to disable x axis knocks)
ST_X_THRESHOLD = 2
# short term threshold for y (0 to disable y axis knocks)
ST_Y_THRESHOLD = 2

# length of the long term buffer (same value will be used for x and y buffers)
LT_LENGTH = 6
# long term standard deviation threshold for x
LT_X_STDDEV_THRESHOLD = 2
# long term standard deviation threshold for y
LT_Y_STDDEV_THRESHOLD = 2

# Debug (0 to 4) 0=no output
DEBUG = 1

# END OF CONFIG SECTION

# dbus init
#bus = dbus.SessionBus()
#kwin = bus.get_object('org.kde.kwin','/KWin')

def switch_to_workspace_at_right():
# cdb.py is the compiz-send.py script from http://wiki.compiz.org/Plugins/Dbus
  os.system('/full/path/cdb.py wall next_key')
#  Use the rotate commands for desktop cube rotations
#  os.system('/full/path/cdb.py rotate rotate_right_key')
#  kwin.nextDesktop()

def switch_to_workspace_at_left():
# cdb.py is the compiz-send.py script from http://wiki.compiz.org/Plugins/Dbus
  os.system('/full/path/cdb.py wall prev_key')
#  Use the rotate commands for desktop cube rotations
#  os.system('/full/path/cdb.py rotate rotate_left_key')
#  kwin.previousDesktop()

def launch_x_left():
  debug("X-Left",1)
#  switch_to_workspace_at_left()
def launch_x_right():
  debug("X-Right",1)
#  switch_to_workspace_at_right()
def launch_y_front():
  debug("Y-Front",1)
def launch_y_back():
  debug("Y-Back",1)
def launch_x_left_y_front():
  debug("X-Left Y-Front",1)
#  switch_to_workspace_at_left()
def launch_x_left_y_back():
  debug("X-Left Y-Back",1)
#  switch_to_workspace_at_left()
def launch_x_right_y_front():
  debug("X-Right Y-Front",1)
#  switch_to_workspace_at_right()
def launch_x_right_y_back():
  debug("X-Right Y-Back",1)
#  switch_to_workspace_at_right()

def get_pos():
  pos = open(POS_FILE).read()
  match = POS_RX.match(pos)
  return (int(match.group(1)), int(match.group(2)))

def loop():
  st_x = [0] * ST_LENGTH
  st_y = [0] * ST_LENGTH
  st_x_idx = 0
  st_y_idx = 0
  
  lt_x = [0] * LT_LENGTH
  lt_y = [0] * LT_LENGTH
  lt_x_idx = 0
  lt_y_idx = 0
  
  lt_x_stable = False
  lt_y_stable = False

  while True:
    if INVERT_AXIS:
      y, x = get_pos()
    else:
      x, y = get_pos()
    
    st_x[st_x_idx] = x
    st_y[st_y_idx] = y
    
    if stddev(lt_x) < LT_X_STDDEV_THRESHOLD and stddev(lt_y) < LT_Y_STDDEV_THRESHOLD:
      if not lt_x_stable or not lt_y_stable:
	debug("Stable",1)
	lt_x_stable = True
	lt_y_stable = True

      # Split short term buffer into older and newer values
      old_x = []
      old_y = []
      new_x = []
      new_y = []
      for i in range(ST_LENGTH / 2):
	old_x.append(st_x[(st_x_idx + i + 1) % ST_LENGTH])
	old_y.append(st_y[(st_y_idx + i + 1) % ST_LENGTH])
	new_x.append(st_x[(st_x_idx + i + 1 + ST_LENGTH / 2) % ST_LENGTH])
	new_y.append(st_y[(st_y_idx + i + 1 + ST_LENGTH / 2) % ST_LENGTH])
      
      # Add some older stable data to new array, to make sure it's gone
      # back to the same stable state rather than a new one
      for i in range(ST_LENGTH / 2 + 1, ST_LENGTH):
	new_x.append(lt_x[(lt_x_idx + i) % LT_LENGTH])
	new_y.append(lt_y[(lt_y_idx + i) % LT_LENGTH])

      if (stddev(new_x) < ST_X_STDDEV_THRESHOLD) and (stddev(new_y) < ST_Y_STDDEV_THRESHOLD):
	st_x_mean = mean(st_x)
	st_y_mean = mean(st_y)
	debug("Max x: " + str(max(old_x)) + " > " + str(st_x_mean + ST_X_THRESHOLD) + \
	      " Min x: " + str(min(old_x)) + " < " + str(st_x_mean - ST_X_THRESHOLD) + \
	      " SD x: " + str(stddev(new_x)) + " < " + str(ST_X_STDDEV_THRESHOLD),4)
	debug("Max y: " + str(max(old_y)) + " < " + str(st_y_mean + ST_Y_THRESHOLD) + \
	      " Min y: " + str(min(old_y)) + " > " + str(st_y_mean - ST_Y_THRESHOLD) + \
	      " SD y: " + str(stddev(new_y)) + " < " + str(ST_Y_STDDEV_THRESHOLD),4)
	max_x_idx = -1
	max_y_idx = -1
	min_x_idx = -1
	min_y_idx = -1

	# Heartbeat
	for i in range(len(old_y)):
	  if ST_X_THRESHOLD != 0:
	    if old_x[i] > st_x_mean + ST_X_THRESHOLD:
	      max_x_idx = i;
	    if old_x[i] < st_x_mean - ST_X_THRESHOLD:
	      min_x_idx = i;
	  if ST_Y_THRESHOLD != 0:
	    if old_y[i] > st_y_mean + ST_Y_THRESHOLD:
	      max_y_idx = i;
	    if old_y[i] < st_y_mean - ST_Y_THRESHOLD:
	      min_y_idx = i;

	# Check knock directions and launch associated commands
	if max_x_idx != -1 and min_x_idx != -1 or max_y_idx != -1 and min_y_idx != -1:
	  if max_x_idx == min_x_idx and max_y_idx >= min_y_idx:
	    debug("Smack! X-Disabled or stable x=" + str(old_x[max_x_idx]) + "/" + str(old_x[min_x_idx]) + \
		  " Y-Front y=" + str(old_y[max_y_idx]) + "/" + str(old_y[min_y_idx]),2)
	    launch_y_front()
	  if max_x_idx == min_x_idx and max_y_idx <= min_y_idx:
	    debug("Smack! X-Disabled or stable x=" + str(old_x[max_x_idx]) + "/" + str(old_x[min_x_idx]) + \
		  " Y-Back y=" + str(old_y[max_y_idx]) + "/" + str(old_y[min_y_idx]),2)
	    launch_y_back()
	  if max_x_idx >= min_x_idx and max_y_idx == min_y_idx:
	    debug("Smack! X-Right x=" + str(old_x[max_x_idx]) + "/" + str(old_x[min_x_idx]) + \
		  " Y-Disabled or stable y=" + str(old_y[max_y_idx]) + "/" + str(old_y[min_y_idx]),2)
	    launch_x_right()
	  if max_x_idx < min_x_idx and max_y_idx == min_y_idx:
	    debug("Smack! X-Left x=" + str(old_x[max_x_idx]) + "/" + str(old_x[min_x_idx]) + \
		  " Y-Disabled or stable y=" + str(old_y[max_y_idx]) + "/" + str(old_y[min_y_idx]),2)
	    launch_x_left()
	  if max_x_idx > min_x_idx and max_y_idx > min_y_idx:
	    debug("Smack! X-Right x=" + str(old_x[max_x_idx]) + "/" + str(old_x[min_x_idx]) + \
		  " Y-Front y=" + str(old_y[max_y_idx]) + "/" + str(old_y[min_y_idx]),2)
	    launch_x_right_y_front()
	  if max_x_idx < min_x_idx and max_y_idx < min_y_idx:
	    debug("Smack! X-Left x=" + str(old_x[max_x_idx]) + "/" + str(old_x[min_x_idx]) + \
		  " Y-Back y=" + str(old_y[max_y_idx]) + "/" + str(old_y[min_y_idx]),2)
	    launch_x_left_y_back()
	  if max_x_idx < min_x_idx and max_y_idx > min_y_idx:
	    debug("Smack! X-Left x=" + str(old_x[max_x_idx]) + "/" + str(old_x[min_x_idx]) + \
		  " Y-Front y=" + str(old_y[max_y_idx]) + "/" + str(old_y[min_y_idx]),2)
	    launch_x_left_y_front()
	  if max_x_idx > min_x_idx and max_y_idx < min_y_idx:
	    debug("Smack! X-Right x=" + str(old_x[max_x_idx]) + "/" + str(old_x[min_x_idx]) + \
		  " Y-Back y=" + str(old_y[max_y_idx]) + "/" + str(old_y[min_y_idx]),2)
	    launch_x_right_y_back()

	  # No further smacks for a while; bias long-term stddev
	  #lt_x[(lt_x_idx + LT_LENGTH - 1) % LT_LENGTH] = 10000000;
	  lt_y[(lt_y_idx + LT_LENGTH - 1) % LT_LENGTH] = 10000000;
    else:
      if lt_x_stable or lt_y_stable:
        debug("Unstable",1)
	lt_x_stable = False
	lt_y_stable = False

    st_x_idx += 1
    st_x_idx %= ST_LENGTH
    st_y_idx += 1
    st_y_idx %= ST_LENGTH

    if st_x_idx == 0:
      lt_x[lt_x_idx] = st_x[st_x_idx]
      lt_x_idx += 1
      lt_x_idx %= LT_LENGTH
      debug("X Stability stddev: " + str(stddev(lt_x)),3)
    if st_y_idx == 0:
      lt_y[lt_y_idx] = st_y[st_y_idx]
      lt_y_idx += 1
      lt_y_idx %= LT_LENGTH
      debug("Y Stability stddev: " + str(stddev(lt_y)),3)

    time.sleep(INTERVAL)

def debug(param, level):
  # show the message depending on the DEBUG level
  if level <= DEBUG:
    print param

def mean(values):
  # average of the values
  return sum(values) / float(len(values))

def stddev(values):
  # standard deviation of the values
  meanval = mean(values)
  return math.sqrt(sum((x - meanval)**2 for x in values) / (len(values)-1))

def main():
  try:
    loop()
  except KeyboardInterrupt:
    pass

if __name__ == '__main__':
  main()
