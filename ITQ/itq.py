# !/usr/bin/python
# -*- coding:utf-8 -*-

import os, sys
import numpy
import time
from basic import *
from pca import *

def itq(matrix, iterationTime):
	# Initialize a orthogonal random rotation matrix R
	samplesize, bitNum = matrix.shape
	# Gaussian distribution of mean 0 and variance 1
	R = numpy.random.randn(bitNum, bitNum)
	U, V2, S2 = numpy.linalg.svd(R)
	R = U[:, range(0, bitNum)]
	# Fix and Update iterations
	for i in range(iterationTime):
		startTime = time.time()
		print 'Iteration %d' % (i + 1) 
		# Fix R and update B(UX)
		Z = matrix * R
		row, col = Z.shape
		UX = numpy.ones((row, col)) * -1
		UX[Z >= 0] = 1
		del(Z)
		# Fix B and update R
		C = UX.T * matrix
		UB, sigma, UA = numpy.linalg.svd(C)
		R = UA * UB.T
		endTime = time.time()
		print "time used:%f seconds" % (endTime - startTime)
	Z = matrix * R
	row, col = Z.shape
	UX = numpy.ones((row, col)) * -1
	UX[Z >= 0] = 1
	del(Z)
	# Transform into binary code
	UX[UX < 0] = 0
	UX = UX.astype(int)
	return (UX, R)

def build():
	if os.path.exists(binarySearchFile):
		return
	else:
		if not os.path.exists(itqResultFile):
			buildPca()
			matrix = readMatrixFromFile(pcaResultFile, haveImgPath=True)
			matrix = numpy.mat(matrix)
			startClock = time.time()
			B, R = itq(matrix, 50)
			endClock = time.time()
			print "ITQone, time used:%f seconds" % (endClock - startClock)
			writeMatrixToFile(itqResultFile, B)
			writeMatrixToFile(rmatrixFile, R)
		os.system("./convertBinary.bin %s" % itqResultFile)
		os.system("rm %s" % itqResultFile)

if __name__ == "__main__":
	if len(sys.argv) >= 2:
		if (sys.argv[1] == "build"):
			build()

	

