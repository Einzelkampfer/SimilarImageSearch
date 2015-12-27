from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from forms import *

def index(request):
	return render(request, 'index.html')

def handle_uploaded_file(f):
	with open('test.jpg', 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)

def uploadPicture(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'])
			return HttpResponseRedirect('/success/url/')
	else:
		form = UploadFileForm()
	return render(request, 'index.html')


