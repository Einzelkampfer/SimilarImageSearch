# !/usr/bin/python
# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from forms import *
import string
import time
import zmq
import random
from itqhash import *

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def index(request):
	return render(request, 'index.html')

def handleUploadedImg(f):
	filename = id_generator(10)
	filename = "Images/%s" % filename
	with open("static/" + filename, 'w') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
	return filename

def extractCaffeFeature(imgPath):
	imgName = imgPath.split("/")[-1]
	featurePath = "Cache/Features/%s.txt" % imgName
	cmd = """../caffe/build/tools/googlenet_extract_feature.bin \
		../caffe/models/bvlc_googlenet/deploy.prototxt \
		../caffe/models/bvlc_googlenet/bvlc_googlenet.caffemodel \
		../caffe/data/ilsvrc12/imagenet_mean.binaryproto \
		%s pool5/7x7_s1 %s""" % (featurePath, imgPath)
	os.system(cmd)
	feature = open(featurePath, "r").read().strip().split(",")
	feature = getFloatVector(feature[1:])
	os.system("rm -f %s" % featurePath)
	return feature

def uploadPicture(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			imgPath = handleUploadedImg(request.FILES['image'])
			start = time.time()
			caffeFeatures = extractCaffeFeature("static/" + imgPath)
			hashFeature = getHash(caffeFeatures)
			context = zmq.Context()
			# print "Connecting to hello world server..."
			socket = context.socket(zmq.REQ)
			socket.connect("tcp://localhost:5555")
			socket.send(hashFeature)
			# Get the reply.
			message = socket.recv()
			message = eval(message)[:20]
			end = time.time()
			# print "Received reply ", request, "[", message, "]"
			return render(request, 'search.html', {'imgpath':imgPath, "result":message, "searchTime": end - start})
		else:
			form = UploadFileForm()
	return render(request, 'index.html')


