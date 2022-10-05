from tasks import views
from .forms import UserForm
from django.views import generic
from django.views.generic import View
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from directory.models import Patient, Agency, Document
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# this is for login request
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .class_decorator import class_view_decorator


# Create your views here.
@login_required
def Dashboard(request):
	patA = request.user.patient_set.filter(status__iexact='active').count()
	patI = request.user.patient_set.filter(status__iexact='inactive').count()
	events = Document.objects.filter(patient__agency__desNurse=request.user.id).filter(file='').count()
	tasks = len(views.getContext(request.user, 'weekly'))
	context={
            "patNumA"	: patA,
            "patNumI"	: patI,
            "taskNum"	: tasks,
            "events"	: events,
            }
	return render(request, 'dashboard.html', context)



@login_required
def ProfileView(request):
	return render(request, 'directory/profile.html')



@class_view_decorator(login_required)
class CreateAgency(CreateView):
	model = Agency
	fields = ['companyName', 'phoneNumber', 'faxNumber', 'companyEmail', 
				'desNurse', 'placeID', 'formatted_address', 'ext_address']

	def get_form(self, form_class=None):
		# instantiate using parent
		form = super(CreateAgency, self).get_form(form_class) 
		return addStyleAgencyForm(form)


	def form_valid(self, form):
		candidate = form.save(commit=False)
		candidate.desNurse= self.request.user 
		candidate.save()
		return HttpResponseRedirect(reverse('profile'))



@class_view_decorator(login_required)
class UpdateAgency(UpdateView):
	model = Agency
	fields = ['companyName', 'phoneNumber', 'faxNumber', 'companyEmail',
				'placeID', 'formatted_address', 'ext_address']

	# this is to make sure: one user cant access other user's objects
	def get_queryset(self):
		queryset = super(UpdateAgency, self).get_queryset()
		return queryset.filter(desNurse=self.request.user.id)

	def get_form(self, form_class=None):
		# instantiate using parent
		form = super(UpdateAgency, self).get_form(form_class) 
		return addStyleAgencyForm(form)


def addStyleAgencyForm(form):
	# add HTML attributes to form fields
	for field in form.fields:
		form.fields[field].widget.attrs.update({'class': 'form-control'})

	form.fields["companyName"].widget.attrs.update({'placeholder':'Agency Name'})
	form.fields["companyEmail"].widget.attrs.update({'placeholder':'Agency Email'})
	form.fields["phoneNumber"].widget.attrs.update({'placeholder':'Phone Number'})
	form.fields["faxNumber"].widget.attrs.update({'placeholder':'Fax Number'})
	form.fields["formatted_address"].widget.attrs.update({'placeholder':'Enter your address','id': 'autocomplete'})
	form.fields["ext_address"].widget.attrs.update({'placeholder':'Apt/Suite'})
	return form

@class_view_decorator(login_required)
class AgencyDetail(generic.DetailView):
	model = Agency
	template_name="directory/agencyDetail.html"

	# this is to make sure: one user cant access other user's objects
	def get_queryset(self):
		queryset = super(AgencyDetail, self).get_queryset()
		return queryset.filter(desNurse=self.request.user.id)


class loginView(View):
	form_class = UserForm
	template_name="ClientBase.html"
	
	def get(self, request):
		if request.user.is_authenticated:
			return redirect('dashboard')
		else: 
			form=self.form_class(None)
			form.fields["username"].widget.attrs.update({'placeholder':'Hint: guest'})
			form.fields["password"].widget.attrs.update({'placeholder':'Hint: demoview'})
			return render(request, self.template_name, {'form': form})

	# process the registeration data
	def post(self, request):
		# logs in the user
		user=authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			if user.is_active:
				login(request, user)
				# try to see if the user wanted to go somewhere before the log in
				if request.GET.get('next') != None:
					return HttpResponseRedirect(request.GET.get('next'))
				else:
					return redirect('dashboard')
		return redirect('login')



def logout_view(request):
    logout(request)
    return redirect('login')


