import array
import numpy
def writeBinaryToFile(filename, matrix):
	bin_array = array.array('B')
	row, col = matrix.shape
	byteSize = 8
	fileObj = open(filename, 'wb')
	for i in range(row):
		binstr = ""
		for j in range(col):
			binstr += ("%d" % matrix[i, j])
			if len(binstr) == byteSize:
				bin_array.append(int(binstr, 2))
				binstr = ""
		bin_array.tofile(fileObj)
	fileObj.close()

l = [[0,0,1,0,1,1,0,1]]
l = numpy.mat(l)
writeBinaryToFile("debug.bin", l)