# -*- encoding: utf-8 -*-

import datetime
import pdb

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import Context

from main.forms import  (
                                   ExemplaireVenteForm,
                                   ExemplaireReceptionForm,
                                  )
from main.models import (
                                    Vendeur, Session,
                                    Livre, Facture,
                                    ETAT_LIVRE_CHOICES,
                                    Exemplaire, Reception,
                                    Vente, Facture
                                   )

class ExemplaireReceptionInline(admin.TabularInline):

    exclude = ['facture', 'actif', 'etat', 'livre']
    model = Exemplaire
    form = ExemplaireReceptionForm
    fields = ['isbn', 'titre', 'auteur', 'prix']
    extra = 5

class ExemplaireVenteInline(admin.TabularInline):

    exclude = [ 'actif', 'etat', 'livre']
    model = Exemplaire
    form = ExemplaireVenteForm
    fields = ['identifiant','isbn', 'titre', 'auteur', 'prix']
    extra = 5

class SessionAdmin(admin.ModelAdmin):
    exclude = ('actif',)
    list_display = ('nom', 'date_debut', 'date_fin',)

class ReceptionAdmin(admin.ModelAdmin):
    model = Reception
    exclude = ('actif',)
    fields = [
			  'code_carte_etudiante',
              'code_permanent',
              'prenom',
              'nom' ,
              'email',
              'telephone'
             ]
    inlines = [ ExemplaireReceptionInline, ]
    list_display = ('date_creation', 'nom', 'prenom',
                    'nb_livres', 'code_permanent')

    def save_model(self, request, obj, form, change):
        #ne save pas le modele si le meme vendeur existe deja!
        try:
            Vendeur.objects.get(code_permanent=obj.code_permanent)
        except Vendeur.DoesNotExist:
            obj.save()
        return

    #TODO: utiliser url reverser
    def response_add(self, request, obj, post_url_continue=None):
        context = {}
        # Afficher recu
        try:
            vendeur = Vendeur.objects.all().exclude(pk=obj.pk).get(code_permanent=obj.code_permanent)
            context['vendeur'] = vendeur
            context['exemplaires'] = vendeur.exemplaires.filter(date_creation__startswith=datetime.date.today())

        except Vendeur.DoesNotExist:
            context['vendeur'] = obj
            context['exemplaires'] = obj.exemplaires.all()

        context['date_transaction'] = datetime.date.today()
        context['employe'] = request.user.username
        context['montant_total'] = sum([e.prix for e in context['exemplaires']]) or 0
        context['ext']='admin/base.html'

        return render(request, 'encefal/depots.html', Context(context))

    def has_change_permission(self, request, obj=None):
        return obj is None or False

def annuler_vente(modeladmin, request, queryset):
    for vente in queryset.all():
        exemplaires = vente.exemplaires
        for exemplaire in exemplaires.all():
            exemplaire.etat = 'VENT'
            exemplaire.facture = None
            exemplaire.save()
    queryset.delete()
    return HttpResponseRedirect('/employee/')
annuler_vente.short_description = "Annuler la ou les vente(s) selectionnée(s)"

class VenteAdmin(admin.ModelAdmin):

	def __init__(self, *args, **kwargs):
		super(VenteAdmin, self).__init__(*args, **kwargs)

	def get_form(self, request, obj=None, **kwargs):
		self.model.session = Session.current_session()
		form = super(VenteAdmin, self).get_form(request, obj, **kwargs)
		self.model.employe = request.user
		return form

	def save_model(self, request, obj, form, change):
		obj.employe_id = self.model.employe.id
        # If the book is from this session
		if not self.model.session:
			session = Session.session_null()
		else:
			session = self.model.session
		obj.session_id = session.id
		obj.save()

    #TODO: utiliser url reverser admin_index ??
	def response_add(self, request, obj, post_url_continue=None):
		return HttpResponseRedirect('/factures/?id=' + str(obj.id))

	def has_change_permission(self, request, obj=None):
		return obj is None or False

	def has_delete_permission(self, request, obj=None):
		return obj is not None or False

	def get_actions(self, request):
		actions = { 'annuler_vente':(annuler_vente, 'annuler_vente', annuler_vente.short_description) }
		return actions

	model = Facture
	readonly_fields = ('employe','session',)
	fields = ('employe', 'session')
	list_display = ( 'date_creation', 'employe', 'session', 'nb_livres', 'prix_avant_taxes',)

	exclude = ('actif',)
	actions = [ annuler_vente ]
	inlines = [ ExemplaireVenteInline, ]

class LivreAdmin(admin.ModelAdmin):
    fields = ('isbn', 'titre', 'auteur', 'edition')
    list_display = ('isbn', 'titre', 'auteur', 'edition')
    search_fields = ['titre', 'auteur', 'isbn']

def remettre_exemplaires(modeladmin, request, queryset):
    for exemplaire in queryset.all():

        if exemplaire.etat != 'VENT':
            modeladmin.message_user(request, "Erreur! Seul les exemplaires en vente peuvent être rendus")
            return

    queryset.all().update(etat='REND')
remettre_exemplaires.short_description = "Remettre le(s) exemplaire(s) au client"


def rembourser_exemplaires(modeladmin, request, queryset):
    for exemplaire in queryset.all():

        if exemplaire.etat != 'VEND':
            modeladmin.message_user(request, "Erreur! Seul les exemplaires vendus peuvent être remboursés")
            return

    queryset.all().update(etat='REMB')

rembourser_exemplaires.short_description = "Rembourser le(s) exemplaire(s) au client"

class ExemplaireAdmin(admin.ModelAdmin):
    list_display = ('id','titre','code_permanent_vendeur','etat','prix','date_creation', 'date_modification', 'facture' )
    order_by = ('date_creation', 'date_modification')
    search_fields = ('livre__isbn','livre__titre','id', 'vendeur__code_permanent')
    actions = [remettre_exemplaires, rembourser_exemplaires]

class FactureAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_creation', 'employe', 'session', 'nb_livres',)

class VendeurAdmin(admin.ModelAdmin):
    list_display = ('date_creation', 'nom', 'prenom', 'nb_livres', 'code_permanent')
    exclude = ['actif']
    fields = [
              'code_permanent',
              'prenom',
              'nom' ,
              'email'
             ]

admin.site.register(Vendeur, VendeurAdmin)
admin.site.register(Reception, ReceptionAdmin)
admin.site.register(Vente, VenteAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Livre, LivreAdmin)
admin.site.register(Facture, FactureAdmin)
admin.site.register(Exemplaire, ExemplaireAdmin)
