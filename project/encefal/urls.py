# -*- encoding: utf-8 -*-
from django.conf.urls import *
from . import views

urlpatterns = [
    url(r'^$', views.acceuil, name='acceuil'),
    url(r'^livres/$', views.livres, name='livres'),
    url(r'^livre/$', views.livre, name='livre'),
    url(r'^exemplaire/$', views.exemplaire, name='exemplaire'),
    url(r'^vendeur/$', views.vendeur, name='vendeur'),
    url(r'^rapport/$', views.rapport, name='rapport'),
    url(r'^factures/$', views.factures, name='factures'),
]
