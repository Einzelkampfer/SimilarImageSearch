# !/usr/bin/python
# -*- coding:utf-8 -*-

import os, sys
import numpy
import time

tempDirName = "../../temp"
covarianceFileName = "covariance.txt"
centralizedFile = "centralized.txt"
meanFile = "mean.txt"
featureFile = "../../features.txt"
pmatrixFile = "pmatrix.txt"
pcaResultFile = "pcaresult.txt"

def readMatrixFromFile(filename, haveImgPath=False):
	fileObj = open(filename, "r")
	content =  fileObj.read().strip()
	content = content.split('\n')
	for i in range(len(content)):
		content[i] = content[i].split(',')
		if haveImgPath:
			content[i] = content[i][1:]
		for j in range(len(content[i])):
			content[i][j] = float(content[i][j])
	return content

def writeMatrixToFile(filename, matrix):
	fileObj = open(filename, "w")
	if isinstance(matrix, (numpy.matrixlib.defmatrix.matrix)):
		row, col = matrix.shape
		for i in range(row):
			for j in range(col):
				fileObj.write(str(matrix[i, j]))
				if j != col - 1:
					fileObj.write(",")
			fileObj.write("\n")
	else:
		for row in matrix:
			for i in range(len(row)):
				fileObj.write(str(row[i]))
				if i != len(row) - 1:
					fileObj.write(",")
			fileObj.write("\n")
	fileObj.close()

def splitColumn(fileName, colNum):
	if not os.path.exists(tempDirName):
		os.mkdir(tempDirName)
	indexStart = 0
	buffSize = 128
	meanObj = open("%s/%s" % (tempDirName, meanFile), "w")
	while indexStart < colNum:
		sys.stdout.write("dealing from col %d to col %d\n" % (indexStart, indexStart + buffSize - 1))
		s = time.time()
		fileObj = open(fileName, "r")
		line = fileObj.readline()
		data = []
		while True:
			if not line:
				break
			items = line.strip().split(",")
			row = []
			for k in range(indexStart + 1, indexStart + buffSize + 1):
				f = float(items[k])
				row.append(f)
			data.append(row)
			line = fileObj.readline()
		data = numpy.mat(data)
		row, col = data.shape
		for i in range(col):
			meanObj.write("%f\n" % data[:, i].mean())
			data[:, i] -= data[:, i].mean()

		for i in range(indexStart, indexStart + buffSize):
			tempObj = open("%s/%d.txt" % (tempDirName, i), "w")
			for j in range(row):
				tempObj.write(str(data[j, i - indexStart]) + "\n")
		e = time.time()
		sys.stdout.write("time used:%f seconds\n" % (e - s))
		indexStart += buffSize
		tempObj.close()
		fileObj.close()
	meanObj.close()

def readColFile(num):
	fileObj = open("%s/%d.txt" % (tempDirName, num), "r")
	content = fileObj.read().strip().split("\n")
	for i in range(len(content)):
		content[i] = float(content[i])
	return content

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
	writeMatrixToFile("%s/%s" % (tempDirName, covarianceFileName), covariance)
	covariance = numpy.mat(covariance)
	return covariance

def calPmatrix(bitNum, covariance):
	# Calculate eigenvectors and eigenvalues of covariance matrix
	eigenvalue, eigenvector = numpy.linalg.eig(covariance)

	# Sort eigenvectors together with its corresponding eigenvalues
	index = numpy.argsort(-eigenvalue)
	eigenvalue = eigenvalue[index]
	eigenvector = eigenvector[:, index]
	
	# # Choose first k rows of eigenvectors
	k = bitNum
	index = index[:k]
	P = eigenvector[:, index]
	print str(1.0 * sum(eigenvalue[:k]) / sum(eigenvalue))
	writeMatrixToFile("%s/%s" % (tempDirName, pmatrixFile), P)
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
	# 	if not os.path.exists("%s/%d.txt" % (tempDirName, i)):
	# 		splitDone = False
	# if not splitDone:
	# 	splitColumn(featureFile, featureNum)
	# print "split file done"
	# covariance = None
	# covarianceFile = "%s/%s" % (tempDirName, covarianceFileName)
	# if not os.path.exists(covarianceFile):
	# 	covariance = calCovarianceMat(featureNum)
	# else:
	# 	covariance = readMatrixFromFile(covarianceFile)
	# 	covariance = numpy.mat(covariance)
	# print "Calculate covariance done"
	# P = None
	# pFile = "%s/%s" % (tempDirName, pmatrixFile)
	# if not os.path.exists(pFile):
	# 	startClock = time.time()
	# 	P = calPmatrix(256, covariance)
	# 	endClock = time.time()
	# 	print "Calculate P matrix done, time used %f seconds" % (endClock - startClock)
	# else:
	# 	P = readMatrixFromFile(pFile)
	startClock = time.time()
	pcaFile = "%s/%s" % (tempDirName, pcaResultFile)
	if not os.path.exists(pcaFile):
		pcaMulti("%s/%s" % (tempDirName, centralizedFile), P, pcaFile)
	matrix = readMatrixFromFile(pcaFile, haveImgPath=True)
	# matrix = matrix[:456500]
	matrix = numpy.mat(matrix)
	endClock = time.time()
	print "PCA done, time used:%f seconds" % (endClock - startClock)
	startClock = time.time()
	B, R = itq(matrix, 50)
	endClock = time.time()
	print "ITQone, time used:%f seconds" % (endClock - startClock)
	writeMatrixToFile("%s/itqresult.txt" % tempDirName, B)
	writeMatrixToFile("%s/rmatrix.txt" % tempDirName, R)

