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

if __name__ == '__main__':
	matrix = readFeatureFile("../../features.txt")
	print "done"
	pca(matrix, 128)