from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
	def authenticate(self, request, username=None, password=None, **kwargs):
		if username is None:
			username = kwargs.get(User.USERNAME_FIELD)
		if username is None or password is None:
			return
		try:
			if '@' in username:
				user = User.objects.get(email=username)
			else:
				user = User.objects.get(username=username)
		except User.DoesNotExist:
			User().set_password(password)
		else:
			if user.check_password(password) and self.user_can_authenticate(user):
				return user

	def get_user(self, user_id):
		try:
			user = User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None
		return user if self.user_can_authenticate(user) else None