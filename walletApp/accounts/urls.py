from django.urls import path
from . import views
from .views import CustomLoginView


app_name='accounts'
urlpatterns = [
	path('register/', views.register, name='register'),
	#path('login/', views.login_view, name='login'),
	path('logout/', views.logout_view, name='logout'),
	path('login/', CustomLoginView.as_view(), name='login'),
	path('profile/', views.profile, name='profile')
]