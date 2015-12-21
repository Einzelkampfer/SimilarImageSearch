# !/usr/bin/python
# -*- coding:utf-8 -*-

import os, sys
import numpy
import time

# def readFeatureFile(fileName, colBegin=-1, colNum=-1):
# 	fileObj = open(fileName, "r")
# 	line = fileObj.readline()
# 	data = []
# 	i = 0
# 	if not colBegin == -1 or not colNum == -1:
# 		sys.stdout.write("read from col %d to col %d\n" % (colBegin, colBegin + colNum - 1))
# 	while True:
# 		if not line:
# 			break
# 		line = line.strip()
# 		items = line.split(",")
# 		row = []
# 		if colBegin == -1 and colNum == -1:
# 			for f in items[1:]:
# 				row.append(float(f))
# 		else:
# 			indexEnd = colBegin + 1 + colNum
# 			indexEnd = indexEnd if (len(items) - 1 > indexEnd) else len(items) - 1
# 			for i in range(colBegin + 1, indexEnd):
# 				row.append(float(items[i]))
# 		data.append(row)
# 		i += 1
# 		# if i % 5000 == 0:
# 		# 	sys.stdout.write("%d lines read\r" % i)
# 		# 	sys.stdout.flush()
# 		line = fileObj.readline()
# 	fileObj.close()
# 	data = numpy.mat(data)
# 	return data


def pca(matrix, bitNum):
	# Centralization
	row, col = matrix.shape
	for i in range(col):
		matrix[:, i] -= matrix[:, i].mean()

	# Calculate covariance matrix
	covariance = numpy.cov(matrix, rowvar = 0)
	row, col = covariance.shape
	print "%d, %d" % (row, col)
	# # Calculate eigenvectors and eigenvalues of covariance matrix
	# eigenvalue, eigenvector = numpy.linalg.eig(covariance)

	# # Sort eigenvectors together with its corresponding eigenvalues
	# index = numpy.argsort(-eigenvalue)
	# eigenvalue = eigenvalue[index]
	# eigenvector = eigenvector[:, index]
	
	# # Choose first k rows of eigenvectors
	# k = bitNum
	# index = index[:k]
	# P = eigenvector[:, index]

	# # # Step 6 -> calculate the value of contribution (>= 0.85 is accepted)
	# # print str(1.0 * sum(sort_val[:K]) / sum(sort_val))
	
	# # return transformed matrix
	# result = matrix * P
	# return result

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
	if not os.path.exists("temp"):
		os.mkdir('temp')
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
			tempObj = open("temp/%d.txt" % i, "w")
			for j in range(row):
				tempObj.write(str(data[j, i - indexStart]) + "\n")
		e = time.time()
		sys.stdout.write("time used:%f seconds\n" % (e - s))
		indexStart += buffSize
		tempObj.close()
		fileObj.close()

def readColFile(num):
	fileObj = open("temp/%d.txt" % num, "r")
	content = fileObj.read().strip().split("\n")
	for i in range(len(content)):
		content[i] = float(content[i])
	return content



def calCovarianceMat(featureNum):
	covariance = [[0.0] * featureNum] * featureNum
	buffSize = 32
	# for i in range(featureNum / buffSize):
	# 	s = time.time()
	# 	indexStart = i * buffSize
	# 	print "read feature %d to feature %d" % (indexStart, indexStart + buffSize - 1)
	# 	data = []
	# 	for j in range(buffSize):
	# 		col = readColFile(j + indexStart)
	# 		if len(data) == 0:
	# 			for i in range(len(col)):
	# 				data.append([])
	# 		for k in range(len(col)):
	# 			data[k].append(col[k])
	# 	data = numpy.mat(data)
	# 	cov = numpy.cov(data, rowvar = 0)
	# 	print "%d * %d" % cov.shape
	# 	for k in range(buffSize):
	# 		for l in range(buffSize):
	# 			covariance[indexStart + k][indexStart + l] = cov[k, l]
	# 	e = time.time()
	# 	sys.stdout.write("time used:%f seconds\n" % (e - s))

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

	fileObj = open("temp/covariance.txt", "w")
	for i in range(featureNum):
		for j in range(featureNum):
			fileObj.write(covariance[i][j])
			if j != featureNum - 1:
				fileObj.write(",")
		fileObj.write("\n")
	fileObj.close()
	covariance = numpy.mat(covariance)
	return covariance

if __name__ == '__main__':
	featureNum = 1024
	splitDone = True
	for i in range(featureNum):
		if not os.path.exists("temp/%d.txt" % i):
			splitDone = False
	if not splitDone:
		splitColumn("../../features.txt", featureNum)
	if not os.path.exists("temp/covariance.txt"):
		calCovarianceMat(featureNum)


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