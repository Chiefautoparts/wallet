from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Wallet, Transaction 
from .utils import get_bitcoin_price

@login_required
def dashboard(request):
	wallet, ccreated = Wallet.objects.get_or_create(user=request.user)
	bitcoin_price = get_bitcoin_price()
	usd_balance = None
	if bitcoin_price is not None:
		usd_balance = wallet.bitcoin_balance * bitcoin_price
	transactions = Transaction.objects.filter(wallet=wallet).order_by('-date')
	return render(request, 'wallet/dashboard.html', {
									'wallet': wallet,
									'bitcoin_price': bitcoin_price,
									'usd_balance': usd_balance,
									'transactions': transactions
									})

# display current balance

# add bitcoin to wallet

# send to another wallet address

# purchase coin from crypto exchange

# sell crypto 

# view transaction history 

