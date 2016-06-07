# Todo, to get some help on how to test the admin site goto : https://github.com/django/django/blob/master/tests/modeladmin/tests.py#L14

from django.test import TestCase
from django.contrib.admin.sites import AdminSite

from main.models import *

# Create your tests here.

class MockRequest(object):
	pass

class MockSuperUser(object):
	def has_perm(self, perm):
		return true

request = MockRequest()
request.user = MockSuperUser()

class ModelAdminTests(TestCase):
	 def setUp(self):
		self.site = AdminSite()
		self.vendeur = Vendeur.objects.create(
						nom="Robert",
						prenom="Bob",
						code_permanent="ROBB11223300",
						email="bob.robert@truc.org"
						)
		
		
