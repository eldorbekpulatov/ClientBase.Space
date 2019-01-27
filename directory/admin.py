from django.contrib import admin
from directory.models import Agency, Patient, Document

# Register your models here.
class AgencyAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'phoneNumber', 'faxNumber', 'companyEmail']
	list_display_links = ['__unicode__']
	search_fields = ['companyName','phoneNumber', 'faxNumber', 'companyEmail'] 
	list_filter = ["desNurse"]
	class Meta:
		agency=Agency
admin.site.register(Agency, AgencyAdmin)


class PatientAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "status", "phoneNumber", "agency"]
	list_display_links = ["__unicode__"]
	list_filter = ["status", "desNurse", "agency", "lastModified", "firstEntered"]
	search_fields = ["firstName", "lastName", "phoneNumber", "DOB"]
	class Meta:
		patient=Patient
admin.site.register(Patient, PatientAdmin)


class DocumentAdmin(admin.ModelAdmin):
	list_display = ["__unicode__"]
	list_filter = ["visitDate"]
	search_fields = ["patient", "visitDate"]
	class Meta:
		document=Document
admin.site.register(Document, DocumentAdmin)