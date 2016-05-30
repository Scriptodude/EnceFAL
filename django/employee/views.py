# Views for administration
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

def index_admin(request):
    return redirect('/employee/')

@login_required()
def index_employee(request):
	return render(request, 'index.html')

