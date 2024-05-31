from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm


def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username_or_email = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(request, username=username_or_email, password=password)
			if user is not None:
				login(request, user)
				return redirect('dashboard')
	else:
		form = AuthenticationForm()
	return render(request, 'accounts/login.html', {'form': form})

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.profile.date_of_birth = form.cleaned_data.get('date_of_birth')
			user.save()
			login(request, user)
			return redirect('dashboard')
	else:
		form = RegisterForm()
	return render(request, 'accounts/register.html', {'form': form})