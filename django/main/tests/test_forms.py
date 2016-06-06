# -*- encoding: utf-8 -*-

from django.test import TestCase
from main.models import Exemplaire
from main.forms import *

class FormsTest(TestCase):
	def setUp(self):
		v = Vendeur.objects.create(nom="Robert", prenom="Bob", code_permanent="ROBB11223300", email="bob.robert@truc.org")
		self.livre = Livre.objects.create(titre="abc123", auteur="Moi", isbn="1122334455", edition=5)
		self.livre.save()

		self.exemp = Exemplaire.objects.create(livre=self.livre, vendeur=v, etat="VENT", prix='10.05')
		self.exemp.save()

	def testExempReceptionInvalide(self):
		data_info = {'isbn': self.livre.isbn, 'titre': self.livre.titre, 'auteur': ''}
		form = ExemplaireReceptionForm(data=data_info)
		self.assertFalse(form.is_valid())

	def testExempVenteInvalide(self):
		data_info = {'isbn': self.livre.isbn, 'titre': '', 'auteur': self.livre.auteur,
					'prix':self.exemp.prix, 'identifiant': self.exemp.pk}
		form = ExemplaireVenteForm(data=data_info)
		self.assertFalse(form.is_valid())


