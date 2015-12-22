# !/usr/bin/python
# -*- coding:utf-8 -*-

import os, sys
import numpy
import time

tempDirName = "../../temp"
covarianceFileName = "covariance.txt"
featureFile = "../../features.txt"
pcaResultFile = "pcaresult.txt"

def itq(V, n):
	# Initialize a orthogonal random rotation matrix R
	(number, bit) = V.shape
	# Gaussian distribution of mean 0 and variance 1
	R = numpy.random.randn(bit, bit)
	U, V2, S2 = np.linalg.svd(R)
	R = U[:, range(0, bit)]
	
	# Fix and Update iterations
	for i in range(n):
		print 'Iteration ' + str(i + 1) + ' loading..'
		# Fix R and update B(UX)
		Z = V * R
		(row, col) = Z.shape
		UX = numpy.ones((row, col)) * -1
		UX[Z >= 0] = 1
		
		# Fix B and update R
		C = UX.T * V
		UB, sigma, UA = numpy.linalg.svd(C)
		R = UA * UB.T
	B = UX
	# Transform into binary code
	B[B < 0] = 0
	return (B, R)

def splitColumn(fileName, colNum):
	# splitFiles = []
	if not os.path.exists(tempDirName):
		os.mkdir(tempDirName)
	indexStart = 0
	buffSize = 128
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

def readColFile(num):
	fileObj = open("%s/%d.txt" % (tempDirName, num), "r")
	content = fileObj.read().strip().split("\n")
	for i in range(len(content)):
		content[i] = float(content[i])
	return content

def calCovarianceMat(featureNum):
	covariance = [[0.0] * featureNum] * featureNum
	buffSize = 128
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
	fileObj = open("%s/%s" % (tempDirName, covarianceFileName), "w")
	for i in range(featureNum):
		for j in range(featureNum):
			fileObj.write(str(covariance[i][j]))
			if j != featureNum - 1:
				fileObj.write(",")
		fileObj.write("\n")
	fileObj.close()
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
	return P

def pcaMulti(matFile, P, outputFile):
	fileObj = open(matFile, "r")
	outObj = open(outputFile, "w")
	line = fileObj.readline()
	while True:
		if not line:
			break
		items = line.strip().split(',')
		imgPath = items[0]
		items = items[1:]
		outObj.write("%s," % imgPath)
		for i in range(len(items)):
			items[i] = float(items[i])
		items = numpy.mat(items)
		resultRow = items * P
		row, col = resultRow.shape
		for i in range(col):
			outObj.write("%f" % resultRow[0, i])
			if i != col - 1:
				outObj.write(",")
		outObj.write("\n")
		line = fileObj.readline()
	outObj.close()

if __name__ == '__main__':
	featureNum = 1024
	splitDone = True
	for i in range(featureNum):
		if not os.path.exists("%s/%d.txt" % (tempDirName, i)):
			splitDone = False
	if not splitDone:
		splitColumn(featureFile, featureNum)
	print "split file done"
	covariance = None
	covarianceFile = "%s/%s" % (tempDirName, covarianceFileName)
	if not os.path.exists(covarianceFile):
		covariance = calCovarianceMat(featureNum)
	else:
		covariance = []
		fileObj = open(covarianceFile, "r")
		content = fileObj.read().strip().split("\n")
		for line in content:
			items = line.split(",")
			for i in range(len(items)):
				items[i] = float(items[i])
			covariance.append(items)
	print "Calculate covariance done"
	P = calPmatrix(256, covariance)
	print "Calculate P matrix done"
	pcaMulti(featureFile, P, "%s/%s" % (tempDirName, pcaResultFile))


	# sClock = time.time()
	# i = 0
	# while i < 1024:
	# 	startClock = time.time()
	# 	matrix = readFeatureFile("../../features.txt", i, 100)
	# 	pca(matrix, 128)
	# 	sys.stdout.write("done\n")
	# 	i += 100
	# 	endClock = time.time()
	# 	sys.stdout.write("time used:%f seconds\n" % (endClock - startClock))
	# eClock = time.time()
	# print "total time used:%f seconds" % (eClock - sClock)

	# pca(matrix, 128)