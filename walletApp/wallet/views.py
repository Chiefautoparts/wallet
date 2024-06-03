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

# create a new bitcoin wallet & address
def create_new_wallet(request):

# add bitcoin to wallet
def add_funds(request):

# send to another wallet address
def send_crypto(request):

# purchase coin from crypto exchange
def purchase_crypto(request):

# sell crypto 
def sell_crypto(request):

# view transaction history 
def view_transaction_history(request):
