from django.urls import path
from . import views
from .views import CustomLoginView


app_name='accounts'
urlpatterns = [
	path('register/', views.register, name='register'),
	path('login/', views.login_view, name='login'),
	path('logout/', views.logout_view, name='logout'),
	#path('login/', CustomLoginView.as_view(), name='login'),
	path('profile/', views.profile, name='profile'),
	path('update_email/', views.update_email, name='update_email'),
	path('update_username/', views.update_username, name='update_username'),
	path('update_password/', views.update_password, name='update_password'),
	path('account_settings/', views.account_settings, name='account_settings'),
]