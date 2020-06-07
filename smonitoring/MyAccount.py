from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

class MyAccount(BaseBackend):
	def authenticate(self,request, username=None,password=None):
		try:
			user = User.objects.get(username=username)
			pwd_valid = check_password(password,user.password)
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
	def change_password(self,request,username,old_password,new_password):
		try:
			user = User.objects.get(username=username)
			pwd_valid = check_password(old_password,user.password)
			if pwd_valid:
				# changing the password
				user.set_password(new_password)
				# saving the change
				user.save()
				# confirm password change success
				return True
			else:
				return False
		except User.DoesNotExist:
			return False
"""
class MyUser(User):
	super(User)
	code = str()
"""
