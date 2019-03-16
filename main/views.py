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
			file = request.FILES['ufr-file']
		except Exception as e:
			print("No file uploaded")
			messages.error(request, "No file uploaded")
			return redirect("main:homepage")

		ufr_meta_data = Ufr(file)
		
		if not ufr_meta_data.ok:
			messages.error(request,'Invalid file format passed. Please upload a valid .ufr file.')
		else:
			messages.info(request,'File uploaded successfully!')				
	return redirect("main:homepage")
		