import os, sys
import numpy
import time

featureFile = "../../features.txt"
covarianceFileName = "covariance.txt"
centralizedFile = "centralized.txt"
meanFile = "mean.txt"
pmatrixFile = "pmatrix.txt"
pcaResultFile = "pcaresult.txt"
itqResultFile = "itqresult.txt"
rmatrixFile = "rmatrix.txt"
binarySearchFile = "../../hashcode.dat"

def readMatrixFromFile(filename, haveImgPath=False):
	fileObj = open(filename, "r")
	content =  fileObj.read().strip()
	content = content.split('\n')
	for i in range(len(content)):
		content[i] = content[i].split(',')
		# Skip the firse item: image path
		if haveImgPath:
			content[i] = content[i][1:]
		for j in range(len(content[i])):
			content[i][j] = float(content[i][j])
	return content

def writeMatrixToFile(filename, matrix):
	fileObj = open(filename, "w")
	isNumpyMat = isinstance(matrix, (numpy.matrixlib.defmatrix.matrix))
	if isNumpyMat:
		row, col = matrix.shape
	else:
		row, col = len(matrix), len(matrix[0])

	for i in range(row):
		for j in range(col):
			if isNumpyMat:
				fileObj.write(str(matrix[i, j]))
			else:
				fileObj.write(str(matrix[i][j]))
			if j != col - 1:
				fileObj.write(",")
		fileObj.write("\n")
	fileObj.close()

def readColFile(num):
	fileObj = open("%s/%d.txt" % (tempDirName, num), "r")
	content = fileObj.read().strip().split("\n")
	for i in range(len(content)):
		content[i] = float(content[i])
	return content

def splitColumn(fileName, colNum):
	indexStart = 0
	buffSize = 128
	meanObj = open(meanFile, "w")
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
			tempObj = open("%d.txt" % i, "w")
			for j in range(row):
				tempObj.write(str(data[j, i - indexStart]) + "\n")
		e = time.time()
		sys.stdout.write("time used:%f seconds\n" % (e - s))
		indexStart += buffSize
		tempObj.close()
		fileObj.close()
	meanObj.close()
	# Write the centralized data into file using shell command
	pasteCommand = "paste -d ',' "
	# Paste columns into blocks
	for i in range(featureNum / buffSize):
		cmd = pasteCommand
		for j in range(buffSize * i, buffSize * i + buffSize):
			cmd += "%d.txt " % j
		cmd += "> block%d.txt" % i
		os.popen(cmd)
	# Paste blocks into matrix
	cmd = pasteCommand
	for i in range(featureNum / buffSize):
		cmd += "block%d.txt" % i
	cenTemp = "cenTemp.txt"
	cmd += "> %s" % cenTemp
	os.popen(cmd)
	imgList = "imageList.txt"
	os.popen("awk -F ',' '{print $1}' %s > %s" % (featureFile, imgList))
	pasteCommand += "%s %s > %s" % (imgList, cenTemp, centralizedFile)
	os.popen(pasteCommand)
	# Remove block files
	for i in range(featureNum / buffSize):
		os.popen("rm block%d.txt" % i)