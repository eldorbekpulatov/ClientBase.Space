from datetime import datetime
from django.urls import reverse
from django.utils import timezone
from django.views.generic.base import View
from directory.models import Patient, Document, Agency
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

# this is to request login and redirect after
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from myproject.class_decorator import class_view_decorator


# Create your views here.
@class_view_decorator(login_required)
class IndexPatientView(ListView):
	template_name="directory/directory.html"
	context_object_name='patients'

	def get_queryset(self):
		# get the queryset of the user's patients to return
		return self.request.user.patient_set.all()



@class_view_decorator(login_required)
class DetailPatientView(DetailView):
	
	model = Patient
	template_name="directory/patientDetail.html"

	# this is to make sure one user cant access other user's objects
	def get_queryset(self):
		queryset = super(DetailPatientView, self).get_queryset()
		return queryset.filter(desNurse=self.request.user.id)



@class_view_decorator(login_required)
class CreatePatientView(CreateView):
	model = Patient
	fields = ['firstName', 'lastName', 'sex', 'status', 'phoneNumber', 
				'DOB', 'agency', 'visitType', 'desNurse', 'formatted_address',
				'ext_address', 'placeID']
	
	def get_form(self, form_class=None):
		# instantiate using parent
		form = super(CreatePatientView, self).get_form(form_class) 
		# manually get the agencies that which the user belongs to
		# and feed it as form input options
		form.fields['agency'].queryset = self.request.user.agency_set.all()
		return addStylePatientForm(form)

	def form_valid(self, form):
		candidate = form.save(commit=False)
		# assign a user to agency
		candidate.desNurse= self.request.user 
		candidate.save()
		return HttpResponseRedirect(reverse('directory:list'))


@class_view_decorator(login_required)
class UpdatePatientView(UpdateView):
	model = Patient
	fields = ['firstName', 'lastName', 'sex', 'status', 'phoneNumber', 
				'DOB', 'agency', 'visitType', 'formatted_address',
				'ext_address', 'placeID']
	

	# this is to make sure one user can't edit 
	# other user's patients manually {through link}
	def get_queryset(self):
		queryset = super(UpdatePatientView, self).get_queryset()
		return queryset.filter(desNurse=self.request.user.id)

	def get_form(self, form_class=None):
		# instantiate using parent
		form = super(UpdatePatientView, self).get_form(form_class) 
		# manually get the agencies that which the user belongs to
		# and feed it as form input options
		form.fields['agency'].queryset = self.request.user.agency_set.all()
		return addStylePatientForm(form)
 		
def addStylePatientForm(form):
	# add HTML attributes to the form fields
	for field in form.fields:
		form.fields[field].widget.attrs.update({'class': 'form-control'})
	form.fields["firstName"].widget.attrs.update({'placeholder':'First Name'})
	form.fields["lastName"].widget.attrs.update({'placeholder':'Last Name'})
	form.fields["phoneNumber"].widget.attrs.update({'placeholder':'Phone Number'})
	form.fields["DOB"].widget.attrs.update({'placeholder':'YYYY/MM/DD'})
	form.fields["ext_address"].widget.attrs.update({'placeholder':'Apt/Suite'})
	form.fields["formatted_address"].widget.attrs.update({'placeholder':'Enter your address','id': 'autocomplete'})
	return form



@class_view_decorator(login_required)
class UploadDocument(View):
	def post(self, request, pk):
		# get which patient gets the document
		patient=get_object_or_404(Patient, id=pk)
		# Inactive Patient Backend status check
		if (patient.status=="Inactive"): raise Http404
		# get the appropriate data from the request
		if 'file_field' in request.FILES:
			file=request.FILES['file_field']
		else :
			file=None

		visitDate=datetime.strptime(request.POST["docNewDateStart"], "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
		endDate=datetime.strptime(request.POST["docNewDateEnd"], "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)

		# create an instance of Document with the gathered data
		instance=Document(patient=patient, file=file, visitDate=visitDate, endDate=endDate)
		# save the instance
		instance.save()
		# redirect to appropriate View
		if not request.is_ajax():
			return HttpResponseRedirect('/dir/'+pk)



@class_view_decorator(login_required)
class docUpdateView(View):
	def post(self, request, docId):
		# get the Document that is being Updated
		doc=get_object_or_404(Document, id=docId)

		if request.POST.get("docNewDateStart") != None:
			doc.visitDate=datetime.strptime(request.POST["docNewDateStart"], "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)

		if request.POST.get("docNewDateEnd") != None:
			doc.endDate=datetime.strptime(request.POST["docNewDateEnd"], "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)

		if ('file_field' in request.FILES):
			doc.file=request.FILES['file_field']

		# get the relavant address to redirect to
		url="/dir/"+str(doc.patient.id)
		# save the updated Document
		doc.save()
		# redirect
		return HttpResponseRedirect(url)



@class_view_decorator(login_required)
class docDeleteView(View):
	def post(self, request, docId):
		doc=get_object_or_404(Document, id=docId)
		url="/dir/"+str(doc.patient.id)
		if (not doc.file):
			doc.delete()
		return HttpResponseRedirect(url)


