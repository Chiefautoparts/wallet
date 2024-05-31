from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bitcoin_balance = models.DecimalField(max_digits=16, decimal_places=8, default=0.0)


	def __str__(self):
		return f"{self.user.username}'s Wallet"
		