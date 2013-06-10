import numpy
from scipy import ndimage

smooth_mx = numpy.array([
    [0, 0.25, 0],
    [0.25, 0, 0.25],
    [0, 0.25, 0]
])


def fuzzify(raw_rgb):
    """Fuzyfikuje macierz wektorow RGB lub 8-bitowych odcieni szarosci"""
    # normalizacja z rozciagnieciem histogramu
    rgbmin = raw_rgb.min()
    shifted = raw_rgb - rgbmin
    normalized = shifted.astype(float) / float(raw_rgb.max() - rgbmin)
    if normalized.ndim == 3:
        # konwertuj macierz wektorow RGB na macierz poziomow szarosci
        return normalized.sum(axis=2) / 3.0
    else:
        return normalized


def defuzzify(membership, original_rgb):
    """Odtwarza macierz 8-bitowych odcieni szarosci"""
    return (membership * 255).astype(numpy.uint8)


def membership_pass(membership, intensify_passes=1, convolve=True, second_intensify_passes=1, threshold=0.5, power=2):
    """Modyfikuje wartosci przynaleznosci wedlug algorytmu ulepszania obrazu"""
    for i in xrange(1, intensify_passes + 1):
        membership = intensify(membership, threshold, power)
    if convolve:
        membership = ndimage.convolve(membership, smooth_mx)
        for i in xrange(1, second_intensify_passes + 1):
            membership = intensify(membership, threshold, power)
    return membership


def intensify(membership, threshold, power):
    res = numpy.zeros_like(membership)
    res[membership <= threshold] = (1 / threshold) * membership[membership <= threshold] ** power
    res[membership > threshold] = 1 - (1 / threshold) * (1.0 - membership[membership > threshold]) ** power
    return res
