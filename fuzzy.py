import numpy
from scipy import ndimage

smooth_mx = numpy.array([
	[0,    0.25, 0   ],
	[0.25, 0,    0.25],
	[0,    0.25, 0   ]
])

def fuzzify(raw_rgb):
	'''Fuzyfikuje macierz wektorow RGB lub 8-bitowych odcieni szarosci'''
	# normalizacja z rozciagnieciem histogramu 
	rgbmin = raw_rgb.min()
	shifted = raw_rgb - rgbmin
	normalized = shifted.astype(float) / float(raw_rgb.max() - rgbmin)
	if normalized.ndim == 3:
		# konwertuj macierz wektorow RGB na macierz poziomow szarosci
		return normalized.sum(axis = 2) / 3.0
	else:
		return normalized

def defuzzify(membership, original_rgb):
	'''Odtwarza macierz 8-bitowych odcieni szarosci'''
	return (membership * 255).astype(numpy.uint8)

def membership_pass(membership):
	'''Modyfikuje wartosci przynaleznosci wedlug algorytmu ulepszania obrazu'''
	membership = intensify(membership)
	membership = ndimage.convolve(membership, smooth_mx)
	return intensify(membership)

def intensify(membership):
	res = numpy.zeros_like(membership)
	res[membership <= 0.5] = 2 * membership[membership <= 0.5]**2
	res[membership > 0.5] = 1 - 2 * (1.0 - membership[membership > 0.5])**2
	return res

