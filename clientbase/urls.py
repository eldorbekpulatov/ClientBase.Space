"""clientbase URL Configuration

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
from django.urls import re_path, include
from . import views

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    
    re_path(r'^$', views.loginView.as_view(), name='login'),
    re_path(r'^logout$',  views.logout_view, name='logout'),
    re_path(r'^dashboard/$', views.Dashboard, name='dashboard'),

    re_path(r'^profile/$', views.ProfileView, name='profile'),
    re_path(r'^profile/agency/edit/(?P<pk>[a-zA-Z0-9_.-]+)', views.UpdateAgency.as_view(), name='editAgency'),
    re_path(r'^profile/agency/(?P<pk>[a-zA-Z0-9_.-]+)', views.AgencyDetail.as_view(), name='getAgency'),
    re_path(r'^profile/agency/$', views.CreateAgency.as_view(), name='agency'),
    
    re_path(r'^tasks/', include("tasks.urls")),
    re_path(r'^dir/', include("directory.urls")),
    re_path(r'^calendar/', include("planner.urls")),

]

