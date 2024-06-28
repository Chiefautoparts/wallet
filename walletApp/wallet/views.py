from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Wallet, Transaction
from .gemini_api import get_bitcoin_price, gemini_request
from django.contrib import messages
import uuid
import decimal  # Import the decimal module

@login_required
def dashboard(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    if created:
        wallet.blockchain_address = wallet.generate_blockchain_address()
        wallet.save()

    # Ensure bitcoin_price is converted to decimal.Decimal
    bitcoin_price = decimal.Decimal(str(get_bitcoin_price()))
    usd_balance = wallet.bitcoin_balance * bitcoin_price
    transactions = Transaction.objects.filter(wallet=wallet).order_by('-date')
    return render(request, 'wallet/dashboard.html', {
        'wallet': wallet,
        'bitcoin_price': bitcoin_price,
        'usd_balance': usd_balance,
        'transactions': transactions,
    })

@login_required
def create_wallet(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    if created or not wallet.blockchain_address:
        wallet.blockchain_address = wallet.generate_blockchain_address()
        wallet.save()
        messages.success(request, 'Your wallet has been created.')
    else:
        messages.info(request, 'You already have a wallet.')
    return redirect('wallet:dashboard')

@login_required
def add_bitcoin(request):
    if request.method == 'POST':
        amount = decimal.Decimal(request.POST.get('amount'))
        wallet = Wallet.objects.get(user=request.user)
        wallet.bitcoin_balance += amount
        wallet.save()
        Transaction.objects.create(wallet=wallet, amount=amount, transaction_type='receive', transaction_id='internal')
        messages.success(request, f'Added {amount} BTC to your wallet.')
        return redirect('wallet:dashboard')
    return render(request, 'wallet/add_bitcoin.html')

@login_required
def send_bitcoin(request):
    if request.method == 'POST':
        amount = decimal.Decimal(request.POST.get('amount'))
        address = request.POST.get('address')
        wallet = Wallet.objects.get(user=request.user)
        if wallet.bitcoin_balance >= amount:
            wallet.bitcoin_balance -= amount
            wallet.save()
            Transaction.objects.create(wallet=wallet, amount=-amount, transaction_type='send', transaction_id='external')
            messages.success(request, f'Sent {amount} BTC to {address}.')
        else:
            messages.error(request, 'Insufficient balance.')
        return redirect('wallet:dashboard')
    return render(request, 'wallet/send_bitcoin.html')

@login_required
def buy_bitcoin(request):
    if request.method == 'POST':
        amount_usd = decimal.Decimal(request.POST.get('amount_usd'))
        bitcoin_price = decimal.Decimal(str(get_bitcoin_price()))
        amount_btc = amount_usd / bitcoin_price
        response = gemini_request('/v1/order/new', {
            'symbol': 'btcusd',
            'amount': str(amount_btc),
            'price': str(bitcoin_price),
            'side': 'buy',
            'type': 'exchange limit',
        })
        if 'order_id' in response:
            wallet = Wallet.objects.get(user=request.user)
            wallet.bitcoin_balance += amount_btc
            wallet.save()
            Transaction.objects.create(wallet=wallet, amount=amount_btc, transaction_type='buy', transaction_id=response['order_id'])
            messages.success(request, f'Bought {amount_btc} BTC for ${amount_usd}.')
        else:
            messages.error(request, 'Failed to buy Bitcoin.')
        return redirect('wallet:dashboard')
    return render(request, 'wallet/buy_bitcoin.html')

@login_required
def sell_bitcoin(request):
    if request.method == 'POST':
        amount_btc = decimal.Decimal(request.POST.get('amount_btc'))
        bitcoin_price = decimal.Decimal(str(get_bitcoin_price()))
        amount_usd = amount_btc * bitcoin_price
        response = gemini_request('/v1/order/new', {
            'symbol': 'btcusd',
            'amount': str(amount_btc),
            'price': str(bitcoin_price),
            'side': 'sell',
            'type': 'exchange limit',
        })
        if 'order_id' in response:
            wallet = Wallet.objects.get(user=request.user)
            if wallet.bitcoin_balance >= amount_btc:
                wallet.bitcoin_balance -= amount_btc
                wallet.save()
                Transaction.objects.create(wallet=wallet, amount=-amount_btc, transaction_type='sell', transaction_id=response['order_id'])
                messages.success(request, f'Sold {amount_btc} BTC for ${amount_usd}.')
            else:
                messages.error(request, 'Insufficient balance.')
        else:
            messages.error(request, 'Failed to sell Bitcoin.')
        return redirect('wallet:dashboard')
    return render(request, 'wallet/sell_bitcoin.html')