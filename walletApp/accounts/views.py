from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db() # Load the profile instance created by the signal
			user.profile.date_of_birth = form.cleaned_data.get('date_of_birth')
			user.save()

			# Authenticate the user using the correct backend
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user, backend='django.contrib.auth.backends.ModelBackend')

			return redirect('dashboard')
	else:
		form = RegisterForm()
	return render(request, 'accounts/register.html' , {'form': form})

def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username_or_email = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(request, username=username_or_email, password=password)
			if user is not None:
				login(request, user, backend='accounts.backend.EmailOrUsernameModelBackend')
				return redirect('dashboard')
	else:
		form = AuthenticationForm()
	return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
	logout(request)
	return redirect('landing_page')