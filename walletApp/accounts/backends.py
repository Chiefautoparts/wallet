from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User 

class EmailOrUsernameModelBackend(ModelBackend):
	def authenticate(self, request, username=None, password=None, **kwargs):
		if '@' in username:
			kwargs = {'email': username}
		else:
			kwargs = {'username': username}
		try:
			user = User.objects.get(**kwargs)
			if user.check_password(password):
				return user
		except user.DoesNotExist:
			return None

	def get_user(self, user_id):
		try:
			return user.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None