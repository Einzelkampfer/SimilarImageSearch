# !/usr/bin/python
# -*- coding:utf-8 -*-

import os, sys
import numpy
import time
from basic import *

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
	print "Calculate covariance done"
	return covariance

def calPmatrix(bitNum, covariance):
	startClock = time.time()
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
	# print str(1.0 * sum(eigenvalue[:k]) / sum(eigenvalue))
	writeMatrixToFile(pmatrixFile, P)
	print "Calculate P matrix done, time used %f seconds" % (endClock - startClock)
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

def buildPca():
	if not os.path.exists(pcaResultFile):
		if not checkSplitDone():
			splitColumn(featureFile, featureNum)
		if not os.path.exists(covarianceFileName):
			covariance = calCovarianceMat(featureNum)
		else:
			covariance = readMatrixFromFile(covarianceFileName)
			covariance = numpy.mat(covariance)
		if not os.path.exists(pmatrixFile):
			P = calPmatrix(256, covariance)
		else:
			P = readMatrixFromFile(pmatrixFile)
		pcaMulti(centralizedFile, P, pcaFile)
	print "PCA done"
	os.system("rm %s" % covariance)
	os.system("rm %s" % centralizedFile)
	os.system("rm [0-9]*.txt")

# if __name__ == "__main__":
# 	buildPca()