import numpy

def fuzzify(raw_rgb):
	# normalizacja z rozciagnieciem histogramu 
	rgbmin = raw_rgb.min()
	shifted = raw_rgb - rgbmin
	return shifted.astype(float) / float(raw_rgb.max() - rgbmin)

def defuzzify(membership, original_rgb):
	# TODO
	return membership

def membership_pass(membership):
	return intensify(membership)

def intensify(membership, threshold = 0.5):
	res = numpy.zeros_like(membership)
	res[membership <= 0.5] = 2 * membership[membership <= 0.5]**2
	res[membership > 0.5] = 1 - 2 * (1.0 - membership[membership > 0.5])**2
	return res

