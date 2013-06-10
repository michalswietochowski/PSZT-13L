#!/usr/bin/python2

import sys

# wczytywanie i przetwarzanie obrazow w tablicach numpy
from scipy import misc, ndimage

# nasze przetwarzanie rozmyte
from fuzzy import fuzzify, membership_pass, defuzzify


def process_image(input_path, output_path, pass_count=1, intensify_passes=1, convolve=True, second_intensify_passes=1,
                  threshold=0.5, power=2):
    raw_rgb = misc.imread(input_path)
    membership = fuzzify(raw_rgb)
    for pass_num in xrange(1, pass_count + 1):
        membership = membership_pass(membership, intensify_passes, convolve, second_intensify_passes, threshold, power)
    result_rgb = defuzzify(membership, raw_rgb)
    misc.imsave(output_path, result_rgb)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('usage: %s input_path output_path' % sys.argv[0])
    process_image(sys.argv[1], sys.argv[2])