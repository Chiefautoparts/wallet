from django.urls import path
from . import views


app_name='wallet'
urlpatterns = [
	path('dashboard/', views.dashboard, name='dashboard'),
	path('create_wallet/', views.create_wallet, name='create_wallet'),
	path('add_bitcoin/', views.add_bitcoin, name='add_bitcoin'),
	path('send_bitcoin/', views.send_bitcoin, name='send_bitcoin'),
	path('sell_bitcoin/', views.sell_bitcoin, name='sell_bitcoin'),
	path('buy_bitcoin/', views.buy_bitcoin, name='buy_bitcoin'),
]