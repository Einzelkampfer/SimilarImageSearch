# !/usr/bin/python
# -*- coding:utf-8 -*-

import os, sys
import numpy


def readFeatureFile(fileName):
	fileObj = open(fileName, "r")
	line = fileObj.readline()
	data = []
	i = 0
	while True:
		if not line:
			break
		line = line.strip()
		items = line.split(",")
		row = []
		for f in items[1:]:
			row.append(float(f))
		data.append(row)
		i += 1
		if i % 1000 == 0:
			sys.stdout.write("%d lines read\r" % i)
			sys.stdout.flush()
		line = fileObj.readline()
	fileObj.close()
	data = numpy.mat(data)
	return data

def pca(matrix, bitNum):
	# Centralization
	row, col = matrix.shape
	for i in range(col):
		matrix[:, i] -= matrix[:, i].mean()

	# Calculate covariance matrix
	covariance = numpy.cov(matrix, rowvar = 0)

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

	# # Step 6 -> calculate the value of contribution (>= 0.85 is accepted)
	# print str(1.0 * sum(sort_val[:K]) / sum(sort_val))
	
	# return transformed matrix
	result = matrix * P
	return result

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


if __name__ == '__main__':
	matrix = readFeatureFile("../../features.txt")
	print "done"
	pca(matrix, 128)