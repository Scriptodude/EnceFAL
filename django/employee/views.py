# Views for administration
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from main.models import (
                                    Facture,
                                    Livre,
                                    Session,
                                    Vendeur,
                                    ETAT_LIVRE_CHOICES,
                                    Exemplaire,
                                    ISBN_DB_BASE_QUERY,
                                    COOP_UQAM_BASE_QUERY
                                   )
from datetime import datetime, timedelta, date

def index_admin(request):
    return redirect('/employee/')

@login_required()
def index_employee(request):
	return render(request, 'index.html')

def rapport(request):

    if 'date' in request.GET:
        date = request.GET['date']
        date = datetime.strptime(date,"%Y-%m-%d")
    else:
        date = datetime.today()

    lendemain = date + timedelta(days=1)

    # on met les deux dates a minuit
    date = date.replace(hour=0, minute=0, second=0)
    lendemain = lendemain.replace(hour=0, minute=0, second=0)

    ajoutes = Exemplaire.objects.all().filter(date_creation__gt=date,
                                              date_creation__lt=lendemain)
    factures = Facture.objects.all().filter(date_creation__gt=date,
                             date_creation__lt=lendemain)

    nb_ajoutes = ajoutes.count()
    nb_factures = factures.count()
    nb_vendus = sum([f.nb_livres() for f in factures])
    prix_total_vendu = sum([f.prix_total() for f in factures])

    context = {
        'nb_ajoutes':nb_ajoutes,
        'nb_factures':nb_factures,
        'date':date.date(),
        'nb_vendus':nb_vendus,
        'prix_total_vendu':prix_total_vendu,
    }

    return render(request, 'rapport.html', context)

