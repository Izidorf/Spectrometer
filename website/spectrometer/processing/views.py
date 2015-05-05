from django.shortcuts import get_object_or_404, render
from django.shortcuts import render_to_response

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from processing.models import Question
from processing.models import SpectralImage
from processing.forms import DocumentForm, UnknownSpecter

from PIL import Image
import PIL
import StringIO
from utilities import Spectrometer, LMSClassificator
import numpy as np

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('processing/index.html')
    context = RequestContext(request, {
        'latest_question_list': latest_question_list,
    })
    return HttpResponse(template.render(context))

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def list(request):
	# Handle file upload
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			newdoc = SpectralImage(tag=form.cleaned_data['tag'], source=request.FILES['docfile'])
			newdoc.save()

			# Redirect to the document list after POST
			return HttpResponseRedirect(reverse('processing.views.list'))
	else:
		form = DocumentForm() # A empty, unbound form
       

    # Load documents for the list page
	documents = SpectralImage.objects.all()

	# Render list page with the documents and the form
	return render_to_response(
	    'processing/list.html',
	    {'documents': documents, 'form': form},
	    context_instance=RequestContext(request)
	)
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def analyseSpecter(request,specter_id):
	response = "You're looking at the results of question %s."
	image = get_object_or_404(SpectralImage, pk=specter_id)

	specter = Spectrometer.Spectrometer(image.source)
	figure = specter.plotSpectra()
	canvas=FigureCanvas(figure)

	response=HttpResponse(content_type='image/png')
	canvas.print_png(response)
	return response

def compareSpecter(request,specter_id):
	response = "You're looking at the results of question %s."
	image = get_object_or_404(SpectralImage, pk=specter_id)

	unknownSpecter = Spectrometer.Spectrometer(image.source).getAverageSpectra()
	print unknownSpecter, "sp"
	unknownSpecter = np.array(unknownSpecter)
	# create models of all spectra in the database
	models = {}
	tags = SpectralImage.objects.order_by().values('tag').distinct()
	for t in tags:
		ob = SpectralImage.objects.filter(tag__exact=t['tag'])
		Sps=[0]*len(ob)
		for i,o in enumerate(ob):
			Sps[i]= Spectrometer.Spectrometer(o.source).getAverageSpectra()


		classificator = LMSClassificator.LMSClassificator(Sps, Sps[0])
		errors1,bestA1,bestB1,rng1,smallestError1 = classificator.compareWithUnknown(unknownSpecter)
		models[t['tag']]=smallestError1
	k =  min(models, key=models.get)
	
	print "The unknown sample is: ", k
	return HttpResponse("The unknown sample is %s." % k)

def compareSpecter2(request,unknownSpecter):
	unknownSpecter = np.array(unknownSpecter)
	# create models of all spectra in the database
	models = {}
	tags = SpectralImage.objects.order_by().values('tag').distinct()
	for t in tags:
		ob = SpectralImage.objects.filter(tag__exact=t['tag'])
		Sps=[0]*len(ob)
		for i,o in enumerate(ob):
			Sps[i]= Spectrometer.Spectrometer(o.source).getAverageSpectra()


		classificator = LMSClassificator.LMSClassificator(Sps, Sps[0])
		errors1,bestA1,bestB1,rng1,smallestError1 = classificator.compareWithUnknown(unknownSpecter)
		models[t['tag']]=smallestError1
	k =  min(models, key=models.get)
	
	print "The unknown sample is: ", k
	return HttpResponse("The unknown sample is %s." % k)

import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
def processUnknown(request):
	if request.method == 'POST':
		print request.FILES
		form = UnknownSpecter(request.POST, request.FILES)
		if form.is_valid():
			f =request.FILES['docfile']
			img = Image.open(f)

		 	avg = Spectrometer.Spectrometer(f)
		 # 	unknownSpecter = np.array(avg)
		 # 	# create models of all spectra in the database
			# models = {}
			# tags = SpectralImage.objects.order_by().values('tag').distinct()
			# for t in tags:
			# 	ob = SpectralImage.objects.filter(tag__exact=t['tag'])
			# 	Sps=[0]*len(ob)
			# 	for i,o in enumerate(ob):
			# 		Sps[i]= Spectrometer.Spectrometer(o.source).getAverageSpectra()


			# 	classificator = LMSClassificator.LMSClassificator(Sps, Sps[0])
			# 	errors1,bestA1,bestB1,rng1,smallestError1 = classificator.compareWithUnknown(unknownSpecter)
			# 	models[t['tag']]=smallestError1
			# k =  min(models, key=models.get)
			
			# print "The unknown sample is: ", k
			# return HttpResponse("The unknown sample is %s." % k)

 			# im.show()
			# Redirect to the document list after POST
			# return HttpResponseRedirect(reverse('processing.views.report'))
	else:
		form = UnknownSpecter() # A empty, unbound form
       

    # Load documents for the list page
	documents = SpectralImage.objects.all()

	# Render list page with the documents and the form
	return render_to_response(
	    'processing/index.html',
	    {'documents': documents, 'form': form},
	    context_instance=RequestContext(request)
	)

def report(request):
	# latest_question_list = Question.objects.order_by('-pub_date')[:5]
	# template = loader.get_template('processing/report.html')
	# context = RequestContext(request, {
	#     'latest_question_list': latest_question_list,
	# })
	# return HttpResponse(template.render(context))
# Render list page with the documents and the form
	return render_to_response(
	    'processing/report.html',
	    {},
	    context_instance=RequestContext(request)
	)



