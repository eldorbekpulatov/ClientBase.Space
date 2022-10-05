from django.urls import re_path, include
from . import views


app_name='directory'

urlpatterns = [
	re_path(r'^update_doc/(?P<docId>[a-zA-Z0-9_.-]+)', views.docUpdateView.as_view(), name='eventUpdate'),
	re_path(r'^delete_doc/(?P<docId>[a-zA-Z0-9_.-]+)', views.docDeleteView.as_view(), name='eventDelete'),
    re_path(r'^(?P<pk>[a-zA-Z0-9_.-]+)/upload', views.UploadDocument.as_view(), name='eventCreate'),

 	re_path(r'^new', views.CreatePatientView.as_view(), name='create'),
 	re_path(r'^edit/(?P<pk>[a-zA-Z0-9_.-]+)', views.UpdatePatientView.as_view(), name='update'),
 	re_path(r'^(?P<pk>[a-zA-Z0-9_.-]+)', views.DetailPatientView.as_view(), name='retrieve'),
 	re_path(r'^$', views.IndexPatientView.as_view(), name='list'), 
]