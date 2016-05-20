"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from project.encefal.models import *

class SimpleTest(TestCase):
    #def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
    #    self.failUnlessEqual(1 + 1, 2)

	# Creation des objets de test
	def setUp(self):
		Vendeur.objects.create(nom="Robert", prenom="Bob", code_permanent="ROBB11223300", email="bob.robert@truc.org")
		vend = Vendeur.objects.get(nom="Robert")

		Livre.objects.create(titre="abc123")
		liv = Livre.objects.get(titre="abc123")

		Exemplaire.objects.create(livre=liv, vendeur=vend, etat="VENT", prix=10.05)

	# Test de quelques methodes
	def test1(self):

		# Recuperation des objets precedemment cree
		vend = Vendeur.objects.get(nom="Robert")
		liv = Livre.objects.get(titre="abc123")
		exe = Exemplaire.objects.get(livre=liv)

		# Assert des fonctions de ces objets
		self.assertEqual(vend.nb_livres(), 1)
		self.assertEqual(liv.nb_exemplaires_en_vente(), 1)
		self.assertEqual(exe.vendeur, vend)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

