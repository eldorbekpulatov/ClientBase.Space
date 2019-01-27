from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import RegexValidator
phone_regex = RegexValidator(regex=r'^\(?([0-9]{3})\)?[-.●]?([0-9]{3})[-.●]?([0-9]{4})$')

def upload_to(instance, filename):
	li=folder_name(str(instance.visitDate))
	return "%s/%s/%s/%s/%s" % (instance.patient.agency.desNurse, instance.patient.agency, 
		instance.patient.firstName+"_"+instance.patient.lastName, li[0],li[1])

"""returns the last two file paths as a list for upload to"""
def folder_name(string):
	x=string.index("-")
	y=list()
	y.append(string[:x])
	y.append(string[x+1:11])
	return y

# Create your models here.
class Agency(models.Model):
	"""Agency has:
		-compName
		-phoneNumber
		-faxNumber
		-compEmail
		-desNurse (foreign key)
		-placeID
		-formatted_address
		-ext_address
		"""
	desNurse=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
	companyName=models.CharField(max_length=50)

	phoneNumber=models.CharField(validators=[phone_regex], max_length=10)
	faxNumber=models.CharField(validators=[phone_regex], max_length=10)
	companyEmail=models.EmailField(max_length=50) 

	placeID=models.CharField(max_length=70)
	formatted_address=models.CharField(max_length=100)
	ext_address=models.CharField(max_length=10)


	lastModified=models.DateTimeField(auto_now=True, auto_now_add=False)
	firstEntered=models.DateTimeField(auto_now=False, auto_now_add=True)
	
	def get_absolute_url(self):
		return reverse("getAgency", kwargs={'pk':self.id})

	def __unicode__(self):
		return self.companyName
	def __str__(self):
		return self.companyName


class Person(models.Model):
	"""has attributes like:
		-firstName	(CharField max=20)
		-lastName	(CharField max=25)
		-phoneNumber(CharField max=10)
		-address	(TextField)
		-sex		(M/F)
		-status 	(active/inactive)
	"""
	Male='M'
	Female='F'
	sex_options= ( (Male, 'Male'), (Female, 'Female'))

	Active='Active'
	Inactive='Inactive'
	status_options= ((Active, 'Active'), (Inactive, 'Inactive'))
		
	firstName=models.CharField(max_length=20)
	lastName=models.CharField(max_length=25)
	sex=models.CharField(max_length=1, choices=sex_options, default=Male)
	status=models.CharField(max_length=8, choices=status_options, default=Active)
	phoneNumber=models.CharField(validators=[phone_regex], max_length=10)

	def __unicode__(self):
		return self.firstName+ " "+self.lastName

	def __str__(self):
		return self.firstName+ " "+self.lastName



class Patient(Person):
	"""Patient is a subclass of Person.
		Inherited attr:
			-firstName 
			-lastName
			-status
			-phoneNumber
		New attr:
			-patDOB
			-agency (Patient is ForeignKey to Agency)
			-desNurse (Patient is ForeignKey to User)
			-placeID
			-formatted_address
			-ext_address
		Timestamps:
			-firstEntered
			-lastModified
	"""
	quarterly='Quarterly'
	semiannually='Semiannually'
	type_options= ((quarterly, 'Quarterly'), (semiannually, 'Semiannually'))

	visitType=models.CharField(max_length=12, choices=type_options, default=quarterly)
	DOB=models.DateField(auto_now=False, auto_now_add=False)
	agency=models.ForeignKey(Agency, on_delete=models.CASCADE, default=1)
	desNurse=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
	
	placeID=models.CharField(max_length=70)
	formatted_address=models.CharField(max_length=100)
	ext_address=models.CharField(max_length=10)

	lastModified=models.DateTimeField(auto_now=True, auto_now_add=False)
	firstEntered=models.DateTimeField(auto_now=False, auto_now_add=True)

	def get_absolute_url(self):
		return reverse("directory:retrieve", kwargs={'pk':self.id})

	class Meta:
		ordering=["lastName", "firstName"]



class Document(models.Model):
	"""Document is a foreign key to Patient.
		Attr:
			-patient 	(foreign key to Patient)
			-file 		(file pertaining to the patient)
			-visitDate 	(visitDate)

		Timestamps:
			-firstEntered
			-lastModified
	"""

	patient=models.ForeignKey(Patient, on_delete=models.CASCADE, default=1)
	file = models.FileField(null=True, blank=True, upload_to=upload_to)
	visitDate=models.DateTimeField(auto_now=False, auto_now_add=False)
	endDate=models.DateTimeField(auto_now=False, auto_now_add=False)

	lastModified=models.DateTimeField(auto_now=True, auto_now_add=False)
	firstEntered=models.DateTimeField(auto_now=False, auto_now_add=True)


	class Meta:
		ordering=["visitDate"]

	def __unicode__(self):
		return self.patient.__str__()+ "("+self.visitDate.__str__()+")"

	def __str__(self):
		return self.patient.__str__()+ "("+self.visitDate.__str__()+")"





