from django.conf.urls import url
from . import views

app_name='task'
urlpatterns = [
	url(r'^pull$', views.getTable),
	url(r'^$', views.taskView, name='upcoming'),
]