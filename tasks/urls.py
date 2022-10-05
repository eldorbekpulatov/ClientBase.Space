from django.urls import re_path
from . import views

app_name='task'
urlpatterns = [
	re_path(r'^pull$', views.getTable),
	re_path(r'^$', views.taskView, name='upcoming'),
]