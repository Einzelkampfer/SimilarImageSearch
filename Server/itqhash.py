# !/usr/bin/python
# -*- coding:utf-8 -*-
import sys,os
sys.path.append(os.path.abspath('ITQ'))
import numpy
import time
import subprocess
from basic import *

def getWordMap():
	lines = open("words.txt").read().strip().split("\n")
	wordMap = {}
	for l in lines:
		l = l.split("\t")
		wordMap[l[0]] = l[1]
	return wordMap

def getFloatVector(items):
	v = []
	for f in items:
		v.append(float(f))
	return v

itqCal = None
wordMap = None

class ItqCalculator():
	def __init__(self):
		# print "init"
		fileObj = open("ITQ/mean.txt", "r")
		items = fileObj.read().strip().split("\n")
		fileObj.close()
		self.meanVector = getFloatVector(items)
		pmatrix = readMatrixFromFile("ITQ/pmatrix.txt", False)
		self.pmatrix = numpy.mat(pmatrix)
		rmatrix = readMatrixFromFile("ITQ/rmatrix.txt", False)
		self.rmatrix = numpy.mat(rmatrix)

	def getHashedFeature(self, caffeFeature):
		for i in range(len(caffeFeature)):
			caffeFeature[i] -= self.meanVector[i]
		caffeFeature = caffeFeature * self.pmatrix
		Z = caffeFeature * self.rmatrix
		row, col = Z.shape
		caffeFeature = numpy.ones((row, col)) * -1
		caffeFeature[Z >= 0] = 1
		caffeFeature[caffeFeature < 0] = 0
		result = ""
		row, col = caffeFeature.shape
		for i in range(col):
			result += str(int(caffeFeature[0, i]))
			# result.append(int(caffeFeature[0, i]))
		return result



if itqCal is None:
	p = subprocess.Popen('MIH/mih.bin',
		shell=True,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE)
	os.system("rm static/Images/*")
	itqCal = ItqCalculator()
	wordMap = getWordMap()

def getHash(caffeFeature):
	return itqCal.getHashedFeature(caffeFeature)