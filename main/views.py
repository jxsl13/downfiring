from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404
from .classes.ufr import Ufr

from django.contrib import messages


# Create your views here.


def homepage(request: HttpRequest):
	active_path = request.path
	navbar_tuples = [
	("Homepage", active_path),
	]
	active_index = 0
	context = {
				'navbar_tuples': navbar_tuples,
				'active_index': active_index,
			}
	return render(request=request, template_name='main/index.html', context=context)


def upload(request: HttpRequest):
	if request.method == 'POST':
		file = ""
		try:
			# InMemoryUploadedFile alternatively one could use TemporaryUploadedFile
			# but we are handling rather small files here, so no need for that at he moment.
			file = request.FILES['ufr-file'] 
		except Exception as e:
			messages.error(request, "No file uploaded")
			return redirect("main:homepage")

		ufr_file = Ufr(file)
		if not ufr_file.ok:
			messages.error(request,'Invalid file format passed. Please upload a valid .ufr file.')
		else:
			messages.info(request,f'File uploaded successfully: {ufr_file.ufr_filename} MD5 Hash: {ufr_file.hashes}')
	return redirect("main:homepage")
		