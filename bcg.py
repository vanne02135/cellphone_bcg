#!/usr/bin/python

import sys
import numpy as np
import scipy.signal
from matplotlib import pylab

def readData(filename):
	raw = open(filename).read()
	ti = 0
	x = []
	y = []
	z = []

	t = []
	for row in raw.split("\n"):
		if row.strip().startswith("#"):
			continue
		
		if row.count(" ") == 3:
			a_x, a_y, a_z, dt = row.split()
			ti += float(dt)
			x.append(float(a_x))
			y.append(float(a_y))
			z.append(float(a_z))
			t.append(ti)

	return np.array(x), np.array(y), np.array(z), np.array(t)/1000.0

if __name__ == "__main__":
	x, y, z, t = readData(sys.argv[1])
	z = scipy.signal.detrend(z[500:2500])
	t = t[500:2500]

	z_detrend = scipy.signal.detrend(z, bp=range(0, len(z), 20))
	f, P = scipy.signal.welch(z_detrend, 1 / np.mean(np.diff(t)))

	pylab.plot(t, z_detrend)
	pylab.show()

	pylab.plot(f, P)
	pylab.show()

