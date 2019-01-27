import datetime, json
from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse, Http404
from directory.models import Patient, Document, Agency
# this is for login request and redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from myproject.class_decorator import class_view_decorator


# Create your views here.
@login_required
def taskView(request):
	context={ }
	return render(request, 'tasks/tasks.html', context)


@login_required
def getTable(request):
	if request.is_ajax() and request.method=="GET":
		data = getContext(request.user, request.GET.get("tableType"))
		return HttpResponse(json.dumps(data), content_type='application/json')
	else:
		raise Http404

def getContext(user, selection):
	# list of all active patients
	allPatients=user.patient_set.all().filter(status__iexact='active')
	
	dataArray=[]
	# for every active patient take the date of their latest visit
	for pat in allPatients:
		# if patient has a document
		if pat.document_set.all().count()!=0:
			# get the latest document/event date
			myStr=str(pat.document_set.all().latest('visitDate').visitDate)
			myStr=myStr.split("+")[0]
			# the datetime object determined from the latest doc
			lastDate=datetime.datetime.strptime(myStr, "%Y-%m-%d %H:%M:%S")

			# determine the next visit date from the patient info
			if pat.visitType=="Semiannually":
				nextDate=lastDate + datetime.timedelta(days=180)
			else:
				nextDate=lastDate + datetime.timedelta(days=90)

			upcoming = nextDate - datetime.datetime.now()
			
			color=''
			if upcoming.days<2:
				color='red'
			elif upcoming.days<7:
				color='orange'
			elif upcoming.days<30:
				color='green'

			if selection == "monthly":		
				if upcoming < datetime.timedelta(days = 30):
					patDic = {
						"patID"			: pat.id,
						"patName"		: pat.firstName+', '+pat.lastName,
						"patNumber"		: str(pat.phoneNumber),
						"nextDate"		: nextDate.strftime("%B %d, %Y"),
						"upcoming"		: upcoming.days,
						"color"			: color,
						}
					dataArray.append(patDic)
			elif selection == "weekly":
				if upcoming < datetime.timedelta(days = 7):
					patDic = {
						"patID"			: pat.id,
						"patName"		: pat.firstName+', '+pat.lastName,
						"patNumber"		: str(pat.phoneNumber),
						"nextDate"		: nextDate.strftime("%B %d, %Y"),
						"upcoming"		: upcoming.days,
						"color"			: color,
						}
					dataArray.append(patDic)
			else:
				if upcoming < datetime.timedelta(days = 2):
					patDic = {
						"patID"			: pat.id,
						"patName"		: pat.firstName+', '+pat.lastName,
						"patNumber"		: str(pat.phoneNumber),
						"nextDate"		: nextDate.strftime("%B %d, %Y"),
						"upcoming"		: upcoming.days,
						"color"			: color,
						}
					dataArray.append(patDic)
	return dataArray


