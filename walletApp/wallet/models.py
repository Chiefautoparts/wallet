from django.db import models
from django.contrib.auth.models import User
import uuid

class Wallet(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bitcoin_balance = models.DecimalField(max_digits=16, decimal_places=8, default=0.0)
	blockchain_address = models.CharField(max_length=64, unique=True, blank=True, null=True)


	def __str__(self):
		return f"{self.user.username}'s Wallet"

	def generate_blockchain_address(self):
		return uuid.uuid().hex
		
class Transaction(models.Model):
	wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
	amount = models.DecimalField(max_digits=16, decimal_places=8)
	transaction_type = models.CharField(max_length=20)
	transaction_id = models.CharField(max_length=64)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.transaction_type} - {self.amount} BTC on {self.date}"