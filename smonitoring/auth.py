from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User


class Auth(BaseBackend):
	def authenticate(self,request, username=None,password=None):
		try:
			user = User.objects.get(username=username)
			pwd_valid = check_password(password,user.password)
			print(username,pwd_valid)
			if pwd_valid:
				return user
			else:
				return None
		except User.DoesNotExist:
			return None
		
	def get_user(self, user_id):
		try: 
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None

class MyUser(User):
	super(User)
	code = str()
