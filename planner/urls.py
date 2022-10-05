from django.urls import re_path
from . import views

app_name='calendar'
urlpatterns = [
	re_path(r'^get$', views.getEvents), 
	re_path(r'^pull$', views.pullEvent),
	re_path(r'^post$', views.addEvents), 
	re_path(r'^update$', views.updateEvents),
	re_path(r'^delete$', views.deleteEvent),  
	re_path(r'^$', views.CalendarView, name='schedule'),
]