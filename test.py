#!/usr/bin/python2

import os, os.path, glob, improc

if __name__ == '__main__':
	if not os.path.exists('testout'):
		os.makedirs('testout')
	for testin in glob.glob('testin%s*.png' % os.sep):
		improc.process_image(
				testin,
				'testout%s%s' % (os.sep, os.path.basename(testin)))
