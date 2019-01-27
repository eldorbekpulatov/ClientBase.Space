from django.conf.urls import url
from . import views

app_name='calendar'
urlpatterns = [
	url(r'^get$', views.getEvents), 
	url(r'^pull$', views.pullEvent),
	url(r'^post$', views.addEvents), 
	url(r'^update$', views.updateEvents),
	url(r'^delete$', views.deleteEvent),  
	url(r'^$', views.CalendarView, name='schedule'),
]