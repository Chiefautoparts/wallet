from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date

class RegisterForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(max_length=50, required=True)
	last_name = forms.CharField(max_length=50, required=True)
	date_of_birth = forms.DateField(required=True)

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'date_of_birth', 'password1', 'password2']

	def clean_date_of_birth(self):
		dob = self.cleaned_data['date_of_birth']
		if dob > date.today():
			raise ValidationError("Date of birth cannot be in the future.")
		return dob 