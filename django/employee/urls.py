"""EnceFAL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout
from views import index_employee, rapport

admin.autodiscover()

urlpatterns = [
	url(
		r'^$',
		index_employee
	),

	url(
		r'^rapport/$',
		rapport,
		name='rapport'),

	# Redirect to main page after logout
	url(
		r'^logout/$',
		logout,
		{'next_page': 'main:accueil'}
	),

	#Admin is now on /employee rather than /admin
	url(
		r'^',
		admin.site.urls
	),
]
