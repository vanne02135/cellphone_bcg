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

def lowpass(s, f):
	b = scipy.signal.firwin(100, f)
	return scipy.signal.lfilter(b, 1, s)


if __name__ == "__main__":
	x, y, z, t = readData(sys.argv[1])
	z = scipy.signal.detrend(z[500:2500])
	t = t[500:2500]

	z_detrend = scipy.signal.detrend(z, bp=range(0, len(z), 20))
	f, P = scipy.signal.welch(z_detrend, 1 / np.mean(np.diff(t)))

	pylab.subplot(3, 1, 1)
	pylab.plot(t, z_detrend)
	pylab.title("Detrended z-acceleration")
	pylab.xlabel("t (s)")


	pylab.subplot(3, 1, 2)
	pylab.plot(f, P)
	pylab.title("Welch freq estimation")
	pylab.xlabel("f (Hz)")

	pylab.subplot(3, 1, 3)
	pylab.plot(t, lowpass(z_detrend**2, 0.1))
	pylab.title("Squared and low passed signal for HR estimation")
	pylab.xlabel("t (s)")
	pylab.show()

