from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model, update_session_auth_hash
from .forms import RegisterForm, CustomAuthenticationForm, UpdateEmailForm, UpdateUsernameForm, CustomPasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView  
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile


User = get_user_model()


@login_required
def update_email(request):
	if request.method == 'POST':
		form = UpdateEmailForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, 'Your email has been updated.')
			return redirect('accounts:profile')
	else:
		form = UpdateEmailForm(instance=request.user)
	return render(request, 'accounts/update_email.html', {'form': form})

@login_required
def update_username(request):
	if request.method == 'POST':
		form = UpdateUsernameForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, 'Your username has beeen updated')
			return redirect('accounts:profile')
	else:
		form = UpdateUsernameForm(instance=request.user)
	return render(request, 'accounts/update_username.html', {'form': form})

@login_required
def update_password(request):
	if request.method == 'POST':
		form = CustomPasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, 'Your password has been updated')
			return redirect('accounts:profile')
	else:
		form = CustomPasswordChangeForm(request.user)
	return render(request, 'accounts/update_password.html', {'form': form})


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

			return redirect('accounts:profile')
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
			return redirect('accounts:profile')
	else:
		form = AuthenticationForm()
	return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
	logout(request)
	return redirect('wallet:dashboard')

def account_settings(request):
	return render(request, 'accounts/account_settings.html')


class CustomLoginView(LoginView):
	authentication_form = CustomAuthenticationForm
	template_name = 'accounts/login.html'
	redirect_authenticated_user = True
	success_url = '/wallet/dashboard/'

@login_required
def profile(request):
	user = request.user
	profile, created = Profile.objects.get_or_create(user=user)
	return redirect('wallet:dashboard')