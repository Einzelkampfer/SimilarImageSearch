# !/usr/bin/python
# -*- coding:utf-8 -*-

import os, sys
import numpy
import time
from basic import *
from pca import *
from itq import *

def getHashedFeature(caffeFeature):
	fileObj = open("mean.txt", "r")
	items = fileObj.read().strip().split("\n")
	fileObj.close()
	meanVector = getFloatVector(items)
	for i in range(len(caffeFeature)):
		caffeFeature[i] -= meanVector[i]
	pmatrix = readMatrixFromFile("pmatrix.txt", False)
	pmatrix = numpy.mat(pmatrix)
	caffeFeature = caffeFeature * pmatrix

	rmatrix = readMatrixFromFile("rmatrix.txt", False)
	rmatrix = numpy.mat(rmatrix)
	Z = caffeFeature * rmatrix
	row, col = Z.shape
	caffeFeature = numpy.ones((row, col)) * -1
	caffeFeature[Z >= 0] = 1
	caffeFeature[caffeFeature < 0] = 0
	result = []
	for i in range(caffeFeature.shape[2]):
		result.append(int(caffeFeature[0, i]))
	return result