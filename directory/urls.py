from django.conf.urls import url
from . import views


app_name='directory'

urlpatterns = [
	url(r'^update_doc/(?P<docId>[a-zA-Z0-9_.-]+)', views.docUpdateView.as_view(), name='eventUpdate'),
	url(r'^delete_doc/(?P<docId>[a-zA-Z0-9_.-]+)', views.docDeleteView.as_view(), name='eventDelete'),
    url(r'^(?P<pk>[a-zA-Z0-9_.-]+)/upload', views.UploadDocument.as_view(), name='eventCreate'),

 	url(r'^new', views.CreatePatientView.as_view(), name='create'),
 	url(r'^edit/(?P<pk>[a-zA-Z0-9_.-]+)', views.UpdatePatientView.as_view(), name='update'),
 	url(r'^(?P<pk>[a-zA-Z0-9_.-]+)', views.DetailPatientView.as_view(), name='retrieve'),
 	url(r'^$', views.IndexPatientView.as_view(), name='list'), 
]