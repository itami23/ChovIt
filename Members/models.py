from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	bio=models.TextField(null=True,blank=True,default="")
	date_of_birth = models.CharField(blank=True,max_length=150)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(blank=True,null=True,upload_to='Profile_pics',default='avatar.svg')
	
	def __str__(self):
		return self.user.username