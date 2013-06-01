def fuzzify(raw_rgb):
	# normalizacja z rozciagnieciem histogramu 
	rgbmin = raw_rgb.min()
	shifted = raw_rgb - rgbmin
	return shifted.astype(float) / float(raw_rgb.max() - rgbmin)

def defuzzify(membership, original_rgb):
	# TODO
	return membership

def membership_pass(membership):
	pass
