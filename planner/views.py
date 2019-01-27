import json
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.shortcuts import render
# this is for login request and redirect
from django.contrib.auth.decorators import login_required
from directory.models import Patient, Document, Agency

# Create your views here.
@login_required
def CalendarView(request):
	print('hello')
	context={ 'patients': request.user.patient_set.filter(status__iexact='active')}
	return render(request, 'calendar/calendar.html', context)

@login_required
def getEvents(request):
	if request.is_ajax():
		# get the start/end from AJAXdata and convert to datetime.datetime
		start_view = datetime.strptime(request.GET["start"], "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
		end_view = datetime.strptime(request.GET["end"], "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)		
		data = json.dumps(getViewEvents(start_view, end_view, request.user.id))
		# print(data)
		return HttpResponse(data, content_type='application/json')
	else:
		raise Http404


def getViewEvents(start, end, userID):
	eventArray = []
	# list of all user patients
	allDoc=Document.objects.all().filter(patient__agency__desNurse=userID)
	for document in allDoc:
		# if the start or end time of all documents are within the range
		# or if the document is larger than the range 
		event_smaller_than_range = inRange(document.visitDate, start, end) or inRange(document.endDate, start, end)
		event_bigger_than_range = inRange(start, document.visitDate, document.endDate) and inRange(end, document.visitDate, document.endDate)
		
		# get the event span
		event_span=(document.endDate-document.visitDate)
		# does the event span from 00:00:00 to 00:00:00
		time_zero = event_span.seconds==0
		# does the event span more than/or equal a day
		greater_than_aday = event_span >= timedelta(days=1)
		# is the event all-day [>=1 day and starts and ends at midnight]
		allDay= greater_than_aday and time_zero
		
		# add the appr dictionary to array
		if event_smaller_than_range or event_bigger_than_range:
			event = {	"id"	: document.id,
						"name"	: document.patient.firstName + " " + document.patient.lastName,
						"start"	: str(document.visitDate),
						"end"	: str(document.endDate),
						"patID"	: document.patient.id,
						# "patPlaceID" : document.patient.placeID,
						"completed" : str(document.file)!= "",
						"allDay": allDay }
			eventArray.append(event)
	return {"events" : eventArray, "suggests" : getSuggestArray(start, end, userID)}

def getSuggestArray(start, end, userID):
	suggestArray = []
	# list of all active patients
	allPat=Patient.objects.all().filter(agency__desNurse=userID).filter(status__iexact='active')
	# for every patient in list of patients
	for patient in allPat:
		# get the list of documents
		patsDocuments=patient.document_set.all()
		# if the list isnt empty
		if (patsDocuments.count()!=0):
			# get the latest document by "vistDate"
			patsLatestDoc = patsDocuments.latest('visitDate')
			# make a nextVisit based on patient type
			nextVisit = patsLatestDoc.visitDate+timedelta(days=180) if (patient.visitType=="Semiannually") else patsLatestDoc.visitDate +timedelta(days=90)
			# if the nextVisit is in range of given view
			if inRange(nextVisit, start, end) :
				# create a suggestion dict
				suggestion = {	"patName"	:	patient.firstName + " " + patient.lastName,
								"nextVisit"	:	nextVisit.strftime("%B %d, %Y") 	}
				# and append to suggestion array
				suggestArray.append(suggestion)
	# return the array
	return suggestArray


def inRange(event, start_range, end_range):
	# takes datetime.datetime objects and 
	# checks if event is within start/end range
	if (event<=end_range) and (event>=start_range):
		return True
	return False


@login_required
def pullEvent(request):
	if request.is_ajax() and request.method=="GET":
		doc=get_object_or_404(Document, id=request.GET.get('docID'))
		data = { 	'patID' 		: doc.patient.id,
					'patName' 		: doc.patient.firstName+' '+doc.patient.lastName,
					'patNumber'		: str(doc.patient.phoneNumber),
					'patAddress'	: doc.patient.formatted_address,
					'patExtAdd'		: doc.patient.ext_address,
					# 'patPlaceID'	: doc.patient.placeID,
					'eventStart'	: doc.visitDate.strftime("%B %d, %Y |  %I:%M %p"),
					'eventEnd'		: doc.endDate.strftime("%B %d, %Y |  %I:%M %p"),
					'completed'		: not not doc.file,
					}
		return HttpResponse(json.dumps(data), content_type='application/json')
	else:
		raise Http404

@login_required
def deleteEvent(request):
	if request.is_ajax() and request.method=="POST":
		doc=get_object_or_404(Document, id=request.POST.get('docID'))
		if (not doc.file):
			doc.delete()
		data=[]
		return HttpResponse(json.dumps(data), content_type='application/json')
	else:
		raise Http404


@login_required
def addEvents(request):
	if request.is_ajax() and request.method=="POST":
		# get which patient gets the document
		patient=get_object_or_404(Patient, id=request.POST.get('patID'))
		# Inactive Patient Backend status check
		if (patient.status=="Inactive"): raise Http404

		visitDate=datetime.strptime(request.POST["docNewDateStart"], "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
		endDate=datetime.strptime(request.POST["docNewDateEnd"], "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)	
		if 'file_field' in request.FILES:
			file=request.FILES['file_field']
		else :
			file=None
		# create an instance of Document with the gathered data
		instance=Document(patient=patient, file=file, visitDate=visitDate, endDate=endDate)
		# save the instance
		instance.save()
		data = []
		return HttpResponse(json.dumps(data), content_type='application/json')
	else:
		raise Http404


@login_required
def updateEvents(request):
	if request.is_ajax() and request.method=="POST":
		# get the Document that is being Updated
		doc=get_object_or_404(Document, id=request.POST.get('docID'))
		
		if request.POST.get("docNewDateStart") != None:
			doc.visitDate=datetime.strptime(request.POST["docNewDateStart"], "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)

		if request.POST.get("docNewDateEnd") != None:
			doc.endDate=datetime.strptime(request.POST["docNewDateEnd"], "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)	
		
		doc.save()
		# if HTTP returns data then we know if it was succesfull in AJAX script
		return HttpResponse(content_type='application/json')
	else:
		raise Http404

