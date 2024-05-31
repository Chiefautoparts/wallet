from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Wallet

@login_required
def dashboard(request):
	wallet, ccreated = Wallet.objects.get_or_create(user=request.user)
	return render(request, 'wallet/dashboard.html', {'wallet': wallet})