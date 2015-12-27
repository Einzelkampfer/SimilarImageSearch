# !/usr/bin/python
# -*- coding:utf-8 -*-
import sys,os
sys.path.append(os.path.abspath('../ITQ'))
import numpy
import time
from basic import *
from pca import *
from itq import *

def getFloatVector(items):
	v = []
	for f in items:
		v.append(float(f))
	return v

class ItqCalculator():
	def __init__(self):
		fileObj = open("../ITQ/mean.txt", "r")
		items = fileObj.read().strip().split("\n")
		fileObj.close()
		self.meanVector = getFloatVector(items)
		pmatrix = readMatrixFromFile("../ITQ/pmatrix.txt", False)
		self.pmatrix = numpy.mat(pmatrix)
		rmatrix = readMatrixFromFile("../ITQ/rmatrix.txt", False)
		self.rmatrix = numpy.mat(rmatrix)

	def getHashedFeature(caffeFeature):
		for i in range(len(caffeFeature)):
			caffeFeature[i] -= self.meanVector[i]
		caffeFeature = caffeFeature * pmatrix

		Z = caffeFeature * rmatrix
		row, col = Z.shape
		caffeFeature = numpy.ones((row, col)) * -1
		caffeFeature[Z >= 0] = 1
		caffeFeature[caffeFeature < 0] = 0
		result = []
		for i in range(caffeFeature.shape[2]):
			result.append(int(caffeFeature[0, i]))
		return result
