# -*- encoding: utf-8 -*-
"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from models import *

class SimpleTest(TestCase):

	def setUp(self):
		print("Creating objects...")
		Vendeur.objects.create(nom="Robert", prenom="Bob", code_permanent="ROBB11223300", email="bob.robert@truc.org")
		vend = Vendeur.objects.get(nom="Robert")

		Livre.objects.create(titre="abc123")
		liv = Livre.objects.get(titre="abc123")

		try:
			print("Creating with price 10.03")
			exemp = Exemplaire.objects.create(livre=liv, vendeur=vend, etat='VENT', prix='10.03')
			exemp.full_clean()
		except ValidationError, e:
			exemp.delete()
			print('; '.join(e.messages))

		try:
			print("Creating with price 10.05")
			exemp = Exemplaire.objects.create(livre=liv, vendeur=vend, etat="VENT", prix='10.05')
			exemp.full_clean()
		except ValidationError, e:
			exemp.delete()
			print('; '.join(e.messages))

		print("Objects created")

	# Test de quelques methodes
	def test1(self):

		print("Testing previously created objects...")
		# Recuperation des objets précédemment créé
		vend = Vendeur.objects.get(nom="Robert")
		liv = Livre.objects.get(titre="abc123")
		exe = Exemplaire.objects.get(livre=liv)

		# Assert des fonctions de ces objets
		self.assertEqual(vend.nb_livres(), 1)
		self.assertEqual(liv.nb_exemplaires_en_vente(), 1)
		self.assertEqual(exe.vendeur, vend)
		print("Test complete!")

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

