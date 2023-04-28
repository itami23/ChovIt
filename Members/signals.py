from django.db.models.signals import post_save
from .models import *
from django.contrib.auth.models import User

def create_user_profile(sender,instance,created,**kwargs):
	if created : 
		Profile.objects.create(user = instance)


post_save.connect(create_user_profile,User)