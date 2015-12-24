# !/usr/bin/python
# -*- coding:utf-8 -*-

import os, sys
import numpy
import time
from basicio import *

def calCovarianceMat(featureNum):
	covariance = []
	for i in range(featureNum):
		covariance.append([0.0] * featureNum)
	buffSize = 64
	for i in range(featureNum / buffSize):
		indexStart = i * buffSize
		data = []
		for j in range(buffSize):
			col = readColFile(indexStart + j)
			if len(data) == 0:
				for k in range(len(col)):
					data.append([])
			for k in range(len(col)):
				data[k].append(col[k])
		for k in range(buffSize):
			for l in range(len(data)):
				data[l].append(0.0)
		data = numpy.mat(data)
		for j in range(i, featureNum / buffSize):
			print "covariance between block %d and block %d" % (i, j)
			s = time.time()
			for k in range(buffSize):
				col = readColFile(j * buffSize + k)
				for l in range(len(col)):
					data[l, k + buffSize] = col[l]
			cov = numpy.cov(data, rowvar = 0)
			for k in range(buffSize):
				for l in range(buffSize, buffSize * 2):
					x = k + indexStart
					y = l - buffSize + j * buffSize
					covariance[x][y] = cov[k, l]
					covariance[y][x] = covariance[x][y]
			e = time.time()
			sys.stdout.write("time used:%f seconds\n" % (e - s))
	writeMatrixToFile(covarianceFileName, covariance)
	covariance = numpy.mat(covariance)
	return covariance

def calPmatrix(bitNum, covariance):
	# Calculate eigenvectors and eigenvalues of covariance matrix
	eigenvalue, eigenvector = numpy.linalg.eig(covariance)

	# Sort eigenvectors together with its corresponding eigenvalues
	index = numpy.argsort(-eigenvalue)
	eigenvalue = eigenvalue[index]
	eigenvector = eigenvector[:, index]
	
	# Choose first k rows of eigenvectors
	k = bitNum
	index = index[:k]
	P = eigenvector[:, index]
	print str(1.0 * sum(eigenvalue[:k]) / sum(eigenvalue))
	writeMatrixToFile(pmatrixFile, P)
	return P

def pcaMulti(matFile, P, outputFile):
	fileObj = open(matFile, "r")
	outObj = open(outputFile, "w")
	line = fileObj.readline()
	count = 1
	data = []
	imgName = []
	while True:
		if not line:
			break
		items = line.strip().split(',')
		imgPath = items[0]
		imgName.append(imgPath)
		items = items[1:]
		for i in range(len(items)):
			items[i] = float(items[i])
		data.append(items)
		if len(data) == 50000:
			data = numpy.mat(data)
			result = data * P
			row, col = result.shape
			for i in range(row):
				outObj.write("%s," % imgName[i])
				for j in range(col):
					outObj.write("%f" % result[i, j])
					if j != col - 1:
						outObj.write(",")
				outObj.write("\n")
			data = []
			imgName = []
		count += 1
		line = fileObj.readline()
	if len(data) != 0:
		data = numpy.mat(data)
		result = data * P
		row, col = result.shape
		for i in range(row):
			outObj.write("%s," % imgName[i])
			for j in range(col):
				outObj.write("%f" % result[i, j])
				if j != col - 1:
					outObj.write(",")
			outObj.write("\n")
		data = []
	outObj.close()

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

if __name__ == '__main__':
	# featureNum = 1024
	# splitDone = True
	# for i in range(featureNum):
	# 	if not os.path.exists("%d.txt" % i):
	# 		splitDone = False
	# if not splitDone:
	# 	splitColumn(featureFile, featureNum)
	# print "split file done"
	# if not os.path.exists(covarianceFileName):
	# 	covariance = calCovarianceMat(featureNum)
	# else:
	# 	covariance = readMatrixFromFile(covarianceFileName)
	# 	covariance = numpy.mat(covariance)
	# print "Calculate covariance done"
	# if not os.path.exists(pmatrixFile):
	# 	startClock = time.time()
	# 	P = calPmatrix(256, covariance)
	# 	endClock = time.time()
	# 	print "Calculate P matrix done, time used %f seconds" % (endClock - startClock)
	# else:
	# 	P = readMatrixFromFile(pmatrixFile)
	# if not os.path.exists(pcaResultFile):
	# 	pcaMulti(centralizedFile, P, pcaFile)
	# if not os.path.exists(itqResultFile):
	# 	matrix = readMatrixFromFile(pcaResultFile, haveImgPath=True)
	# 	matrix = numpy.mat(matrix)
	# 	print "PCA done"
	# 	startClock = time.time()
	# 	B, R = itq(matrix, 50)
	# 	endClock = time.time()
	# 	print "ITQone, time used:%f seconds" % (endClock - startClock)
	# 	writeMatrixToFile(itqResultFile, B)
	# 	writeMatrixToFile(rmatrixFile, R)
	if not os.path.exists(binarySearchFile):
		popen("./convertBinary.bin %s" % itqResultFile)

