"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^$', views.loginView.as_view(), name='login'),
    url(r'^logout$',  views.logout_view, name='logout'),
    url(r'^dashboard/$', views.Dashboard, name='dashboard'),

    url(r'^profile/$', views.ProfileView, name='profile'),
    url(r'^profile/agency/edit/(?P<pk>[a-zA-Z0-9_.-]+)', views.UpdateAgency.as_view(), name='editAgency'),
    url(r'^profile/agency/(?P<pk>[a-zA-Z0-9_.-]+)', views.AgencyDetail.as_view(), name='getAgency'),
    url(r'^profile/agency/$', views.CreateAgency.as_view(), name='agency'),
    
    url(r'^tasks/', include("tasks.urls")),
    url(r'^dir/', include("directory.urls")),
    url(r'^calendar/', include("planner.urls")),

]

